# 분야 조사: 통합·업무자동화

## 1. 조사 요약

`integration-automation` 렌즈를 제품별 연결법 모음이 아니라 기존 시스템 사이의
계약·상태·부작용·결과를 제한된 실행으로 조정하는 역량으로 조사했습니다.
OpenAPI·HTTP·AsyncAPI·CloudEvents·WebSub·BPMN·SCXML·DMN·WebDriver·MCP의
공식 사양과 표준을 누락 방지 기준으로 사용하고, 기존 공개 카탈로그와 Candidate를
대조해 소프트웨어·데이터·AI·운영 렌즈의 소유권을 분리했습니다.

## 2. Candidate 목록

| Candidate ID | 한국어 표시명 | 후보 목적지 | 목표 | 주요 경계 |
|---|---|---|---|---|
| `candidate.integration-automation.external-api-consumer-resilience` | 외부 API 소비자 통합·복원력 | Unit | D2 | 제공자 API 설계가 아닌 소비자의 제한·오류·복구 |
| `candidate.integration-automation.event-webhook-delivery-contract` | 이벤트·웹훅 전달계약 검증 | Unit | D2 | broker 운영이 아닌 envelope·callback·전달 검증 |
| `candidate.integration-automation.saas-connector-sync-delivery` | SaaS 커넥터 동기화 전달 | Set | D2 | 제품 사용법이 아닌 계약·상태·부작용·검증 조합 |
| `candidate.integration-automation.deterministic-workflow-orchestration` | 결정적 워크플로 상태·오케스트레이션 | Unit | D2 | 데이터 DAG·agent loop가 아닌 명시적 업무 상태전이 |
| `candidate.integration-automation.side-effect-idempotency-retry-compensation` | 부작용 안전성·멱등성·재시도·보상 | Unit | D2 | 고위험 실거래가 아닌 fake 외부 변경의 안전성 |
| `candidate.integration-automation.business-rule-decision-automation` | 비즈니스 규칙·의사결정표 자동화 | Unit | D2 | ML·LLM 판단이 아닌 명시적 규칙과 trace |
| `candidate.integration-automation.automation-outcome-observability-reconciliation` | 자동화 결과관측·상태조정 | Unit | D2 | 중앙 관측 platform이 아닌 실행 결과의 재조회·불일치 판정 |
| `candidate.integration-automation.ui-driven-task-automation` | UI 구동 업무자동화·변경내성 | Unit | D2 | 제품별 RPA 조작이 아닌 semantic locator·postcondition |
| `candidate.integration-automation.mcp-protocol-integration-adapter` | MCP 프로토콜 연결 Adapter | technology Adapter | D2 | MCP `2025-11-25` lifecycle·version·capability 계약 |
| `candidate.integration-automation.deterministic-agentic-boundary-guide` | 결정적 워크플로·에이전트 경계 가이드 | Resource | D0 | 기존 workflow·agent·Set·Signal의 제어 주체와 책임 경계를 구분 |

## 3. 잠정 Taxonomy

다음 `provisional` subdomain을 `integration-automation` 아래에 추가했습니다.

- `external-api-consumer-integration`
- `event-webhook-integration`
- `deterministic-workflow-orchestration`
- `side-effect-safety-recovery`
- `business-rule-decision-automation`
- `automation-outcome-verification`
- `ui-driven-task-automation`
- `integration-protocol-adapters`

SaaS 커넥터 전달은 API·이벤트·workflow·부작용·결과검증을 조합하는 Set으로
투영하며 별도 제품군 node를 만들지 않습니다. MCP는 안정 코어 Unit이 아니라
version이 고정된 protocol Adapter로 `integration-protocol-adapters`에
배치합니다. 결정적 workflow와 agent 경계 가이드는 새 역량 node가 아니라
`deterministic-workflow-orchestration`을 설명하는 횡단 Resource입니다.

## 4. 인접 경계 판정

- API 제공자 표면·호환성은 `software-product-engineering`이, 소비자의
  pagination·quota·timeout·복구는 이 패키지가 소유합니다.
- 데이터 변환·품질·계보 DAG는 `data-analytics-ml`이, 업무 상태·승인·외부
  부작용 오케스트레이션은 이 패키지가 소유합니다.
