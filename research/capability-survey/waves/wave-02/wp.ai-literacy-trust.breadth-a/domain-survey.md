# 분야 조사 보고서: AI 리터러시·신뢰

> 후보 정본은 `candidates/<candidate-id>/candidate.json`입니다. 이 문서는 사람이
> 검토할 조사 계약, 범위, 구조, 근거와 결정을 요약하며 후보 전문을 복제하지 않습니다.

## 1. 작업 패키지 계약

| 필드 | 값 |
|---|---|
| Wave | `wave-02` |
| Work package | `wp.ai-literacy-trust.breadth-a` |
| 조사 렌즈 | `ai-literacy-trust` |
| 스키마 | `capability-candidate 1.1.0` |
| 조사일 | `2026-07-27` |
| 최대/실제 후보 | 10/10 |
| 출력 경로 | `research/capability-survey/waves/wave-02/wp.ai-literacy-trust.breadth-a/` |

### 포함

- AI 유형, 작동 원리, 역량과 한계에 대한 기초 이해
- 기술·제품 중립적인 과업 프레이밍과 반복 사용
- 출력의 업무 적합성 평가와 위험 비례 검증
- 과신·과소신뢰를 피하는 의존 수준 보정
- 데이터·권리·조직 정책을 고려한 책임 있는 사용 경계
- 영향받는 사람과 유해 편향의 인식 및 전문가 이관
- AI 사용, 인간 검토, 근거 상태와 불확실성의 투명한 전달
- 주장·근거·출처 검증과 콘텐츠 provenance 해석의 기존 역량 연결

### 제외

- 모델, RAG, 에이전트, 시스템 프롬프트와 평가 하네스의 구현
- 법률 해석, 정책·접근통제·개인정보·저작권 통제체계 설계
- 인간 감독 구조, 승인·복구 워크플로와 설명·이의제기 UI 설계
- 조직 교육 운영, 역할 모델, 변화관리와 역량 측정 체계
- 특정 공급자 제품의 사용법과 기능 중심 교육
- 정규 Unit·Set·Resource 승격과 상세 커리큘럼 제작

## 2. 소유 경계

| 영역 | 이번 렌즈가 소유하는 범위 | 다른 렌즈로 넘기는 범위 |
|---|---|---|
| AI 이해 | 사용자가 용도·한계·불확실성을 설명 | 모델·시스템 구현은 `ai-systems-agents` |
| 과업 지시 | 개별 과업의 맥락·제약·완료조건 명시 | 시스템 프롬프트와 컨텍스트 설계는 `ai-systems-agents` |
| 출력 판단 | 사용 시점의 평가·수정·거부·이관 | 자동 평가기와 평가 하네스는 `ai-systems-agents` |
| 감독 | 정해진 책임에 따라 중단·승인·이관 | 감독 구조 설계는 기존 `human-ai-control` |
| 책임 있는 사용 | 민감도·권한·정책 경계를 인식하고 적용 | 법률·보안 통제 설계는 `security-legal-governance` |
| 영향 인식 | 영향받는 사람과 불균등 오류를 식별 | 전문 공정성 평가·완화는 `data-analytics-ml` 및 거버넌스 영역 |
| 투명성 | 사용 사실·검토 범위·한계를 전달 | 고지 의무 결정과 설명·이의제기 UX는 별도 렌즈 |

## 3. 잠정 분류 구조

`ai-literacy-trust` 아래에 다음 잠정 subdomain 7개를 추가했습니다. 기존
`evidence-verification`은 유지했습니다.

| 잠정 node | 초점 | 주요 제외 |
|---|---|---|
| `ai-foundations-and-limitations` | AI 유형·용도·성능·지식 한계 | 모델 수학과 구현 |
| `ai-task-framing-and-use` | 과업·맥락·제약·완료조건과 반복 교정 | 시스템 프롬프트와 제품 사용법 |
| `output-appraisal-and-decision-reliance` | 업무 적합성 평가와 위험 비례 의존 | 자동 평가기와 최종 전문판정 |
| `trust-calibration` | 자동화 편향, 과신·과소신뢰 보정 | 신뢰 인터페이스 설계 |
| `responsible-use-boundaries` | 데이터·권리·정책 경계 적용 | 법률 해석과 통제 구현 |
| `ai-impact-awareness` | 영향받는 사람과 유해 편향 인식 | 전문 영향평가와 모델 완화 |
| `ai-use-transparency` | AI 사용·검토·근거·불확실성 전달 | 법정 고지 의무와 UX 설계 |

