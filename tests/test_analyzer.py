"""
Tests for the main analyzer module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.analyzer import analyze_text, Analyzer
from leximood.config import AnalysisConfig
from leximood.models import SentimentLabel


class TestAnalyzer:
    """Test cases for the main analyzer."""
    
    def test_analyze_text_basic(self):
        """Test basic text analysis functionality."""
        text = "امروز روز خوبی است"
        result = analyze_text(text)
        
        assert result is not None
        assert hasattr(result, 'sentiment')
        assert hasattr(result, 'score')
        assert hasattr(result, 'keywords')
        assert hasattr(result, 'confidence')
        assert hasattr(result, 'text')
        assert hasattr(result, 'analysis_level')
        
        assert result.text == text
        assert isinstance(result.sentiment, SentimentLabel)
        assert -1.0 <= result.score <= 1.0
        assert 0.0 <= result.confidence <= 1.0
    
    def test_analyze_text_empty(self):
        """Test analysis with empty text."""
        with pytest.raises(ValueError, match="Text cannot be empty"):
            analyze_text("")
        
        with pytest.raises(ValueError, match="Text cannot be empty"):
            analyze_text("   ")
    
    def test_analyzer_with_config(self):
        """Test analyzer with custom configuration."""
        config = AnalysisConfig(
            include_keywords=False,
            max_keywords=3
        )
        
        text = "این یک متن تست است"
        result = analyze_text(text, config)
        
        assert result is not None
        assert result.analysis_level == "sentence"
        assert len(result.keywords) == 0  # Keywords disabled
    
    def test_analyzer_with_keywords_enabled(self):
        """Test analyzer with keywords enabled."""
        config = AnalysisConfig(
            include_keywords=True,
            max_keywords=3
        )
        
        text = "امروز خیلی خوشحالم"
        result = analyze_text(text, config)
        
        assert result is not None
        assert len(result.keywords) > 0
        assert len(result.keywords) <= 3
    
    def test_analyzer_class_directly(self):
        """Test Analyzer class directly."""
        analyzer = Analyzer()
        text = "متن تست"
        result = analyzer.analyze(text)
        
        assert result is not None
        assert result.text == text
        assert isinstance(result.sentiment, SentimentLabel)
    
    def test_sentiment_determination(self):
        """Test sentiment label determination."""
        # Test positive sentiment
        positive_text = "امروز خیلی خوشحالم"
        result = analyze_text(positive_text)
        assert result.sentiment in [SentimentLabel.POSITIVE, SentimentLabel.NEUTRAL]
        
        # Test negative sentiment
        negative_text = "دیروز ناراحت بودم"
        result = analyze_text(negative_text)
        assert result.sentiment in [SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL]
    
    def test_confidence_calculation(self):
        """Test confidence score calculation."""
        text = "امروز خیلی خوشحالم"
        result = analyze_text(text)
        
        assert 0.0 <= result.confidence <= 1.0
        assert isinstance(result.confidence, float)
    
    def test_analysis_result_structure(self):
        """Test that analysis result has correct structure."""
        text = "متن تست برای بررسی ساختار"
        result = analyze_text(text)
        
        # Check all required attributes exist
        required_attrs = ['sentiment', 'score', 'keywords', 'confidence', 'text', 'analysis_level']
        for attr in required_attrs:
            assert hasattr(result, attr)
        
        # Check data types
        assert isinstance(result.sentiment, SentimentLabel)
        assert isinstance(result.score, float)
        assert isinstance(result.keywords, list)
        assert isinstance(result.confidence, float)
        assert isinstance(result.text, str)
        assert isinstance(result.analysis_level, str) 