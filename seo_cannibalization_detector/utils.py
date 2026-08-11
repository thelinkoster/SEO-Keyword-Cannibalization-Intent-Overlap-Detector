"""
Utility functions for text normalization, tokenization, and metric calculations.
"""

import re
from typing import Set, List


ENGLISH_STOPWORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
    "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
    "below", "between", "both", "but", "by", "can", "cannot", "could", "did", "do",
    "does", "doing", "down", "during", "each", "few", "for", "from", "further",
    "had", "has", "have", "having", "he", "her", "here", "hers", "herself", "him",
    "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself",
    "just", "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of",
    "off", "on", "once", "only", "or", "other", "our", "ours", "ourselves", "out",
    "over", "own", "same", "she", "should", "so", "some", "such", "than", "that",
    "the", "their", "theirs", "them", "themselves", "then", "there", "these",
    "they", "this", "those", "through", "to", "too", "under", "until", "up", "very",
    "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "with", "you", "your", "yours", "yourself", "yourselves"
}


def normalize_text(text: str) -> str:
    """Clean and standardize input keyword text."""
    if not text:
        return ""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def tokenize(text: str, remove_stopwords: bool = True) -> List[str]:
    """Tokenize normalized text into clean word list."""
    cleaned = normalize_text(text)
    tokens = cleaned.split(" ")
    if remove_stopwords:
        tokens = [t for t in tokens if t and t not in ENGLISH_STOPWORDS]
    return [t for t in tokens if t]


def calculate_jaccard_similarity(str1: str, str2: str) -> float:
    """Calculate Jaccard similarity index between two string token sets."""
    set1: Set[str] = set(tokenize(str1, remove_stopwords=True))
    set2: Set[str] = set(tokenize(str2, remove_stopwords=True))

    if not set1 or not set2:
        return 0.0

    intersection = set1.intersection(set2)
    union = set1.union(set2)
    return len(intersection) / len(union)


def extract_ngrams(text: str, n: int = 2) -> Set[str]:
    """Extract character or word N-Grams from text for fine-grained matching."""
    tokens = tokenize(text, remove_stopwords=False)
    if len(tokens) < n:
        return {" ".join(tokens)} if tokens else set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def calculate_ngram_similarity(str1: str, str2: str, n: int = 2) -> float:
    """Calculate character/word N-gram overlap ratio."""
    ngrams1 = extract_ngrams(str1, n)
    ngrams2 = extract_ngrams(str2, n)

    if not ngrams1 or not ngrams2:
        return 0.0

    intersection = ngrams1.intersection(ngrams2)
    union = ngrams1.union(ngrams2)
    return len(intersection) / len(union)
