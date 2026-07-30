# 승격 후 독립 재감사: wp.security-legal-governance.breadth-a

## 승격 결과

- accepted Candidate: 10개
- 정규 Unit: 9개
- Unit 소유 공개 Reference: 9개
- 정규 Set: 1개

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 2개 수준 불일치 |
| P1 | 2개 추적 마감 범주 |

P0는 AI 거버넌스 Set이 최대 D2인 AI 시스템 평가·Human-AI 승인 Unit에 D3를
요구한 문제였습니다. 두 step을 D2로 내리고, 실제 산출물을 필요로 하면서 D0만
요구하던 기반 Unit 네 step은 D2로 올렸습니다. 모든 step의 `required_level`이
참조 Unit의 `maximum_scope_level` 이하인지 다시 전수 확인했습니다.

P1은 Candidate의 보안 위험 Unit 권고 선수관계가 Set schema의 일반 관계 부재로
누락된 문제와 manifest·checkpoint·candidate `next_action`이 승격 전 상태에
남은 문제였습니다. Set extensions에 권고 선수관계와 원 Candidate 관계를
보존하고 tracking 문서를 `promoted`로 동기화했습니다.

## 추가 교정

- Set 9개 step의 `validation_gate_ids`를 실제 참조 Unit의 required Gate에
  연결했습니다.
- structured `sealed_assessment_contract`를 모든 신규 Unit과 Set에 보존했습니다.
- Set은 필수 Unit 7개와 applicability 조건부 Unit 2개의 exact version·수준·
  blocking rule을 보존합니다.
- transfer 평가를 6사례·오류 0/6·동일 제출 artifact로 고정했습니다.
- 중복된 `evidence evidence` 산출물 문구를 교정했습니다.

## 최종 재감사

| 축 | P0 | P1 |
|---|---:|---:|
| 근거 | 0 | 0 |
| taxonomy·관계·추적 | 0 | 0 |
| 실용성·안전 | 0 | 0 |

`promoted_from`, 후보·정규 evidence claim, Unit 관계 방향, Set DAG·수준·
필수/조건부 구성과 평가계약이 일치합니다. 상세 fixture·runner·학습효과·실제
조직 적합성은 `required_before_activation` 후속 Gate이며 이번 승격 완료를
의미하지 않습니다.
