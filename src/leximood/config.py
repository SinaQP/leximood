"""
Configuration classes for LexiMood sentiment analysis.
"""

from dataclasses import dataclass
from typing import Optional
from enum import Enum
from .constants import (
    DEFAULT_MAX_KEYWORDS, DEFAULT_CONFIDENCE_THRESHOLD,
    MIN_KEYWORDS_REQUIRED, CONFIDENCE_MIN, CONFIDENCE_MAX
)


class AnalysisLevel(Enum):
    SENTENCE = "sentence"
    DOCUMENT = "document"


class Language(Enum):
    PERSIAN = "persian"


@dataclass
class AnalysisConfig:
    analysis_level: AnalysisLevel = AnalysisLevel.SENTENCE
    language: Language = Language.PERSIAN
    include_keywords: bool = True
    max_keywords: int = DEFAULT_MAX_KEYWORDS
    confidence_threshold: float = DEFAULT_CONFIDENCE_THRESHOLD
    
    def __post_init__(self):
        self._validate_max_keywords()
        self._validate_confidence_threshold()
    
    def _validate_max_keywords(self):
        if self.max_keywords >= MIN_KEYWORDS_REQUIRED:
            return
        
        raise ValueError(f"max_keywords must be at least {MIN_KEYWORDS_REQUIRED}")
    
    def _validate_confidence_threshold(self):
        if CONFIDENCE_MIN <= self.confidence_threshold <= CONFIDENCE_MAX:
            return
        
        raise ValueError(f"confidence_threshold must be between {CONFIDENCE_MIN} and {CONFIDENCE_MAX}") 