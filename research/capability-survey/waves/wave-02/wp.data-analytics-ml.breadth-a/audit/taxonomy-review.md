# Taxonomy 감사: wp.data-analytics-ml.breadth-a

## 범위와 방법

- 대상: 신규 Candidate 9개, 기존 영향평가 재사용 판정,
  `taxonomy.ax-capability-map@0.5.0`, 기존 Unit·Set·Signal과 Wave 2 Candidate
- 감사 역할: 발견 조사자와 분리된 읽기 전용 독립 taxonomy 감사자
- 확인: Unit·Set 목적지, 중복·소유권 경계, relation 방향·버전·DAG,
  checkpoint와 Registry 복원 가능성
- 감사일: `2026-07-29`

## 최초 판정

| 구분 | P0 | P1 | P2 |
|---|---:|---:|---:|
| Candidate-level | 0 | 3 | 2 |
| Package-level | 0 | 1 | 0 |
| 합계 | 0 | 4 | 2 |

## P1 교정

- 실제 D2가 책임 메타데이터와 계보 기록인 후보·node를
  `data-catalog-lineage-ownership-metadata`와
  `데이터 카탈로그·계보·책임 메타데이터`로 좁히고 조직 stewardship 운영은
  제외했습니다.
- target·label·calibration·threshold를 사용하는 범위를 일반 ML 전체로
  과대표현하지 않도록 두 후보·node를 `predictive-ml-*`로 좁혔습니다.
- ML 생명주기 후보는 선수 산출물을 종단 실행하는 Set이 아니라
  reference–current drift·성능 비교와 유지·재학습·중단·rollback 판정계약을
  독립적으로 소유하는 Unit이라는 근거를 명시했습니다.
- 조사 README와 Wave checkpoint를 Registry 0.5.0, 네 번째 패키지와 신규
  subdomain 9개 기준으로 갱신했습니다.

## 추가 경계 보강

- 원천 후보는 생산자–소비자 최초 인수계약과 ingest 전 수락을, 데이터 품질
  후보는 반복 실행의 품질 추세·분포 변화·검출률·오탐률 Gate를 소유합니다.
- 전략 측정계약이 승인한 KPI 정의를 분석 지표 후보의 입력으로 고정하고,
  분석 후보는 grain·집계·reconciliation 구현만 소유합니다.

## 결론

최종 독립 재감사 결과 P0 0건, P1 0건, P2 0건입니다. relation 대상과 버전이
유효하고 선수관계 DAG에 순환이 없으며, 신규 후보 9개와 기존 영향평가 재사용
판정 모두 `accept`입니다. `fix`, `defer`, `merge` 권고는 없습니다.
