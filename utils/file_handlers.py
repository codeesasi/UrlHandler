import os, re
import pandas as pd
from datetime import datetime

TRAINING_DIR = 'data/training'
SUMMARY_DATA_FILE = 'data/training/summary_data.xlsx'

def init_data_files():
    """Initialize only training data directory"""
    os.makedirs(TRAINING_DIR, exist_ok=True)
    if not os.path.exists(SUMMARY_DATA_FILE):
        df = pd.DataFrame(columns=[
            'timestamp', 'url', 'raw_text', 'summary',
            'keywords', 'tone', 'rating', 'model'
        ])

    os.makedirs(TRAINING_DIR, exist_ok=True)
    if not os.path.exists(SUMMARY_DATA_FILE):
        df = pd.DataFrame(columns=[
            'timestamp', 'url', 'raw_text', 'summary',
            'keywords', 'tone', 'rating', 'model'
        ])
        df.to_excel(SUMMARY_DATA_FILE, index=False)

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
