# Work Package Manifest: wp.cross-cutting-coverage.matrix-a

## 상태

| 필드 | 값 |
|---|---|
| Wave | `wave-04` |
| 작업 패키지 | `wp.cross-cutting-coverage.matrix-a` |
| 상태 | `complete` |
| 실행일 | `2026-08-02` |
| 총괄·유일 작성자 | Codex 메인 세션 |
| 입력 | Wave 1~3 Candidate 96개, Taxonomy Registry `0.10.0` |
| 신규 Candidate 상한 | `10` |
| 실제 신규 Candidate | `0` |

## 목표

- 10개 조사 렌즈를 역할 관점과 12개 횡단 품질축으로 교차 점검합니다.
- 각 조합을 `조사됨`, `근거 있는 공백`, `미완료`로 재현 가능하게 분류합니다.
- 후보 수의 균형을 coverage로 오인하지 않고 편중과 누락의 이유를 기록합니다.
- 역량지도가 개발자 기술스택 목록으로 축소되었는지 레드팀 검토합니다.

## 비목표

- 기존 Candidate·Unit·Resource·Set·Signal과 Taxonomy node 수정
- 잠정 taxonomy의 canonical 확정 또는 ID 병합·개명·폐기
- 상세 교재·fixture·runner·HUB와 개인 학습경로 제작
- Wave 5 중복 통합, Wave 6 독립 QA와 Phase 2 완료 선언

## 입력과 판정 규칙

1. 렌즈·하위분류·역할 근거는 각 작업 패키지의 `manifest.md`,
   `domain-survey.md`와 Wave Checkpoint에서 확인합니다.
2. 품질축은 Candidate 정본의 `cross_cutting.applicable_axes`를 집계합니다.
3. 역할이 직접 조사되고 품질축 Candidate가 하나 이상이면 해당 3차원 조합을
   `조사됨`으로 판정합니다.
4. 역할 또는 품질축이 인접 렌즈의 명시적 소유권으로 라우팅되었으면
   `근거 있는 공백`으로 판정합니다.
5. 직접 조사도 명시적 라우팅도 없으면 `미완료`입니다.
6. Candidate 개수는 근거의 위치를 보여줄 뿐 충분성이나 학습효과를 뜻하지 않습니다.

## 실행 순서

1. Wave 1~3 Candidate와 조사 보고서를 인벤토리화합니다.
2. 렌즈 × 역할 관점 projection을 작성합니다.
3. 렌즈 × 품질축 Candidate 수 projection을 작성합니다.
4. 두 projection과 판정 규칙으로 3차원 coverage 상태를 도출합니다.
5. 명시적 defer·인접 렌즈 라우팅과 구조화되지 않은 역할 보기를 분리합니다.
6. 기술스택·직무·공급자·D 수준 편향을 레드팀 검토합니다.
7. 자동검증과 Public 경계 검사를 수행하고 Wave 4 Checkpoint를 갱신합니다.

## 중단조건

- 기존 Candidate나 정규 카탈로그를 수정해야만 matrix를 완성할 수 있습니다.
- 새 대분류, 기존 ID 변경 또는 스키마·거버넌스 변경이 필요합니다.
- 직접 근거와 인접 렌즈 라우팅이 모두 없는 고우선 공백이 발견됩니다.
- 신규 Candidate가 10개를 넘거나 공식·1차 근거 조사 없이 후보 생성이 필요합니다.
- 구조·공개 경계·회귀검증이 실패합니다.

## 완료조건

- 10개 렌즈, 8개 역할 관점과 12개 품질축이 matrix에 포함됩니다.
- 0건인 품질축마다 인접 소유자 또는 미완료 상태가 기록됩니다.
- 알려진 defer와 재개 조건이 삭제되지 않고 후속 Wave로 라우팅됩니다.
- 개발자 기술스택 축소 여부와 남은 representation 한계가 기록됩니다.
- 신규 Candidate가 필요하지 않다는 결론을 후보 수가 아닌 마지막 누락 검토와
  기존 라우팅으로 설명합니다.
