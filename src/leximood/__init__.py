"""
LexiMood - Persian Sentiment Analysis Library
"""

__version__ = "0.1.0"
__author__ = "LexiMood Team"
__email__ = "info@leximood.com"

from .analyzer import analyze_text
from .config import AnalysisConfig
from .models import AnalysisResult

__all__ = [
    "analyze_text",
    "AnalysisConfig", 
    "AnalysisResult",
] 