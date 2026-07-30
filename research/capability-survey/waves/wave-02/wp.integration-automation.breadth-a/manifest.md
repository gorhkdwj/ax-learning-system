# Work Package Manifest: wp.integration-automation.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| 상태 | `promoted` |
| 범위 승인일 | `2026-07-29` |
| 범위 승인 근거 | 사용자가 현재 패키지 승격 뒤 다음 Wave 2 패키지 진행을 지시함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.6.0` (`provisional`) |
| 최대 후보 | `10` |
| 이번 제안 | Unit 7개 + Set 1개 + technology Adapter 1개 + Resource 1개 |
| 동시 작업 패키지 | `1` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, node ID·기술명은 영문 병기 허용 |

## 조사 계약

### 포함

- 외부 API 소비자의 pagination·quota·timeout·오류·호환성 대응
- 이벤트·웹훅의 서명·중복·지연·역순·재전송 처리
- 여러 SaaS 연결의 제한된 동기화와 최종 상태 검증
- 명시적 상태·분기·timer·병렬·승인 대기·중단·재개
- 외부 부작용의 idempotency·deduplication·retry·compensation
- 결정표와 규칙의 우선순위·충돌·미일치·version trace
- 자동화 결과의 postcondition 조회·비교와 reconciliation 필요 판정
- 로컬 테스트 UI를 이용한 변경 내성 자동화
- MCP 연결의 lifecycle·version·capability·schema 계약
- 결정적 workflow와 모델·agent 사용 경계를 판단하는 가이드

### 제외

- API 제공자 표면 설계, 애플리케이션 DB schema와 일반 소프트웨어 테스트
- 데이터 변환 pipeline과 분석·ML workflow
- LLM 호출, agent loop·memory·trajectory와 stochastic evaluation
- 기업 gateway·IAM·broker·rule engine·workflow engine의 운영
- 배포·SLO·incident·중앙 logging·고가용성 platform 운영
- CAPTCHA 우회, 실제 개인 계정·자격증명, 실거래와 고위험 외부 변경
- 보안·개인정보·법률 정책 자체의 전문 판정
- 상세 교재·실습·HUB 구축과 정규 Unit·Set 승격

## 중복 방지 판정

- 일반 HTTP API 계약은
  `unit.software.api-contract-compatibility@1.0.0`이 소유하고, 이 패키지는
  소비자 실행·제한·복구를 다룹니다.
- 데이터 변환 DAG는
  `unit.data-analytics-ml.reproducible-data-transformation-pipelines@1.0.0`이
  소유하고, 이 패키지는 업무 상태와 외부 부작용을 조정합니다.
- 모델 주도 agent orchestration은
  `unit.ai.agent-state-memory-handoff-design@1.0.0`과 관련 Set이
  소유하고, 이 패키지는 결정 가능한 상태전이와 인간 승인 경계를 다룹니다.
- 제품별 SaaS 사용법은 Adapter·Resource로 두고 안정 코어를 복제하지 않습니다.
- MCP는 제품 사용법이나 독립 전문과목이 아니라 version이 고정된 technology
  Adapter 후보로 둡니다.
- 관측 platform 운영은 `platform-quality-operations`가 소유하고, 이 패키지는
  자동화 한 건의 의도·실제 결과와 불일치·조정 필요 판정 증거를 다룹니다.

## 실행 구조

1. 읽기 전용 발견 조사자가 공식 사양·표준·1차 근거와 기존
   Candidate·Unit·Set·Signal을 교차검토했습니다.
2. Codex 메인 세션이 후보 상한 10개 안에서 후보와 잠정 taxonomy node를
   작성했습니다.
3. 발견과 분리된 근거·taxonomy·실용성 감사자가 모든 후보를 독립 검토합니다.
4. Codex 메인 세션이 P0·P1을 반영하고 재감사·checkpoint·전체 검증을
   완료합니다.

## 임시 Gate

- 후보는 10개 상한을 넘지 않습니다.
- 모든 Unit 후보는 D0와 관찰 가능한 D2 행동·산출물을 가집니다.
- 각 후보는 독립적인 공식·표준·1차 근거를 2개 이상 가집니다.
- Unit·Set·Resource·Adapter의 소유권과 인접 렌즈 경계를 명시합니다.
- 실제 외부 시스템이 아닌 fake·local fixture로 제한하며 실행 횟수·시간·비용과
  승인·중단 조건을 평가 계약에 고정합니다.
- 감사 P0 0건과 P1 반영·재확인 전에는 `accepted`로 전환하지 않습니다.
- 정규 Unit·Set 승격은 별도 사용자 지시 전에는 수행하지 않습니다.
- 카탈로그·공개 경계·스키마·단위 테스트와 `git diff --check`를 통과해야 합니다.

## 자동 중단조건

- 필수 근거가 없거나 제목·출처·주장 범위가 실제 문서보다 넓습니다.
- 기존 Candidate·Unit·Set과 같은 D2 산출물·Gate를 가집니다.
- 특정 SaaS·workflow engine·browser 도구 없이는 입문 D2 결과를 평가할 수 없습니다.
- 실제 계정·토큰·개인정보·결제·고위험 외부 변경이 필수입니다.
- 무제한 retry·polling·agent loop 또는 승인 없는 외부 변경이 필요합니다.
- 보안·법률·운영 전문 통제를 이 패키지가 임의로 확정해야 합니다.
- 공개 경계·검증·감사가 실패합니다.

## 최종 판정

- Candidate 10개는 모두 `accepted`입니다.
- 목적지는 Unit 7개, Set 1개, technology Adapter 1개와 D0 Resource
  1개로 유지합니다.
- 근거·taxonomy·실용성 독립 감사의 P0는 모두 0건이었고, P1을 교정하고
  잔여 유지관리 권고를 기록한 뒤 재감사에서 P0·P1 0건을 확인했습니다.
- 경계 Resource는 기존 D2 해법 적합성 Candidate와 AI topology Set을
  중복하지 않도록 용어·책임·라우팅을 설명하는 D0로 제한했습니다.
- 후속 사용자 승인에 따라 핵심 Unit 7개, MCP technology Adapter 역할의
  `protocol` Unit 1개, 공개 Reference 8개, 결정적 workflow Unit 소유의 D0
  경계 Resource 1개와 SaaS 프로젝트 Set 1개를 정규 `cataloged`
  메타데이터로 승격했습니다.
- 상세 fixture·교재·파일럿·학습효과는 아직 검증하지 않았습니다.
