import os
from flask import Blueprint, request, jsonify, session
import subprocess
from utils.common import connect_pgdb

settings_bp = Blueprint('settings_bp', __name__)

@settings_bp.route('/', methods=['GET', 'POST'])
def settings():
    if 'user' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
        
    try:
        cursor = connect_pgdb()
        user_id = session['user'].get('userid')
        
        if request.method == 'POST':
            data = request.get_json()
            
            # Update each setting with user ID
            for key, value in data.items():
                cursor.execute(
                    "CALL stp_update_setting(%s, %s, %s);",
                    (key, str(value), user_id)
                )
            cursor.connection.commit()
            return jsonify({'status': 'ok'})
            
        # GET - fetch user specific settings
        cursor.execute("SELECT * FROM stp_get_settings(%s);", (user_id,))
        settings = dict(cursor.fetchall())
        
        # Return settings with defaults if not set
        return jsonify({
            'itemsPerPage': settings.get('itemsPerPage', '10'),
            'theme': settings.get('theme', 'light'),
            'aiProvider': settings.get('aiProvider', 'openai')
        })
        
    except Exception as e:
        if cursor:
            cursor.connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor:
            cursor.close()

@settings_bp.route('/ollama/models', methods=['GET'])
def ollama_models():
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, check=True)
        models = []
        for line in result.stdout.splitlines():
            parts = line.strip().split()
            if parts and parts[0] != 'NAME':
                models.append(parts[0])
        return jsonify({'models': models})
    except Exception as e:
        return jsonify({'models': [], 'error': str(e)}), 500
