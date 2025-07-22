"""
LexiMood - Persian Sentiment Analysis Library

A powerful library for analyzing sentiment and emotions in Persian text.
"""

__version__ = "0.1.0"
__author__ = "LexiMood Team"
__email__ = "info@leximood.com"

# Main API exports
from .analyzer import analyze_text
from .config import AnalysisConfig
from .models import AnalysisResult

__all__ = [
    "analyze_text",
    "AnalysisConfig", 
    "AnalysisResult",
] 