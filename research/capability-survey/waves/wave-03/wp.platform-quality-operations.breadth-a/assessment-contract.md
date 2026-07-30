# 평가 계약: wp.platform-quality-operations.breadth-a

## 공통 원칙

- 평가는 local simulator, 공개·합성 입력, synthetic telemetry, sealed
  incident·cost fixture와 삭제 가능한 sandbox만 사용합니다.
- 실제 production·cloud·SaaS 계정, 자격증명, 개인정보, 결제, 운영 알림,
  외부 배포·삭제·장애 유발은 사용하지 않습니다.
- 실행 전 기준 artifact·desired state·SLI·비용·복구 정답 manifest,
  실패 주입 목록, 시간·요청량·비용 상한과 중단·rollback 절차를 고정합니다.
- 봉인 safety manifest에는 `wall_clock_timeout_seconds≤300`,
  `max_requests≤10000`, `max_concurrency≤16`,
  `max_retries_per_request≤2`, `max_fault_injections≤10`,
  `max_fixture_bytes≤10485760`을 항상 적용하고 record형 입력에는 추가로
  `max_records≤10000`을 적용하며,
  `actual_spend=0`, `allowed_targets=loopback·새 임시 sandbox`, abort trigger와
  rollback·restore·cleanup invariant를 기록합니다. runner는 하나라도
  위반하면 즉시 중단합니다.
- 도구 명령 성공을 사용자 영향, 최종 상태, 복구 무결성 또는 비용효과의
  대리 지표로 사용하지 않습니다.
- 실제 incident·운영효과·조직 성과로 일반화하지 않고 formative fixture
  평가로 제한합니다.

## D0 공통 Gate

- build 재현성과 배포 가능한 artifact provenance를 구분합니다.
- 로그·metric·trace와 사용자 관점 SLI·SLO·alert를 구분합니다.
- 장애 이벤트, 보안 incident, 서비스 incident와 재해복구를 구분합니다.
- backup 존재, restore 성공, RTO·RPO와 업무 복구를 구분합니다.
- 평균 성능, tail latency, 용량 한계와 과부하 보호를 구분합니다.
- 청구 총액, 사용량 할당, unit economics와 업무가치를 구분합니다.
- coverage-only 경계로 공용 도구 모음과 사용자 중심 내부 플랫폼을 구분하되
  이번 패키지의 독립 후보로 승격하지 않습니다.
- 기능 변경, patch·EOL, toil 제거와 운영 유지보수를 구분합니다.

## D2·제한 D3 공통 Gate

- 변경·오류·지연·부분실패·drift·rollback·restore·과부하 시나리오를
  사전 고정된 상한 안에서 주입합니다.
- 의도·실행·관찰·검증·복구 상태와 상관 ID를 남기고 최종 상태를 재조회합니다.
- alert는 사용자 영향·error budget·행동 가능성과 연결하고 무의미한
  duplicate·flapping·누락을 기록합니다.
- 복구는 원본을 덮어쓰지 않는 격리 경로에서 수행하고 manifest·무결성·
  RTO·RPO 결과를 검증합니다.
- 부하는 local fixture의 제한된 요청량·시간으로 실행하고 중단조건과
  시스템 보호가 작동해야 합니다.
- 공통 300초 제한은 제출 artifact를 검사하는 자동 runner와 각 simulator
  실행에 적용합니다. 사람 tabletop은 별도 `exercise_duration_minutes`와
  `max_event_steps`를 봉인해 제한합니다.
- 비용은 합성 청구·사용량 fixture로 분석하고 실제 지출·구매·예약 변경을
  수행하지 않습니다.
- 실제 운영 권한·고위험 변경·법적 통제·보안 사고가 필요하면 중단하고
  해당 전문 소유 영역으로 이관합니다.

## 중단조건

- 실제 운영환경·조직 on-call·고객·개인정보·유료 자원을 사용해야 합니다.
- 격리·rollback·restore 또는 비용·부하 상한을 고정할 수 없습니다.
- 실제 장애·데이터 손실·보안 사고·법적 신고를 재현해야 합니다.
- 특정 공급자 수치나 사례를 보편적인 운영 기준으로 일반화해야 합니다.
- 복구·비용·성능·SLO 결과를 자동검증할 정답 manifest가 없습니다.
- 봉인 safety manifest 필드를 채울 수 없거나 runner가 상한을 강제하지 못합니다.
