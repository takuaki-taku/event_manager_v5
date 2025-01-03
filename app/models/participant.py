from app import db


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
