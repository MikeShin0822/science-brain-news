# Science Brain News

Astro 기반 GitHub Pages용 뇌과학·생명과학 뉴스 큐레이션 사이트입니다.

## Stack

- Astro
- Markdown posts
- GitHub Pages
- RSS feed
- Daily GitHub Actions collector

## Daily automation

`.github/workflows/daily-news.yml`이 매일 10:00 KST에 실행됩니다.

자동화 흐름:

1. `data/daily_sources.json`의 대중 뉴스 RSS와 논문/API 소스를 읽습니다.
2. 대중적 뉴스 5개와 논문 5개를 점수화해서 고릅니다.
3. `data/seen_urls.json`과 기존 Markdown 글의 링크를 기준으로 중복을 제거합니다.
4. `src/content/news/` 아래에 총 10개의 개별 Markdown 글을 생성합니다.
5. 신규 글과 seen URL 기록을 커밋합니다.
6. push를 받은 `.github/workflows/deploy.yml`이 Astro 사이트를 GitHub Pages에 배포합니다.

논문 글은 제목, 요약, 논문 링크 중심으로 구성합니다.

수동 실행:

```bash
python scripts/collect_news.py --dry-run
python scripts/collect_news.py
```

## Run locally

```bash
npm install
npm run dev
```

## Add news manually

`src/content/news/` 폴더에 Markdown 파일을 추가합니다.

```md
---
title: "기사 제목"
description: "한 줄 요약"
date: "2026-06-29"
category: "뇌과학"
source: "Source Name"
sourceUrl: "https://example.com"
tags: ["수면", "기억"]
---

## 핵심 요약

내용을 작성합니다.
```

## Deploy

`main` 브랜치에 push되면 `.github/workflows/deploy.yml`이 Astro 사이트를 빌드해 GitHub Pages에 배포합니다.

저장소 Settings → Pages에서 Source를 GitHub Actions로 설정하세요.
