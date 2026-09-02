---
title: "RNA 표적 CRISPR의 knockdown을 과대평가하던 RT-qPCR 인공신호가 발견됐다"
description: "Nature Biotechnology 연구가 Csm·Cas13b·CasRx에서 guide RNA가 RNA 추출물에 함께 남아 역전사를 방해하면서 실제보다 큰 knockdown처럼 보이는 공통 측정오류를 규명했다."
date: "2026-09-02T09:30:00+09:00"
category: "논문"
source: "Nature Biotechnology"
sourceUrl: "https://www.nature.com/articles/s41587-026-03291-1"
tags: ["CRISPR", "Cas13", "RT-qPCR", "RNA", "측정오류"]
importance: "rna-crispr-rtqpcr-artifact"
---

## 긴 요약

RNA를 직접 표적하는 CRISPR 시스템은 DNA를 영구 변경하지 않고 특정 전사체를 줄일 수 있어 연구와 치료 플랫폼으로 주목받고 있다. knockdown 효율은 흔히 RT-qPCR로 측정되는데, 이번 Nature Biotechnology 연구는 이 표준 측정법 자체가 RNA 표적 CRISPR에서 체계적으로 효율을 부풀릴 수 있음을 보여준다.

연구진은 Csm 시스템에서 RNase 활성을 제거한 ‘dead’ 효소가 단백질 수준에서는 표적을 줄이지 못하는데도 RT-qPCR에서는 강한 knockdown처럼 보이는 이상현상을 발견했다. 원인을 추적하자 guide RNA가 세포 RNA를 추출하는 과정에서 함께 정제돼 표적 RNA에 다시 결합하고, 역전사효소가 지나가는 것을 막는다는 사실이 드러났다. 특히 qPCR amplicon이 guide 결합부위를 가로지르거나 그보다 가까운 upstream에 있을 때 오류가 컸고 downstream amplicon은 상대적으로 정확했다.

이 현상은 Csm 하나에 국한되지 않았다. PspCas13b와 CasRx에서도 catalytically dead 효소가 RT-qPCR상으로는 가짜 knockdown을 보였다. 실제 단백질 측정에서는 효과가 없었다. 예를 들어 일부 조건에서 spanning amplicon은 80~90% 수준의 knockdown을 보고했지만 downstream 위치의 측정은 훨씬 낮거나 거의 변화가 없었다.

기전을 확인하기 위해 합성 guide RNA를 역전사 반응에 직접 넣자 같은 오류가 재현됐다. 반대로 guide와 결합하는 보조 ASO로 guide를 가두거나, 강한 strand-displacement 능력을 가진 processive reverse transcriptase인 ultraMarathonRT를 사용하면 오류가 줄었다. 연구진은 표준 RT를 쓸 경우 downstream primer를 사용하거나, spanning amplicon을 써야 한다면 strand-displacing RT를 사용하고 단백질·RNA-seq 같은 독립 방법으로 확인할 것을 권고했다.

## 읽을 때 볼 점

첫째, 이 연구의 파급력은 새로운 CRISPR 효소를 만든 데 있지 않고 이미 널리 사용되는 정량법의 함정을 찾아낸 데 있다. 기존 RNA-targeting CRISPR 논문 중 guide 결합부위를 가로지르는 primer만으로 효율을 보고한 결과는 실제 knockdown 규모를 재검토할 필요가 있다.

둘째, ‘효과가 모두 가짜’라는 뜻은 아니다. wild-type Cas13/Csm은 실제 RNA·단백질 감소를 일으켰지만, RT-qPCR이 그 크기를 과장할 수 있다는 것이다. 실험설계와 primer 위치가 중요하다.

셋째, 비슷한 원리는 siRNA, shRNA, antisense oligonucleotide처럼 표적 RNA에 강하게 결합하는 다른 기술에도 적용될 가능성이 있다. RNA knockdown 분야에서 orthogonal validation을 표준화해야 한다는 방법론적 경고로 읽을 가치가 크다.

## 논문 링크

[Nature Biotechnology 논문 보기](https://www.nature.com/articles/s41587-026-03291-1)