# Wave 6 독립 QA 대상 Register

## 1. 요약

| 구분 | 고유 후보 |
|---|---:|
| 고위험·D3·논쟁 전수 | 30 |
| 일반 층화표본 | 26 |
| 전체 QA 대상 | 56 |

## 2. 고위험·D3·논쟁 전수 대상

| 대분류 | 후보 | 트리거 |
|---|---|---|
| AI 리터러시·신뢰 | `candidate.ai-literacy-trust.evidence-source-verification` | merge 판정 |
| AX 전략·가치 | `candidate.ax-strategy-value.benefits-realization` | needs_review·defer |
| AX 전략·가치 | `candidate.ax-strategy-value.future-state-redesign` | 핵심 조합 Set |
| AX 전략·가치 | `candidate.ax-strategy-value.measurement-contract` | 여러 대분류 핵심 선수 |
| AX 전략·가치 | `candidate.ax-strategy-value.solution-fit-assessment` | 여러 대분류 핵심 선수 |
| 데이터·분석·ML | `candidate.ax-strategy-value.pilot-impact-evaluation` | 핵심 영향평가 |
| Human-AI 경험 | `candidate.human-ai-experience.personalization-memory-user-control` | deferred |
| 조직·도입 | `candidate.organization-adoption.adoption-outcome-distribution-measurement` | D3 |
| 조직·도입 | `candidate.organization-adoption.adoption-support-community-knowledge-flow` | D3 |
| 조직·도입 | `candidate.organization-adoption.ax-operating-model-decision-rights` | D3 |
| 조직·도입 | `candidate.organization-adoption.enterprise-ax-adoption-lifecycle` | D3 Set |
| 조직·도입 | `candidate.organization-adoption.pilot-scale-transition-governance` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.backup-restore-disaster-recovery` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.declarative-environment-drift-reconciliation` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.incident-response-postmortem-learning` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.performance-capacity-overload-protection` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.resilience-failure-mode-experimentation` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.safe-release-deployment-rollback` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.service-observability-telemetry-contract` | D3 |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.service-production-readiness-lifecycle` | D3 Set |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.ai-system-risk-impact-governance-assurance` | 고위험·D3 Set |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.ai-system-security-threat-evaluation` | 고위험·D3 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.digital-asset-license-rights-provenance-routing` | 법무·저작권 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.identity-access-policy-lifecycle` | 권한·D3 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.privacy-engineering-impact-data-rights-lifecycle` | 개인정보·법무 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.secrets-credentials-key-lifecycle` | 비밀·키·D3 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.security-control-assurance-audit-exception-governance` | 감사·D3 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.security-incident-evidence-reporting-routing` | 사고·신고·법무 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.security-risk-requirements-threat-model-controls` | 보안위험·D3 |
| 보안·법무·거버넌스 | `candidate.security-legal-governance.software-supply-chain-integrity-vulnerability-governance` | 공급망·D3 |

## 3. 일반 층화표본

| 대분류 | 후보 |
|---|---|
| AI 리터러시·신뢰 | `candidate.ai-literacy-trust.affected-person-impact-awareness` |
| AI 리터러시·신뢰 | `candidate.ai-literacy-trust.content-provenance-interpretation` |
| AI 리터러시·신뢰 | `candidate.ai-literacy-trust.trust-calibration` |
| AI 시스템·에이전트 | `candidate.ai-systems-agents.agent-state-memory-handoff-design` |
| AI 시스템·에이전트 | `candidate.ai-systems-agents.ai-workflow-agent-topology-design` |
| AI 시스템·에이전트 | `candidate.ai-systems-agents.system-context-design` |
| AX 전략·가치 | `candidate.ax-strategy-value.current-state-work-analysis` |
| AX 전략·가치 | `candidate.ax-strategy-value.opportunity-value-framing` |
| AX 전략·가치 | `candidate.ax-strategy-value.task-allocation` |
| 데이터·분석·ML | `candidate.data-analytics-ml.analytical-model-metric-semantics` |
| 데이터·분석·ML | `candidate.data-analytics-ml.exploratory-statistical-analysis` |
| 데이터·분석·ML | `candidate.data-analytics-ml.reproducible-data-transformation-pipelines` |
| Human-AI 경험 | `candidate.human-ai-experience.accessible-multimodal-ai-interaction` |
| Human-AI 경험 | `candidate.human-ai-experience.human-ai-experience-evaluation` |
| Human-AI 경험 | `candidate.human-ai-experience.user-question-centered-explanation-experience` |
| 통합·자동화 | `candidate.integration-automation.automation-outcome-observability-reconciliation` |
| 통합·자동화 | `candidate.integration-automation.event-webhook-delivery-contract` |
| 통합·자동화 | `candidate.integration-automation.ui-driven-task-automation` |
| 조직·도입 | `candidate.organization-adoption.change-impact-readiness-engagement` |
| 조직·도입 | `candidate.organization-adoption.learning-transfer-operations` |
| 조직·도입 | `candidate.organization-adoption.workforce-capability-gap-transition` |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.sli-slo-error-budget-alerting` |
| 플랫폼 품질·운영 | `candidate.platform-quality-operations.technology-cost-allocation-optimization` |
| 소프트웨어·제품 엔지니어링 | `candidate.software-product-engineering.accessible-ui-state-interaction` |
| 소프트웨어·제품 엔지니어링 | `candidate.software-product-engineering.layered-software-verification` |
| 소프트웨어·제품 엔지니어링 | `candidate.software-product-engineering.version-control-change-integration` |

보안·법무 대분류는 10개 전부 고위험 전수 대상이고, 플랫폼 대분류는 D3 8개와
남은 일반 후보 2개를 모두 포함하므로 두 분야는 사실상 100% 재검수합니다.
