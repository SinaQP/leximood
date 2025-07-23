"""
Sentiment analysis module for Persian text.
"""

import json
import os
import re
from typing import Dict, Any, List
from .constants import (
    SENTIMENT_POSITIVE_THRESHOLD, SENTIMENT_NEGATIVE_THRESHOLD,
    SENTIMENT_SCORE_MIN, SENTIMENT_SCORE_MAX
)


class  SentimentAnalyzer:
    def __init__(self):
        self.lexicon = self._load_sentiment_lexicon()
    
    def analyze(self, text: str) -> float:
        if not self._is_valid_text(text):
            return 0.0
        
        words = self._tokenize_text(text)
        raw_score = self._calculate_sentiment_score(words)
        normalized_score = self._normalize_score(raw_score)
        return normalized_score
    
    def _is_valid_text(self, text: str) -> bool:
        return text and text.strip()
    
    def _calculate_sentiment_score(self, words: List[str]) -> float:
        if not words:
            return 0.0
        
        total_score = 0.0
        word_count = 0
        
        for word in words:
            word = word.strip().lower()
            if not word:
                continue
            
            word_score = self._get_word_sentiment_score(word)
            if word_score != 0:
                total_score += word_score
                word_count += 1
        
        return total_score / word_count if word_count > 0 else 0.0
    
    def _get_word_sentiment_score(self, word: str) -> float:
        if word in self.lexicon["positive_words"]:
            return self.lexicon["positive_words"][word]
        if word in self.lexicon["negative_words"]:
            return self.lexicon["negative_words"][word]
        return 0.0
    
    def _load_sentiment_lexicon(self) -> Dict[str, Any]:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            lexicon_path = os.path.join(current_dir, "data", "persian_sentiment_lexicon.json")
            
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"Warning: Could not load sentiment lexicon: {e}")
            return {
                "positive_words": {},
                "negative_words": {}
            }
    
    def _tokenize_text(self, text: str) -> List[str]:
        return re.findall(r'\b\w+\b', text)
    
    def _normalize_score(self, score: float) -> float:
        return max(SENTIMENT_SCORE_MIN, min(SENTIMENT_SCORE_MAX, score))
    
    def get_sentiment_label(self, score: float) -> str:
        if score > SENTIMENT_POSITIVE_THRESHOLD:
            return "positive"
        if score < SENTIMENT_NEGATIVE_THRESHOLD:
            return "negative"
        return "neutral" 