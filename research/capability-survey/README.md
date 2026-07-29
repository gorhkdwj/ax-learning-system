# Phase 2 AX 역량지도 전수조사 작업대

이 디렉터리는 정규 카탈로그에 넣기 전 후보 역량을 조사·감사·통합하는
staging 영역입니다. Candidate는 학습 Unit이나 현재 학습 배정이 아닙니다.

## 정본

- Claude 온보딩: `docs/research/claude-phase2-onboarding.md`
- 실행 Runbook: `docs/research/phase2-capability-survey-runbook.md`
- 후보 스키마: `schemas/capability-candidate.schema.json`
- 후보 템플릿: `templates/research/capability-candidate.template.json`
- 분류 Registry: `taxonomy/taxonomy.json`
- 분류 스키마: `schemas/capability-taxonomy.schema.json`
- 분야 보고서 템플릿: `templates/research/domain-survey.template.md`
- Checkpoint 템플릿: `templates/research/wave-checkpoint.template.md`
- Claude→Codex 인계 계약: `research/capability-survey/handoffs/README.md`
- 인계 스키마: `schemas/phase2-handoff.schema.json`
- 현재 상태: `research/capability-survey/checkpoints/wave-02.md`

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

Wave 2의 첫 작업 패키지 `wp.ai-literacy-trust.breadth-a`는 Candidate 10개와
evidence 22건, 고유 URL 13개로 구성되며 사용자 승인 상태입니다. 구성은 신규
Unit 후보 8개, 기존 `unit.foundation.evidence-verification@1.0.0` 병합 1개,
Resource 전용 1개입니다. 읽기 전용 감사자가 근거·분류·실무성을 독립 감사했고
최초 P0는 0건이며 P1은 교정했습니다. 과목·후보 표시명은 한국어를 우선하고 node
ID와 영문 병기는 허용한다는 명명 원칙도 승인되었습니다.

`taxonomy.ax-capability-map@0.5.0`에는 기존 조사 렌즈와 Wave 1 node에 더해
`ai-literacy-trust` 잠정 subdomain 7개와 `ai-systems-agents` 잠정 subdomain
7개, `software-product-engineering` 잠정 subdomain 9개,
`data-analytics-ml` 잠정 subdomain 9개가 등록되었습니다.

두 번째 작업 패키지 `wp.ai-systems-agents.breadth-a`는 한국어 우선 표시명의
Candidate 8개로 조사·감사를 완료한 `approved` 상태입니다. 전문 판단이 필요한
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
표시명의 Candidate 10개로 조사·감사를 완료한 `approved` 상태입니다. 구성은
요구사항, 모듈 설계, 버전관리, API, 관계형 DB, 접근 가능한 UI, 계층형 테스트,
디버깅, 빌드 재현성의 Unit 후보 9개와 AI 보조 변경 전달 Set 후보 1개입니다.
독립 근거·taxonomy·실용성 재감사에서 P0·P1 0건을 확인했습니다. 이 세 번째
패키지의 후속 승인에 따라 Unit 후보 9개는 공개 Reference와 함께 정규
`cataloged` Unit으로, AI 보조 변경 전달 후보는 정규 `cataloged` Set으로
승격했습니다. 상세 교재·파일럿·학습효과는 아직 검증하지 않았습니다.

네 번째 작업 패키지 `wp.data-analytics-ml.breadth-a`는 한국어 우선 표시명의
신규 Candidate 9개와 기존 영향평가 Candidate 재사용 1개로 조사·감사를 완료한
`approved` 상태입니다. 구성은 데이터 원천계약, 변환 pipeline, 분석 지표
의미계약, 탐색·통계 분석, 데이터 품질, 카탈로그·계보·책임 메타데이터,
예측 ML 문제정의·기준선, 예측 ML 모델 검증, ML 생명주기의 Unit 후보입니다.
기존 `candidate.ax-strategy-value.pilot-impact-evaluation@1.0.0`은 새 ID로
복제하지 않고 열 번째 결과로 재사용했습니다. 독립 감사에서 발견한 P1을
교정한 뒤 P0·P1 0건을 재확인했으며, 후보 정규 Unit 승격과 상세 교재·파일럿은
아직 수행하지 않았습니다.
