# 引入 Flask 框架
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
import datetime

# --- 應用程式設定 ---
# 建立 Flask 應用程式實例
app = Flask(__name__)

# 設定資料庫連線：指定使用 SQLite，資料庫檔案為 database.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 選擇性：關閉不必要的效能通知

# 建立資料庫操作對象
db = SQLAlchemy(app)


# --- 資料庫模型定義 ---

# 使用者模型
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # 建立關聯
    settings = db.relationship('UserSetting', backref='user', uselist=False, cascade="all, delete-orphan")
    habits = db.relationship('Habit', backref='user', lazy=True, cascade="all, delete-orphan")
    mood_logs = db.relationship('MoodLog', backref='user', lazy=True, cascade="all, delete-orphan")

# 使用者設定模型
class UserSetting(db.Model):
    __tablename__ = 'user_settings'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    enable_reminders = db.Column(db.Boolean, nullable=False, default=True)
    reminder_time = db.Column(db.String(5), nullable=False, default='21:00') # HH:MM

# 習慣模型
class Habit(db.Model):
    __tablename__ = 'habits'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    frequency_type = db.Column(db.String(20), nullable=False, default='daily') # e.g., 'daily', 'weekly'
    frequency_value = db.Column(db.String(50), nullable=True) # e.g., '1,3,5' for weekly
    created_at = db.Column(db.DateTime, nullable=False, server_default=func.now())

    # 建立關聯
    logs = db.relationship('HabitLog', backref='habit', lazy=True, cascade="all, delete-orphan")

# 習慣打卡紀錄模型
class HabitLog(db.Model):
    __tablename__ = 'habit_logs'
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    log_date = db.Column(db.Date, nullable=False, default=datetime.date.today)
    notes = db.Column(db.Text, nullable=True)

# 心情紀錄模型
class MoodLog(db.Model):
    __tablename__ = 'mood_logs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    mood_score = db.Column(db.Integer, nullable=False) # e.g., 1-5
    notes = db.Column(db.Text, nullable=True)
    log_date = db.Column(db.Date, nullable=False, default=datetime.date.today)


# --- 路由定義 ---
# 定義根路由 ('/')
@app.route('/')
def hello_world():
    """
    當使用者訪問網站根目錄時，回傳一個簡單的歡迎訊息。
    """
    return 'Hello, World!'

# --- 啟動伺服器 ---
# Python 的主程式進入點
if __name__ == '__main__':
    """
    如果這個腳本是直接被執行的 (而不是被其他腳本引入的)，
    則啟動 Flask 內建的開發伺服器。
    debug=True 會在程式碼變更時自動重載，並提供詳細的錯誤訊息。
    """
    app.run(debug=True)