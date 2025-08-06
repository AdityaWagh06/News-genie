import logging
from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsSummarizer:
    """
    BART-based news summarization using facebook/bart-large-cnn model.
    Provides abstractive summarization for news articles.
    """
    
    def __init__(self, model_name: str = "facebook/bart-large-cnn"):
        """
        Initialize the summarizer with BART model.
        
        Args:
            model_name: Hugging Face model identifier
        """
        self.model_name = model_name
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        logger.info(f"Loading BART model: {model_name}")
        logger.info(f"Using device: {self.device}")
        
        try:
            self.tokenizer = BartTokenizer.from_pretrained(model_name)
            self.model = BartForConditionalGeneration.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info("BART model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading BART model: {e}")
            raise
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """
        Summarize the given text using BART.
        
        Args:
            text: Input text to summarize
            max_length: Maximum length of the summary
            min_length: Minimum length of the summary
            
        Returns:
            Summarized text
        """
        if not text or len(text.strip()) < 50:
            logger.warning("Input text too short for summarization")
            return text
        
        try:
            # Tokenize input text
            inputs = self.tokenizer(
                text,
                max_length=1024,  # BART's maximum input length
                truncation=True,
                padding=True,
                return_tensors="pt"
            )
            
            # Move inputs to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs["input_ids"],
                    attention_mask=inputs["attention_mask"],
                    max_length=max_length,
                    min_length=min_length,
                    num_beams=4,
                    length_penalty=2.0,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode the summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            
            logger.info(f"Successfully summarized text: {len(text)} chars -> {len(summary)} chars")
            return summary.strip()
            
        except Exception as e:
            logger.error(f"Error during summarization: {e}")
            # Return a fallback summary
            return self._fallback_summary(text)
    
    def _fallback_summary(self, text: str) -> str:
        """
        Fallback summarization method when BART fails.
        Creates a simple extractive summary.
        
        Args:
            text: Input text
            
        Returns:
            Simple summary
        """
        sentences = text.split('.')
        if len(sentences) <= 3:
            return text
        
        # Take first 3 sentences as fallback
        summary_sentences = sentences[:3]
        return '. '.join(summary_sentences) + '.'
    
    def batch_summarize(self, texts: list, max_length: int = 150) -> list:
        """
        Summarize multiple texts in batch.
        
        Args:
            texts: List of texts to summarize
            max_length: Maximum length of each summary
            
        Returns:
            List of summaries
        """
        summaries = []
        for i, text in enumerate(texts):
            logger.info(f"Summarizing text {i+1}/{len(texts)}")
            summary = self.summarize(text, max_length)
            summaries.append(summary)
        
        return summaries

# Global summarizer instance
_summarizer_instance: Optional[NewsSummarizer] = None

def get_summarizer() -> NewsSummarizer:
    """
    Get or create the global summarizer instance.
    
    Returns:
        NewsSummarizer instance
    """
    global _summarizer_instance
    if _summarizer_instance is None:
        _summarizer_instance = NewsSummarizer()
    return _summarizer_instance 