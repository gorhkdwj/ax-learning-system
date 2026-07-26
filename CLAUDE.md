@AGENTS.md

# Claude Code 프로젝트 진입점

이 파일은 Claude Code가 `AGENTS.md`를 자동으로 읽도록 연결하는 얇은
호환 계층입니다. 기존 거버넌스 내용을 이 파일에 복제하지 않습니다.

## Phase 2 전수조사

Phase 2 전수조사를 요청받았을 때 다음 문서를 순서대로 읽으십시오.

1. `docs/research/claude-phase2-onboarding.md`
2. `docs/research/phase2-capability-survey-runbook.md`
3. `research/capability-survey/README.md`
4. `research/capability-survey/checkpoints/wave-00.md` 또는 현재 Wave Checkpoint
5. 작업 패키지에서 지정한 스키마와 템플릿

일반 Claude 메인 세션이 총괄과 유일한 파일 작성자를 맡습니다. 프로젝트 기본
agent를 변경하지 마십시오.

프로젝트 전용 조사 에이전트는 `.claude/agents/`에 있습니다.

- `ax-domain-researcher`
- `ax-evidence-auditor`
- `ax-taxonomy-auditor`
- `ax-practicality-auditor`

서브에이전트는 읽기·검색만 수행하고 결과를 반환합니다. 메인 세션만 승인된
`research/capability-survey/` 작업 패키지 경로에 파일을 작성합니다.

## 강제 경계

- Candidate는 정규 Unit·Set·Resource·Trend Signal이 아닙니다.
- 조사 에이전트 결과를 감사 없이 확정하지 마십시오.
- 승인된 Wave manifest 밖으로 범위를 확장하지 마십시오.
- 사용자 승인 없이 스키마·거버넌스·기존 ID를 변경하지 마십시오.
- 사용자 승인 없이 Candidate나 Signal을 정규 카탈로그로 승격하지 마십시오.
- `catalog/`, `sets/`, `research/signals/`와 생성 HUB를 Phase 2 조사 중 수정하지 마십시오.
- 한 작업 패키지에서 후보 25개를 넘기지 마십시오.
- 첫 시험 배치는 후보 10개 이하로 제한하고 사용자 승인을 기다리십시오.
- 대화 기록을 정본으로 사용하지 말고 매 Wave Checkpoint를 갱신하십시오.

## 검증

변경 후 작업공간 루트에서 실행하십시오.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

검증 실패, 할당 밖 파일 수정, 출처의 중대한 오류, 기존 사용자 변경과의 충돌,
삭제·이동·기존 ID 변경 필요가 발생하면 추가 쓰기를 중단하고 보고하십시오.

Claude 측 작업 범위를 종료할 때에는
`research/capability-survey/handoffs/README.md`에 따라 기계 판독형
`handoff.json`과 사람용 `handoff.md`를 함께 작성하십시오.

Claude Code 설정을 확인할 때에는 세션 안에서 `/memory`, `/agents`, `/doctor`를
사용하십시오. 비밀정보나 인증정보를 프로젝트 파일에 기록하지 마십시오.
