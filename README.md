# Science Brain News

Astro 기반 GitHub Pages용 뇌과학·생명과학 뉴스 큐레이션 사이트입니다.

## Stack

- Astro
- Markdown posts
- GitHub Pages
- RSS feed
- ChatGPT Scheduled daily collector

## Daily automation

ChatGPT Scheduled의 `Science Brain News` 작업이 매일 09:30 KST에 실행됩니다.

자동화 흐름:

1. 대중 뉴스 RSS와 논문/API 소스를 확인합니다.
2. 대중적 뉴스 5개와 논문/프리프린트 5개를 고릅니다.
3. 기존 저장소 글과 seen URL을 기준으로 중복을 제거합니다.
4. `src/content/news/` 아래에 총 10개의 개별 Markdown 글을 생성합니다.
5. 뉴스 글은 확장 요약, 왜 중요한가, 읽을 때 주의할 점, 원문 링크 중심으로 구성합니다.
6. 논문 글은 긴 요약, 읽을 때 볼 점, 논문 링크 중심으로 구성합니다.
7. 변경사항을 GitHub에 커밋합니다.
8. 커밋 push 이후 `.github/workflows/deploy.yml`이 Astro 사이트를 빌드하고 route verification을 통과한 뒤 GitHub Pages에 배포합니다.

중복 실행 방지를 위해 GitHub Actions의 daily news collection workflow는 제거했습니다. GitHub Actions는 사이트 배포용 workflow만 유지합니다.

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
