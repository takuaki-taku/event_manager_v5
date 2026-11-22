from app import create_app, db
from app.models import Event, User
from datetime import datetime, timedelta
import os

def seed_demo_data():
    app = create_app()
    with app.app_context():
        # 管理者ユーザーを取得
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Admin user not found. Please create admin user first.")
            return

        # 既存のイベントを少し残しつつ、新しいデモデータを追加
        today = datetime.now().replace(hour=10, minute=0, second=0, microsecond=0)
        
        demo_events = [
            {"title": "Morning Pickleball Session", "start": today + timedelta(days=1), "end": today + timedelta(days=1, hours=2), "location": "Court A", "color": "#3788d8"},
            {"title": "Beginner Training", "start": today + timedelta(days=2), "end": today + timedelta(days=2, hours=1.5), "location": "Court B", "color": "#28a745"},
            {"title": "Weekend Tournament", "start": today + timedelta(days=3, hours=4), "end": today + timedelta(days=3, hours=8), "location": "Main Arena", "color": "#dc3545"},
            {"title": "Evening Practice", "start": today - timedelta(days=1), "end": today - timedelta(days=1, hours=-2), "location": "Court A", "color": "#ffc107"},
            {"title": "Advanced Drills", "start": today + timedelta(days=5), "end": today + timedelta(days=5, hours=2), "location": "Court C", "color": "#6f42c1"},
        ]

        for data in demo_events:
            event = Event(
                title=data['title'],
                start=data['start'],
                end=data['end'],
                location=data['location'],
                color=data['color'],
                created_by=admin.id
            )
            db.session.add(event)
        
        db.session.commit()
        print("Successfully added 5 demo events!")

if __name__ == "__main__":
    seed_demo_data()
