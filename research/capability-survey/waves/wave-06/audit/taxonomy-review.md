# 분류 독립 감사: wp.independent-qa.stratified-a

## 범위

- QA Register 56개와 Candidate 96개의 ID·명칭·alias·목적지
- canonical 107개·provisional 3개 taxonomy node의 부모·참조·중복
- Wave 5 신규 Unit 7개·Reference 7개·Set 1개의 관계·수준·구성

## 1차 결과와 교정

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 1개 provenance 범주 |
| P2 | 1개 역할 representation 범주 |

Wave 5 정규화 문서가 보존한다고 선언한 Candidate 관계가 신규 전략 Unit 7개에
없었습니다. 각 Candidate 최상위 `relations`를 Unit의
`extensions.source_candidate_relations`에 exact-copy했습니다. 정규 관계와
포트폴리오의 편익 실현 pending 관계는 변경하지 않았습니다.

## 최종 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 1 |

- 원천 관계 수 0·0·1·2·2·4·2개가 구조와 순서까지 일치합니다.
- 정규 관계 변환은 정확하며 편익 실현 Candidate 1개만 pending입니다.
- Candidate·taxonomy·목적지 충돌, 부모 불일치와 활성 참조 오류는 0건입니다.
- 잔여 P2는 개발 중심 planned view 3개 외 역할 view가 없는 공백이며 Wave 7의
  8개 역할 관점 조립으로 라우팅합니다.

## 결론

분류·관계·Set 조합 기준으로 Wave 7 진행을 승인합니다.
