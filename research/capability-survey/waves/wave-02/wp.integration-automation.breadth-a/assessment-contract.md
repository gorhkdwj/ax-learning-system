# 통합·업무자동화 D2 평가 계약

## 공통 원칙

- 과목명과 산출물 표시는 한국어를 우선하고 protocol·node·기술 ID는 영문을
  병기할 수 있습니다.
- 요구사항, 입력·출력 schema, 상태·오류 종류, 승인 정책, 실행 한도는 학습자에게
  공개합니다. 평가용 fixture에서는 결함 위치와 최종 정답만 숨깁니다.
- 모든 실행은 저장소 안의 fake service·local test UI·제공된 test key로
  제한합니다. 실제 계정·토큰·개인정보·결제·외부 메시지·고위험 변경을
  사용하지 않습니다.
- 각 fixture는 호출 횟수, retry 횟수, 누적 대기, wall-clock, 처리 건수와
  허용 비용을 manifest로 고정합니다. 한도를 넘기면 추가 실행을 중단하고
  `판단 불가` 또는 인간 이관으로 처리합니다.
- 무제한 retry·polling·workflow·agent loop를 허용하지 않습니다. 종료조건,
  timeout, cancel과 재개 지점을 명시합니다.
- 성공은 API 응답이나 UI click 자체가 아니라 외부 상태를 다시 읽어 확인한
  postcondition과 correlation 가능한 실행 증거로 판정합니다.
- 쓰기·삭제·발송·승인 같은 외부 효과는 명시적 승인 전에 실행하지 않습니다.
  승인 거절·취소·무응답 fixture에서는 외부 상태변경 0건, 원본 보존과 감사
  기록을 확인합니다.
- 자동검사만으로 끝내지 않고 안전성 주장, 상태 불확실성, 경계 선택과 실패 후
  이관 판단을 사람이 함께 검토합니다.
- 보안·개인정보·법률 정책의 정답을 추정하지 않습니다. 제공된 정책·권한·보존
  제약이 없으면 실행하지 않고 전문 검토로 이관하는 것을 올바른 결과로 봅니다.

## 공통 D2 Gate

다음 Gate는 D2 Unit·Set·Adapter 후보에 적용하며 D0 경계 Resource에는 적용하지
않습니다.

1. 입력·출력·상태·오류·부작용·승인·종료 계약을 실행 전에 선언합니다.
2. 정상, 경계, 부분실패, 중복, 지연, 순서변경과 불확실 결과 fixture를
   구분합니다.
3. 같은 입력·초기상태·구성에서 허용된 결과집합과 trace를 재현합니다.
4. 모든 외부 변경에는 business idempotency key 또는 동등한 중복 방지
   근거가 있습니다.
5. transport retry와 업무 부작용 재실행을 분리하고 각 횟수·대기를 제한합니다.
6. 실행·step·attempt·외부 객체를 연결하는 correlation 증거를 남깁니다.
7. postcondition 재조회로 누락·중복·잘못된 성공을 검출하고 조정 필요성을
   판정한 뒤 부작용 안전성 계약 또는 인간 이관으로 연결합니다.
8. 승인 거절·취소·timeout에서는 추가 부작용 없이 종료하며 재개 가능 지점을
   기록합니다.
9. 입력에 없는 성공·정책·권한·보상을 임의로 만들지 않습니다.

## 후보별 fixture

### 외부 API 소비자 통합·복원력

- fake API가 cursor pagination, `429 Retry-After`, `5xx`, timeout, malformed
  problem detail과 비호환 response를 순서대로 주입합니다.
- 학습자는 명세와 응답을 구분해 오류를 분류하고 retry·대기·호출 한도 안에서
  수집을 끝내거나 안전하게 중단합니다.
- 페이지 누락·중복 0건, quota 위반 0건, 업무 부작용 중복 0건과 최종 상태
  manifest 일치를 확인합니다. transport retry는 business idempotency와
  별도 항목으로 채점합니다.

### 이벤트·웹훅 전달계약 검증

- 제공된 fake key와 local callback으로 정상 서명, 잘못된 서명, duplicate,
  out-of-order, replay, 지연과 poison message를 주입합니다.
- 수신 확인과 업무 처리 완료를 분리하고 event ID·timestamp·signature·delivery
  attempt를 검증합니다.
- 유효 이벤트는 한 번만 반영되고 무효·replay·poison 입력은 격리되며, ack와
  처리 결과가 정답 manifest와 일치해야 합니다.

### SaaS 커넥터 동기화 전달

- 서로 다른 pagination·token·cursor·delete·conflict 규칙을 가진 fake SaaS
  두 개와 봉인된 최종 상태 manifest를 제공합니다.
- API 소비, event 수신, workflow 상태, 부작용 안전성, 결과판정 Gate를
  조합하되 제품별 click 절차는 평가하지 않습니다.