- LLM 호출·tool contract·agent memory·loop·stochastic evaluation은
  `ai-systems-agents`가 소유합니다. 이 패키지는 결정적 상태전이와 외부
  효과의 실행 경계만 소유합니다.
- 배포·고가용성·SLO·incident·중앙 telemetry는
  `platform-quality-operations`가 소유합니다. 이 패키지는 개별 자동화의
  correlation trace, postcondition과 reconciliation 필요 판정을 다룹니다.
- IAM·비밀관리·개인정보·법률 통제의 내용은
  `security-legal-governance`가 소유하며 이 패키지는 제공된 정책을
  실행계약·승인 Gate에 반영합니다.
- 제품별 SaaS·browser·workflow engine 사용법은 후속 Adapter·Resource가
  담당하며 후보의 D2 Gate는 fake·local fixture로 제품 독립적으로 유지합니다.

## 5. 주요 근거

| 출처 | 확인 범위 |
|---|---|
| OpenAPI Specification 3.2.0·RFC 9110·RFC 6585·RFC 9457·RFC 9700 | HTTP 계약, 상태·429·오류·재시도·인증 안전경계 |
| AsyncAPI 3.0.0·CloudEvents 1.0.2·W3C WebSub | 비동기 channel·message·event envelope·구독·callback·전달 |
| OpenAPI Arazzo 1.1.0 | 여러 API 작업의 입력·출력과 순차 workflow 기술 |
| OMG BPMN 2.0.2·W3C SCXML 1.0·Durable Functions 공식 문서 | 명시적 process·state·transition과 구현별 checkpoint·recovery 사례 |
| OMG DMN 1.5 | decision requirement·decision table·hit policy·규칙 표현 |
| OpenTelemetry Specification 1.59.0 | trace·span·context·attribute·status의 상관관계 |
| Microsoft Graph delta query·Google Calendar sync | 서로 다른 공급자의 초기·증분 동기화, token·삭제·replay·재동기화 사례 |
| W3C WebDriver 2·WAI-ARIA 1.2 | 브라우저 원격제어, element 탐색·상호작용과 semantic role·state |
| Model Context Protocol Specification `2025-11-25` | initialization·version·capability negotiation과 lifecycle |

## 6. 누락·중복 레드팀

- OAuth·API key 발급법은 전문 보안·제품 Adapter 영역이며 실제 자격증명을
  요구하지 않습니다.
- webhook은 API 후보에 숨기지 않고 비동기 전달의 중복·지연·역순·서명·replay
  Gate 때문에 별도 Unit 후보로 유지했습니다.
- retry는 API·workflow마다 복제하지 않고 외부 부작용 안전성 Unit을 공통
  prerequisite로 제안했습니다.
- workflow engine 문법, iPaaS·RPA 제품 UI와 connector catalog는 Adapter·Resource로
  라우팅했습니다.
- 관측성은 platform telemetry 수집이 아니라 자동화 한 건의 의도·시도·관찰
  결과와 불일치·조정 필요 판정으로 제한했습니다. 실제 retry·보상·수동복구는
  부작용 안전성 후보가 소유합니다.
- MCP를 범용 API Unit에 병합하면 protocol lifecycle·version·capability
  negotiation을 잃고, 정규 Unit으로 두면 변동 기술을 과대고정하므로 Adapter로
  분리했습니다.
- AI를 사용하는 모든 workflow를 agent로 부르지 않도록 제어 주체와 기존
  Candidate·Set·Signal의 책임 경계를 설명하는 D0 Resource를 제안했습니다.
  새 과제의 D2 해법 선택은 기존 `solution-fit-assessment`가 소유합니다.
- 화면 자동화는 접근 가능한 UI 구현 Unit과 구분해 기존 UI의 semantic
  locator·wait·postcondition을 소비하는 입장으로 제한했습니다.

## 7. 현재 판정

Candidate 10개와 잠정 subdomain 8개의 근거·taxonomy·실용성 독립 감사를
완료했습니다. 최초 P0는 모두 0건이었고 P1을 교정하고 잔여 유지관리 권고를
기록한 뒤 재감사에서 P0·P1 0건을 확인해 10개 모두 `accepted`로 승인했습니다. 상세
교재·fixture·파일럿·학습효과는 아직 검증하지 않았고 정규 승격도 수행하지
않았습니다.
