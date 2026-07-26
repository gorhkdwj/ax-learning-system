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
- 현재 상태: `research/capability-survey/checkpoints/wave-01.md`

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

Wave 1의 `ax-strategy-value` 첫 시험 배치는 Candidate 10개와 evidence 34건,
고유 URL 25개로 구성됩니다. 최초 8개는 Codex 읽기 전용 감사자, 후속 누락
레드팀에서 추가한 포트폴리오 우선순위·전사 AX 로드맵 2개는 Orca로 조정한
Claude Code 감사자가 근거·분류·실무성을 독립 감사했습니다. 확인된 P0·P1은
교정되었고 정규 카탈로그에는 아직 승격하지 않았습니다. 조사 렌즈 10개와 Wave 1
후보용 하위 node 20개, 예제 Unit용 하위 node 2개는
`taxonomy.ax-capability-map@0.1.0`에 각각 `research_lens`와 `provisional`
상태로 등록되었습니다. 이는 정규 분류 확정이 아니라 Wave 2에서 분류 드리프트를
추적하기 위한 기준선입니다.
