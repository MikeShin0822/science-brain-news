#!/usr/bin/env python3
"""Daily Science Brain News collector.

Runs in GitHub Actions with the Python standard library only.
It creates one daily Markdown briefing containing 5 public-facing news items
and 5 papers/preprints, while avoiding URLs already stored in data/seen_urls.json
or existing Markdown posts.
"""

import argparse
import email.utils
import hashlib
import html
import json
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from zoneinfo import ZoneInfo
except Exception:
    ZoneInfo = None

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "data" / "daily_sources.json"
SEEN = ROOT / "data" / "seen_urls.json"
NEWS_DIR = ROOT / "src" / "content" / "news"
HEADERS = {
    "User-Agent": "ScienceBrainNewsBot/0.1 (+https://github.com/MikeShin0822/science-brain-news)",
    "Accept": "application/rss+xml, application/atom+xml, application/xml, application/json, text/xml, */*;q=0.5",
}
KEYWORDS = {
    "brain": 7, "neuro": 7, "neuroscience": 8, "neuron": 7, "synapse": 6,
    "memory": 5, "learning": 4, "sleep": 5, "cognition": 5, "cognitive": 5,
    "mental health": 4, "depression": 4, "anxiety": 3, "alzheimer": 7,
    "dementia": 6, "parkinson": 6, "stroke": 4, "dopamine": 5,
    "brain-computer": 7, "bci": 7, "neuroai": 7, "genome": 4, "gene": 3,
    "cell": 3, "stem cell": 5, "immune": 4, "aging": 5, "longevity": 5,
    "biotech": 4, "crispr": 5, "epigenetic": 4, "microbiome": 3,
}
RISK_TERMS = ["miracle", "cure", "one simple trick", "detox", "supplement"]


def kst_now():
    if ZoneInfo:
        return datetime.now(ZoneInfo("Asia/Seoul"))
    return datetime.now(timezone.utc) + timedelta(hours=9)


def fetch(url, timeout=25):
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        charset = res.headers.get_content_charset() or "utf-8"
        return res.read().decode(charset, errors="replace")


def clean(value, limit=None):
    value = html.unescape(value or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = unicodedata.normalize("NFKC", value)
    value = re.sub(r"\s+", " ", value).strip()
    if limit and len(value) > limit:
        value = value[: limit - 1].rstrip() + "…"
    return value


def canon(url):
    if not url:
        return ""
    p = urllib.parse.urlsplit(url.strip())
    q = [(k, v) for k, v in urllib.parse.parse_qsl(p.query, keep_blank_values=True)
         if not k.lower().startswith(("utm_", "fbclid", "gclid", "mc_"))]
    path = p.path.rstrip("/") or "/"
    return urllib.parse.urlunsplit((p.scheme.lower(), p.netloc.lower(), path, urllib.parse.urlencode(q), ""))


def h(value):
    return hashlib.sha1(value.encode("utf-8")).hexdigest()[:16]


def local(tag):
    return tag.split("}", 1)[-1].lower()


def text_child(elem, names):
    names = {n.lower() for n in names}
    for child in list(elem):
        if local(child.tag) in names:
            return "".join(child.itertext()).strip()
    return ""


def link_child(elem):
    for child in list(elem):
        if local(child.tag) == "link":
            href = child.attrib.get("href")
            if href:
                return href.strip()
            txt = "".join(child.itertext()).strip()
            if txt:
                return txt
    return text_child(elem, ["guid", "id"])


def parse_date(value):
    if not value:
        return kst_now().date().isoformat()
    value = value.strip()
    try:
        dt = email.utils.parsedate_to_datetime(value)
        if not dt.tzinfo:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).date().isoformat()
    except Exception:
        pass
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d", "%Y.%m.%d"):
        try:
            return datetime.strptime(value[:25], fmt).date().isoformat()
        except Exception:
            pass
    return kst_now().date().isoformat()


