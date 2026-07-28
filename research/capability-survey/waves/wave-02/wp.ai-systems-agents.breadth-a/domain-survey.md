# 분야 조사 보고서: AI 시스템·에이전트

> 후보 정본은 `candidates/<candidate-id>/candidate.json`입니다. 이 문서는 사람이
> 검토할 조사 계약, 범위, 구조, 근거와 결정을 요약하며 후보 전문을 복제하지 않습니다.

## 1. 작업 패키지 계약

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| Work package | `wp.ai-systems-agents.breadth-a` |
| 조사 렌즈 | `ai-systems-agents` |
| 스키마 | `capability-candidate 1.1.0` |
| 조사일 | `2026-07-28` |
| 최대/실제 후보 | 10/8 |
| 출력 경로 | `research/capability-survey/waves/wave-02/wp.ai-systems-agents.breadth-a/` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, node ID·영문 병기 허용 |

### 포함

- LLM 응용의 모델 호출·버전·입출력·실패 계약
- 시스템 지시·도구·외부자료·기록의 컨텍스트 조립과 예산
- query-time 검색·재정렬·근거 조립과 retrieval-grounded 생성
- 구조화 출력의 스키마·검증·복구·중단
- 모델향 도구의 입력·출력·오류·부작용 계약
- 에이전트 상태·메모리 수명주기·checkpoint·handoff
- 단일 호출·고정 workflow·agent 토폴로지의 기술적 비교
- 시스템·trajectory 평가, 실패 taxonomy와 변경 회귀

### 제외

- 일반 사용자의 과업 프레이밍·출력 적합성 판단·책임 있는 사용
- 일반 서비스·API·DB 구현과 소프트웨어 테스트 전체
- corpus ETL·저장·색인 운영과 모델 학습
- MCP·API·SaaS 전송·인증·연결 수명주기와 결정적 자동화 전체
- 배포·SLO·운영 관측성·비용·incident 대응
- 위협모델·권한정책·sandbox·법무·개인정보 전문 통제
- 특정 공급자 SDK·vector DB·agent framework 사용법
- 정규 Unit·Set·Resource·Signal 승격과 상세 커리큘럼 제작

## 2. 소유 경계

| 영역 | 이번 렌즈가 소유하는 범위 | 다른 렌즈·정본으로 넘기는 범위 |
|---|---|---|
| LLM 응용 | 비결정적 호출·버전·입출력·fallback 계약 | 일반 백엔드와 배포는 소프트웨어·플랫폼 |
| 컨텍스트 | 시스템이 매 추론에 제공할 전체 상태·신뢰·예산 | 사용자 요청 작성은 `ai-literacy-trust` |
| 검색·RAG | query-time retrieval·근거 조립·단계별 실패 | corpus 파이프라인은 데이터, 개별 근거 판정은 기존 Unit |
| 구조화 출력 | 모델 출력 스키마·검증·복구·중단 | 일반 JSON 처리와 공급자 SDK는 소프트웨어·Adapter |
| 도구 | 모델향 설명·입출력·오류·부작용 계약 | 전송·인증은 통합, 권한정책은 보안 |
| 상태·메모리 | AI 작업 상태·checkpoint·기억 수명주기·handoff | DB 구현·법적 보존정책·조직 인계는 인접 렌즈 |
| 토폴로지 | 구축 후 단일 호출·workflow·agent 기술 선택 | 사업 해법은 Wave 1, 일반 자동화는 통합 |
| 평가 | 개발·release 평가 세트·trajectory·회귀 gate | 운영 SLO·incident와 업무효과 인과평가는 인접 렌즈 |

## 3. 잠정 분류 구조

`ai-systems-agents` 아래에 잠정 subdomain 7개를 추가했습니다.

| 잠정 node | 초점 | 주요 제외 |
|---|---|---|
| `llm-application-architecture` | 모델 호출·버전·입출력·routing·fallback 계약 | 일반 서비스·배포, 사업 해법과 실행 토폴로지 |
| `context-engineering` | 컨텍스트 선택·순서·격리·압축·예산 | 사용자 prompt, 검색기와 영속 메모리 |
| `retrieval-grounding-systems` | retrieval·근거 조립·인용·보류·최신성 | corpus ETL·저장·색인 운영 |
| `structured-output-and-tool-contracts` | 출력·도구의 스키마·검증·오류·부작용 | 일반 API 전송·인증과 권한정책 |
| `agent-state-memory-handoff` | 상태·checkpoint·메모리 수명주기·인계 | 일반 DB·개인 지식관리 |
| `agent-workflow-orchestration` | 단일 호출·workflow·agent 토폴로지 | 사업 해법·일반 자동화·Loop Engineering 확정 |
| `ai-system-evaluation-regression` | scenario·grader·trajectory·회귀 gate | 운영 SLO와 현장 인과평가 |

다음 항목은 별도 node로 만들지 않았습니다.

