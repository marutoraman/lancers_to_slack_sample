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
- VSCODEにmysql拡張機能をインストールする<BR>
![mysql]("https://i.gyazo.com/a2c3368fe9def84a2bfdad92b8e123f8.png")
- docker-composeを実行しMySQLコンテナを起動する(dockerは事前にインストールしておくこと)
```
新しいターミナルを開く
cd docker
docker-compose up --build
```
- データベースMigrate
以下コマンドを実行し、DBにテーブルが作成されていればOK
```
python commands/migrate.py
```
- mysql拡張機能の接続情報を以下の通りに追加してDBを確認する（Add Connectionより追加できる）
```
Host: localhost
Port: 4444
Username: docker
Password: docker
```

# 実行方法
```
python main/lancers_crawler.py
```