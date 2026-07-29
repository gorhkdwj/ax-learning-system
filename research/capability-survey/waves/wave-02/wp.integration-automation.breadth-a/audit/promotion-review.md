# 정규 승격 감사: wp.integration-automation.breadth-a

## 범위와 방법

- 대상: Candidate 10개에서 승격한 핵심 Unit 7개, MCP technology Adapter
  역할의 `protocol` Unit 1개, 공개 Reference 8개, D0 경계 Resource 1개와
  SaaS 프로젝트 Set 1개
- 감사 역할: 승격 작성과 분리된 읽기 전용 독립 감사자
- 확인: Candidate→Unit·Resource·Set 추적, ID·관계 변환, D0·D2
  성과·검증 정렬, 출처 보존, Resource 역참조, Set DAG·선수요건,
  Taxonomy·스키마·공개 경계와 범위 과대승격
- 감사일: `2026-07-29`

## 최종 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2개 범주의 후속 검증 |

- Candidate 10개는 Unit 8개, Reference 8개, D0 경계 Resource 1개와
  SaaS Set 1개로 정확히 추적됩니다.
- `requires`는 `prerequisite`, `recommended_prerequisite`는
  `recommended_before`, `related_to`는 `related_to`로 변환했으며 중복과
  누락이 없습니다.
- 외부 API 소비 Unit의 기존 API 계약 관계는 정규
  `unit.software.api-contract-compatibility@1.0.0` 선수요건 하나로
  중복 제거했습니다.
- Candidate의 D0·D2 outcome과 판정 가설, 근거의 제목·발행자·URL·확인일·
  버전을 정규 항목과 Reference에 보존했습니다.
- Candidate 스키마의 `practitioner_primary` 출처는 정규 Unit·Resource
  스키마가 허용하는 `official_source`로 변환하고 해당 정규화 사실을
  `extensions.source_type_normalizations`에 기록했습니다.
- Resource owner와 Unit `resource_refs` 역참조가 일치하며 SaaS Set은 요구한
  5개 Unit과 기존 API 계약 선수요건을 포함하고 DAG 순환이 없습니다.
- MCP Adapter는 `item_type: protocol`인 D2 Unit으로 등록하되
  `extensions.artifact_role: technology_adapter`와 고정 사양 버전을
  보존했습니다.
- 실제 계정·secret·절대경로·비공개 자료는 발견되지 않았습니다.

## P2 추적

- 공개 Reference의 `verification.status`는 `partial`,
  `accessibility.status`는 `unverified`입니다. URL·근거 범위만 검토했으며
  상세 교재의 완전성, 평가 타당성과 접근성은 후속 검증이 필요합니다.
- SaaS Set의 업무효과 근거는 `hypothesis` 단계이고 모든 정규 항목은 상세
  fixture·파일럿·학습효과 미검증 상태를 명시합니다.

## 검증

- `python tools/validate_catalog.py`: 오류 0건, 경고 0건
- `python tools/check_public_boundary.py`: 오류 0건
- `git diff --check`: 통과

## 결론

최종 P0·P1은 0건이며 정규 `cataloged` 승격을 승인합니다. 이 판정은 상세
교재·독립 평가 타당성·접근성·파일럿·학습효과 또는 업무효과 검증 완료를
뜻하지 않습니다.
