#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Blueprint, jsonify, request
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth_bp', __name__)

# 註冊新使用者
@auth_bp.route('/register', methods=['POST'])
def register():
    """註冊新使用者"""
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Missing email or password'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'message': 'Email already registered'}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(email=data['email'], password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        'id': new_user.id,
        'email': new_user.email,
        'created_at': new_user.created_at.isoformat()
    }), 201

# 使用者登入
@auth_bp.route('/login', methods=['POST'])
def login():
    """使用者登入"""
    data = request.get_json()
    if not data or not 'email' in data or not 'password' in data:
        return jsonify({'message': 'Missing email or password'}), 400

    user = User.query.filter_by(email=data['email']).first()

    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    # 在真實應用中，這裡會生成並返回一個 JWT token
    return jsonify({'token': 'fake-jwt-token-for-now-user-' + str(user.id)})