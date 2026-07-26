# 분야 조사 보고서: AX 전략·업무재설계·가치실현

> 후보별 정본은 `candidates/<candidate-id>/candidate.json`입니다. 이 문서는
> 사람이 검토할 구조와 결정만 요약하며 후보 전문을 복제하지 않습니다.

## 1. 작업 패키지 계약

| 필드 | 값 |
|---|---|
| Wave | `wave-01` |
| Work package | `wp.ax-strategy-value.pilot` |
| 조사·통합 | Codex 메인 세션, 최초 Codex 감사자와 신규 Orca·Claude 감사자 |
| 스키마 | `capability-candidate 1.1.0` |
| 조사일 / 최종 감사일 | `2026-07-26` / `2026-07-27` |
| 최대/실제 후보 | 10/10 |
| 출력 경로 | `research/capability-survey/waves/wave-01/wp.ax-strategy-value.pilot/` |

### 포함

- 업무 문제와 AX 가치가설의 정의
- 실제 현행 업무 분석과 과업 수준 역할 배분
- 현행·SaaS·결정적 자동화·AI 워크플로우·에이전트의 기술중립 비교
- 미래 인간-AI 업무시스템 설계
- 측정계약, 파일럿 영향평가와 편익 추적의 경계
- 복수 AX 후보의 포트폴리오 우선순위·재균형
- 전사 AX 역량 격차·의존성·실행 파동 로드맵

### 제외

- 특정 제품 사용법과 상세 소프트웨어 구현
- 상세 목표운영모델·조직변화·인력계획·법률 자문·조달·전문 회계
- 상세 교재·실습·HUB 구축
- Candidate의 정규 Unit·Set·Resource 승격

### 관점 커버리지

- 경영·전략, 현업 프로세스 소유자, 제품·서비스 기획
- 데이터·분석, 보안·위험·감사, 운영·지원
- 인사·변화관리, 재무·조달 관점은 경계를 확인하고 별도 렌즈로 라우팅

## 2. 분야 구조 초안

| 중분류 ID | 이름 | 정의 | 주요 후보 | 조사 상태 |
|---|---|---|---|---|
| `portfolio-strategy` | AX 포트폴리오 전략 | 복수 후보를 가치·위험·역량·의존성으로 비교하고 재균형 | portfolio-prioritization | 독립 감사·교정 완료 |
| `enterprise-roadmap` | 전사 AX 역량 로드맵 | 사업 결과와 공통 기반 역량을 실행 파동·게이트로 연결 | enterprise-ax-roadmap | 독립 감사·교정 완료 |
| `opportunity-value` | 기회·가치 프레이밍 | 기술보다 문제·기대결과·반증조건을 먼저 정의 | opportunity-value-framing | 조사·감사 완료 |
| `work-system-analysis` | 현행 업무 분석 | 실제 증거로 흐름·병목·기준선을 복원 | current-state-work-analysis | 조사·감사 완료 |
| `task-work-design` | 과업·역할 배분 | 과업 수준에서 인간·자동화·AI 책임을 배분 | task-allocation | 조사·감사 완료 |
| `solution-selection` | 해법 적합성 | 같은 수용기준으로 대안을 기술중립 비교 | solution-fit-assessment | 조사·감사 완료 |
| `future-state-design` | 미래 업무시스템 | 선행 역량을 결합해 정상·예외·복구 흐름 설계 | future-state-redesign | Set 후보 |
| `outcome-measurement` | 성과 측정계약 | 분모·창·출처·가드레일이 재현되는 계약 설계 | measurement-contract | 조사·감사 완료 |
| `impact-evaluation` | 개입 영향평가 | 반사실과 주장 한계를 포함한 파일럿 평가 설계 | pilot-impact-evaluation | 데이터 렌즈 이관 |
| `benefits-realization` | 편익 실현 | 실제 편익과 완전원가의 운영 추적 | benefits-realization | 공통 Unit 발견 전 보류 |

이 구조는 고정 트리가 아니라 탐색 보기입니다. 영향평가는
`data-analytics-ml`에, 일반 편익관리는 향후 공통 프로젝트·제품 역량에
소유권을 두도록 라우팅했습니다.

## 2A. 커버리지 근거

### 검색·탐색 계약

