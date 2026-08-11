"""
Utility script to package the entire repository into a clean ZIP archive for easy distribution or upload.
"""

import zipfile
from pathlib import Path

FILES_TO_INCLUDE = [
    "pyproject.toml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    ".gitignore",
    "example_data.csv",
    "seo_cannibalization_detector/__init__.py",
    "seo_cannibalization_detector/__main__.py",
    "seo_cannibalization_detector/cli.py",
    "seo_cannibalization_detector/core.py",
    "seo_cannibalization_detector/models.py",
    "seo_cannibalization_detector/utils.py",
    "tests/test_core.py",
]


def build_zip():
    zip_filename = "seo-keyword-cannibalization-detector.zip"
    print(f"[*] Packaging project into {zip_filename}...")

    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_str in FILES_TO_INCLUDE:
            p = Path(file_str)
            if p.exists():
                arcname = f"seo-keyword-cannibalization-detector/{file_str}"
                zipf.write(p, arcname=arcname)
                print(f"  + Added: {file_str}")
            else:
                print(f"  ! Warning: File not found: {file_str}")

    print(f"[✓] Successfully generated {zip_filename}")


if __name__ == "__main__":
    build_zip()