def score(title, summary, priority, date_value):
    hay = f"{title} {summary}".lower()
    score_value = int(priority)
    for term, weight in KEYWORDS.items():
        if term in hay:
            score_value += weight
    for term in RISK_TERMS:
        if term in hay:
            score_value -= 8
    try:
        age = (kst_now().date() - datetime.fromisoformat(date_value).date()).days
        score_value += 6 if age <= 1 else 4 if age <= 3 else 2 if age <= 7 else -5 if age > 21 else 0
    except Exception:
        pass
    return score_value


def item(kind, title, url, summary, source, date_value, category, score_value):
    return {
        "kind": kind,
        "title": title,
        "url": url,
        "summary": summary,
        "source": source,
        "date": date_value,
        "category": category,
        "score": score_value,
        "hash": h(canon(url) or title),
    }


def parse_rss(src, kind):
    try:
        root = ET.fromstring(fetch(src["url"]))
    except Exception as exc:
        print(f"WARN rss {src.get('name')}: {exc}", file=sys.stderr)
        return []
    out = []
    for elem in root.iter():
        if local(elem.tag) not in {"item", "entry"}:
            continue
        title = clean(text_child(elem, ["title"]), 220)
        url = link_child(elem)
        summary = clean(text_child(elem, ["description", "summary", "content", "encoded"]), 700)
        if not title or not url:
            continue
        date_value = parse_date(text_child(elem, ["pubDate", "updated", "published", "date"]))
        out.append(item(kind, title, url, summary or title, src["name"], date_value,
                        src.get("category", "뇌과학"), score(title, summary, src.get("priority", 0), date_value)))
    return out


def parse_biorxiv(src):
    server = src.get("server", "biorxiv")
    days = int(src.get("days", 14))
    url = f"https://api.biorxiv.org/details/{server}/{days}d/0"
    if src.get("api_category"):
        url += "?category=" + urllib.parse.quote(src["api_category"])
    try:
        data = json.loads(fetch(url))
    except Exception as exc:
        print(f"WARN biorxiv {src.get('name')}: {exc}", file=sys.stderr)
        return []
    out = []
    for row in data.get("collection", []):
        title = clean(row.get("title"), 240)
        doi = str(row.get("doi") or "").strip()
        summary = clean(row.get("abstract"), 900)
        if not title or not doi:
            continue
        link = row.get("url") or f"https://doi.org/{doi}"
        date_value = parse_date(row.get("date") or row.get("published") or row.get("server_date"))
        out.append(item("paper", title, link, summary or title, src["name"], date_value, "논문",
                        score(title, summary, src.get("priority", 0), date_value)))
    return out


def load_seen():
    seen = set()
    entries = []
    if SEEN.exists():
        try:
            raw = json.loads(SEEN.read_text(encoding="utf-8"))
        except Exception:
            raw = []
        for x in raw:
            if isinstance(x, str):
                digest = h(canon(x))
                entries.append({"url": x, "hash": digest})
                seen.add(digest)
            elif isinstance(x, dict):
                digest = x.get("hash") or h(canon(str(x.get("url", ""))))
                x["hash"] = digest
                entries.append(x)
                seen.add(digest)
    url_re = re.compile(r"https?://[^\s\]\)\"']+")
    for md in NEWS_DIR.glob("*.md"):
        try:
            for url in url_re.findall(md.read_text(encoding="utf-8")):
                seen.add(h(canon(url)))
        except Exception:
            pass
    return seen, entries


def select(candidates, limit, seen, per_source):
    picked, source_count, title_seen = [], {}, set()
    for x in sorted(candidates, key=lambda v: (v["score"], v["date"]), reverse=True):
        title_key = h(re.sub(r"\W+", "", x["title"].lower())[:160])
        if x["hash"] in seen or title_key in title_seen:
            continue
        if source_count.get(x["source"], 0) >= per_source:
            continue
        picked.append(x)
        seen.add(x["hash"])
        title_seen.add(title_key)
        source_count[x["source"]] = source_count.get(x["source"], 0) + 1
        if len(picked) >= limit:
            break
    return picked


