from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    """
    User model for storing user information.
    """

    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))  # Increased column size for password hash
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """
        パスワードをハッシュ化して保存します。
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        渡されたパスワードが、保存されているハッシュ化されたパスワードと一致するかどうかを確認します。

        Args:
            password: チェックするパスワード

        Returns:
            パスワードが一致する場合はTrue、そうでない場合はFalse
        """
        return check_password_hash(self.password_hash, password)
