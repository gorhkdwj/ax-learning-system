# Wave 5 Candidate·Taxonomy 정규화 검토

## 1. 결론

Candidate 96개의 제목·정규명·alias·제안 Unit·Set ID를 전수 대조한 결과 직접
충돌은 모두 0건입니다. 기존 근거 검증 Unit과 같은 학습성과인 Candidate 1개는
기존 `merge_existing` 결정을 유지하고, 서로 비슷하지만 산출물·검증이 다른 항목은
분리했습니다.

Wave 1에서 감사·사용자 승인을 받았으나 정규 카탈로그에 남지 않았던 전략 후보
7개와 조합형 후보 1개를 각각 Unit·Reference와 Set으로 승격했습니다. 편익 실현과
개인화·장기 memory 통제는 근거·경계가 부족하므로 승격하지 않았습니다.

## 2. 기계적 충돌 점검

| 검사 | 대상 | 결과 |
|---|---:|---:|
| 동일 `title` | 96개 | 0건 |
| 동일 `canonical_name` | 96개 | 0건 |
| 정규화 alias 충돌 | 전체 alias | 0건 |
| 동일 `proposed_unit_id` | Unit 후보 | 0건 |
| 동일 `proposed_set_id` | Set 후보 | 0건 |
| 기존 카탈로그 ID와 신규 ID 충돌 | 신규 8개 대상 | 0건 |
| 기존 ID 삭제·개명 | 전체 | 0건 |

문자열 충돌이 없다는 사실만으로 의미 중복이 없다고 확정하지 않고 다음 경계군을
별도로 검토했습니다.

## 3. 의미 경계 검토

| 비교군 | 결정 | 이유 |
|---|---|---|
| 주장·출처 검증 / 근거 연결 출력 평가 | 기존 Unit 유지·별도 유지 | 전자는 일반 claim–evidence 판정, 후자는 제공 근거와 AI 출력의 정합성 평가입니다. |
| AX 해법 적합성 / workflow·agent 토폴로지 | 별도 Unit·Set 유지 | 사업 해법 선택과 구축 후 실행구조 비교의 판정 단위가 다릅니다. |
| 성과 측정계약 / 지표 의미계약 / 영향평가 | 세 Unit 유지·관계 연결 | KPI 선택계약, 계산 의미, 반사실 기반 영향평가는 산출물과 검증 방식이 다릅니다. |
| 결정적 workflow / agent 경계 | Unit + Resource 유지 | 구현 역량과 D0 선택 경계를 분리합니다. |
| 접근 가능한 UI 구현 / AI 다중양식 접근성 | Unit + Resource 유지 | 구현 소유권은 UI Unit에 있고 AI 특화 요구는 Reference로 연결됩니다. |
| MCP와 특정 공급자 SDK | protocol Unit 역할 유지, 제품 사용법은 Resource·Adapter | 공급자 독립 계약과 변동 구현을 분리합니다. |
| RAG·agent topology·미래 업무설계 | Set 유지 | 여러 독립 Unit을 조합해야 종단 간 산출물이 성립합니다. |
| 편익 실현 / 포트폴리오·측정 | `defer` 유지 | 공통 프로젝트 편익관리와 AX 특화 Resource 경계가 아직 확정되지 않았습니다. |

## 4. Wave 1 정규 승격

| Candidate | 정규 목적지 |
|---|---|
| `candidate.ax-strategy-value.opportunity-value-framing` | `unit.ax-strategy-value.opportunity-value-framing@1.0.0` |
| `candidate.ax-strategy-value.current-state-work-analysis` | `unit.ax-strategy-value.current-state-work-analysis@1.0.0` |
| `candidate.ax-strategy-value.task-allocation` | `unit.ax-strategy-value.task-allocation@1.0.0` |
| `candidate.ax-strategy-value.solution-fit-assessment` | `unit.ax-strategy-value.solution-fit-assessment@1.0.0` |
| `candidate.ax-strategy-value.measurement-contract` | `unit.ax-strategy-value.measurement-contract@1.0.0` |
| `candidate.ax-strategy-value.portfolio-prioritization` | `unit.ax-strategy-value.portfolio-prioritization@1.0.0` |
| `candidate.ax-strategy-value.enterprise-ax-roadmap` | `unit.ax-strategy-value.enterprise-ax-roadmap@1.0.0` |
| `candidate.ax-strategy-value.future-state-redesign` | `set.deliverable.ax-future-state-work-design@1.0.0` |

각 Unit에는 Candidate의 공식·1차 근거를 보존한 공개 Reference 1개를 등록했습니다.
`cataloged`는 상세 교재·fixture·학습효과 또는 업무효과 검증 완료를 뜻하지 않습니다.

## 5. 관계 정규화

- 새 전략 Unit 7개의 Candidate 관계를 `prerequisite`, `recommended_before`,
  `related_to`의 정확한 Unit 버전으로 변환했습니다.
- 영향평가 Unit의 측정계약 pending 관계를 정규 `prerequisite`로 전환했습니다.
- 분석 지표 의미계약과 예측 ML 문제정의 Unit의 측정·해법 pending 관계를 정규
  Unit 관계로 전환했습니다.
- 결정적 workflow 경계 Resource의 해법 적합성 pending 관계를 정규 카탈로그
  참조로 전환했습니다.
- 포트폴리오 Unit의 편익 실현 관계는 대상 Candidate가 `needs_review`이므로
  유일한 `pending_candidate_relations`로 유지했습니다.
- `source_candidate_relations`는 발견·승격 provenance이므로 정규 관계와 함께
  보존하며 현재 관계로 오해하지 않습니다.

## 6. Taxonomy 정규화

Coverage와 승격 근거가 있는 10개 domain과 97개 subdomain을 canonical로
확정하고 Registry를 `taxonomy.ax-capability-map@1.0.0`으로 올렸습니다.
Candidate의 `discovery.lens_id`와 provenance가 최초 조사 렌즈 이력을 보존하므로
안정 ID는 변경하지 않았습니다.

다음 3개 node는 provisional로 유지합니다.

| node | 이유 | 재개 조건 |
|---|---|---|
| `operational-value` | 편익 실현 후보의 상위 경계만 존재 | 공통 프로젝트·제품 가치 운영 소유권 확정 |
| `benefits-realization` | Candidate가 `needs_review`·`defer` | 중복·Resource 경계와 검증 가능한 학습성과 확정 |
| `personalization-memory-user-control` | Candidate가 `deferred` | 장기 memory lifecycle 직접 근거와 삭제·철회 평가계약 확보 |

기존 프론트엔드·백엔드·데이터 엔지니어링 role view는 여전히 `planned`입니다.
Wave 4의 8개 역할 관점과 canonical subdomain 조합은 Wave 6 QA 결과를 반영한 뒤
Wave 7 지도 조립에서 확정합니다.

## 7. 현재 정규 결과

| 항목 | 수량 |
|---|---:|
| Candidate | 96 |
| accepted / merged / deferred / needs_review | 93 / 1 / 1 / 1 |
| Unit | 83 |
| Resource | 89 |
| Set | 9 |
| Signal | 3 |
| canonical / provisional taxonomy node | 107 / 3 |
