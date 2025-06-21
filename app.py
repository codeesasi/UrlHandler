from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from blueprints.url_routes import url_bp
from blueprints.queue_routes import queue_bp
from blueprints.auth_routes import auth_bp, login_required
from utils.file_handlers import init_data_files
from clipboard_monitor import start_monitoring
import logging
import secrets
from datetime import timedelta

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Add secret key for session management
app.secret_key = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Register blueprints
app.register_blueprint(url_bp, url_prefix='/api/urls')
app.register_blueprint(queue_bp, url_prefix='/api/queue')
app.register_blueprint(auth_bp, url_prefix='/api/auth')

# Initialize data files
init_data_files()

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # If user is already logged in, redirect to home
    if 'user' in session:
        return redirect(url_for('index'))
    # Pass the next parameter to the template
    next_url = request.args.get('next', '')
    return render_template('login.html', next_url=next_url)

if __name__ == '__main__':
    start_monitoring()
    app.run(debug=True, port=4000, host='localhost')
