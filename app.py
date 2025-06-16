from flask import Flask, render_template
from blueprints.url_routes import url_bp
from blueprints.queue_routes import queue_bp
from utils.file_handlers import init_data_files
from clipboard_monitor import start_monitoring
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
app.logger.setLevel(logging.DEBUG)

# Register blueprints
app.register_blueprint(url_bp, url_prefix='/api/urls')
app.register_blueprint(queue_bp, url_prefix='/api/queue')

# Initialize data files
init_data_files()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    start_monitoring()
    app.run(debug=True, port=4000, host='localhost')
