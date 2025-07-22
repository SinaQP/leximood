"""
Data models for LexiMood sentiment analysis results.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class SentimentLabel(Enum):
    """Sentiment label enumeration."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class AnalysisResult:
    """
    Result of sentiment analysis.
    
    Attributes:
        sentiment: Sentiment label (positive, negative, neutral)
        score: Sentiment score between -1 and 1
        keywords: List of extracted keywords
        confidence: Confidence score of the analysis
        text: Original text that was analyzed
        analysis_level: Level of analysis performed
    """
    
    sentiment: SentimentLabel
    score: float
    keywords: List[str]
    confidence: float
    text: str
    analysis_level: str
    
    def __post_init__(self):
        """Validate result parameters."""
        if not -1.0 <= self.score <= 1.0:
            raise ValueError("score must be between -1.0 and 1.0")
        
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("confidence must be between 0.0 and 1.0")
    
    def to_dict(self) -> dict:
        """Convert result to dictionary."""
        return {
            "sentiment": self.sentiment.value,
            "score": self.score,
            "keywords": self.keywords,
            "confidence": self.confidence,
            "text": self.text,
            "analysis_level": self.analysis_level
        }
    
    def __str__(self) -> str:
        """String representation of the result."""
        return f"AnalysisResult(sentiment={self.sentiment.value}, score={self.score:.3f}, confidence={self.confidence:.3f})" 