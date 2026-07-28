# 분야 조사: 소프트웨어·제품 엔지니어링

## 1. 조사 요약

`software-product-engineering` 렌즈를 기술·프레임워크 목록이 아니라 변경 가능한
소프트웨어를 요구–설계–구현–검증–통합하는 공학 행동으로 조사했습니다.
SWEBOK V4.0a의 요구사항·설계·구축·테스트·형상관리·유지보수 범위를 누락 방지
기준으로 사용하고 OpenAPI, PostgreSQL, W3C·WHATWG, Git, NIST와
Reproducible Builds의 공식 문서로 구체 경계를 확인했습니다.

## 2. Candidate 목록

| Candidate ID | 한국어 표시명 | 후보 목적지 | 목표 | 주요 경계 |
|---|---|---|---|---|
| `candidate.software-product-engineering.requirements-acceptance-traceability` | 요구사항·인수기준·추적 설계 | Unit | D2 | 제품 전략이 아닌 단일 변경의 검증 계약 |
| `candidate.software-product-engineering.modular-design-dependency-boundaries` | 모듈형 설계·의존성 경계 | Unit | D2 | 프레임워크 구조가 아닌 책임·변경 경계 |
| `candidate.software-product-engineering.version-control-change-integration` | 버전관리·변경 통합 | Unit | D2 | 특정 호스팅 UI·단일 branching 정책 제외 |
| `candidate.software-product-engineering.api-contract-compatibility` | API 계약·호환성 설계 | Unit | D2 | HTTP 소비자 계약, MCP·SaaS 통합 제외 |
| `candidate.software-product-engineering.relational-data-model-schema-evolution` | 관계형 데이터 모델·스키마 진화 | Unit | D2 | 애플리케이션 DB, 분석모델·DB 운영 제외 |
| `candidate.software-product-engineering.accessible-ui-state-interaction` | 접근 가능한 UI 상태·상호작용 구현 | Unit | D2 | 구현·검증, UX 연구·법적 선언 제외 |
| `candidate.software-product-engineering.layered-software-verification` | 계층형 소프트웨어 검증·테스트 | Unit | D2 | 결정적 변경, AI 확률평가·운영 SLO 제외 |
| `candidate.software-product-engineering.reproducible-debugging-fault-isolation` | 재현 가능한 디버깅·결함 격리 | Unit | D2 | 개발환경 결함, 운영 incident 제외 |
| `candidate.software-product-engineering.build-dependency-reproducibility` | 빌드·의존성 재현성 | Unit | D2 | 재현 계약, 공급망 통제·CI 운영 제외 |
| `candidate.software-product-engineering.ai-assisted-change-delivery` | AI 보조 소프트웨어 변경 전달 | Set | D2 | 특정 도구가 아닌 기존 공학 Gate 조합 |

## 3. 잠정 Taxonomy

다음 `provisional` subdomain을 `software-product-engineering` 아래에 추가했습니다.

- `software-requirements-acceptance`
- `modular-software-design`
- `version-control-change-integration`
- `api-contracts-compatibility`
- `relational-data-modeling-schema-evolution`
- `accessible-ui-state-interaction`
- `software-verification-testing`
- `debugging-fault-isolation`
- `build-dependency-reproducibility`

프론트엔드·백엔드·제품 엔지니어는 이 node들의 조합 보기이며 별도 정규
대분류로 복제하지 않습니다. AI 보조 변경 전달은 독립 역량 node가 아니라 이
구성 역량들을 조합하는 Set으로만 둡니다.

## 4. 인접 경계 판정

- LLM 호출·컨텍스트·AI 도구·stochastic eval은 `ai-systems-agents`가 소유합니다.
- 일반 HTTP API 계약은 이 패키지가, MCP·SaaS 연결과 업무 orchestration은
  `integration-automation`이 소유합니다.
- 관계형 애플리케이션 schema는 이 패키지가, 분석·ML 데이터 모델과 파이프라인은
  `data-analytics-ml`이 소유합니다.
- UI 상태·semantic interaction 구현은 이 패키지가, 사용자 연구·Human-AI
  interaction 전략은 `human-ai-experience`가 소유합니다.
- 결정적 개발 검증은 이 패키지가, 배포·SLO·관측성·incident 대응은
  `platform-quality-operations`가 소유합니다.
- 보안·개인정보·권한·법률 통제의 내용은 `security-legal-governance`가
  소유하고 이 패키지는 제공된 통제가 요구·설계·테스트에 반영되는지를 다룹니다.

## 5. 주요 근거

| 출처 | 확인 범위 |
|---|---|
| IEEE Computer Society, SWEBOK Guide V4.0a | 요구사항·설계·구축·테스트·형상관리·유지보수 지식영역 |
| ISO/IEC/IEEE 29148:2018 | 요구공학 생명주기·정보항목 |
| Git 공식 문서 | 분산 workflow·branch·merge·bisect |
| OpenAPI Specification 3.2.0 | 언어 중립 HTTP API 계약 |
| PostgreSQL 18 공식 문서 | 관계형 제약과 table definition 변경 |
| WCAG 2.2·WHATWG HTML | UI 이름·역할·상태·입력·오류·접근성 계약 |
| NISTIR 8397 | 여러 소프트웨어 검증 기법의 조합 |
| NIST SP 800-218 | 개발환경·변경추적·release 구성요소 provenance 경계 |
| Reproducible Builds 정의 | 소스·환경·명령·artifact 재현성 |
| DORA 2025·GitHub 공식 지침 | AI 보조 개발 효과의 맥락 의존성과 검증·리뷰 필요 |

## 6. 누락·중복 레드팀

- 언어 문법·프레임워크 사용법은 Adapter·Resource이며 독립 Candidate로 만들지
  않았습니다.
- code review는 변경 통합·테스트·AI 보조 전달에 포함하고 별도 Unit으로
  과분할하지 않았습니다.
- refactoring은 모듈형 설계의 검증 가능한 변경 행동으로 포함했습니다.
- secure coding·threat modeling·IAM·supply-chain attestation은 전문 보안
  렌즈로 넘기되 요구·테스트·재현성의 횡단축에서 누락하지 않았습니다.
- 성능·관측성·배포·incident는 운영 렌즈로 넘겼습니다.
- 프론트엔드와 백엔드를 직무별 기술스택 과정으로 축소하지 않았습니다.

## 7. 현재 판정

Candidate 10개는 근거·taxonomy·실용성 독립 감사의 P1을 반영한 뒤 모두
`accepted`로 승인했습니다. 최종 재감사 결과는 P0 0건, P1 0건입니다. 이 판정은
후속 사용자 지시에 따라 Unit 9개와 Set 1개의 정규 `cataloged` 메타데이터
승격으로 이어졌습니다. 상세 교재와 학습효과는 아직 검증되지 않았습니다.
