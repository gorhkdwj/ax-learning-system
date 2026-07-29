# 근거 독립 감사: wp.integration-automation.breadth-a

## 감사 범위

- Candidate 10개 전수
- 근거 제목·발행자·URL·version·조회일
- 정의·범위·D0/D2·위험·업무 관련성 주장과 실제 근거의 대응
- 표준이 보장하지 않는 동작의 과대 일반화 여부

감사자는 파일을 수정하지 않았고 Codex 메인 세션만 판정과 교정을 반영했습니다.

## 1차 결과

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 6 |
| P2 | 4개 유지관리 묶음 |

P1은 후보 삭제나 범위 전면 재설계가 아니라 직접 근거와 주장 한계를 맞추는
교정이었습니다.

| 후보 | 1차 판정 | 교정 |
|---|---|---|
| 외부 API 소비자 통합·복원력 | fix | RFC 6585를 추가하고 pagination·cursor 의미는 제공자 계약별 입력임을 명시 |
| SaaS 커넥터 동기화 전달 | fix | Microsoft Graph delta query와 Google Calendar incremental sync 공식 사례 추가 |
| 결정적 워크플로 상태·오케스트레이션 | fix | durable checkpoint·recovery 구현 사례와 Adapter별 persistence 경계 추가 |
| 자동화 결과관측·상태조정 | fix | RFC 9110의 202 Accepted와 Arazzo success criteria·output 근거 추가 |
| UI 구동 업무자동화·변경내성 | fix | WebDriver `2026-07-02` dated URL 고정, WAI-ARIA와 Adapter locator 경계 추가 |
| MCP 프로토콜 연결 Adapter | fix | MCP Tools와 Resources 문서를 정확한 제목·URL로 분리 |

나머지 이벤트·웹훅, 부작용 안전성, 비즈니스 규칙, 결정적·agent 경계 Resource의
근거는 1차 감사에서 `accept` 판정을 받았습니다.

## 재감사

| 심각도 | 건수 |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 6개 유지관리 권고군 |

10개 Candidate 모두 근거 Gate를 통과했습니다. 남은 P2는 다음과 같습니다.

- 변경 가능한 공식·실무 자료의 release·발행일·갱신일을 상세화 시 더 강하게 고정
- NIST SP 800-92 후속 개정 상태 모니터링
- WebSub 서명 존재를 안전성 보증으로 확대 해석하지 않는 경계 유지
- poison 격리와 전체 순서는 표준 보장이 아닌 local fixture 정책으로 유지
- 조회일로 기록한 일부 공식 문서의 실제 revision을 정규 승격 전에 보강
- WebDriver Working Draft와 Adapter별 locator 동작을 구현 시 재확인

## 검증

- `python tools/validate_catalog.py`: 오류 0건, 경고 0건
- `python tools/check_public_boundary.py`: 오류 0건
- `git diff --check`: 통과

`taxonomy/taxonomy.json`의 CRLF→LF 안내는 내용 오류나 diff 검사 실패가
아닙니다.
