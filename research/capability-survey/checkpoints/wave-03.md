# Phase 2 Capability Survey — Wave 3 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `active` |
| 시작일·마지막 갱신일 | `2026-07-29` · `2026-07-30` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.9.0` (`provisional`) |
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
| `wp.platform-quality-operations.breadth-a` | promoted | 10/10 | `research/capability-survey/waves/wave-03/wp.platform-quality-operations.breadth-a/` | 승격 전·후 독립 3중 재감사 P0·P1 0건, 9 Unit·9 Reference·1 Set cataloged |
| `wp.security-legal-governance.breadth-a` | promoted | 10/10 | `research/capability-survey/waves/wave-03/wp.security-legal-governance.breadth-a/` | 승격 전·후 독립 3중 재감사 P0·P1 0건, 9 Unit·9 Reference·1 Set cataloged |

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

플랫폼 품질·운영은 안전한 릴리스, 선언형 환경, 서비스 telemetry, SLI·SLO,
사고대응, 백업·복원, 성능·용량, 기술비용, 복원력의 Unit 후보 9개와 서비스
운영준비·수명주기 Set 후보 1개를 작성했습니다. 내부 플랫폼 독립 Unit은 실제
내부 사용자와 조직 operating model 근거가 필요해 유보했으며 alert·on-call과
toil은 관련 후보의 하위 성과로 흡수했습니다. 마지막 누락 점검의 새 고우선
독립 후보는 0개입니다.

보안·법무·거버넌스는 보안 요구·위협 모델, identity·접근정책, 비밀·암호키,
소프트웨어 공급망, 개인정보 영향·권리, 보안사고 증거·보고 이관, 통제감사,
디지털 자산 권리 provenance, AI 보안위협의 Unit 후보 9개와 AI 위험·영향
거버넌스 보증 Set 후보 1개를 작성했습니다. 모든 실습은 합성 fixture와
loopback sandbox로 제한하며 실제 법률·규제·위험수용 판단은 qualified owner에게
이관합니다. 마지막 발견 누락 점검의 새 고우선 독립 후보는 0개입니다.
승격 전 근거·taxonomy·실용성 감사와 승격 후 정규 산출물 재감사에서 P0·P1
0건을 확인해 9개 Unit·9개 Reference·1개 Set을 `cataloged`로 등록했습니다.
상세 fixture·runner 구현과 실제 조직·관할·제품 적합성·학습효과는 검증하지
않았으며 활성화 전 후속 Gate입니다.

## 5. 다음 한 단계

보안·법무·거버넌스 정규 승격과 승격 후 재검수를 완료했습니다. 다음 순차
패키지 `organization-adoption`의 Manifest·평가계약을 고정하고 발견 조사·후보
작성·독립 감사·정규 승격을 같은 절차로 진행합니다.
