#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from app.models import db, User, Habit, HabitTracking, MoodLog
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# 這裡我們將會硬編碼 user_id = 1 作為範例，以簡化認證流程
# 在一個完整的應用中，這裡應該是透過解析 JWT token 來取得當前使用者
TEMP_USER_ID = 1

habits_bp = Blueprint('habits_bp', __name__)

# 取得所有習慣
@habits_bp.route('/habits', methods=['GET'])
def get_habits():
    """取得當前使用者的所有習慣"""
    habits = Habit.query.filter_by(user_id=TEMP_USER_ID).all()
    return jsonify([{
        'id': habit.id,
        'name': habit.name,
        'type': habit.type,
        'created_at': habit.created_at.isoformat()
    } for habit in habits])

# 建立新習慣
@habits_bp.route('/habits', methods=['POST'])
def create_habit():
    """建立一個新習慣"""
    data = request.get_json()
    if not data or not 'name' in data or not 'type' in data:
        return jsonify({'message': 'Missing name or type'}), 400

    new_habit = Habit(
        user_id=TEMP_USER_ID,
        name=data['name'],
        type=data['type']
    )
    db.session.add(new_habit)
    db.session.commit()

    return jsonify({
        'id': new_habit.id,
        'name': new_habit.name,
        'type': new_habit.type,
        'created_at': new_habit.created_at.isoformat()
    }), 201

# 透過 ID 取得特定習慣
@habits_bp.route('/habits/<int:habitId>', methods=['GET'])
def get_habit_by_id(habitId):
    """透過 ID 取得特定習慣"""
    habit = Habit.query.filter_by(id=habitId, user_id=TEMP_USER_ID).first()
    if not habit:
        return jsonify({'message': 'Habit not found'}), 404
    
    return jsonify({
        'id': habit.id,
        'name': habit.name,
        'type': habit.type,
        'created_at': habit.created_at.isoformat()
    })

# 更新一個現有的習慣
@habits_bp.route('/habits/<int:habitId>', methods=['PUT'])
def update_habit(habitId):
    """更新一個現有的習慣"""
    habit = Habit.query.filter_by(id=habitId, user_id=TEMP_USER_ID).first()
    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    data = request.get_json()
    habit.name = data.get('name', habit.name)
    habit.type = data.get('type', habit.type)
    db.session.commit()

    return jsonify({
        'id': habit.id,
        'name': habit.name,
        'type': habit.type,
        'created_at': habit.created_at.isoformat()
    })

# 刪除一個習慣
@habits_bp.route('/habits/<int:habitId>', methods=['DELETE'])
def delete_habit(habitId):
    """刪除一個習慣"""
    habit = Habit.query.filter_by(id=habitId, user_id=TEMP_USER_ID).first()
    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    db.session.delete(habit)
    db.session.commit()
    return '', 204