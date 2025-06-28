from flask import Blueprint, jsonify, request, current_app
from utils.url_helpers import is_valid_url, get_url_metadata
from utils.file_handlers import read_urls, write_urls, save_summary_data
from utils.common import get_current_utc_datetime
import requests
from bs4 import BeautifulSoup
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

url_bp = Blueprint('urls', __name__)

class WebSummaryResult(BaseModel):
    summary: str = Field(description="Concise summary of the web content")
    keywords: List[str] = Field(description="List of important keywords extracted from the content")
    tone: str = Field(description="The tone of the original content, e.g., informative, persuasive, casual")
    rating: int = Field(default=0, ge=0, le=5, description="Rating of the content quality from 0 to 5")


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

        print(soup.title.string)  # Debugging line to check title extraction

        # Check if the page has a t

        # Extract main text content
        text = soup.get_text(separator='\n', strip=True)
        if not text or len(text) < 10:
            return jsonify({'summary': 'Content too short to summarize.'})
        
        # Store first 4000 chars for LLM context
        raw_text = text[:4000]
        output_parser = PydanticOutputParser(pydantic_object=WebSummaryResult)
        escaped_format_instructions = output_parser.get_format_instructions().replace("{", "{{").replace("}", "}}")

        # 3. Prompt with stricter instruction
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    (
                        "You are an intelligent content summarizer designed to analyze and distill meaningful information from raw HTML or plain text extracted from HTTPS URLs.Your goal is to produce high-quality, human-readable summaries that are informative, concise, and keyword-rich.\n"
                        "Each summary should highlight the main purpose, insights, or value offered by the page, while using clear and professional language.\n"
                        "Your response should strictly follow the JSON format below without any additional text or explanation.\n"
                        "Ignore irrelevant elements like navigation bars, ads, cookie banners, and footers.\n"
                        "Add relevant **keywords** naturally to improve discoverability (SEO-friendly).\n"
                        "Identify the main purpose of the page (e.g., educate, promote, inform, instruct).\n"
                        "If the content is multi-sectioned, prioritize the most impactful parts.\n"
                        "Analyze and summarize the following web content, rating for the site. Do not include any explanation or text outside the JSON.\n\n"
                        f"Respond using this format:\n{escaped_format_instructions}"
                    ),
                ),
                ("human", "{web_content}"),
            ]
        )

        # 4. LLM setup
        llm = ChatOllama(
            model="deepseek-r1:8b",
            temperature=0.3,
            max_tokens=1500,
            top_p=0.8,
            top_k=10,
            stream=False,
            num_thread=5,
            num_gpu=1,
            num_ctx=4096,
        )

        # 5. Chain
        chain = prompt | llm | output_parser

        # 6. Input
        web_content_text = """
        OpenAI has released GPT-4o, the newest generation of its powerful language model. Unlike earlier versions, GPT-4o offers
        multimodal capabilities, meaning it can understand and generate text, audio, and images. It is faster, more cost-effective,
        and offers better real-time reasoning. The model is freely available to ChatGPT users, with enhanced access for paid tiers.
        """

        # 7. Safe call with debugging
        try:
            result = chain.invoke({"web_content": web_content_text})
            # Save data for training
            save_summary_data(url, raw_text, result, "deepseek-r1:8b")
            return jsonify({'summary': result.summary,'keywords': result.keywords, 'tone': result.tone, 'rating': result.rating})
            
        except Exception as e:
            # Optional fallback: get raw model output to inspect
            raw_output = (prompt | llm).invoke({"web_content": web_content_text})
            return jsonify({'summary': raw_output.summary,'keywords': raw_output.keywords, 'tone': raw_output.tone, 'rating': raw_output.rating})
        
    except Exception as e:
        return jsonify({'summary': f'Error: {str(e)}'}), 500

# No changes needed here for splitting, as the summary already includes <think>...</think>