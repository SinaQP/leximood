"""
Constants for LexiMood sentiment analysis.
"""

# Sentiment Analysis Constants
SENTIMENT_POSITIVE_THRESHOLD = 0.1
SENTIMENT_NEGATIVE_THRESHOLD = -0.1
SENTIMENT_SCORE_MIN = -1.0
SENTIMENT_SCORE_MAX = 1.0
CONFIDENCE_MIN = 0.0
CONFIDENCE_MAX = 1.0

# Confidence Calculation Constants
CONFIDENCE_SCORE_MULTIPLIER = 2.0
KEYWORD_CONFIDENCE_FACTOR = 0.2
KEYWORD_COUNT_DIVISOR = 3

# Configuration Defaults
DEFAULT_MAX_KEYWORDS = 5
DEFAULT_CONFIDENCE_THRESHOLD = 0.5
MIN_KEYWORDS_REQUIRED = 1

# Text Processing Constants
SINGLE_SPACE = ' '
EMPTY_STRING = ''
MIN_WORD_LENGTH_FOR_PROCESSING = 2
MAX_WORD_LENGTH_FOR_NORMALIZATION = 10
FREQUENCY_BOOST_FACTOR = 10
MIN_WORD_LENGTH_FOR_KEYWORD_EXTRACTION = 2

# Unicode Control Character Ranges
CONTROL_CHARACTERS_START = 0x00
CONTROL_CHARACTERS_END = 0x08
CONTROL_CHARACTERS_MIDDLE_START = 0x0B
CONTROL_CHARACTERS_MIDDLE_END = 0x0C
CONTROL_CHARACTERS_LATE_START = 0x0E
CONTROL_CHARACTERS_LATE_END = 0x1F
DELETE_CHARACTER = 0x7F

# Zero-Width Character Ranges
ZERO_WIDTH_START = 0x200B
ZERO_WIDTH_END = 0x200D
ZERO_WIDTH_NO_BREAK_SPACE = 0xFEFF

# Text Direction Marks
LEFT_TO_RIGHT_MARK = 0x200E
RIGHT_TO_LEFT_MARK = 0x200F

# Persian Punctuation Marks
PERSIAN_COMMA = '،'
PERSIAN_SEMICOLON = '؛'
PERSIAN_QUESTION_MARK = '؟'
EXCLAMATION_MARK = '!'
PERIOD = '.'
COLON = ':'

# Sentence Termination Marks for Tokenization
SENTENCE_TERMINATORS = {PERSIAN_QUESTION_MARK, EXCLAMATION_MARK, PERIOD}

# Persian Stop Words
PERSIAN_STOP_WORDS = {
    'این', 'آن', 'که', 'را', 'به', 'از', 'در', 'با', 'برای', 'تا', 'بر', 'بی', 'پس', 'پیش',
    'تو', 'ما', 'شما', 'آنها', 'اینها', 'خود', 'خویش', 'خویشتن', 'هم', 'نیز', 'همچنین',
    'اما', 'ولی', 'اگر', 'چون', 'چرا', 'چگونه', 'کجا', 'کی', 'چه', 'چند', 'کدام',
    'هست', 'هستند', 'بود', 'بودند', 'شده', 'شده‌اند', 'می‌شود', 'می‌شوند',
    'می‌کرد', 'می‌کردند', 'کرده', 'کرده‌اند', 'خواهد', 'خواهند', 'دارد', 'دارند',
    'داشته', 'داشته‌اند', 'بوده', 'بوده‌اند', 'شده‌بود', 'شده‌بودند',
    'و', 'یا', 'نه', 'هم', 'همه', 'هیچ', 'چیزی', 'کسی', 'جایی', 'وقتی', 'چطور',
    'چقدر', 'کدام', 'کدام‌یک', 'هر', 'همه', 'تمام', 'همگی', 'همه‌ی', 'همه‌ی‌این',
    'همه‌ی‌آن', 'همه‌ی‌آنها', 'همه‌ی‌اینها', 'همه‌ی‌ما', 'همه‌ی‌شما',
    'من', 'تو', 'او', 'ما', 'شما', 'آنها', 'ایشان', 'خودم', 'خودت', 'خودش',
    'خودمان', 'خودتان', 'خودشان', 'خویش', 'خویشتن', 'خود', 'خودم', 'خودت',
    'خودش', 'خودمان', 'خودتان', 'خودشان', 'خویش', 'خویشتن',
    'است', 'هست', 'بود', 'شده', 'دارد', 'روی', 'بالا', 'پایین', 'چپ', 'راست',
    'جلو', 'عقب', 'داخل', 'خارج', 'کنار', 'کنار', 'پشت', 'جلوی', 'عقب‌تر',
    'بالاتر', 'پایین‌تر', 'چپ‌تر', 'راست‌تر', 'جلوتر', 'عقب‌تر'
}

# Persian Stemming Constants
PERSIAN_SUFFIXES = [
    'ها', 'ان', 'ات', 'ین', 'ون', 'ها', 'ی', 'یی', 'ی‌ها', 'ی‌ان', 'ی‌ات',
    'ی‌ین', 'ی‌ون', 'ی‌ی', 'ی‌یی', 'ی‌ی‌ها', 'ی‌ی‌ان', 'ی‌ی‌ات',
    'ی‌ی‌ین', 'ی‌ی‌ون', 'ی‌ی‌ی', 'ی‌ی‌یی'
]

PERSIAN_PREFIXES = [
    'بی', 'با', 'بر', 'پس', 'پیش', 'در', 'را', 'رو', 'زیر', 'سو', 'سوی',
    'فرا', 'فرو', 'کم', 'که', 'گه', 'می', 'نا', 'نو', 'وا', 'هم', 'هیچ'
]

PERSIAN_VERB_SUFFIXES = [
    'م', 'ی', 'د', 'یم', 'ید', 'ند', 'ه', 'ه‌ای', 'ه‌ا', 'ه‌ان',
    'ه‌ی', 'ه‌یی', 'ه‌ی‌ها', 'ه‌ی‌ان', 'ه‌ی‌ات', 'ه‌ی‌ین', 'ه‌ی‌ون'
]

PERSIAN_VERB_PREFIXES = [
    'می', 'نمی', 'بی', 'بر', 'در', 'فرا', 'فرو', 'وا', 'هم'
]

# Minimum word length for stemming
MIN_WORD_LENGTH_FOR_STEMMING = 3 