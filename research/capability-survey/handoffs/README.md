# Phase 2 조사 인계

이 디렉터리는 Claude가 종료한 조사 범위를 Codex가 이어받기 위한 정형 인계
공간입니다. 대화 요약만으로 상태를 복원하지 않고, 파일과 검증 결과를 기준으로
재개합니다.

## 폴더와 파일

인계마다 다음 구조를 사용합니다.

```text
research/capability-survey/handoffs/
  YYYY-MM-DD-claude-to-codex/
    handoff.json
    handoff.md
```

- `handoff.json`: 기계 판독형 정본입니다.
- `handoff.md`: 사람이 빠르게 검토할 요약입니다.
- 같은 사실이 충돌하면 `handoff.json`과 실제 저장소 상태를 우선합니다.

## 작성 절차

1. `templates/research/phase2-handoff.template.json`을 복사하여 실제 값으로
   교체합니다.
2. `artifacts`에는 작업 중 생성·수정·검토한 파일을 상대경로로 기록합니다.
3. Candidate 상태 수와 work package별 Candidate 수를 실제 파일과 맞춥니다.
4. 미검증 주장, 충돌, 위험, 사용자 질문을 빈칸으로 숨기지 말고 `open_items`에
   기록합니다.
5. 사용자 승인 요청과 실제 승인 여부를 `approval`에 구분하여 기록합니다.
6. 다음 담당자가 처음 읽을 파일, 단일 다음 행동, 예상 출력, 승인 필요 여부,
   중단 조건을 `resume`에 기록합니다.
7. `handoff.md`에는 판단 배경과 사용자가 확인할 핵심만 요약합니다.
8. 아래 검증을 실행한 뒤 실제 종료 코드와 결과를 `quality`에 기록합니다.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

## 상태 의미

| 상태 | 의미 |
|---|---|
| `partial` | 정상 중간 종료이며 후속 작업이 남았습니다. |
| `ready_for_review` | 계획한 작업은 끝났고 사용자 또는 Codex 검토가 필요합니다. |
| `blocked` | 명시된 충돌·실패·권한 문제로 진행할 수 없습니다. |
| `phase_complete` | Phase 전체 완료 조건과 사용자 승인이 충족되었습니다. |

`phase_complete`는 단순히 Claude에게 배정된 범위가 끝났다는 뜻으로 사용하지
않습니다. 그 경우에는 `ready_for_review`를 사용합니다.

## Codex 재개 절차

Codex는 다음 순서로 인계를 검증합니다.

1. `handoff.json`의 스키마와 의미 검증
2. Checkpoint, work package, Candidate 수와 실제 파일 대조
3. `artifacts`에 기록된 변경과 저장소 상태 대조
4. 검증 명령 재실행
5. `open_items`와 승인 필요 여부 확인
6. `resume.next_action`을 기준으로 후속 계획 수립

인계 파일이 유효하지 않거나 실제 상태와 다르면 자동으로 작업을 이어가지 않고
불일치를 먼저 정리합니다.

## Claude 최종 응답 형식

Claude는 인계 파일 작성과 검증을 끝낸 뒤 최종 응답 마지막에 다음 영수증을
실제 값으로 출력합니다.

```text
HANDOFF_RECEIPT
handoff_json: research/capability-survey/handoffs/<실제 폴더>/handoff.json
handoff_markdown: research/capability-survey/handoffs/<실제 폴더>/handoff.md
status: <partial|ready_for_review|blocked|phase_complete>
validation: <pass|fail>
next_action: <handoff.json의 resume.next_action과 같은 문장>
END_HANDOFF_RECEIPT
```

사용자가 Codex에 이 영수증 또는 `handoff.json` 경로만 전달해도 재개할 수
있습니다. 대화 전문은 인계의 정본으로 사용하지 않습니다.
