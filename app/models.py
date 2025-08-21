from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    habits = db.relationship('Habit', backref='user', lazy=True)
    mood_logs = db.relationship('MoodLog', backref='user', lazy=True)

class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # e.g., 'positive', 'negative'
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    trackings = db.relationship('HabitTracking', backref='habit', lazy=True, cascade="all, delete-orphan")

class HabitTracking(db.Model):
    __tablename__ = 'habit_trackings'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text, nullable=True)

class MoodLog(db.Model):
    __tablename__ = 'mood_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_level = db.Column(db.Integer, nullable=False) # 1-5 scale
    notes = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, nullable=False)
