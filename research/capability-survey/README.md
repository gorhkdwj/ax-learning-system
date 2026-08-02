# Phase 2 AX 역량지도 전수조사 작업대

이 디렉터리는 정규 카탈로그에 넣기 전 후보 역량을 조사·감사·통합하는
staging 영역입니다. Candidate는 학습 Unit이나 현재 학습 배정이 아닙니다.

## 정본

- Claude 온보딩: `docs/research/claude-phase2-onboarding.md`
- 실행 Runbook: `docs/research/phase2-capability-survey-runbook.md`
- 후보 스키마: `schemas/capability-candidate.schema.json`
- 후보 템플릿: `templates/research/capability-candidate.template.json`
- Phase 2 완료 시점 분류 Registry: `taxonomy/taxonomy.json`
  (`taxonomy.ax-capability-map@1.1.0`; 후속 학습 설계 버전은 Registry 정본 참조)
- 분류 스키마: `schemas/capability-taxonomy.schema.json`
- 분야 보고서 템플릿: `templates/research/domain-survey.template.md`
- Checkpoint 템플릿: `templates/research/wave-checkpoint.template.md`
- Claude→Codex 인계 계약: `research/capability-survey/handoffs/README.md`
- 인계 스키마: `schemas/phase2-handoff.schema.json`
- 현재 상태: `research/capability-survey/checkpoints/wave-07.md`
- Phase 2 완료 보고서: `research/capability-survey/waves/wave-07/phase2-completion-report.md`

## 쓰기 규칙

- 승인된 총괄 메인 세션만 이 디렉터리에 씁니다.
- 서브에이전트는 읽기·검색 결과만 반환합니다.
- 각 작업 패키지는 독립 경로를 소유합니다.
- 후보 전문을 분야 요약이나 Checkpoint에 복제하지 않습니다.
- 기존 `catalog/`, `sets/`, `research/signals/`를 조사 단계에서 수정하지 않습니다.
- Candidate 또는 Signal 승격은 사용자 승인 후 별도 작업으로 수행합니다.

## 검증

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

## 현재 상태

Wave 2의 다섯 패키지와 Wave 3의 네 패키지는 조사·독립 감사·사용자 승인·
정규 메타데이터 승격을 완료했습니다. Wave 4에서는 Candidate 96개를 10개
조사 렌즈, 8개 역할 관점과 12개 횡단 품질축으로 교차 점검하고 개발자 기술스택
편향을 레드팀 검토했습니다. 라우팅 없는 신규 고우선 공백은 0개였으며 신규
Candidate를 만들지 않았습니다. Wave 5에서는 Candidate 96개의 명칭·alias·
목적지·관계를 정규화하고 Wave 1의 승인 후보 7개 Unit·7개 Reference·1개 Set을
정규 승격했습니다. Taxonomy는 canonical node 107개와 provisional node 3개인
`taxonomy.ax-capability-map@1.0.0`으로 전환했습니다. Wave 6에서는 고위험·D3·
논쟁 후보 30개와 일반 층화표본 26개를 세 독립 감사축으로 재검수하고 P0·P1을
0건으로 교정했습니다. Wave 7에서는 Registry를 1.1.0으로 갱신하고 Wave 4의
8개 역할 관점을 active view로 조립하고 세 독립 완료 감사를 통과했습니다.
사용자가 `2026-08-02`에 완료를 승인하여 현재 상태는 `phase_complete`입니다.

Wave 2의 첫 작업 패키지 `wp.ai-literacy-trust.breadth-a`는 Candidate 10개와
evidence 22건, 고유 URL 13개로 구성되며 정규 승격 상태입니다. 구성은 신규
Unit 후보 8개, 기존 `unit.foundation.evidence-verification@1.0.0` 병합 1개,
Resource 전용 1개입니다. 읽기 전용 감사자가 근거·분류·실무성을 독립 감사했고
최초 P0는 0건이며 P1은 교정했습니다. 과목·후보 표시명은 한국어를 우선하고 node
ID와 영문 병기는 허용한다는 명명 원칙도 승인되었습니다.

Wave 1~3에서 `taxonomy.ax-capability-map@0.10.0`까지 조사 렌즈와 잠정
subdomain을 누적했습니다. Wave 5 정규화에서 1.0.0을 확정했고 Wave 7 역할
view 조립 후 Phase 2 완료 시점 Registry는 `taxonomy.ax-capability-map@1.1.0`입니다. 10개
domain과 근거가 확인된 97개 subdomain은 canonical, deferred 근거만 있는
3개 subdomain은 provisional입니다.

