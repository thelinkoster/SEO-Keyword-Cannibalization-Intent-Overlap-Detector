# SEO-Keyword-Cannibalization-Intent-Overlap-Detector
Lightweight, zero-dependency Python CLI tool to detect SEO keyword cannibalization, calculate intent overlap, and generate actionable canonicalization recommendations.
# SEO Keyword Cannibalization & Search Intent Detector

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen.svg)](tests/)

A lightweight, production-grade Python CLI tool designed for Technical SEO specialists, agency strategists, and webmasters to detect keyword cannibalization, calculate search intent conflict across URLs, and output actionable canonicalization recommendations.

---

## Why This Project Exists

When multiple URLs on the same website compete for identical or semantically similar search queries, Google gets confused about which page to rank. This causes **keyword cannibalization**, leading to:
* Search rankings stuck on Page 2 or Page 3 (Positions 11–25).
* Fluctuation and ranking flip-flops between competing URLs.
* Split backlink equity and lower organic click-through rates (CTR).

This tool automates the process of analyzing Google Search Console (GSC) or Ahrefs exports to isolate intent overlaps and recommend concrete SEO fixes (`MERGE_AND_301_REDIRECT`, `CANONICALIZE_OR_REMAP_CONTENT`, or `DIFFERENTIATE_SEARCH_INTENT`).

---

## Key Features

- **Zero Heavy External Dependencies:** Built using Python 3.10+ standard libraries (`dataclasses`, `difflib`, `csv`, `json`, `argparse`).
- **N-Gram & Jaccard Similarity Engine:** Captures both exact keyword matches and high-intent semantic overlaps.
- **Cannibalization Severity Scoring (0–100%):** Combines textual similarity with Search Console metrics (position proximity and impressions conflict).
- **Automated Primary Canonical Target Selection:** Recommends the strongest destination URL based on performance signals (clicks, impressions, position).
- **Flexible Export Options:** Supports interactive console reporting alongside structured `CSV` and `JSON` output formats.

---

## Technology Stack

* **Language:** Python 3.10+
* **Core Modules:** `dataclasses`, `difflib`, `math`, `csv`, `json`, `re`, `argparse`
* **Testing Framework:** `pytest`
* **Packaging:** `pyproject.toml` (Flit build system)

---

## Project Structure

```text
seo-keyword-cannibalization-detector/
│
├── seo_cannibalization_detector/
│   ├── __init__.py          # Package initialization
│   ├── __main__.py          # Python -m execution entry point
│   ├── cli.py               # Command-line interface logic
│   ├── core.py              # Main cannibalization analysis engine
│   ├── models.py            # Dataclasses for entries and matches
│   └── utils.py             # Normalization and N-Gram similarity logic
│
├── tests/
│   └── test_core.py         # Pytest unit tests
│
├── .gitignore
├── CHANGELOG.md
├── LICENSE
├── README.md
├── example_data.csv         # Sample dataset for testing
└── pyproject.toml           # Python packaging configuration
