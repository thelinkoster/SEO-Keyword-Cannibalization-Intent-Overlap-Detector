"""
Command-Line Interface (CLI) for running cannibalization audits from CSV files.
"""

import argparse
import csv
import json
import sys
from pathlib import Path
from typing import List

from .core import CannibalizationDetector
from .models import KeywordEntry


def parse_csv_input(filepath: Path) -> List[KeywordEntry]:
    """Parse CSV input file into structured KeywordEntry list."""
    if not filepath.exists():
        raise FileNotFoundError(f"Input file not found: {filepath}")

    entries: List[KeywordEntry] = []
    with open(filepath, mode="r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fieldnames = [fn.lower().strip() for fn in (reader.fieldnames or [])]

        if "url" not in fieldnames or "keyword" not in fieldnames:
            raise ValueError("CSV input must contain at least 'url' and 'keyword' columns.")

        for row_idx, row in enumerate(reader, start=2):
            normalized_row = {k.lower().strip(): v.strip() for k, v in row.items() if k}
            url = normalized_row.get("url", "")
            keyword = normalized_row.get("keyword", "")

            if not url or not keyword:
                continue

            try:
                position = float(normalized_row.get("position", 0.0) or 0.0)
                impressions = int(float(normalized_row.get("impressions", 0) or 0))
                clicks = int(float(normalized_row.get("clicks", 0) or 0))
            except ValueError:
                position, impressions, clicks = 0.0, 0, 0

            entries.append(
                KeywordEntry(
                    url=url,
                    keyword=keyword,
                    position=position,
                    impressions=impressions,
                    clicks=clicks,
                )
            )

    return entries


def write_csv_output(matches: List, filepath: Path) -> None:
    """Export audit results into structured CSV file."""
    fieldnames = [
        "url_a",
        "url_b",
        "keyword_a",
        "keyword_b",
        "similarity_score",
        "severity_score",
        "recommended_action",
        "primary_canonical_candidate",
    ]
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for m in matches:
            d = m.to_dict()
            d.pop("details", None)
            writer.writerow(d)


def main() -> None:
    """CLI Entrypoint function."""
    parser = argparse.ArgumentParser(
        description="SEO Keyword Cannibalization & Search Intent Conflict Detector"
    )
    parser.add_argument("input_csv", type=Path, help="Path to input CSV file (must contain 'url' and 'keyword' columns)")
    parser.add_argument("--threshold", "-t", type=float, default=0.75, help="Similarity threshold between 0.0 and 1.0 (default: 0.75)")
    parser.add_argument("--csv", type=Path, help="Export output results to CSV file path")
    parser.add_argument("--json", type=Path, help="Export output results to JSON file path")
    parser.add_argument("--version", "-v", action="version", version="%(prog)s 0.1.0")

    args = parser.parse_args()

    try:
        entries = parse_csv_input(args.input_csv)
        print(f"[*] Loaded {len(entries)} keyword-URL records from {args.input_csv}")

        detector = CannibalizationDetector(similarity_threshold=args.threshold)
        matches = detector.analyze(entries)

        print(f"[+] Detected {len(matches)} potential cannibalization conflict(s) (Threshold: {args.threshold})\n")

        if matches:
            print("-" * 80)
            for idx, match in enumerate(matches[:5], start=1):
                print(f"Conflict #{idx} [Severity: {match.severity_score:.1f}%]")
                print(f"  URL A   : {match.url_a} ('{match.keyword_a}')")
                print(f"  URL B   : {match.url_b} ('{match.keyword_b}')")
                print(f"  Action  : {match.recommended_action}")
                print(f"  Canonical Target: {match.primary_canonical_candidate}")
                print("-" * 80)

            if len(matches) > 5:
                print(f"... and {len(matches) - 5} more conflicts.")

        if args.csv:
            write_csv_output(matches, args.csv)
            print(f"[✓] CSV report saved to {args.csv}")

        if args.json:
            json_data = [m.to_dict() for m in matches]
            with open(args.json, "w", encoding="utf-8") as f:
                json.dump(json_data, f, indent=2)
            print(f"[✓] JSON report saved to {args.json}")

    except Exception as e:
        print(f"[!] Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