| Query family | 조사 범위 | 확인한 출처 계층 | 결과·라우팅 |
|---|---|---|---|
| 기회·사업가치·no-go | 문제, 목표, 기대 가치, 비AI 대안 | NIST, 정부 평가 지침, 원 실무자 | opportunity-value-framing |
| 현행 업무·과업·역할 | 실제 흐름, 병목, 인간-AI 책임 | 표준, 1차 연구, 원 실무자 | current-state-work-analysis, task-allocation |
| 해법 선택·업무 재설계 | SaaS·자동화·AI·에이전트 비교, 예외·복구 | 공식 프레임워크, 원 실무자 | solution-fit-assessment, future-state-redesign |
| 측정·영향·편익 | 측정계약, 반사실, 운영 편익 | 공식 통계·평가 지침, 1차 연구 | measurement-contract, impact-evaluation, benefits-realization |
| 포트폴리오·전사 로드맵 | 우선순위, 위험선호, 공통 역량, 실행 파동 | ISO, NIST, OECD, 정부·독립 실무기관 | portfolio-prioritization, enterprise-ax-roadmap |
| 운영모델·변화·조달 | 조직 책임, 인력, 공급자·재무 경계 | 공식 지침과 인접 분야 확인 | 운영모델·변화는 organization-adoption, 보안·법무는 security-legal-governance로 라우팅; 전문 재무·조달은 미개설 렌즈 공백 |

### 반복 패스와 포화 판정

| Pass | 초점 | 새 고우선 후보 | 다른 렌즈로 보낸 공백 | 판정 |
|---|---|---:|---|---|
| P1 | 전략·업무재설계·가치실현 최초 발견 | 8 | 영향평가, 공통 편익관리 | 계속 |
| P2 | “전략 렌즈인데 전사 선택·순서화가 빠졌는가” 레드팀 | 2 | 상세 운영모델 | 계속 |
| P3 | 역할·인접 분야·출처 편향 확인 | 0 | 변화관리, 보안·법무, 재무·조달 | Manifest 범위 내 잠정 포화 |

후보 수 상한 때문에 끝낸 것이 아닙니다. P3에서 새 고우선 후보가 없었고 남은
공백을 다른 렌즈 또는 Deep Research로 라우팅했으므로 이 작업 패키지 범위
안에서만 잠정 포화로 판정합니다. 이는 Phase 2 전수조사의 완료 선언이 아닙니다.

### 역할 관점

| 역할·기능 | 상태 | 발견 후보·공백 | 근거 또는 라우팅 |
|---|---|---|---|
| 경영·포트폴리오 | 조사됨 | 기회, 포트폴리오, 로드맵 | 본 작업 패키지 |
| 현업 프로세스 소유자 | 조사됨 | 현행 분석, 과업 배분, 미래상태 | 본 작업 패키지 |
| 제품·서비스·UX | 조사됨 | 해법 적합성, 미래상태; 상세 UX 제외 | `human-ai-experience` |
| 데이터·분석 | 조사됨 | 측정계약; 영향평가 이관 | `data-analytics-ml` |
| 아키텍처·플랫폼 | 근거 있는 공백 | 로드맵 의존성까지만 포함 | `software-product-engineering` |
| 보안·법무·감사 | 근거 있는 공백 | 제약·게이트까지만 포함 | `security-legal-governance` |
| 운영·지원 | 조사됨 | 예외·복구·운영 편익 | 본 패키지와 운영 렌즈 |
| 인사·변화관리 | 근거 있는 공백 | 상세 역할·역량 전환 제외 | `organization-adoption` |
| 재무·조달 | 근거 있는 공백 | 전문 투자심사·계약 제외 | 승인 렌즈 목록에 소유자가 없는 공백 |

## 3. 후보 인벤토리

| Candidate ID | 정규 명칭 | 목적지 | 목표 | 신뢰도 | 판정 |
|---|---|---|---|---|---|
| `candidate.ax-strategy-value.portfolio-prioritization` | AX initiative portfolio prioritization and rebalancing | Unit 후보 | D2 | medium | 유지 제안 |
| `candidate.ax-strategy-value.enterprise-ax-roadmap` | Enterprise AX capability roadmap design | Unit 후보 | D2 | medium | 유지 제안 |
| `candidate.ax-strategy-value.opportunity-value-framing` | AX opportunity and value-hypothesis framing | Unit 후보 | D2 | medium | 유지 |
| `candidate.ax-strategy-value.current-state-work-analysis` | Current-state work-system analysis | Unit 후보 | D2 | medium | 유지 |
| `candidate.ax-strategy-value.task-allocation` | Task decomposition and human-AI work allocation | Unit 후보 | D2 | medium | 유지 |
| `candidate.ax-strategy-value.solution-fit-assessment` | Technology-neutral solution fit assessment | Unit 후보 | D2 | medium | 유지 |
| `candidate.ax-strategy-value.future-state-redesign` | Future-state human-AI work-system design | Set 후보 | D2 | medium | 통합 산출물로 유지 |
| `candidate.ax-strategy-value.measurement-contract` | AX outcome measurement contract design | Unit 후보 | D2 | medium | 유지 |
| `candidate.ax-strategy-value.pilot-impact-evaluation` | Intervention impact evaluation design | Unit 후보 | D2 | medium | 데이터 렌즈로 이관 |
| `candidate.ax-strategy-value.benefits-realization` | Benefits realization and value tracking | 보류 | D2 | medium | 공통 Unit에 병합 대기 |

