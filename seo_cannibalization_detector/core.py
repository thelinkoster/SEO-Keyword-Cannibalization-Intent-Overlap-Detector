"""
Core analysis engine for keyword cannibalization and intent conflict detection.
"""

from typing import List, Dict, Tuple
from .models import KeywordEntry, CannibalizationMatch
from .utils import calculate_jaccard_similarity, calculate_ngram_similarity, normalize_text


class CannibalizationDetector:
    """Main analyzer class to process keyword data and identify search cannibalization."""

    def __init__(self, similarity_threshold: float = 0.75):
        """
        Initialize the detector.

        :param similarity_threshold: Float between 0.0 and 1.0 triggering match flag.
        """
        if not 0.0 <= similarity_threshold <= 1.0:
            raise ValueError("Similarity threshold must be between 0.0 and 1.0")
        self.similarity_threshold = similarity_threshold

    def analyze(self, entries: List[KeywordEntry]) -> List[CannibalizationMatch]:
        """
        Process list of keyword observations and detect conflict matches across URLs.

        :param entries: List of KeywordEntry dataclass instances.
        :return: List of CannibalizationMatch results sorted by severity score descending.
        """
        if not entries:
            return []

        matches: List[CannibalizationMatch] = []
        n = len(entries)

        for i in range(n):
            for j in range(i + 1, n):
                entry1 = entries[i]
                entry2 = entries[j]

                # Cannibalization only happens between DISTINCT URLs
                if entry1.url == entry2.url:
                    continue

                # Calculate text and keyword similarity
                norm1 = normalize_text(entry1.keyword)
                norm2 = normalize_text(entry2.keyword)

                # Exact match or semantic overlap check
                if norm1 == norm2:
                    sim_score = 1.0
                else:
                    jaccard = calculate_jaccard_similarity(norm1, norm2)
                    ngram = calculate_ngram_similarity(norm1, norm2, n=2)
                    sim_score = max(jaccard, ngram)

                if sim_score >= self.similarity_threshold:
                    match = self._evaluate_conflict(entry1, entry2, sim_score)
                    matches.append(match)

        # Sort matches by severity score descending
        matches.sort(key=lambda x: x.severity_score, reverse=True)
        return matches

    def _evaluate_conflict(
        self, entry1: KeywordEntry, entry2: KeywordEntry, sim_score: float
    ) -> CannibalizationMatch:
        """Compute severity score and decide primary canonical candidate and action."""
        
        # Decide stronger canonical candidate based on clicks, impressions, then position
        if entry1.clicks > entry2.clicks:
            primary = entry1
            secondary = entry2
        elif entry2.clicks > entry1.clicks:
            primary = entry2
            secondary = entry1
        elif entry1.impressions > entry2.impressions:
            primary = entry1
            secondary = entry2
        elif entry2.impressions > entry1.impressions:
            primary = entry2
            secondary = entry1
        else:
            # Lower average rank number is better (e.g., position 3 beats position 12)
            primary = entry1 if entry1.position <= entry2.position else entry2
            secondary = entry2 if primary == entry1 else entry1

        # Calculate Severity Score (0 to 100%)
        # Base severity from keyword similarity
        base_severity = sim_score * 50.0

        # Additional severity if both pages are ranking close on Page 2 or Top 20 (position 4 to 25)
        pos_conflict_boost = 0.0
        if 1.0 <= entry1.position <= 30.0 and 1.0 <= entry2.position <= 30.0:
            pos_diff = abs(entry1.position - entry2.position)
            if pos_diff <= 10.0:
                pos_conflict_boost = 30.0 - (pos_diff * 2.0)

        # Impressions conflict boost
        imp_boost = 0.0
        if entry1.impressions > 0 and entry2.impressions > 0:
            imp_boost = 20.0

        severity_score = min(100.0, base_severity + pos_conflict_boost + imp_boost)

        # Determine actionable SEO directive
        if sim_score >= 0.95 and severity_score >= 70.0:
            action = "MERGE_AND_301_REDIRECT"
        elif sim_score >= 0.85:
            action = "CANONICALIZE_OR_REMAP_CONTENT"
        else:
            action = "DIFFERENTIATE_SEARCH_INTENT"

        details = {
            "similarity_type": "EXACT" if sim_score == 1.0 else "SEMANTIC_OVERLAP",
            "primary_impressions": primary.impressions,
            "secondary_impressions": secondary.impressions,
            "primary_position": primary.position,
            "secondary_position": secondary.position,
        }

        return CannibalizationMatch(
            url_a=entry1.url,
            url_b=entry2.url,
            keyword_a=entry1.keyword,
            keyword_b=entry2.keyword,
            similarity_score=sim_score,
            severity_score=severity_score,
            recommended_action=action,
            primary_canonical_candidate=primary.url,
            details=details,
        )
