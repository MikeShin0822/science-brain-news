---
title: "단일세포·공간 multi-omics의 잡음을 반복적으로 줄이며 통합했다… 6개 modality·13개 플랫폼을 묶은 DePass"
description: "Nature Cell Biology Technical Report가 paired single-cell 및 spatial multi-omics에서 denoising과 embedding 통합을 반복적으로 결합하는 graph-learning framework DePass를 제시하고 6개 modality, 9개 조직, 13개 실험 플랫폼에서 비교 평가했다."
date: "2026-09-25T09:30:00+09:00"
category: "생명과학"
source: "Nature Cell Biology"
sourceUrl: "https://www.nature.com/articles/s41556-026-02067-8"
tags: ["single-cell", "spatial-omics", "multi-omics", "그래프학습", "DePass", "생물정보학"]
importance: "depass-multiomics-integration"
---

## 긴 요약

같은 세포에서 RNA, 단백질, 염색질 접근성 같은 여러 분자층을 동시에 측정하거나, 조직 위치정보와 함께 multi-omics를 얻는 기술이 빠르게 늘고 있다. 문제는 서로 다른 modality의 값 범위와 잡음구조가 크게 다르고, 측정량이 적은 단일세포 데이터에서는 결측과 technical noise가 특히 심하다는 점이다. Nature Cell Biology에 Technical Report로 발표된 DePass는 이런 paired multi-omics를 하나의 공통표현으로 통합할 때 단순히 modality를 정렬하는 데서 끝나지 않고, 통합 결과를 이용해 다시 원자료의 잡음을 줄이는 과정을 반복하는 graph-learning 구조를 제안했다.

DePass의 핵심은 enhancement와 integration을 한 방향으로만 수행하지 않는 것이다. 각 modality에서 세포 또는 공간 spot 사이의 관계를 그래프로 표현하고, 초기 특징을 이용해 공통 embedding을 만든 뒤, 그 embedding에서 얻은 이웃관계를 이용해 각 modality의 신호를 다시 보정한다. 이렇게 개선된 특징을 다시 통합단계로 보내 여러 차례 순환시키면서, 잡음 때문에 처음에는 보이지 않던 공통 생물학적 구조를 강화하는 방식이다.

연구진은 RNA, 단백질, chromatin accessibility, metabolite imaging 등 6개 modality를 포함한 데이터에서 DePass를 시험했다. 총 9개 조직과 13개 실험 플랫폼을 사용해 single-cell paired data와 spatial multi-omics 모두를 평가했고, 기존 통합기법들과 비교했을 때 cell-type alignment, modality mixing, 공간적 구조 보존 등의 여러 지표에서 높은 성능을 보였다고 보고했다. 특정 한 종류의 sequencing technology만을 위한 알고리즘이 아니라 서로 다른 paired measurement에 공통으로 적용할 수 있도록 설계한 점이 특징이다.

연구팀은 자체 제작한 colorectal cancer Stereo-CITE-seq 데이터에도 방법을 적용했다. RNA와 표면단백질을 공간적으로 함께 측정한 데이터에서 T cell과 macrophage niche의 세부 구조를 더 선명하게 분리하고, 종양조직 안에서 서로 다른 세포상태가 공간적으로 배치되는 이질성을 near-single-cell scale로 보여줬다. raw data에서 약한 RNA-단백질 상관성이 enhancement 뒤 더 뚜렷해졌고, 학습한 한 modality에서 다른 modality를 예측하는 성능도 일부 향상됐다.

또한 mouse embryo의 여러 modality를 동시에 포함하는 공간자료와 기존 single-cell multiome 데이터에서도 같은 framework를 적용했다. 저자들은 단일세포와 공간데이터를 별도의 문제로 처리하는 기존 도구보다 하나의 구조로 다양한 데이터형을 다룰 수 있다는 점을 장점으로 강조한다. 구현코드와 문서, protocol도 공개돼 있어 후속 연구자가 독립적으로 재현하거나 자신의 데이터에 적용할 수 있다.

## 읽을 때 볼 점

첫째, multi-omics 통합에서 높은 benchmark 점수와 생물학적 진실은 완전히 같은 개념이 아니다. 알고리즘이 modality 사이의 공통구조를 너무 강하게 강화하면 실제로 존재하는 modality-specific variation까지 지워버리는 over-smoothing 위험이 있다. 따라서 새로운 세포상태나 공간 niche를 발견했을 때는 원자료와 독립된 실험적 표지를 함께 확인해야 한다.

둘째, DePass는 paired data, 즉 같은 세포나 같은 위치에서 여러 modality가 연결돼 있다는 정보를 적극 활용한다. 서로 다른 사람이나 서로 다른 세포집단에서 따로 측정한 completely unpaired data를 통합하는 문제와는 조건이 다르다. 실제 연구설계가 DePass가 가정하는 paired structure를 얼마나 만족하는지 확인해야 한다.

셋째, 자체 colorectal cancer 사례는 알고리즘의 활용 예시이지만 그 생물학적 발견 자체가 별도의 임상결론을 확정하는 것은 아니다. 이번 논문의 중심 성과는 특정 종양표지보다 여러 multi-omics 플랫폼을 한 graph-learning framework로 통합하고 denoising과 integration을 상호강화한 계산방법론이다.

## 논문 링크

- [Nature Cell Biology 논문 보기](https://www.nature.com/articles/s41556-026-02067-8)