- 반복 실행 후 양쪽 상태가 계약대로 수렴하고 누락·중복·의도하지 않은 삭제가
  없으며 unresolved conflict는 자동 은폐하지 않고 이관해야 합니다.

### 결정적 워크플로 상태·오케스트레이션

- 상태표와 event·timer·approval 계약을 공개하고 crash, timeout, duplicate
  signal, 병렬 join, 승인 거절과 cancel fixture를 제공합니다.
- 학습자는 상태전이를 명시하고 중간 checkpoint에서 재개해 동일 완료 상태 또는
  명시된 실패·이관 상태에 도달합니다.
- 종료되지 않는 실행 0건, 완료 단계 재실행 0건, 승인 전 외부 효과 0건과
  상태전이 trace 일치를 확인합니다.

### 부작용 안전성·멱등성·재시도·보상

- fake ledger에 response loss, partial success, duplicate·concurrent request,
  late completion과 compensation 실패를 주입합니다.
- 같은 업무 요청의 transport 재전송과 실제 부작용 중복을 구분하고 불확실
  상태에서는 결과검증 판정을 먼저 받은 뒤 retry·보상·수동복구를 실행합니다.
- 중복 부작용 0건을 기본 Gate로 하며, 자동 판정할 수 없는 상태는 추가 변경
  없이 `unresolved`와 인간 이관 증거를 남겨야 합니다.

### 비즈니스 규칙·의사결정표 자동화

- 입력·출력·모든 규칙·우선순위·hit policy·version은 공개하고 경계값, 충돌,
  미일치와 다중일치 평가 case만 봉인합니다.
- 학습자는 규칙을 코드와 분리해 검증하고 각 결정에 사용한 table version,
  matched rule과 입력 snapshot을 남깁니다.
- 기대 결정·충돌·미일치 판정이 manifest와 일치하고 임의 default 결정은
  0건이어야 합니다.

### 자동화 결과관측·상태조정

- `202 Accepted`, 지연 적용, log 유실, out-of-band 변경과 중복 callback을
  주입합니다.
- 응답·log만으로 성공을 선언하지 않고 correlation ID로 실제 외부 상태와
  의도 postcondition을 다시 조회합니다.
- 누락·불일치를 검출해 제한된 재조회 후 `일치`, `조정 필요`, `판단 불가·이관`
  중 하나로 판정하고 잘못된 성공 판정 0건을 확인합니다. retry·보상·수동복구
  실행은 부작용 안전성 평가에서 다룹니다.

### UI 구동 업무자동화·변경내성

- local test UI만 사용하며 CAPTCHA, 실제 계정·자격증명과 실외부 효과는
  포함하지 않습니다.
- delayed render, semantic locator 변경, modal, duplicate submit, session
  expiry와 이미 완료된 상태를 주입합니다.
- 고정 sleep·좌표보다 semantic role·label·state 정보를 사용하는
  Adapter locator와 조건 대기를 사용하고, 재실행 시 중복 제출 없이
  postcondition을 확인해야 합니다. 구체 locator API는 Adapter가 명시합니다.

### MCP 프로토콜 연결 Adapter

- MCP Specification `2025-11-25`를 고정하고 서로 다른 capability·상태·권한
  범위를 가진 fake server 두 개와 fake client, 공개된 protocol 요구사항과
  local test payload를 제공합니다.
- initialization 순서, protocol version·capability negotiation, schema
  validation과 연결 종료를 구현합니다.
- version·capability mismatch, 잘못된 schema, disconnect, timeout,
  connection·session 혼선과 다른 server의 resource·tool 접근 시도를 주입합니다.
  server별 실패 격리, 상태·권한 누출 0건, 제한된 재시도와 안전한 종료를
  확인합니다.

### 결정적 워크플로·에이전트 경계 가이드

- 고정 workflow, model-routed workflow, agent loop, delegated topology,
  harness의 짧은 사례와 기존 Candidate·Set·Signal 목록을 제공합니다.
- 학습자는 각 사례의 다음 행동·도구·종료를 누가 결정하는지와 상태·budget·승인
  책임을 구분하고 실제 구조 선택 과제는 `solution-fit-assessment` 또는 기존
  AI topology Set으로 라우팅합니다.
- 새 설계안을 선택·구현하거나 특정 방식의 생산성·품질 효과를 주장하는 것은
  이 D0 Resource의 평가 범위가 아닙니다.

## 후속 상세화 항목

- 정규 승격 후 각 fixture의 호출·retry·대기·시간·처리량 수치를 작은 local
  기준 실행으로 고정합니다.
- 제품별 SaaS·browser·workflow engine·MCP 구현은 안정 코어와 분리된
  Adapter·Resource에서 version과 유지보수 기한을 명시합니다.
- 실제 조직의 승인·비용·보안·개인정보 정책은 공개 예제에 복제하지 않고
  Vault 또는 배포 환경의 별도 정책 입력으로 연결합니다.
