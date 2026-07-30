# Work Package Manifest: wp.security-legal-governance.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `promoted` |
| 범위 승인일 | `2026-07-30` |
| 승인 근거 | 사용자가 남은 패키지의 연속 생성·이중 검수·정규 승격·커밋을 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.9.0` (`provisional`) |
| 최대 후보 | `10` |
| 동시 작업 패키지 | `1` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, 표준 ID·법령명·기술명은 영문 병기 허용 |

## 조사 계약

### 포함

- 위험 기반 보안 요구·위협 모델·보안 아키텍처와 검증 가능한 통제
- identity·authentication·authorization·least privilege·access lifecycle
- secret·credential·cryptographic key의 생성·저장·회전·폐기 경계
- software dependency·artifact provenance·SBOM·취약점·공급망 위험
- 개인정보 영향·목적·최소수집·보유·삭제·정보주체 권리와 privacy engineering
- security incident 분류·대응·증거 보존·보고 의무 라우팅
- 감사 가능한 통제·정책·증거·예외·책임·주기적 검토
- 저작권·license·데이터·모델·콘텐츠 출처와 사용권 provenance
- AI 위험·영향·공정성·투명성·인간 감독·책임 거버넌스
- AI system threat·prompt injection·data poisoning·model abuse의 위험 기반 평가

### 제외

- 실제 조직·제품의 법률 자문, 규제 적합성 인증과 최종 승인
- 실제 개인정보·기밀·credential·private key·고객·운영계정의 수집·처리
- 실제 외부 target·network·cloud·SaaS에 대한 scan·exploit·침투·장애 유발
- malware·credential theft·bypass·persistence·exfiltration 구현
- 제품별 IAM·SIEM·GRC·DLP·scanner·법률 DB 도구 조작법
- 실제 수사·법적 증거능력·신고·통지·소송·계약 체결 판단
- 상세 교재·실습환경·HUB와 실제 통제 효과·법적 결과 검증
- 조직 역할·교육·문화·변화관리 전체

## 실행 구조

1. 읽기 전용 발견 조사자가 공식 표준·법령·사양·1차 연구와 기존
   Candidate·Unit·Set을 교차검토합니다.
2. Codex 메인 세션이 후보 상한 10개 안에서 Candidate와 잠정 taxonomy를
   작성합니다.
3. 발견과 분리된 근거·taxonomy·실용성 감사자가 모든 고위험 후보를
   전수검수합니다.
4. 본 세션이 P0·P1을 교정하고 독립 재감사와 자동검증을 수행합니다.
5. 사용자 사전 승인에 따라 accepted 항목만 정규화한 뒤 정규 산출물을 다시
   독립 전수검수하고 P0·P1 0건일 때만 커밋합니다.

## Gate

- 후보는 10개 이하이고 한국어 우선 표시명을 사용합니다.
- 각 후보는 관할·위험·역할·결정권과 전문 이관 조건을 명시합니다.
- Unit 후보는 D0와 local·합성 fixture에서 관찰 가능한 D2 또는 제한 D3
  산출물·판정기준을 가집니다.
- 공식 표준·법령·사양·1차 근거를 후보별 2개 이상 연결합니다.
- 실제 secret·개인정보·운영권한·외부 target 대신 synthetic canary,
  fake identity, 공개 test key와 삭제 가능한 loopback sandbox를 사용합니다.
- 자동 runner·simulator는 300초, 요청 10,000건, 동시성 16, retry 2회,
  fault 10회, fixture 10MiB 및 record형 입력 10,000건 이하, 실제 지출 0원으로
  제한합니다.
- 법률·규제·보안 승인과 실제 업무 판단은 qualified owner에게 이관하며
  학습 fixture 결과를 적합성 인증으로 표현하지 않습니다.
- 승격 전과 승격 후에 근거·taxonomy·실용성 검수를 각각 수행합니다.
- 카탈로그·공개 경계·스키마·단위 테스트와 `git diff --check`를 통과합니다.

## 자동 중단조건

- 실제 개인정보·기밀·credential·private key·운영계정이 필요합니다.
- 외부 target scan·exploit·우회·침투·malware·데이터 유출이 필요합니다.
- 원본 또는 운영 데이터를 덮어쓰거나 삭제해야 합니다.
- 관할·적용 법령·정책 owner를 알 수 없는데 법적 결론을 내려야 합니다.
- 위험등급·승인·이관·중단·rollback·증거 보존 기준을 고정할 수 없습니다.
- 특정 규정·공급자 사례를 보편적인 적합성 또는 효과 보장으로 일반화해야 합니다.
- 기존 Unit과 같은 D2/D3 산출물·검증 Gate를 가집니다.
- 공개 경계·스키마·독립 감사가 실패합니다.
