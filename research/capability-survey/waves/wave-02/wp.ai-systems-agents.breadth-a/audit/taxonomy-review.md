# Taxonomy·중복 감사: wp.ai-systems-agents.breadth-a

## 범위와 방법

- 대상: Candidate 8개, 신규 잠정 subdomain 7개, 기존 Unit·Set·Signal,
  Wave 1과 Wave 2 첫 패키지 Candidate
- 감사 역할: 발견 조사자와 분리된 읽기 전용 taxonomy·중복 감사자
- 확인: 소유 경계, 중복·목적지, 후보 종류, 관계 방향·순환, 기존 Signal과
  인접 렌즈 이관
- 감사일: `2026-07-28`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 수정 묶음 | 3 |
| P2 개선 묶음 | 3 |

깨진 참조와 관계 순환은 없었습니다. `Agent Harness`와 Control Loop는 기존
Signal 정본에 남겨 새 Candidate·node의 이중 관리를 피했습니다.

## P1 교정

| 대상 | 지적 | 반영 |
|---|---|---|
| LLM 응용·토폴로지 node | 단일 호출·workflow·agent 선택 소유권 중복 | LLM node를 호출·버전·입출력·routing·fallback으로 좁히고 토폴로지를 단일 소유자로 유지 |
| 토폴로지 후보 | LLM node를 함께 참조하고 호출 계약 선수관계 누락 | 토폴로지 subdomain만 참조하고 LLM 응용 계약을 권장 선수로 추가 |
| RAG 후보 | 종단 간 검색·컨텍스트·생성·평가 조합을 Unit으로 라우팅 | `set.workflow.retrieval-grounded-generation` Set 후보로 변경 |
| 토폴로지 후보 | 여러 기반 역량 조합이 필요한 D2를 Unit으로 라우팅 | `set.project.ai-workflow-agent-topology-comparison` Set 후보로 변경 |
| 토폴로지·node | 기존 Control Loop Signal의 runner 내부 제어까지 소유 | 토폴로지 선택·gate 배치로 좁히고 반복·재시도·멱등성·예산 집행·중단·복구 구현 제외 |
| 두 Set 후보 | 평가 기반 역량의 관계 방향 누락 | Set에서 시스템 평가·회귀 후보로 `requires`를 추가하고 역방향 관계 제거 |

## 기존 콘텐츠와의 소유 경계

- `unit.ai.grounded-output-evaluation`: 제공 근거에 대한 개별 출력 판정
- RAG Set 후보: retrieval·컨텍스트·생성·평가의 종단 간 조합과 실패 귀속
- 시스템 평가 후보: scenario·grader·trajectory·변경 회귀 gate
- `signal.agent.agent-harness`: 여러 기반 역량을 조합하는 기존 Probe Set 경로
- `signal.agent.agent-control-loop`: runner 내부 실행 제어와 신흥 명칭의 관찰
- LLM 응용 node: 호출·버전·입출력·routing·fallback 계약
- 토폴로지 node: 단일 호출·workflow·agent 구조 선택과 gate 배치
- AI 도구 후보: 모델향 의미 계약과 fake adapter 검증
- 통합 렌즈: 실제 재시도·deduplication·전송 수명주기·최종 상태 구현

## P2 반영·추적

- 도구 계약을 부작용 등급·멱등성 요구·오류 의미 선언으로 좁히고 실제 통합
  실행 책임을 제외했습니다.
- 제안 Unit ID의 중복 `ai` 접두어를 제거했습니다.
- 상태·checkpoint, 메모리 수명주기와 handoff envelope는 과업 연속성을 보존하는
  하나의 Unit으로 확정했습니다. 파일럿은 분리 여부를 다시 결정하는 Gate가 아니라
  평가시간과 난이도를 조정하는 자료로만 사용합니다.

## 결론

최종 구성은 잠정 subdomain 7개, Unit 후보 6개, Set 후보 2개입니다. 정규
Unit·Set·Signal은 수정하지 않았습니다. P1 반영 후 독립 재확인과 자동검증에서
P0·P1 0건, 참조 오류·경고 0건과 관계 DAG 순환 0건을 확인했습니다.
