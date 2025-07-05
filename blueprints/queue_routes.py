from flask import Blueprint, jsonify, request
from utils.db_handler import get_queue, get_db_connection

queue_bp = Blueprint('queue', __name__)

@queue_bp.route('/get_queue')
def get_queue():
    try:
        queue_items = get_queue()
        return jsonify(queue_items)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@queue_bp.route('/move_queued_urls', methods=['POST'])
def move_queued_urls():
    try:
        urls_to_move = request.json.get('items', [])
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    UPDATE tbl_urlqueue 
                    SET ismoved = true 
                    WHERE url = ANY(%s)
                """, (urls_to_move,))
                conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@queue_bp.route('/delete_queue_item', methods=['POST'])
def delete_queue_item():
    try:
        url_to_delete = request.json.get('url')
        if not url_to_delete:
            return jsonify({'status': 'error', 'message': 'Missing URL'}), 400
        
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    DELETE FROM tbl_urlqueue 
                    WHERE url = %s
                """, (url_to_delete,))
                conn.commit()
        
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500