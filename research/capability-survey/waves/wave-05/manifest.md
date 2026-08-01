# Work Package Manifest: wp.candidate-normalization.integration-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-05` |
| 작업 패키지 | `wp.candidate-normalization.integration-a` |
| 상태 | `complete` |
| 실행일 | `2026-08-02` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 입력 | Candidate 96개, Taxonomy node 110개, Unit 76개, Resource 82개, Set 8개 |
| 변경 상한 | 기존 ID 삭제·개명 0개, 신규 정규 산출물 15개 |

## 목표

- 같은 이름·다른 학습성과와 다른 이름·같은 학습성과를 구분합니다.
- Candidate 제목·정규명·alias·제안 Unit·Set ID 충돌을 전수 점검합니다.
- 공급자 구현은 stable core의 Adapter·Resource 경계로, 조합 성과는 Set으로 유지합니다.
- 아직 정규 승격되지 않은 Wave 1 승인 후보를 Unit·Reference·Set으로 승격합니다.
- 정규 대상이 생긴 `pending_candidate_relations`를 정확한 Unit 버전 관계로 전환합니다.
- Coverage와 감사를 통과한 domain·subdomain을 canonical taxonomy로 확정하고
  근거가 부족한 node는 provisional로 유지합니다.

## 비목표

- 기존 ID 삭제·개명·병합과 연쇄 alias 생성
- deferred Candidate를 상한 충족 목적으로 승격
- 상세 교재·fixture·runner·HUB와 개인 학습 우선순위 제작
- Wave 6 독립 QA와 Phase 2 완료 선언

## 정규화 규칙

1. 제목, `canonical_name`, 정규화 alias와 제안 정규 ID가 중복되면 학습성과와
   검증 방식을 비교합니다.
2. 같은 학습성과는 새 ID를 만들지 않고 최종 정규 대상 하나를 직접 참조합니다.
3. 경계·검증이 다르면 비슷한 명칭이어도 별도 Unit 또는 Set으로 유지합니다.
4. 공급자·버전 사용법은 stable core를 대체하지 않고 Adapter·Resource로 둡니다.
5. 여러 Unit을 조합해야 산출물이 완성되면 Set으로 유지합니다.
6. 정규 대상이 생긴 Candidate 관계는 `prerequisite`, `recommended_before` 또는
   `related_to`의 정확한 Unit 버전으로 변환합니다.
7. accepted·merged·정규 Set·Resource 또는 기존 정규 Unit 근거가 있는 node만
   canonical로 확정합니다. deferred 전용 node는 provisional로 유지합니다.

## 중단조건

- 기존 정규 ID의 삭제·개명·실질 병합이 필요합니다.
- 학습성과와 검증 방식이 충돌하여 정규 대상을 하나로 결정할 수 없습니다.
- 고위험 후보를 독립 QA 없이 제외하거나 깊이를 낮춰야 합니다.
- 스키마·참조·DAG·공개 경계 검증이 실패합니다.

## 완료조건

- Candidate 제목·정규명·alias·제안 ID 충돌이 0건이거나 직접 대상이 기록됩니다.
- Wave 1 승인 후보 7개 Unit·7개 Reference·1개 Set이 정규 등록됩니다.
- 정규화 가능한 pending 관계가 정확한 Unit 버전 관계로 전환됩니다.
- canonical 107개와 provisional 3개의 근거가 문서화됩니다.
- 기존 ID 삭제·개명·연쇄 중복이 0건입니다.
