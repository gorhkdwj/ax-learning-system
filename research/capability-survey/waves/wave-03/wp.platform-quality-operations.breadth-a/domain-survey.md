# 분야 조사: 플랫폼 품질·운영

## 1. 조사 요약

`platform-quality-operations`는 특정 cloud·CI/CD·관측 제품의 조작법이 아니라
서비스 변경을 안전하게 전달하고, 사용자 영향과 운영 상태를 관찰하며, 장애와
복구·용량·비용·수명주기를 재현 가능한 증거로 판단하는 렌즈로 조사했습니다.
Google SRE, OpenTelemetry, W3C Trace Context, OpenGitOps, NIST 연속성 지침,
FinOps Framework·FOCUS와 CNCF 플랫폼 자료를 기존 Candidate·Unit·Set과
교차검토했습니다.

## 2. Candidate 목록

| Candidate ID | 한국어 표시명 | 목적지 | 목표 |
|---|---|---|---|
| `candidate.platform-quality-operations.safe-release-deployment-rollback` | 안전한 릴리스·배포·롤백 검증 | Unit | D3 |
| `candidate.platform-quality-operations.declarative-environment-drift-reconciliation` | 선언적 환경·구성 드리프트 조정 | Unit | D3 |
| `candidate.platform-quality-operations.service-observability-telemetry-contract` | 서비스 관측성·텔레메트리 계약 | Unit | D3 |
| `candidate.platform-quality-operations.sli-slo-error-budget-alerting` | SLI·SLO·오류예산·알림 설계 | Unit | D2 |
| `candidate.platform-quality-operations.incident-response-postmortem-learning` | 서비스 사고 대응·사후학습 | Unit | D3 |
| `candidate.platform-quality-operations.backup-restore-disaster-recovery` | 백업·복원·재해복구 검증 | Unit | D3 |
| `candidate.platform-quality-operations.performance-capacity-overload-protection` | 성능·용량·과부하 보호 검증 | Unit | D3 |
| `candidate.platform-quality-operations.technology-cost-allocation-optimization` | 기술비용 할당·이상·최적화 | Unit | D2 |
| `candidate.platform-quality-operations.resilience-failure-mode-experimentation` | 복원력 설계·장애실험 | Unit | D3 |
| `candidate.platform-quality-operations.service-production-readiness-lifecycle` | 서비스 운영준비·수명주기 전환 | Set | D3 |

## 3. 잠정 Taxonomy

- `release-deployment-safety`
- `declarative-environment-configuration`
- `service-observability-telemetry`
- `service-level-objectives-reliability`
- `incident-response-postmortem`
- `backup-restore-continuity`
- `performance-capacity-overload-protection`
- `technology-cost-finops`
- `resilience-failure-mode-experimentation`
- `production-readiness-service-lifecycle`

## 4. 인접 경계와 중복 처리

- build·test·Git·API 회복성·부작용 안전·결과 조정은 기존 `software`와
  `integration-automation` Unit을 재사용하며 본 패키지는 서비스 운영 수준의
  변경·관측·신뢰성 증거만 소유합니다.
- 데이터·ML 관측성과 분석 지표 의미계약은 `data-analytics-ml`이 소유합니다.
  본 패키지는 서비스 횡단 telemetry와 운영 의사결정만 소유합니다.
- 보안 사고, IAM, 취약점, 개인정보, 법률·감사통제는
  `security-legal-governance`로 이관합니다.
- 조직의 실제 당직·인력·도입문화와 FinOps 조직체계는
  `organization-adoption`이 소유합니다.
- Kubernetes·Terraform/OpenTofu·Prometheus·Grafana 등 제품 조작법은
  core Unit이 아니라 후속 Adapter 또는 Resource 후보입니다.
- 포괄적 DevOps·SRE·platform engineering 개론은 독립 검증 산출물이 없어
  정규 Unit으로 만들지 않습니다.
- 내부 플랫폼·self-service·golden path는 실제 내부 사용자 조사와 operating
  model 근거가 필요한 범위이므로 독립 후보 승격을 유보합니다. 이번에는
  안전한 운영변경 Unit과 서비스 운영준비 Set에서 필요한 계약만 사용합니다.
  후속 소유자는 `organization-adoption`이며 내부 사용자 조사와 플랫폼 제품
  operating model을 확보했을 때 독립 후보 여부를 재검토합니다.