이 구조는 탐색용 잠정 taxonomy입니다. 사용자 승인 전에는 안정된 정규 분류로
간주하지 않습니다.

## 4. 커버리지 근거

| Query family | 확인 범위 | 대표 출처 | 후보로 정규화한 결과 |
|---|---|---|---|
| AI literacy foundation | 원리, 용도, 지시, 평가, 책임 | DOL TEN 07-25, UNESCO, OECD·EC | foundations, task-framing, output-appraisal, responsible-use |
| 신뢰와 인간 판단 | 인간 역할, 인지편향, 적절한 의존 | NIST AI RMF HAI 부록, 1차 연구 | trust-calibration, risk-proportional-reliance |
| 위험과 영향 | 지식 한계, 인간 감독, 영향과 위험 비례 | NIST AI RMF Core, GenAI Profile | output-appraisal, reliance, impact-awareness |
| 근거와 provenance | 주장–출처 검증, 출처·변경 이력 | 기존 Unit, C2PA | merge-existing, resource-only |
| 규제 변화 | 역할·맥락·위험에 맞춘 AI literacy 지원 | Regulation (EU) 2026/1744 | reliance의 맥락·위험 비례 근거 |

EU 규제 근거는 2026년 개정 본문을 정본으로 사용합니다. 개정 전 Article 4 문구나
갱신되지 않은 FAQ를 현재 의무의 직접 인용으로 사용하지 않습니다.

## 5. 후보 인벤토리

