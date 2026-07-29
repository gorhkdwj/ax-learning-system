# 근거 감사: wp.data-analytics-ml.breadth-a

## 범위와 방법

- 대상: 신규 Candidate 9개, 재사용 Candidate 1개와 내장 evidence 레코드
- 감사 역할: 발견 조사자와 분리된 읽기 전용 독립 근거 감사자
- 확인: 공식·표준·1차 출처의 제목·버전·URL·유형, `claim_scope`,
  `supports`, D0·D2 학습성과의 근거 충분성과 맥락 전이 한계
- 감사일: `2026-07-29`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 수정 유형 | 6 |
| P2 추적 묶음 | 4 |

## P1 교정

- 데이터 변환 후보의 NIST 출처를 최신 Volume 6 Version 3의 정확한 제목과
  DOI로 교정하고 Airflow 공식 best practices와 Google Dataflow 1차 연구를
  보강했습니다.
- 분석 지표 후보에 SDMX 3.1, ISO/IEC 11179-4와 dbt Measures의 제한된
  구현 근거를 추가하고 제품별 일반화를 금지했습니다.
- 원천 계약에 W3C Data on the Web Best Practices를 추가해 소비자 관점의
  구조·품질·provenance·version 계약을 보강했습니다.
- 탐색·통계 분석의 ASA PDF 표제를 실제 문서와 일치시켰습니다.
- 데이터 품질에 ISO/IEC 25012를 추가해 일반 품질 요구·측정·평가 범위를
  보강했습니다.
- 예측 ML 문제정의에는 Google 문서의 정확한 표제와 비ML·단순 모델 기준선,
  threshold·오류비용 근거를 반영했습니다.

## P2 추적

- dbt `Measures`는 현재 공식 문서이지만 새 spec에서 deprecated 상태이므로
  Resource 승격 시 최신 simple metrics·OSI 문서로 교체하거나 역사적 구현
  사례임을 명시합니다.
- Airflow·scikit-learn의 `/stable/` 및 Google 교육 문서는 변경 가능하므로
  승격 시 고정 버전·revision을 기록합니다.
- NIST AI RMF Playbook은 후속 개정 상태를 정기적으로 재확인합니다.
- RDaF·DWBP·DQV·Google Data Validation의 서로 다른 적용 맥락을 보편화하지
  않고, 다른 업무 맥락으로 옮길 때 로컬 fixture로 검증합니다.

## 결론

P1 반영 후 독립 감사자가 최종 재확인했습니다. 최종 P0 0건, P1 0건이며 신규
후보 9개와 기존 영향평가 재사용 1개 모두 `accept`를 권고했습니다. P2는
정규 Resource 승격과 상세 평가설계 때 추적할 비차단 항목입니다.
