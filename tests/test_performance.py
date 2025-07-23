"""
Performance tests for LexiMood sentiment analysis system.
"""

import sys
import os
import time
import random
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood import analyze_text, AnalysisConfig


class TestPerformance:
    """Performance tests for the LexiMood system."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Sample texts for performance testing
        self.sample_texts = [
            "امروز خیلی خوشحالم چون کار مهمی تمام کردم",
            "دیروز ناراحت بودم و احساس بدی داشتم",
            "این محصول عالی است و کیفیت فوق‌العاده‌ای دارد",
            "خدمات بد بود و اصلاً راضی نیستم",
            "امروز هوا معمولی است و هیچ اتفاق خاصی نیفتاده",
            "خیلی خوشحالم از این موفقیت",
            "بدترین تجربه زندگی‌ام بود",
            "محصول معمولی است، نه خوب نه بد",
            "عالی! فوق‌العاده! عاشقش شدم",
            "وحشتناک! اصلاً راضی نیستم"
        ]
    
    def test_processing_speed(self):
        """Measure processing speed for single text analysis."""
        text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم و راضی هستم"
        
        # Warm up
        for _ in range(5):
            analyze_text(text)
        
        # Measure processing time
        start_time = time.time()
        result = analyze_text(text)
        end_time = time.time()
        
        processing_time = end_time - start_time
        
        print(f"Single text processing time: {processing_time:.6f} seconds")
        print(f"Text length: {len(text)} characters")
        
        if processing_time > 0:
            print(f"Processing speed: {len(text) / processing_time:.0f} characters/second")
        else:
            print("Processing speed: Very fast (under measurement threshold)")
        
        # Assert reasonable performance (should be under 1 second)
        assert processing_time < 1.0
        assert result is not None
    
    def test_batch_processing_speed(self):
        """Measure processing speed for batch text analysis."""
        # Create a batch of texts
        batch_size = 50  # Reduced for faster testing
        batch_texts = random.choices(self.sample_texts, k=batch_size)
        
        # Warm up
        for _ in range(5):
            analyze_text(batch_texts[0])
        
        # Measure batch processing time
        start_time = time.time()
        results = []
        for text in batch_texts:
            result = analyze_text(text)
            results.append(result)
        end_time = time.time()
        
        total_time = end_time - start_time
        avg_time_per_text = total_time / batch_size
        
        print(f"Batch processing time: {total_time:.4f} seconds")
        print(f"Batch size: {batch_size} texts")
        print(f"Average time per text: {avg_time_per_text:.4f} seconds")
        print(f"Texts per second: {batch_size / total_time:.1f}")
        
        # Assert reasonable performance
        assert total_time < 30.0  # Should process 50 texts in under 30 seconds
        assert avg_time_per_text < 1.0  # Each text should take under 1 second
        assert len(results) == batch_size
    
    def test_high_volume_data(self):
        """Test with high volume data."""
        # Create a large dataset
        large_dataset_size = 100  # Reduced for faster testing
        large_dataset = random.choices(self.sample_texts, k=large_dataset_size)
        
        print(f"Testing with {large_dataset_size} texts...")
        
        start_time = time.time()
        results = []
        for i, text in enumerate(large_dataset):
            result = analyze_text(text)
            results.append(result)
            
            # Progress indicator
            if (i + 1) % 25 == 0:
                elapsed = time.time() - start_time
                print(f"Processed {i + 1}/{large_dataset_size} texts in {elapsed:.2f} seconds")
        
        total_time = time.time() - start_time
        
        print(f"High volume test completed:")
        print(f"  Total texts: {large_dataset_size}")
        print(f"  Total time: {total_time:.2f} seconds")
        print(f"  Average time per text: {total_time / large_dataset_size:.4f} seconds")
        print(f"  Texts per second: {large_dataset_size / total_time:.1f}")
        
        # Verify all results are valid
        assert len(results) == large_dataset_size
        for result in results:
            assert result is not None
            assert hasattr(result, 'sentiment')
            assert hasattr(result, 'score')
            assert hasattr(result, 'keywords')
            assert hasattr(result, 'confidence')
    
    def test_configuration_performance_impact(self):
        """Test how different configurations affect performance."""
        text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم و راضی هستم"
        
        # Test with keywords enabled
        config_with_keywords = AnalysisConfig(include_keywords=True, max_keywords=5)
        start_time = time.time()
        result_with_keywords = analyze_text(text, config_with_keywords)
        time_with_keywords = time.time() - start_time
        
        # Test with keywords disabled
        config_without_keywords = AnalysisConfig(include_keywords=False)
        start_time = time.time()
        result_without_keywords = analyze_text(text, config_without_keywords)
        time_without_keywords = time.time() - start_time
        
        print(f"Performance comparison:")
        print(f"  With keywords: {time_with_keywords:.4f} seconds")
        print(f"  Without keywords: {time_without_keywords:.4f} seconds")
        print(f"  Performance difference: {time_with_keywords - time_without_keywords:.4f} seconds")
        
        # Keywords should add some overhead but not be excessive
        assert time_with_keywords > time_without_keywords
        assert time_with_keywords - time_without_keywords < 0.1  # Should be under 100ms difference
        
        # Verify results
        assert len(result_with_keywords.keywords) > 0
        assert len(result_without_keywords.keywords) == 0
    
    def test_text_length_performance(self):
        """Test how text length affects performance."""
        short_text = "خوشحالم"
        medium_text = "امروز خیلی خوشحالم چون کار مهمی تمام کردم"
        long_text = """
        امروز خیلی خوشحالم چون کار مهمی تمام کردم و راضی هستم. 
        این پروژه خیلی سخت بود اما با تلاش و پشتکار موفق شدم آن را به پایان برسانم. 
        احساس غرور می‌کنم و مطمئنم که این موفقیت آینده‌ام را درخشان‌تر خواهد کرد.
        """
        
        # Measure processing times
        start_time = time.time()
        analyze_text(short_text)
        short_time = time.time() - start_time
        
        start_time = time.time()
        analyze_text(medium_text)
        medium_time = time.time() - start_time
        
        start_time = time.time()
        analyze_text(long_text)
        long_time = time.time() - start_time
        
        print(f"Text length performance test:")
        print(f"  Short text ({len(short_text)} chars): {short_time:.4f} seconds")
        print(f"  Medium text ({len(medium_text)} chars): {medium_time:.4f} seconds")
        print(f"  Long text ({len(long_text)} chars): {long_time:.4f} seconds")
        
        # Performance should scale reasonably with text length
        assert short_time < medium_time
        assert medium_time < long_time
        assert long_time < 1.0  # Even long texts should process quickly 