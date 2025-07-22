"""
Tests for the configuration module.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import pytest
from leximood.config import AnalysisConfig, AnalysisLevel, Language


class TestAnalysisConfig:
    """Test cases for AnalysisConfig class."""
    
    def test_default_config(self):
        """Test default configuration values."""
        config = AnalysisConfig()
        
        assert config.analysis_level == AnalysisLevel.SENTENCE
        assert config.language == Language.PERSIAN
        assert config.include_keywords is True
        assert config.max_keywords == 5
        assert config.confidence_threshold == 0.5
    
    def test_custom_config(self):
        """Test custom configuration values."""
        config = AnalysisConfig(
            analysis_level=AnalysisLevel.DOCUMENT,
            include_keywords=False,
            max_keywords=10,
            confidence_threshold=0.8
        )
        
        assert config.analysis_level == AnalysisLevel.DOCUMENT
        assert config.include_keywords is False
        assert config.max_keywords == 10
        assert config.confidence_threshold == 0.8
    
    def test_invalid_max_keywords(self):
        """Test validation of max_keywords parameter."""
        with pytest.raises(ValueError, match="max_keywords must be at least 1"):
            AnalysisConfig(max_keywords=0)
        
        with pytest.raises(ValueError, match="max_keywords must be at least 1"):
            AnalysisConfig(max_keywords=-1)
    
    def test_invalid_confidence_threshold(self):
        """Test validation of confidence_threshold parameter."""
        with pytest.raises(ValueError, match="confidence_threshold must be between 0.0 and 1.0"):
            AnalysisConfig(confidence_threshold=1.5)
        
        with pytest.raises(ValueError, match="confidence_threshold must be between 0.0 and 1.0"):
            AnalysisConfig(confidence_threshold=-0.1)


class TestEnums:
    """Test cases for enumeration classes."""
    
    def test_analysis_level_enum(self):
        """Test AnalysisLevel enumeration."""
        assert AnalysisLevel.SENTENCE.value == "sentence"
        assert AnalysisLevel.DOCUMENT.value == "document"
    
    def test_language_enum(self):
        """Test Language enumeration."""
        assert Language.PERSIAN.value == "persian" 