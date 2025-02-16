# ベースイメージ
FROM python:3.10-slim

# 作業ディレクトリを設定
WORKDIR /app

# アプリケーションのルートディレクトリ全体をコピー
COPY . .

# 依存関係をインストール
RUN pip install --no-cache-dir -r requirements.txt

# Flask-Migrate を使用したデータベースのマイグレーションとアプリの起動
CMD ["sh", "-c", "flask db upgrade && gunicorn --bind 0.0.0.0:5000 --workers 2 wsgi:application"]