- `Agent Harness`는 여러 기반 역량을 조합하는 기존 Signal·Probe Set입니다.
- `Loop Engineering`은 기존 `researching` Signal의 관찰 대상입니다.
- `prompt engineering`은 사용자 과업 프레이밍과 시스템 컨텍스트로 분리합니다.
- `agent observability`는 개발 평가 trace와 운영 관측성으로 분리합니다.
- 특정 vector DB·MCP·A2A·agent SDK는 Adapter 또는 Resource입니다.

## 4. 커버리지 근거

| Query family | 확인 범위 | 대표 출처 | 후보로 정규화한 결과 |
|---|---|---|---|
| LLM 응용 구조 | 호출 경계, workflow·agent 구분, fallback | NIST AI 600-1, Anthropic | 아키텍처·추론 계약 |
| 컨텍스트 | 위치·분량·신뢰·압축·예산 | Lost in the Middle, Anthropic | 시스템 컨텍스트 |
| 검색·RAG | retrieval–generation 결합과 실패 분해 | RAG 원 논문, ARES | 검색·근거 연결 생성 |
| 구조화 인터페이스 | schema·validation과 tool 오류 | JSON Schema, OpenAPI, MCP | 구조화 출력, 도구 계약 |
| 상태·인계 | 메모리 수명주기, task·status·artifact | MemGPT, A2A 1.0 | 상태·메모리·handoff |
| 토폴로지 | 단일 호출·workflow·agent·위임 | Anthropic, ReAct | workflow·agent 토폴로지 |
| 평가 | scenario·grader·trajectory·회귀 | NIST AI 800-2 IPD, Anthropic | 시스템 평가·회귀 |

NIST AI 800-2는 초기 공개초안이며 최종 표준으로 부르지 않습니다. Anthropic
자료는 공급자 실무자료이고 RAG·ReAct·MemGPT·ARES는 제한된 과제와 구현의
1차 연구이므로 특정 방식의 보편적 우월성을 주장하지 않습니다.

## 5. 후보 인벤토리

| Candidate ID | 목적지 | 목표 | 현재 결정 |
|---|---|---|---|
| `candidate.ai-systems-agents.llm-application-architecture-contract` | Unit 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.system-context-design` | Unit 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.retrieval-grounded-generation-design` | Set 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.structured-output-contract-validation` | Unit 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.ai-tool-function-contract-design` | Unit 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.agent-state-memory-handoff-design` | Unit 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.ai-workflow-agent-topology-design` | Set 후보 | D2 | 승인 |
| `candidate.ai-systems-agents.ai-system-evaluation-regression-design` | Unit 후보 | D2 | 승인 |

### 병합·보류 판단

- `unit.ai.grounded-output-evaluation@1.0.0`은 제공 근거에 대한 개별 출력 판정을
  계속 소유합니다. RAG와 시스템 평가 후보는 이를 다시 만들지 않습니다.
- `signal.agent.agent-harness@1.0.0`은 `substantiated` 상태와 기존 Probe Set
  목적지를 유지합니다. 새 포괄 Harness Candidate·node를 만들지 않았습니다.
- `signal.agent.agent-control-loop@1.0.0`은 `researching`·관찰 상태를 유지합니다.
  안정된 상태·도구·종료·평가 요소는 후보에 반영하되 `Loop Engineering` 명칭을
  Unit이나 잠정 node로 승격하지 않았습니다.
- 기존 Signal과 같은 대상을 새 defer·merge Candidate로 이중 관리하지 않았습니다.

신규 후보는 Unit 후보 6개와 여러 기반 역량을 조합하는 Set 후보 2개입니다. 기존
정본으로 병합된 후보 파일은 0개이며 발견된 포괄 신흥 개념 두 건은 기존 Signal에
남겨 중복 생성을 사전에 차단했습니다.

## 6. 학습 흐름과 관찰 가능한 결과

1. 확률적 모델 호출과 결정적 로직·외부 변경 경계를 정의합니다.
2. 시스템 지시·상태·근거·도구 결과를 신뢰와 예산에 따라 조립합니다.
3. 검색·재정렬·근거 조립·생성의 실패를 분리합니다.
4. 모델 출력의 구조를 검증하고 복구 또는 명시적 실패를 선택합니다.
5. 도구 선택·인자·실행·결과 해석·부작용을 별도 경계로 검증합니다.
6. 상태·checkpoint·메모리·handoff의 소유권과 수명주기를 보존합니다.
7. 같은 과제를 단일 호출·workflow·agent로 비교해 최소 복잡도를 선택합니다.
8. 정상·경계·실패 scenario와 반복 회귀 gate로 변경을 검증합니다.

평가는 특정 SDK 사용법이나 단일 성공 실행보다 공급자 중립 계약, 실패 주입,
최종 외부 상태와 재현 가능한 평가 기록을 우선합니다.

## 7. 역할·맥락 커버리지

다음 관점을 조사와 평가 가설에 포함했습니다.

- AI 응용 개발자와 소프트웨어 엔지니어
- retrieval·search·지식관리 담당자와 data steward
- 통합·플랫폼·SRE 담당자
- 평가·QA·테스트 담당자
- 보안·개인정보·감사 검토자
- 현업 소유자·도메인 전문가·인간 승인자

