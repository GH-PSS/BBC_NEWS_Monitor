# BBC News Monitor
## 概要
選択したジャンルのBBCニュースを自動取得し、Discordへ通知・OneDriveへ保存するツールです。ダウンロードしておけばオフラインでも閲覧できます。
## 機能

ジャンルを選択して最新記事を取得（複数選択・追加・やり直し対応）
選択ジャンルをconfig.jsonに保存し、次回以降は設定を引き継ぎ
最新5件をDiscordに通知
HTML形式でOneDriveに保存（オフライン閲覧対応）
Excel形式でも保存

## 必要なセットアップ
pip install requests beautifulsoup4 pandas openpyxl python-dotenv
.envファイルを作成し、以下を記入してください。
DISCORD_WEBHOOK_URL=あなたのWebhookURL
## 使い方
python bbc_news_monitor.py
実行するとジャンル選択画面が表示されます。番号をカンマ区切りで入力してください。
## 出力

Discord：選択ジャンルごとに最新5件を通知
OneDrive：HTML・Excel形式で保存
