"""
Main analyzer module for LexiMood sentiment analysis.
"""

from typing import Optional
from .config import AnalysisConfig, AnalysisLevel
from .models import AnalysisResult, SentimentLabel
from .preprocessor import TextPreprocessor
from .sentiment import SentimentAnalyzer
from .keywords import KeywordExtractor


class Analyzer:
    """
    Main analyzer class for Persian sentiment analysis.
    """
    
    def __init__(self, config: Optional[AnalysisConfig] = None):
        """
        Initialize the analyzer with configuration.
        
        Args:
            config: Analysis configuration
        """
        self.config = config or AnalysisConfig()
        self.preprocessor = TextPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.keyword_extractor = KeywordExtractor()
    
    def analyze(self, text: str) -> AnalysisResult:
        """
        Analyze the sentiment of Persian text.
        
        Args:
            text: Persian text to analyze
            
        Returns:
            AnalysisResult containing sentiment analysis results
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")
        
        # Preprocess text
        processed_text = self.preprocessor.preprocess(text)
        
        # Analyze sentiment
        sentiment_score = self.sentiment_analyzer.analyze(processed_text)
        sentiment_label = self._get_sentiment_label(sentiment_score)
        
        # Extract keywords if enabled
        keywords = []
        if self.config.include_keywords:
            keywords = self.keyword_extractor.extract(
                processed_text, 
                max_keywords=self.config.max_keywords
            )
        
        # Calculate confidence
        confidence = self._calculate_confidence(sentiment_score, len(keywords))
        
        return AnalysisResult(
            sentiment=sentiment_label,
            score=sentiment_score,
            keywords=keywords,
            confidence=confidence,
            text=text,
            analysis_level=self.config.analysis_level.value
        )
    
    def _get_sentiment_label(self, score: float) -> SentimentLabel:
        """Determine sentiment label based on score."""
        if score > 0.1:
            return SentimentLabel.POSITIVE
        elif score < -0.1:
            return SentimentLabel.NEGATIVE
        else:
            return SentimentLabel.NEUTRAL
    
    def _calculate_confidence(self, score: float, keyword_count: int) -> float:
        """Calculate confidence score based on analysis results."""
        # Base confidence on absolute score value
        base_confidence = min(abs(score) * 2, 1.0)
        
        # Adjust based on keyword availability
        keyword_factor = min(keyword_count / 3, 1.0) * 0.2
        
        return min(base_confidence + keyword_factor, 1.0)


# Global analyzer instance
_analyzer = None


def analyze_text(text: str, config: Optional[AnalysisConfig] = None) -> AnalysisResult:
    """
    Analyze the sentiment of Persian text.
    
    This is the main function for sentiment analysis.
    
    Args:
        text: Persian text to analyze
        config: Optional configuration for analysis
        
    Returns:
        AnalysisResult containing sentiment analysis results
        
    Raises:
        ValueError: If text is empty or invalid
    """
    global _analyzer
    
    if _analyzer is None or config is not None:
        _analyzer = Analyzer(config)
    
    return _analyzer.analyze(text) 