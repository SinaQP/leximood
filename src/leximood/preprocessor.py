"""
Text preprocessing module for Persian text normalization and tokenization.
"""

import re
import json
import os
from typing import List, Dict, Set
from .constants import (
    SINGLE_SPACE, EMPTY_STRING,
    CONTROL_CHARACTERS_START, CONTROL_CHARACTERS_END,
    CONTROL_CHARACTERS_MIDDLE_START, CONTROL_CHARACTERS_MIDDLE_END,
    CONTROL_CHARACTERS_LATE_START, CONTROL_CHARACTERS_LATE_END,
    DELETE_CHARACTER, ZERO_WIDTH_START, ZERO_WIDTH_END,
    ZERO_WIDTH_NO_BREAK_SPACE, LEFT_TO_RIGHT_MARK, RIGHT_TO_LEFT_MARK,
    PERSIAN_COMMA, PERSIAN_SEMICOLON, PERSIAN_QUESTION_MARK,
    EXCLAMATION_MARK, PERIOD, COLON, SENTENCE_TERMINATORS, PERSIAN_STOP_WORDS,
    PERSIAN_SUFFIXES, PERSIAN_PREFIXES, PERSIAN_VERB_SUFFIXES, PERSIAN_VERB_PREFIXES,
    MIN_WORD_LENGTH_FOR_STEMMING, MIN_WORD_LENGTH_FOR_PROCESSING
)


