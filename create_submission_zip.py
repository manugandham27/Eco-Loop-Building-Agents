"""
EcoLoop AI - Submission Package Generator
Zips all source code, IDF building models, test suites, and documentation into a single submission zip file.
"""

import os
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
ZIP_FILENAME = PROJECT_ROOT / "EcoLoop_AI_Honeywell_Hackathon.zip"

EXCLUDE_DIRS = {".venv", ".venv312", "__pycache__", ".git", ".pytest_cache"}
EXCLUDE_EXTS = {".pyc", ".zip", ".tar.gz"}


def build_submission_zip():
    print(f"Creating submission package: {ZIP_FILENAME.name}...")
    count = 0
    with zipfile.ZipFile(ZIP_FILENAME, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            # Exclude unwanted directories
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                file_path = Path(root) / file
                if file_path.suffix in EXCLUDE_EXTS or file_path == ZIP_FILENAME:
                    continue

                arcname = file_path.relative_to(PROJECT_ROOT)
                zipf.write(file_path, arcname)
                count += 1

    print(f"Successfully packaged {count} files into {ZIP_FILENAME.name} ({ZIP_FILENAME.stat().st_size / 1024:.1f} KB).")


if __name__ == "__main__":
    build_submission_zip()
