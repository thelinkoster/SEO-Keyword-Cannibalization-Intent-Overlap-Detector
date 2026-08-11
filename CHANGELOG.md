# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-08-11

### Added
- Initial release of `seo-keyword-cannibalization-detector`.
- Core similarity engine supporting N-Gram Jaccard index and Cosine token overlap.
- Automated Cannibalization Severity Scoring algorithm (0–100%).
- Actionable SEO directive generation (`MERGE_AND_301`, `REMAP_INTENT`, `CANONICALIZE`).
- Command-line interface (CLI) with CSV and JSON export options.
- Complete unit test suite using `pytest`.
- Sample CSV data file for immediate testing.
