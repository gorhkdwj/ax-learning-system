# 메타데이터 작성 및 검증

## 목적

학습공간은 파일명이나 본문을 추측하여 구조를 만들지 않습니다. 모든 Learning
Unit, Resource와 Learning Set은 정규 메타데이터를 가지며, HUB와 후속 추천
로직은 이 메타데이터만 읽습니다. 신흥 개념 연구는 별도의 Trend Signal
메타데이터로 관리하며 검증 전에는 학습 카탈로그로 취급하지 않습니다. Phase 2
Breadth 조사 결과도 Capability Candidate 메타데이터로 staging한 뒤 감사를
통과한 항목만 정규 구조로 라우팅합니다. 대분류·하위분류와 역할 보기의 정본은
`taxonomy/taxonomy.json`이며 Candidate와 Unit은 활성 node를 참조합니다.

`examples/valid`의 예제는 스키마와 검증기 확인을 위한 가상 표본입니다. 사용자의
실제 업무 우선순위, 학습 배정 또는 확인된 비즈니스 성과를 뜻하지 않습니다.

## 정본과 역할

- `schemas/*.schema.json`: 개별 JSON 파일의 필드, 자료형, enum과 필수값을
  검사합니다.
- `schemas/private-source-manifest.schema.json`: 공개 구조를 특정 개인 원천명에
  결합하지 않고 Vault 원천 패키지의 권리 상태·선정 범위·파일 무결성 계약을
  검사합니다.
- `schemas/learning-study.schema.json`: 자료 한 편 단위 학습 기록 Study의
  원천, 상태, takeaway 검증 상태와 적용 기록 계약을 검사합니다.
- `tools/validate_catalog.py`: 여러 파일 사이의 정확한 버전 참조, 소유관계,
  학습성과 정렬, 상대경로, Unit·Set DAG, Trend Signal, Taxonomy와 생명주기
  규칙을 검사합니다.
- `tools/validate_private_sources.py`: `AX_VAULT_ROOT`로만 선택적 Vault를 찾고,
  Vault가 있으면 `source.json`의 상대경로·크기·SHA-256·PDF 페이지 수를
  읽기 전용으로 검사합니다. Vault가 없으면 성공으로 건너뜁니다. 추적된 manifest만
  복원되고 한 package의 원문이 전혀 없으면 `manifest_only`로 통과하지만, 일부만
  복원되었거나 복원된 파일이 다르면 실패합니다. 모든 원문을 필수로 검사할 때에는
  `python tools/validate_private_sources.py --require-files`를 실행합니다.
- `templates/metadata/*.template.json`: 새 항목을 작성할 때 복제하는 시작점입니다.
- `examples/valid`: 검증기 정상 동작과 테스트에 사용하는 최소 참조 구현입니다.
- `catalog/items`: 승인된 정규 Unit과 그 Unit이 소유하는 Resource를 관리합니다.
- `sets`: 승인된 정규 Learning Set을 관리합니다.
- `studies`: 자료 한 편 단위의 학습 기록 Study를 관리합니다. 이수 대상이나
  숙련도 부여 대상이 아닙니다.
- `research/signals`: 검증 전 신흥 개념의 정의, 주장·근거와 승격 판정을 보존합니다.
- `research/capability-survey`: Phase 2 후보, 분야 보고서와 Wave Checkpoint를 보존합니다.
- `taxonomy/taxonomy.json`: 조사 렌즈, 잠정·정규 분류 node, 외부 참고체계와
  역할·업무 탐색 보기를 관리하는 단일 정본입니다.
- `research/capability-survey/handoffs`: Claude 조사 결과를 Codex가 재개하기 위한
  정형 인계를 보존합니다.
- `templates/research`: Candidate, 분야 조사, Checkpoint와 인계 작성 계약입니다.

스키마를 우회하는 별도 파서 규칙을 만들지 않습니다. 스키마로 표현하기 어려운
교차 파일 규칙만 검증기에 둡니다.

## 작성 순서

1. 적합한 템플릿을 실제 카탈로그 위치로 복제합니다.
2. `replace-me`와 `교체:`가 포함된 모든 값을 실제 정보로 바꿉니다.
3. Unit의 D0–D4 학습성과를 먼저 정하고 Resource 및 필수 검증 항목에 같은
   outcome ID를 연결합니다.
4. 모든 참조에 ID와 정확한 콘텐츠 버전을 함께 기록합니다.
5. 로컬 자료 경로는 작업공간 기준 `/` 상대경로로 기록합니다.
6. 공식 문서나 1차 출처, 확인일, 적용 버전과 검증한 범위를 기록합니다.
7. 단일 검증 명령과 자동 테스트를 실행합니다.

