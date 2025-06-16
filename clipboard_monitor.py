import time
import pyperclip
import threading
import os
from utils.url_helpers import is_valid_url, get_url_metadata
from utils.file_handlers import read_queue, write_queue
import random
from utils.common import get_current_utc_datetime

QUEUE_FILE = 'data/queue.json'

def safe_paste():
    max_retries = 3
    base_delay = 1
    
    for attempt in range(max_retries):
        try:
            return pyperclip.paste()
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            delay = (base_delay * (2 ** attempt) + 
                    random.uniform(0, 0.1))  # Add jitter
            time.sleep(delay)
    return None

def monitor_clipboard():
    last_copied = ''
    os.makedirs('data', exist_ok=True)
    
    while True:
        try:
            current_clipboard = safe_paste()
            
            if current_clipboard is None:
                print("Failed to access clipboard, retrying in 2 seconds...")
                time.sleep(2)
                continue
                
            if current_clipboard != last_copied and is_valid_url(current_clipboard):
                metadata = get_url_metadata(current_clipboard)
                queue = read_queue()
                
                # Check if URL already exists in queue
                if not any(item['url'] == current_clipboard for item in queue):
                    print(f"Cliptext: {current_clipboard}")
                    new_entry = {
                        'url': current_clipboard,
                        'title': metadata['title'],
                        'thumbnail': metadata['thumbnail'],
                        'added': get_current_utc_datetime(),
                        'isRead': False,
                        'clickCount': 0
                    }
                    queue.append(new_entry)
                    write_queue(queue)
                
                last_copied = current_clipboard
            
            time.sleep(2)  # Check every 2 seconds
            
        except Exception as e:
            print(f"Error monitoring clipboard ({type(e).__name__}): {str(e)}")
            time.sleep(2)  # Continue monitoring even after error

def start_monitoring():
    thread = threading.Thread(target=monitor_clipboard, daemon=True)
    thread.start()
