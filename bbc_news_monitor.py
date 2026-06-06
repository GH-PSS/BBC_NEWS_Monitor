import requests
import xml.etree.ElementTree as ET
import pandas as pd
from bs4 import BeautifulSoup  
from dotenv import load_dotenv
import os
import shutil
import json

def select_genres():
    number_to_genre = {
        "1": "uk", "2": "world", "3": "business",
        "4": "technology", "5": "science",
        "6": "entertainment", "7": "health"
    }
    print("取得するジャンルを選んでください（複数可、カンマ区切り）")
    print("1: UK\n2: World\n3: Business\n4: Technology\n5: Science\n6: Entertainment\n7: Health\n8: 全て")
    while True:
        selected = input("番号を入力: ")
        numbers = [n.strip() for n in selected.split(",")]
        if "8" in numbers:
            return list(number_to_genre.values())
        genres = [number_to_genre[n] for n in numbers if n in number_to_genre]
        if genres:
            return genres
        print("適切に入力してください")

if os.path.exists("config.json"):
    print("このまま実行しますか，それともジャンルを編集しますか")
    print("1: このまま実行\n2: ジャンルを選びなおす\n3: ジャンルを追加する")
    while True:
        selected = input("番号を入力: ")
        if selected == "1":
            with open("config.json", "r") as f:
                config = json.load(f)
                break
        elif selected == "2":
            new_genres = select_genres()
            config = {"genres": new_genres}
            with open("config.json", "w") as f:
                json.dump(config, f)
                break

        elif selected == "3":
            with open("config.json", "r") as f:
                config = json.load(f)
            new_genres = select_genres()
            config["genres"] = list(set(config["genres"] + new_genres))
            with open("config.json", "w") as f:
                json.dump(config, f)
                break     

        print("1,2,3のいずれかを入力してください")

else:
    new_genres = select_genres()
    config = {"genres": new_genres}
    with open("config.json", "w") as f:
        json.dump(config, f)
        
    
load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

# ① RSSフィード取得
all_feeds = {
    "uk": "https://feeds.bbci.co.uk/news/uk/rss.xml",
    "world": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "business": "https://feeds.bbci.co.uk/news/business/rss.xml",
    "technology": "https://feeds.bbci.co.uk/news/technology/rss.xml",
    "science": "https://feeds.bbci.co.uk/news/science_and_environment/rss.xml",
    "entertainment": "https://feeds.bbci.co.uk/news/entertainment_and_arts/rss.xml",
    "health": "https://feeds.bbci.co.uk/news/health/rss.xml",
}

feeds = {genre: all_feeds[genre] for genre in config["genres"]}
    


for genre, url in feeds.items():
    response = requests.get(url)
    root = ET.fromstring(response.content)
# ② 記事を取り出す
    data = []
    for item in root.findall(".//item"):
        title = item.find("title").text
        pubDate = item.find("pubDate").text
        link = item.find("link").text
        try:
            article_response = requests.get(link, timeout=5)
            article_soup = BeautifulSoup(article_response.text, "html.parser")
            paragraphs = article_soup.find_all("p")
            body = "\n".join(p.get_text() for p in paragraphs)
        except Exception as e:
            body = f"本文取得失敗: {e}"
        data.append({"タイトル": title, "日時": pubDate, "URL": link, "本文": body})

# ③ DataFrame変換・Excel保存
    df = pd.DataFrame(data)
    df.to_excel(f"bbc_news_{genre}.xlsx", index=False)
    print("Excel保存完了")

# ④ 上位5件をDiscord通知
    message_lines = [f"**📰 BBC News {genre} 最新5件**\n"]
    for row in data[:5]:
        message_lines.append(
            f"📌 {row['タイトル']}\n"
            f"🕒 {row['日時']}\n"
            f"🔗 {row['URL']}\n"
        )
    message = {"content": "\n".join(message_lines)}
    result = requests.post(WEBHOOK_URL, json=message)
    if result.status_code == 204:
        print("Discord通知 成功")
    else:
        print(f"失敗: {result.status_code}")

# ⑤ テキストファイル保存（本文も格納）
    with open(f"bbc_news_{genre}.html", "w", encoding="utf-8") as f:
        f.write("<html><body>\n")
        for row in data:
            f.write(f"<h2>{row['タイトル']}</h2>\n")
            f.write(f"<p>{row['日時']}</p>\n")
            f.write(f"<p>{row['本文']}</p>\n")
            f.write(f'<a href="{row["URL"]}">記事を読む</a>\n\n')
            f.write("<hr>\n")
        f.write("</body></html>\n")
        print("HTML保存完了")

# ⑥ OneDriveへコピー保存

    onedrive_path = os.path.expanduser("~/OneDrive/bbc_news")
    os.makedirs(onedrive_path, exist_ok=True)
    shutil.copy(f"bbc_news_{genre}.html", os.path.join(onedrive_path, f"bbc_news_{genre}.html"))
    shutil.copy(f"bbc_news_{genre}.xlsx", os.path.join(onedrive_path, f"bbc_news_{genre}.xlsx"))
    print("OneDrive保存完了")




