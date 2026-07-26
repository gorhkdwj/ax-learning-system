# Work Package Manifest: wp.ax-strategy-value.pilot

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-01` |
| 상태 | `ready_for_review` |
| 범위 승인일 | `2026-07-26` |
| 범위 승인 근거 | 사용자가 병렬 조사 실행과 실패 시 백업 경로 전환을 승인함 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 최대 후보 | `10` |

## 조사 계약

### 포함

- AX 적용 기회의 가치발견과 문제정의
- 현재 업무·의사결정·프로세스의 구조화와 재설계
- 자동화·증강·비자동화 방식의 적합성 비교
- 기준선, 가치가설, KPI·보호지표와 효과측정
- 운영·유지보수 비용과 통제를 포함한 가치실현 판단
- 복수 후보의 포트폴리오 우선순위·재균형
- 전사 AX 역량 격차·의존성·실행 파동 로드맵

### 제외

- 특정 AI 제품의 사용법
- 상세 소프트웨어 구현
- 조직 전체 변화관리
- 상세 교재·실습·HUB 구축
- Candidate의 정규 Unit·Set·Resource·Trend Signal 승격

### 관점

- 경영·전략
- 현업 프로세스 소유자
- 제품·서비스 기획
- 데이터·분석
- 보안·위험·감사
- 운영·지원

## 실행 구조

1. 세 개의 읽기 전용 Codex 서브에이전트가 최초 후보 발견, 가치·측정 근거,
   taxonomy·학습경계를 독립 조사했습니다.
2. Codex 메인 세션이 중복을 제거하고 최대 10개 Candidate 초안을 작성합니다.
3. 최초 8개는 Codex 읽기 전용 감사자, 신규 2개는 Orca로 조정한 Claude Code
   읽기 전용 감사자가 근거, taxonomy, 실무성을 독립 감사했습니다.
4. Codex 메인 세션만 감사 결과를 반영하여 작업 패키지 파일을 작성합니다.
5. 자동 검증과 Checkpoint를 통과하기 전에는 다음 영역으로 확장하지 않습니다.

2026-07-26 최초 Candidate 8개와 evidence 27건은 evidence·taxonomy·practicality
독립 전수감사와 교정 후 재감사를 완료했습니다. 후속 자체 검토에서 전략
렌즈의 포트폴리오 우선순위와 전사 로드맵 누락을 발견하여 Candidate 2개와
evidence 8건을 추가했습니다. 2026-07-27 Orca로 조정한 Claude Code 감사자
3개가 신규 2개를 독립 감사했고 P0 2건과 P1을 교정했습니다. 부정확한 NDA
evidence를 삭제하여 최종 범위는 Candidate 10개·evidence 34건·고유 URL
25개이며 남은 P0·P1은 없습니다.

## 파일 소유권

Codex 메인 세션만 다음 경로에 쓸 수 있습니다.

```text
research/capability-survey/waves/wave-01/wp.ax-strategy-value.pilot/
  manifest.md
  domain-survey.md
  candidates/<candidate-id>/candidate.json
  audit/evidence-review.md
  audit/taxonomy-review.md
  audit/practicality-review.md
```

서브에이전트는 파일을 수정하지 않고 대화 결과만 반환합니다.

## 품질 Gate

- 후보 수는 10개 이하입니다.
- 모든 후보에 문제·포함·제외 범위와 관찰 가능한 행동이 있습니다.
- 모든 후보에 서로 다른 업무 전이 맥락이 있습니다.
- 정의와 범위를 지지하는 공식·표준·1차 또는 원 실무자 근거가 있습니다.
- 확인된 사실과 비즈니스 효과 가설을 구분합니다.
- 기존 Unit·Set·Signal과 목적지 경계를 검토합니다.
- evidence, taxonomy, practicality 감사를 후보 100%에 수행합니다.
- 검색군·출처 계층·역할 관점과 최소 1회의 누락 레드팀 패스를 기록합니다.
- 마지막 누락 패스의 새 고우선 후보가 0개이고 남은 공백을 명시적으로 라우팅합니다.
- P0는 0건이어야 하며 P1은 반영 또는 명시적 보류해야 합니다.
- 아래 두 명령이 오류 없이 통과해야 합니다.

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

## 자동 중단조건

- 필수 근거가 없거나 원문과 핵심 주장이 다릅니다.
- 승인된 포함·제외 범위를 벗어납니다.
- 후보 중복 비율이 15%를 초과합니다.
- 기존 사용자 파일과 충돌하거나 할당 밖 파일 수정이 필요합니다.
- 스키마·참조 검증 또는 회귀 테스트가 실패합니다.
- 사용자 업무에 대한 확인되지 않은 가정을 전사 범위로 일반화합니다.
- Candidate를 정규 카탈로그로 승격해야만 진행할 수 있습니다.

## 실행 경로 변경 기록

Claude CLI 외부 워커는 다음 사전 Gate에서 중단되었습니다.

1. Windows PowerShell에서 `--json-schema` 인라인 인자가 손상되었습니다.
2. 표준 JSON 응답 백업 호출은 종료코드 0이었으나 회수 가능한 출력이 없었습니다.
3. Claude 백그라운드 세션은 생성되지 않았고 Candidate 및 정규 카탈로그 파일도
   변경되지 않았습니다.

추가 사용량과 불확실성을 발생시키지 않기 위해 Claude CLI 원인 추적을 중단하고,
사용자가 승인한 백업 경로인 Codex 읽기 전용 서브에이전트 병렬 조사로
전환했습니다.

2026-07-27에는 Orca CLI의 공식 orchestration 경로로 Claude Code 터미널
사전 Gate를 다시 수행했습니다. 작업공간 신뢰 확인과 읽기 전용 응답 Gate를
통과한 뒤 근거·분류·실무성 Task 3개를 병렬 dispatch했고, 세 Worker의
`worker_done`을 모두 수신했습니다. Worker는 파일을 수정하지 않았으며 Codex
메인 세션만 결과를 판정하고 교정했습니다. 따라서 과거의 직접 Claude CLI
구조화 출력 실패와 이번 Orca 조정 성공은 서로 다른 실행 경로의 기록입니다.