def md_escape(value):
    return (value or "").replace("|", "\\|").strip()


def yaml_list(values):
    return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in values) + "]"


def render(popular, papers, today):
    date_str = today.date().isoformat()
    total = len(popular) + len(papers)
    lines = [
        "---",
        f"title: {json.dumps(f'{date_str} 데일리 브리핑: 뇌과학·생명과학 {total}선', ensure_ascii=False)}",
        f"description: {json.dumps(f'대중적 뉴스 {len(popular)}개와 논문 {len(papers)}개를 중복 없이 정리했습니다.', ensure_ascii=False)}",
        f"date: {json.dumps(date_str, ensure_ascii=False)}",
        'category: "브리핑"',
        'source: "Daily Collector"',
        'sourceUrl: "https://github.com/MikeShin0822/science-brain-news"',
        f"tags: {yaml_list(['daily', '뇌과학', '생명과학', '논문'])}",
        'importance: "매일 10:00 KST 자동 수집"',
        "---", "",
        f"이 글은 {date_str} 10:00 KST 기준 자동 수집 후보 중 중복 URL을 제외하고 선별한 데일리 브리핑입니다.", "",
        "## 대중적 뉴스 5개", "",
    ]
    if popular:
        for i, x in enumerate(popular, 1):
            lines += [f"### {i}. {md_escape(x['title'])}", "", f"- 출처: {md_escape(x['source'])}",
                      f"- 요약: {md_escape(x['summary'])}", f"- 링크: [원문 보기]({x['url']})", ""]
    else:
        lines += ["수집된 신규 대중 뉴스가 없습니다.", ""]
    lines += ["## 논문 5개", ""]
    if papers:
        for i, x in enumerate(papers, 1):
            lines += [f"### {i}. {md_escape(x['title'])}", "", f"요약: {md_escape(x['summary'])}", "",
                      f"[논문 링크]({x['url']})", ""]
    else:
        lines += ["수집된 신규 논문이 없습니다.", ""]
    return "\n".join(lines).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--date")
    args = parser.parse_args()
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    today = kst_now()
    if args.date:
        today = datetime.fromisoformat(args.date).replace(tzinfo=today.tzinfo)
    seen, entries = load_seen()
    popular_candidates, paper_candidates = [], []
    for src in cfg.get("popular_news", []):
        if src.get("type") == "rss":
            popular_candidates += parse_rss(src, "popular")
    for src in cfg.get("papers", []):
        if src.get("type") == "biorxiv":
            paper_candidates += parse_biorxiv(src)
        elif src.get("type") == "rss":
            paper_candidates += parse_rss(src, "paper")
    popular = select(popular_candidates, int(cfg.get("popular_news_limit", 5)), set(seen), int(cfg.get("popular_per_source_limit", 2)))
    paper_seen = set(seen) | {x["hash"] for x in popular}
    papers = select(paper_candidates, int(cfg.get("papers_limit", 5)), paper_seen, int(cfg.get("papers_per_source_limit", 3)))
    print(f"Candidates popular={len(popular_candidates)} papers={len(paper_candidates)}")
    print(f"Selected popular={len(popular)} papers={len(papers)}")
    if not popular and not papers:
        return 0
    content = render(popular, papers, today)
    if args.dry_run:
        print(content)
        return 0
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    out = NEWS_DIR / f"{today.date().isoformat()}-daily-briefing.md"
    out.write_text(content, encoding="utf-8")
    by_hash = {x.get("hash"): x for x in entries if x.get("hash")}
    for x in popular + papers:
        by_hash[x["hash"]] = {"hash": x["hash"], "url": canon(x["url"]), "title": x["title"],
                              "source": x["source"], "kind": x["kind"],
                              "added_at": today.isoformat(timespec="seconds")}
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(list(by_hash.values())[-1200:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {out.relative_to(ROOT)} and updated {SEEN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
