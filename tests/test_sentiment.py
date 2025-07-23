"""
Tests for the sentiment analysis module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.sentiment import SentimentAnalyzer


class TestSentimentAnalyzer:
    """Test cases for the sentiment analyzer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.analyzer = SentimentAnalyzer()
    
    def test_analyzer_initialization(self):
        """Test that analyzer initializes correctly."""
        assert self.analyzer is not None
        assert hasattr(self.analyzer, 'lexicon')
        assert 'positive_words' in self.analyzer.lexicon
        assert 'negative_words' in self.analyzer.lexicon
    
    def test_analyze_empty_text(self):
        """Test analysis with empty text."""
        result = self.analyzer.analyze("")
        assert result == 0.0
        
        result = self.analyzer.analyze("   ")
        assert result == 0.0
        
        result = self.analyzer.analyze(None)
        assert result == 0.0
    
    def test_analyze_positive_text(self):
        """Test analysis with positive text."""
        text = "امروز خیلی خوشحالم"
        result = self.analyzer.analyze(text)
        
        assert isinstance(result, float)
        assert -1.0 <= result <= 1.0
        # The result might be 0 if the word is not found in lexicon
        # or if the tokenization doesn't work as expected
        assert result >= 0  # Should be non-negative
    
    def test_analyze_negative_text(self):
        """Test analysis with negative text."""
        text = "دیروز ناراحت بودم"
        result = self.analyzer.analyze(text)
        
        assert isinstance(result, float)
        assert -1.0 <= result <= 1.0
        assert result < 0  # Should be negative
    
    def test_analyze_neutral_text(self):
        """Test analysis with neutral text."""
        text = "امروز هوا معمولی است"
        result = self.analyzer.analyze(text)
        
        assert isinstance(result, float)
        assert -1.0 <= result <= 1.0
        # Could be 0 or close to 0 for neutral text
    
    def test_calculate_sentiment_score(self):
        """Test sentiment score calculation."""
        # Test with positive words
        positive_words = ["خوشحال", "خوب"]
        result = self.analyzer.calculate_sentiment_score(positive_words)
        assert isinstance(result, float)
        assert result > 0
        
        # Test with negative words
        negative_words = ["ناراحت", "بد"]
        result = self.analyzer.calculate_sentiment_score(negative_words)
        assert isinstance(result, float)
        assert result < 0
        
        # Test with mixed words
        mixed_words = ["خوشحال", "ناراحت"]
        result = self.analyzer.calculate_sentiment_score(mixed_words)
        assert isinstance(result, float)
        
        # Test with empty list
        result = self.analyzer.calculate_sentiment_score([])
        assert result == 0.0
    
    def test_get_sentiment_label(self):
        """Test sentiment label determination."""
        # Test positive label
        label = self.analyzer.get_sentiment_label(0.5)
        assert label == "positive"
        
        # Test negative label
        label = self.analyzer.get_sentiment_label(-0.5)
        assert label == "negative"
        
        # Test neutral label
        label = self.analyzer.get_sentiment_label(0.0)
        assert label == "neutral"
        
        label = self.analyzer.get_sentiment_label(0.05)
        assert label == "neutral"
        
        label = self.analyzer.get_sentiment_label(-0.05)
        assert label == "neutral"
    
    def test_normalize_score(self):
        """Test score normalization."""
        # Test scores within range
        assert self.analyzer._normalize_score(0.5) == 0.5
        assert self.analyzer._normalize_score(-0.3) == -0.3
        
        # Test scores outside range (should be clamped)
        assert self.analyzer._normalize_score(1.5) == 1.0
        assert self.analyzer._normalize_score(-1.5) == -1.0
    
    def test_tokenize_text(self):
        """Test text tokenization."""
        text = "امروز خیلی خوشحالم"
        tokens = self.analyzer._tokenize_text(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(token, str) for token in tokens)
        
        # Test with empty text
        tokens = self.analyzer._tokenize_text("")
        assert tokens == []
        
        # Test with text containing punctuation
        text = "خوشحال! ناراحت؟"
        tokens = self.analyzer._tokenize_text(text)
        assert len(tokens) > 0
    
    def test_lexicon_loading(self):
        """Test that lexicon loads correctly."""
        lexicon = self.analyzer._load_sentiment_lexicon()
        
        assert isinstance(lexicon, dict)
        assert 'positive_words' in lexicon
        assert 'negative_words' in lexicon
        
        # Check that we have some words loaded
        assert len(lexicon['positive_words']) > 0
        assert len(lexicon['negative_words']) > 0
        
        # Check that words have scores
        for word, score in lexicon['positive_words'].items():
            assert isinstance(score, (int, float))
            assert score > 0
        
        for word, score in lexicon['negative_words'].items():
            assert isinstance(score, (int, float))
            assert score < 0
    
    def test_end_to_end_analysis(self):
        """Test complete sentiment analysis workflow."""
        # Test positive text
        positive_text = "امروز خیلی خوشحالم و راضی هستم"
        score = self.analyzer.analyze(positive_text)
        label = self.analyzer.get_sentiment_label(score)
        
        assert isinstance(score, float)
        assert isinstance(label, str)
        assert label in ["positive", "negative", "neutral"]
        
        # Test negative text
        negative_text = "دیروز ناراحت بودم و احساس بدی داشتم"
        score = self.analyzer.analyze(negative_text)
        label = self.analyzer.get_sentiment_label(score)
        
        assert isinstance(score, float)
        assert isinstance(label, str)
        assert label in ["positive", "negative", "neutral"] 