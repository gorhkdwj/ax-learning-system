# 데이터·분석·ML D2 평가 계약

## 공통 원칙

- 과목명과 제출물 표시는 한국어를 우선하고 기술·표준 ID는 영문을 허용합니다.
- 제공된 소규모 dataset·schema·요구·비용·정답 manifest를 사용합니다.
- 평가 전용 manifest에는 정답과 채점기준만 두며 학습자가 찾을 오류·경계를
  미리 노출하지 않습니다.
- 자동검사만으로 완료하지 않고 주장·가정·잔여 한계·실패 처리와 인간 승인점을
  함께 평가합니다.
- 개인정보·보안·법적 판단은 승인된 가상 정책과 fixture로 제한하며 전문
  통제의 정답을 학습자에게 추정시키지 않습니다.
- 특정 제품의 UI 조작보다 입력–변환–출력 계약, 재현성, 검증 증거와 판정을
  평가합니다.
- 실행 전에 query·변환·저장·backfill·재학습·인간 검토의 시간·금액·자원
  한도를 고정합니다. 한도를 넘으면 추가 실행을 중단하고 `판단 불가` 또는
  인간 이관으로 처리합니다.
- 제공된 승인정책이 요구하는 backfill, 지표 정의 변경, 데이터 격리 해제,
  model threshold 변경, 재학습·rollback은 승인 전에 실행하지 않습니다.
- 승인 거부·취소·무응답 fixture에서는 외부 상태변경 0건, 원본 보존과
  감사로그 생성을 확인합니다. 승인 후에도 최종 dataset·metric·model 상태를
  정답 manifest와 대조합니다.
- 대표성·적법성·품질 임계·인과·재학습 판단에 필요한 정보가 없으면 임의로
  결론을 만들지 않는 것을 올바른 결과로 인정합니다.

## Unit 후보 공통 D2 Gate

1. 입력의 목적·관찰단위·버전·시간범위·허용 제약을 식별합니다.
2. 정상·경계·실패 fixture를 분리하고 예상 결과와 판정 임계값을 선언합니다.
3. 입력에 없는 사실·정책·대표성·인과를 임의로 추가하지 않습니다.
4. 같은 입력·코드·환경에서 결과나 허용된 변동범위를 재현합니다.
5. 누락·중복·단위·시간·분할·계보 오류를 자동검출하고 원인을 추적합니다.
6. 품질·불확실성·오류 slice와 잔여 한계를 보고합니다.
7. 변경·재실행·중단·rollback 또는 이관 판정을 명시합니다.

## 후보별 핵심 fixture

### 데이터 원천 수집·계약

- 열 이름·자료형·단위·키·필수값·시간대·갱신시점이 다른 정상·오류 원천을
  제공합니다.
- 이 후보는 생산자–소비자 사이의 최초 인수계약과 ingest 전 수락 여부를
  소유합니다. 반복 실행에서의 품질 추세·분포 변화·오탐률 판정은 데이터 품질
  후보로 이관합니다.
- 필수 필드·키·단위·시간대·허용 지연은 학습자에게 제공된 요구·schema·원천
  설명에 모두 존재하고, 평가자 manifest는 정답 목록과 위반 위치만 숨깁니다.
- schema 통과 여부와 대표성·적법성·업무 적합성 판단을 분리합니다.
- late data, duplicate event, 단위 변환과 원천 수정 이력을 검출합니다.
- 치명 계약 위반은 모두 검출하고 허용 가능한 정상 입력은 거부하지 않으며,
  입력에 없는 대표성·적법성 주장과 임의 계약 추가는 0건이어야 합니다.

### 재현 가능한 데이터 변환·파이프라인

- 동일 입력 재실행, 부분 실패 후 재시작, 중복 입력, backfill과 schema 변경을
  제공합니다.
- 출력 내용·row grain·중복·checkpoint와 lineage가 기대값과 일치해야 합니다.
- 단순 실행 성공이 아니라 동일하고 올바른 결과를 판정합니다.

### 분석 모델·지표 의미계약

- transaction grain과 분석 grain이 다르고 비가산 measure가 섞인 데이터를
  제공합니다.
