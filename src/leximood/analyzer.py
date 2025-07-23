"""
Main analyzer module for LexiMood sentiment analysis.
"""

from typing import Optional
from .config import AnalysisConfig, AnalysisLevel
from .models import AnalysisResult, SentimentLabel
from .preprocessor import TextPreprocessor
from .sentiment import SentimentAnalyzer
from .keywords import KeywordExtractor
from .constants import (
    SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEGATIVE_THRESHOLD,
    CONFIDENCE_SCORE_MULTIPLIER, KEYWORD_CONFIDENCE_FACTOR, KEYWORD_COUNT_DIVISOR,
    CONFIDENCE_MAX
)


class Analyzer:
    def __init__(self, config: Optional[AnalysisConfig] = None):
        self.config = config or AnalysisConfig()
        self.preprocessor = TextPreprocessor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.keyword_extractor = KeywordExtractor()
    
    def analyze(self, text: str) -> AnalysisResult:
        if not self._is_valid_input_text(text):
            raise ValueError("Text cannot be empty")
        
        processed_text = self.preprocessor.preprocess(text)
        sentiment_score = self.sentiment_analyzer.analyze(processed_text)
        sentiment_label = self._determine_sentiment_label(sentiment_score)
        keywords = self._extract_keywords_if_enabled(processed_text)
        confidence = self._calculate_confidence_score(sentiment_score, len(keywords))
        return self._create_analysis_result(
            sentiment_label, sentiment_score, keywords, confidence, text
        )
    
    def _is_valid_input_text(self, text: str) -> bool:
        return text is not None and text.strip() != ""
    
    def _determine_sentiment_label(self, score: float) -> SentimentLabel:
        if score > SENTIMENT_POSITIVE_THRESHOLD:
            return SentimentLabel.POSITIVE
        if score < SENTIMENT_NEGATIVE_THRESHOLD:
            return SentimentLabel.NEGATIVE
        return SentimentLabel.NEUTRAL
    
    def _extract_keywords_if_enabled(self, processed_text: str) -> list:
        if not self.config.include_keywords:
            return []
        
        return self.keyword_extractor.extract(
            processed_text, 
            max_keywords=self.config.max_keywords
        )
    
    def _calculate_confidence_score(self, sentiment_score: float, keyword_count: int) -> float:
        base_confidence = self._calculate_base_confidence(sentiment_score)
        keyword_confidence = self._calculate_keyword_confidence(keyword_count)
        total_confidence = base_confidence + keyword_confidence
        
        return min(total_confidence, CONFIDENCE_MAX)
    
    def _calculate_base_confidence(self, sentiment_score: float) -> float:
        return min(abs(sentiment_score) * CONFIDENCE_SCORE_MULTIPLIER, CONFIDENCE_MAX)
    
    def _calculate_keyword_confidence(self, keyword_count: int) -> float:
        keyword_factor = min(keyword_count / KEYWORD_COUNT_DIVISOR, CONFIDENCE_MAX)
        return keyword_factor * KEYWORD_CONFIDENCE_FACTOR
    
    def _create_analysis_result(
        self, 
        sentiment_label: SentimentLabel, 
        sentiment_score: float, 
        keywords: list, 
        confidence: float, 
        original_text: str
    ) -> AnalysisResult:
        return AnalysisResult(
            sentiment=sentiment_label,
            score=sentiment_score,
            keywords=keywords,
            confidence=confidence,
            text=original_text,
            analysis_level=self.config.analysis_level.value
        )


_global_analyzer_instance = None


def analyze_text(text: str, config: Optional[AnalysisConfig] = None) -> AnalysisResult:
    global _global_analyzer_instance
    
    if _should_create_new_analyzer(config):
        _global_analyzer_instance = Analyzer(config)
    
    return _global_analyzer_instance.analyze(text)


def _should_create_new_analyzer(config: Optional[AnalysisConfig]) -> bool:
    return _global_analyzer_instance is None or config is not None 