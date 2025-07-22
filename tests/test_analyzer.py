"""
Tests for the main analyzer module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.analyzer import analyze_text, LexiMoodAnalyzer
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
    
    def test_leximood_analyzer_class(self):
        """Test LexiMoodAnalyzer class directly."""
        analyzer = LexiMoodAnalyzer()
        text = "متن تست"
        result = analyzer.analyze(text)
        
        assert result is not None
        assert result.text == text 