from flask import Blueprint, jsonify, request, session
from functools import wraps
import hashlib
import os

auth_bp = Blueprint('auth', __name__)

# Simple user store - replace with database in production
USERS = {
    'admin@example.com': {
        'password': hashlib.sha256('admin123'.encode()).hexdigest(),
        'role': 'admin'
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    remember_me = data.get('rememberMe', False)

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    user = USERS.get(email)
    if not user or user['password'] != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({'message': 'Invalid email or password'}), 401

    session['user'] = {
        'email': email,
        'role': user['role']
    }
    
    if remember_me:
        session.permanent = True

    return jsonify({'message': 'Login successful'})

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logout successful'})

@auth_bp.route('/check-auth', methods=['GET'])
def check_auth():
    if 'user' in session:
        return jsonify({'authenticated': True, 'user': session['user']})
    return jsonify({'authenticated': False}), 401
