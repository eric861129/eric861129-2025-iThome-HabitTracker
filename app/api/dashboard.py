#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify
from app.models import Habit, MoodLog, HabitTracking
from datetime import date, timedelta

# 這裡我們將會硬編碼 user_id = 1 作為範例，以簡化認證流程
TEMP_USER_ID = 1

dashboard_bp = Blueprint('dashboard_bp', __name__)

@dashboard_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """
    取得儀表板所需的整合數據
    - 使用者的所有習慣
    - 最近30天的心情紀錄
    - 最近30天的習慣打卡紀錄
    """
    end_date = date.today()
    start_date = end_date - timedelta(days=29)

    # 1. 取得使用者的所有習慣
    habits = Habit.query.filter_by(user_id=TEMP_USER_ID).all()
    habits_data = [{
        'id': habit.id,
        'name': habit.name,
        'type': habit.type
    } for habit in habits]

    # 2. 取得最近30天的心情紀錄
    mood_logs = MoodLog.query.filter(
        MoodLog.user_id == TEMP_USER_ID,
        MoodLog.date >= start_date,
        MoodLog.date <= end_date
    ).all()
    mood_logs_data = [{
        'date': log.date.isoformat(),
        'mood_level': log.mood_level
    } for log in mood_logs]

    # 3. 取得最近30天的習慣打卡紀錄
    habit_trackings = HabitTracking.query.join(Habit).filter(
        Habit.user_id == TEMP_USER_ID,
        HabitTracking.date >= start_date,
        HabitTracking.date <= end_date
    ).all()
    habit_trackings_data = [{
        'date': tracking.date.isoformat(),
        'habit_id': tracking.habit_id
    } for tracking in habit_trackings]

    return jsonify({
        'habits': habits_data,
        'mood_logs': mood_logs_data,
        'habit_trackings': habit_trackings_data,
        'start_date': start_date.isoformat(),
        'end_date': end_date.isoformat()
    })
