"""
Data models for SEO entries, similarity results, and conflict analysis.
"""

from dataclasses import dataclass, field
from typing import Dict, Any


@dataclass(frozen=True)
class KeywordEntry:
    """Represents a single URL-Keyword ranking observation from Search Console or Ahrefs."""
    url: str
    keyword: str
    position: float = 0.0
    impressions: int = 0
    clicks: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url": self.url,
            "keyword": self.keyword,
            "position": self.position,
            "impressions": self.impressions,
            "clicks": self.clicks,
        }


@dataclass
class CannibalizationMatch:
    """Represents a detected cannibalization conflict between two distinct URLs."""
    url_a: str
    url_b: str
    keyword_a: str
    keyword_b: str
    similarity_score: float
    severity_score: float
    recommended_action: str
    primary_canonical_candidate: str
    details: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "url_a": self.url_a,
            "url_b": self.url_b,
            "keyword_a": self.keyword_a,
            "keyword_b": self.keyword_b,
            "similarity_score": round(self.similarity_score, 4),
            "severity_score": round(self.severity_score, 4),
            "recommended_action": self.recommended_action,
            "primary_canonical_candidate": self.primary_canonical_candidate,
            "details": self.details,
        }
