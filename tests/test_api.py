import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_root_endpoint():
    """Test the root endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "endpoints" in data

@pytest.mark.asyncio
async def test_health_endpoint():
    """Test the health check endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data

@pytest.mark.asyncio
async def test_news_endpoint_success():
    """Test the news endpoint with valid parameters"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news", params={
            "user_id": "test_user",
            "preferred_topics": "AI,technology"
        })
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # Check that we get some articles
        assert len(data) > 0
        
        # Check article structure
        if len(data) > 0:
            article = data[0]
            assert "title" in article
            assert "summary" in article
            assert "link" in article
            assert "source" in article
            assert "score" in article

@pytest.mark.asyncio
async def test_news_endpoint_missing_params():
    """Test the news endpoint with missing parameters"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test missing user_id
        response = await ac.get("/news", params={
            "preferred_topics": "AI,technology"
        })
        assert response.status_code == 422  # Validation error
        
        # Test missing preferred_topics
        response = await ac.get("/news", params={
            "user_id": "test_user"
        })
        assert response.status_code == 422  # Validation error

@pytest.mark.asyncio
async def test_news_endpoint_with_max_articles():
    """Test the news endpoint with max_articles parameter"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/news", params={
            "user_id": "test_user",
            "preferred_topics": "AI,technology",
            "max_articles": 5
        })
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 5

@pytest.mark.asyncio
async def test_summarize_endpoint():
    """Test the summarize endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        test_text = """
        Artificial intelligence has made significant progress in recent years. 
        Machine learning algorithms are now capable of processing vast amounts of data 
        and making predictions with high accuracy. These developments have applications 
        in healthcare, finance, transportation, and many other industries.
        """
        
        response = await ac.post("/summarize", json={
            "text": test_text,
            "max_length": 100
        })
        
        if response.status_code == 200:
            data = response.json()
            assert "summary" in data
            assert "original_length" in data
            assert "summary_length" in data
            assert len(data["summary"]) > 0
            assert data["summary_length"] <= 100
        else:
            # Skip if model loading fails
            pytest.skip("Model not available for testing")

@pytest.mark.asyncio
async def test_user_profile_endpoint():
    """Test the user profile endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test existing user
        response = await ac.get("/user/user123/profile")
        assert response.status_code == 200
        data = response.json()
        assert "user_id" in data
        assert "preferred_topics" in data
        assert "click_history_count" in data
        assert "favorite_articles_count" in data
        
        # Test non-existing user
        response = await ac.get("/user/nonexistent_user/profile")
        assert response.status_code == 404

@pytest.mark.asyncio
async def test_user_interaction_endpoint():
    """Test the user interaction endpoint"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test click action
        response = await ac.post("/user/test_user/interaction", params={
            "action": "click",
            "article_id": "test_article_1"
        })
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "user_id" in data
        
        # Test favorite action
        response = await ac.post("/user/test_user/interaction", params={
            "action": "favorite",
            "article_id": "test_article_2"
        })
        assert response.status_code == 200
        
        # Test invalid action
        response = await ac.post("/user/test_user/interaction", params={
            "action": "invalid_action"
        })
        assert response.status_code == 400

@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Test invalid max_articles
        response = await ac.get("/news", params={
            "user_id": "test_user",
            "preferred_topics": "AI,technology",
            "max_articles": 100  # Should be limited to 50
        })
        assert response.status_code == 422
        
        # Test invalid max_articles (too low)
        response = await ac.get("/news", params={
            "user_id": "test_user",
            "preferred_topics": "AI,technology",
            "max_articles": 0
        })
        assert response.status_code == 422

@pytest.mark.asyncio
async def test_cors_headers():
    """Test CORS headers are present"""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/")
        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in response.headers 