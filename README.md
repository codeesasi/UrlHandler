# URL Collector

A modern web application for collecting, organizing, and managing URL bookmarks with thumbnail previews.

## Features

- 🎯 Easy URL collection with automatic thumbnail and title extraction
- 🔍 Smart search functionality with keyword filtering
- 🗂️ Advanced sorting and filtering options
- ⏱️ Time-based filtering (Today, This Week, This Month)
- 📱 Responsive design using Bootstrap 5
- 🎨 Modern UI with hover effects and animations
- 📊 Pagination for better performance

## Tech Stack

- Frontend:
  - Bootstrap 5
  - Font Awesome
  - Vanilla JavaScript
- Backend:
  - Python/Flask
  - BeautifulSoup4 (for metadata extraction)

## Getting Started

1. Clone the repository
```bash
git clone https://github.com/yourusername/url-collector.git
cd url-collector
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Set up MongoDB
- Make sure MongoDB is installed and running
- Update connection settings in config.py if needed

4. Run the application
```bash
python app.py
```

5. Visit `http://localhost:5000` in your browser

## Project Structure

```
MaintainUrl/
├── static/
│   └── script.js         # Frontend JavaScript
├── templates/
│   └── index.html        # Main HTML template
├── app.py               # Flask application
├── requirements.txt     # Python dependencies
└── README.md           # Documentation
```

## API Endpoints

- `GET /get_urls` - Retrieve all saved URLs
- `POST /add_url` - Add a new URL
- `POST /delete_url` - Delete a URL

## Features in Detail

### URL Collection
- Automatically extracts website titles and thumbnails
- Validates URL format
- Prevents duplicate entries
- Shows loading states during operations

### Search & Filtering
- Keyword-based search in titles
- Multiple sorting options (newest, oldest, A-Z, Z-A)
- Time-based filtering
- Reset filters functionality

### User Interface
- Responsive sidebar for filters
- Floating action button for adding URLs
- Bootstrap modals for actions
- Toast notifications for feedback
- Hover effects and smooth transitions

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

MIT License - feel free to use this project for your own purposes.
