from flask import Blueprint, jsonify, request
from utils.file_handlers import read_queue, write_queue, read_urls, write_urls

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/get_queue')
def get_queue():
    return jsonify(read_queue())

@queue_bp.route('/move_queued_urls', methods=['POST'])
def move_queued_urls():
    try:
        indices = request.json.get('indices', [])
        queue = read_queue()
        urls = read_urls()
        
        selected_items = [queue[i] for i in sorted(indices)]
        remaining_items = [item for i, item in enumerate(queue) if i not in indices]
        
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
    
@queue_bp.route('/move_queue_item', methods=['POST'])
def move_queue_item():
    try:
        data = request.json
        url_to_move = data.get('url')
        if not url_to_move:
            return jsonify({'status': 'error', 'message': 'Missing URL'}), 400
        
        queue = read_queue()
        urls = read_urls()
        
        for item in queue:
            if item['url'] == url_to_move:
                urls.append(item)
                break
        
        queue = [item for item in queue if item['url'] != url_to_move]
        
        write_queue(queue)
        write_urls(urls)
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500