| Candidate ID | 목적지 | 목표 | 결정 |
|---|---|---|---|
| `candidate.ai-literacy-trust.ai-foundations-limitations` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.ai-task-framing-use` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.output-fitness-appraisal` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.risk-proportional-reliance` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.trust-calibration` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.responsible-use-boundaries` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.affected-person-impact-awareness` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.ai-use-transparency` | Unit 후보 | D2 | 승인 |
| `candidate.ai-literacy-trust.evidence-source-verification` | 기존 Unit 병합 | D2 | 병합 승인 |
| `candidate.ai-literacy-trust.content-provenance-interpretation` | Resource 전용 | D1 | 승인 |

### 병합·보류 판단

- 주장·근거·출처 검증은 `unit.foundation.evidence-verification@1.0.0`이 이미
  소유하므로 신규 Unit으로 만들지 않습니다.
- AI 출력의 제공 근거에 대한 체계적 평가는
  `unit.ai.grounded-output-evaluation@1.0.0`과 경계를 유지합니다.
- C2PA provenance는 콘텐츠의 출처·변경 이력을 해석하는 도구이지 진실 판정 자체가
  아니므로 독립 Unit 대신 Resource 전용 후보로 둡니다.
- 사고 보고는 위험 비례 의존과 책임 있는 사용의 관찰 가능한 행동에 포함하며,
  조직 보고체계는 다른 렌즈가 소유합니다.

신규 후보 기준의 명시적 중복 병합은 8개 중 1개가 아니라 전체 인벤토리 10개 중
1개입니다. 중복률은 10%로 작업 중단 기준인 15%를 넘지 않습니다.

## 6. 학습 흐름과 관찰 가능한 결과

1. AI의 용도와 한계를 설명합니다.
2. 실제 과업을 맥락·제약·완료조건과 함께 프레이밍합니다.
3. 결과의 관련성·완전성·제약 충족 여부를 평가합니다.
4. 영향과 오류 비용에 비례해 추가 검증·인간 승인을 선택합니다.
5. 과신과 과소신뢰를 독립 판단·비교 검토로 보정합니다.
6. 데이터·권리·정책 경계에 따라 사용·중단·이관을 결정합니다.
7. 영향받는 사람과 불균등 오류 가능성을 식별합니다.
8. AI 사용 사실, 인간 검토 범위, 근거와 불확실성을 전달합니다.

평가는 설명 암기보다 시나리오 산출물을 우선합니다. 저위험과 고위험 사례, AI
출력을 수용해야 하는 사례와 거부해야 하는 사례를 함께 사용합니다.

## 7. 역할·맥락 커버리지

다음 관점을 사례와 평가 가설에 포함했습니다.

- 사무직 문서·분석 사용자뿐 아니라 현장 운영자와 고객지원 담당자
- 관리자, 승인 책임자, 독립 검토자와 구매·조달 담당자
- 콘텐츠 제작·편집 담당자와 교육·상담 담당자
- AI 결정의 대상이 되는 고객·시민·직원
- 장애인, 비영어권 사용자와 낮은 디지털 숙련도 사용자
- 생성형 AI 외의 분류·추천·예측·컴퓨터비전·음성·내장형 AI

특정 제품 UI, 공급자 안전 기능과 영어 프롬프트 숙련도를 공통 역량으로 승격하지
않습니다.

## 8. 근거 현황과 제한

- 후보 10개에 evidence 레코드 22개, 고유 URL 13개를 기록했습니다.
- 정부·국제기구·표준기관의 공식 문서와 1차 연구를 우선했습니다.
- DOL 프레임워크는 미국 노동·교육 맥락, UNESCO와 OECD·EC 프레임워크는 교육
  맥락이므로 모든 직장 역할의 완전한 taxonomy나 교육 효과를 증명하지 않습니다.
- NIST 문서는 위험관리 결과와 경계를 지지하지만 특정 교육과정의 효과를
  확정하지 않습니다.
- 적절한 의존의 측정 구성은 발전 중이므로 단일 보편 지표가 있다고 가정하지
  않습니다.
- C2PA Content Credentials는 provenance 정보를 제공하지만 콘텐츠의 진실성을
  보증하지 않습니다.
- 역할별 깊이, 공통 fixture와 치명 조건은 `assessment-contract.md`에 별도
  기록했습니다.

## 9. 확정 결정과 운영 기본값

- 8개 Unit 후보는 그대로 유지하고 역할별 목표 깊이로 조합합니다. 모든 구성원의
  D0·D1 공통 코어는 AI 기초·한계, 책임 있는 사용 경계, 영향 인식과 사용
  투명성입니다. 실제 AI 사용자·검토자의 D2 수행 코어는 과업 프레이밍, 출력
  적합성 평가와 위험 비례 의존입니다. 신뢰 보정은 빈번한 사용자·검토자·승인자를
  위한 D2 Overlay로 둡니다.
- 위험 비례 의존과 신뢰 보정은 병합하지 않습니다. 전자는 제공된 위험정책에 따라
  검증·승인·중단 강도를 선택하는 행동이고, 후자는 자동화 편향과 과신·과소신뢰를
  교정하는 인간 판단 행동입니다. 동일 fixture를 공유할 수 있지만 별도로 채점합니다.
- AI 사용 투명성의 공통 코어는 AI 사용 사실, 인간 검토 범위, 근거 상태,
  한계·불확실성과 교정 경로를 전달하는 능력입니다. 관할·업종별 법정 고지 문구와
  의무 판정은 법무 Overlay·Resource로 분리하며 공통 Unit에서 적법성을 확정하지
  않습니다.
- 비영어권·낮은 디지털 숙련도·접근성 맥락에서도 안전·정확성·근거의 합격 기준은
  낮추지 않습니다. 동등한 입력·응답 방식과 충분한 시간·보조기술을 제공하고,
  과업 판단 점수와 전달 접근성 점수를 분리하여 채점합니다.
- 생성형 chatbot 편향을 막기 위한 운영 기본값으로 공통 평가 fixture의 최소
  25%를 분류·추천·예측·컴퓨터비전·음성·내장형 AI 같은 비생성형 사례로
  구성합니다. 이는 과학적 보편값이 아니라 파일럿 전 적용할 governance floor이며,
  어떤 핵심 평가에서도 비생성형 사례를 0건으로 두지 않습니다.

## 10. 자체 점검

- [x] 최대 10개 후보 상한을 지켰습니다.
- [x] 후보마다 정의·포함·제외·경계와 관찰 가능한 결과를 기록했습니다.
- [x] 신규 8개, 병합 1개, Resource 전용 1개로 중복을 정규화했습니다.
- [x] 잠정 taxonomy만 추가하고 정규 Unit·Set·Resource·Signal은 수정하지 않았습니다.
- [x] 특정 제품, 공급자와 생성형 AI에만 종속되지 않도록 범위를 제한했습니다.
- [x] 사실, 적용 해석, 교육 효과의 불확실성을 구분했습니다.
- [x] 독립 근거·taxonomy·실용성 감사의 P1 지적을 반영했습니다.

## 11. 다음 게이트

독립 감사와 구조·회귀 검증 후 사용자가 `2026-07-28`에 후보·잠정 분류·역할별
깊이를 모두 승인했습니다. 후보는 승인된 연구 산출물이지만 정규 Unit·Set·Resource
승격은 별도 정규화 작업 전에는 수행하지 않습니다.
