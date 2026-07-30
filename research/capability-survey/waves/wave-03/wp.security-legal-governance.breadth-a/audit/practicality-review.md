# 실용성·안전 독립 감사: wp.security-legal-governance.breadth-a

## 범위

- Candidate 10개의 D0·D2·제한 D3 산출물·Gate
- 합성 fixture·sandbox·수치 상한·멱등성·cleanup·evidence 보존
- qualified review 이관과 AI Set 조합·transfer 평가계약

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 7개 교정군 |

후보별 `fixture@1.0.0`, D0 12사례·오답 0건, 결함 6건·전부 탐지·처리,
고정 제출 artifact를 추가했습니다. 공통으로 독립 sandbox 2회 실행의
canonical hash 일치, 추가 mutation·잔여 자원 0건, 초기·최종 manifest 일치와
sanitized evidence hash 보존을 요구합니다.

break-glass 승인·만료·회수, synthetic key state machine, 공급망
detect·block·quarantine·remediate·revalidate, incident evidence 필드와
45분·20단계 상한, AI 위협 유형별 주입, Set blocking·N/A·qualified routing을
각각 수치 Gate로 보강했습니다.

## 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |

- AI transfer fixture는 6사례·허용 오류 0건·동일 제출 artifact로 고정했습니다.
- 실제·운영 private key는 금지하고 일회성 synthetic test keypair만 허용합니다.
- 실제 fixture·runner 구현은 `required_before_activation`이며 Phase 2
  `cataloged` 승격과 구분됩니다.

## 결론

최종 P0·P1은 0건이며 9개 Unit 후보와 1개 Set 후보 모두 `cataloged` 승격
조건을 충족합니다.
