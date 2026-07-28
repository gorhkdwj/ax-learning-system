# Taxonomy·중복 감사: wp.ai-literacy-trust.breadth-a

## 범위와 방법

- 대상: Candidate 10개, 신규 잠정 subdomain 7개, 기존 Unit·Resource·Set·Signal,
  Wave 1 Candidate
- 감사 역할: 읽기 전용 taxonomy·중복 감사자
- 확인: 소유 경계, 중복·병합, 후보 종류, 관계·순환, 깊이와 다른 렌즈 이관
- 감사일: `2026-07-27`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| Pass | 3 |
| Conditional pass | 7 |
| Fail | 0 |
| P0 | 0 |
| P1 수정 묶음 | 7 |
| P2 개선 묶음 | 4 |

깨진 참조와 관계 순환은 없었습니다. 명시적 기존 항목 병합은 1/10건으로 중단
기준 15% 이하이며 신규 Unit 후보 8개는 서로 분리할 수 있다고 판정했습니다.

## P1 교정

| 대상 | 지적 | 반영 |
|---|---|---|
| 과업 프레이밍 | 명칭은 전체 AI이나 행동은 대화형·생성형 중심 | 정의·요약·성과를 상호작용형·생성형으로 한정하고 비대화형 운영 설정 제외 |
| 과업 프레이밍 | `두 번 이하` 임의 기준 | 사전 반복·시간 한도와 제약 충족·안전한 중단 기준으로 교체 |
| AI 사용 투명성 | 출력 적합성을 필수 선수로 둠 | `recommended_prerequisite`로 완화하고 근거 검증 후보를 권장 선수로 추가 |
| 근거·출처 검증 | `candidate_kind: practice` | `capability`로 교정, 기존 Unit 병합은 유지 |
| 출력 적합성 | 직접 사실 검증과 정확성 표현 중복 | 제공된 입력·참조 사실·업무계약 일치성으로 좁히고 직접 주장–출처 검증과 분리 |
| 출력 적합성 | 과업 프레이밍을 필수 선수로 둠 | 외부 업무계약 평가를 허용하도록 권장 선수로 완화 |
| 책임 있는 사용 | 사용자 능력을 `control`로 분류 | `capability`로 교정하고 제공된 정책·분류표·승인 규칙 안의 행동으로 제한 |
| 위험 비례 의존 | 사용자가 조직 위험정책을 설계하는 것으로 읽힐 수 있음 | 제공된 위험 허용도·승인·이관 규칙 안의 행동으로 제한 |
| 위험 비례 의존 | 출력 평가를 필수 선수로 둠 | 사전 금지·승인 판단을 허용하도록 권장 선수로 완화 |
| 두 taxonomy node | 업무 위험 판단과 인지적 의존 보정 경계가 겹침 | 각 node의 상호 제외 문구 추가 |

## 기존 콘텐츠와의 소유 경계

- `unit.foundation.evidence-verification`: 주장–출처 직접 검증
- `unit.ai.grounded-output-evaluation`: 제공 근거에 대한 체계적 AI 출력 평가
- `output-fitness-appraisal`: 업무계약 충족과 수정·재생성·폐기 선택
- `risk-proportional-reliance`: 정해진 정책 아래 검증·승인·중단 강도 선택
- Wave 1 `human-ai-control`: 감독·승인·복구 구조 설계
- `trust-calibration`: 자동화 편향과 과신·과소신뢰의 인간 행동 보정
- `content-provenance-interpretation`: 기존 근거 검증 Unit의 Resource

## P2 반영·추적

- 신규 node의 provenance는 매니페스트가 아니라 실제 조사 결과
  `domain-survey.md`를 참조하도록 교정했습니다.
- provenance Resource의 기본 귀속을
  `unit.foundation.evidence-verification@1.0.0`으로 명시했습니다.
- 신뢰 보정 평가는 정답·오답과 오류 기저율이 고정된 혼합 과제를 사용하도록
  명시했습니다.
- 책임 있는 사용↔위험 비례 의존, 신뢰 보정↔출력 적합성의 탐색 관계를
  추가했습니다.

## 결론

P0는 없었고 P1을 모두 반영했습니다. 기존 정규 카탈로그·Set·Signal은 수정하지
않았으며 후보와 잠정 taxonomy만 조사 산출물로 유지합니다. 수정 후 같은 읽기
전용 감사자가 재확인한 결과 P0·P1·잔여 P2는 모두 0건이며 관계 대상·버전과
순환 검사도 통과했습니다.
