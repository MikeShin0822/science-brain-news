---
title: "시냅스 가중치는 고정해도 수십 개 과제를 바꿔 풀었다… 뉴런 흥분성만 학습하는 bias-only network"
description: "Communications Biology 연구진이 무작위로 고정된 시냅스 연결을 유지한 채 뉴런별 bias current만 학습해 feedforward·recurrent network가 분류, 회귀, 시계열, 게임, 운동제어 등 여러 과제를 전환해 수행할 수 있음을 보였다."
date: "2026-09-27T09:30:00+09:00"
category: "뇌과학"
source: "Communications Biology"
sourceUrl: "https://www.nature.com/articles/s42003-026-10877-7"
tags: ["신경망", "흥분성", "시냅스가소성", "representational drift", "계산신경과학"]
importance: "bias-only-fixed-synapse-computing"
---

## 긴 요약

학습과 기억은 흔히 뉴런 사이 시냅스 연결강도가 바뀌는 synaptic plasticity로 설명된다. 인공신경망도 대부분 수많은 weight를 조절해 과제를 학습한다. 하지만 연결가중치를 계속 바꾸는 방식은 파라미터 수가 많고, 새로운 과제를 배울 때 이전 과제의 연결을 덮어쓰는 catastrophic forgetting 문제가 생긴다. 실제 뇌는 오랫동안 다양한 기술을 유지하면서도 상황에 따라 빠르게 계산을 바꿀 수 있기 때문에, 시냅스 변화 외의 조절기전이 어느 정도 역할을 하는지가 중요한 질문이다.

Communications Biology 연구진은 각 뉴런의 흥분성에 해당하는 bias current만 과제별로 조절하고, 뉴런 사이의 synaptic weight는 처음의 무작위 연결상태로 고정한 네트워크를 분석했다. feedforward network와 recurrent network 모두에서 과제별 bias 벡터만 바꾸는 방식으로 서로 다른 계산상태를 빠르게 호출할 수 있었다.

이 방식은 단순한 toy problem에만 작동하지 않았다. 회귀와 분류, 자율적인 time-series 생성, 게임, 두 관절 운동제어 등 서로 성격이 다른 수십 개 과제에서 고정연결 네트워크가 과제별 bias를 사용해 성능을 냈다. 즉 동일한 연결구조가 뉴런별 excitability 패턴에 따라 여러 계산기처럼 재구성될 수 있었다.

연구진은 recurrent network에서 이러한 상태전환이 representational drift와도 양립할 수 있음을 보였다. 개별 뉴런의 표현은 시간에 따라 달라질 수 있지만, population level의 계산결과는 안정적으로 유지될 수 있었다. bias-only learning은 뉴런 수준의 변동과 집단 수준의 안정성을 동시에 설명하는 하나의 계산모델을 제공한다.

저자들은 생물학적으로 basal ganglia나 cerebellum 같은 하위피질 구조가 neocortex에 과제별 bias 입력을 제공하는 상황을 가설로 제시한다. 핵심 주장은 뇌가 실제로 이 방식만 사용한다는 것이 아니라, 빠른 task switching과 기억 간섭 감소를 위해 시냅스 재학습 없이 excitability modulation만으로도 놀랄 만큼 많은 계산이 가능하다는 것이다.

## 읽을 때 볼 점

첫째, 이 논문은 계산모델 연구다. 실제 피질에서 과제별 뉴런 흥분성 벡터가 이런 방식으로 저장되고 불러와진다는 생체실험을 직접 보여준 것이 아니다. 생물학적 plausibility와 계산 가능성은 구분해야 한다.

둘째, 시냅스 가중치를 고정했다는 것은 synaptic plasticity가 필요 없다는 뜻이 아니다. 실제 뇌에서는 장기기억 형성과 회로발달에 시냅스 변화가 핵심이라는 강한 증거가 있다. 이 모델은 그 위에 더 빠른 조절층이 추가될 가능성을 제시한다.

셋째, 저자 일부는 관련 기술과 연결된 기업 역할 및 provisional patent를 공개했다. 또한 네트워크의 무작위 고정연결, bias 학습규칙과 과제 구성은 모델설계에 의존한다. 독립적인 구현과 생체자료를 통한 검증이 후속 단계다.

## 논문 링크

- [Communications Biology 논문 보기](https://www.nature.com/articles/s42003-026-10877-7)
