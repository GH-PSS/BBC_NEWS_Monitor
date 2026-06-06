# github-trending-monitor

GitHubのTrendingページを自動取得し、Excelに保存・Discordに上位5件を通知するツールです。

## 機能

- GitHub Trendingページのスクレイピング
- リポジトリ名・説明・言語・本日のスター数を取得
- Excel（.xlsx）への保存
- スター数上位5件をDiscordへ通知

## 必要なライブラリ

```
pip install requests beautifulsoup4 pandas openpyxl python-dotenv
```

## セットアップ

1. リポジトリをクローン
2. `.env` ファイルを作成し、以下を記入
3. `DISCORD_WEBHOOK_URL=あなたのWebhookURL`
4. 実行： `python github_trending.py`

## 出力

- `github_trending.xlsx` — 全件をExcelに保存
- Discord — スター数上位5件を通知
