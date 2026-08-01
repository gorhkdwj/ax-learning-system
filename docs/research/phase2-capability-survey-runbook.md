# Phase 2 전사 AX 역량지도 전수조사 Runbook

## 1. 목적

Phase 2의 목적은 특정 직무나 제품 목록이 아니라 전사 AX를 수행하고 검증하는 데
필요한 역량 범위를 얕고 넓게 조사하는 것입니다. 결과는 상세 교재나 현재 학습
배정이 아니라 다음 산출물입니다.

- 잠정 대분류·중분류와 조사 공백
- 구조화된 후보 역량 `candidate.json`
- 후보별 정의·포함·제외 범위
- 실무 전이성, 목표 숙련도와 깊이 상한 가설
- 공식·1차 근거와 해당 근거가 지지하는 범위
- Unit·Set·Resource·Adapter·Trend Signal·보류·제외 라우팅 제안
- 중복·경계·품질축·직무 편향 검토 결과

“전수”는 세상에 존재하는 모든 기술을 수집한다는 뜻이 아닙니다. 합의된 전사
업무와 품질축의 조사범위에서 누락·중복·근거와 불확실성을 검증 가능한 방식으로
관리할 수 있게 된 상태를 뜻합니다.

## 2. 비목표와 금지사항

Phase 2에서는 다음 작업을 수행하지 않습니다.

- 상세 챕터·실습·평가자료 대량 제작
- 사용자 현재 학습경로와 우선순위 확정
- 후보를 정규 Unit·Set으로 자동 승격
- Trend Signal을 검증 없이 Unit으로 승격
- HUB 화면이나 검색 인덱스 구축
- 사용자 승인 없는 스키마·거버넌스·기존 ID 변경
- 출처가 없는 생산성·비용절감·업계 표준 주장
- 후보 수나 토큰 사용량만을 근거로 한 완료 선언

조사 결과는 `research/capability-survey/`에만 저장합니다. `catalog/`, `sets/`,
`research/signals/`, `schemas/`와 거버넌스 문서는 별도 승인 전 수정하지 않습니다.

## 3. Claude 운영 구조

### 3.1 총괄

일반 Claude 메인 세션이 조사 총괄과 유일한 파일 작성자를 맡습니다. 프로젝트
기본 agent는 변경하지 않습니다. Phase 2 전용 custom agent를 기본값으로 설정하면
일반 작업까지 조사 프롬프트가 적용될 수 있기 때문입니다.

메인 세션은 다음을 수행합니다.

- 작업 패키지 범위·최대 후보 수·출력 경로 배정
- 읽기 전용 조사 서브에이전트 실행
- 서브에이전트 결과를 후보 템플릿에 맞춰 파일로 기록
- 독립 출처·분류·실무성 감사 요청
- Checkpoint와 검증 결과 갱신
- 사용자 승인 전 쓰기 중단

### 3.2 프로젝트 서브에이전트

| Agent | 역할 | 쓰기 권한 |
|---|---|---|
| `ax-domain-researcher` | 할당된 분야의 후보와 근거 씨앗 조사 | 없음 |
| `ax-evidence-auditor` | 원문을 다시 열어 claim 범위와 출처 품질 감사 | 없음 |
| `ax-taxonomy-auditor` | 중복·명명·분류·경계·누락·직무 편향 감사 | 없음 |
| `ax-practicality-auditor` | 업무 전이성·비즈니스 가설·깊이·운영성 감사 | 없음 |

모든 연구자와 감사자는 결과를 메인 세션에 반환합니다. 메인 세션만 할당된
`research/capability-survey/` 경로에 씁니다. 한 에이전트가 발견·감사·승인까지
모두 수행하지 않습니다.

