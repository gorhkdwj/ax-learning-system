# 실용성·안전 독립 감사: wp.organization-adoption.breadth-a

## 범위

- Candidate 10개의 D0·D2·제한 D3 산출물·정량 Gate
- 합성 fixture·sandbox·멱등성·cleanup·evidence 보존
- 소집단·differencing 방지, 설문 참여 안전, qualified review 이관
- lifecycle Set의 blocking·transfer 평가계약

## 1차 결과와 교정

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 5개 공통 안전계약 범주 |

다음을 공통 계약에 반영했습니다.

1. `max_report_queries≤20`, `max_dimensions_per_report≤2`와
   complementary suppression을 고정했습니다.
2. 자유서술·채팅·행동에서 감정·의도·건강·노조활동·보호속성 추론을
   금지했습니다.
3. 설문·참여의 자발성, 불참 불이익 금지, 관리자 개인응답 접근 금지,
   비보복, 이의제기·철회 경로를 요구했습니다.
4. `needs_qualified_review`의 review domain·owner·reason·missing evidence·
   resume condition을 기계 판정 가능한 필드로 고정했습니다.
5. 평가 종료 후 synthetic raw row·event 0건과 보존 evidence의 목적·owner·
   access·expiry·hash를 요구했습니다.

## 최종 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |

- 후보별 fixture 1.0.0, D0 12사례 오답 0건, 결함 6/6 탐지·처리와 고정
  JSON 산출물 3개를 요구합니다.
- 독립 sandbox 2회 canonical hash 일치, 추가 mutation·잔여자원 0건과
  초기·최종 manifest 일치를 요구합니다.
- Set은 필수 또는 applicable conditional Gate 하나라도 실패하면
  `not-ready`이며 transfer 6사례의 허용 오류는 0/6입니다.
- 실제 fixture·runner는 모든 후보에서 `required_before_activation`입니다.

## 결론

실용성·안전 기준으로 Candidate 10개 모두 Phase 2 `cataloged` 승격을
승인합니다.
