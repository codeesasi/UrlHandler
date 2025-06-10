import re
import requests
from bs4 import BeautifulSoup

def is_valid_url(url):
    return re.match(r'^https?://', url) is not None

def get_page_title(url):
    try:
        response = requests.get(url, timeout=5)
        if response.ok:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string.strip() if soup.title else "No Title"
    except:
        return "No Title"
    return "No Title"

def get_url_metadata(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        thumbnail = soup.find('meta', property='og:image')
        if not thumbnail:
            thumbnail = soup.find('meta', property='twitter:image')
        thumbnail_url = thumbnail['content'] if thumbnail else ''
        
        title = soup.find('title')
        title_text = title.string if title else url
        
        return {
            'thumbnail': thumbnail_url,
            'title': title_text
        }
    except:
        return {'thumbnail': '', 'title': url}
