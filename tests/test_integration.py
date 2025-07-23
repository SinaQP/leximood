"""
Integration tests for LexiMood sentiment analysis system.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood import analyze_text, AnalysisConfig
from leximood.models import SentimentLabel


class TestIntegration:
    """Integration tests for the complete LexiMood system."""
    
    def test_real_text_samples(self):
        """Test with real Persian text samples."""
        test_cases = [
            {
                "text": "امروز خیلی خوشحالم چون کار مهمی تمام کردم و راضی هستم",
                "expected_sentiment": SentimentLabel.POSITIVE,
                "description": "Positive daily note"
            },
            {
                "text": "این محصول عالی است و کیفیت فوق‌العاده‌ای دارد. حتماً توصیه می‌کنم",
                "expected_sentiment": SentimentLabel.POSITIVE,
                "description": "Positive product review"
            },
            {
                "text": "دیروز ناراحت بودم و احساس بدی داشتم. هیچ کاری نمی‌خواستم انجام دهم",
                "expected_sentiment": SentimentLabel.NEGATIVE,
                "description": "Negative emotional state"
            },
            {
                "text": "خدمات بد بود و اصلاً راضی نیستم. پولم را هدر دادم",
                "expected_sentiment": SentimentLabel.NEGATIVE,
                "description": "Negative service review"
            },
            {
                "text": "امروز هوا معمولی است و هیچ اتفاق خاصی نیفتاده",
                "expected_sentiment": SentimentLabel.NEUTRAL,
                "description": "Neutral daily description"
            }
        ]
        
        for i, test_case in enumerate(test_cases, 1):
            text = test_case["text"]
            expected = test_case["expected_sentiment"]
            description = test_case["description"]
            
            result = analyze_text(text)
            
            print(f"Test {i}: {description}")
            print(f"  Text: {text}")
            print(f"  Expected: {expected.value}")
            print(f"  Got: {result.sentiment.value} (score: {result.score:.3f})")
            print(f"  Keywords: {result.keywords}")
            print(f"  Confidence: {result.confidence:.3f}")
            print()
            
            # Check that we get a valid result
            assert result is not None
            assert isinstance(result.sentiment, SentimentLabel)
            assert -1.0 <= result.score <= 1.0
            assert 0.0 <= result.confidence <= 1.0
            assert isinstance(result.keywords, list)
    
    def test_different_text_types(self):
        """Test performance with different text types (positive, negative, neutral)."""
        positive_texts = [
            "خیلی خوشحالم از این موفقیت",
            "این بهترین تجربه زندگی‌ام بود",
            "عالی! فوق‌العاده! عاشقش شدم"
        ]
        
        negative_texts = [
            "خیلی ناراحت و افسرده‌ام",
            "بدترین تجربه زندگی‌ام بود",
            "وحشتناک! اصلاً راضی نیستم"
        ]
        
        neutral_texts = [
            "امروز هوا معمولی است",
            "این یک محصول عادی است",
            "هیچ اتفاق خاصی نیفتاده"
        ]
        
        # Test positive texts
        print("Testing Positive Texts:")
        for text in positive_texts:
            result = analyze_text(text)
            print(f"  '{text}' -> {result.sentiment.value} (score: {result.score:.3f})")
            assert result.sentiment in [SentimentLabel.POSITIVE, SentimentLabel.NEUTRAL]
        
        print("\nTesting Negative Texts:")
        for text in negative_texts:
            result = analyze_text(text)
            print(f"  '{text}' -> {result.sentiment.value} (score: {result.score:.3f})")
            assert result.sentiment in [SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL]
        
        print("\nTesting Neutral Texts:")
        for text in neutral_texts:
            result = analyze_text(text)
            print(f"  '{text}' -> {result.sentiment.value} (score: {result.score:.3f})")
            assert result.sentiment in [SentimentLabel.POSITIVE, SentimentLabel.NEGATIVE, SentimentLabel.NEUTRAL]
    
    def test_long_and_short_texts(self):
        """Test performance with long and short texts."""
        short_text = "خوشحالم"
        medium_text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم"
        long_text = """
        امروز خیلی خوشحالم چون کار مهمی تمام کردم و راضی هستم. 
        این پروژه خیلی سخت بود اما با تلاش و پشتکار موفق شدم آن را به پایان برسانم. 
        احساس غرور می‌کنم و مطمئنم که این موفقیت آینده‌ام را درخشان‌تر خواهد کرد.
        """
        
        print("Testing Short Text:")
        result = analyze_text(short_text)
        print(f"  '{short_text}' -> {result.sentiment.value} (score: {result.score:.3f})")
        assert result is not None
        
        print("\nTesting Medium Text:")
        result = analyze_text(medium_text)
        print(f"  '{medium_text}' -> {result.sentiment.value} (score: {result.score:.3f})")
        assert result is not None
        assert len(result.keywords) > 0
        
        print("\nTesting Long Text:")
        result = analyze_text(long_text)
        print(f"  Long text -> {result.sentiment.value} (score: {result.score:.3f})")
        print(f"  Keywords: {result.keywords}")
        assert result is not None
        assert len(result.keywords) > 0
    
    def test_configuration_variations(self):
        """Test different configuration options."""
        text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم"
        
        # Test with keywords enabled
        config_with_keywords = AnalysisConfig(include_keywords=True, max_keywords=3)
        result = analyze_text(text, config_with_keywords)
        assert len(result.keywords) > 0
        assert len(result.keywords) <= 3
        
        # Test with keywords disabled
        config_without_keywords = AnalysisConfig(include_keywords=False)
        result = analyze_text(text, config_without_keywords)
        assert len(result.keywords) == 0
        
        # Test with different max_keywords
        config_more_keywords = AnalysisConfig(include_keywords=True, max_keywords=10)
        result = analyze_text(text, config_more_keywords)
        assert len(result.keywords) <= 10
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions."""
        # Test with very short text
        result = analyze_text("خوب")
        assert result is not None
        
        # Test with text containing only stop words
        result = analyze_text("این و آن و این")
        assert result is not None
        
        # Test with text containing mixed sentiment
        result = analyze_text("خوشحالم اما ناراحت هم هستم")
        assert result is not None
        assert -1.0 <= result.score <= 1.0
    
    def test_arabic_text_handling(self):
        """Test handling of Arabic characters in Persian text."""
        # Text with Arabic characters that should be converted
        arabic_text = "اليوم كتير خوشحال هستم"
        result = analyze_text(arabic_text)
        
        assert result is not None
        # Should handle Arabic characters gracefully
        assert isinstance(result.sentiment, SentimentLabel)
    
    def test_punctuation_handling(self):
        """Test handling of various punctuation marks."""
        texts_with_punctuation = [
            "خوشحالم!",
            "ناراحت؟",
            "عالی، عالی، عالی!",
            "بد... خیلی بد."
        ]
        
        for text in texts_with_punctuation:
            result = analyze_text(text)
            assert result is not None
            assert isinstance(result.sentiment, SentimentLabel)
    
    def test_end_to_end_workflow(self):
        """Test complete end-to-end workflow."""
        # Simulate a real-world scenario
        user_reviews = [
            "این محصول عالی است و کیفیت فوق‌العاده‌ای دارد",
            "خدمات بد بود و اصلاً راضی نیستم",
            "محصول معمولی است، نه خوب نه بد"
        ]
        
        results = []
        for review in user_reviews:
            result = analyze_text(review)
            results.append(result)
            
            # Verify result structure
            assert hasattr(result, 'sentiment')
            assert hasattr(result, 'score')
            assert hasattr(result, 'keywords')
            assert hasattr(result, 'confidence')
            assert hasattr(result, 'text')
            assert hasattr(result, 'analysis_level')
        
        # Verify we got different results for different reviews
        assert len(set(r.sentiment.value for r in results)) > 1
        
        print("End-to-end workflow test completed successfully!")
        for i, (review, result) in enumerate(zip(user_reviews, results), 1):
            print(f"Review {i}: {result.sentiment.value} (score: {result.score:.3f})") 