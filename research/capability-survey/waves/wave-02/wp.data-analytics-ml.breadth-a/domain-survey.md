# 분야 조사: 데이터·분석·ML

## 1. 조사 요약

`data-analytics-ml` 렌즈를 직무명이나 제품 목록이 아니라 데이터가 원천에서
의사결정과 ML 운영 Gate까지 이동하는 동안 반복되는 검증 가능한 실무행동으로
조사했습니다. W3C 데이터 사양, NIST 데이터·통계·AI 지침, SDMX, ASA 공식
성명과 Google·scikit-learn의 공식 문서·1차 연구를 교차검토했습니다.

신규 후보는 9개입니다. Wave 1에서 전략 렌즈가 먼저 발견했으나 데이터 렌즈로
소유권을 이관한 `candidate.ax-strategy-value.pilot-impact-evaluation@1.0.0`을
열 번째 결과로 재사용합니다. 이번 Breadth 단계에서는 별도 Set을 만들지
않습니다.

## 2. Candidate 목록

| Candidate ID | 한국어 표시명 | 목적지 | 목표 | 주요 경계 |
|---|---|---|---|---|
| `candidate.data-analytics-ml.data-source-acquisition-contract-design` | 데이터 원천 수집·계약 설계 | Unit | D2 | 일반 API·커넥터와 정책 결정 제외 |
| `candidate.data-analytics-ml.reproducible-data-transformation-pipelines` | 재현 가능한 데이터 변환·파이프라인 | Unit | D2 | 제품별 scheduler·플랫폼 운영 제외 |
| `candidate.data-analytics-ml.analytical-model-metric-semantics` | 분석 모델·지표 의미계약 | Unit | D2 | KPI 선택과 애플리케이션 DB 제외 |
| `candidate.data-analytics-ml.exploratory-statistical-analysis` | 탐색적·통계적 분석과 불확실성 해석 | Unit | D2 | 인과 귀속·고급 전문 통계 제외 |
| `candidate.data-analytics-ml.data-quality-validation-observability` | 데이터 품질 검증·관측 | Unit | D2 | 인프라 SLO·incident 운영 제외 |
| `candidate.data-analytics-ml.data-catalog-lineage-ownership-metadata` | 데이터 카탈로그·계보·책임 메타데이터 | Unit | D2 | stewardship 정책·IAM·법적 보존 결정 제외 |
| `candidate.ax-strategy-value.pilot-impact-evaluation` | AX 파일럿 실험·영향평가 설계 | 기존 Unit 후보 재사용 | D2 | 새 ID·node를 만들지 않음 |
| `candidate.data-analytics-ml.predictive-ml-problem-framing-baselines` | 예측 ML 문제정의·비ML 기준선 | Unit | D2 | LLM prompting·투자 우선순위 제외 |
| `candidate.data-analytics-ml.predictive-ml-model-validation-decision-thresholds` | 예측 ML 모델 검증·의사결정 임계값 | Unit | D2 | LLM·agent 평가와 운영 drift 제외 |
| `candidate.data-analytics-ml.ml-lifecycle-reproducibility-monitoring` | ML 생명주기 재현성·모니터링 | Unit | D2 | 실제 배포·incident·serving 운영 제외 |

## 3. 잠정 Taxonomy

`data-analytics-ml` 아래 다음 `provisional` subdomain 9개를 추가했습니다.

- `data-source-acquisition-contracts`
- `data-transformation-pipelines`
- `analytical-modeling-metric-semantics`
- `exploratory-statistical-analysis`
- `data-quality-validation-observability`
- `data-catalog-lineage-ownership-metadata`
- `predictive-ml-problem-framing-baselines`
- `predictive-ml-model-evaluation-validation`
- `ml-lifecycle-reproducibility-monitoring`

기존 `impact-evaluation`과 `test-and-learn`은 유지합니다. 역할 보기나 향후
종단 Set은 이 node들을 조합하며 별도 정규 역량 node로 복제하지 않습니다.

## 4. 인접 경계 판정

- 일반 HTTP API·애플리케이션 관계형 schema는
  `software-product-engineering`이 소유합니다.
- SaaS·MCP 연결과 범용 업무 orchestration은 `integration-automation`이
  소유합니다.
- LLM·agent의 반복평가·grader·trajectory는 `ai-systems-agents`가 소유합니다.
- 실제 배포·서빙·SLO·incident·복구와 플랫폼 비용은
  `platform-quality-operations`가 소유합니다.
- 개인정보·IAM·DLP·법적 보존과 전문 위험통제는
  `security-legal-governance`가 소유합니다.
- 사업 KPI·가드레일의 선택은 `ax-strategy-value`가, 분석 grain과 계산
  의미계약은 이 패키지가 소유합니다.

## 5. 주요 근거

| 출처 | 확인 범위 |
|---|---|
| W3C Metadata Vocabulary for Tabular Data | 기계 판독 가능한 열·자료형·키·필수값 계약과 검증 |
| W3C DCAT 3·PROV-O·Data Quality Vocabulary | 카탈로그·버전·계보와 사용목적별 품질 표현 |
| W3C RDF Data Cube·SDMX Information Model | 관찰 grain·dimension·measure·attribute 의미 |
| NIST RDaF·Big Data Reference Architecture | 데이터 획득–처리–분석 생명주기와 기술중립 경계 |
| NIST/SEMATECH e-Handbook·ASA p-value 성명 | 탐색·추론·효과크기·불확실성 해석 경계 |
| Google ML Problem Framing | 비ML 기준선, ML 적합성, 목표·출력·성공기준 |
| scikit-learn 공식 평가·common pitfalls | 분할·교차검증·metric·누수 방지 |
| NIST AI RMF·Google ML Test Score | 맥락별 평가·monitoring·change Gate와 ML 유지보수 위험 |

## 6. 누락·오판 레드팀

- 스키마 적합성을 표본 대표성·적법성·업무 적합성으로 오인하지 않습니다.
- late/out-of-order event, 중복, 부분 출력, backfill과 schema 변경을
  재실행 fixture에 포함합니다.
- 평균의 평균, 비가산 measure, timezone·통화·단위와 동일 이름·다른 분모를
  지표 의미계약의 공격 사례로 둡니다.
- 결측 메커니즘, 다중 비교, 반복적 data peeking, 작은 표본, 군집·시계열
  의존성과 Simpson 역설을 통계 평가에 포함합니다.
- 계절성에 의한 정상 변화와 실제 품질 결함, upstream 장애와 현상 변화를
  구분합니다.
- catalog·lineage 존재를 데이터 정확성 보증으로 오인하지 않습니다.
- ML에서는 예측 이후에만 존재하는 feature, identity·시간 누수, proxy label,
  희귀 사건·label 지연과 test set 반복 최적화를 공격합니다.
- drift 없는 성능악화, drift가 있어도 유지되는 성능, feedback loop와 자동
  재학습 악화를 서로 다른 판정으로 다룹니다.

## 7. 현재 판정

신규 Candidate 9개는 `accepted`입니다. 기존 영향평가 Candidate는 최초 발견
ID와 내용을 보존한 채 재사용합니다. 독립 근거·taxonomy·실용성 감사에서
발견한 P1을 교정하고 최종 P0·P1 0건을 재확인했습니다. 비차단 P2는 정규
Resource 승격과 상세 평가 fixture 설계 때 추적하며, 정규 Unit 승격은 별도
사용자 지시에서 수행합니다.
