# Phase 2 Capability Survey — Wave 4 Checkpoint

## 1. 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-04` |
| 상태 | `ready_for_wave-05-planning` |
| 시작일·마지막 갱신일 | `2026-08-02` · `2026-08-02` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 입력 Candidate | 96개 |
| 분류 Registry | `taxonomy.ax-capability-map@0.10.0` (`provisional`) |
| 작업 패키지 | `wp.cross-cutting-coverage.matrix-a` |
| 신규 Candidate 상한·실제 | `10` · `0` |

## 2. 목표와 비목표

### 완료한 목표

- 10개 조사 렌즈 × 8개 역할 관점 × 12개 품질축 Coverage 판정 규칙 확정
- 렌즈 × 역할 및 렌즈 × 품질축 projection 작성
- 0건 품질축의 인접 소유권과 명시적 defer·재개 조건 기록
- 개발자 기술스택·공급자·역할·D 수준 편향 레드팀
- Wave 5로 넘길 taxonomy·role view representation 공백 분리

### 비목표

- 기존 Candidate와 정규 Unit·Resource·Set·Signal 수정
- provisional taxonomy의 canonical 확정과 ID 변경·병합·폐기
- 상세 교재·fixture·runner·HUB와 개인 학습 우선순위 제작
- Wave 6 독립 QA와 Phase 2 완료 선언

## 3. 작업 패키지

| 패키지 | 상태 | 신규 후보 | 경로 | 판정 |
|---|---|---:|---|---|
| `wp.cross-cutting-coverage.matrix-a` | complete | 0/10 | `research/capability-survey/waves/wave-04/` | 라우팅 없는 신규 고우선 공백 0개, Wave 5 정규화 준비 |

## 4. Coverage 결과

| 항목 | 결과 |
|---|---|
| 조사 렌즈 | 10/10 포함 |
| 역할 관점 | 8/8 포함, 사람이 검토한 projection |
| 품질축 | 정의된 12개 축 모두 최소 1개 Candidate에 존재 |
| 전체 Candidate | 96 |
| 기술·운영 / 사람·업무·통제 | 48 / 48 |
| 목표 깊이 | D0 3, D1 1, D2 72, D3 20, D4 0 |
| 신규 고우선 Candidate | 0 |
| 명시적 defer·공백군 | 6개, 재개 조건 유지 |

세부 matrix와 0건 축 라우팅은
`research/capability-survey/waves/wave-04/coverage-matrix.md`에 있습니다.
Candidate 개수는 coverage 충분성이나 학습효과의 증거로 사용하지 않았습니다.

## 5. 결정 기록

- 역할과 품질축이 직접 조사되었으면 `조사됨`, 인접 렌즈 소유권이 명시되었으면
  `근거 있는 공백`, 둘 다 없으면 `미완료`로 판정합니다.
- 현재 3차원 조합에는 라우팅 없는 미완료가 없지만 역할 관점이 Candidate의
  구조화 필드가 아니므로 기계 검증 가능한 역할별 지도는 아직 미완료입니다.
- 역할 view 확정은 Wave 5 taxonomy 정규화와 영향분석 뒤 Wave 7에서 조립합니다.
- 개인화 memory, 내부 플랫폼, 보안 engineering, vendor assurance, 전문
  HR·노무·조달과 편익 실현 공백은 신규 Candidate로 복제하지 않고 기존 defer와
  재개 조건을 유지합니다.
- Wave 4에서는 Taxonomy, Candidate와 정규 카탈로그를 변경하지 않습니다.

## 6. QA와 한계

| 검사 | 범위 | 결과 | 한계·후속 |
|---|---|---|---|
| Candidate 인벤토리 | 96/96 | 렌즈별 8~10개, 합계 96 확인 | 내용 독립 재감사는 Wave 6 |
| 품질축 집계 | 96/96 | 12개 축 전체 존재, 렌즈별 0건 라우팅 기록 | 역할 × 축의 구조화 필드 없음 |
| 특정 직무 편향 | 10개 렌즈 전수 | 기술·운영 48 / 사람·업무·통제 48 | 후보 수만으로 완전성을 확정하지 않음 |
| 깊이 편향 | 96/96 | D4 0, D3 20 | D3는 Wave 6 전수검수 |
| 명시적 defer | 기존 보고서 전수 | 6개 공백군과 재개 조건 보존 | 실제 필요 발생 시 제한 Deep Research |
| 독립성 | Wave 4 문서 | 메인 세션 자체 검토 | 독립 QA는 Wave 6에서 수행 |

## 7. 검증 증거

검증일 `2026-08-02`의 결과는 다음과 같습니다.

```text
Public boundary: errors=0
Catalog: units=76, resources=82, sets=8, signals=3, candidates=96
Catalog validation: errors=0, warnings=0
Regression tests: 33/33 passed
git diff --check: passed
```

현재 셸에서는 Windows 앱 실행 별칭이 실제 Python보다 먼저 해석되어 첫 통합
명령이 저장소 검사 전에 중단되었습니다. 실제 Python 실행기가 우선되도록 PATH를
교정한 같은 셸에서 공식 `tools/verify.ps1`을 다시 실행해 위 결과로 통과했습니다.
이는 콘텐츠·스키마 검증 실패가 아닙니다.

## 8. 변경 범위

### 생성

- `research/capability-survey/waves/wave-04/manifest.md`
- `research/capability-survey/waves/wave-04/coverage-matrix.md`
- `research/capability-survey/waves/wave-04/audit/coverage-red-team.md`
- `research/capability-survey/checkpoints/wave-04.md`

### 수정

- `research/capability-survey/README.md`
- `docs/plans/curriculum-foundation-plan.md`

### 의도적으로 수정하지 않음

- `catalog/`, `sets/`, `research/signals/`, `schemas/`
- 기존 Candidate와 `taxonomy/taxonomy.json`
- Vault의 추적 파일과 로컬 전용 원문

## 9. 중단조건 확인

- [x] 기존 사용자 변경과 원격 차이가 없습니다.
- [x] 승인된 Wave 4 manifest 밖으로 범위를 확장하지 않았습니다.
- [x] 신규 Candidate와 정규 승격을 수행하지 않았습니다.
- [x] 기존 ID·스키마·거버넌스를 변경하지 않았습니다.
- [x] 미확인 효과를 확인된 사실로 확정하지 않았습니다.
- [x] 명시적 defer와 잔여 위험을 삭제하지 않았습니다.
- [x] 이 Checkpoint와 Wave 4 산출물로 현재 상태를 복원할 수 있습니다.

## 10. 다음 한 단계

Wave 5 manifest에서 alias·중복·상하위 경계, stable core와 Adapter·Resource·Set
목적지, provisional taxonomy와 8개 역할 view의 정규화 범위·순서·변경 상한을
고정합니다. 기존 ID의 병합·개명·폐기와 canonical taxonomy 확정은 영향분석과
사용자 승인 전에는 적용하지 않습니다.
