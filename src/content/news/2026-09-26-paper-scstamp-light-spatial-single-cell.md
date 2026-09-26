---
title: "빛으로 세포의 위치를 먼저 찍고 single-cell multiome을 읽었다… scSTAMP-seq의 공간 바코딩"
description: "Nature Biotechnology의 scSTAMP-seq는 세포막에 photolabile oligonucleotide를 붙이고 패턴광으로 위치정보를 기록한 뒤 기존 단일세포 sequencing으로 읽는다. 살아 있는 세포와 고정세포, 전사체·후성유전체 결합 분석에 적용됐다."
date: "2026-09-26T09:30:00+09:00"
category: "생명과학"
source: "Nature Biotechnology"
sourceUrl: "https://www.nature.com/articles/s41587-026-03328-5"
tags: ["scSTAMP-seq", "공간전사체", "single-cell", "multiome", "광바코딩"]
importance: "scstamp-light-spatial-single-cell"
---

## 긴 요약

single-cell RNA-seq는 수천 개 세포의 분자상태를 정밀하게 읽을 수 있지만, 조직을 세포 단위로 분리하는 순간 “그 세포가 원래 어디에 있었는가”라는 공간정보를 잃는다. 반대로 공간전사체 기술은 위치를 보존하지만 플랫폼에 따라 해상도, 측정 가능한 분자종, 살아 있는 세포 적용성에 제한이 있다. Nature Biotechnology에 발표된 scSTAMP-seq(single-cell Spatial Transcriptomic And Multiomic Profiling)는 조직을 해리하기 전에 각 세포에 위치를 빛으로 기록한 뒤 표준 single-cell 분석으로 넘기는 방식을 택했다.

기술의 핵심은 cholesterol-conjugated photolabile hashtag oligonucleotide(PHO)다. 이 oligo는 세포막에 붙고 특정 파장의 빛을 받으면 절단된다. 연구진은 디지털 패턴광을 공간적으로 다르게 쏘아 각 위치의 세포에 서로 다른 정도 또는 조합의 oligo 신호를 남겼다. 이후 세포를 섞어 sequencing을 해도 각 세포가 가지고 있는 barcode를 읽어 원래의 공간좌표를 추정할 수 있다. 조직을 분해하기 전에 빛으로 ‘주소’를 새겨 두는 셈이다.

여러 PHO와 순차적인 광조사를 조합하면 단순한 영역 구분을 넘어 더 세밀한 공간부호를 만들 수 있다. 연구진은 살아 있는 세포와 고정세포 모두에서 방법을 시험했고 plate 기반과 droplet 기반 scRNA-seq에 연결했다. 공간정보를 얻기 위해 완전히 새로운 sequencing 장비를 구축하는 대신 기존 single-cell workflow 앞에 광학 tagging 단계를 추가한다는 모듈성이 큰 장점이다.

연구팀은 전사체뿐 아니라 DNA 접근성과 DNA methylation을 함께 측정하는 multiomic workflow에도 scSTAMP를 연결했다. 같은 세포에서 “어디에 있었는가”, “어떤 유전자가 발현되는가”, “chromatin이 얼마나 열려 있는가”, “DNA methylation 상태가 어떤가”를 함께 읽는 방향이다. 사람 iPSC에서 만든 gastruloid/embryoid 모델에서는 발생과정의 공간적 패턴과 후성유전상태의 관계를 재구성했다.

공간생물학의 핵심은 좌표 자체보다 위치가 세포상태와 어떻게 연결되는지를 밝히는 것이다. scSTAMP-seq는 위치정보를 sequencing library 안의 tag로 변환해 이후 계산분석과 직접 결합한다. 특히 여러 molecular modality를 동시에 측정할 때 조직위치와 세포내 상태를 동일한 single-cell 단위로 연결할 수 있다는 것이 이 방법의 가장 중요한 장점이다.

## 읽을 때 볼 점

첫째, 공간해상도는 현미경의 픽셀 크기만으로 정해지지 않는다. 패턴광의 형태, oligo 절단의 동역학, 세포막에 남는 tag 양, 조직의 빛 산란이 실제 좌표 정확도를 좌우한다. 배양세포와 발생모델에서 좋은 성능을 보였더라도 두껍고 불투명한 성인조직에서 같은 성능을 유지하는지는 별도 검증이 필요하다.

둘째, 위치 barcode를 넣은 뒤 조직을 해리하므로 세포 주변의 형태학적 구조를 그대로 보존하는 imaging 기반 공간기법과는 정보의 성격이 다르다. 대신 표준 single-cell sequencing의 높은 분자해상도와 확장성을 얻는다. 연구질문에 따라 어느 접근이 더 유리한지가 달라진다.

셋째, 기술 개발 논문인 만큼 후속 독립 연구실의 재현성과 다양한 조직에서의 benchmark가 중요하다. 초기 데모의 높은 성능이 곧 두껍고 복잡한 모든 임상조직에서 같은 우위를 보장하는 것은 아니다.

## 논문 링크

- [Nature Biotechnology 논문 보기](https://www.nature.com/articles/s41587-026-03328-5)
