# Phase 2 Capability Survey — Wave 6 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-06` |
| 상태 | `ready_for_wave-07-planning` |
| 시작일·마지막 갱신일 | `2026-08-02` · `2026-08-02` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| Candidate 모집단 | 96개 |
| 독립 QA 대상 | 고위험·D3·논쟁 30개 + 일반 층화표본 26개 = 고유 56개 |
| 작업 패키지 | `wp.independent-qa.stratified-a` |

## 2. 완료한 목표

- QA 대상 56개를 결정적 규칙으로 고정하고 세 독립 감사축으로 재검수
- 고위험·D3·논쟁 30개와 관련 evidence 99건 전수검수
- 일반 층화표본 26개의 정의·학습성과·분류·전이성 재검수
- Wave 5 신규 Unit 7개·Reference 7개·Set 1개 승격 추적성 재검수
- 공식 원문 URL, evidence claim, Candidate 관계와 실행 안전계약 교정

## 3. 최종 결과

| 감사축 | P0 | P1 | P2 | 판정 |
|---|---:|---:|---:|---|
| 근거 | 0 | 0 | 2 | 승인 |
| Taxonomy | 0 | 0 | 1 | 승인 |
| 실용성·안전 | 0 | 0 | 0 | 승인 |

Taxonomy 잔여 P2는 8개 역할 관점의 기계 판독형 view가 아직 없다는 공백이며
Wave 7로 이관합니다. 근거 메타데이터의 비필수 `source_version` 공란과 projection
차이는 값을 추정하지 않고 잔여위험으로 보존합니다.

## 4. 교정 범위

- 현행 Orange Book, Arazzo 1.1.0과 RPA Program Playbook 공식 URL
- 승격 산출물 15개의 `evidence_claims`
- 전략 Unit 7개의 `source_candidate_relations`, 활성화 전 Gate와 오프라인 평가
- 미래 상태 Set의 활성화 전 Gate
- 현행 업무분석·과업 역할배분의 안전한 fixture와 실제 자료 overlay 경계

기존 ID·정규 관계·Candidate 판정·taxonomy 상태는 변경하지 않았습니다.

## 5. 검증 증거

```text
Public boundary: errors=0
Catalog: units=83, resources=89, sets=9, signals=3, candidates=96
Catalog validation: errors=0, warnings=0
Regression tests: 33/33 passed
git diff --check: passed
```

## 6. 다음 한 단계

Wave 7에서 Wave 4의 8개 역할 관점을 canonical node 조합의 role view로 만들고,
공백·deferred·불확실성과 `cataloged`·활성·검증 상태를 구분한 최종 역량지도를
조립하여 Phase 2 완료 Gate를 판정합니다.
