# MaintainUrl

<h1 align="center">UrlHandler</h1>

<p align="center">
  <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status"/>
  <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License"/>
</p>

<hr/>

<h2>About</h2>
<p>
  <b>UrlHandler</b> is a project for handling and processing URLs efficiently.<br/>
  This repository contains utilities and tools for URL parsing, validation, and manipulation.
</p>

## Features

- 🎯 Easy URL collection with automatic thumbnail and title extraction
- 🔍 Smart search functionality with keyword filtering
- 🗂️ Advanced sorting and filtering options
- ⏱️ Time-based filtering (Today, This Week, This Month)
- 📱 Responsive design using Bootstrap 5
- 🎨 Modern UI with hover effects and animations
- 📊 Pagination for better performance
- 📋 Clipboard monitoring for automatic URL detection
- ⏳ Queue management for URL processing

## Tech Stack

- Frontend:
  - Bootstrap 5
  - Font Awesome
  - Vanilla JavaScript
- Backend:
  - Python/Flask
  - BeautifulSoup4 (for metadata extraction)
  - Pyperclip (for clipboard monitoring)

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/yourusername/MaintainUrl.git
cd MaintainUrl
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the application
```bash
python app.py
```

4. Visit `http://localhost:4000` in your browser

## Project Structure

```
MaintainUrl/
├── blueprints/
│   ├── url_routes.py     # URL management endpoints
│   └── queue_routes.py   # Queue management endpoints
├── utils/
│   ├── url_helpers.py    # URL validation and metadata
│   └── file_handlers.py  # JSON file operations
├── data/
│   ├── urls.json        # Stored URLs
│   └── queue.json       # URL queue
├── templates/
│   └── index.html       # Main HTML template
├── clipboard_monitor.py  # Clipboard URL detection
├── app.py              # Flask application
└── requirements.txt    # Python dependencies
```

## API Endpoints

### URL Management
- `GET /api/urls/get_urls` - Retrieve all saved URLs
- `POST /api/urls/add_url` - Add a new URL
- `POST /api/urls/delete_url` - Delete a URL
- `POST /api/urls/edit_url` - Edit URL details
- `POST /api/urls/mark_as_read` - Mark URL as read
- `POST /api/urls/increment_click` - Increment URL click count

### Queue Management
- `GET /api/queue/get_queue` - Get queued URLs
- `POST /api/queue/move_queued_urls` - Move URLs from queue to main list
- `POST /api/queue/delete_queue_item` - Delete item from queue
- `POST /api/queue/move_queue_item` - Move single item from queue

## Features in Detail

### Clipboard Monitor
- Automatically detects URLs copied to clipboard
- Validates and extracts metadata
- Adds valid URLs to queue

### URL Management
- Store URLs with titles and thumbnails
- Track read status and click counts
- Edit URL metadata
- Delete unwanted URLs

### Queue System
- Temporary storage for new URLs
- Batch move to main list
- Individual item management

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

<h2>License</h2>
<p>
  This project is licensed under the MIT License.
</p>
