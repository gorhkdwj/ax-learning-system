# Claude Phase 2 온보딩

이 문서는 Claude가 Phase 2 AX 역량지도 전수조사를 처음 인수할 때 사용하는
진입점입니다. 조사 규칙의 정본은 Runbook과 현재 Checkpoint이며, 이 문서는
그 내용을 복제하지 않고 첫 응답과 최종 인계 형식만 고정합니다.

## 사용 방법

1. 새 Claude Code 세션을 저장소 루트에서 시작합니다.
2. `/memory`, `/agents`, `/doctor`로 프로젝트 지침과 custom agent 상태를 확인합니다.
3. 아래 프롬프트를 그대로 전달합니다.
4. Claude의 첫 응답에서 승인 요청 사항을 검토한 뒤에만 시험 배치 시작을 승인합니다.

## 바로 전달할 온보딩 프롬프트

```text
이 저장소의 Phase 2 AX 역량지도 전수조사를 인수하십시오.

지금은 실제 후보 조사를 시작하지 말고 온보딩과 Wave 0 승인 준비까지만
수행하십시오. 저장소 루트의 CLAUDE.md를 진입점으로 삼아 다음 정본을 순서대로
읽으십시오.

1. AGENTS.md
2. docs/governance/learning-governance.md
3. docs/architecture/learning-system.md
4. docs/research/trend-signal-governance.md
5. docs/research/phase2-capability-survey-runbook.md
6. research/capability-survey/README.md
7. research/capability-survey/checkpoints/wave-00.md
8. schemas/capability-candidate.schema.json
9. templates/research/capability-candidate.template.json
10. schemas/phase2-handoff.schema.json
11. research/capability-survey/handoffs/README.md

읽은 파일과 현재 파일 상태를 대조한 뒤 아래 항목을 순서대로 보고하십시오.

## 1. 온보딩 확인
- 실제로 읽은 정본 파일
- 현재 Phase, Wave, 마지막 Checkpoint
- 현재 조사 시작 여부
- 메인 세션과 read-only 서브에이전트의 역할

## 2. 이해한 조사 계약
- 목표와 명시적 비목표
- 조사 렌즈, 포함 범위, 제외 범위
- Candidate와 정규 Catalog/Set/Signal의 경계
- 사용자 승인 없이 할 수 없는 변경
- 중단 조건

## 3. 첫 시험 배치 제안
- work package ID와 소유 출력 경로
- 조사할 렌즈와 최대 후보 수
- 사용할 서브에이전트와 각 역할
- 조사·증거·분류·실무성 감사 절차
- 예상 산출물
- 완료 및 검증 기준

## 4. 불일치와 위험
- 정본 간 충돌, 누락 파일, 모호한 규칙
- 발견하지 못했다면 “확인된 불일치 없음”이라고 명시

## 5. 승인 요청
- 사용자가 승인해야 할 항목만 번호 목록으로 제시
- 승인 전에는 후보 조사, 파일 작성, Catalog/Set/Signal 승격을 시작하지 말 것

작업 중에는 다음 제약을 지키십시오.

- Claude 메인 세션만 파일을 작성합니다.
- custom subagent는 조사와 감사 결과만 반환하는 read-only 역할입니다.
- 각 work package는 자신의 경로만 소유합니다.
- Candidate는 제안이며 정규 학습 항목이 아닙니다.
- 최신성 주장에는 확인일과 근거가 필요합니다.
- 근거가 부족한 내용은 사실처럼 보완하지 말고 미검증 또는 보류로 기록합니다.
- 정본 충돌, 검증 실패, 범위 초과가 발생하면 즉시 중단하고 보고합니다.

Claude 측 작업 범위가 끝날 때에는
research/capability-survey/handoffs/README.md의 계약에 따라 handoff.json과
handoff.md를 작성하고 아래 두 명령이 통과한 상태로 남기십시오.

python tools/validate_catalog.py
python -m unittest discover -s tests -v

최종 답변의 마지막에는 설명을 덧붙이지 말고 다음 인계 영수증을 실제 값으로
채워 출력하십시오.

HANDOFF_RECEIPT
handoff_json: research/capability-survey/handoffs/<실제 폴더>/handoff.json
handoff_markdown: research/capability-survey/handoffs/<실제 폴더>/handoff.md
status: <partial|ready_for_review|blocked|phase_complete>
validation: <pass|fail>
next_action: <handoff.json의 resume.next_action과 같은 문장>
END_HANDOFF_RECEIPT
```

## 첫 응답 승인 기준

다음 조건을 모두 만족할 때 시험 배치를 승인할 수 있습니다.

- 조사 미시작 상태를 정확히 인식했습니다.
- 10개 조사 렌즈를 확정안이 아니라 승인 대기안으로 구분했습니다.
- 첫 시험 배치를 최대 10개 후보로 제한했습니다.
- 메인 세션만 쓰고 서브에이전트는 읽기 전용으로 사용합니다.
- Candidate를 Catalog/Set/Signal로 자동 승격하지 않습니다.
- 출력 경로, 감사 절차, 검증 명령, 중단 조건을 명시했습니다.
- 불확실한 사항을 임의로 결정하지 않고 승인 요청으로 분리했습니다.

## 작업 종료 시 인계 기준

인계는 사람이 읽는 `handoff.md`와 기계가 검사하는 `handoff.json` 두 파일로
구성합니다. Codex는 JSON을 기준으로 범위, 산출물, 검증 결과, 미해결 사항,
다음 행동을 복원하고 Markdown으로 판단 배경을 확인합니다.

- 형식 계약: `schemas/phase2-handoff.schema.json`
- JSON 예시: `templates/research/phase2-handoff.template.json`
- 사람용 예시: `templates/research/phase2-handoff.template.md`
- 운영 규칙: `research/capability-survey/handoffs/README.md`

사용자는 Claude의 마지막 답변 전체를 전달할 필요가 없습니다. 인계 영수증이나
`handoff.json` 경로만 Codex에 알려주면 Codex가 스키마, 실제 파일, Checkpoint,
검증 결과를 다시 대조한 뒤 후속 작업을 이어갈 수 있습니다.
