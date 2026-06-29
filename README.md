# Science Brain News

Astro 기반 GitHub Pages용 뇌과학·생명과학 뉴스 큐레이션 사이트입니다.

## Stack

- Astro
- Markdown posts
- GitHub Pages
- RSS feed

## Run locally

```bash
npm install
npm run dev
```

## Add news

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

`main` 브랜치에 push되면 GitHub Actions가 Astro 사이트를 빌드해 GitHub Pages에 배포합니다.

저장소 Settings → Pages에서 Source를 GitHub Actions로 설정하세요.
