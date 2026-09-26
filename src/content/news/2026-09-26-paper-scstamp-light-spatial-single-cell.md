---
title: "빛으로 세포의 위치를 먼저 찍고 single-cell multiome을 읽었다… scSTAMP-seq의 공간 바코딩"
description: "Nature Biotechnology 연구가 photocleavable oligonucleotide와 패턴광을 이용해 조직을 분리하기 전에 각 세포의 공간정보를 기록하고, 표준 single-cell transcriptome·multiome 분석과 결합하는 scSTAMP-seq를 제시했다."
date: "2026-09-26T09:30:00+09:00"
category: "생명과학"
source: "Nature Biotechnology"
sourceUrl: "https://www.nature.com/articles/s41587-026-03328-5"
tags: ["single-cell", "공간전사체", "multiome", "광바코딩", "인간embryoid"]
importance: "scstamp-light-spatial-single-cell"
---

## 긴 요약

단일세포 RNA 분석은 세포별 유전자 발현을 정밀하게 읽을 수 있지만 조직을 해체하면 원래 위치정보가 사라진다. 반대로 공간전사체 기술은 위치를 보존하지만 플랫폼별 격자와 해상도, 고정조건의 제약이 있다. 연구진은 세포막에 붙는 cholesterol-conjugated photolabile hashtag oligonucleotide를 이용해 조직을 분리하기 전에 위치를 빛으로 기록하는 scSTAMP-seq를 개발했다.

세포에 광분해 가능한 올리고를 붙인 뒤 특정 공간에 패턴광을 비추면 노출된 위치와 노출되지 않은 위치가 서로 다른 바코드 상태를 갖는다. 여러 번의 광패턴을 순차 적용하면 위치정보의 해상도를 높일 수 있고, 그 뒤 세포를 분리해 기존 plate 기반 또는 droplet 기반 single-cell sequencing으로 분석한다. 즉 공간정보를 읽는 장비와 분자측정 장비를 하나의 전용 플랫폼에 묶기보다, 위치를 먼저 '도장'처럼 찍어 표준 분석 파이프라인으로 넘기는 방식이다.

연구팀은 인간 embryoid에 적용해 세포의 공간조직과 전사체뿐 아니라 같은 세포의 epigenetic state를 함께 연결했다. 살아 있는 세포와 고정된 시료 모두에서 활용 가능성을 시험했고, 막 표지의 유지시간과 빛 노출 자체가 전사체에 미치는 영향도 평가했다.

## 읽을 때 볼 점

핵심 장점은 modularity다. 이미 널리 쓰이는 single-cell 플랫폼에 공간좌표를 덧붙일 수 있어 새로운 측정기계를 완전히 구축하지 않아도 된다. 특히 transcriptome과 epigenome을 같은 세포에서 읽으면서 위치를 보존할 수 있다는 점이 중요하다.

다만 공간해상도는 광학 패턴, 표지 효율, 세포 이동과 조직형태에 영향을 받는다. 조직을 완전히 그대로 이미지화하는 방식과 달리 최종 분석은 세포 분리를 거치므로, 세포 간 물리적 접촉이나 미세구조 정보를 모두 보존하는 것은 아니다. 인간 embryoid에서의 시연이 다양한 성체 조직과 임상 시료에서 같은 성능을 보장하지도 않는다.

## 논문 링크

- [Nature Biotechnology 논문 보기](https://www.nature.com/articles/s41587-026-03328-5)