class TextPreprocessor:
    def __init__(self):
        self._arabic_to_persian_mapping = self._create_arabic_to_persian_mapping()
        self._characters_to_remove = self._create_characters_to_remove_set()
        self._punctuation_marks = self._create_punctuation_marks_set()
        self._stop_words = PERSIAN_STOP_WORDS
        self._sentence_terminators = SENTENCE_TERMINATORS
        self._persian_roots = self._load_persian_roots()
        self._suffixes = PERSIAN_SUFFIXES
        self._prefixes = PERSIAN_PREFIXES
        self._verb_suffixes = PERSIAN_VERB_SUFFIXES
        self._verb_prefixes = PERSIAN_VERB_PREFIXES
    
    def preprocess(self, text: str) -> str:
        if not self._is_valid_text(text):
            return text
        return self.normalize_text(text)
    
    def normalize_text(self, text: str) -> str:
        if not self._is_valid_text(text):
            return text
        
        text_copy = str(text)
        text_copy = self._convert_arabic_to_persian(text_copy)
        text_copy = self._remove_unwanted_characters(text_copy)
        text_copy = self._remove_control_characters(text_copy)
        text_copy = self._remove_text_direction_marks(text_copy)
        text_copy = self._normalize_whitespace(text_copy)
        text_copy = self._normalize_punctuation_spacing(text_copy)
        text_copy = self._final_cleanup(text_copy)
        
        return text_copy
    
    def tokenize_text(self, text: str) -> List[str]:
        if not self._is_valid_text(text):
            return []
        
        normalized_text = self.normalize_text(text)
        sentences = self._split_into_sentences(normalized_text)
        return self._clean_sentences(sentences)
    
    def word_tokenize(self, sentence: str) -> List[str]:
        if not self._is_valid_text(sentence):
            return []
        
        words = self._split_into_words(sentence)
        return self._remove_stop_words(words)
    
    def stem_words(self, words: List[str]) -> List[str]:
        if not words:
            return []
        
        return [self._stem_word(word) for word in words]
    
    def _is_valid_text(self, text: str) -> bool:
        return text is not None and text.strip() != EMPTY_STRING
    
    def _load_persian_roots(self) -> Dict[str, List[str]]:
        try:
            data_dir = os.path.join(os.path.dirname(__file__), 'data')
            roots_file = os.path.join(data_dir, 'persian_roots.json')
            
            if os.path.exists(roots_file):
                with open(roots_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception:
            return {}
    
    def _create_arabic_to_persian_mapping(self) -> Dict[str, str]:
        return {
            'ي': 'ی',
            'ك': 'ک',
            'ة': 'ه',
            'أ': 'ا',
            'إ': 'ا',
            'آ': 'آ',
            'ؤ': 'و',
            'ئ': 'ی',
            'ء': EMPTY_STRING,
            'ٱ': 'ا',
            'ٲ': 'ا',
            'ٳ': 'ا',
            'ٵ': 'ا',
            'ٶ': 'و',
            'ٷ': 'ی',
            'ٸ': 'ی',
        }
    
    def _create_characters_to_remove_set(self) -> Set[str]:
        arabic_diacritics = {'ـ', 'ً', 'ٌ', 'ٍ', 'َ', 'ُ', 'ِ', 'ّ', 'ْ', 'ٰ', 'ٖ', 'ٗ', '٘', 'ٙ', 'ٚ', 'ٛ', 'ٜ', 'ٝ', 'ٞ', 'ٟ'}
        arabic_numerals = {'٠', '١', '٢', '٣', '٤', '٥', '٦', '٧', '٨', '٩'}
        persian_numerals = {'۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'}
        
        return arabic_diacritics | arabic_numerals | persian_numerals
    
    def _create_punctuation_marks_set(self) -> Set[str]:
        return {
            PERSIAN_COMMA, PERSIAN_SEMICOLON, PERSIAN_QUESTION_MARK,
            EXCLAMATION_MARK, PERIOD, COLON, '(', ')', '[', ']', '{', '}', '"', "'", '«', '»'
        }
    
    def _convert_arabic_to_persian(self, text: str) -> str:
        for arabic_char, persian_char in self._arabic_to_persian_mapping.items():
            text = text.replace(arabic_char, persian_char)
        return text
    
    def _remove_unwanted_characters(self, text: str) -> str:
        for char in self._characters_to_remove:
            text = text.replace(char, EMPTY_STRING)
        return text
    
    def _remove_control_characters(self, text: str) -> str:
        control_char_pattern = self._create_control_character_pattern()
        text = re.sub(control_char_pattern, EMPTY_STRING, text)
        
        zero_width_pattern = self._create_zero_width_pattern()
        text = re.sub(zero_width_pattern, EMPTY_STRING, text)
        
        return text
    
    def _create_control_character_pattern(self) -> str:
        return f'[{chr(CONTROL_CHARACTERS_START)}-{chr(CONTROL_CHARACTERS_END)}{chr(CONTROL_CHARACTERS_MIDDLE_START)}{chr(CONTROL_CHARACTERS_MIDDLE_END)}{chr(CONTROL_CHARACTERS_LATE_START)}-{chr(CONTROL_CHARACTERS_LATE_END)}{chr(DELETE_CHARACTER)}]'
    
    def _create_zero_width_pattern(self) -> str:
        return f'[{chr(ZERO_WIDTH_START)}-{chr(ZERO_WIDTH_END)}{chr(ZERO_WIDTH_NO_BREAK_SPACE)}]'
    
    def _remove_text_direction_marks(self, text: str) -> str:
        direction_marks_pattern = f'[{chr(LEFT_TO_RIGHT_MARK)}{chr(RIGHT_TO_LEFT_MARK)}]'
        return re.sub(direction_marks_pattern, EMPTY_STRING, text)
    
    def _normalize_whitespace(self, text: str) -> str:
        return re.sub(r'\s+', SINGLE_SPACE, text)
    
    def _normalize_punctuation_spacing(self, text: str) -> str:
        punctuation_marks = [PERSIAN_COMMA, PERSIAN_SEMICOLON, PERSIAN_QUESTION_MARK, EXCLAMATION_MARK, PERIOD, COLON]
        
        for punctuation_mark in punctuation_marks:
            text = self._remove_space_before_punctuation(text, punctuation_mark)
            text = self._normalize_space_after_punctuation(text, punctuation_mark)
        
        return text
    
    def _remove_space_before_punctuation(self, text: str, punctuation_mark: str) -> str:
        pattern = r'\s+' + re.escape(punctuation_mark)
        return re.sub(pattern, punctuation_mark, text)
    
    def _normalize_space_after_punctuation(self, text: str, punctuation_mark: str) -> str:
        pattern = re.escape(punctuation_mark) + r'\s+'
        return re.sub(pattern, punctuation_mark + SINGLE_SPACE, text)
    
    def _final_cleanup(self, text: str) -> str:
        text = text.strip()
        return re.sub(r'\s+', SINGLE_SPACE, text)
    
    def _split_into_sentences(self, text: str) -> List[str]:
        sentence_pattern = self._create_sentence_split_pattern()
        sentences = re.split(sentence_pattern, text)
        return self._reconstruct_sentences(sentences)
    
    def _reconstruct_sentences(self, sentences: List[str]) -> List[str]:
        cleaned_sentences = []
        
        for i in range(0, len(sentences) - 1, 2):
            if i + 1 < len(sentences):
                sentence = sentences[i].strip()
                terminator = sentences[i + 1].strip()
                if sentence:
                    cleaned_sentences.append(sentence + terminator)
            else:
                sentence = sentences[i].strip()
                if sentence:
                    cleaned_sentences.append(sentence)
        
        if len(sentences) % 2 == 1 and sentences[-1].strip():
            cleaned_sentences.append(sentences[-1].strip())
        
        return cleaned_sentences
    
    def _create_sentence_split_pattern(self) -> str:
        terminators = [re.escape(term) for term in self._sentence_terminators]
        return r'(' + '|'.join(terminators) + r')'
    
    def _clean_sentences(self, sentences: List[str]) -> List[str]:
        return [sentence for sentence in sentences if len(sentence) > MIN_WORD_LENGTH_FOR_PROCESSING]
    
    def _split_into_words(self, sentence: str) -> List[str]:
        words = re.split(r'\s+', sentence.strip())
        return [self._clean_word(word) for word in words if word]
    
    def _clean_word(self, word: str) -> str:
        return word.strip('،؛؟!.:()[]{}""''«»')
    
    def _remove_stop_words(self, words: List[str]) -> List[str]:
        return [word for word in words if word not in self._stop_words]
    
    def _stem_word(self, word: str) -> str:
        if len(word) < MIN_WORD_LENGTH_FOR_STEMMING:
            return word
        
        stemmed_word = self._lookup_in_dictionary(word)
        if stemmed_word:
            return stemmed_word
        
        return self._apply_rule_based_stemming(word)
    
    def _lookup_in_dictionary(self, word: str) -> str:
        for root, inflections in self._persian_roots.items():
            if word in inflections:
                return root
        return EMPTY_STRING
    
    def _apply_rule_based_stemming(self, word: str) -> str:
        original_word = word
        
        word = self._remove_verb_prefixes(word)
        word = self._remove_verb_suffixes(word)
        word = self._remove_suffixes(word)
        word = self._remove_prefixes(word)
        
        if self._is_valid_stem(word):
            return word
        
        return original_word
    
    def _remove_suffixes(self, word: str) -> str:
        return self._remove_affixes(word, self._suffixes, self._remove_suffix_from_word)
    
    def _remove_prefixes(self, word: str) -> str:
        return self._remove_affixes(word, self._prefixes, self._remove_prefix_from_word)
    
    def _remove_verb_suffixes(self, word: str) -> str:
        return self._remove_affixes(word, self._verb_suffixes, self._remove_suffix_from_word)
    
    def _remove_verb_prefixes(self, word: str) -> str:
        return self._remove_affixes(word, self._verb_prefixes, self._remove_prefix_from_word)
    
    def _remove_affixes(self, word: str, affixes: List[str], removal_function) -> str:
        for affix in sorted(affixes, key=len, reverse=True):
            stemmed = removal_function(word, affix)
            if stemmed != word and self._is_valid_stem(stemmed):
                return stemmed
        return word
    
    def _remove_suffix_from_word(self, word: str, suffix: str) -> str:
        if word.endswith(suffix) and len(word) > len(suffix) + MIN_WORD_LENGTH_FOR_STEMMING:
            return word[:-len(suffix)]
        if word.endswith('\u200c' + suffix) and len(word) > len(suffix) + 1 + MIN_WORD_LENGTH_FOR_STEMMING:
            return word[:-len(suffix)-1]
        return word
    
    def _remove_prefix_from_word(self, word: str, prefix: str) -> str:
        if word.startswith(prefix) and len(word) > len(prefix) + MIN_WORD_LENGTH_FOR_STEMMING:
            return word[len(prefix):]
        if word.startswith(prefix + '\u200c') and len(word) > len(prefix) + 1 + MIN_WORD_LENGTH_FOR_STEMMING:
            return word[len(prefix)+1:]
        return word
    
    def _is_valid_stem(self, stem: str) -> bool:
        if len(stem) < MIN_WORD_LENGTH_FOR_STEMMING:
            return False
        
        if '\u200c' in stem or '\u200d' in stem:
            return False
        
        return True 