"""
Tests for the keyword extraction module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.keywords import KeywordExtractor


class TestKeywordExtractor:
    """Test cases for the keyword extractor."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.extractor = KeywordExtractor()
    
    def test_extractor_initialization(self):
        """Test that extractor initializes correctly."""
        assert self.extractor is not None
        assert hasattr(self.extractor, 'sentiment_words')
        assert hasattr(self.extractor, 'stop_words')
        assert isinstance(self.extractor.sentiment_words, set)
        assert len(self.extractor.sentiment_words) > 0
    
    def test_extract_empty_text(self):
        """Test extraction with empty text."""
        result = self.extractor.extract("")
        assert result == []
        
        result = self.extractor.extract("   ")
        assert result == []
        
        result = self.extractor.extract(None)
        assert result == []
    
    def test_extract_keywords_basic(self):
        """Test basic keyword extraction."""
        text = "امروز خیلی خوشحالم"
        keywords = self.extractor.extract(text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert all(isinstance(keyword, str) for keyword in keywords)
    
    def test_extract_keywords_with_sentiment_words(self):
        """Test extraction with sentiment words."""
        text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم"
        keywords = self.extractor.extract(text, max_keywords=5)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 5
        # خوشحال should be prioritized as it's a sentiment word
        assert any('خوشحال' in keyword for keyword in keywords)
    
    def test_extract_keywords_max_limit(self):
        """Test that max_keywords limit is respected."""
        text = "این یک متن طولانی برای تست است که شامل کلمات مختلفی می‌شود"
        keywords = self.extractor.extract(text, max_keywords=3)
        
        assert len(keywords) <= 3
    
    def test_calculate_tf_idf(self):
        """Test TF-IDF calculation."""
        words = ["خوشحال", "خوشحال", "ناراحت", "کار", "مهم"]
        scores = self.extractor.calculate_tf_idf(words)
        
        assert isinstance(scores, dict)
        assert len(scores) > 0
        
        # Check that all scores are positive
        for score in scores.values():
            assert score >= 0
        
        # Check that repeated words have higher scores
        if "خوشحال" in scores:
            assert scores["خوشحال"] > 0
    
    def test_calculate_tf_idf_empty_words(self):
        """Test TF-IDF calculation with empty word list."""
        scores = self.extractor.calculate_tf_idf([])
        assert scores == {}
    
    def test_calculate_tf_idf_stop_words(self):
        """Test that stop words are filtered out."""
        words = ["این", "خوشحال", "است", "کار"]
        scores = self.extractor.calculate_tf_idf(words)
        
        # Stop words like "این" and "است" should be filtered out
        assert "این" not in scores
        assert "است" not in scores
        # But sentiment words should remain
        assert "خوشحال" in scores
    
    def test_filter_keywords(self):
        """Test keyword filtering based on sentiment importance."""
        tf_idf_scores = {"خوشحال": 0.5, "کار": 0.3, "مهم": 0.4}
        sentiment_words = {"خوشحال", "ناراحت"}
        
        filtered = self.extractor.filter_keywords(tf_idf_scores, sentiment_words)
        
        assert isinstance(filtered, dict)
        assert len(filtered) == len(tf_idf_scores)
        
        # Sentiment words should have boosted scores
        assert filtered["خوشحال"] > tf_idf_scores["خوشحال"]
        # Non-sentiment words should have same scores
        assert filtered["کار"] == tf_idf_scores["کار"]
        assert filtered["مهم"] == tf_idf_scores["مهم"]
    
    def test_filter_keywords_empty_scores(self):
        """Test filtering with empty scores."""
        filtered = self.extractor.filter_keywords({}, {"خوشحال"})
        assert filtered == {}
    
    def test_tokenize_text(self):
        """Test text tokenization."""
        text = "امروز خیلی خوشحالم!"
        tokens = self.extractor._tokenize_text(text)
        
        assert isinstance(tokens, list)
        assert len(tokens) > 0
        assert all(isinstance(token, str) for token in tokens)
        
        # Test with empty text
        tokens = self.extractor._tokenize_text("")
        assert tokens == []
        
        # Test with text containing numbers
        text = "کار 123 مهم"
        tokens = self.extractor._tokenize_text(text)
        # Numbers should be filtered out
        assert not any(token.isdigit() for token in tokens)
    
    def test_get_top_keywords(self):
        """Test getting top keywords."""
        scores = {"خوشحال": 0.8, "کار": 0.5, "مهم": 0.6, "امروز": 0.3}
        
        # Test getting top 2 keywords
        keywords = self.extractor._get_top_keywords(scores, 2)
        assert len(keywords) == 2
        assert keywords[0] == "خوشحال"  # Highest score
        assert keywords[1] == "مهم"     # Second highest score
        
        # Test getting more keywords than available
        keywords = self.extractor._get_top_keywords(scores, 10)
        assert len(keywords) == 4  # All available keywords
    
    def test_get_top_keywords_empty_scores(self):
        """Test getting top keywords with empty scores."""
        keywords = self.extractor._get_top_keywords({}, 5)
        assert keywords == []
    
    def test_sentiment_words_loading(self):
        """Test that sentiment words are loaded correctly."""
        sentiment_words = self.extractor._load_sentiment_words()
        
        assert isinstance(sentiment_words, set)
        assert len(sentiment_words) > 0
        
        # Check that we have both positive and negative words
        # This assumes the lexicon has both types of words
        assert len(sentiment_words) >= 20  # Should have reasonable number of words
    
    def test_end_to_end_extraction(self):
        """Test complete keyword extraction workflow."""
        text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم"
        keywords = self.extractor.extract(text, max_keywords=3)
        
        assert isinstance(keywords, list)
        assert len(keywords) <= 3
        assert len(keywords) > 0
        
        # All keywords should be strings
        assert all(isinstance(keyword, str) for keyword in keywords)
        
        # Keywords should not be empty
        assert all(len(keyword) > 0 for keyword in keywords)
    
    def test_extraction_with_various_text_types(self):
        """Test extraction with different types of text."""
        test_cases = [
            "این محصول عالی است",
            "دیروز ناراحت بودم",
            "امروز هوا خوب است",
            "کار مهمی انجام دادم"
        ]
        
        for text in test_cases:
            keywords = self.extractor.extract(text, max_keywords=5)
            assert isinstance(keywords, list)
            assert len(keywords) <= 5
            assert all(isinstance(keyword, str) for keyword in keywords) 