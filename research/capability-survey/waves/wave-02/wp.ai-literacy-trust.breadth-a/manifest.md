# Work Package Manifest: wp.ai-literacy-trust.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| 상태 | `promoted` |
| 범위 승인일 | `2026-07-27` |
| 결과 승인일 | `2026-07-28` |
| 범위 승인 근거 | 사용자가 후보 최대 10개, 동시 작업 패키지 1개 실행을 승인함 |
| 결과 승인 근거 | 사용자가 후보·잠정 분류·역할별 깊이를 모두 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.3.0` |
| 최대 후보 | `10` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, node ID·영문 병기 허용 |

## 조사 계약

### 포함

- 전사 구성원이 AI 시스템의 용도·한계와 출력의 불확실성을 설명하는 능력
- AI 출력의 주장·근거·출처를 확인하고 업무 위험에 맞는 검증 강도를 선택하는 능력
- 자동화 편향과 과신·과소신뢰를 피하고 인간 판단·승인·에스컬레이션을 적용하는 능력
- 편향·공정성·접근성·인권 영향을 식별하고 책임 있는 사용 경계를 적용하는 능력
- AI 생성물과 상호작용 사실, 한계와 불확실성을 이해관계자에게 투명하게 전달하는 능력
- 개인정보·기밀정보·저작권·출처·콘텐츠 진위를 AI 사용 판단에 반영하는 공통 리터러시
- 오류·유해 결과와 새로운 위험을 기록·보고하고 사용을 중단하거나 교정하는 능력

### 제외

- 모델 학습·추론·RAG·에이전트·평가 하네스의 상세 구현
- 특정 AI 제품이나 공급자의 사용법
- 조직 전체 AI 거버넌스 시스템과 법률 준수 체계의 상세 설계
- 보안 위협 모델링·접근통제·개인정보 엔지니어링의 전문 구현
- 상세 교재·실습·HUB 구축
- Candidate의 정규 Unit·Set·Resource·Trend Signal 승격

### 관점

- 일반 임직원과 현업 사용자
- 경영·의사결정자와 업무 승인자
- 제품·서비스·고객지원 담당자
- 데이터·개발·AI 시스템 제공자
- 위험·법무·개인정보·감사 담당자
- 교육·인사·조달·운영 담당자

## 예상 분류 범위

현재 Registry의 `ai-literacy-trust` 조사 렌즈를 대분류 참조로 사용합니다.
후보 정본 작성에 필요한 잠정 하위 node는 조사 결과에서 정의·포함·제외·부모
경계를 비교한 뒤 Wave 2 Checkpoint에 추가·병합·보류 제안으로 기록합니다.
새 대분류, 기존 ID 개명·병합·폐기는 적용하지 않습니다.

## 실행 구조

1. 읽기 전용 분야 조사자가 공식·표준·1차 출처를 중심으로 후보와 근거 씨앗을 조사합니다.
2. Codex 메인 세션이 중복을 제거하고 후보를 최대 10개로 제한합니다.
3. 누락 주제·반대 관점과 인접 렌즈 경계를 별도 패스로 검토합니다.
4. Codex 메인 세션만 잠정 하위 node 제안과 Candidate 정본을 기록합니다.
5. 발견자와 분리된 읽기 전용 감사자가 근거, taxonomy, 실무성을 독립 감사합니다.
6. Codex 메인 세션이 P0·P1을 반영하고 자동검증과 Checkpoint를 갱신합니다.

## 파일 소유권

Codex 메인 세션만 다음 경로에 씁니다.

```text
research/capability-survey/waves/wave-02/wp.ai-literacy-trust.breadth-a/
  manifest.md
  domain-survey.md
  assessment-contract.md
  candidates/<candidate-id>/candidate.json
  audit/evidence-review.md
  audit/taxonomy-review.md
  audit/practicality-review.md
```

Wave 공용 상태는 Codex 메인 세션만
`research/capability-survey/checkpoints/wave-02.md`에 기록합니다.
서브에이전트는 파일을 수정하지 않고 조사·감사 결과만 반환합니다.

## 품질 Gate

- 후보 수는 10개 이하입니다.
- 모든 후보에 문제·포함·제외 범위와 관찰 가능한 행동이 있습니다.
- 모든 후보에 둘 이상의 업무 또는 역할 전이 맥락이 있습니다.
- 정의와 범위를 지지하는 표준·공식·1차 또는 원 실무자 근거가 있습니다.
- 최신 법적·표준 상태는 2026-07-27 기준 공식 출처에서 확인합니다.
- 정의·위험과 비즈니스 효과 가설을 분리합니다.
- 기존 Candidate·Unit·Set·Signal 및 인접 렌즈와 목적지 경계를 검토합니다.
- evidence, taxonomy, practicality 감사를 신규 후보 100%에 수행합니다.
- 마지막 누락 레드팀 패스의 새 고우선 후보가 0개이거나 명시적 미완료로 남깁니다.
- P0는 0건이어야 하며 P1은 반영 또는 명시적으로 보류합니다.
- 카탈로그 검증과 전체 회귀 테스트가 통과해야 합니다.

## 자동 중단조건

- 필수 근거가 없거나 원문과 핵심 주장이 다릅니다.
- 승인된 포함·제외 범위를 벗어납니다.
- 후보 중복 비율이 15%를 초과합니다.
- 기존 사용자 파일과 충돌하거나 할당 밖 파일 수정이 필요합니다.
- 스키마·참조·DAG 검증 또는 회귀 테스트가 실패합니다.
- 사용자 업무에 대한 확인되지 않은 가정을 전사 범위로 일반화합니다.
- 새 대분류, 기존 분류 ID 변경 또는 정규 카탈로그 승격이 필요합니다.

## 완료 요약

- 후보 10개: 신규 Unit 후보 8개, 기존 Unit 병합 1개, Resource 전용 1개
- evidence 22건, 고유 URL 13개
- 신규 잠정 subdomain 7개
- 독립 근거·taxonomy·실용성 감사 완료, 수정 후 재확인 P0·P1 0건
- 정규 Unit·Set·Resource·Signal 변경 없음
- 공개 경계·카탈로그·단위 테스트·diff 검증 통과
- 사용자 결과 승인 완료

## 후속 정규 승격

사용자가 `2026-07-28`에 Codex의 전문 판정에 따른 정규 승격을 지시했습니다.
그 결과 신규 Unit 후보 8개를 `cataloged` Unit과 공개 Reference Resource로
승격하고, Resource 전용 후보는
`resource.foundation.evidence-verification.content-provenance-reference@1.0.0`로
등록했습니다. 병합 후보는 기존
`unit.foundation.evidence-verification@1.0.0`을 그대로 사용합니다.

`cataloged`는 정규 메타데이터 등록을 뜻하며 상세 교재·독립 평가의 타당성이나
학습효과가 검증되었다는 뜻이 아닙니다. Candidate는 삭제하지 않고 발견·감사·승격
이력으로 보존합니다.
