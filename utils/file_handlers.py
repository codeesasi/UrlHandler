import json
import os

DATA_FILE = 'data/urls.json'
QUEUE_FILE = 'data/queue.json'
USERS_FILE = 'data/users.json'

def init_data_files():
    os.makedirs('data', exist_ok=True)
    for file in [DATA_FILE, QUEUE_FILE, USERS_FILE]:
        if not os.path.exists(file):
            initial_data = [] if file != USERS_FILE else {}
            with open(file, 'w') as f:
                json.dump(initial_data, f, indent=2)

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

def read_users():
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def write_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
