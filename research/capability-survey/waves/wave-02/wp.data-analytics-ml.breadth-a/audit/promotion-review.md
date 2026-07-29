# 정규 승격 감사: wp.data-analytics-ml.breadth-a

## 범위와 방법

- 대상: 신규 Candidate 9개, 기존 영향평가 Candidate 1개에서 승격한 정규
  Unit 10개와 공개 Reference 10개
- 감사 역할: 승격 작성과 분리된 읽기 전용 독립 감사자
- 확인: Candidate→Unit·Resource 추적, ID·관계 변환, D0·D2 성과·검증 정렬,
  출처 보존, Taxonomy·DAG·스키마와 범위 과대승격
- 감사일: `2026-07-29`

## 최종 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 3 |

- 신규 후보 9개와 기존 영향평가 후보 1개가 정확히 Unit 10개와 Reference
  10개로 연결되었습니다.
- `requires`는 `prerequisite`, `recommended_prerequisite`는
  `recommended_before`로 변환했고, 승격 대상 관계는 정확한 Unit ID와
  `1.0.0` 버전을 참조합니다.
- 아직 정규화되지 않은 `measurement-contract` 3건과
  `solution-fit-assessment` 1건은 원 type·ID·version·rationale를
  `pending_candidate_relations`에 보존했습니다.
- D0·D2 학습성과, 범위 상한, 성공기준과 모든 근거 출처는 Candidate와
  일치하며 신규 선수관계 DAG에 순환이 없습니다.

## P2 추적

- 상세 평가 제작 시 현재 단일 `manual` 검증을 D0 판정과 숨은 fixture·봉인
  test·자동검출 기반 D2 검사로 분리합니다.
- 공통 평가계약의 비용 한도, 승인 거부·무응답, 원본 보존과 외부 변경 0건을
  정규 평가 Resource로 이관합니다.
- HUB·교재 생성 시 Reference의 첫 `location.url`뿐 아니라
  `provenance.sources` 전체를 노출합니다.

## 결론

최종 P0·P1은 0건이며 정규 `cataloged` 승격을 승인합니다. 이 판정은 상세 교재,
독립 평가 타당성, 학습효과 또는 업무효과 검증 완료를 뜻하지 않습니다.
