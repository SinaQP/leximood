"""
Keyword extraction module for Persian text.
"""

import re
import json
import os
from typing import List, Dict, Set
from collections import Counter
from .constants import (
    PERSIAN_STOP_WORDS, MIN_WORD_LENGTH_FOR_KEYWORD_EXTRACTION,
    MAX_WORD_LENGTH_FOR_NORMALIZATION, FREQUENCY_BOOST_FACTOR
)


class KeywordExtractor:
    def __init__(self):
        self.sentiment_words = self._load_sentiment_words()
        self.stop_words = PERSIAN_STOP_WORDS
    
    def extract(self, text: str, max_keywords: int = 5) -> List[str]:
        if not self._is_valid_text(text):
            return []
        
        words = self._tokenize_text(text)
        if not words:
            return []
        
        tf_idf_scores = self._calculate_tf_idf_scores(words)
        filtered_scores = self._filter_keywords_by_sentiment(tf_idf_scores)
        keywords = self._get_top_keywords(filtered_scores, max_keywords)
        
        return keywords
    
    def _is_valid_text(self, text: str) -> bool:
        return text and text.strip()
    
    def _calculate_tf_idf_scores(self, words: List[str]) -> Dict[str, float]:
        if not words:
            return {}
        
        word_counts = Counter(words)
        total_words = len(words)
        
        tf_scores = self._calculate_term_frequency_scores(word_counts, total_words)
        tf_idf_scores = self._calculate_tf_idf_approximation(tf_scores)
        
        return tf_idf_scores
    
    def _calculate_term_frequency_scores(self, word_counts: Counter, total_words: int) -> Dict[str, float]:
        tf_scores = {}
        for word, count in word_counts.items():
            if self._should_skip_word(word):
                continue
            tf_scores[word] = count / total_words
        return tf_scores
    
    def _should_skip_word(self, word: str) -> bool:
        return word in self.stop_words or len(word) < MIN_WORD_LENGTH_FOR_KEYWORD_EXTRACTION
    
    def _calculate_tf_idf_approximation(self, tf_scores: Dict[str, float]) -> Dict[str, float]:
        tf_idf_scores = {}
        for word, tf_score in tf_scores.items():
            word_length_factor = min(len(word) / MAX_WORD_LENGTH_FOR_NORMALIZATION, 1.0)
            frequency_factor = 1.0 / (1.0 + tf_score * FREQUENCY_BOOST_FACTOR)
            tf_idf_scores[word] = tf_score * word_length_factor * frequency_factor
        return tf_idf_scores
    
    def _filter_keywords_by_sentiment(self, tf_idf_scores: Dict[str, float]) -> Dict[str, float]:
        sentiment_boost_factor = 2.0
        filtered_scores = {}
        
        for word, score in tf_idf_scores.items():
            if word in self.sentiment_words:
                filtered_scores[word] = score * sentiment_boost_factor
            else:
                filtered_scores[word] = score
        
        return filtered_scores
    
    def _load_sentiment_words(self) -> Set[str]:
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            lexicon_path = os.path.join(current_dir, "data", "persian_sentiment_lexicon.json")
            
            with open(lexicon_path, 'r', encoding='utf-8') as f:
                lexicon_data = json.load(f)
            
            sentiment_words = set()
            sentiment_words.update(lexicon_data.get("positive_words", {}).keys())
            sentiment_words.update(lexicon_data.get("negative_words", {}).keys())
            
            return sentiment_words
        except (FileNotFoundError, json.JSONDecodeError, KeyError):
            return set()
    
    def _tokenize_text(self, text: str) -> List[str]:
        words = re.findall(r'\b\w+\b', text.lower())
        return [word for word in words if self._is_valid_word(word)]
    
    def _is_valid_word(self, word: str) -> bool:
        return len(word) >= MIN_WORD_LENGTH_FOR_KEYWORD_EXTRACTION and not word.isdigit()
    
    def _get_top_keywords(self, scores: Dict[str, float], max_keywords: int) -> List[str]:
        if not scores:
            return []
        
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [word for word, score in sorted_words[:max_keywords]] 