# 평가 계약: wp.organization-adoption.breadth-a

## 공통 원칙

- 합성 조직도·역할·업무·skill·survey·학습·지원·adoption event fixture와
  삭제 가능한 local sandbox만 사용합니다.
- 실제 직원·지원자·고객의 개인정보·성과·감정·건강·생체·행동 telemetry,
  운영계정·예산·조달·계약·외부 target은 사용하지 않습니다.
- 실행 전에 목적·이해관계자·영향·위험등급·owner·참여·이의제기·지원·
  중단·rollback·보유·cleanup·정답표를 봉인합니다.
- safety manifest에는 `wall_clock_timeout_seconds≤300`,
  `max_records≤10000`, `max_fixture_bytes≤10485760`,
  `max_groups≤100`, `minimum_reportable_group_size≥10`,
  `max_report_queries≤20`, `max_dimensions_per_report≤2`,
  `complementary_suppression=true`,
  `max_survey_items≤50`, `max_learning_events≤10000`,
  `actual_spend=0`, `allowed_targets=local·새 임시 sandbox`를 기록합니다.
- 소규모 집단·교차표·중첩 집단·반복 질의의 differencing 가능 결과는
  complementary suppression으로 억제하고 개인 row·ranking·punitive score를
  출력하지 않습니다.
- 자유서술·채팅·행동에서 sentiment·감정·의도·건강·노조활동·보호속성을
  추론하지 않습니다.
- 설문·참여에는 자발성, 불참 불이익 금지, 관리자 개인응답 접근 금지,
  비보복, 이의제기·철회 경로를 요구합니다.
- checklist 완료·교육 참석·로그인 수만을 도입 성공이나 업무성과의 대리
  지표로 사용하지 않습니다.
- qualified HR·노무·법무·보안·privacy·재무·조달 owner의 실제 판단을
  학습 결과가 대체하지 않습니다.
- 전문판단 이관은 `status=needs_qualified_review`,
  `review_domains=[hr|labor|legal|security|privacy|finance|procurement|accessibility]`,
  `owner`, `reason`, `missing_evidence`, `resume_condition`을 모두 요구합니다.
- 평가 종료 시 synthetic raw row·event는 0건이어야 합니다. 보존 evidence는
  집계·비식별 필드만 허용하며 `purpose`, `owner`, `access`, `expiry`,
  `hash`를 기록합니다.

## 공통 재현성 Gate

- 각 후보는 `candidate.<id>.fixture@1.0.0`을 사용하고 D0 분류 12사례의
  오답 `0/12`, 주입 결함 `6/6` 탐지·처리와 후보별 고정 제출 JSON의
  필수 필드·참조 무결성을 요구합니다.
- 같은 입력으로 독립 sandbox에서 2회 평가한 canonical result hash가 같고
  추가 mutation·잔여 임시자원은 각각 0건이어야 합니다.
- 초기·최종 sandbox manifest가 일치하고 cleanup 대상 밖의 sanitized
  evidence hash가 유지되어야 합니다.
- 실제 fixture·runner 구현은 Phase 2 `cataloged` 승격이 아니라 Unit
  활성화 전 별도 필수 Gate입니다.

## 조직 도입 공통 Gate

- 업무·역할·역량·학습·지원·도입·성과·위험·분배효과를 서로 다른 측정
  단위로 구분합니다.
- 이해관계자·영향·owner·참여·feedback·이의제기·지원·중단 경로의 누락을
  봉인 matrix와 대조합니다.
- adoption 선행지표와 quality·risk·cycle time·outcome 후행지표를 연결하되
  인과효과는 적절한 비교설계 없이 주장하지 않습니다.
- training completion과 실제 업무 전이·성과를 구분하고 transfer task와
  유지·지원·재평가 trigger를 포함합니다.
- pilot·확대·중단 결정은 기술·보안·privacy·운영·사람 영향 Gate 중 하나라도
  실패하면 `not-ready` 또는 `needs_qualified_review`로 처리합니다.
- 특정 집단에 불리한 분배효과·접근성·부담·직무 영향은 평균값에 묻지 않고
  최소 집단크기를 충족할 때만 집단 수준으로 보고합니다.

## 중단조건

- 실제 개인·민감·성과 데이터나 개인별 surveillance·ranking이 필요합니다.
- 인사·노무·고용·보상·징계·조달·계약 결론을 자동화해야 합니다.
- 최소 집단크기·억제·보유·삭제·이의제기·지원 기준이 없습니다.
- 실제 조직·외부 시스템·예산·권한을 변경해야 합니다.
- 봉인 manifest·결정적 answer key·rollback·cleanup 기준이 없습니다.
