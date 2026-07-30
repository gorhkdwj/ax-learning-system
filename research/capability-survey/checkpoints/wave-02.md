# Phase 2 Wave Checkpoint: wave-02

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| 상태 | `ready_for_wave-03-planning` |
| 시작일 | `2026-07-27` |
| 마지막 갱신일 | `2026-07-29` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.6.0` (`provisional`) |
| 동시 작업 패키지 | `1` |
| 작업 패키지별 후보 상한 | `10` |

## 2. 목표와 비목표

### 목표

- 기술·데이터 중심 Breadth 조사 A의 `ai-literacy-trust`,
  `ai-systems-agents`, `software-product-engineering`, `data-analytics-ml`,
  `integration-automation` 순차 조사
- 후보 최대 10개 범위의 발견·중복 제거·목적지 라우팅
- 공식·표준·1차 근거와 역할·품질축 기반 커버리지 확인
- 신규 후보의 evidence·taxonomy·practicality 독립 전수감사
- 필요한 잠정 하위 분류 node의 추가·병합·보류 제안

### 비목표

- 나머지 Wave 2 렌즈의 동시 조사
- 상세 교재·실습·HUB 구축과 개인 학습 우선순위
- 사용자 승인 전 Candidate의 정규 Unit·Set·Resource 승격
- 새 대분류 또는 기존 분류 ID 변경

## 3. 작업 패키지 현황

| Work package | 담당 | 상태 | 후보 | 출력 | 마지막 검증 |
|---|---|---|---:|---|---|
| `wp.ai-literacy-trust.breadth-a` | Codex 메인 + 읽기 전용 조사·감사자 | promoted | 10/10 | `research/capability-survey/waves/wave-02/wp.ai-literacy-trust.breadth-a/` | 2026-07-27 통과·정규 승격 완료 |
| `wp.ai-systems-agents.breadth-a` | Codex 메인 + 읽기 전용 조사·감사자 | promoted | 8/10 | `research/capability-survey/waves/wave-02/wp.ai-systems-agents.breadth-a/` | 2026-07-28 전문판정 위임 반영·감사·정규 승격 완료 |
| `wp.software-product-engineering.breadth-a` | Codex 메인 + 읽기 전용 감사자 | promoted | 10/10 | `research/capability-survey/waves/wave-02/wp.software-product-engineering.breadth-a/` | 2026-07-28 P1 반영·독립 재감사·정규 승격 완료 |
| `wp.data-analytics-ml.breadth-a` | Codex 메인 + 읽기 전용 조사·감사자 | promoted | 10/10 | `research/capability-survey/waves/wave-02/wp.data-analytics-ml.breadth-a/` | 2026-07-29 P1 반영·독립 재감사·정규 승격 완료 |
| `wp.integration-automation.breadth-a` | Codex 메인 + 읽기 전용 조사·감사자 | promoted | 10/10 | `research/capability-survey/waves/wave-02/wp.integration-automation.breadth-a/` | 2026-07-29 P1 반영·잔여 권고 기록·독립 재감사·정규 승격 완료 |

## 4. 승인된 실행 조건

- 사용자가 후보 최대 10개를 승인했습니다.
- 사용자가 동시 작업 패키지 1개를 승인했습니다.
- 첫 패키지는 `ai-literacy-trust`로 고정했습니다.
- 사용자는 후속 지시로 첫 두 패키지의 정규 카탈로그 승격을 승인했습니다.
- 사용자가 `2026-07-28`에 첫 패키지의 후보·잠정 분류·역할별 깊이를 모두
  승인했습니다.
- 과목·후보 표시명은 한국어를 우선하며 node ID와 영문 병기는 허용합니다.
- 다음 순차 패키지는 `ai-systems-agents`, 후보 최대 10개와 동시 패키지 1개로
  승인되었습니다.
- 사용자가 `2026-07-28`에 전문 지식이 필요한 미해결 판단을 Codex에 위임했고,
  Codex는 기존 정본·근거·독립 감사에 따라 운영 기본값을 확정했습니다.
- 사용자가 `2026-07-28`에 Codex의 판정에 따른 정규 승격과 다음 순차 패키지
  진행을 지시해 `software-product-engineering` 패키지를 조사·감사했습니다.
- 사용자가 후속으로 다음 작업 진행을 지시해 `data-analytics-ml` 패키지를
  후보 상한 10개와 동일한 독립 감사 Gate로 조사·감사했습니다.
- 사용자가 `2026-07-29`에 데이터·분석·ML 패키지 커밋, 현재 패키지의 정규
  Unit 승격과 다음 `integration-automation` 패키지 진행을 승인했습니다.

## 5. 잠정 분류와 후보 결과

`ai-literacy-trust` 아래 다음 잠정 subdomain 7개를 추가했습니다.

- `ai-foundations-and-limitations`
- `ai-task-framing-and-use`
- `output-appraisal-and-decision-reliance`
- `trust-calibration`
- `responsible-use-boundaries`
- `ai-impact-awareness`
- `ai-use-transparency`

기존 `evidence-verification`은 유지했습니다. 후보 결과는 신규 Unit 후보 8개,
`unit.foundation.evidence-verification@1.0.0` 병합 1개, 기존 근거 검증 Unit용
Resource 전용 후보 1개입니다. 후속 승인에 따라 신규 Unit 8개와 Resource를
정규 `cataloged` 메타데이터로 승격했고 병합 후보는 기존 Unit을 유지했습니다.

`ai-systems-agents` 아래 다음 잠정 subdomain 7개를 추가했습니다.

- `llm-application-architecture`
- `context-engineering`
- `retrieval-grounding-systems`
- `structured-output-and-tool-contracts`
- `agent-state-memory-handoff`
- `agent-workflow-orchestration`
- `ai-system-evaluation-regression`

후보 결과는 Unit 후보 6개와 여러 기반 역량을 조합하는 Set 후보 2개입니다.
`Agent Harness`와 `Loop Engineering`은 새 Candidate·node로 복제하지 않고 기존
Signal의 Probe Set·관찰 경로를 유지했습니다. 후속 승인에 따라 Unit 6개와
Set 2개를 정규 `cataloged` 메타데이터로 승격했습니다.

`software-product-engineering` 아래 잠정 subdomain 9개를 추가했습니다. 후보
결과는 요구사항·설계·버전관리·API·관계형 DB·UI·테스트·디버깅·빌드 재현성
Unit 후보 9개와 AI 보조 변경 전달 Set 후보 1개입니다. 후속 사용자 지시에 따라
Unit 9개는 공개 Reference와 함께, Set 1개는 승인된 Unit 조합과 평가 Gate로
정규 `cataloged` 메타데이터 승격을 완료했습니다.

`data-analytics-ml` 아래 잠정 subdomain 9개를 추가했습니다. 후보 결과는 데이터
원천계약, 변환 pipeline, 분석 지표 의미계약, 탐색·통계 분석, 데이터 품질,
카탈로그·계보·책임 메타데이터, 예측 ML 문제정의·기준선, 예측 ML 모델 검증,
ML 생명주기의 신규 Unit 후보 9개와 기존 영향평가 Candidate 재사용 1개입니다.
기존 `impact-evaluation`과 `test-and-learn` node 및 최초 발견 Candidate ID는
유지했습니다. 후속 승인에 따라 신규 후보 9개와 기존 영향평가 재사용 1개를
공개 Reference와 함께 정규 `cataloged` Unit으로 승격했습니다. 아직 정규화되지
않은 `measurement-contract`와 `solution-fit-assessment` Candidate 관계는
Unit 확정 전까지 `pending_candidate_relations`에 보존했습니다.

`integration-automation` 아래 다음 잠정 subdomain 8개를 추가했습니다.

- `external-api-consumer-integration`
- `event-webhook-integration`
- `deterministic-workflow-orchestration`
- `side-effect-safety-recovery`
- `business-rule-decision-automation`
- `automation-outcome-verification`
- `ui-driven-task-automation`
- `integration-protocol-adapters`

후보 결과는 외부 API 소비, 이벤트·웹훅, 결정적 workflow, 부작용 안전성,
비즈니스 규칙, 자동화 결과판정과 UI 구동 자동화의 Unit 후보 7개, SaaS
커넥터 동기화 Set 후보 1개, MCP technology Adapter 후보 1개와 기존
해법 적합성 Candidate·AI topology Set·Signal을 잇는 D0 Resource 후보
1개입니다. 근거·taxonomy·실용성 감사의 P1을 반영하고 잔여 유지관리 권고를
기록한 뒤 10개 모두 `accepted`로 승인했습니다.

후속 사용자 승인에 따라 핵심 Unit 7개와 MCP technology Adapter 역할의
`protocol` Unit 1개, 각 Unit의 공개 Reference 8개, 결정적 workflow Unit이
소유하는 D0 경계 Resource 1개와 SaaS 동기화 프로젝트 Set 1개를 정규
`cataloged` 메타데이터로 승격했습니다. `requires`는 `prerequisite`,
`recommended_prerequisite`는 `recommended_before`로 변환했으며 아직
정규화되지 않은 `solution-fit-assessment` Candidate 관계와 기존 AI topology
Set·Signal 연결은 확장 메타데이터에 보존했습니다.

## 6. 중단조건 확인

- [x] 승인된 Manifest와 출력 경로를 만들었습니다.
- [x] 후보 상한과 병렬 규모를 고정했습니다.
- [x] 정규 승격은 승인된 다섯 패키지로 제한했고 Signal은 수정하지 않았습니다.
- [x] 첫 패키지 후보 10개, 둘째 8개, 셋째 10개, 넷째 10개와 다섯째 10개 조사를 완료했습니다.
- [x] 다섯 패키지의 근거·taxonomy·실용성 독립 감사를 완료했습니다.
- [x] 최초 감사 P0는 0건이며 P1을 반영한 후 독립 재확인에서 P0·P1 0건을 확인했습니다.
- [x] 승인된 다섯 패키지의 정규 Unit·Resource·Set·Adapter 메타데이터 승격을 완료했습니다.
- [x] 카탈로그 검증은 오류·경고 없이 통과했습니다.
- [x] 공개 경계 검사는 오류 없이 통과했습니다.
- [x] 단위 테스트 33개가 모두 통과했습니다.
- [x] `git diff --check`가 통과했습니다.

## 7. 다음 한 단계

Wave 2 Breadth 조사 A의 다섯 패키지 조사·감사와 정규 메타데이터 승격을
완료했습니다. 상세 콘텐츠 제작, 파일럿·학습효과 검증은 아직 수행하지
않았습니다. 다음 순차 패키지는 Wave 3의 `human-ai-experience`이며 별도
Checkpoint와 작업 패키지에서 조사·감사를 진행합니다.