## 5. 주요 근거

| 출처 | 확인 범위 |
|---|---|
| Google SRE Book·Workbook | release·SLO·monitoring·incident·postmortem·recovery·overload·reliability·toil·production readiness |
| OpenTelemetry Specification·Semantic Conventions | logs·metrics·traces·events와 공통 telemetry 계약 |
| W3C Trace Context | 분산 요청의 vendor-neutral 추적 문맥 전파 |
| OpenGitOps Principles | 선언형·versioned·자동 pull·지속 조정 원칙 |
| NIST SP 800-34 Rev.1 | 업무영향·복구전략·계획·시험을 포함한 연속성 계획 |
| FinOps Framework 2026·FOCUS | 기술비용 할당·사용 최적화와 vendor-neutral 비용 데이터 계약 |
| CNCF Platforms White Paper·Maturity Model | 내부 플랫폼 경계와 조직 의존성을 독립 Unit으로 일반화하지 않을 근거 |

각 Candidate에는 확인일, 직접 지지 범위와 미지원 범위를 포함한 원천별 evidence를
기록했습니다. 제품별 효과 크기나 실제 운영 적합성은 근거가 지지하는 범위를
넘어 일반화하지 않습니다.

## 6. 마지막 누락·반대 관점 점검

| 점검 패스 | 검색군·역할 관점 | 발견과 처리 |
|---|---|---|
| 변경·상태 | release, deployment, rollback, configuration, drift, patch | 서비스 소유자·운영자 관점에서 release와 drift를 분리했습니다. patch는 기존 build·dependency 재현성 Unit, 선언형 환경과 안전한 릴리스를 운영준비 Set에서 조합하고 EOL은 Set의 수명주기 결정으로 흡수했습니다. |
| 관찰·판정 | logs, metrics, traces, SLI, SLO, error budget, alert, on-call | 서비스 소유자·운영자 관점에서 telemetry와 신뢰성 판정을 분리했습니다. alert는 SLO, on-call 실행은 사고대응에 흡수했습니다. |
| 실패·복구 | incident, postmortem, backup, restore, resilience, overload | 운영자·감사 관점에서 사고 지휘, 데이터 복구, 부하 한계와 dependency 장애전파를 별도 후보로 유지했습니다. 보안 사고는 전문 렌즈로 이관했습니다. |
| 비용·수명주기 | allocation, forecast, anomaly, optimization, toil, maintenance, deprecation | 재무·서비스 소유자 관점에서 기술비용 Unit과 운영준비 Set으로 분리했습니다. 실제 예산·회계·조직 책임은 이관했습니다. |
| 내부 플랫폼 | platform user, self-service, golden path, platform product | 플랫폼 사용자 관점의 실제 조사와 operating model이 없어 독립 후보를 유보했습니다. `organization-adoption` 근거가 확보되면 재검토합니다. |
| 반대·인접 관점 | tool success vs user impact, operator vs owner, finance vs engineering, auditor vs executor | 기존 후보 흡수·전문 렌즈 이관 외 새 후보는 없었습니다. 제품별 도구 조작법은 Adapter·Resource로 유보했습니다. |

각 패스에서 신규 독립 후보, 기존 후보 흡수, 전문 렌즈 이관과 유보를 다시
대조했습니다. 최종 새 고우선 독립 후보는 0개입니다.

## 7. 현재 판정

후보 10개와 잠정 subdomain 10개의 독립 근거·taxonomy·실용성 전수감사를
완료했습니다. 최초 감사의 P0는 0건이었고 P1을 모두 교정한 뒤 세 관점
재감사에서 P0·P1 0건을 확인했습니다. Unit 후보 9개와 Set 후보 1개는 모두
`accepted`입니다. 사용자 사전 승인에 따라 Unit 후보 9개는 각 공개 Reference와
함께 정규 `cataloged` Unit으로, Set 후보 1개는 정규 `cataloged` Set으로
승격했습니다. 승격 후 정규 ID·관계·근거·owner·평가·안전 Gate를 다시
독립 전수검수하여 P0·P1 0건을 확인했습니다. 내부 플랫폼 독립 Unit은 이번
후보 상한 밖의 별도 `defer` 판단이며 Candidate로 만들지 않았습니다.
