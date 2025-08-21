#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from app.models import db, Habit, HabitTracking
from datetime import datetime

# 這裡我們將會硬編碼 user_id = 1 作為範例，以簡化認證流程
TEMP_USER_ID = 1

trackings_bp = Blueprint('trackings_bp', __name__)

# 為指定日期建立一筆習慣打卡紀錄
@trackings_bp.route('/habit-trackings', methods=['POST'])
def log_habit_tracking():
    """為指定日期建立一筆習慣打卡紀錄"""
    data = request.get_json()
    if not data or not 'habit_id' in data or not 'date' in data:
        return jsonify({'message': 'Missing habit_id or date'}), 400

    # 檢查習慣是否存在且屬於當前使用者
    habit = Habit.query.filter_by(id=data['habit_id'], user_id=TEMP_USER_ID).first()
    if not habit:
        return jsonify({'message': 'Habit not found or not owned by user'}), 404

    try:
        tracking_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # 檢查該習慣當天是否已經打卡
    existing_tracking = HabitTracking.query.filter_by(habit_id=data['habit_id'], date=tracking_date).first()
    if existing_tracking:
        return jsonify({'message': 'Habit already tracked for this date'}), 400

    new_tracking = HabitTracking(
        habit_id=data['habit_id'],
        date=tracking_date,
        notes=data.get('notes')
    )
    db.session.add(new_tracking)
    db.session.commit()

    return jsonify({
        'id': new_tracking.id,
        'habit_id': new_tracking.habit_id,
        'date': new_tracking.date.isoformat(),
        'notes': new_tracking.notes
    }), 201
