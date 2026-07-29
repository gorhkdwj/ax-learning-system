# 실용성·평가 독립 감사: wp.integration-automation.breadth-a

## 감사 범위

- Candidate 10개의 D0·D2 또는 D0 Resource 평가 가능성
- fake·local fixture, 실제 자격증명·개인정보·외부 효과 차단
- 호출·retry·대기·비용·실행시간의 제한과 stop condition
- 승인 거절·취소·무응답, no-op, postcondition, reconciliation과 인간 이관
- 비즈니스 가치 가설의 과대 확정 여부

감사자는 파일을 수정하지 않았고 Codex 메인 세션만 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 2 |
| P2 | 1 |

P1은 다음과 같이 교정했습니다.

1. 경계 가이드의 목표 수준을 문서 사이에서 일치시켰고, 후속 taxonomy 감사에
   따라 최종적으로 기존 선택 역량을 중복하지 않는 D0 Resource로 축소했습니다.
2. MCP fixture를 서로 다른 capability·상태·권한의 fake server 두 개로
   확대하고 connection·session 혼선, 다른 server 접근 시도와 상태·권한
   누출 0건을 직접 검증하게 했습니다.

## 재감사 기준

- 외부 시스템 대신 fake API·service·ledger·SaaS·MCP server와 local test UI를
  사용합니다.
- 실제 계정·token·개인정보·결제·발송·고위험 변경을 요구하지 않습니다.
- 무제한 retry·polling·workflow·agent loop를 허용하지 않습니다.
- 승인 거절·취소·무응답은 외부 변경 0건, 원본 보존과 감사기록으로 판정합니다.
- 응답·log·click이 아니라 재조회한 postcondition으로 완료를 판정합니다.
- 근거가 없는 효과를 확정하지 않고 모든 가치 주장을 측정 가설로 유지합니다.

## 최종 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 0 |

10개 Candidate 모두 `accept` 판정을 받았습니다. 상세 fixture 구현 전 호출 수,
retry 수, 누적 대기, wall-clock, 처리량과 유료 network 비용 0의 실제 수치
상한을 fixture manifest에 고정하는 일은 후속 구현 계약으로 남겼으며 현재
Candidate 판정의 미해결 감사 이슈는 아닙니다.

## 검증

- `python tools/validate_catalog.py`: 오류 0건, 경고 0건
- `git diff --check`: 통과
