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


class Event(db.Model):
    """
    Event model for storing event information.
    """

    __tablename__ = "event"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(255))
    color = db.Column(db.String(20), default="#3788d8")
    created_by = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    created_by_user = db.relationship("User", backref="events")

    def __init__(self, *args, **kwargs):
        """
        Initialize the Event object and validate start and end times.
        """
        super(Event, self).__init__(*args, **kwargs)
        if self.start and self.end and self.start > self.end:
            raise ValueError("終了時間は開始時間より後でなければなりません")

    def __repr__(self):
        """
        String representation of the Event object.
        """
        return f"<Event {self.title} ({self.start} - {self.end})>"


class Participant(db.Model):
    """
    Participant model for storing event participation information.
    """

    __tablename__ = "participant"
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(20), default="未定")

    event = db.relationship("Event", backref="participants")
    user = db.relationship("User", backref="participations")

    def __repr__(self):
        """
        String representation of the Participant object.
        """
        return (
            f"<Participant {self.user.username} - {self.event.title} ({self.status})>"
        )
