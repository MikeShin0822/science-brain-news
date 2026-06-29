#!/usr/bin/env python3
"""Verify generated Astro routes after build.

This catches GitHub Pages 404 problems by ensuring every Markdown news file has a
matching static detail page under dist/news/<slug>/index.html.
"""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
NEWS_DIR = ROOT / "src" / "content" / "news"
DIST_NEWS_DIR = ROOT / "dist" / "news"
REQUIRED_TOP_LEVEL = [
    ROOT / "dist" / "index.html",
    ROOT / "dist" / "brain" / "index.html",
    ROOT / "dist" / "life" / "index.html",
    ROOT / "dist" / "papers" / "index.html",
    ROOT / "dist" / "about" / "index.html",
]


def main() -> int:
    missing = []
    for required in REQUIRED_TOP_LEVEL:
        if not required.exists():
            missing.append(required.relative_to(ROOT).as_posix())

    markdown_files = sorted(NEWS_DIR.glob("*.md"))
    for md in markdown_files:
        slug = md.stem
        expected = DIST_NEWS_DIR / slug / "index.html"
        if not expected.exists():
            missing.append(expected.relative_to(ROOT).as_posix())

    if missing:
        print("Route verification failed. Missing generated files:")
        for path in missing:
            print(f"- {path}")
        return 1

    print(f"Route verification passed: {len(markdown_files)} news detail pages verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
