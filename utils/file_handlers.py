import json
import os

DATA_FILE = 'data/urls.json'
QUEUE_FILE = 'data/queue.json'

def init_data_files():
    os.makedirs('data', exist_ok=True)
    for file in [DATA_FILE, QUEUE_FILE]:
        if not os.path.exists(file) or os.path.getsize(file) == 0:
            with open(file, 'w') as f:
                json.dump([], f)

def read_urls():
    try:
        with open(DATA_FILE, 'r') as f:
            content = f.read().strip()
            return json.loads(content) if content else []
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_urls(urls):
    with open(DATA_FILE, 'w') as f:
        json.dump(urls, f, indent=2)

def read_queue():
    try:
        with open(QUEUE_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def write_queue(queue):
    with open(QUEUE_FILE, 'w') as f:
        json.dump(queue, f, indent=2)
