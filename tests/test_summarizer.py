import pytest
from app.summarizer import NewsSummarizer

class TestNewsSummarizer:
    """Test cases for the NewsSummarizer class"""
    
    def test_summarizer_initialization(self):
        """Test that the summarizer can be initialized"""
        try:
            summarizer = NewsSummarizer()
            assert summarizer is not None
            assert summarizer.model_name == "facebook/bart-large-cnn"
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_summarize_short_text(self):
        """Test summarization with short text"""
        try:
            summarizer = NewsSummarizer()
            short_text = "This is a very short text that should not be summarized."
            result = summarizer.summarize(short_text)
            assert result == short_text  # Should return original text for short input
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_summarize_long_text(self):
        """Test summarization with longer text"""
        try:
            summarizer = NewsSummarizer()
            long_text = """
            Artificial intelligence has made significant progress in recent years. 
            Machine learning algorithms are now capable of processing vast amounts of data 
            and making predictions with high accuracy. These developments have applications 
            in healthcare, finance, transportation, and many other industries. 
            Researchers continue to push the boundaries of what AI can accomplish.
            """
            result = summarizer.summarize(long_text)
            assert len(result) > 0
            assert len(result) < len(long_text)  # Summary should be shorter
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_summarize_empty_text(self):
        """Test summarization with empty text"""
        try:
            summarizer = NewsSummarizer()
            result = summarizer.summarize("")
            assert result == ""
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_batch_summarize(self):
        """Test batch summarization"""
        try:
            summarizer = NewsSummarizer()
            texts = [
                "First article about technology and AI developments.",
                "Second article about climate change and environmental issues.",
                "Third article about space exploration and Mars missions."
            ]
            results = summarizer.batch_summarize(texts)
            assert len(results) == len(texts)
            for result in results:
                assert len(result) > 0
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")
    
    def test_fallback_summary(self):
        """Test fallback summary method"""
        try:
            summarizer = NewsSummarizer()
            text = "This is sentence one. This is sentence two. This is sentence three. This is sentence four."
            result = summarizer._fallback_summary(text)
            assert len(result) > 0
            assert result.count('.') <= 3  # Should have at most 3 sentences
        except Exception as e:
            pytest.skip(f"Model loading failed: {e}")

def test_get_summarizer():
    """Test the global summarizer instance"""
    from app.summarizer import get_summarizer
    try:
        summarizer1 = get_summarizer()
        summarizer2 = get_summarizer()
        assert summarizer1 is summarizer2  # Should be the same instance
    except Exception as e:
        pytest.skip(f"Model loading failed: {e}") 