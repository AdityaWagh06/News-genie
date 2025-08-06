import logging
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import List, Optional
import os
from dotenv import load_dotenv

# Import local modules
from app.models import NewsArticle, SummarizationRequest, SummarizationResponse
from app.summarizer import get_summarizer
from app.recommender import get_recommender
from app.utils import get_news_client, validate_topics, format_article_for_response, log_api_request

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="NewsGenie API",
    description="AI-powered news summarization and recommendation service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    logger.info("Starting NewsGenie API...")
    
    # Initialize components
    try:
        get_summarizer()
        get_recommender()
        get_news_client()
        logger.info("All components initialized successfully")
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Welcome to NewsGenie API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "news": "/news",
            "summarize": "/summarize",
            "health": "/health"
        }
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "version": "1.0.0"
    }

@app.get("/news", response_model=List[NewsArticle], tags=["News"])
async def get_personalized_news(
    user_id: str = Query(..., description="User identifier"),
    preferred_topics: str = Query(..., description="Comma-separated list of preferred topics (e.g., 'AI,politics,sports')"),
    max_articles: int = Query(10, description="Maximum number of articles to return", ge=1, le=50)
):
    """
    Get personalized and summarized news articles.
    
    This endpoint fetches news articles based on user preferences,
    summarizes them using BART, and ranks them using a content-based
    recommendation engine.
    """
    try:
        # Validate and parse topics
        topics = validate_topics(preferred_topics)
        logger.info(f"Processing request for user {user_id} with topics: {topics}")
        
        # Fetch news articles
        news_client = get_news_client()
        articles = news_client.fetch_news(topics, max_articles * 2)  # Fetch more for better recommendations
        
        if not articles:
            logger.warning(f"No articles found for topics: {topics}")
            return []
        
        # Get summarizer and recommender
        summarizer = get_summarizer()
        recommender = get_recommender()
        
        # Summarize articles
        summaries = []
        for article in articles:
            content = article.get('content', '') or article.get('description', '')
            if content:
                summary = summarizer.summarize(content, max_length=150)
                summaries.append(summary)
            else:
                summaries.append("No content available for summarization.")
        
        # Get recommendations
        recommendations = recommender.recommend_articles(
            user_id=user_id,
            articles=articles,
            topics=topics,
            top_k=max_articles
        )
        
        # Format response
        response_articles = []
        for (article, score), summary in zip(recommendations, summaries[:len(recommendations)]):
            formatted_article = format_article_for_response(article, summary, score)
            response_articles.append(formatted_article)
        
        # Log the request
        log_api_request(user_id, topics, len(response_articles))
        
        logger.info(f"Successfully processed request: {len(response_articles)} articles returned")
        return response_articles
        
    except Exception as e:
        logger.error(f"Error processing news request: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/summarize", response_model=SummarizationResponse, tags=["AI"])
async def summarize_text(request: SummarizationRequest):
    """
    Summarize text using BART model.
    
    This endpoint uses the facebook/bart-large-cnn model to generate
    abstractive summaries of the provided text.
    """
    try:
        summarizer = get_summarizer()
        
        # Generate summary
        summary = summarizer.summarize(
            text=request.text,
            max_length=request.max_length
        )
        
        return SummarizationResponse(
            summary=summary,
            original_length=len(request.text),
            summary_length=len(summary)
        )
        
    except Exception as e:
        logger.error(f"Error in summarization: {e}")
        raise HTTPException(status_code=500, detail=f"Summarization error: {str(e)}")

@app.get("/user/{user_id}/profile", tags=["User"])
async def get_user_profile(user_id: str):
    """
    Get user profile and preferences.
    """
    try:
        recommender = get_recommender()
        profile = recommender.get_user_profile(user_id)
        
        if not profile:
            raise HTTPException(status_code=404, detail="User profile not found")
        
        return {
            "user_id": profile.user_id,
            "preferred_topics": profile.preferred_topics,
            "click_history_count": len(profile.click_history),
            "favorite_articles_count": len(profile.favorite_articles)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.post("/user/{user_id}/interaction", tags=["User"])
async def record_user_interaction(
    user_id: str,
    article_id: Optional[str] = None,
    action: str = Query(..., description="Action type: 'click' or 'favorite'")
):
    """
    Record user interaction with articles.
    """
    try:
        recommender = get_recommender()
        
        if action == "click":
            recommender.update_user_profile(user_id, clicked_article_id=article_id)
        elif action == "favorite":
            recommender.update_user_profile(user_id, favorited_article_id=article_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid action. Use 'click' or 'favorite'")
        
        return {"message": f"Interaction recorded: {action}", "user_id": user_id}
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error recording user interaction: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 