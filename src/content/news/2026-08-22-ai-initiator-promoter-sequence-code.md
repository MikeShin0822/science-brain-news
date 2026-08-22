---
title: "50만 개 DNA 서열과 AI로 유전자 발현을 시작하는 ‘initiator’ 코드를 풀었다"
description: "UC San Diego 연구진은 약 50만 개 initiator 변이의 발현활성을 측정하고 기계학습 모델을 구축해 사람 유전자의 약 60%에서 이 전사 시작 서열을 예측할 수 있는 규칙을 제시했다."
date: "2026-08-22T09:30:00+09:00"
category: "생명과학"
source: "University of California San Diego / Newswise"
sourceUrl: "https://www.newswise.com/articles/researchers-use-ai-to-decode-key-dna-sequence-in-gene-activation"
tags: ["유전자발현", "프로모터", "initiator", "기계학습", "전사"]
importance: "ai-initiator-promoter-sequence-code"
---

## 핵심 요약

유전자가 켜지려면 RNA 중합효소와 여러 전사인자가 DNA의 정확한 위치에서 전사를 시작해야 한다. 이때 프로모터 안의 'initiator(Inr)'라는 짧은 서열은 전사 시작점을 정하는 핵심 요소지만, 어떤 염기 조합이 강한 initiator를 만드는지에 대한 규칙은 오랫동안 불완전했다.

UC San Diego 연구진은 약 50만 개의 서로 다른 initiator 서열을 실험적으로 만들어 각각이 어느 정도의 유전자 발현을 일으키는지 측정했다. 이어 이 대규모 기능 데이터를 기계학습 모델에 학습시켜, DNA 염기서열만 보고 initiator가 존재하는지와 상대적인 활성을 예측하도록 했다.

모델을 사람 유전체에 적용했을 때 약 60%의 인간 유전자에서 initiator 특징이 확인됐다. 연구진은 이 규칙을 이용하면 특정 돌연변이가 전사 시작을 약화시키거나 강화하는지 예측하고, 원하는 발현 강도를 갖는 합성 프로모터를 설계하는 데도 활용할 수 있다고 본다.

## 왜 중요한가

단백질 코딩 영역의 돌연변이는 해석하기 비교적 쉽지만, 프로모터와 같은 조절 DNA의 변이가 질병에 어떤 영향을 주는지는 훨씬 어렵다. 실험 데이터에 기반한 initiator 모델은 '비암호화 변이 → 전사 변화 → 질병 위험' 연결고리를 정량적으로 분석하는 도구가 될 수 있다.

합성생물학에서도 의미가 크다. 세포 종류나 치료 목적에 맞게 유전자 발현량을 정밀 조절해야 하는 유전자치료·세포공학에서는 예측 가능한 프로모터 설계가 중요한 기반기술이기 때문이다.

## 읽을 때 주의할 점

AI 모델이 유전자 발현 전체를 설명하는 것은 아니다. 실제 전사는 initiator 외에도 TATA box, enhancer, 크로마틴 접근성, 세포 유형별 전사인자, 3차원 유전체 구조 등 많은 요소의 영향을 받는다.

또 특정 변이가 initiator 점수를 바꾼다고 해서 곧바로 질병 원인이라는 뜻은 아니다. 환자 유전체와 세포 맥락에서 기능 검증이 추가로 필요하다.

## 출처

[UC San Diego 연구 보도자료 보기](https://www.newswise.com/articles/researchers-use-ai-to-decode-key-dna-sequence-in-gene-activation)
