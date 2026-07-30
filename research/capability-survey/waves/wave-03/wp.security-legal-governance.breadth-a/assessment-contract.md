# 평가 계약: wp.security-legal-governance.breadth-a

## 공통 원칙

- 평가는 공개·합성 입력, fake identity·service·policy·license·incident fixture,
  synthetic secret canary, 공개 test key와 삭제 가능한 loopback sandbox만
  사용합니다.
- 실제 개인정보·기밀·credential·실제·운영 private key·운영계정·결제·외부 target
  scan·exploit·침투·삭제·통지·신고는 수행하지 않습니다.
- 실행 전에 자산·데이터·actor·위험·관할·정책·권한·예상 통제·정답
  manifest, 실패 주입, 승인·이관·중단·rollback·cleanup 기준을 봉인합니다.
- safety manifest에는 `wall_clock_timeout_seconds≤300`,
  `max_requests≤10000`, `max_concurrency≤16`,
  `max_retries_per_request≤2`, `max_fault_injections≤10`,
  `max_fixture_bytes≤10485760`, record형 입력은 추가로
  `max_records≤10000`, `actual_spend=0`,
  `allowed_targets=loopback·새 임시 sandbox`를 기록하고 위반 즉시
  runner를 중단합니다.
- 각 후보는 `candidate.<id>.fixture@1.0.0`을 사용하고 D0 분류 12사례의
  오답 `0/12`, 주입 결함 `6/6` 탐지·처리, 후보가 지정한 JSON 제출 파일의
  필수 필드·참조 무결성을 공통 합격식으로 사용합니다. Phase 2에서는 이
  평가계약을 고정하며 실제 fixture·runner 구현은 Unit 활성화 전 별도
  필수 Gate입니다.
- 독립된 새 sandbox에서 같은 입력으로 2회 평가했을 때 canonical result
  hash가 같고 추가 mutation과 잔여 임시자원이 각각 0건이어야 합니다.
  초기·최종 sandbox manifest는 일치해야 하고 cleanup 대상 밖으로 분리한
  sanitized evidence의 hash는 유지되어야 합니다. 비변경형 D2 평가도
  sandbox·제출물 생성은 이 Gate를 적용하며 생략하지 않습니다.
- 도구 실행 성공, checklist 존재와 문서 분량을 위험 감소·규제 적합성·법적
  결론의 대리 지표로 사용하지 않습니다.
- 전문 변호사·DPO·보안 책임자·시스템 owner의 실제 승인과 조직별 위험수용을
  학습 결과가 대신하지 않습니다.

## D0 공통 Gate

- threat·vulnerability·risk·control과 policy·standard·procedure·evidence를
  구분합니다.
- identification·authentication·authorization·accounting과 역할·속성·정책
  기반 접근통제를 구분합니다.
- secret·credential·key·certificate·token과 hash·encryption·signature의
  목적을 구분합니다.
- privacy·security·confidentiality, 목적·법적 근거·동의와 보유·삭제를
  구분합니다.
- service incident와 security incident, 기술 복구와 법적 신고·증거 보존을
  구분합니다.
- copyright·license·contract·provenance와 보안·개인정보 의무를 구분합니다.
- AI 위험관리, 모델·시스템 보안, 공정성·투명성·인간 감독의 소유권을
  구분합니다.
- 봉인 사례 12건의 분류표를 answer key와 대조해 오답이 `0/12`여야 합니다.

## D2·제한 D3 공통 Gate

- 위험 register와 위협·통제·owner·검증증거·잔여위험·예외·재검토일을
  양방향 추적합니다.
- allow·deny·escalate·expire·revoke와 권한상승·분리의무·break-glass 경로를
  fake identity·policy decision fixture로 검증합니다. 승인된 break-glass
  2건은 성공 후 15분 가상시간 안에 만료·회수·사후감사 기록이 남아야 하고,
  무승인 2건은 모두 차단되며 2회차 잔여권한은 0건이어야 합니다.
- synthetic secret canary 누출·평문 저장·로그 출력 0건과 공개 test key의
  rotation·revocation·cleanup을 확인합니다. private-key destruction은
  일회성 sandbox 안의 폐기 가능한 synthetic test keypair와 합성 key-registry 상태
  머신으로만 검증하고 sandbox 밖 원문 key material 출력과 cleanup 후 잔여
  material은 각각 0건이어야 합니다.
- 취약 dependency·변조 artifact·오래된 SBOM·정책 예외를 주입하고
  detect·block·quarantine·remediate·revalidate 결과를 정답과 대조합니다.
- 개인정보와 AI 영향평가는 목적·범위·데이터 흐름·이해관계자·위험·통제·
  이관·재평가 trigger를 누락 없이 연결하되 법률 결론을 내리지 않습니다.
- 감사·incident·license evidence는 무결성·출처·시간·owner·보존·access와
  누락·모순을 검증하고 실제 법적 증거능력을 주장하지 않습니다.
- 보안사고 tabletop은 `exercise_duration_minutes≤45`,
  `max_event_steps≤20`을 추가로 봉인하고 실제 통지·신고를 0건으로 유지합니다.
- AI 보안은 prompt injection·poisoned retrieval·무권한 tool abuse를 각 2건
  주입하여 detect·block·quarantine·revalidate를 검증하고 cleanup 후 side
  effect를 0건으로 유지합니다.
- AI 거버넌스 Set은 고정 버전의 모든 필수 Unit Gate를 요구하며 하나라도
  실패하면 `not-ready`입니다. N/A에는 `rule_id`·범위·근거가 필요하고
  관할·고위험 잔여위험 불명은 `needs_qualified_review`로 이관합니다.
- 실제 전문 판단이 필요하거나 합성 fixture에서 검증할 수 없으면
  `needs_qualified_review`로 중단·이관합니다.

## 중단조건

- 실제 secret·개인정보·운영권한·외부 target이 필요합니다.
- exploit·bypass·malware·credential theft·exfiltration 구현이 필요합니다.
- 법률·규제·계약·수사·통지의 최종 결론을 학습자가 단독으로 내려야 합니다.
- 위험수용 owner·승인기준·이관경로가 없습니다.
- 봉인 manifest나 결정적 answer key가 없습니다.
- rollback·cleanup·증거 보존을 함께 달성할 수 없습니다.
