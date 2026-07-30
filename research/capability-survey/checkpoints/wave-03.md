# Phase 2 Capability Survey — Wave 3 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `active` |
| 시작일·마지막 갱신일 | `2026-07-29` · `2026-07-30` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.7.0` (`provisional`) |
| 동시 작업 패키지 | `1` |
| 작업 패키지별 후보 상한 | `10` |

## 2. 범위

Wave 3은 사람·운영·통제 중심 Breadth 조사 B입니다. 순서는 다음과 같습니다.

1. `human-ai-experience`
2. `platform-quality-operations`
3. `security-legal-governance`
4. `organization-adoption`

Wave 2 후보에 누락된 접근성·인간통제·운영·보안·법무·조직 도입 품질축을
함께 표시하되 각 전문 렌즈의 소유권을 유지합니다.

## 3. 작업 패키지

| 패키지 | 상태 | 후보 | 경로 | 판정 |
|---|---|---:|---|---|
| `wp.human-ai-experience.breadth-a` | promoted | 9/10 | `research/capability-survey/waves/wave-03/wp.human-ai-experience.breadth-a/` | 승격 전·후 재검수 P0·P1 0건, 6 Unit·2 Resource cataloged·1 deferred |

## 4. 현재 결과

`human-ai-experience` 아래 잠정 subdomain 8개를 추가했습니다.

- `ai-capability-mental-model-onboarding`
- `human-centered-ai-explanations`
- `ai-feedback-user-control`
- `human-approval-escalation-interaction`
- `conversational-ai-repair`
- `accessible-multimodal-ai-interaction`
- `personalization-memory-user-control`
- `human-ai-experience-evaluation`

후보 결과는 mental model·온보딩, 사용자 중심 설명, 피드백·통제,
승인·이관, 대화 복구와 경험 평가의 accepted Unit 후보 6개, 접근 가능한
다중양식 요구와 사회적 단서·의인화 경계의 accepted D0 Resource 후보 2개,
개인화·기억 통제의 deferred 후보 1개입니다. 접근성 구현, 시스템 memory,
AI 결과 검증, workflow와 보안·법무 통제를 복제하지 않도록 경계를 고정했습니다.
사용자의 연속 진행 승인에 따라 accepted Unit 후보 6개는 공개 Reference와 함께
정규 `cataloged` Unit으로 승격했습니다. 접근 가능한 다중양식 D0 Resource는
`unit.software.accessible-ui-state-interaction@1.0.0`이, 사회적 단서·의인화
D0 Resource는 신규 기대형성·온보딩 Unit이 소유합니다. 승격 전 문자 손상
16개 필드를 교정했고, 정규 메타데이터 생성 후 후보 추적·출처·관계·평가
Gate를 다시 독립 검수했습니다. 개인화·기억 후보는 승격하지 않았습니다.

## 5. 다음 한 단계

Human-AI 경험 패키지의 조사·감사·정규 승격과 승격 후 검수를 완료했습니다.
다음 순차 패키지는 `platform-quality-operations`입니다. 동일하게 발견 조사,
독립 근거·taxonomy·실용성 감사, 본 세션 재검수, 정규 승격과 승격 후 검수를
순차 수행합니다.
