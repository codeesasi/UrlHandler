import time
import random
import logging
import pyperclip
import threading
from utils.file_handlers import read_queue
from utils.common import clipboard_safe_insert
from utils.url_helpers import is_valid_url, get_url_metadata

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

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
    logging.info("Clipboard monitor started")
    
    while True:
        try:
            current_clipboard = safe_paste()
            
            if current_clipboard is None:
                logging.warning("Failed to access clipboard, retrying in 2 seconds...")
                time.sleep(2)
                continue
            
            # Debug print current clipboard content
            if current_clipboard != last_copied:
                logging.debug(f"New clipboard content: {current_clipboard[:100]}...")
                
            if current_clipboard != last_copied and is_valid_url(current_clipboard):
                logging.info(f"Valid URL detected: {current_clipboard}")
                try:
                    metadata = get_url_metadata(current_clipboard)
                    queue = read_queue()
                    
                    # Check if URL already exists in queue
                    if not any(item['url'] == current_clipboard for item in queue):
                        result = clipboard_safe_insert(current_clipboard, metadata['title'], metadata['thumbnail'])
                        logging.info(f"Queue insert result: {result}")
                    else:
                        logging.info(f"URL already exists in queue: {current_clipboard}")
                        
                    last_copied = current_clipboard
                except Exception as e:
                    logging.error(f"Error processing URL: {str(e)}")
            
            time.sleep(2)
            
        except Exception as e:
            logging.error(f"Error monitoring clipboard ({type(e).__name__}): {str(e)}")
            time.sleep(2)

def start_monitoring():
    thread = threading.Thread(target=monitor_clipboard, daemon=True)
    thread.start()