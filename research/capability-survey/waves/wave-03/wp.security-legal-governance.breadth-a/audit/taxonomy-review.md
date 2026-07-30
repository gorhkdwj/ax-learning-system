# 분류 독립 감사: wp.security-legal-governance.breadth-a

## 범위

- 신규 Candidate 10개, 기존 Candidate 76개와 정규 Unit·Set 전수 대조
- ID·표시명 충돌, Unit·Set 판정, subdomain 소유권, 후보 DAG와 기존 관계
- taxonomy 0.9.0 부모·상호관계·누락

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 7개 교정군 |

다음을 교정했습니다.

1. 보안사고 후보를 기존 플랫폼 사고대응과 분리해 증거보존·신고의무 검토
   이관 D2로 축소했습니다.
2. 개인정보 후보에 처리·권리 register와 DPIA packet Gate를 함께 고정했습니다.
3. IAM 범위를 authentication이 아닌 authorization 접근정책·권한 수명주기로
   좁혔습니다.
4. IP subdomain을 저작권·license·권리 provenance 범위로 축소했습니다.
5. 패키지 내부 recommended prerequisite·related·requires DAG를 추가했습니다.
6. AI 거버넌스 Set의 필수 7개 Unit과 applicability 조건부 2개 Unit을 exact
   version·blocking rule로 연결했습니다.
7. 신규 subdomain의 `related_ids`를 실제 기존·신규 소유 경계로 정밀화했습니다.

## 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |

- 9개 Unit 후보와 1개 Set 후보 분할이 적합합니다.
- taxonomy는 `taxonomy.ax-capability-map@0.9.0`으로 정상 bump되었습니다.
- schema·참조·ID·부모·순환 오류와 교정 전 subdomain 참조는 0건입니다.

## 결론

최종 P0·P1은 0건입니다. 기존 Set과의 cross-link는 정규 승격 후 optional
overlay 보강 대상으로 남기며 이번 후보 소유권을 바꾸지 않습니다.
