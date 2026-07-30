# 도메인 조사: 조직 도입·변화·학습운영

## 결론

기존 정규 catalog와 교차검토한 결과, 조직 도입은 독립적인 9개 Unit 후보와
이를 조합하는 1개 Set 후보로 구성합니다. `ax-strategy-value`의 기회선정·
투자 우선순위, 기존 기술 Unit의 구현, 보안·법무 전문판정과 개인 인사결정을
복제하지 않습니다.

| 후보 | 목적지 | 목표 | 독립 경계 |
|---|---|---|---|
| 변화 영향·도입 준비도·이해관계자 참여 설계 | Unit | D2 | 영향·참여·지원·contest 경로 |
| AX 운영모델·의사결정권·책임·인계 설계 | Unit | 제한 D3 | 사람·AI·자동화의 조직 decision contract |
| 과업·역량·인력 수요·skill gap·전환 분석 | Unit | D2 | 선택된 업무설계 이후의 workforce transition |
| 역할 기반 학습·평가·업무전이 설계 | Unit | D2 | gap→outcome→assessment→transfer |
| 포용적 직무영향·직원참여·지원 경계 | Unit | D2 | job quality·voice·support 전문이관 |
| 도입 지원·챔피언·community·지식흐름 운영 | Unit | 제한 D3 | support queue·지식 lifecycle |
| 도입 행동·품질·위험·성과·분배효과 측정 | Unit | 제한 D3 | adoption 운영지표·억제·재평가 |
| AX pilot·단계확대·중단·rollback 전환 거버넌스 | Unit | 제한 D3 | 조직 확대 transition decision |
| 공급자·조달·SaaS 도입 증거·전문검토 이관 | Unit | D2 | 선정·계약이 아닌 qualified evidence handoff |
| 조직 AX 도입·확산 lifecycle assurance | Set | D3 | 위 Unit의 종단 간 조합 |

## 근거와 버전 판단

- 조직 AI 역할·훈련·risk culture·제3자는 NIST AI RMF 1.0과 Playbook,
  GAO-21-519SP, ISO/IEC 42001:2023을 사용하며 certification을 주장하지 않습니다.
- 참여·workforce·학습은 ISO 10018:2020, ISO 30409:2016, ISO 10015:2019,
  ISO 30422:2022와 Weiner 2009 readiness 이론·Blume 2010 training-transfer
  meta-analysis를 사용하고 보건·일반 학습연구의 한계와 실제 HR·고용판단을
  구분합니다.
- 지식·지원 운영은 ISO 30401:2018+Amd1:2022+Amd2:2024와 DOL TEN 07-25를
  사용하되 revision·미국 workforce guidance 맥락과 champion·community의
  보편 효과를 주장하지 않습니다.
- 측정·포용은 Proctor 2011 implementation outcome 구분, ISO 30414:2025와
  ISO 30415:2021을 사용하고 연구의 보건 맥락·개인 score·국가별 노무·법률
  결론을 제외합니다.
- 공급자·조달 이관은 UK Guidelines for AI Procurement 2020을 사용하되
  영국 공공조달 맥락이며 선정·가격·계약·법적 적합성을 판정하지 않습니다.
- worker voice·algorithmic management는 ILO 2025 다국가 사례와 2022
  개념 연구를 사용하며 사례조건을 보편화하지 않습니다.
- pilot·scale은 GOV.UK Service Manual과 ISO 56002:2019를 사용하되 공공
  디지털서비스·혁신관리 맥락의 한계와 ISO 56002 개정 진행을 기록합니다.

## 중복·누락 레드팀

- 기회선정·value case·target work design은 `ax-strategy-value` 소유입니다.
- causal impact는 기존 intervention impact Unit을 사용하고 조직 후보는
  adoption 운영지표·분배효과·재평가 연결만 소유합니다.
- 기술 release·운영준비·보안·privacy·license 검증은 기존 정규 Unit을
  재사용하며 조직 후보는 확대·지원·전문이관 결정을 소유합니다.
- 실제 workforce data, 감정·행동 추론, 개인 ranking·성과·고용결정,
  노사협의·법률·조달·계약 결론은 제외합니다.
- 조직문화 진단, 보상·성과관리, 채용·succession, 노사관계 협상,
  실제 vendor 선정은 전문 HR·labor·procurement 후속 Resource·Set으로
  `defer`합니다.
- 마지막 누락 점검에서 현재 10개 상한 안에 추가할 독립 고우선 후보는
  0개입니다.

## 안전 경계

합성 조직·역할·업무·skill·survey·학습·지원·adoption fixture만 사용하고
소규모 집단·differencing 가능 교차표를 억제합니다. 실제 개인 data·감시·
ranking·punitive use·고용·노무·조달·계약·조직변경은 수행하지 않으며
불명확 전문판단은 `needs_qualified_review`로 중단·이관합니다.
