import json
import os,re
import pandas as pd
from datetime import datetime

DATA_FILE = 'data/urls.json'
QUEUE_FILE = 'data/queue.json'
USERS_FILE = 'data/users.json'
TRAINING_DIR = 'data/training'
SUMMARY_DATA_FILE = 'data/training/summary_data.xlsx'

def init_data_files():
    os.makedirs('data', exist_ok=True)
    for file in [DATA_FILE, QUEUE_FILE, USERS_FILE]:
        if not os.path.exists(file):
            initial_data = [] if file != USERS_FILE else {}
            with open(file, 'w') as f:
                json.dump(initial_data, f, indent=2)
    os.makedirs(TRAINING_DIR, exist_ok=True)
    if not os.path.exists(SUMMARY_DATA_FILE):
        df = pd.DataFrame(columns=[
            'timestamp', 'url', 'raw_text', 'summary',
            'keywords', 'tone', 'rating', 'model'
        ])
        df.to_excel(SUMMARY_DATA_FILE, index=False)

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

def extract_summary_parts(summary: str) -> tuple[str, str]:
    """Extract <think> content and remaining summary."""
    think_matches = re.findall(r"<think>(.*?)</think>", summary, re.DOTALL)
    think = think_matches[0].strip() if think_matches else ""
    outside = re.sub(r"<think>.*?</think>", "", summary, flags=re.DOTALL).strip()
    return think, outside

def create_summary_row(url: str, raw_text: str, summary: dict, model_name: str) -> dict:
    """Create a new summary row with metadata."""
    return {
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "raw_text": raw_text,
        "summary": summary.get('summary', ''),
        "keywords": ','.join(summary.get('keywords', [])),
        "tone": summary.get('tone', ''),
        "rating": summary.get('rating', 0),
        "model": model_name,
    }

def save_summary_data(url: str, raw_text: str, summary: str, model_name: str) -> bool:
    """Save or update summary data in an Excel file."""
    try:
        if os.path.exists(SUMMARY_DATA_FILE):
            df = pd.read_excel(SUMMARY_DATA_FILE)
        else:
            df = pd.DataFrame(columns=["timestamp", "url", "raw_text", "summary", "think", "model"])

        new_row = create_summary_row(url, raw_text, summary, model_name)

        if url in df["url"].values:
            df.loc[df["url"] == url, df.columns] = list(new_row.values())
        else:
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

        df.to_excel(SUMMARY_DATA_FILE, index=False)
        return True

    except Exception as e:
        print(f"[ERROR] Failed to save summary data: {e}")
        return False