두 번째 작업 패키지 `wp.ai-systems-agents.breadth-a`는 한국어 우선 표시명의
Candidate 8개로 조사·감사를 완료한 `promoted` 상태입니다. 전문 판단이 필요한
구조·재사용·Adapter·전이성·평가 Gate는 사용자의 위임에 따라 운영 기본값으로
확정했습니다. 구성은
LLM 응용 계약, 시스템 컨텍스트, 구조화 출력, AI 도구, 상태·메모리·인계,
시스템 평가의 Unit 후보 6개와 종단 간 RAG, workflow·agent 토폴로지의 Set 후보
2개입니다. 독립 근거·taxonomy·실용성 재감사에서 P0·P1 0건을 확인했습니다.

사용자의 후속 지시에 따라 두 패키지의 승인 결과를 정규 구조로 승격했습니다.
신규 Unit 후보 14개는 `catalog/items/`의 `cataloged` Unit과 공개 Reference
Resource로, RAG와 workflow·agent 토폴로지 후보는 `sets/`의 `cataloged`
Set으로 등록했습니다. Content provenance 후보는 기존 근거 검증 Unit의
Resource로 등록했고 병합 후보는 기존 Unit을 그대로 사용합니다.

`cataloged`는 정규 메타데이터 등록을 뜻하며 상세 교재·독립 평가 타당성·학습효과
또는 업무효과 검증 완료를 뜻하지 않습니다. `Agent Harness`와 `Loop Engineering`
Signal은 수정하지 않았습니다.

세 번째 작업 패키지 `wp.software-product-engineering.breadth-a`는 한국어 우선
표시명의 Candidate 10개로 조사·감사를 완료한 `promoted` 상태입니다. 구성은
요구사항, 모듈 설계, 버전관리, API, 관계형 DB, 접근 가능한 UI, 계층형 테스트,
디버깅, 빌드 재현성의 Unit 후보 9개와 AI 보조 변경 전달 Set 후보 1개입니다.
독립 근거·taxonomy·실용성 재감사에서 P0·P1 0건을 확인했습니다. 이 세 번째
패키지의 후속 승인에 따라 Unit 후보 9개는 공개 Reference와 함께 정규
`cataloged` Unit으로, AI 보조 변경 전달 후보는 정규 `cataloged` Set으로
승격했습니다. 상세 교재·파일럿·학습효과는 아직 검증하지 않았습니다.

네 번째 작업 패키지 `wp.data-analytics-ml.breadth-a`는 한국어 우선 표시명의
신규 Candidate 9개와 기존 영향평가 Candidate 재사용 1개로 조사·감사를 완료한
`promoted` 상태입니다. 구성은 데이터 원천계약, 변환 pipeline, 분석 지표
의미계약, 탐색·통계 분석, 데이터 품질, 카탈로그·계보·책임 메타데이터,
예측 ML 문제정의·기준선, 예측 ML 모델 검증, ML 생명주기의 Unit 후보입니다.
기존 `candidate.ax-strategy-value.pilot-impact-evaluation@1.0.0`은 새 ID로
복제하지 않고 열 번째 결과로 재사용했습니다. 독립 감사에서 발견한 P1을
교정한 뒤 P0·P1 0건을 재확인했습니다. 후속 사용자 승인에 따라 신규 후보 9개와
기존 영향평가 재사용 1개를 공개 Reference와 함께 정규 `cataloged` Unit으로
승격했습니다. 상세 교재·파일럿과 학습효과는 아직 검증하지 않았습니다.

다섯 번째 작업 패키지 `wp.integration-automation.breadth-a`는 한국어 우선
표시명의 Candidate 10개로 조사·감사를 완료한 `promoted` 상태입니다. 구성은
외부 API 소비, 이벤트·웹훅, 결정적 workflow, 부작용 안전성, 비즈니스 규칙,
자동화 결과판정과 UI 구동 자동화의 Unit 후보 7개, SaaS 커넥터 동기화 Set
후보 1개, MCP technology Adapter 후보 1개와 결정적 workflow·agent 경계를
설명하는 D0 Resource 후보 1개입니다. 독립 근거·taxonomy·실용성 감사의 P1을
교정하고 잔여 유지관리 권고를 기록한 뒤 P0·P1 0건을 재확인했습니다. 후속
사용자 승인에 따라 핵심 Unit 7개, `protocol` Unit으로 등록한 MCP technology
Adapter 1개, SaaS 프로젝트 Set 1개와 결정적 workflow Unit 소유의 D0 경계
Resource 1개를 공개 Reference와 함께 정규 `cataloged` 메타데이터로
승격했습니다. 상세 fixture·교재·파일럿과 학습효과는 아직 검증하지 않았습니다.

