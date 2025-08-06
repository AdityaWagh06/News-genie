# NewsGenie 🧠📰

A full-stack AI-powered news application that provides personalized and summarized news content using BART (Bidirectional and Auto-Regressive Transformers) for summarization and a content-based recommendation engine.

## Features

- 🤖 **AI-Powered Summarization**: Uses Facebook's BART-large-CNN model for abstractive summarization
- 🎯 **Personalized Recommendations**: Content-based recommendation engine using TF-IDF
- 📱 **Modern Frontend**: React-based UI with clean, responsive design
- 🔧 **RESTful API**: FastAPI backend with automatic documentation
- 🧪 **Comprehensive Testing**: Unit tests and API testing

## Project Structure

```
newsgenie/
├── app/
│   ├── main.py              # FastAPI application
│   ├── summarizer.py        # BART summarization module
│   ├── recommender.py       # Content-based recommendation engine
│   ├── utils.py            # Utility functions
│   └── models.py           # Pydantic models
├── frontend/               # React frontend
├── data/                   # Mock data and user profiles
├── tests/                  # Test files
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Quick Start

### Backend Setup

1. **Clone and navigate to the project:**
   ```bash
   cd newsgenie
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory:
   ```env
   NEWS_API_KEY=your_news_api_key_here
   ```

5. **Run the backend server:**
   ```bash
   cd app
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

6. **Access the API documentation:**
   - Swagger UI: http://localhost:8000/docs
   - ReDoc: http://localhost:8000/redoc

### Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## API Endpoints

### GET /news
Retrieve personalized and summarized news articles.

**Query Parameters:**
- `user_id` (required): User identifier
- `preferred_topics` (required): Comma-separated list of topics (e.g., "AI,politics,sports")

**Example Request:**
```bash
curl "http://localhost:8000/news?user_id=user123&preferred_topics=AI,technology"
```

**Response:**
```json
[
  {
    "title": "AI Breakthrough in Natural Language Processing",
    "summary": "Researchers have developed a new AI model that significantly improves natural language understanding...",
    "link": "https://example.com/article1",
    "source": "Tech News",
    "score": 0.87
  }
]
```

## Testing

### Run Backend Tests
```bash
pytest tests/ -v
```

### Test API Endpoints
Use the Swagger UI at http://localhost:8000/docs for interactive API testing.

## Technologies Used

- **Backend**: FastAPI, Python 3.8+
- **AI/ML**: Transformers (Hugging Face), BART, scikit-learn
- **Frontend**: React, TypeScript, Tailwind CSS
- **Testing**: pytest, httpx
- **API Documentation**: Swagger/OpenAPI

## Configuration

### News API
The application uses NewsAPI to fetch articles. Get your free API key at [newsapi.org](https://newsapi.org).

### Model Configuration
- **Summarization Model**: `facebook/bart-large-cnn`
- **Max Input Tokens**: 1024
- **Summary Length**: 3-5 sentences

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request
