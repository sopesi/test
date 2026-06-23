"""
Check Markdown files for Latin abbreviations.
Inspired by The Turing Way style guide:
https://book.the-turing-way.org/community-handbook/style/style-writing-markdown/

Fails CI if any .md file contains: e.g., etc., i.e. (or variants).
"""
import sys
from pathlib import Path

BAD_LATIN = [
    ("e.g.", "for example, such as, like, including"),
    ("i.e.", "that is, meaning"),
    ("etc.", "for example, such as"),
    ("etc", "for example, such as"),   # " etc " with surrounding context
    (" ie ", "that is, meaning"),
    ("et cetera", "and so on"),
]

IGNORE_FILES = {"references.bib"}


def check_file(filepath: Path) -> list[str]:
    """Check a single file and return list of errors."""
    errors = []
    try:
        text = filepath.read_text(encoding="utf-8", errors="ignore").lower()
    except Exception:
        return errors

    for bad, suggestion in BAD_LATIN:
        if bad in text:
            # Find the offending line
            for i, line in enumerate(text.split("\n"), start=1):
                if bad in line:
                    errors.append(
                        f"  Line {i}: found '{bad.strip()}' — use '{suggestion}' instead"
                    )
    return errors


def main():
    repo_root = Path.cwd()
    md_files = list(repo_root.rglob("*.md"))

    if not md_files:
        print("No Markdown files found. Nothing to check.")
        return 0

    failed = False
    for filepath in sorted(md_files):
        if filepath.name in IGNORE_FILES:
            continue
        errors = check_file(filepath)
        if errors:
            failed = True
            print(f"\n{filepath.relative_to(repo_root)}:")
            for err in errors:
                print(err)

    if failed:
        print(
            "\n---\n"
            "Latin abbreviations found!\n"
            "See: https://book.the-turing-way.org/community-handbook/style/style-writing-markdown/\n"
        )
        return 1

    print("No Latin abbreviations found.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
