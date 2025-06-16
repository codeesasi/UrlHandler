from flask import Blueprint, jsonify, request
from utils.file_handlers import read_queue, write_queue, read_urls, write_urls
from utils.common import get_current_utc_datetime

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/get_queue')
def get_queue():
    return jsonify(read_queue())

@queue_bp.route('/move_queued_urls', methods=['POST'])
def move_queued_urls():
    try:
        urls_to_move = request.json.get('items', [])
        queue = read_queue()
        urls = read_urls()
        
        selected_items = [item for item in queue if item.get('url') in urls_to_move]
        remaining_items = [item for item in queue if item.get('url') not in urls_to_move]
        
        urls.extend(selected_items)
        write_urls(urls)
        write_queue(remaining_items)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@queue_bp.route('/delete_queue_item', methods=['POST'])
def delete_queue_item():
    try:
        url_to_delete = request.json.get('url')
        if not url_to_delete:
            return jsonify({'status': 'error', 'message': 'Missing URL'}), 400
        
        queue = read_queue()
        queue = [item for item in queue if item['url'] != url_to_delete]
        write_queue(queue)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500