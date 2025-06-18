from flask import Blueprint, jsonify, request, session, redirect, url_for
from functools import wraps
from utils.file_handlers import read_users, write_users
import hashlib

auth_bp = Blueprint('auth', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            # Check if it's an API request (starts with /api)
            if request.path.startswith('/api/'):
                return jsonify({'message': 'Unauthorized'}), 401
            # For regular page requests, redirect to login
            return redirect(url_for('login'))
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

    users = read_users()
    user = users.get(email)
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

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'message': 'Missing email or password'}), 400

    users = read_users()
    if email in users:
        return jsonify({'message': 'Email already registered'}), 400

    # Hash the password and store new user
    users[email] = {
        'password': hashlib.sha256(password.encode()).hexdigest(),
        'role': 'user'
    }
    write_users(users)

    return jsonify({'message': 'Account created successfully'})
