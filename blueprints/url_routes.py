from flask import Blueprint, jsonify, request, current_app
from utils.url_helpers import is_valid_url, get_url_metadata
from utils.file_handlers import read_urls, write_urls
from utils.common import get_current_utc_datetime
import requests
from bs4 import BeautifulSoup
from langchain_community.llms import Ollama
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document

url_bp = Blueprint('urls', __name__)

@url_bp.route('/get_urls', methods=['GET'])
def get_urls():
    try:
        urls = read_urls()
        return jsonify(urls)
    except Exception as e:
        current_app.logger.error(f"Error in get_urls: {str(e)}")
        return jsonify({'error': 'Failed to fetch URLs'}), 500

@url_bp.route('/add_url', methods=['POST'])
def add_url():
    data = request.json
    url = data.get('url')
    if not url or not is_valid_url(url):
        return jsonify({'status': 'error', 'message': 'Invalid or missing URL'}), 400

    urls = read_urls()
    if any(entry['url'] == url for entry in urls):
        return jsonify({
            'success': False,
            'message': 'This URL has already been added to your collection'
        }), 409

    metadata = get_url_metadata(url)
    new_entry = {
        'url': url,
        'title': metadata['title'],
        'thumbnail': metadata['thumbnail'],
        'added': get_current_utc_datetime(),
        'isRead': False,
        'clickCount': 0
    }
    
    urls.append(new_entry)
    write_urls(urls)
    return jsonify({'status': 'success'}), 200

@url_bp.route('/delete_url', methods=['POST'])
def delete_url():
    url_to_delete = request.json.get('url')
    if not url_to_delete:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400

    urls = read_urls()
    urls = [u for u in urls if u['url'] != url_to_delete]
    write_urls(urls)
    return jsonify({'status': 'success'}), 200

@url_bp.route('/edit_url', methods=['POST'])
def edit_url():
    data = request.json
    try:
        urls = read_urls()
        for entry in urls:
            if entry['url'] == data['url']:
                entry['title'] = data['title']
                entry['thumbnail'] = data['thumbnail']
                break
        write_urls(urls)
        return jsonify({'success': True})
    except Exception as e:
        current_app.logger.error(f"Error in edit_url: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500
    
@url_bp.route('/mark_as_read', methods=['POST'])
def mark_as_read():
    data = request.json
    url_to_mark = data.get('url')
    if not url_to_mark:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400

    urls = read_urls()
    for entry in urls:
        if entry['url'] == url_to_mark:
            entry['isRead'] = True
            break
    write_urls(urls)
    return jsonify({'status': 'success'}), 200

@url_bp.route('/update_url_status', methods=['POST'])
def update_url_status():
    data = request.json
    url_to_update = data.get('url')
    if not url_to_update:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400

    urls = read_urls()
    for entry in urls:
        if entry['url'] == url_to_update:
            entry['isRead'] = data.get('isRead', entry['isRead'])
            break
    write_urls(urls)
    return jsonify({'status': 'success'}), 200  

@url_bp.route('/increment_click', methods=['POST'])
def increment_click():
    data = request.json
    url_to_increment = data.get('url')
    if not url_to_increment:
        return jsonify({'status': 'error', 'message': 'Missing URL'}), 400

    urls = read_urls()
    for entry in urls:
        if entry['url'] == url_to_increment:
            entry['clickCount'] += 1
            break
    write_urls(urls)
    return jsonify({'status': 'success'}), 200

@url_bp.route('/summarize_url', methods=['POST'])
def summarize_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({'summary': 'No URL provided.'}), 400

    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Extract main text content
        text = soup.get_text(separator='\n', strip=True)
        if not text or len(text) < 10:
            return jsonify({'summary': 'Content too short to summarize.'})
        # Limit to first 4000 chars for LLM context
        think = text[:1000]  # shrink/think details (first 1000 chars)
        text = text[:4000]
        doc = Document(page_content=text)
        llm = Ollama(model="deepseek-r1:8b")  # or your preferred model
        chain = load_summarize_chain(llm, chain_type="stuff")
        summary = chain.run([doc])
        return jsonify({'summary': summary, 'think': think})
    except Exception as e:
        return jsonify({'summary': f'Error: {str(e)}'}), 500

# No changes needed here for splitting, as the summary already includes <think>...</think>