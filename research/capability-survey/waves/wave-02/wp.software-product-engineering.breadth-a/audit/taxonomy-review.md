# Taxonomy 감사: wp.software-product-engineering.breadth-a

## 범위와 방법

- 대상: Candidate 10개, `taxonomy.ax-capability-map@0.4.0`, 기존 정규
  Unit·Set·Signal과 Wave 2 Candidate
- 감사 역할: 발견 조사자와 분리된 읽기 전용 독립 taxonomy 감사자
- 확인: Unit·Set 목적지, item type, 중복·소유권 경계, relation 방향·버전·DAG
- 감사일: `2026-07-28`

## 최초 판정

| 항목 | 결과 |
|---|---:|
| P0 | 0 |
| P1 | 5 |
| P2 | 3 |

## P1 교정

- 업무 조합인 `ai-assisted-software-change-delivery`를 역량 node에서 제거하고
  AI 보조 Set이 실제 구성 역량 4개를 참조하도록 했습니다.
- 버전관리·API·관계형 스키마 후보의 item type을 제품·기술이 아닌
  `practice`로 통일했습니다.
- 일반 AI 보조 여부의 효과와 기존 `signal.agent.agent-harness`의 harness
  구성효과 비교 경계를 Candidate와 평가계약에 명시했습니다.
- AI 보조 Set에 `responsible-use-boundaries@1.0.0` 선행관계를 추가했습니다.
- 일반 HTTP API와 모델향 AI tool contract의 소유권 경계를 taxonomy에
  명시했습니다.

## 추가 개선

- 접근 가능한 UI 후보에 계층형 검증 후보를 권장 선수관계로 연결했습니다.
- AI 보조 Set에 빌드·의존성 재현성 후보를 권장 선수관계로 연결했습니다.
- 요구사항 후보와 taxonomy node에서 사업 가치 프레이밍 및 일반 사용자의
  AI 과업 프레이밍을 제외했습니다.

## 결론

독립 재감사 결과 최종 P0 0건, P1 0건입니다. 잠정 소프트웨어 하위 node는
정확히 9개이며 관계 버전·방향이 유효하고 DAG 순환이 없습니다. 최종 라우팅은
Unit 후보 9개와 Set 후보 1개이며 merge·defer 권고는 없습니다.
