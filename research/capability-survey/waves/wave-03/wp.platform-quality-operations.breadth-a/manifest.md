# Work Package Manifest: wp.platform-quality-operations.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `promoted` |
| 범위 승인일 | `2026-07-30` |
| 승인 근거 | 사용자가 남은 패키지의 연속 생성·이중 검수·정규 승격·커밋을 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.8.0` (`provisional`) |
| 최대 후보 | `10` |
| 동시 작업 패키지 | `1` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, node ID·기술명은 영문 병기 허용 |

## 조사 계약

### 포함

- 변경 가능한 artifact·configuration의 배포·릴리스·rollback 검증
- 재현 가능한 환경·desired state·drift·reconciliation
- 서비스 telemetry의 logs·metrics·traces·events 계약
- 사용자 관점 SLI·SLO·error budget과 위험 비례 알림
- incident 준비·triage·지휘·통신·복구·postmortem
- backup·restore·RTO·RPO·재해복구와 복구 무결성
- 부하·성능·용량·과부하 보호와 확장 판단
- 기술 사용량·비용의 할당·예측·이상·최적화
- 내부 플랫폼·self-service·golden path의 제품적 운영 경계와 승격 타당성
- dependency·runtime·service의 patch·EOL·toil·운영 유지보수

### 제외

- 애플리케이션 기능·API·DB·테스트·build 재현성 자체의 반복
- 데이터 품질·ML drift·AI 평가·자동화 한 건의 결과조정 반복
- 제품별 cloud·CI/CD·monitoring·ITSM 도구 조작법
- 기업 IAM·보안정책·개인정보·법률·감사통제의 최종 판정
- 실제 production 계정·비밀정보·결제·삭제·장애 유발·실제 on-call
- 조직 도입·팀 구조·교육 운영 전체
- 상세 교재·실습·HUB와 실제 운영효과 검증

## 실행 구조

1. 읽기 전용 발견 조사자가 공식 표준·사양·1차 연구와 기존 카탈로그를
   교차검토합니다.
2. Codex 메인 세션이 후보 상한 10개 안에서 Candidate와 잠정 taxonomy를
   작성합니다.
3. 발견과 분리된 근거·taxonomy·실용성 감사자가 전수검수합니다.
4. 본 세션이 P0·P1을 교정하고 독립 재감사와 자동검증을 수행합니다.
5. 사용자 사전 승인에 따라 accepted 항목만 정규화한 뒤 정규 산출물을 다시
   독립 검수하고 P0·P1 0건일 때만 커밋합니다.

## Gate

- 후보는 10개 이하이고 한국어 우선 표시명을 사용합니다.
- Unit 후보는 D0와 관찰 가능한 D2 또는 제한된 D3 산출물·판정기준을 가집니다.
- 각 후보는 독립적인 공식·표준·1차 근거를 2개 이상 가집니다.
- production 대신 local simulator·sealed fixture·synthetic telemetry·
  bounded load와 복구 가능한 sandbox를 사용합니다.
- 실행시간·요청량·비용·오류주입·중단·rollback 상한을 평가 전에 고정합니다.
- 공통 상한은 wall clock 300초, 요청 10,000건, 동시성 16, 요청별 retry 2회,
  fault 주입 10회, fixture 10MiB 이하이며 record형 입력은 추가로 10,000건
  이하, 실제 지출 0원입니다. loopback·새 임시 sandbox만 허용합니다.
- 사용자 영향·SLO·비용·복구 결과를 단순 도구 실행 성공과 구분합니다.
- 보안·개인정보·법률·재무·고위험 운영 판단은 전문 소유 영역으로 이관합니다.
- 승격 전과 승격 후에 근거·taxonomy·실용성 검수를 각각 수행합니다.
- 카탈로그·공개 경계·스키마·단위 테스트와 `git diff --check`를 통과합니다.

## 자동 중단조건

- 실제 운영계정·자격증명·유료 자원·개인정보·외부 상태 변경이 필요합니다.
- 무제한 부하·retry·polling·자동 확장 또는 실제 장애 유발이 필요합니다.
- rollback·restore 경로가 없거나 원본·운영 데이터를 덮어써야 합니다.
- 제품별 수치를 보편적인 SLO·용량·비용 기준으로 일반화해야 합니다.
- 보안·법률·재무 승인권을 이 패키지가 임의로 확정해야 합니다.
- 기존 Unit과 같은 D2/D3 산출물·검증 Gate를 가집니다.
- 공개 경계·스키마·독립 감사가 실패합니다.

## 현재 진행

읽기 전용 발견 조사를 완료하고 후보 상한 10개를 작성했습니다. 내부 플랫폼은
독립 검증보다 조직 operating model과 실제 사용자 근거가 선행되어야 하므로
독립 후보에서 유보했습니다. 대신 서비스 장애의 영향 범위를 제한해 검증하는
복원력 Unit과 운영 증거를 수명주기 결정으로 묶는 운영준비 Set을 포함했습니다.
독립 근거·taxonomy·실용성 감사에서 발견한 P1을 모두 교정하고 세 관점
재감사에서 P0·P1 0건을 확인했습니다. 9개 Unit 후보와 1개 Set 후보를
`accepted`로 확정했습니다. 사용자 사전 승인에 따라 9개 Unit과 각 공개
Reference, 서비스 운영준비 Set을 정규 승격했으며 승격 후 세 관점 재감사에서도
P0·P1 0건을 확인했습니다.
