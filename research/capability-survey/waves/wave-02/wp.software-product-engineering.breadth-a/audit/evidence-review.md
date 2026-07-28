# 근거 감사: wp.software-product-engineering.breadth-a

## 범위와 방법

- 대상: Candidate 10개와 내장 evidence 레코드
- 감사 역할: 발견 조사자와 분리된 읽기 전용 독립 근거 감사자
- 확인: 공식·1차 출처의 제목·버전·URL·유형, `claim_scope`, `supports`,
  학습성과에 대한 근거 충분성, 기술별 일반화 한계
- 감사일: `2026-07-28`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 수정 유형 | 5 |
| P2 추적 묶음 | 5 |

## P1 교정

| 대상 | 지적 | 반영 |
|---|---|---|
| API 계약 | OpenAPI만으로 소비자 호환성까지 지지하지 못함 | OpenAPI의 `supports`를 축소하고 승인된 Google AIP-180을 공급자 한계와 함께 추가 |
| 관계형 모델·스키마 | PostgreSQL DDL만으로 migration·호환성을 일반화 | PostgreSQL 18 고정 문서와 PVLDB PRISM 1차 연구를 추가하고 근거 없는 정규화·비정규화 범위 제거 |
| 버전관리 | 분산 workflow 문서만으로 index·충돌·복구 D2가 부족 | `git-add`, `git-merge`, `git-restore` 공식 문서 추가 |
| 빌드 재현성 | 기능·테스트 동등성을 bit-for-bit 재현성의 대체 증거로 허용 | 지정 artifact 또는 unsigned inner artifact의 hash 일치를 필수화하고 차이가 남으면 불합격 처리 |
| NIST 출처 유형 | NISTIR 8397·SP 800-218을 규격으로 분류 | `official_source`로 교정 |

## P2 추적

- mutable 공식 문서는 `checked_at`을 유지하고 정규 Resource 승격 시 고정
  버전·revision을 보강합니다.
- SWEBOK Topics 페이지는 공식 V4.0a PDF의 절·페이지 직접 연결로 보강할 수
  있습니다.
- ISO/IEC/IEEE 29148:2018의 후속 개정 상태를 정기검토에서 추적합니다.
- rebase는 현재 필수 방법이 아니며, Adapter에서 다룰 때 공식 문서를 추가합니다.
- DORA 자료는 고정 효과값의 근거로 사용하지 않으며 정규 Set 승격 시 report·
  methodology 직접 링크를 보강합니다.

## 결론

두 차례 P1 반영 뒤 같은 독립 감사자가 최종 재확인했습니다. 최종 P0 0건,
P1 0건이며 10개 후보 모두 `accept`를 권고했습니다. 후보는 특정 도구나 공급자
효과를 보편적 학습효과로 확정하지 않습니다.
