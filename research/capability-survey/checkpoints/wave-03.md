# Phase 2 Capability Survey — Wave 3 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `ready_for_wave-04-planning` |
| 시작일·마지막 갱신일 | `2026-07-29` · `2026-07-30` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.10.0` (`provisional`) |
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
| `wp.organization-adoption.breadth-a` | promoted | 10/10 | `research/capability-survey/waves/wave-03/wp.organization-adoption.breadth-a/` | 승격 전·후 독립 3중 재감사 완료, 9 Unit·9 Reference·1 Set cataloged |

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

조직·도입은 변화 영향·준비도·참여, 운영모델·의사결정권, workforce
capability gap·전환, 학습·업무전이, 포용적 직무영향·지원, adoption
support·community·지식흐름, aggregate 도입성과·분배효과 monitoring,
pilot·scale·stop·rollback, vendor·SaaS 전문검토 이관의 Unit 후보 9개와
이를 조합하는 lifecycle Set 후보 1개를 작성했습니다. 실제 개인·성과·감정
데이터와 고용·노무·법률·조달 결론은 제외하고 qualified owner에게
이관합니다. 승격 전 독립 감사의 모든 P0·P1·P2를 교정해 9개 Unit·9개
Reference와 필수 8개·조건부 5개인 13단계 Set으로 `cataloged` 등록했습니다.
상세 fixture·runner, 실제 조직 tailoring과 도입·학습효과는
`required_before_activation` 후속 Gate입니다.

## 5. 다음 한 단계

Wave 3의 네 작업 패키지 생성·정규 승격·승격 후 재검수와 Wave 4 착수 전
추적 문서 정합화를 완료했습니다. 다음 단계는 Wave 4 조사 렌즈·범위·패키지
순서·후보 상한을 계획하고 사용자 승인을 받는 것입니다.
