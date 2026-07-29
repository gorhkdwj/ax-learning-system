# Taxonomy 독립 감사: wp.integration-automation.breadth-a

## 감사 범위

- `taxonomy.ax-capability-map@0.6.0`의 신규 provisional subdomain 8개
- Candidate 10개의 node 배치와 부모·관련 node
- Unit 7개, Set 1개, technology Adapter 1개, Resource 1개의 목적지
- 기존 Candidate·Unit·Set·Signal과의 중복 및 인접 렌즈 소유권
- Candidate 관계의 정확한 ID·version과 DAG 순환

감사자는 파일을 수정하지 않았고 Codex 메인 세션만 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 4 |
| P2 | 2 |

P1과 P2는 다음과 같이 반영했습니다.

1. 결정적 workflow·agent 경계 가이드를 D2 선택 과제가 아닌 D0 용어·책임·라우팅
   Resource로 축소하고 기존 `solution-fit-assessment` Candidate와 AI topology
   Set·Signal을 정확히 연결했습니다.
2. SaaS 커넥터 Set에 `deterministic-workflow-orchestration` subdomain과
   Candidate `requires` 관계를 추가했습니다.
3. Manifest의 잘못된 Agent 상태 Unit ID를
   `unit.ai.agent-state-memory-handoff-design@1.0.0`으로 교정했습니다.
4. Registry와 상태 문서를 `taxonomy.ax-capability-map@0.6.0`으로 맞추고 신규
   node 8개와 다섯 번째 패키지를 기록했습니다.
5. 외부 API 후보를 “소비자 실행·복구 실천”으로 정리하고 기존 API 계약
   Candidate를 권고 선수로 연결했습니다.
6. 결과검증은 상태 재조회·비교·불일치·조정 필요 판정을, 부작용 안전성은 그
   판정 뒤 retry·중복방지·보상·수동복구 실행을 소유하도록 분리했습니다.

## 최종 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |

- 신규 subdomain 8개의 부모·관련 node와 포함·제외 경계가 유효합니다.
- Candidate 10개는 모두 `accept`이며 `fix`·`defer`·`merge` 권고가 없습니다.
- Candidate 관계의 ID·version이 정확하고 DAG 순환이 없습니다.
- Candidate·taxonomy·Manifest·분야 조사·평가 계약의 소유권 경계가 일치합니다.

## 검증

- `python tools/validate_catalog.py`: 오류 0건, 경고 0건
