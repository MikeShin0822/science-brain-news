#!/usr/bin/env python3
"""Daily Science Brain News collector.

Runs in GitHub Actions with the Python standard library only.
It creates 10 individual Markdown posts every day:
- 5 public-facing news posts
- 5 paper summary posts
It avoids URLs already stored in data/seen_urls.json or existing Markdown posts.
Generated posts use longer summaries so cards lead to useful detail pages.
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
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%d"):
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


def make_item(kind, title, url, summary, source, date_value, category, score_value):
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
        summary = clean(text_child(elem, ["description", "summary", "content", "encoded"]), 1800)
        if not title or not url:
            continue
        date_value = parse_date(text_child(elem, ["pubDate", "updated", "published", "date"]))
        category = src.get("category", "뇌과학") if kind == "popular" else "논문"
        out.append(make_item(kind, title, url, summary or title, src["name"], date_value,
                             category, score(title, summary, src.get("priority", 0), date_value)))
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
        summary = clean(row.get("abstract"), 2400)
        if not title or not doi:
            continue
        link = row.get("url") or f"https://doi.org/{doi}"
        date_value = parse_date(row.get("date") or row.get("published") or row.get("server_date"))
        out.append(make_item("paper", title, link, summary or title, src["name"], date_value, "논문",
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


def slugify(title):
    value = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii")
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:70].strip("-") or h(title)


def yaml_list(values):
    return "[" + ", ".join(json.dumps(v, ensure_ascii=False) for v in values) + "]"


def md_escape(value):
    return (value or "").replace("|", "\\|").strip()


def compact_summary(value, fallback):
    value = md_escape(value) or fallback
    return value


def news_context(title, source, category):
    return (
        f"이 항목은 {source}에서 수집한 {category} 관련 뉴스입니다. "
        "자동 수집 단계에서는 원문 전체를 복사하지 않고, 공개 RSS 설명과 제목을 바탕으로 핵심 맥락을 정리합니다. "
        "따라서 세부 수치, 연구 설계, 표본 규모, 제한점은 반드시 원문을 함께 확인하는 방식으로 읽는 것이 좋습니다."
    )


def paper_context(source):
    return (
        f"이 논문 항목은 {source}에서 수집한 연구 요약입니다. "
        "자동 수집 결과는 논문의 초록이나 공개 메타데이터를 바탕으로 정리되며, 결론을 확정적으로 받아들이기보다는 연구 질문, 방법, 대상, 한계를 함께 확인하는 출발점으로 보는 것이 좋습니다. "
        "특히 프리프린트나 조기 공개 논문은 후속 검증과 동료평가 과정에서 해석이 달라질 수 있습니다."
    )


def render_post(x, today, index):
    date_str = today.date().isoformat()
    is_paper = x["kind"] == "paper"
    source_url = canon(x["url"])
    title = x["title"]
    summary = compact_summary(x.get("summary"), title)
    desc = summary[:220] + ("…" if len(summary) > 220 else "")
    tags = ["논문", "summary", "long-summary"] if is_paper else ["뉴스", "뇌과학", "생명과학", "long-summary"]
    category = "논문" if is_paper else x.get("category", "뇌과학")
    lines = [
        "---",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"description: {json.dumps(desc, ensure_ascii=False)}",
        f"date: {json.dumps(date_str, ensure_ascii=False)}",
        f"category: {json.dumps(category, ensure_ascii=False)}",
        f"source: {json.dumps(x['source'], ensure_ascii=False)}",
        f"sourceUrl: {json.dumps(source_url, ensure_ascii=False)}",
        f"tags: {yaml_list(tags)}",
        f"importance: {json.dumps('매일 09:30 KST 자동 수집 · 확장 요약', ensure_ascii=False)}",
        "---", "",
    ]
    if is_paper:
        lines += [
            "## 요약", "",
            summary, "",
            "## 읽을 때 볼 점", "",
            paper_context(x["source"]), "",
            "- 연구가 다루는 핵심 질문이 무엇인지 확인합니다.",
            "- 동물실험, 세포실험, 인간 대상 연구인지 구분합니다.",
            "- 결과가 실제 치료, 제품, 생활 조언으로 이어지기까지 어느 정도 거리가 있는지 확인합니다.",
            "", f"[논문 링크]({source_url})", "",
        ]
    else:
        lines += [
            "## 핵심 요약", "",
            summary, "",
            "## 왜 중요한가", "",
            news_context(title, x["source"], category), "",
            "## 읽을 때 주의할 점", "",
            "- 기사 제목만 보고 건강 조언으로 바로 바꾸지 않습니다.",
            "- 원문에서 연구 대상, 방법, 한계, 이해상충 여부를 확인합니다.",
            "- 같은 주제를 다른 연구와 비교해 반복적으로 확인된 결과인지 살펴봅니다.",
            "", "## 원문", "", f"[원문 보기]({source_url})", "",
        ]
    prefix = "paper" if is_paper else "news"
    filename = f"{date_str}-{prefix}-{index:02d}-{slugify(title)}.md"
    return filename, "\n".join(lines).rstrip() + "\n"


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
    selected = popular + papers
    rendered = [render_post(x, today, i + 1) for i, x in enumerate(selected)]
    if args.dry_run:
        for name, content in rendered:
            print(f"--- {name} ---")
            print(content[:1800])
        return 0
    NEWS_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in rendered:
        (NEWS_DIR / name).write_text(content, encoding="utf-8")
    by_hash = {x.get("hash"): x for x in entries if x.get("hash")}
    for x in selected:
        by_hash[x["hash"]] = {"hash": x["hash"], "url": canon(x["url"]), "title": x["title"],
                              "source": x["source"], "kind": x["kind"],
                              "added_at": today.isoformat(timespec="seconds")}
    SEEN.parent.mkdir(parents=True, exist_ok=True)
    SEEN.write_text(json.dumps(list(by_hash.values())[-1200:], ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(rendered)} individual posts and updated {SEEN.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