Wave 3 첫 작업 패키지 `wp.human-ai-experience.breadth-a`는 한국어 우선
표시명의 Candidate 9개를 조사·감사했습니다. mental model·온보딩, 사용자
질문 중심 설명, 피드백·통제, 승인·이관, 대화 복구와 Human-AI 경험 평가의
Unit 후보 6개와 접근 가능한 다중양식 요구, 사회적 단서·의인화 경계의 D0
Resource 후보 2개는 `accepted`입니다. 개인화·기억 통제 후보 1개는 장기
memory lifecycle 직접 근거를 보강할 때까지 `deferred`입니다. 독립 감사의
P1을 교정하고 P0·P1 0건을 재확인했으며 정규 승격, 상세 prototype·파일럿과
학습효과는 아직 수행·검증하지 않았습니다. 후속 사용자 승인과 승격 전·후
이중 검수에 따라 accepted Unit 후보 6개는 공개 Reference와 함께 정규
`cataloged` Unit으로, D0 Resource 후보 2개는 기존 접근 가능한 UI Unit과
신규 기대형성·온보딩 Unit이 소유하는 정규 Resource로 승격했습니다. 개인화·
기억 후보와 provisional node는 조사 공백 추적을 위해 그대로 유지했습니다.

Wave 3 두 번째 작업 패키지 `wp.platform-quality-operations.breadth-a`는
안전한 릴리스, 선언적 환경, 서비스 telemetry, SLI·SLO, 사고대응, 백업·복원,
성능·용량, 기술비용과 복원력의 Unit 후보 9개, 서비스 운영준비·수명주기
Set 후보 1개를 조사했습니다. 내부 플랫폼 독립 Unit은 실제 내부 사용자 조사와
operating model 근거가 필요해 `organization-adoption` 후속 범위로 유보했습니다.
승격 전·후 독립 근거·taxonomy·실용성 전수검수에서 P0·P1 0건을 확인한 뒤
9개 Unit·9개 공개 Reference·1개 Set을 정규 `cataloged` 메타데이터로
승격했습니다. 실제 production 적합성, 상세 simulator·교재·파일럿과
학습효과는 아직 검증하지 않았습니다.

Wave 3 세 번째 작업 패키지 `wp.security-legal-governance.breadth-a`는
보안 요구·위협 모델, 접근정책, secret·key lifecycle, 소프트웨어 공급망,
privacy 영향·권리, 보안사고 evidence, 통제감사, 디지털 자산 권리 provenance,
AI 보안평가의 Unit 후보 9개와 AI 위험·영향 거버넌스 Set 후보 1개를
조사했습니다. 승격 전·후 독립 3축 재감사에서 최종 P0·P1 0건을 확인한 뒤
9개 Unit·9개 공개 Reference·1개 Set을 정규 `cataloged` 메타데이터로
승격했습니다. 실제 관할·법률·규제·위험수용 판단은 qualified owner 검토
대상이며 상세 fixture·runner와 학습효과는 활성화 전 후속 Gate입니다.

Wave 3 네 번째 작업 패키지 `wp.organization-adoption.breadth-a`는 변화 영향·
준비도·참여, 운영모델·의사결정권, workforce 역량 gap·전환, 학습·업무전이,
포용적 직무영향·지원, adoption support·지식흐름, aggregate 성과·분배효과,
pilot·scale·rollback, vendor·SaaS 전문 이관의 Unit 후보 9개와 lifecycle
Set 후보 1개를 조사했습니다. 승격 전·후 독립 3축 재감사에서 최종
P0·P1·P2 0건을 확인하고 9개 Unit·9개 공개 Reference와 필수 8개·조건부
5개인 13단계 Set을 정규 `cataloged` 메타데이터로 승격했습니다.

현재 카탈로그 검증 기준은 Unit 83개, Resource 89개, Set 9개, Candidate
96개와 Signal 3개입니다. `cataloged`는 정규 메타데이터 등록을 뜻하며 실제
fixture·runner, 상세 교재, 조직 tailoring, 파일럿, 학습·업무효과 검증
완료를 뜻하지 않습니다.
