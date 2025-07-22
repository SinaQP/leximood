# LexiMood - Persian Sentiment Analysis Library

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-0.1.0-orange.svg)](https://github.com/leximood/leximood)

LexiMood is a powerful Persian sentiment analysis library designed to detect emotions and sentiment in Persian text. It provides accurate emotion detection, keyword extraction, and comprehensive text analysis capabilities.

## Features

- **Persian Text Processing**: Optimized for Persian language with proper normalization and tokenization
- **Sentiment Analysis**: Lexicon-based sentiment analysis with customizable scoring
- **Keyword Extraction**: TF-IDF based keyword extraction from text
- **Multiple Analysis Levels**: Support for sentence-level and document-level analysis
- **Easy Integration**: Simple API for quick integration into your projects
- **Comprehensive Testing**: Extensive test coverage for reliability

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install from Source

```bash
# Clone the repository
git clone https://github.com/leximood/leximood.git
cd leximood

# Install the package
pip install -e .
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from leximood import analyze_text

# Analyze a Persian text
text = "امروز روز بسیار خوبی بود و خیلی خوشحالم"
result = analyze_text(text)

print(f"Sentiment: {result.sentiment}")
print(f"Score: {result.score}")
print(f"Keywords: {result.keywords}")
```

## Usage Examples

### Basic Sentiment Analysis

```python
from leximood import analyze_text

# Positive text
positive_text = "این محصول عالی است و کیفیت فوق‌العاده‌ای دارد"
result = analyze_text(positive_text)
print(f"Sentiment: {result.sentiment}")  # Output: positive

# Negative text
negative_text = "خدمات بد بود و اصلاً راضی نیستم"
result = analyze_text(negative_text)
print(f"Sentiment: {result.sentiment}")  # Output: negative
```

### Custom Configuration

```python
from leximood import analyze_text, AnalysisConfig

config = AnalysisConfig(
    analysis_level="sentence",
    language="persian",
    include_keywords=True,
    max_keywords=5
)

result = analyze_text("متن مورد نظر برای تحلیل", config=config)
```

### Batch Processing

```python
from leximood import analyze_text

texts = [
    "امروز هوا خوب است",
    "دیروز باران آمد",
    "فردا احتمالاً آفتابی خواهد بود"
]

results = [analyze_text(text) for text in texts]

for i, result in enumerate(results):
    print(f"Text {i+1}: {result.sentiment} (score: {result.score:.2f})")
```

## API Reference

### Main Function

#### `analyze_text(text, config=None)`

Analyzes the sentiment of Persian text.

**Parameters:**
- `text` (str): The Persian text to analyze
- `config` (AnalysisConfig, optional): Configuration for analysis

**Returns:**
- `AnalysisResult`: Object containing sentiment analysis results

### Configuration

#### `AnalysisConfig`

Configuration class for sentiment analysis.

**Parameters:**
- `analysis_level` (str): Level of analysis ("sentence" or "document")
- `language` (str): Language of the text ("persian")
- `include_keywords` (bool): Whether to extract keywords
- `max_keywords` (int): Maximum number of keywords to extract

### Results

#### `AnalysisResult`

Result object containing analysis information.

**Attributes:**
- `sentiment` (str): Sentiment label ("positive", "negative", "neutral")
- `score` (float): Sentiment score between -1 and 1
- `keywords` (list): Extracted keywords
- `confidence` (float): Confidence score of the analysis

## Project Structure

```
leximood/
├── src/
│   └── leximood/
│       ├── __init__.py
│       ├── analyzer.py
│       ├── preprocessor.py
│       ├── sentiment.py
│       ├── keywords.py
│       └── data/
│           ├── lexicon.json
│           └── stopwords.txt
├── tests/
│   ├── test_analyzer.py
│   ├── test_preprocessor.py
│   └── test_sentiment.py
├── docs/
│   └── tasks/
├── data/
├── requirements.txt
├── setup.py
└── README.md
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/leximood/leximood.git
cd leximood

# Install in development mode
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=leximood

# Run specific test file
pytest tests/test_analyzer.py
```

### Code Quality

```bash
# Format code
black src/ tests/

# Lint code
flake8 src/ tests/

# Type checking
mypy src/
```

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Persian NLP community for resources and inspiration
- Contributors and maintainers of Persian text processing libraries
- Research community for sentiment analysis methodologies

## Support

If you encounter any issues or have questions:

- Check the [documentation](https://leximood.readthedocs.io/)
- Search [existing issues](https://github.com/leximood/leximood/issues)
- Create a [new issue](https://github.com/leximood/leximood/issues/new)

## Roadmap

- [ ] Machine learning-based sentiment analysis
- [ ] Emotion detection (joy, sadness, anger, fear, etc.)
- [ ] Multi-language support
- [ ] Real-time analysis API
- [ ] Web interface
- [ ] Mobile SDK

---

**LexiMood** - Making Persian text analysis simple and accurate. 