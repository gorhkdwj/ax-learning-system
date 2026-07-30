# Work Package Manifest: wp.organization-adoption.breadth-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-03` |
| 상태 | `promoted` |
| 범위 승인일 | `2026-07-30` |
| 승인 근거 | 사용자가 남은 패키지의 연속 생성·이중 검수·정규 승격·커밋을 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.10.0` (`provisional`) |
| 최대 후보 | `10` |
| 동시 작업 패키지 | `1` |
| 표시명 규칙 | 과목·후보명은 한국어 우선, 표준 ID·프레임워크·기술명은 영문 병기 허용 |

## 조사 계약

### 포함

- AX 도입 대상 업무·이해관계자·영향·준비도·저항·참여 경로
- 사람·AI·자동화의 역할·책임·의사결정권·인계·운영모델
- 과업·역량·인력 수요·skill gap·학습 요구 분석
- 학습 프로그램·실습·평가·업무 전이·운영 품질
- 챔피언·지원·community of practice·지식 공유·feedback loop
- 도입 사용행동·품질·위험·업무성과·분배효과의 측정과 재평가
- pilot·단계 도입·확대·중단·rollback·benefit realization
- 정책·지원·예외·조달·vendor·SaaS 도입의 조직 이관
- 접근성·포용성·직무 영향·업무부담·직원 참여·지원의 변화 경계
- 여러 정규 Unit을 조직 도입 lifecycle로 조합하는 Set 가능성

### 제외

- 실제 조직의 인사·노무·노사관계·해고·보상·평가·채용 최종 판단
- 실제 개인 성과·건강·감정·생체·민감정보 수집과 감시
- 실제 조직개편·예산·조달·계약·vendor 선정·배포 승인
- 법률·규제·보안·privacy·위험수용의 최종 전문 판단
- 특정 변화관리·교육·HR·survey·LMS 제품의 조작법
- 상세 교재·실제 사용자 연구·실제 조직 pilot·학습효과·업무효과 검증
- `ax-strategy-value`의 기회선정·투자 우선순위·가치 case 자체
- 기존 기술 Unit의 구현·보안·운영·Human-AI interaction 내용 복제

## 실행 구조

1. 읽기 전용 발견 조사에서 공식 표준·법령·정부·1차 연구와 기존 전체
   Candidate·Unit·Set을 교차검토합니다.
2. 메인 세션만 후보 상한 10개 안에서 Candidate와 잠정 taxonomy를 작성합니다.
3. 근거·taxonomy·실용성 감사자가 고위험 후보를 전수 검토합니다.
4. 메인 세션이 P0·P1을 교정하고 독립 재감사와 자동 검증을 수행합니다.
5. accepted 후보만 정규화하고 정규 산출물을 다시 전수 감사한 뒤 커밋합니다.
6. Set 승격은 동일 패키지의 Unit 9개를 먼저 생성하고 schema·exact version·
   `required_level≤maximum_scope_level`을 검증한 뒤에만 수행합니다.

## Gate

- 후보는 10개 이하이고 한국어 우선 표시명을 사용합니다.
- 각 후보는 조직 단위의 관찰 가능한 D2 또는 제한 D3 산출물·판정기준을 가집니다.
- 합성 조직·역할·업무·survey·학습·도입 fixture만 사용하고 개인 감시·성과평가·
  고용결정·실제 조직 변경은 수행하지 않습니다.
- 사람·팀·역할 단위 지표는 최소 집단크기·억제·비식별·목적제한·보유기간을
  봉인하고 개인 ranking·punitive use를 금지합니다.
- 전문 HR·노무·법무·보안·privacy·재무 판단은 qualified owner에게 이관합니다.
- 승격 전과 후에 근거·taxonomy·실용성 전수 재검수를 각각 수행합니다.

## 결과

- accepted Candidate 10개: Unit 후보 9개, Set 후보 1개
- 정규 `cataloged` Unit 9개와 Unit 소유 공개 Reference 9개
- 정규 project Set 1개: 필수 조직 Unit 8개와 applicability 기반 조건부
  Unit 5개를 조합한 13단계 lifecycle assurance
- 승격 전 독립 3축 최종 감사: P0·P1·P2 0건
- 상세 fixture·runner와 실제 조직·관할·학습·도입 효과 검증:
  `required_before_activation`

## 자동 중단조건

- 실제 직원·지원자·고객의 개인·민감·성과·행동 데이터를 요구합니다.
- 개인 감시·ranking·징계·해고·보상·채용 판단을 자동화하려 합니다.
- 실제 조직·예산·조달·계약·접근권한·외부 시스템을 변경해야 합니다.
- 법률·규제·노무·보안·위험수용 결론을 학습자가 단독으로 내려야 합니다.
- 영향받는 사람의 참여·이의제기·지원·중단 경로가 없습니다.
- 결정적 answer key·평가분모·cleanup·evidence 보존 기준이 없습니다.
