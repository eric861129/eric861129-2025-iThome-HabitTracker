#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from app.models import db, MoodLog
from datetime import datetime

# 這裡我們將會硬編碼 user_id = 1 作為範例，以簡化認證流程
TEMP_USER_ID = 1

moods_bp = Blueprint('moods_bp', __name__)

# 記錄或更新指定日期的心情
@moods_bp.route('/moods', methods=['POST'])
def log_mood():
    """記錄或更新指定日期的心情"""
    data = request.get_json()
    if not data or not 'mood_level' in data or not 'date' in data:
        return jsonify({'message': 'Missing mood_level or date'}), 400

    try:
        log_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD.'}), 400

    # 檢查該使用者當天是否已有紀錄 (Upsert 邏輯)
    mood_log = MoodLog.query.filter_by(user_id=TEMP_USER_ID, date=log_date).first()

    if mood_log:
        # 更新現有紀錄
        mood_log.mood_level = data['mood_level']
        mood_log.notes = data.get('notes', mood_log.notes)
        status_code = 200 # OK
    else:
        # 建立新紀錄
        mood_log = MoodLog(
            user_id=TEMP_USER_ID,
            mood_level=data['mood_level'],
            date=log_date,
            notes=data.get('notes')
        )
        db.session.add(mood_log)
        status_code = 201 # Created
    
    db.session.commit()

    return jsonify({
        'id': mood_log.id,
        'user_id': mood_log.user_id,
        'mood_level': mood_log.mood_level,
        'date': mood_log.date.isoformat(),
        'notes': mood_log.notes
    }), status_code