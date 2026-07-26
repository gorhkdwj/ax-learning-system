# Phase 2 Wave Checkpoint: wave-01

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-01` |
| 상태 | `ready_for_wave-02-planning` |
| 시작일 | 2026-07-26 |
| 마지막 갱신일 | 2026-07-27 |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 후보 스키마 | `capability-candidate 1.1.0` |
| 분류 Registry | `taxonomy.ax-capability-map@0.1.0` (`provisional`) |
| 작업 패키지 | `wp.ax-strategy-value.pilot` |

## 2. 목표와 비목표

### 완료한 목표

- `ax-strategy-value` 조사 렌즈의 첫 시험 배치
- 최대 10개 범위 안에서 후보 발견·중복 제거·목적지 라우팅
- 최초 8개 후보의 evidence·taxonomy·practicality 100% 독립 감사
- 최초 8개 후보의 모든 P0 교정과 전수 재감사
- 전략 누락 레드팀과 포트폴리오·전사 로드맵 후보 2개 자체 보완
- Orca로 조정한 Claude Code 감사자 3개의 신규 2개 근거·분류·실무성 독립 감사
- 신규 2개에서 확인된 P0·P1 교정과 전수 재검증
- 검색군·역할 관점·반복 패스 기반 커버리지 근거 기록
- 조사 렌즈 10개, Wave 1 후보용 하위 node 20개와 예제 Unit용 node 2개의
  Registry 기준선 및 자동 참조 검증

### 비목표

- 전체 10개 조사 렌즈 전수조사
- 상세 교재·실습·HUB 구축과 학습 우선순위
- Candidate의 정규 Unit·Set·Resource·Signal 승격

## 3. 작업 패키지 현황

| Work package | 담당 | 상태 | 후보 | 출력 | 마지막 검증 |
|---|---|---|---:|---|---|
| `wp.ax-strategy-value.pilot` | Codex + 최초 Codex 감사자 + 신규 Orca·Claude 감사자 | ready_for_review | 10 | `research/capability-survey/waves/wave-01/wp.ax-strategy-value.pilot/` | 2026-07-27 |

후보 구성은 Unit 후보 8개, Set 후보 1개, 보류 1개입니다. 영향평가 Unit
후보는 소유권상 `data-analytics-ml`로 이관되므로 현재 렌즈에 남는 Unit
후보는 7개입니다. 신규 Unit 후보 2개도 독립 감사와 P0·P1 교정을 마쳤으며
사용자 검토 전에는 정규 카탈로그로 승격하지 않습니다.

## 4. 결정 기록

### 유지

- 기회·가치가설 프레이밍
- 현행 업무시스템 분석
- 과업 분해와 인간-AI 역할 배분
- 기술중립적 해법 적합성 평가
- AX 성과 측정계약 설계
- AX 후보 포트폴리오 우선순위·재균형 — 유지 제안
- 전사 AX 역량 로드맵 설계 — 유지 제안

### 이관·조합·보류

- 미래 인간-AI 업무시스템 설계:
  `set.deliverable.ax-future-state-work-design` 후보
- 개입 영향평가 설계:
  `unit.data-analytics-ml.intervention-impact-evaluation` 후보
- 편익 실현·가치 추적:
  일반 편익관리와 중복되어 `defer`
정규 카탈로그에는 아무 항목도 승격하지 않았습니다.

## 5. Coverage Matrix

| 중분류 | 업무행동 | 역할 관점 | 품질축 | 공식·1차 근거 | 상태 |
|---|---|---|---|---|---|
| 포트폴리오 전략 | 충분 | 경영·전략·재무·위험 | 비용·법무·승인 | 있음 | 감사·교정 완료 |
| 전사 역량 로드맵 | 충분 | 경영·현업·기술·운영 | 전 품질축 | 있음 | 감사·교정 완료 |
| 기회·가치 | 충분 | 전략·현업·제품 | 비용·승인 | 있음 | 감사 완료 |
| 현행 분석 | 충분 | 현업·운영·UX | 개인정보·관측성 | 있음 | 감사 완료 |
| 과업·역할 | 충분 | 현업·조직·위험 | 법무·권한·승인 | 있음 | 감사 완료 |
| 해법 적합성 | 충분 | 제품·개발·운영 | 전 품질축 | 있음 | 감사 완료 |
| 미래상태 | Set로 충분 | 현업·제품·위험 | 전 품질축 | 있음 | 감사 완료 |
| 측정계약 | 충분 | 데이터·현업·운영 | 비용·관측성·신뢰성 | 있음 | 감사 완료 |
| 영향평가 | 타 렌즈 이관 | 데이터·의사결정 | 개인정보·비용·가드레일 | 있음 | 경계 확인 필요 |
| 편익 실현 | 공통 Unit 중복 | 전략·재무·운영 | 비용·관측성·복구 | 있음 | 보류 |

## 6. 독립 QA

| 검사 | 대상 | 범위 | 최초 결과 | 최종 결과 |
|---|---|---|---|---|
| 출처 원문 일치 | 모든 evidence | 최초 27 + 신규 8 | 최초 revise 6 후보, 신규 P0 2 | 34건 유지, P0·P1 0 |
| 중복·명칭·목적지 | 모든 후보 | 10/10 | 최초 P1 7·P2 4, 신규 P1 6·P2 9 | P0·P1 0 |
| 실무성·D2 적정성 | 모든 후보 | 10/10 | 최초 P0 5 항목군, 신규 P0 후보별 1 | P0·P1 0 |
| 특정 직무 편향 | 분야 전체 | 전수 | 단일 직무 한정 없음 | 통과 |

신규 2개는 근거 8건·URL 8개 원문, 기존 8개와의 분류 중복, D2 fixture와
객관 합격조건을 별도 독립 감사했습니다. 부정확한 NDA evidence 1건은 삭제했고
Orange Book 본문은 포트폴리오 위험관리 Annex로 교체했습니다. 상세 발견,
Codex 판정과 교정 결과는 작업 패키지의 `audit/`에 있습니다.

## 7. 실행 경로 변경

Claude CLI 외부 워커는 두 사전 Gate에서 중단했습니다.

1. Windows 인라인 `--json-schema` 인자가 JSON으로 전달되지 않았습니다.
2. 일반 JSON 출력 백업 호출은 종료코드 0이었으나 회수 가능한 출력이
   없었습니다.

백그라운드 세션과 파일 변경이 없음을 확인한 뒤 원인 추적을 중단하고,
사용자가 승인한 Codex 서브에이전트 병렬 백업 경로로 전환했습니다.

2026-07-27에는 Orca 공식 orchestration 경로로 Claude Code 터미널 사전 Gate를
재검증했습니다. 작업공간 신뢰와 읽기 전용 응답을 확인한 뒤 근거·분류·실무성
Task 3개를 병렬 dispatch했고 세 `worker_done`을 모두 정상 수신했습니다.
감사자는 파일을 수정하지 않았고 Codex 메인 세션만 교정했습니다. 과거 실패는
직접 Claude CLI 구조화 출력 경로였으며 이번 Orca 조정 경로는 정상
완료되었습니다.

## 8. 검증 증거

```powershell
python tools/validate_catalog.py
python -m unittest discover -s tests -v
```

2026-07-27 실행 결과:

```text
Catalog: units=2, resources=4, sets=1, signals=3, candidates=10, handoffs=0, taxonomies=1
Catalog errors=0, warnings=0
Regression tests=28/28 passed
Independent audits: candidates 10/10
New strategic candidates: evidence P0=0/P1=0, taxonomy P0=0/P1=0, practicality P0=0/P1=0
Evidence inventory: 34 records, 25 unique URLs
```

자동검사 통과와 조사 내용의 사실 판정은 구분합니다. 최초 8개와 신규 2개는
서로 독립된 감사 경로로 전수 확인했으며 신규 2개의 원문·분류·실무성 P0·P1을
교정했습니다.

## 9. 변경 범위

### 생성·수정

- 작업 패키지 manifest와 분야 보고서
- Candidate 정본 10개
- evidence·taxonomy·practicality 감사 보고서
- 이 Checkpoint와 조사 README의 현재 상태
- 조사 인계 템플릿의 조사 렌즈 ID 정합성
- Candidate 스키마·템플릿·관계 검증기와 거버넌스·Runbook
- Taxonomy Registry 스키마·초기 Registry·Unit 분류 참조와 회귀검사

### 의도적으로 수정하지 않음

- `examples/valid/`의 학습 본문·Resource·Set 내용
- `research/signals/`
- 상세 학습자료와 HUB

## 10. 중단조건 확인

- [x] 승인된 manifest 밖으로 조사 범위를 확장하지 않았습니다.
- [x] 스키마·참조·회귀검사 실패가 없습니다.
- [x] 미확인 효과를 사실로 확정하지 않았습니다.
- [x] 사용자 변경을 덮어쓰거나 자동 롤백하지 않았습니다.
- [x] Candidate를 사용자 승인 없이 정규 카탈로그로 승격하지 않았습니다.
- [x] Claude CLI 이상 징후에서 즉시 백업 경로로 전환했습니다.
- [x] 신규 2개의 독립 감사와 P0·P1 교정을 완료했습니다.
- [x] 이 Checkpoint와 정본 파일만으로 현재 상태를 복원할 수 있습니다.

## 11. 다음 한 단계

사용자가 승인한 분류 운영 원칙과 Registry 기준선을 사용하여 Wave 2 작업 패키지
Manifest를 작성합니다. 작업 패키지별 후보 상한과 병렬 규모를 고정한 뒤
`ai-literacy-trust`부터 기술·데이터 중심 렌즈를 조사합니다. 정규
Unit·Set·Resource 승격은 별도 단계에서 판단합니다.

## 12. 사용자 승인 필요

- Wave 2 작업 패키지별 후보 상한과 병렬 규모
- 새 대분류, 기존 분류 ID의 개명·병합·폐기
- 정규 Unit·Set·Resource 승격은 향후 별도 승인
