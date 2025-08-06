import pytest
from app.recommender import ContentBasedRecommender
from app.models import UserProfile

class TestContentBasedRecommender:
    """Test cases for the ContentBasedRecommender class"""
    
    def test_recommender_initialization(self):
        """Test that the recommender can be initialized"""
        recommender = ContentBasedRecommender()
        assert recommender is not None
        assert recommender.vectorizer is not None
        assert len(recommender.user_profiles) > 0
    
    def test_preprocess_text(self):
        """Test text preprocessing"""
        recommender = ContentBasedRecommender()
        
        # Test normal text
        text = "Hello, World! This is a test."
        processed = recommender.preprocess_text(text)
        assert processed == "hello world this is a test"
        
        # Test empty text
        processed = recommender.preprocess_text("")
        assert processed == ""
        
        # Test text with special characters
        text = "AI & ML: The Future of Technology!!!"
        processed = recommender.preprocess_text(text)
        assert "ai" in processed
        assert "ml" in processed
        assert "future" in processed
    
    def test_validate_topics(self):
        """Test topic validation"""
        from app.utils import validate_topics
        
        # Test normal topics
        topics = validate_topics("AI,technology,machine learning")
        assert topics == ["AI", "technology", "machine learning"]
        
        # Test empty topics
        topics = validate_topics("")
        assert topics == ["technology"]
        
        # Test topics with spaces
        topics = validate_topics("  AI  ,  technology  ")
        assert topics == ["AI", "technology"]
    
    def test_fit_articles(self):
        """Test article fitting"""
        recommender = ContentBasedRecommender()
        
        articles = [
            {
                "title": "AI Breakthrough",
                "content": "Artificial intelligence has made significant progress."
            },
            {
                "title": "Machine Learning News",
                "content": "Machine learning algorithms are improving rapidly."
            }
        ]
        
        recommender.fit_articles(articles)
        assert recommender.article_features is not None
        assert len(recommender.article_texts) == 2
    
    def test_calculate_topic_boost(self):
        """Test topic boost calculation"""
        recommender = ContentBasedRecommender()
        
        article = {
            "title": "AI Technology News",
            "content": "Artificial intelligence is transforming industries."
        }
        
        # Test with matching topics
        boost = recommender._calculate_topic_boost(article, ["AI", "technology"])
        assert boost > 1.0
        
        # Test with non-matching topics
        boost = recommender._calculate_topic_boost(article, ["sports", "entertainment"])
        assert boost == 1.0
    
    def test_recommend_articles(self):
        """Test article recommendation"""
        recommender = ContentBasedRecommender()
        
        articles = [
            {
                "title": "AI Breakthrough in NLP",
                "content": "New AI model shows unprecedented performance in natural language processing tasks."
            },
            {
                "title": "Machine Learning in Healthcare",
                "content": "Healthcare providers are adopting machine learning for better diagnostics."
            },
            {
                "title": "Sports News Today",
                "content": "Latest updates from the world of sports and athletics."
            }
        ]
        
        # Test recommendation for AI-focused user
        recommendations = recommender.recommend_articles(
            user_id="test_user",
            articles=articles,
            topics=["AI", "technology"],
            top_k=2
        )
        
        assert len(recommendations) <= 2
        for article, score in recommendations:
            assert score >= 0
            assert score <= 1
    
    def test_user_profile_management(self):
        """Test user profile management"""
        recommender = ContentBasedRecommender()
        
        # Test getting existing user
        profile = recommender.get_user_profile("user123")
        assert profile is not None
        assert profile.user_id == "user123"
        
        # Test getting non-existing user
        profile = recommender.get_user_profile("new_user")
        assert profile is None
    
    def test_update_user_profile(self):
        """Test user profile updates"""
        recommender = ContentBasedRecommender()
        
        # Test updating new user
        recommender.update_user_profile("new_user", clicked_article_id="article1")
        profile = recommender.get_user_profile("new_user")
        assert profile is not None
        assert "article1" in profile.click_history
        
        # Test updating existing user
        recommender.update_user_profile("user123", favorited_article_id="article2")
        profile = recommender.get_user_profile("user123")
        assert "article2" in profile.favorite_articles

def test_get_recommender():
    """Test the global recommender instance"""
    from app.recommender import get_recommender
    
    recommender1 = get_recommender()
    recommender2 = get_recommender()
    assert recommender1 is recommender2  # Should be the same instance 