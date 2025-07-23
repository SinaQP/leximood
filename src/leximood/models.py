"""
Data models for LexiMood sentiment analysis results.
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum
from .constants import (
    SENTIMENT_SCORE_MIN, SENTIMENT_SCORE_MAX,
    CONFIDENCE_MIN, CONFIDENCE_MAX
)


class SentimentLabel(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"


@dataclass
class AnalysisResult:
    sentiment: SentimentLabel
    score: float
    keywords: List[str]
    confidence: float
    text: str
    analysis_level: str
    
    def __post_init__(self):
        self._validate_score()
        self._validate_confidence()
    
    def _validate_score(self):
        if SENTIMENT_SCORE_MIN <= self.score <= SENTIMENT_SCORE_MAX:
            return
        
        raise ValueError(f"score must be between {SENTIMENT_SCORE_MIN} and {SENTIMENT_SCORE_MAX}")
    
    def _validate_confidence(self):
        if CONFIDENCE_MIN <= self.confidence <= CONFIDENCE_MAX:
            return
        
        raise ValueError(f"confidence must be between {CONFIDENCE_MIN} and {CONFIDENCE_MAX}")
    
    def to_dict(self) -> dict:
        return {
            "sentiment": self.sentiment.value,
            "score": self.score,
            "keywords": self.keywords,
            "confidence": self.confidence,
            "text": self.text,
            "analysis_level": self.analysis_level
        }
    
    def __str__(self) -> str:
        return f"AnalysisResult(sentiment={self.sentiment.value}, score={self.score:.3f}, confidence={self.confidence:.3f})" 