템플릿은 설명용 JSON이므로 그대로는 실제 카탈로그가 아닙니다. 템플릿 파일명을
`unit.json`, `resource.json`, `set.json`, `study.json`, `signal.json`,
`candidate.json`, `handoff.json` 또는 `taxonomy.json`으로
바꾼 뒤에는 모든 자리표시자와
참조 대상 및 실제 파일을 먼저 준비해야 합니다.

## ID와 버전

- Unit: `unit.<영역>.<이름>`
- Resource: `resource.<영역>.<이름>.<역할>`
- Set: `set.<유형>.<이름>`
- Study: `study.<영역>.<이름>`
- Trend Signal: `signal.<영역>.<이름>`
- Capability Candidate: `candidate.<영역>.<이름>`
- Phase 2 Handoff: `handoff.phase2.<범위>`
- Taxonomy Registry: `taxonomy.<영역>`
- 콘텐츠 버전: SemVer 형식의 `major.minor.patch`
- 참조: ID만으로 최신 버전을 추정하지 않고 항상 정확한 버전을 지정합니다.
- 예외: Study의 관련 Unit 참조는 과거 시점 기록이므로 ID로만 조인하고 당시
  버전은 `observed_at_version`에 참고로 기록합니다. Study의 발견 Signal 참조는
  정확한 버전을 사용합니다.
- 대체 항목: `lifecycle.superseded_by`에도 같은 종류의 ID와 정확한 버전을
  지정합니다.

Unit 또는 Set 버전이 바뀌면 그 정확한 버전을 owner로 가진 Resource의 버전과
owner도 함께 검토합니다. 검증기는 다른 버전의 Resource를 자동 재사용하지
않습니다.

## 단일 검증 명령

작업공간 루트에서 실행합니다.

```powershell
python tools/validate_catalog.py
```

기본 검증 범위는 `examples/valid`, `catalog`, `sets`, `studies`,
`research/signals`, `research/capability-survey`, `taxonomy`입니다. 따라서
정규 승격 파일도 별도 인자 없이 교차 참조와 Taxonomy 검증을 받습니다.

전체 자동 회귀검사는 다음과 같습니다.

```powershell
python -m unittest discover -s tests -v
```

검증 결과는 사람이 읽고 CI에서도 파싱할 수 있는 한 줄 형식입니다.

```text
SEVERITY|CODE|relative/path.json|message
SUMMARY|units=N|resources=N|sets=N|studies=N|signals=N|candidates=N|handoffs=N|taxonomies=N|errors=N|warnings=N
```

오류가 하나라도 있으면 종료코드 `1`, 스키마 자체를 불러오지 못하면 `2`,
오류가 없으면 `0`을 반환합니다. 경고는 검토 대상이지만 단독으로 실패시키지
않습니다.

## 검증 범위

현재 검증기는 다음을 실패로 처리합니다.

- 잘못된 JSON·스키마·ID 및 중복 `(종류, ID, 버전)`
- 누락된 정확 버전 참조와 archived 항목 참조
- Resource owner 불일치, owner의 역참조 누락과 알 수 없는 학습성과
- Resource가 없는 outcome과 필수 검증 항목이 없는 outcome
- 검증 항목의 outcome 및 Resource 소유관계 불일치
- 절대경로, 역슬래시, 작업공간 이탈과 존재하지 않는 로컬 경로
- Unit prerequisite 누락 수준·자기참조·순환
- Set 단계 누락 의존성·순환 및 필수 단계의 선택 단계 의존
- Set 단계의 선수 Unit·수준 미충족
- D2 이상 Set의 전이평가 누락
- 위험 권한 Set의 승인·중단·롤백 통제 누락
- 파일럿 이상 Set의 기준선·목표 누락 또는 미측정 기준선
- 잘못된 대체 항목 및 대체 관계 순환
- Signal의 잘못된 상태 전이와 현재 상태 불일치
- Signal claim–evidence 누락, 상태와 근거 stance 불일치
- Signal 별칭·정규 명칭 충돌과 해소되지 않은 중의성
- Signal의 누락된 정확 버전 참조, 자기참조와 계층관계 순환
- `substantiated`·`promoted` Signal의 근거·관련성·신뢰도·승격 조건 미충족
- Candidate의 누락·중복 ID, 잘못된 출처 날짜와 정확 버전 병합 대상
- Candidate의 최종 판정과 목적지 불일치
- 중간 이상 신뢰도 또는 공식·1차 근거가 없는 `accepted` Candidate
- 활성 Taxonomy Registry 수, 중복 node·프레임워크·보기 ID와 깨진 내부 참조
- Taxonomy 계층 순환, 별칭·명칭 충돌, 폐기 node 참조와 잘못된 외부 매핑
- Candidate·Unit의 미등록 대분류·하위분류와 부모 계층 불일치
- Study의 미등록 또는 폐기된 Taxonomy node 참조
- URL과 비공개 원천 참조가 모두 없는 Study 원천
- `applied` Study의 적용 기록 누락 또는 사람 확인 이상 takeaway 부재
- `contradicts` 학습성과 대응의 `cross_checked` takeaway 부재
- Study의 알 수 없는 학습성과·Unit·Signal 참조
- 영상·팟캐스트 여부와 `media` 기록의 불일치
- Study 적용 증적 경로의 경로 규칙 위반과 중복 `(study, ID, 버전)`