Claude Code 2.1.220에서 프로젝트 전용 서브에이전트는 `.claude/agents/`에서
발견됩니다. 새 `agents` 디렉터리를 실행 중인 세션에서 처음 만들었다면 Claude를
다시 시작한 뒤 `/agents`로 로드 여부를 확인합니다. 공식 동작은 변경될 수 있으므로
실행 전 [Claude Code subagents 문서](https://code.claude.com/docs/en/sub-agents)와
[configuration 진단](https://code.claude.com/docs/en/debug-your-config)을 확인합니다.

### 3.3 병렬화 원칙

- 서로 독립적인 작업 패키지만 병렬 실행합니다.
- 한 작업 패키지는 후보 25개를 넘지 않습니다.
- 최초 시험 배치는 후보 10개 이하로 제한합니다.
- 감사는 연구 결과가 준비된 뒤 순차 실행합니다.
- 서브에이전트가 공용 집계 파일이나 정규 카탈로그를 수정하지 않습니다.
- 현재 작업공간은 Git 저장소가 아니므로 worktree 격리를 전제로 하지 않습니다.
- 여러 쓰기 세션을 동시에 실행하지 않습니다.
- 토큰이 남았다는 이유로 승인된 manifest 밖의 조사를 추가하지 않습니다.

Claude 공식 문서도 독립 연구에는 서브에이전트를, 작업이 여러 패스로 커지면
파일·스크립트에 계획을 고정하는 방식을 구분합니다. 이 프로젝트에서는 초기에는
메인 세션과 읽기 전용 서브에이전트를 사용하고, 후보 수와 반복성이 실제로 커진
뒤에만 dynamic workflow 도입을 검토합니다.

## 4. 정본과 산출물 계약

### 4.1 작업 전 읽기 순서

1. `AGENTS.md`
2. `docs/governance/learning-governance.md`
3. `docs/architecture/learning-system.md`
4. `docs/research/trend-signal-governance.md`
5. `docs/plans/curriculum-foundation-plan.md`
6. 본 Runbook
7. `taxonomy/README.md`와 `taxonomy/taxonomy.json`
8. 현재 Wave Checkpoint

### 4.2 파일 구조

```text
research/
  capability-survey/
    README.md
    checkpoints/
      wave-00.md
    waves/
      <wave-id>/
        <work-package-id>/
          domain-survey.md
          candidates/
            <candidate-id>/
              candidate.json
          audit/
            evidence-review.md
            taxonomy-review.md
            practicality-review.md
```

빈 Wave 폴더는 미리 대량 생성하지 않습니다. 실제 작업 패키지가 승인될 때
필요한 경로만 만듭니다.

### 4.3 후보 메타데이터

- 스키마: `schemas/capability-candidate.schema.json`
- 템플릿: `templates/research/capability-candidate.template.json`
- 파일명: `candidate.json`
- ID: `candidate.<영역>.<이름>`
- 버전: SemVer
- 분류 정본: `taxonomy/taxonomy.json`
- 분류 스키마: `schemas/capability-taxonomy.schema.json`

Candidate는 정규 카탈로그 항목이 아닙니다. `proposed_unit_id`나
`proposed_set_id`는 통합을 위한 제안이며 실제 ID 확보나 승격을 뜻하지 않습니다.
정규 승격 시 기존 Unit·Set·Resource 또는 Trend Signal 스키마로 새 레코드를
작성하고 사용자 승인을 받습니다.

후보 하나에는 확인된 정의와 범위, 관찰 가능한 행동, 업무 전이 맥락, 목표 수준,
깊이 상한, 비즈니스 가설, 품질축, 근거와 임시 판정을 기록합니다. 일반 Breadth
후보는 근거 1~3개와 미해결 질문 최대 3개를 권장합니다. 장문의 본문은 후보
메타데이터에 넣지 않습니다.

후보 ID의 영역 부분은 최초 발견 렌즈를 보존하며 정규 소유 분야는
`taxonomy.major_domain`으로 기록합니다. `discovery.lens_id`와 `basis`에는
할당 렌즈, 교차 렌즈 발견, 사용자 요청, 기존 카탈로그 검토 또는 Trend Signal
등 실제 발견 경로를 기록합니다. 후보 간 선행·연관 관계는 최상위 `relations`에
대상 Candidate의 정확한 ID와 버전을 사용합니다. 임의 `extensions` 문자열로
관계를 이중 기록하지 않습니다.
`discovery.lens_id`, `taxonomy.major_domain`, `taxonomy.subdomains`는 Registry의
활성 node와 계층에 맞아야 합니다. 기존 node로 표현할 수 없는 후보는 임의 문자열을
먼저 기록하지 않고 정의·포함·제외·부모 후보와 분리 비용을 Checkpoint에 제안합니다.

### 4.4 사람용 보고서

- 분야 템플릿: `templates/research/domain-survey.template.md`
- Wave 템플릿: `templates/research/wave-checkpoint.template.md`

분야 보고서는 후보 목록과 공백을 요약하며 후보 전문을 복제하지 않습니다.
Checkpoint는 새 세션이 대화 기록 없이 작업을 재개할 수 있는 Handoff Packet입니다.

## 5. 잠정 조사 렌즈

다음은 고정 taxonomy가 아니라 누락 방지를 위한 조사 렌즈입니다. Wave 0 보정과
사용자 승인 없이 정규 대분류로 확정하지 않습니다.

이 렌즈들은 Wave 0~4 동안 `research_lens` 상태로 조사되었고, Wave 5에서
Coverage·중복·목적지 검토를 통과한 10개 안정 ID를 canonical domain으로
전환했습니다. 최초 발견 렌즈는 Candidate의 `discovery.lens_id`와 provenance에
보존합니다. 근거가 부족한 하위 node 3개는 `provisional`이며, 프론트엔드·
백엔드·데이터 엔지니어링은 현재 `planned` 역할 보기로 유지합니다.

| 렌즈 ID | 범위 |
|---|---|
| `ax-strategy-value` | AX 전략, 가치발견, 업무·프로세스·제품 재설계, 성과측정 |
| `ai-literacy-trust` | AI 리터러시, 결과 검증, 책임 있는 사용, 인간 판단 |
| `ai-systems-agents` | LLM, 검색·RAG, 에이전트, 평가, 컨텍스트·도구·메모리 |
| `software-product-engineering` | 프론트엔드, 백엔드, API, DB, 테스트, 설계와 바이브 코딩 |
| `data-analytics-ml` | 데이터 수집·모델링·분석·품질·거버넌스·ML |
| `integration-automation` | API, MCP, SaaS, 결정적 자동화, 워크플로우 오케스트레이션 |
| `human-ai-experience` | UI·UX, Human-AI Interaction, 접근성, 설명과 승인 경험 |
| `platform-quality-operations` | 배포, 관측성, 신뢰성, 비용, 장애·복구, 유지보수 |
| `security-legal-governance` | 보안, 개인정보, 권한, 감사, 법무, 저작권, 윤리 |
| `organization-adoption` | 조직변화, 역할·협업, 교육 운영, 도입·성과 확산 |

보안·검증·접근성·비용·운영·조직 도입은 독립 렌즈인 동시에 모든 분야를
가로지르는 품질축입니다.

## 6. Wave 계획

### Wave 0 — 조사 계약과 보정

목표:

- 조사 렌즈의 포함·제외 범위와 책임 경계를 보정합니다.
- 후보 스키마, 관계어, 라우팅과 출처 우선순위를 확정합니다.
- 동일한 경계 사례에 대한 판정 편차를 확인합니다.

완료조건:

- 모든 렌즈에 포함·제외 범위와 담당 관점이 있습니다.
- 공통 경계 사례의 라우팅 판정 일치율이 85% 이상입니다.
- 후보 스키마·템플릿과 단일 검증 명령이 통과합니다.
- 첫 시험 배치 범위와 최대 후보 수를 사용자가 승인합니다.

### Wave 1 — 첫 시험 배치

권장 시험 영역은 `ax-strategy-value`이며 후보 10개 이하로 제한합니다. 기술
스택 목록으로 편향되지 않는지 먼저 검증하기 위한 선택입니다.

완료조건:

- 모든 후보에 정의·포함·제외·행동·근거·라우팅 사유가 있습니다.
- 현재 사용자 업무를 전사 필요로 일반화하지 않았습니다.
- 공식·1차 출처가 실제 claim 범위를 지지합니다.
- 검색군, 출처 계층, 역할 관점과 누락 레드팀 패스를 기록합니다.
- 마지막 누락 레드팀 패스가 새 고우선 후보 0개이거나 미완료 사유가 있습니다.
- 독립 감사와 자동검증이 통과합니다. 독립 감사를 받지 않은 신규 후보가 있으면
  작업 패키지를 `ready_for_review`로 표시하지 않습니다.
- 사용자가 확장 여부를 승인합니다.

### Wave 2 — Breadth 조사 A

다음 기술·데이터 중심 렌즈를 작업 패키지별 최대 25개 후보로 조사합니다.

- `ai-literacy-trust`
- `ai-systems-agents`
- `software-product-engineering`
- `data-analytics-ml`
- `integration-automation`

상세 교재와 승격은 금지합니다.
각 작업 패키지는 시작 전에 기존 Registry node로 예상 범위를 표현하고, 조사 중
새 node가 필요하면 동일 Wave Checkpoint에 추가·병합·보류 제안을 기록합니다.
새 대분류, 기존 ID 개명·병합·폐기는 사용자 승인 전에는 적용하지 않습니다.

### Wave 3 — Breadth 조사 B

다음 사람·운영·통제 중심 렌즈를 조사합니다.

- `human-ai-experience`
- `platform-quality-operations`
- `security-legal-governance`
- `organization-adoption`

Wave 2 후보에 누락된 횡단 품질축도 함께 표시합니다.

### Wave 4 — 교차 품질축과 Coverage

- 대분류 × 역할 관점 × 품질축 Coverage Matrix를 작성합니다.
- 각 칸을 `조사됨`, `근거 있는 공백`, `미완료`로 구분합니다.
- 후보 수를 강제로 균등하게 만들지 않지만 편중 사유를 보고합니다.
- 개발자 기술스택 목록으로 축소되었는지 레드팀 검토합니다.

### Wave 5 — 정규화와 중복 통합

- 같은 이름·다른 학습성과는 범위를 나누어 유지합니다.
- 다른 이름·같은 학습성과는 canonical 후보 하나와 alias로 병합합니다.
- 공급자 구현 차이는 안정 코어 아래 Adapter 또는 Resource로 라우팅합니다.
- 여러 Unit의 조합에서만 가치가 생기면 Set 후보로 라우팅합니다.
- 중복은 연쇄시키지 않고 최종 canonical 대상을 직접 참조합니다.
- 신흥·중의적 용어는 Trend Signal로 보냅니다.

### Wave 6 — 독립 QA와 제한 Deep Research

일반 후보는 대분류별 `max(3건, 후보의 15%)`를 층화 표본으로 독립 재검토합니다.
다음 후보는 100% 검토합니다.

- 보안·개인정보·권한·법무 위험이 높은 후보
- D3·D4 후보
- 승격 검토 대상 Trend Signal
- 공식 근거가 충돌한 후보
- 논쟁적인 병합·제외 판정
- 여러 대분류의 핵심 선수역량

Deep Research는 다음 트리거가 있는 후보에만 수행합니다.

- 고위험 의무 또는 운영 책임
- 높은 업무효과·비용절감 주장
- 공급자·버전에 따른 빠른 변화
- 어려운 중복·분류 판정
- 가까운 파일럿 Set 편입
- D3·D4 학습성과 필요

### Wave 7 — 역량지도 조립과 완료 감사

- 승인된 canonical 후보를 지도에 배치합니다.
- 관계 DAG, 공백, 중복·제외·보류와 불확실성을 표시합니다.
- 상세 교재로 넘어갈 후보와 메타데이터만 유지할 후보를 구분합니다.
- Phase 2 완료 보고서를 제출하고 사용자 승인을 받습니다.

## 7. 영역별 실행 Loop

1. **Manifest 고정**: Wave, 작업 패키지, 포함·제외, 역할 관점, 검색군, 출력 경로,
   최대 후보 수와 중단조건을 Checkpoint에 기록합니다.
2. **후보 발견**: `ax-domain-researcher`가 읽기 전용으로 조사합니다.
3. **누락 레드팀**: 역할 반전, 인접 분야와 제외 경계를 조사하여 새 고우선
   후보가 더 나오는지 확인합니다.
4. **Registry 대조**: 기존 node·별칭·경계를 대조하고 새 node 제안과 역할 보기를 분리합니다.
5. **정본 기록**: 메인 세션이 후보별 `candidate.json`과 분야 요약을 작성합니다.
6. **출처 감사**: `ax-evidence-auditor`가 원문을 독립적으로 다시 확인합니다.
7. **분류 감사**: `ax-taxonomy-auditor`가 중복·경계·편향을 검토합니다.
8. **실무성 감사**: `ax-practicality-auditor`가 가치·전이성·깊이와 운영성을 검토합니다.
9. **수정·검증**: 메인 세션이 감사 결과를 반영하고 자동검증합니다.
10. **Checkpoint**: 결정, 커버리지 근거, 공백, 검증 결과와 다음 한 단계를 기록합니다.
11. **승인**: 사용자 승인 대상이면 추가 쓰기를 멈추고 diff preview를 제출합니다.

## 8. 출처와 정확성 규칙

- 표준·공식 사양, 공식 문서·소스, 1차 연구, 원 실무자 사례를 우선합니다.
- 기술 질문의 사실 근거는 가능한 한 공식·1차 출처를 사용합니다.
- 커뮤니티·검색량·SNS는 발견 신호로만 사용합니다.
- 검색결과 요약, AI 재서술, 출처가 확인되지 않은 인용은 evidence가 아닙니다.
- URL, 발행자, 출처 유형, 확인일과 지지하는 claim 범위를 기록합니다.
- 공급자 사례는 해당 조건의 사례로만 기록하며 보편적 효과로 일반화하지 않습니다.
- 공공부문 또는 단일 공급자 자료에만 의존하는 후보는 적용 범위를 그 맥락으로
  제한하거나, 산업 중립 표준·1차 연구·독립 실무자 자료로 전이 가능성을 보강합니다.
- 정의 신뢰도와 효과·비즈니스 가설의 신뢰도를 혼합하지 않습니다.
- 외부 URL 실시간 접근 검증은 조사 시 수행하되 구조검증기가 대신한다고 표현하지 않습니다.

## 9. 판정 기준

| 판정 | 사용 조건 |
|---|---|
| `capability_map_only` | 전사 범위 이해에는 필요하지만 독립 학습 Unit이 필요하지 않습니다. |
| `merge_existing` | 기존 항목과 문제·학습성과·검증 방식이 실질적으로 같습니다. |
| `resource_only` | 독립 역량보다 기존 Unit의 설명·사례로 적합합니다. |
| `technology_adapter` | 공급자 독립 코어와 분리해야 하는 제품·버전 사용법입니다. |
| `unit_candidate` | 둘 이상의 맥락으로 전이되는 독립 학습성과와 검증 가능성이 있습니다. |
| `set_candidate` | 여러 Unit의 조합·업무 Pipeline에서만 가치가 발생합니다. |
| `trend_signal` | 중요할 가능성은 있지만 정의·효과·안정성이 충분하지 않습니다. |
| `defer` | 관련성은 있으나 근거·우선순위·학습 가능성이 부족합니다. |
| `exclude` | 전사 전이성이 없거나 마케팅성 재명명·폐기 기술·교육 불가능 대상입니다. |

`unit_candidate`의 D2에는 새로운 입력의 전이과제와 자동·객관적 검증 가능성이
필요합니다. D3에는 권한, 보안, 비용, 관측성, 장애·복구와 롤백이 필요합니다.
D4는 실제 업무 필요가 입증되기 전에는 기본적으로 제외합니다.

## 10. 사용자 승인 지점

다음 상황에서는 작업을 멈추고 현재 Checkpoint와 변경 예정 파일을 제시합니다.

1. 최초 렌즈·순서·시험 배치 확정
2. 첫 시험 배치 결과와 전체 확장 결정
3. 새 대분류 또는 분류원칙 추가, 기존 분류 ID의 개명·병합·폐기
4. 스키마·거버넌스 변경
5. 기존 ID 병합·변경·폐기
6. 한 번에 25개를 넘는 파일 생성·수정
7. 사용자 실제 업무나 우선순위를 전제해야 하는 판단
8. Candidate 또는 Signal을 정규 Unit·Set·Resource로 승격
9. 고위험·법적·보안 통제의 제외 또는 후순위화
10. Phase 2 완료 선언

## 11. 자동 중단조건

- 스키마·참조·DAG 검증 실패
- 할당되지 않은 경로 수정
- 기존 사용자 변경과 충돌
- 필수 근거 없이 확정 상태로 등록
- 독립 감사에서 허위·접근 불가 출처 또는 중대한 claim 오류 발견
- 동일 작업 패키지의 중복 후보 비율이 15% 초과
- 승인된 manifest 밖으로 범위 확장
- 미확인 효과를 확인된 정의와 혼합
- 사용자 업무에 대한 확인되지 않은 가정 사용
- 삭제·이동·기존 ID 변경 필요
- Checkpoint만으로 현재 상태를 복원할 수 없음

중단 시 기존 변경을 자동 롤백하지 않습니다. 추가 쓰기를 멈추고 영향범위와
복구 선택지를 보고합니다.

## 12. 완료 Gate

- 승인된 모든 조사 렌즈와 중분류가 Coverage Matrix에 있습니다.
- 모든 Candidate·Unit 분류 참조가 단일 활성 Taxonomy Registry에 존재하고
  하위 node의 부모 계층이 정합합니다.
- 모든 칸이 `조사됨`, `근거 있는 공백` 또는 명시적 미완료로 구분됩니다.
- 각 작업 패키지에 검색군, 출처 계층, 역할 관점과 반복 탐색 패스가 기록됩니다.
- 마지막 누락 주제·반대 관점 패스가 새 고우선 후보 0개이며, 남은 공백은 다른
  렌즈·Deep Research·제외 중 하나로 라우팅됩니다.
- 각 후보에 범위, 행동, 근거, 임시 판정과 이유가 있습니다.
- `accepted` 후보는 중간 이상 신뢰도와 공식·1차 또는 원 실무자 근거가 있습니다.
- 모든 신흥·중의적 개념은 Trend Signal로 분리되었습니다.
- 중복·상하위·대안·Adapter 경계가 검토되었습니다.
- 특정 직무와 기술스택 편향 감사를 통과했습니다.
- 고위험·D3·D4·논쟁 후보를 100% 검토했습니다.
- 일반 후보 층화표본 QA에서 중대한 오류가 없습니다.
- 독립 감사를 받지 않은 신규·중대 수정 후보가 `accepted` 또는 작업 패키지
  `ready_for_review` 상태로 표시되지 않았습니다.
- 스키마·ID·참조·DAG 검증이 통과합니다.
- 변경 파일, 잔여 불확실성과 후속 Deep Research 목록이 있습니다.
- `handoff.json`과 `handoff.md`가 실제 산출물·검증 결과·다음 행동을 복원할 수
  있는 상태로 작성되었습니다.
- 사용자가 Phase 2 완료를 승인했습니다.

## 13. 시작·검증 명령

Claude Code 2.1.220이 현재 설치되어 있음을 확인했습니다. 새 세션에서 다음을
확인합니다.

```powershell
claude --version
claude
```

Claude 세션 안에서 다음을 확인합니다.

```text
/memory
/agents
/doctor
```

Claude에게 전달할 전체 시작 프롬프트와 첫 응답 승인 기준은
`docs/research/claude-phase2-onboarding.md`를 사용합니다. 짧은 대화 지시보다
해당 문서의 온보딩 계약을 우선합니다.

Claude 측 작업 범위가 끝나면
`research/capability-survey/handoffs/README.md`의 형식으로
`handoff.json`과 `handoff.md`를 작성합니다. 배정 범위만 끝난 상태를
`phase_complete`로 표시하지 않고 `ready_for_review`로 인계합니다.

저장소 검증:

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```
