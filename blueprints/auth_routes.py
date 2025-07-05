from flask import Blueprint, jsonify, request, session, redirect, url_for
from functools import wraps
import hashlib
from utils.common import connect_pgdb

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

    try:
        cursor = connect_pgdb()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Call login procedure
        cursor.execute("""
            CALL stp_user_login(%s, %s, NULL, NULL, NULL);
            """, (email, hashed_password))
        
        result = cursor.fetchone()
        if result and result[0]:  # Check success flag
            session['user'] = {
                'email': result[1],
                'role': result[2]
            }
            
            if remember_me:
                session.permanent = True
                
            return jsonify({'message': 'Login successful'})
            
        return jsonify({'message': 'Invalid email or password'}), 401
        
    except Exception as e:
        return jsonify({'message': f'Login failed: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()

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

    try:
        cursor = connect_pgdb()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Insert new user
        cursor.execute("""
            INSERT INTO tbl_Users (Email, Password, Username)
            VALUES (%s, %s, %s)
            """, (email, hashed_password, email.split('@')[0]))
            
        cursor.connection.commit()
        return jsonify({'message': 'Account created successfully'})
        
    except Exception as e:
        cursor.connection.rollback()
        if 'uq_users_email' in str(e):
            return jsonify({'message': 'Email already registered'}), 400
        return jsonify({'message': f'Registration failed: {str(e)}'}), 500
    finally:
        if cursor:
            cursor.close()
