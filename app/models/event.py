from app import db
from datetime import datetime


class Event(db.Model):
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
        super(Event, self).__init__(*args, **kwargs)
        if self.start and self.end and self.start > self.end:
            raise ValueError("終了時間は開始時間より後でなければなりません")
