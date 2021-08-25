クラウドソーシングCrawler
====

# フォルダ説明
- main/ Crawlerを起動するためのファイルを格納
- models/ DB連携用
- commands/ コマンド系処理を記述
- common/ 共通処理
- config/ 共通設定
- docker/ docker用
- .env.develop 開発環境用の環境変数

# 環境構築
- .env.develop → .envにリネーム
- venvの作成
- requirements.txtのインストール
- docker-composeを実行しMySQLコンテナを起動する
```
新しいターミナルを開く
cd docker
docker-compose up --build
```

# 実行方法
```
python main/lancers_crawler.py
```