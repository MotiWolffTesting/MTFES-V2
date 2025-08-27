import json
import logging
import re
from typing import Any, Dict
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

logger = logging.getLogger(__name__)

# regexes for cleaning text
_punct_re = re.compile(r"[\.,!?;:\-_/\\()\[\]{}'\"`~@#$%^&*+=|<>]")
_specials_re = re.compile(r"[^a-zA-Z0-9\s]")
_whitespace_re = re.compile(r"\s+")

def ensure_nltk() -> None:
    "Ensure that the NLTK data is downloaded."
    try:
        nltk.data.find("corpora/stopwords")
    except LookupError:
        nltk.download("stopwords")
    try:
        nltk.data.find("corpora/wordnet")
    except LookupError:
        nltk.download("wordnet")
        
class TextPreprocessor:
    def __init__(self, language: str = "english"):
        "Initialize the TextPreprocessor"
        ensure_nltk()
        self.stop_words = set(stopwords.words(language))
        self.lemmatizer = WordNetLemmatizer()
        
    def clean(self, text: str) -> str:
        "Clean the text using the regexes"
        if not text:
            return ""
        lowered = text.lower()
        no_punct = _punct_re.sub(" ", lowered)
        no_specials = _specials_re.sub(" ", no_punct)
        collapsed = _whitespace_re.sub(" ", no_specials.strip())
        tokens = [t for t in collapsed.split(" ") if t and t not in self.stop_words]
        lemmatized = [self.lemmatizer.lemmatize(t) for t in tokens]
        return " ".join(lemmatized)
    
def transform_message(msg: Dict[str, Any], pre: TextPreprocessor) -> Dict[str, Any]:
    "Transform a message"
    original = msg.get("original_text") or msg.get("text") or msg.get("Text") or ""
    cleaned = pre.clean(original)
    out = dict(msg)
    out["original_text"] = original
    out["clean_text"] = cleaned
    return out