실제 의사결정자나 조직 데이터가 없는 경우에도 최소 5개의 합성 후보와 변경
제약을 사용해 포트폴리오·로드맵 판단 능력을 학습할 수 있도록 설계했습니다.
실제 조직의 최종 투자 승인과 전략 결정은 학습 범위에 포함하지 않습니다.

### 사용자 결정 매트릭스

| 후보 | 유지 이유 | 병합하지 않는 이유 | 잔여 위험 | 조사팀 권고 |
|---|---|---|---|---|
| 포트폴리오 우선순위 | 복수 후보 선택·재균형이라는 독립 산출물 | 개별 기회·해법 평가는 후보 간 자원배분을 다루지 않음 | 민간 전이·재무 경계 | 유지 제안 |
| 전사 AX 로드맵 | 공통 역량·의존성·실행 파동을 연결 | 프로젝트 일정이나 개별 후보 순위와 판정 기준이 다름 | 운영모델 경계 | 유지 제안 |
| 기회·가치 프레이밍 | 문제·가설·no-go를 고정하는 공통 입력 | 측정·해법 선택보다 앞선 별도 업무성과 | 민간 산출물 크기 | 유지 |
| 현행 업무 분석 | 실제 흐름·병목·기준선을 증거로 복원 | 미래상태나 과업 배분이 대신할 수 없음 | 로그 없는 업무 표본 | 유지 |
| 과업·역할 배분 | 인간·자동화·AI 책임 경계를 과업 수준에서 결정 | 전체 프로세스 설계와 다른 판정 단위 | 산업별 책임 한계 | 유지 |
| 해법 적합성 | 같은 수용기준으로 비AI·AI 대안을 비교 | 기회 프레이밍은 상세 대안 판정을 소유하지 않음 | 가중치 보정 | 유지 |
| 미래상태 재설계 | 앞선 역량을 정상·예외·복구 흐름으로 통합 | 단일 Unit보다 조합형 수행평가가 적합 | Set 크기 | Set 후보 유지 |
| 측정계약 | 분모·창·출처·가드레일을 재현 가능하게 고정 | 전문 영향평가 이전의 독립 선수역량 | 업무별 기준 | 유지 |
| 파일럿 영향평가 | 반사실과 주장 한계를 포함한 평가 설계 | 측정계약만으로 인과 주장을 판정할 수 없음 | 전문 평가 경계 | 데이터 렌즈 이관 |
| 편익 실현 | 운영 중 편익·완전원가 추적은 필요 | 일반 프로젝트 편익관리와 중복 가능 | 정규 소유자 미정 | 보류 |

## 4. 선행관계와 학습 흐름

업무 단위 실행 흐름은 다음과 같습니다.

1. 기회·가치 프레이밍과 현행 업무 분석으로 문제·기준선을 고정합니다.
2. 현행 분석을 바탕으로 과업·역할을 배분합니다.
3. 기회 정의와 과업-역할 행렬로 기술중립 해법을 선택합니다.
4. 측정계약을 설계하고 위 역량들을 미래 업무시스템 Set에서 통합합니다.
5. 파일럿 영향평가로 실제 효과와 설계 예상값을 구분합니다.
6. 편익 추적은 공통 편익관리 역량의 소유권이 확인된 뒤 연결합니다.

전사 전략 흐름은 여러 업무 단위의 기회·측정 정보를 포트폴리오에서 비교하고,
선택된 후보와 공통 선행 역량을 전사 로드맵으로 순서화한 뒤 새 증거와 제약
변화에 따라 두 산출물을 반복 갱신합니다. 이는 선형 일회성 절차가 아니라
업무 루프와 포트폴리오 루프가 서로 증거를 공급하는 구조입니다.

기존 예제 카탈로그의 `unit.foundation.evidence-verification`과
`unit.ai.grounded-output-evaluation`은 후보의 직접 중복이 아니라 모든 조사와
향후 실습에 적용할 조건부 선수역량입니다.

## 5. 교차 품질축

| 품질축 | 적용 | 주요 위치 | 후속 조치 |
|---|---|---|---|
| 정확성과 결과 검증 | 적용 | 전 후보 | 미지 입력·fixture·제약 변경·실패 주입 합격조건 유지 |
| 보안·개인정보·권한 | 적용 | 현행 분석, 역할 배분, 미래상태, 평가 | 상세 통제는 보안·법무 렌즈에 연결 |
| 법무·윤리·저작권 | 조건부 | 역할 배분, 미래상태 | 고위험 자동결정은 별도 전문 검토 |
| 접근성·Human-AI Interaction | 조건부 | 역할 배분, 미래상태 | 상세 UX는 human-ai-experience가 소유 |
| 비용·성능 | 적용 | 포트폴리오, 해법 적합성, 측정, 편익 | 수용 결과당 완전원가와 가용 역량으로 비교 |
| 관측성·신뢰성·복구 | 적용 | 현행 분석, 미래상태, 측정 | D3 구현은 운영 렌즈로 이관 |
| 유지보수·변경관리 | 적용 | 포트폴리오, 로드맵, 해법 적합성, 미래상태, 편익 | D2에서는 설계·판단·재계획까지만 학습 |
| 조직 도입·성과측정 | 적용 | 측정, 영향평가, 편익 | 조직변화 소유권은 별도 렌즈 |

