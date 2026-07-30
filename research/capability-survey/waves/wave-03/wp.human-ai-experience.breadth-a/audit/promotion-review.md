# 정규 승격 감사: wp.human-ai-experience.breadth-a

## 범위와 방법

- 대상: accepted Candidate 8개에서 승격한 정규 Unit 6개, 공개 Reference
  6개와 기존·신규 Unit이 소유하는 D0 경계 Resource 2개
- 제외: 장기 memory lifecycle 직접 근거가 부족한 deferred Candidate 1개
- 감사 역할: 승격 작성과 분리된 읽기 전용 근거·taxonomy·실용성 감사자
- 확인: Candidate→정규 항목 추적, 출처·일반화 제한, ID·관계·owner 역참조,
  D0·D2 성과·평가계약, 합성 fixture·전문 이관과 미검증 상태
- 감사일: `2026-07-30`

## 승격 전 재검수

기존 패키지를 정규화하기 전에 Candidate 9개를 다시 전수검수했습니다.
accepted Candidate 8개의 `decision.rationale`과 `review.next_action` 총
16개 필드에 실제 `?` 문자 손상이 있음을 발견해 UTF-8 한국어로 교정했습니다.
교정 후 세 독립 감사에서 P0·P1 0건을 확인한 뒤에만 승격을 시작했습니다.

## 승격 후 1차 결과

| 심각도 | 결과 |
|---|---:|
| P0 | 0 |
| P1 | 4개 교정군 |

P1은 다음과 같이 처리했습니다.

1. 정규 D0 Resource 두 개의 description에 남은 후보 표현을 정규 가이드
   표현으로 교정했습니다.
2. 의인화 Resource에 미국 성인 2,165명·pseudo-LLM·단기·text/speech·
   1인칭 단서라는 근거 범위와 일반화 금지·전문 이관을 보존했습니다.
3. Unit 6개에 공통 정상·오류·거부·무응답·지연·변경·접근성 시나리오,
   사전 정답 manifest·실패 목록·관찰 protocol, 실제 데이터·계정·고위험
   변경 중단과 실제 참여자 동의·비식별·최소 수집 Gate를 추가했습니다.
4. 대화복구는 clarification·repair 최대 3회 후 대안 또는 인간 도움으로
   이관하고, D0 Resource의 30분은 공개 Reference 검토 가설로 교정했습니다.

## 최종 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| 정규 Unit | 6 |
| 공개 Reference | 6 |
| D0 경계 Resource | 2 |
| 승격 제외 deferred Candidate | 1 |

- Unit outcome과 판정 기준은 Candidate D0·D2 outcome·evidence hypothesis를
  보존하고 공통 평가계약을 추가했습니다.
- 출처 제목·발행자·유형·URL·버전·claim scope는 정규 sources와
  `extensions.evidence_claims`에 보존했고 승격 재확인일은 `2026-07-30`입니다.
- Resource owner와 Unit `resource_refs`는 양방향으로 일치합니다.
- `requires`는 `prerequisite`와 명시적 D2 수준으로,
  `recommended_prerequisite`는 `recommended_before`로 변환했습니다.
- 접근 가능한 다중양식 Resource는 기존
  `unit.software.accessible-ui-state-interaction@1.0.0`이 소유합니다.
- 사회적 단서·의인화 Resource는 신규 기대형성·온보딩 Unit이 소유하며
  일반 신뢰 보정 Unit과의 관계를 유지합니다.
- 실제 계정·secret·개인정보·결제·삭제·고위험 외부 변경은 요구하지 않습니다.
- 개인화·기억 Candidate와 provisional node는 조사 공백으로 유지하며 정규
  Unit·Resource·Set과 `promoted_from` 경로를 만들지 않았습니다.

## 잔여 P2

- 공개 Reference의 검증은 `partial`, 접근성은 `unverified`입니다.
- 예상 시간은 prebuilt fixture·prototype 또는 30분 D0 Reference 검토
  가설이며 실제 파일럿으로 확인해야 합니다.
- 상세 교재·독립 평가 타당성·접근성·학습효과와 업무효과는 검증하지 않았습니다.

## 결론

승격 전·후 이중 검수의 최종 P0·P1은 0건이며 정규 `cataloged` 승격을
승인합니다. 이 판정은 상세 콘텐츠·파일럿·학습효과 또는 규제 적합성 검증
완료를 뜻하지 않습니다.
