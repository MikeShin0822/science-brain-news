"""Future automation entry point.

This repository is currently set up as an Astro/GitHub Pages news site.
A later pass can replace this placeholder with a real collector that:
1. reads data/sources.yml,
2. fetches RSS or source pages,
3. scores brain/life science relevance,
4. writes Markdown files into src/content/news/,
5. updates data/seen_urls.json.
"""

from pathlib import Path

NEWS_DIR = Path("src/content/news")


def main() -> None:
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    print("Collector placeholder ready. Add real RSS/source collection in the next pass.")


if __name__ == "__main__":
    main()
