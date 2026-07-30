# 분야 조사: Human-AI 경험·접근성

## 1. 조사 요약

`human-ai-experience`는 AI 사용자의 일반 리터러시나 화면 구현 목록이 아니라
AI의 확률적·변동적 행동을 사람이 이해·통제·수정·복구하고 다양한 방식으로
접근할 수 있게 설계·평가하는 렌즈로 조사했습니다. Microsoft의 CHI 2019
Human-AI Interaction 지침, NIST AI RMF·AI Use Taxonomy, Google PAIR,
W3C WCAG·NAUR·WAI-ARIA, ISO 9241-110과 설명·의인화 1차 연구를 중심으로
기존 Candidate·Unit·Set·Signal과 교차검토했습니다.

## 2. Candidate 목록

| Candidate ID | 한국어 표시명 | 목적지 | 목표 |
|---|---|---|---|
| `candidate.human-ai-experience.mental-model-capability-onboarding` | AI 역량·한계 기대형성과 점진적 온보딩 | Unit | D2 |
| `candidate.human-ai-experience.user-question-centered-explanation-experience` | 사용자 질문 중심 AI 설명경험 설계 | Unit | D2 |
| `candidate.human-ai-experience.feedback-correction-user-control` | AI 피드백·수정·되돌리기 사용자 통제 설계 | Unit | D2 |
| `candidate.human-ai-experience.human-approval-override-escalation-experience` | 인간 승인·재정의·이관 상호작용 설계 | Unit | D2 |
| `candidate.human-ai-experience.conversational-repair-fallback-experience` | 대화형 AI 오류복구·대체경로 경험 설계 | Unit | D2 |
| `candidate.human-ai-experience.personalization-memory-user-control` | 개인화·기억 사용자 제어 경험 설계 | Unit | D2 |
| `candidate.human-ai-experience.human-ai-experience-evaluation` | Human-AI 경험·사용성 평가 | Unit | D2 |
| `candidate.human-ai-experience.accessible-multimodal-ai-interaction` | 접근 가능한 다중양식 AI 상호작용 가이드 | Resource | D0 |
| `candidate.human-ai-experience.social-cue-anthropomorphism-boundary-guide` | AI 사회적 단서·의인화 경계 가이드 | Resource | D0 |

## 3. 잠정 Taxonomy

- `ai-capability-mental-model-onboarding`
- `human-centered-ai-explanations`
- `ai-feedback-user-control`
- `human-approval-escalation-interaction`
- `conversational-ai-repair`
- `accessible-multimodal-ai-interaction`
- `personalization-memory-user-control`
- `human-ai-experience-evaluation`

접근 가능한 다중양식 항목은 AI 특유의 사용자 요구와 라우팅을 설명하는 D0
Resource로 제한하고 구현·검증은
`unit.software.accessible-ui-state-interaction@1.0.0`과 경험 평가 후보가
소유합니다. 사회적 단서·의인화도 효과가 맥락에 따라 달라 독립 Unit이 아닌
D0 경계 Resource로 제한합니다.

## 4. 인접 경계

- AI 기초·한계, 업무 적합성, 위험 비례 의존과 신뢰 보정은
  `ai-literacy-trust`가 소유합니다. 이번 패키지는 제품 경험이 사용자의
  mental model·행동·통제에 미치는 설계 책임을 소유합니다.
- 시스템 context·memory·평가 회귀는 `ai-systems-agents`가 소유합니다.
  이번 패키지는 사용자가 보는 기억·개인화 통제와 Human-AI 상호작용 평가만
  다룹니다.
- semantic UI·keyboard·focus·status 구현은 `software-product-engineering`이
  소유합니다. 이번 패키지는 AI 특유의 동적·다중양식 요구와 경험 평가를
  연결합니다.
- 결정적 workflow와 부작용 복구는 `integration-automation`이 소유합니다.
  이번 패키지는 승인·거부·override·fallback을 사용자가 행사하는 경험을
  다룹니다.
- 개인정보·법적 설명·고위험 감독·취약사용자 정책은
  `security-legal-governance`가 소유하며 이번 후보가 임의 확정하지 않습니다.
- 업무 역할 배분과 미래 상태 업무흐름은 기존
  `ax-strategy-value` Candidate가 소유합니다.

## 5. 주요 근거

| 출처 | 확인 범위 |
|---|---|
| Guidelines for Human-AI Interaction, CHI 2019 | 기대형성·상황별 정보·통제·오류·시간 변화 HAI 지침 |
| NIST AI RMF 1.0 Appendix C | Human-AI configuration, 역할·책임·인지편향 |
| NIST AI 200-1 | 기술 독립 Human-AI 활동과 human-centered quality |
| Google People + AI Guidebook | mental model, 설명, feedback·control의 공급자 실무 지침 |
| W3C WCAG 2.2·NAUR·WAI-ARIA 1.2 | 가역성·상태·자연어 인터페이스 대안과 구현 경계 |
| ISO 9241-110:2020 | 기술 독립 상호작용 원칙과 AI 특수성 별도 검토 경계 |
| Liao et al., CHI 2020·arXiv 2021 | 사용자 질문 중심 설명 요구·설계 process |
| Google Research, CHI EA 2024 | 의인화 단서와 신뢰의 특정 실험 범위 |

## 6. 현재 판정

후보 9개와 잠정 subdomain 8개의 독립 근거·taxonomy·실용성 감사를
완료했습니다. 최초 P0는 0건이었고 P1을 교정한 뒤 재감사에서 P0·P1 0건을
확인했습니다. Unit 후보 6개와 D0 Resource 후보 2개는 `accepted`입니다.
개인화·기억 후보 1개는 preference control을 넘는 장기 memory lifecycle
직접 근거를 보강할 때까지 `deferred`입니다. 상세 prototype·파일럿·학습효과는
검증하지 않았습니다. 후속 사용자 승인과 승격 전·후 이중 검수에 따라 Unit
후보 6개는 공개 Reference와 함께 정규 `cataloged` Unit으로, D0 Resource
후보 2개는 기존 접근 가능한 UI Unit과 신규 기대형성·온보딩 Unit의 정규
Resource로 승격했습니다. 개인화·기억 후보는 승격하지 않았습니다.
