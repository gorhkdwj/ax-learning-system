# Taxonomy 독립 감사: wp.human-ai-experience.breadth-a

## 범위

- 신규 잠정 subdomain 8개와 Candidate 9개의 배치
- 기존 Candidate·Unit·Set·Signal 중복과 인접 소유권
- Unit·Resource·defer 목적지, 관계 ID·version과 DAG

감사자는 파일을 수정하지 않고 메인 세션만 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 2 |

1. 신규 node의 공통 domain 수준 `related_ids`에 AI 기초·신뢰·투명성,
   접근 가능한 UI, 부작용 안전성, 인간-AI 통제, workflow, context·memory,
   AI 시스템 평가 같은 구체 node 관계를 추가했습니다.
2. 기대형성·설명·피드백·승인·대화복구·경험평가 후보에 기존 정규 Unit
   관계를 `extensions.existing_catalog_relations`로 보강했습니다.

## 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |

- Candidate 관계는 모두 `1.0.0`을 고정하고 DAG 순환이 없습니다.
- 접근성 Resource는 기존 접근 가능한 UI Unit으로 라우팅하며 새 구현 Unit을
  만들지 않습니다.
- 사회적 단서 Resource는 새 기대형성 후보와 기존 신뢰 보정 Unit을 잇습니다.
- 개인화·기억 후보의 `deferred` 판정과 provisional node 유지는 조사 공백
  추적이라는 Registry 상태와 모순되지 않습니다.

## 결론

최종 P0·P1은 0건이며 현재 후보 배치와 잠정 taxonomy를 승인합니다.