## 6. 근거 품질

| 출처 유형 | 등록 수 | 직접 지지하는 범위 | 제한 |
|---|---:|---|---|
| 표준 | 2 | BPMN 표현, AI 관리체계 | 특정 실무 효과나 로드맵 형식은 지지하지 않음 |
| 공식 문서·소스 | 25 | 범위·위험·평가·업무·전략 관련성 | 공공부문에서 민간으로의 전이는 가설 |
| 1차 연구 | 2 | 과업 노출과 지표 해석 위험 | 특정 연구 맥락 밖 효과 일반화 금지 |
| 원 실무자 자료 | 5 | 업무 경험조사·RPA 후보평가·에이전트 선택·프로세스 마이닝·포트폴리오 실무 | 보편 임계값이나 효과 크기 아님 |

총 34개 evidence 레코드와 25개 고유 URL을 사용했습니다. 검색결과 요약,
커뮤니티 재진술과 AI의 설명은 evidence로 등록하지 않았습니다.

## 7. Deep Research 후보와 재개 조건

| 대상 | 트리거 | 확인할 주장 | 우선순위 |
|---|---|---|---|
| 영향평가 | 여러 렌즈에서 재사용되는 핵심 선수역량 | D2와 전문 평가 이관 기준 | 높음 |
| 고위험 인간 통제 | 법적·권한상 고위험 | 산업별 필수 승인·이의제기·복구 | 높음 |
| 편익 실현 | 중복·병합 판정 | 공통 Unit과 AX 특화 Resource 경계 | 중간 |
| 민간부문 전이 | 공식 근거의 공공부문 편향 | 산출물 최소 크기와 의사결정 유효성 | 중간 |
| 포트폴리오 우선순위 | 사용자 유지 결정·파일럿 편입 | 재무 전문성 없는 D2 비교 기준과 민간 전이 | 높음 |
| 전사 AX 로드맵 | 사용자 유지 결정·다른 렌즈 조사 | 운영모델·변화관리와의 최소 경계 | 높음 |

## 8. 미해결 질문

- 민간·비영리 조직에서 각 산출물의 최소 유효 크기는 얼마입니까?
- 이벤트 로그가 없는 수작업 업무의 신뢰 표본은 어떻게 보정해야 합니까?
- 영향평가의 공통 Unit과 AI 특화 Resource를 어떤 경계로 나눕니까?
- 산업별 고위험 승인·권한 통제는 어느 렌즈가 최종 소유합니까?
- 역량 로드맵과 목표운영모델·변화관리의 최소 학습 경계는 어디입니까?
- 포트폴리오 비교에서 일반 실무자가 다룰 수 있는 가치·위험 판단과 전문
  투자심사의 경계를 어떻게 교정합니까?
- 전사 위험선호 정의와 make·buy·partner 판단을 어느 향후 렌즈가
  소유합니까?

## 9. 자체 점검

- [x] 모든 후보에 정의·포함·제외와 관찰 가능한 행동이 있습니다.
- [x] 모든 후보에 서로 다른 업무 전이 맥락이 있습니다.
- [x] 사실과 비즈니스 효과 가설을 구분했습니다.
- [x] D2 목표·상한과 객관적 평가 가설을 명시했습니다.
- [x] 기술·제품을 범용 역량으로 과대승격하지 않았습니다.
- [x] 후보 파일이 스키마와 참조 검증을 통과했습니다.
- [x] 정규 카탈로그·Set·Signal을 수정하거나 승격하지 않았습니다.
- [x] 검색군·역할 관점·반복 패스와 잠정 포화의 범위를 기록했습니다.
- [x] 신규 전략 후보 2개의 독립 근거·분류·실무성 감사와 P0·P1 교정을
  완료했습니다.

## 10. 다음 검토

10개 후보 모두 독립 감사를 마쳤고 신규 전략 후보 2개의 P0·P1 교정과 구조
검증을 완료했습니다. 다음 단계는 사용자가 10개 후보의 유지·이관·보류 판정,
커버리지 근거와 이번 시험 배치의 조사 깊이를 검토하는 것입니다. 이 검토
전에는 정규 Unit·Set·Resource로 승격하지 않습니다.
