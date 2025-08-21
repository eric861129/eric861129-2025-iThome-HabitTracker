from app import create_app, db
from app.models import User, Habit, HabitTracking, MoodLog
from werkzeug.security import generate_password_hash
from datetime import date, timedelta

app = create_app()

with app.app_context():
    print("Seeding database with sample data...")

    # Clean up existing data
    db.session.query(HabitTracking).delete()
    db.session.query(MoodLog).delete()
    db.session.query(Habit).delete()
    db.session.query(User).delete()
    db.session.commit()
    print("Cleaned up old data.")

    # 1. Create a sample user
    user1 = User(
        email='testuser@example.com',
        password_hash=generate_password_hash('password123', method='pbkdf2:sha256')
    )
    db.session.add(user1)
    db.session.commit()
    print(f"Created user: {user1.email}")

    # 2. Create some habits for the user
    habit1 = Habit(user_id=user1.id, name="每天運動 30 分鐘", type="positive")
    habit2 = Habit(user_id=user1.id, name="閱讀 10 頁書", type="positive")
    habit3 = Habit(user_id=user1.id, name="吃宵夜", type="negative")
    db.session.add_all([habit1, habit2, habit3])
    db.session.commit()
    print(f"Created habits: {[h.name for h in [habit1, habit2, habit3]]}")

    # 3. Create mood logs and habit trackings for the past 7 days
    today = date.today()
    for i in range(7):
        current_date = today - timedelta(days=i)
        
        # Log mood for the day (cycling through 3, 4, 5)
        mood = MoodLog(user_id=user1.id, mood_level=(i % 3) + 3, date=current_date)
        db.session.add(mood)

        # Log habit trackings
        # Day 0 (today): track habit 1 & 2
        if i == 0:
            db.session.add(HabitTracking(habit_id=habit1.id, date=current_date))
            db.session.add(HabitTracking(habit_id=habit2.id, date=current_date))
        # Day 1: track habit 1 & 3 (negative)
        elif i == 1:
            db.session.add(HabitTracking(habit_id=habit1.id, date=current_date))
            db.session.add(HabitTracking(habit_id=habit3.id, date=current_date))
        # Day 2, 3, 4: track habit 1
        elif i in [2, 3, 4]:
            db.session.add(HabitTracking(habit_id=habit1.id, date=current_date))
        # Day 5, 6: track habit 2
        elif i in [5, 6]:
            db.session.add(HabitTracking(habit_id=habit2.id, date=current_date))

    db.session.commit()
    print("Seeded mood logs and habit trackings for the past 7 days.")

    print("\nSeed data has been successfully added to the database.")
