# イベント管理アプリケーション

## 概要

このアプリケーションは、イベントの作成、管理、参加者の追跡を行うためのウェブベースのツールです。Flask、SQLAlchemy、FullCalendar、Google Spreadsheet APIを使用して構築されており、ユーザー認証、イベントのCRUD操作、参加者管理機能、イベントの一括作成機能を提供します。また、日本語と英語の言語設定をサポートしています。

## 機能

- ユーザー認証（登録、ログイン、ログアウト）
- イベントの作成、読み取り、更新、削除（CRUD）
- カレンダーベースのイベント表示
- イベントへの参加登録と参加状況の管理
- 管理者ユーザーによるイベント管理
- Google Spreadsheetを使用したイベントの一括作成
- 日本語・英語の言語切り替え

## セットアップ

1. リポジトリをクローンします：

   ```
   git clone https://github.com/takuaki-taku/pickle_attendance.git
   ```

2. 仮想環境を作成し、アクティベートします：

   ```
   python -m venv .venv
   source .venv/bin/activate  # Windowsの場合: venv\Scripts\activate
   ```

3. 必要なパッケージをインストールします：

   ```
   pip install -r requirements.txt
   ```

4. 環境変数を設定します：

   ```
   export SECRET_KEY=your_secret_key_here
   export FLASK_APP=app.py
   export FLASK_ENV=development
   export GOOGLE_SHEETS_CREDS_JSON='{"your": "credentials", "json": "here"}'
   ```

   Windowsの場合：

   ```
   set SECRET_KEY=your_secret_key_here
   set FLASK_APP=app.py
   set FLASK_ENV=development
   set GOOGLE_SHEETS_CREDS_JSON={"your": "credentials", "json": "here"}
   ```

5. データベースを初期化します：

   ```
   flask db upgrade
   ```

6. アプリケーションを実行します：

   ```
   flask run
   ```

   アプリケーションは http://localhost:5000 で実行されます。

## 使用方法

1. ブラウザで http://localhost:5000 にアクセスします。
2. 新規ユーザーの場合は登録を行い、既存ユーザーの場合はログインします。
3. ホームページでカレンダーを表示し、イベントを閲覧します。
4. 管理者ユーザーは新しいイベントを作成、編集、削除できます。
5. 一般ユーザーはイベントの詳細を確認し、参加状況を更新できます。
6. 管理者ユーザーは「イベント一括作成」ページでGoogle Spreadsheetからイベントデータを取得し、一括でイベントを作成できます。
7. 画面右上の言語切り替えボタンで、日本語と英語を切り替えることができます。

## Google Spreadsheet APIのセットアップ

1. Google Cloud Consoleで新しいプロジェクトを作成します。
2. Google Sheets APIを有効にします。
3. サービスアカウントを作成し、JSONキーをダウンロードします。
4. ダウンロードしたJSONキーの内容を環境変数`GOOGLE_SHEETS_CREDS_JSON`に設定します。

## 管理者アカウントの作成

初期の管理者アカウントを作成するには、以下の手順を実行します：

1. Pythonインタラクティブシェルを開きます：

   ```
   python
   ```

2. 以下のコードを実行して管理者ユーザーを作成します：

   ```python
   from app import app, db, User
   with app.app_context():
       admin = User(username='admin', is_admin=True)
       admin.set_password('your_admin_password')
       db.session.add(admin)
       db.session.commit()
   ```

   [仮でアカウントが登録されています。]
   管理者アカウント

   ユーザー名　東
   パスワード　tennispickle

   一般ユーザー
   
   ユーザー名　sample
   パスワード　sample

3. これで管理者としてもログインできます。

## ライセンス

このプロジェクトは MIT ライセンスの下で公開されています。詳細については、[LICENSE](LICENSE) ファイルを参照してください。

## 貢献

プロジェクトへの貢献を歓迎します。問題を報告したり、プルリクエストを送信したりする場合は、GitHub リポジトリの Issues セクションをご利用ください。

## サポート

質問やサポートが必要な場合は、GitHub の Issues セクションに投稿するか、[tatennisku@gmail.com] までメールでお問い合わせください。