"""
Configuration classes for LexiMood sentiment analysis.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum


class AnalysisLevel(Enum):
    """Analysis level enumeration."""
    SENTENCE = "sentence"
    DOCUMENT = "document"


class Language(Enum):
    """Language enumeration."""
    PERSIAN = "persian"


@dataclass
class AnalysisConfig:
    """
    Configuration for sentiment analysis.
    
    Attributes:
        analysis_level: Level of analysis (sentence or document)
        language: Language of the text
        include_keywords: Whether to extract keywords
        max_keywords: Maximum number of keywords to extract
        confidence_threshold: Threshold for confidence scoring
    """
    
    analysis_level: AnalysisLevel = AnalysisLevel.SENTENCE
    language: Language = Language.PERSIAN
    include_keywords: bool = True
    max_keywords: int = 5
    confidence_threshold: float = 0.5
    
    def __post_init__(self):
        """Validate configuration parameters."""
        if self.max_keywords < 1:
            raise ValueError("max_keywords must be at least 1")
        
        if not 0.0 <= self.confidence_threshold <= 1.0:
            raise ValueError("confidence_threshold must be between 0.0 and 1.0") 