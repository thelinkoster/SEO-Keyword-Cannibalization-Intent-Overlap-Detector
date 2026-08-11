"""
SEO Keyword Cannibalization & Intent Overlap Detector
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A lightweight, production-grade Python package to detect keyword cannibalization
and calculate search intent conflict across website URLs.

Author: Rajesh Kumar Nitharwal
License: MIT
"""

__version__ = "0.1.0"
__author__ = "Rajesh Kumar Nitharwal"

from .core import CannibalizationDetector
from .models import CannibalizationMatch, KeywordEntry

__all__ = ["CannibalizationDetector", "KeywordEntry", "CannibalizationMatch"]
