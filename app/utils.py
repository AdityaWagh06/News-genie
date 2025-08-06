import os
import logging
import requests
from typing import List, Dict, Optional
from datetime import datetime, timedelta
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsAPIClient:
    """
    Client for fetching news articles from NewsAPI.
    Falls back to mock data if API key is not available.
    """
    
    def __init__(self):
        self.api_key = os.getenv('NEWS_API_KEY')
        self.base_url = "https://newsapi.org/v2"
        
    def fetch_news(self, topics: List[str], max_articles: int = 20) -> List[Dict]:
        """
        Fetch news articles based on topics.
        
        Args:
            topics: List of topics to search for
            max_articles: Maximum number of articles to fetch
            
        Returns:
            List of article dictionaries
        """
        if not self.api_key:
            logger.warning("No NEWS_API_KEY found, using mock data")
            return self._get_mock_articles(topics, max_articles)
        
        articles = []
        for topic in topics:
            try:
                url = f"{self.base_url}/everything"
                params = {
                    'q': topic,
                    'apiKey': self.api_key,
                    'language': 'en',
                    'sortBy': 'publishedAt',
                    'pageSize': min(max_articles, 20)
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                if data.get('status') == 'ok':
                    topic_articles = data.get('articles', [])
                    articles.extend(topic_articles)
                    logger.info(f"Fetched {len(topic_articles)} articles for topic: {topic}")
                else:
                    logger.error(f"NewsAPI error: {data.get('message', 'Unknown error')}")
                    
            except requests.RequestException as e:
                logger.error(f"Error fetching news for topic {topic}: {e}")
                continue
        
        # Remove duplicates and limit results
        unique_articles = self._remove_duplicates(articles)
        return unique_articles[:max_articles]
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """
        Remove duplicate articles based on URL.
        
        Args:
            articles: List of articles
            
        Returns:
            List of unique articles
        """
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
    
    def _get_mock_articles(self, topics: List[str], max_articles: int) -> List[Dict]:
        """
        Get mock articles for testing and development.
        
        Args:
            topics: List of topics
            max_articles: Maximum number of articles
            
        Returns:
            List of mock articles
        """
        mock_articles = [
            {
                "title": "AI Breakthrough in Natural Language Processing",
                "content": "Researchers have developed a new AI model that significantly improves natural language understanding. The model, based on transformer architecture, shows remarkable performance on various NLP tasks including translation, summarization, and question answering. This breakthrough could revolutionize how we interact with AI systems in everyday applications.",
                "url": "https://example.com/ai-breakthrough",
                "source": {"name": "Tech News"},
                "publishedAt": datetime.now().isoformat(),
                "description": "New AI model shows unprecedented performance in language tasks."
            },
            {
                "title": "Machine Learning Revolutionizes Healthcare Diagnostics",
                "content": "Healthcare providers are increasingly adopting machine learning algorithms to improve diagnostic accuracy. These AI systems can analyze medical images, patient data, and symptoms to provide faster and more accurate diagnoses. Early results show significant improvements in detection rates for various conditions.",
                "url": "https://example.com/ml-healthcare",
                "source": {"name": "Health Tech"},
                "publishedAt": (datetime.now() - timedelta(hours=2)).isoformat(),
                "description": "AI-powered diagnostics show promising results in healthcare."
            },
            {
                "title": "Global Economic Trends in 2024",
                "content": "The global economy is showing signs of recovery with emerging markets leading the way. Technology sectors continue to drive growth while traditional industries adapt to digital transformation. Experts predict sustained growth in AI and renewable energy sectors.",
                "url": "https://example.com/economic-trends",
                "source": {"name": "Business Daily"},
                "publishedAt": (datetime.now() - timedelta(hours=4)).isoformat(),
                "description": "Economic recovery continues with technology sectors leading growth."
            },
            {
                "title": "Climate Change: New Solutions Emerge",
                "content": "Scientists are developing innovative solutions to address climate change challenges. From carbon capture technologies to renewable energy breakthroughs, these developments offer hope for a sustainable future. International cooperation is key to implementing these solutions effectively.",
                "url": "https://example.com/climate-solutions",
                "source": {"name": "Science Today"},
                "publishedAt": (datetime.now() - timedelta(hours=6)).isoformat(),
                "description": "Innovative climate solutions show promise for sustainable future."
            },
            {
                "title": "Space Exploration: Mars Mission Update",
                "content": "The latest Mars mission has provided unprecedented data about the red planet's geology and atmosphere. Scientists are analyzing samples that could reveal evidence of past water and potential for future human habitation. This mission represents a major step forward in space exploration.",
                "url": "https://example.com/mars-mission",
                "source": {"name": "Space News"},
                "publishedAt": (datetime.now() - timedelta(hours=8)).isoformat(),
                "description": "Mars mission reveals new insights about the red planet."
            }
        ]
        
        # Filter articles based on topics
        filtered_articles = []
        for article in mock_articles:
            article_text = f"{article['title']} {article['content']}".lower()
            for topic in topics:
                if topic.lower() in article_text:
                    filtered_articles.append(article)
                    break
        
        return filtered_articles[:max_articles]

def format_article_for_response(article: Dict, summary: str, score: float) -> Dict:
    """
    Format article data for API response.
    
    Args:
        article: Raw article data
        summary: Generated summary
        score: Recommendation score
        
    Returns:
        Formatted article dictionary
    """
    return {
        "title": article.get('title', ''),
        "summary": summary,
        "link": article.get('url', ''),
        "source": article.get('source', {}).get('name', 'Unknown'),
        "score": round(score, 3),
        "published_at": article.get('publishedAt'),
        "content": article.get('content', '')
    }

def validate_topics(topics_str: str) -> List[str]:
    """
    Validate and parse topics string.
    
    Args:
        topics_str: Comma-separated topics string
        
    Returns:
        List of validated topics
    """
    if not topics_str:
        return ["technology"]  # Default topic
    
    # Split and clean topics
    topics = [topic.strip() for topic in topics_str.split(',')]
    topics = [topic for topic in topics if topic]  # Remove empty topics
    
    if not topics:
        return ["technology"]  # Default if no valid topics
    
    return topics

def log_api_request(user_id: str, topics: List[str], article_count: int):
    """
    Log API request for monitoring.
    
    Args:
        user_id: User identifier
        topics: Requested topics
        article_count: Number of articles returned
    """
    logger.info(f"API Request - User: {user_id}, Topics: {topics}, Articles: {article_count}")

def create_error_response(message: str, status_code: int = 400) -> Dict:
    """
    Create standardized error response.
    
    Args:
        message: Error message
        status_code: HTTP status code
        
    Returns:
        Error response dictionary
    """
    return {
        "error": True,
        "message": message,
        "status_code": status_code,
        "timestamp": datetime.now().isoformat()
    }

# Global news client instance
_news_client = None

def get_news_client() -> NewsAPIClient:
    """
    Get or create the global news client instance.
    
    Returns:
        NewsAPIClient instance
    """
    global _news_client
    if _news_client is None:
        _news_client = NewsAPIClient()
    return _news_client 