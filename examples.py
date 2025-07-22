"""
Examples demonstrating how to use LexiMood for Persian sentiment analysis.
"""

import sys
sys.path.insert(0, 'src')
from leximood import analyze_text, AnalysisConfig


def basic_usage_example():
    """Basic usage example."""
    print("=== Basic Usage Example ===")
    
    # Simple text analysis
    text = "امروز روز بسیار خوبی بود و خیلی خوشحالم"
    result = analyze_text(text)
    
    print(f"Text: {text}")
    print(f"Sentiment: {result.sentiment.value}")
    print(f"Score: {result.score:.3f}")
    print(f"Confidence: {result.confidence:.3f}")
    print(f"Keywords: {result.keywords}")
    print()


def custom_config_example():
    """Example with custom configuration."""
    print("=== Custom Configuration Example ===")
    
    # Create custom configuration
    config = AnalysisConfig(
        include_keywords=True,
        max_keywords=3,
        confidence_threshold=0.6
    )
    
    text = "این محصول کیفیت خوبی دارد اما قیمت بالایی دارد"
    result = analyze_text(text, config)
    
    print(f"Text: {text}")
    print(f"Sentiment: {result.sentiment.value}")
    print(f"Score: {result.score:.3f}")
    print(f"Keywords: {result.keywords}")
    print()


def batch_analysis_example():
    """Example of batch text analysis."""
    print("=== Batch Analysis Example ===")
    
    texts = [
        "امروز هوا عالی است",
        "دیروز باران آمد و خیس شدم",
        "فردا احتمالاً آفتابی خواهد بود",
        "این غذا خیلی خوشمزه است",
        "خدمات بد بود و اصلاً راضی نیستم"
    ]
    
    print("Batch Analysis Results:")
    print("-" * 50)
    
    for i, text in enumerate(texts, 1):
        result = analyze_text(text)
        print(f"{i}. {text}")
        print(f"   Sentiment: {result.sentiment.value} (Score: {result.score:.3f})")
        print()


def main():
    """Run all examples."""
    print("LexiMood Persian Sentiment Analysis Examples")
    print("=" * 50)
    print()
    
    basic_usage_example()
    custom_config_example()
    batch_analysis_example()
    
    print("Note: These examples use placeholder implementations.")
    print("Full functionality will be available after completing all tasks.")


if __name__ == "__main__":
    main() 