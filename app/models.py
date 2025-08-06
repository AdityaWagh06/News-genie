from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class NewsRequest(BaseModel):
    """Request model for news endpoint"""
    user_id: str = Field(..., description="User identifier")
    preferred_topics: str = Field(..., description="Comma-separated list of preferred topics")

class NewsArticle(BaseModel):
    """Model for a news article"""
    title: str = Field(..., description="Article title")
    summary: str = Field(..., description="AI-generated summary")
    link: str = Field(..., description="Original article URL")
    source: str = Field(..., description="News source name")
    score: float = Field(..., description="Recommendation score (0-1)")
    published_at: Optional[datetime] = Field(None, description="Publication date")
    content: Optional[str] = Field(None, description="Original article content")

class UserProfile(BaseModel):
    """Model for user profile and preferences"""
    user_id: str
    preferred_topics: List[str]
    click_history: List[str] = Field(default_factory=list, description="List of clicked article IDs")
    favorite_articles: List[str] = Field(default_factory=list, description="List of favorited article IDs")

class SummarizationRequest(BaseModel):
    """Request model for summarization endpoint"""
    text: str = Field(..., description="Text to summarize", min_length=50)
    max_length: int = Field(default=150, description="Maximum summary length", ge=50, le=500)

class SummarizationResponse(BaseModel):
    """Response model for summarization endpoint"""
    summary: str = Field(..., description="Generated summary")
    original_length: int = Field(..., description="Original text length")
    summary_length: int = Field(..., description="Summary length") 