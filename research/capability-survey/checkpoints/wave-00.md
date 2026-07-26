# Phase 2 Wave Checkpoint: wave-00

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-00` |
| 상태 | `approved` |
| 시작일 | 2026-07-26 |
| 마지막 갱신일 | 2026-07-26 |
| 총괄 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.0.0` |
| Trend Signal 스키마 | `trend-signal 1.0.0` |

## 2. 완료된 준비

- Claude Code 프로젝트 진입점 `CLAUDE.md`
- 읽기 전용 조사·근거·분류·실무성 에이전트 정의
- Phase 2 Runbook과 잠정 조사 렌즈
- Candidate JSON Schema와 작성 템플릿
- 분야 보고서와 Wave Checkpoint 템플릿
- 단일 카탈로그 검증기 Candidate 지원

2026-07-26 사용자 승인에 따라 `wp.ax-strategy-value.pilot`의 읽기 전용
후보 조사를 시작했습니다. Candidate 파일은 아직 작성하지 않았습니다.

## 3. 목표와 비목표

### Wave 0 목표

- 잠정 조사 렌즈의 포함·제외 범위를 확정합니다.
- 첫 시험 배치의 대상, 최대 후보 수와 감사 방식을 승인받습니다.
- 경계 사례를 이용해 에이전트 판정 일치도를 보정합니다.

### 비목표

- 전체 분야 Breadth 조사
- 상세 교재·실습·HUB 구축
- Candidate·Signal의 Unit·Set 승격
- 현재 사용자 학습 우선순위 배정

## 4. 잠정 조사 렌즈

| ID | 이름 | 상태 |
|---|---|---|
| `ax-strategy-value` | AX 전략·업무재설계·가치실현 | 시험 배치 진행 |
| `ai-literacy-trust` | AI 리터러시·검증·책임 있는 사용 | Wave 0 승인·미조사 |
| `ai-systems-agents` | LLM·RAG·에이전트 시스템 | Wave 0 승인·미조사 |
| `software-product-engineering` | 소프트웨어·제품 엔지니어링과 바이브 코딩 | Wave 0 승인·미조사 |
| `data-analytics-ml` | 데이터·분석·ML·데이터 거버넌스 | Wave 0 승인·미조사 |
| `integration-automation` | API·MCP·SaaS·업무자동화 | Wave 0 승인·미조사 |
| `human-ai-experience` | UI·UX·Human-AI Interaction·접근성 | Wave 0 승인·미조사 |
| `platform-quality-operations` | 평가·배포·관측성·비용·운영·복구 | Wave 0 승인·미조사 |
| `security-legal-governance` | 보안·개인정보·권한·법무·윤리 | Wave 0 승인·미조사 |
| `organization-adoption` | 조직변화·협업·교육운영·성과확산 | Wave 0 승인·미조사 |

이 목록은 누락 방지용 조사 렌즈이며 정규 대분류가 아닙니다.

## 5. 첫 시험 배치 제안

| 필드 | 제안 |
|---|---|
| 작업 패키지 | `wp.ax-strategy-value.pilot` |
| 대분류 렌즈 | `ax-strategy-value` |
| 최대 후보 | 10개 |
| 포함 | AX 가치발견, 업무·의사결정·프로세스 재설계, 자동화 적합성, 기준선·성과측정 |
| 제외 | 특정 AI 제품 사용법, 상세 소프트웨어 구현, 조직 전체 변화관리, 상세 교재 |
| 조사 에이전트 | `ax-domain-researcher` |
| 독립 감사 | evidence 100%, taxonomy 100%, practicality 100% |
| 출력 경로 | `research/capability-survey/waves/wave-01/wp.ax-strategy-value.pilot/` |

기술스택 목록으로 편향되지 않는지 가장 먼저 검증하기 위해 비즈니스·업무설계
영역을 시험 배치로 제안합니다.

## 6. 승인 및 실행 상태

- [x] 사용자가 조사 렌즈와 첫 시험 배치 진행을 승인했습니다.
- [x] 승인된 작업 패키지 manifest를 작성했습니다.
- [x] 읽기 전용 병렬 후보 조사를 시작했습니다.
- [x] 정규 카탈로그와 Trend Signal을 수정하지 않았습니다.
- [x] 프로젝트 기본 Claude agent를 변경하지 않았습니다.
- [x] Claude CLI 사전 Gate 실패 후 실행 중 세션이 없음을 확인하고 Codex
      서브에이전트 백업 경로로 전환했습니다.

## 7. 검증

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

2026-07-26 실행 결과:

```text
Catalog: units=2, resources=4, sets=1, signals=3, candidates=0
Catalog errors=0, warnings=0
Regression tests=17/17 passed
JSON Schemas=5 valid
JSON Templates=5 valid
Claude project agents=4 frontmatter valid, read-only tool allowlist 확인
Claude Code doctor=2.1.220, installation issues 없음
Markdown links=정상
Absolute local path scan=위반 없음
```

실제 Candidate가 0개인 것은 Wave 1 조사를 아직 시작하지 않았기 때문입니다.

## 8. 다음 한 단계

세 읽기 전용 조사 결과를 통합하여 후보 10개 이하의 Candidate 초안을 만들고
evidence·taxonomy·practicality 독립 감사를 수행합니다.

## 9. 사용자 판단 필요

현재 추가 판단 요청은 없습니다. 범위 변경, P0 근거 오류, 정규 승격 필요 또는
자동 중단조건이 발생하면 즉시 중단하고 보고합니다.
