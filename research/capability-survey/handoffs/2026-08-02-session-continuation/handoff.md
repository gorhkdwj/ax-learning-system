# 새 로컬 세션 작업 인계

## 1. 가장 먼저 확인할 상태

이 인계는 대화 기록을 대신하는 새 세션 진입점입니다. 기계 판독형 정본은 같은
폴더의 `handoff.json`이며, 실제 Git 상태와 충돌하면 Git과 현재 Checkpoint를
우선합니다.

```text
Phase 2 완료 기준 커밋: 62506b8e04cb62b0e1072476a012f6ee34ef70d3
Public main·origin/main: 이 인계 문서 커밋을 포함한 동일 SHA인지 새 세션에서 확인
Vault main: ed2e9ad7a00a0830321cc3ca49f1a3ec73d4d57f
Public worktree: clean
Vault worktree: clean
상위 AX/.git: 없음
현재 상태: phase_complete
```

새 세션에서는 작업 전에 `git fetch origin main`을 실행하고 로컬 HEAD와 원격
main이 같은지, Phase 2 완료 기준 커밋이 현재 main의 조상인지 확인하십시오.
원격이 더 진행되었으면 새 원격 상태를 정본으로 사용하고 기존 변경을 덮어쓰지
마십시오.

## 2. 완료된 작업

### 작업공간 Bootstrap

- 커밋 `c931472 feat: add workspace bootstrap`
- `tools/bootstrap-workspace.ps1`과 상위 진입점 템플릿 3개를 Public에 등록했습니다.
- 상위 AX에는 Git을 만들지 않고 Public을 기준으로 Vault와 진입점 파일을 안전하게
  재구성합니다.

### Phase 2 조사와 정규 승격

- Wave 1~3: Candidate 96개 조사·독립 감사와 승인 결과 정규 승격
- Wave 4 `b36f558`: 10개 렌즈·8개 역할·12개 품질축 Coverage와 편향 검토
- Wave 5 `d280771`: 후보·목적지·관계 정규화와 taxonomy 1.0.0 확정
- Wave 6 `17ea78e`: 고위험·D3·논쟁 30개 전수, 일반 26개 층화표본 독립 QA
- Wave 7 `62506b8`: taxonomy 1.1.0, active role view 8개, 최종 역량지도와
  Phase 2 완료 감사

현재 Candidate 판정은 accepted 93, merged 1, deferred 1, needs_review 1입니다.
목적지는 Unit 후보 80, Set 후보 8, Resource-only 4, Adapter 1, 기존 병합 1,
defer 2로 합계 96입니다.

## 3. 지금 읽을 정본

1. `AGENTS.md`, `CLAUDE.md`
2. `research/capability-survey/checkpoints/wave-07.md`
3. `research/capability-survey/waves/wave-07/capability-map.md`
4. `research/capability-survey/waves/wave-07/phase2-completion-report.md`
5. `docs/research/phase2-capability-survey-runbook.md`
6. `taxonomy/taxonomy.json`

Phase 2 결과는 canonical domain 10개, canonical subdomain 97개, provisional
subdomain 3개와 active role view 8개입니다. Role view의 active는 탐색 가능
상태이며 개인별 필수과정, 상세 교재 완료나 실제 효과 검증을 뜻하지 않습니다.

## 4. 완료 승인과 다음 작업

### Phase 2 완료 승인

사용자가 `2026-08-02`에 최종 역량지도와 Phase 2 완료 감사 보고서를 승인했습니다.
`handoff.json`의 상태는 `phase_complete`, 승인 상태는 `approved`로 전환했습니다.
이 승인은 상세 교재·개인별 우선순위·실제 효과 검증의 완료를 뜻하지 않습니다.

### 즉시 다음 행동

1. Phase 3에서 8개 role view를 입력으로 사용자 업무·역량·제약을 확인합니다.
2. 가치·선행관계·안전·유지비를 기준으로 우선순위를 평가합니다.
3. 80 Unit·8 Set을 한꺼번에 제작하지 않고 소수 우선 패키지를 먼저 선택합니다.
4. 선택된 패키지만 fixture·runner·교재·전이평가 Gate를 구현합니다.

### 비차단 후속 정리

- 15 Candidate·25 evidence의 빈 `source_version`을 공식 원문에서 확인합니다.
- Wave 5 source projection의 `source_type` 5건·`source_version` 7건 차이에 대한
  정규화 정책을 정합니다.
- 개인화·장기 memory, 편익 실현, `operational-value`와 Wave 4 후속 공백은 각
  재개 조건이 충족될 때만 다시 조사합니다.
- planned 엔지니어링 view 3개는 실제 사용례·subdomain 영향분석과 사용자 승인
  전까지 활성화·병합·대체하지 않습니다.

## 5. 검증과 환경 주의

작업공간 루트에서 다음을 실행합니다.

```powershell
.\ax-learning-system\tools\verify.ps1
```

마지막 확인 결과는 Public boundary 오류 0, catalog 오류·경고 0, 단위 테스트
33/33 통과입니다. 이 PC에서 `python`이 Windows Store 별칭을 가리키면 실제
Python이 PATH에서 먼저 해석되게 하거나 다음 하위 명령을 `py -3`으로 실행해
같은 내용을 확인하십시오.

```powershell
py -3 tools/check_public_boundary.py
py -3 tools/validate_catalog.py
py -3 -m unittest discover -s tests -v
git diff --check
```

`codex-windows-sandbox-setup.exe` 미발견과 `UserPromptSubmit hook exited with
code 1` 메시지는 저장소 밖 로컬 도구 문제로 관찰되었습니다. 지금까지 Git 작업,
Public 검증과 Vault 상태에는 영향을 주지 않았습니다. 새 세션에서 계속 발생하면
저장소 변경과 분리하여 Codex 설치·hook 설정을 진단하십시오.

## 6. 저장소 경계

- Public과 Vault를 한 명령으로 함께 커밋하거나 푸시하지 않습니다.
- Vault HEAD `ed2e9ad`와 clean 상태를 유지합니다.
- Vault의 원문·임베딩·개인 진행자료는 Git 복원 대상이 아니며 ignore 정책을
  유지합니다.
- 상위 AX는 Git 저장소가 아니어야 합니다.
- Public에 Vault 원문, 개인정보, 절대경로와 인증정보를 기록하지 않습니다.

## 7. 새 세션에 전달할 한 문장

다음 문장과 `handoff.json` 경로만 전달해도 됩니다.

> `research/capability-survey/handoffs/2026-08-02-session-continuation/handoff.json`을
> 검증하고 Phase 3 역할별 우선순위 평가를 위한 사용자 업무·역량·제약 확인부터
> 재개하십시오. 상세 패키지는 우선순위가 확정된 소수 항목만 구현하십시오.
