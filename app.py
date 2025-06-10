from flask import Flask, render_template, request, jsonify
from blueprints.url_routes import url_bp
from blueprints.queue_routes import queue_bp
from utils.file_handlers import init_data_files
from clipboard_monitor import start_monitoring
import logging
import json
from datetime import datetime

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

@app.route('/move-queue-items', methods=['POST'])
def move_queue_items():
    try:
        data = request.json
        titles = data.get('titles', [])
        
        # Load both JSON files
        with open('queue.json', 'r') as f:
            queue_data = json.load(f)
        
        with open('urls.json', 'r') as f:
            urls_data = json.load(f)
        
        # Find matching items and mark them as moved
        for title in titles:
            for item in queue_data:
                if item['title'] == title:
                    item['moved'] = True
                    # Add to urls if not already present
                    if not any(url['title'] == title for url in urls_data):
                        urls_data.append({
                            'title': item['title'],
                            'url': item['url'],
                            'thumbnail': item.get('thumbnail', ''),
                            'timestamp': datetime.now().isoformat(),
                            'read': False,
                            'clickCount': 0,
                        })
        
        # Save both files
        with open('queue.json', 'w') as f:
            json.dump(queue_data, f, indent=4)
            
        with open('urls.json', 'w') as f:
            json.dump(urls_data, f, indent=4)
            
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    start_monitoring()
    app.run(debug=True, port=4000, host='localhost')