- `candidate.ax-strategy-value.measurement-contract@1.0.0`에서 승인된 KPI
  정의를 입력으로 받으며, 이 후보는 KPI 선택이나 정의 변경이 아니라
  grain·집계·reconciliation 구현만 소유합니다.
- dimension·measure·attribute, 분자·분모·단위·시간창과 집계 가능성을
  선언합니다.
- 중복 join, 평균의 평균, 누락 차원과 단위·timezone 불일치를 탐지합니다.

### 탐색적·통계적 분석

- 결측·이상치·작은 표본·집단 불균형·시계열 또는 군집 의존성이 숨은
  데이터를 제공합니다.
- 질문–가정–탐색–분석–민감도 검사를 재현하고 효과크기·구간·한계를
  보고합니다.
- p-value·상관·전체 평균만으로 인과나 실무 중요성을 단정하면 실패입니다.

### 데이터 품질 검증·관측

- 정상 계절성, 실제 결함, 지연, 분포 이동과 소수 slice 오류를 함께 제공합니다.
- 공개된 calibration 구간과 평가자만 label을 가진 봉인된 holdout 구간을
  분리합니다.
- 사용목적별 dimension·metric·threshold·격리 규칙을 holdout 실행 전에
  고정하고 threshold 조정 이력과 holdout 접근 횟수를 기록합니다.
- 계절성·정상 변화, 실제 결함, upstream 장애와 현상 변화를 holdout에
  포함하고 사전 고정한 최소 검출률·최대 오탐률로 평가합니다.
- label이나 도메인 허용한계가 없으면 임의 threshold를 확정하지 않고
  `판단 불가`·인간 승인으로 보냅니다.

### 데이터 카탈로그·계보·책임 메타데이터

- 자동 pipeline과 수동 export가 섞인 source–activity–output 경로를 제공합니다.
- dataset ID·version·owner·steward·distribution과 derivation을 기록합니다.
- 임의 출력에서 원천·변환·책임자를 역추적하며 미포착 경로를 명시합니다.

### 기존 통제 실험·영향평가

- 기존 Candidate의 평가계약을 재사용하고 배정단위·비교조건·sample-ratio,
  attrition, telemetry loss와 반복 중간검정을 추가 공격 사례로 확인합니다.
- 기존 ID·목적지·선수관계를 변경하는 평가는 하지 않습니다.

### 예측 ML 문제정의·비ML 기준선

- 비ML 목표·결정·행동, prediction time과 label 지연이 주어진 업무를
  제공합니다.
- target·prediction unit·feature 가용성·비용행렬과 heuristic·단순모델
  기준선을 만듭니다.
- 예측 가능성·ML 필요성·업무가치를 같은 주장으로 취급하면 실패입니다.

### 예측 ML 모델 검증·의사결정 임계값

- 시간·사용자·집단 구조, 불균형 class와 누수 가능 feature가 있는 데이터를
  제공합니다.
- train·validation은 제공하되 최종 test label은 평가자가 봉인합니다.
- preprocessing·feature 선택·calibration·threshold를 validation에서 고정한
  뒤 test를 한 번만 실행하고 test dataset hash·접근 횟수·실험 설정 이력을
  기록합니다.
- preprocessing fit이 validation·test를 사용하지 않았는지 자동검사하고 전체
  metric과 manifest의 필수 slice·calibration·비용 결과를 함께 보고합니다.
- 사전 고정한 baseline 대비 비열등성·개선기준을 충족하지 못하면 no-go를
  인정하며 전문 fairness·규제 threshold는 인간 승인 없이 확정하지 않습니다.

### ML 생명주기 재현성·모니터링

- versioned data·code·config·model과 label 지연, drift·skew·성능 악화 조합을
  제공합니다.
- 학습 결과를 허용 오차 안에서 재현하고 변화 signal을 기준선과 비교합니다.
- 유지·재학습·중단·rollback 판정과 인간 승인점을 제시합니다.
- 실제 production rollout·serving·incident 대응은 D3 운영 overlay로
  이관합니다.