코딩 agent 사례에 치우치지 않도록 문서 합성, 리서치 갱신, 고객지원, 운영 분류,
다국어·쉬운 언어 콘텐츠와 지식관리 사례를 포함합니다. 텍스트뿐 아니라 문서·표,
필요한 경우 이미지·음성·접근성 대체 표현에서 같은 계약 실패를 확인합니다.

## 8. 근거 현황과 제한

- 후보 8개에 evidence 레코드 18개를 기록했습니다.
- 공식 사양·정부 문서와 1차 연구를 우선하고 공급자 문서는 실무 사례로 제한했습니다.
- JSON Schema·OpenAPI는 구조 계약을 정의하지만 모델 출력의 의미 정확성이나
  도구 선택 품질을 보장하지 않습니다.
- MCP·A2A는 프로토콜 사례이며 범용 학습성과나 업무효과의 근거가 아닙니다.
- NIST 문서는 위험·평가 경계를 지원하지만 이 커리큘럼의 Unit 경계를 규정하지
  않습니다.
- agent memory 유형, 자동 grader 타당성, 다중 agent 순효과와 trajectory metric은
  아직 수렴하지 않았습니다.

## 9. 확정 결정과 운영 기본값

- 종단 간 검색·생성·평가 조합은 Set 후보로 유지합니다. query-time retrieval만의
  별도 Unit 후보는 이번 패키지에서 만들지 않습니다. 검색·컨텍스트·근거 판정과
  회귀를 실제로 조합해야 업무 결과가 성립하므로 지금 분리하면 중복 학습성과가
  생깁니다.
- 상태·checkpoint, 메모리 수명주기와 handoff는 하나의 “에이전트 연속성 계약”
  Unit 후보로 유지합니다. 세 기능을 별도 기술 목록이 아니라 중단·재개·위임 뒤
  동일한 과업 소유권과 상태가 보존되는 하나의 D2 scenario로 평가합니다.
- `unit.ai.grounded-output-evaluation@1.0.0`은 RAG Set의 필수 선행 Unit으로
  재사용합니다. 시스템 평가·회귀 Unit에서는 grounding이 평가 대상일 때만 권장
  선행으로 사용하며 새 Resource나 중복 Unit을 만들지 않습니다.
- 프로토콜 독립 도구 계약의 코어는 목적·입출력 schema·오류 의미·부작용 등급·
  권한 요구·멱등성 요구·상관관계입니다. handoff 코어는 task/context ID, 현재
  소유자, 상태, payload·artifact, 완료·취소·실패, provenance·만료입니다.
  MCP·A2A의 전송·인증·discovery·streaming·version negotiation과 SDK 호출은
  Adapter·Resource로 분리합니다.
- 전이성 Gate는 동일 계약 테스트를 통과하는 Adapter 2개로 고정합니다. 하나는
  반드시 로컬 fake adapter이고 다른 하나는 실제 공급자 또는 독립 참조
  구현입니다. 두 유료 공급자 계정을 필수로 요구하지 않습니다.
- 확률적 D2 평가의 기본값은 scenario별 독립 실행 10회입니다. 치명 실패는
  0건, 결정적 assertion은 10/10 통과, 전체 업무 성공은 80% 이상이며 비용·시간
  상한은 모든 실행에서 지켜야 합니다. 성공률이 80~89%이거나 실행별 실패 유형이
  달라 불안정하면 30회로 확대합니다. 이 수치는 파일럿 전 governance default이며
  더 엄격한 도메인 기준은 Overlay에서 상향만 할 수 있습니다.

## 10. 자체 점검

- [x] 최대 10개 후보 상한 안에서 8개 후보로 정규화했습니다.
- [x] 과목·후보 표시명은 한국어를 우선하고 영문은 canonical name·병기로 두었습니다.
- [x] 후보마다 포함·제외·경계와 관찰 가능한 D0·D2 결과를 기록했습니다.
- [x] 잠정 taxonomy만 추가하고 정규 Unit·Set·Resource·Signal은 수정하지 않았습니다.
- [x] 기존 Unit·Signal과 인접 렌즈의 소유권을 명시했습니다.
- [x] 제품·공급자·코딩 agent 목록으로 범위를 대체하지 않았습니다.
- [x] 공식 초안, 공급자 문서와 제한된 1차 연구의 불확실성을 기록했습니다.

## 11. 다음 게이트

발견자와 분리된 근거·taxonomy·실용성 감사의 P1을 반영했고 독립 재확인에서
P0·P1 0건을 확인했습니다. 구조·공개 경계·단위 테스트와 diff 검증을 통과한
패키지의 전문 판단이 필요한 항목은 사용자의 위임에 따라 위 운영 기본값으로
확정했고 후보·잠정 분류·역할별 깊이를 승인 상태로 전환했습니다. 정규 Unit·Set
승격과 다음 작업 패키지는 별도 지시 전에는 수행하지 않습니다.
