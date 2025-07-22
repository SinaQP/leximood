"""
Tests for the data models module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.models import AnalysisResult, SentimentLabel


class TestAnalysisResult:
    """Test cases for AnalysisResult class."""
    
    def test_valid_result(self):
        """Test creating a valid analysis result."""
        result = AnalysisResult(
            sentiment=SentimentLabel.POSITIVE,
            score=0.8,
            keywords=["خوب", "عالی"],
            confidence=0.9,
            text="امروز روز خوبی بود",
            analysis_level="sentence"
        )
        
        assert result.sentiment == SentimentLabel.POSITIVE
        assert result.score == 0.8
        assert result.keywords == ["خوب", "عالی"]
        assert result.confidence == 0.9
        assert result.text == "امروز روز خوبی بود"
        assert result.analysis_level == "sentence"
    
    def test_invalid_score(self):
        """Test validation of score parameter."""
        with pytest.raises(ValueError, match="score must be between -1.0 and 1.0"):
            AnalysisResult(
                sentiment=SentimentLabel.POSITIVE,
                score=1.5,
                keywords=[],
                confidence=0.5,
                text="test",
                analysis_level="sentence"
            )
        
        with pytest.raises(ValueError, match="score must be between -1.0 and 1.0"):
            AnalysisResult(
                sentiment=SentimentLabel.NEGATIVE,
                score=-1.5,
                keywords=[],
                confidence=0.5,
                text="test",
                analysis_level="sentence"
            )
    
    def test_invalid_confidence(self):
        """Test validation of confidence parameter."""
        with pytest.raises(ValueError, match="confidence must be between 0.0 and 1.0"):
            AnalysisResult(
                sentiment=SentimentLabel.NEUTRAL,
                score=0.0,
                keywords=[],
                confidence=1.5,
                text="test",
                analysis_level="sentence"
            )
    
    def test_to_dict(self):
        """Test conversion to dictionary."""
        result = AnalysisResult(
            sentiment=SentimentLabel.NEGATIVE,
            score=-0.5,
            keywords=["بد"],
            confidence=0.7,
            text="روز بدی بود",
            analysis_level="sentence"
        )
        
        result_dict = result.to_dict()
        
        assert result_dict["sentiment"] == "negative"
        assert result_dict["score"] == -0.5
        assert result_dict["keywords"] == ["بد"]
        assert result_dict["confidence"] == 0.7
        assert result_dict["text"] == "روز بدی بود"
        assert result_dict["analysis_level"] == "sentence"
    
    def test_str_representation(self):
        """Test string representation."""
        result = AnalysisResult(
            sentiment=SentimentLabel.NEUTRAL,
            score=0.0,
            keywords=[],
            confidence=0.5,
            text="test",
            analysis_level="sentence"
        )
        
        str_repr = str(result)
        assert "AnalysisResult" in str_repr
        assert "neutral" in str_repr
        assert "0.000" in str_repr


class TestSentimentLabel:
    """Test cases for SentimentLabel enumeration."""
    
    def test_sentiment_labels(self):
        """Test sentiment label values."""
        assert SentimentLabel.POSITIVE.value == "positive"
        assert SentimentLabel.NEGATIVE.value == "negative"
        assert SentimentLabel.NEUTRAL.value == "neutral" 