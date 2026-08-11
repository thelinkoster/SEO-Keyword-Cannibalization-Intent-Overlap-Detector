"""
Unit tests for the Cannibalization Detector core engine and CLI utilities.
"""

import pytest
from seo_cannibalization_detector.core import CannibalizationDetector
from seo_cannibalization_detector.models import KeywordEntry
from seo_cannibalization_detector.utils import calculate_jaccard_similarity, normalize_text


def test_normalize_text():
    assert normalize_text(" Locksmith Local SEO Guide!! ") == "locksmith local seo guide"
    assert normalize_text("") == ""


def test_jaccard_similarity():
    sim = calculate_jaccard_similarity("technical seo audit", "technical seo audit checklist")
    assert sim > 0.6
    assert calculate_jaccard_similarity("locksmith", "plumber") == 0.0


def test_no_cannibalization_same_url():
    detector = CannibalizationDetector(similarity_threshold=0.7)
    entries = [
        KeywordEntry("https://linkoster.com/page1", "technical seo audit", position=5, impressions=1000),
        KeywordEntry("https://linkoster.com/page1", "technical seo audit guide", position=6, impressions=800),
    ]
    matches = detector.analyze(entries)
    assert len(matches) == 0


def test_detected_cannibalization_different_urls():
    detector = CannibalizationDetector(similarity_threshold=0.7)
    entries = [
        KeywordEntry("https://linkoster.com/blog/local-seo", "locksmith local seo strategy", position=12, impressions=1400, clicks=40),
        KeywordEntry("https://linkoster.com/services/seo", "locksmith local seo strategy", position=14, impressions=1200, clicks=30),
    ]
    matches = detector.analyze(entries)
    assert len(matches) == 1
    match = matches[0]
    assert match.similarity_score == 1.0
    assert match.recommended_action == "MERGE_AND_301_REDIRECT"
    assert match.primary_canonical_candidate == "https://linkoster.com/blog/local-seo"


def test_invalid_threshold():
    with pytest.raises(ValueError):
        CannibalizationDetector(similarity_threshold=1.5)
