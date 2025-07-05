import time
import random
import logging
import pyperclip
import threading
from utils.common import clipboard_safe_insert
from utils.url_helpers import is_valid_url, get_url_metadata

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ClipboardMonitor:
    def __init__(self):
        self._running = False
        self._thread = None
        self._last_copied = ''
        self._failure_count = 0
        self._max_failures = 5  # Reset clipboard after 5 consecutive failures
    
    def safe_paste(self):
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

    def monitor_clipboard(self):
        self._running = True
        logging.info("Clipboard monitor started")
        
        while self._running:
            try:
                current_clipboard = self.safe_paste()
                
                if current_clipboard is None:
                    self._failure_count += 1
                    if self._failure_count >= self._max_failures:
                        logging.error("Too many clipboard failures, resetting clipboard state")
                        self._last_copied = ''
                        self._failure_count = 0
                    logging.warning("Failed to access clipboard, retrying in 2 seconds...")
                    time.sleep(2)
                    continue

                self._failure_count = 0  # Reset failure count on successful paste
                
                # Prevent race condition with local copy
                last_copied = self._last_copied
                
                if current_clipboard != last_copied:
                    if is_valid_url(current_clipboard):
                        logging.info(f"Valid URL detected: {current_clipboard}")
                        try:
                            # Validate URL again before metadata fetch
                            if not current_clipboard.startswith(('http://', 'https://')):
                                raise ValueError("Invalid URL protocol")
                                
                            metadata = get_url_metadata(current_clipboard)
                            if not metadata or not metadata.get('title'):
                                logging.warning(f"Invalid or empty metadata for URL: {current_clipboard}")
                                continue
                                
                            result = clipboard_safe_insert(current_clipboard, metadata['title'], metadata['thumbnail'])
                            
                            if result is True:
                                logging.info("URL successfully added to database")
                                self._last_copied = current_clipboard
                            else:
                                logging.error(f"Failed to insert URL: {result}")
                                
                        except Exception as e:
                            logging.error(f"Error processing URL: {str(e)}")
                            # Don't update last_copied on error
                
                time.sleep(1 if current_clipboard != last_copied else 2)
                
            except Exception as e:
                logging.error(f"Error monitoring clipboard ({type(e).__name__}): {str(e)}")
                time.sleep(2)

    def start(self):
        """Start the clipboard monitoring thread."""
        if not self._running:
            self._thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
            self._thread.start()
            return True
        return False
    
    def stop(self):
        """Stop the clipboard monitoring thread."""
        try:
            self._running = False
            if self._thread:
                self._thread.join(timeout=5)
                if self._thread.is_alive():  
                    logging.warning("Thread failed to stop gracefully")
                self._thread = None
            self._last_copied = ''
            self._failure_count = 0
            return True
        except Exception as e:
            logging.error(f"Error stopping monitor: {str(e)}")
            return False

# Create singleton instance
monitor = ClipboardMonitor()

def start_monitoring():
    """Start the clipboard monitoring thread."""
    return monitor.start()