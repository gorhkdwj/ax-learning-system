# Phase 2 Capability Survey — Wave 5 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-05` |
| 상태 | `ready_for_wave-06-planning` |
| 시작일·마지막 갱신일 | `2026-08-02` · `2026-08-02` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 입력 Candidate | 96개 |
| 분류 Registry | `taxonomy.ax-capability-map@1.0.0` (`canonical`) |
| 작업 패키지 | `wp.candidate-normalization.integration-a` |

## 2. 완료한 목표

- Candidate 제목·정규명·alias·제안 ID 충돌 전수 점검
- stable core, Adapter·Resource와 Set 목적지 의미 경계 재검수
- Wave 1 전략 후보 7개 Unit·7개 Reference·1개 Set 정규 승격
- 해결 가능한 pending Candidate 관계의 정확한 Unit 버전 전환
- taxonomy domain 10개·subdomain 97개 canonical 확정
- deferred 근거만 있는 taxonomy node 3개 provisional 유지

## 3. 결과

| 항목 | 결과 |
|---|---|
| 제목·정규명·alias·제안 ID 충돌 | 0건 |
| 기존 ID 삭제·개명·폐기 | 0건 |
| Candidate 판정 | accepted 93, merged 1, deferred 1, needs_review 1 |
| 정규 카탈로그 | Unit 83, Resource 89, Set 9, Signal 3 |
| Taxonomy node | canonical 107, provisional 3 |
| unresolved pending 관계 | 편익 실현 Candidate 1건 |

## 4. 핵심 결정

- 동일 학습성과인 근거 검증 후보는 기존 Unit에 직접 병합하고 새 ID를 만들지 않습니다.
- 측정계약·지표 의미계약·영향평가와 해법 적합성·agent topology는 판정 단위가
  다르므로 별도 항목으로 유지하고 정확한 관계로 연결합니다.
- 조합에서만 가치가 생기는 미래 상태 업무설계는 deliverable Set으로 승격합니다.
- domain ID는 변경하지 않고 최초 조사 렌즈 이력을 Candidate discovery와
  provenance에 보존하면서 canonical 상태로 전환합니다.
- 편익 실현과 개인화 memory 관련 3개 node는 근거가 보강되기 전 provisional입니다.
- role view는 Wave 6 QA를 반영하기 전까지 planned로 유지합니다.

## 5. QA 한계

Wave 5는 기존 독립 감사를 통과한 후보의 정규화·승격 후 자체 재검수입니다.
원문 독립 재확인, 고위험·D3 전수 QA와 일반 후보 층화표본 검사는 Wave 6에서
수행합니다. 자동검사 통과는 학습효과·업무효과나 실제 조직 적합성을 뜻하지 않습니다.

## 6. 검증 증거

`2026-08-02` 공식 검증 결과입니다.

```text
Public boundary: errors=0
Catalog: units=83, resources=89, sets=9, signals=3, candidates=96
Catalog validation: errors=0, warnings=0
Regression tests: 33/33 passed
git diff --check: passed
```

## 7. 변경 범위

### 생성

- Wave 5 manifest·normalization review·자체 감사·Checkpoint
- 전략·가치 Unit 7개와 공개 Reference 7개
- 미래 상태 업무설계 Set 1개

### 수정

- Wave 1 Candidate 9개 추적 상태
- 기존 Unit 3개와 Resource 1개의 pending 관계
- Taxonomy Registry와 관련 거버넌스·아키텍처·Runbook·추적 문서

### 의도적으로 수정하지 않음

- `research/signals/`
- deferred·needs_review Candidate의 판정과 근거
- 상세 교재·fixture·runner·HUB
- Vault 추적 파일과 로컬 원문

## 8. 중단조건 확인

- [x] 기존 ID를 삭제·개명·폐기하지 않았습니다.
- [x] defer 후보를 자동 승격하지 않았습니다.
- [x] 정규 산출물은 exact Candidate ID·version을 역참조합니다.
- [x] 해결되지 않은 관계는 명시적 pending으로 유지했습니다.
- [x] 미확인 효과를 확인된 사실로 확정하지 않았습니다.
- [x] 현재 상태를 이 Checkpoint와 Wave 5 산출물로 복원할 수 있습니다.

## 9. 다음 한 단계

Wave 6 manifest에서 고위험·D3·논쟁 후보 전수검수 대상과 대분류별
`max(3건, 후보의 15%)` 일반 층화표본을 고정합니다. 근거 원문, taxonomy 판정,
실무성·깊이와 승격 후 정규 산출물의 추적성을 독립 재검수합니다.
