import os
from app import create_app

# 環境変数 FLASK_ENV が production に設定されている場合は、production 設定を使用する
config_name = os.environ.get("FLASK_ENV", "development")
if config_name == "production":
    application = create_app(config_name="production")
else:
    application = create_app()


if __name__ == "__main__":
    application.run()
