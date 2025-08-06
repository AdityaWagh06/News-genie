import logging
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from typing import List, Dict, Tuple
from .models import UserProfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ContentBasedRecommender:
    """
    Content-based recommendation engine using TF-IDF and keyword matching.
    Provides personalized article recommendations based on user preferences.
    """
    
    def __init__(self):
        """Initialize the recommender with TF-IDF vectorizer"""
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            min_df=2
        )
        self.article_features = None
        self.article_texts = []
        self.user_profiles = self._load_mock_user_profiles()
        
    def _load_mock_user_profiles(self) -> Dict[str, UserProfile]:
        """
        Load mock user profiles for demonstration.
        In production, this would come from a database.
        
        Returns:
            Dictionary of user profiles
        """
        return {
            "user123": UserProfile(
                user_id="user123",
                preferred_topics=["AI", "technology", "machine learning"],
                click_history=["article1", "article3"],
                favorite_articles=["article1"]
            ),
            "user456": UserProfile(
                user_id="user456",
                preferred_topics=["politics", "economics", "business"],
                click_history=["article2", "article4"],
                favorite_articles=["article2"]
            ),
            "user789": UserProfile(
                user_id="user789",
                preferred_topics=["sports", "entertainment", "health"],
                click_history=["article5"],
                favorite_articles=[]
            )
        }
    
    def preprocess_text(self, text: str) -> str:
        """
        Preprocess text for better TF-IDF analysis.
        
        Args:
            text: Raw text
            
        Returns:
            Preprocessed text
        """
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def fit_articles(self, articles: List[Dict]) -> None:
        """
        Fit the TF-IDF vectorizer on article data.
        
        Args:
            articles: List of article dictionaries with 'title' and 'content' keys
        """
        if not articles:
            logger.warning("No articles provided for fitting")
            return
        
        # Prepare text data for TF-IDF
        article_texts = []
        for article in articles:
            title = article.get('title', '')
            content = article.get('content', '')
            # Combine title and content for better representation
            combined_text = f"{title} {content}"
            processed_text = self.preprocess_text(combined_text)
            article_texts.append(processed_text)
        
        # Fit TF-IDF vectorizer
        try:
            self.article_features = self.vectorizer.fit_transform(article_texts)
            self.article_texts = article_texts
            logger.info(f"Fitted TF-IDF on {len(articles)} articles")
        except Exception as e:
            logger.error(f"Error fitting TF-IDF: {e}")
            raise
    
    def calculate_user_preference_vector(self, user_id: str, topics: List[str]) -> np.ndarray:
        """
        Calculate user preference vector based on topics.
        
        Args:
            user_id: User identifier
            topics: List of preferred topics
            
        Returns:
            User preference vector
        """
        # Get user profile
        user_profile = self.user_profiles.get(user_id)
        if not user_profile:
            # Create default profile for new user
            user_profile = UserProfile(
                user_id=user_id,
                preferred_topics=topics
            )
            self.user_profiles[user_id] = user_profile
        
        # Create preference text from topics
        preference_text = " ".join(topics)
        processed_preference = self.preprocess_text(preference_text)
        
        # Transform to TF-IDF vector
        preference_vector = self.vectorizer.transform([processed_preference])
        
        return preference_vector.toarray()[0]
    
    def recommend_articles(self, user_id: str, articles: List[Dict], 
                         topics: List[str], top_k: int = 10) -> List[Tuple[Dict, float]]:
        """
        Recommend articles for a user based on their preferences.
        
        Args:
            user_id: User identifier
            articles: List of article dictionaries
            topics: List of user's preferred topics
            top_k: Number of recommendations to return
            
        Returns:
            List of (article, score) tuples sorted by score
        """
        if not articles:
            logger.warning("No articles provided for recommendation")
            return []
        
        try:
            # Fit articles if not already fitted
            if self.article_features is None:
                self.fit_articles(articles)
            
            # Calculate user preference vector
            user_vector = self.calculate_user_preference_vector(user_id, topics)
            
            # Calculate similarity scores
            similarities = []
            for i, article in enumerate(articles):
                # Get article vector
                article_vector = self.article_features[i].toarray()[0]
                
                # Calculate cosine similarity
                similarity = cosine_similarity(
                    [user_vector], 
                    [article_vector]
                )[0][0]
                
                # Apply topic boost
                topic_boost = self._calculate_topic_boost(article, topics)
                final_score = similarity * topic_boost
                
                similarities.append((article, final_score))
            
            # Sort by score and return top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            recommendations = similarities[:top_k]
            
            logger.info(f"Generated {len(recommendations)} recommendations for user {user_id}")
            return recommendations
            
        except Exception as e:
            logger.error(f"Error in recommendation: {e}")
            # Return articles with default scores
            return [(article, 0.5) for article in articles[:top_k]]
    
    def _calculate_topic_boost(self, article: Dict, topics: List[str]) -> float:
        """
        Calculate topic boost based on keyword matching.
        
        Args:
            article: Article dictionary
            topics: User's preferred topics
            
        Returns:
            Topic boost multiplier
        """
        article_text = f"{article.get('title', '')} {article.get('content', '')}".lower()
        
        # Count topic matches
        topic_matches = 0
        for topic in topics:
            if topic.lower() in article_text:
                topic_matches += 1
        
        # Calculate boost (1.0 = no boost, 1.5 = 50% boost)
        if topic_matches == 0:
            return 1.0
        elif topic_matches == 1:
            return 1.2
        else:
            return 1.5
    
    def update_user_profile(self, user_id: str, clicked_article_id: str = None, 
                          favorited_article_id: str = None) -> None:
        """
        Update user profile based on interactions.
        
        Args:
            user_id: User identifier
            clicked_article_id: ID of clicked article
            favorited_article_id: ID of favorited article
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                preferred_topics=[]
            )
        
        user_profile = self.user_profiles[user_id]
        
        if clicked_article_id:
            user_profile.click_history.append(clicked_article_id)
            # Keep only last 50 clicks
            user_profile.click_history = user_profile.click_history[-50:]
        
        if favorited_article_id:
            if favorited_article_id not in user_profile.favorite_articles:
                user_profile.favorite_articles.append(favorited_article_id)
        
        logger.info(f"Updated profile for user {user_id}")
    
    def get_user_profile(self, user_id: str) -> UserProfile:
        """
        Get user profile.
        
        Args:
            user_id: User identifier
            
        Returns:
            UserProfile object
        """
        return self.user_profiles.get(user_id)

# Global recommender instance
_recommender_instance = None

def get_recommender() -> ContentBasedRecommender:
    """
    Get or create the global recommender instance.
    
    Returns:
        ContentBasedRecommender instance
    """
    global _recommender_instance
    if _recommender_instance is None:
        _recommender_instance = ContentBasedRecommender()
    return _recommender_instance 