외부 URL의 실시간 접속, 공급자별 버전 제약 해석, 명령 실행, 내용 정확성과
학습효과 측정은 이 구조검증기가 대신하지 않습니다. 해당 검증은 Resource
메타데이터의 검증 범위와 후속 평가 하네스에서 별도로 증명합니다.

## Capability Candidate 작성과 감사

Phase 2 후보는 `templates/research/capability-candidate.template.json`에서
시작하고 `research/capability-survey/`의 승인된 작업 패키지에 둡니다.
Candidate는 정규 카탈로그가 아니며 제안 Unit·Set ID는 실제 ID 확보나 승격을
뜻하지 않습니다.

후보에는 정의·포함·제외 범위, 학습자의 관찰 가능한 행동, 전이 맥락, 목표 D 수준과
깊이 상한, 업무가치 가설, 횡단 품질축, evidence와 임시 판정을 기록합니다.
분야 발견자와 출처·taxonomy·실무성 감사자를 분리합니다. 일반 Breadth 후보는
장문의 dossier를 만들지 않으며, 고위험·D3/D4·공식 근거 충돌·높은 효과 주장
등 Runbook의 트리거가 있는 후보만 Deep Research로 보냅니다.

세부 Wave와 샘플링 QA는
`docs/research/phase2-capability-survey-runbook.md`를 따릅니다.

## Trend Signal 작성과 승격

새로 유통되는 명칭을 발견하면 `templates/metadata/trend-signal.template.json`에서
시작합니다. 커뮤니티 자료는 발견 근거로 사용할 수 있지만, 핵심 정의와 효과를
확정하려면 공식·1차 출처와 claim별 근거 연결이 필요합니다. 정의 신뢰도와 효과
신뢰도를 분리하고, 기존 Unit·Signal과의 중복 여부를 먼저 확인합니다.

`substantiated`는 핵심 정의를 방어할 수 있다는 뜻이며 업무효과가 입증되었다는
뜻이 아닙니다. 실제 효과가 불확실하면 비교 가능한 기준선·성공지표·중단조건을
갖춘 Probe Set 후보로 둡니다. `promoted`로 바꿀 때에는 생성·갱신·연결한 실제
Unit·Set·Resource의 ID와 정확한 버전을 기록합니다.

상태 전이, G0–G8 승격 게이트와 과장 방지 기준은
`docs/research/trend-signal-governance.md`를 따릅니다.

## 승격 기준

`cataloged`는 구조가 등록되었다는 뜻이며 교재·학습효과·업무효과가 검증되었다는
뜻이 아닙니다.

- `active` 이상 Unit은 최소 Resource와 검증 항목을 가져야 합니다.
- D2 완료 주장은 새로운 입력에서 독립 실행과 전이평가 증거가 필요합니다.
- `pilot`, `operational`, `scale` Set은 측정된 기준선과 목표가 필요합니다.
- 외부 쓰기·삭제·관리·재무 권한을 추가하면 승인점, 중단조건과 롤백을 다시
  검토합니다.

## 다음 스키마 진화 게이트

첫 파일럿을 만들기 전 다음 항목을 Phase 2 조사 결과와 함께 구조화합니다.

- Set 전용 통합 학습성과와 종단 간 검증 게이트
- capstone 입력·제출물·루브릭 Resource
- 기존 답안 복사를 차단하는 전이과제의 입력, 산출물과 제한시간
- Resource 검증 상태를 파일 무결성, 실행, 내용 정확성, 평가 타당성,
  접근성과 학습효과로 분리하는 모델
- 저자 예상시간과 파일럿 중앙값, 재이수자의 통합 전용 시간을 구분하는 모델
