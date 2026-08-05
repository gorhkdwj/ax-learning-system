# 자료 단위 Study 계층 설계

## 1. 목적과 문제

현재 공개 카탈로그에는 외부 아티클이나 영상을 **그 자체로 학습하는 자리**가
없습니다. 확인된 상태는 다음과 같습니다.

- 예제를 제외한 실제 Resource 88개 중 85개가 `external_reference`이며 URL
  링크만 있습니다.
- `resource_type`이 `article`인 실제 Resource는 0개이고 2개는 모두
  `examples/valid`의 가상 표본입니다.
- `resource.json`의 `owner`는 필수이며 `unit` 또는 `set`만 허용하므로 소유자
  없는 Resource가 존재할 수 없습니다.
- Unit의 `item_type`은 학습 대상의 종류를 뜻하며 자료 형식이 아닙니다.

따라서 아티클과 영상은 Unit 설계의 배경 자료이거나 참고 링크로만 쓰이고,
학습 기록으로 축적되지 않습니다. 이 설계는 **자료 한 편을 단위로 하는 학습
기록 계층**을 추가하여 이 공백을 메웁니다.

## 2. 범위

포함합니다.

- 공개 저장소의 Study 메타데이터 스키마와 검증
- Vault 원천 manifest의 미디어 확장(트랜스크립트·프레임·오디오·영상)
- 두 검증기와 회귀 테스트, 관련 문서 갱신

포함하지 않습니다.

- Reading Set 유형 신설
- Study에서 Unit으로의 승격 게이트
- HUB 생성기

뒤의 세 항목은 실제 필요가 확인되기 전까지 만들지 않습니다.

## 3. 계층에서의 지위

Study는 다섯 번째 학습 계층이 아닙니다. Trend Signal이 네 계층 앞의 연구
인입인 것과 같은 위상으로, **네 계층 옆의 학습 기록**입니다.

- 이수 대상이 아닙니다.
- 숙련도 D0–D4를 부여하지 않습니다.
- 선수관계 DAG에 참여하지 않습니다.

이 구분이 필요한 이유는 명확합니다. Study가 이수 대상이 되면 "아티클 30편
읽음"이 숙련도 주장으로 바뀌는데, 거버넌스는 D2 완료 주장에 새로운 입력에서의
독립 실행과 전이평가 증거를 요구합니다.

## 4. 물리 위치

```text
ax-learning-system/
  catalog/items/     정규 Unit과 그 Unit이 소유하는 Resource
  sets/              업무 목적별 Learning Set
  studies/           자료 단위 학습 기록          <- 신설
  research/signals/  용어 단위 조사 기록
```

`catalog/items`는 승인된 정규 Unit을 관리하는 자리이므로 Study를 그 아래 두지
않습니다. `sets/`가 최상위인 것과 같은 방식으로 `studies/`를 최상위에 둡니다.

## 5. Trend Signal과의 경계

| 구분 | 단위 | 질문 |
|---|---|---|
| Study | 자료 한 편 | 이 자료에서 무엇을 배웠고 어떻게 쓰는가 |
| Trend Signal | 용어·개념 하나 | 이 용어가 실재하며 정규 학습에 넣을 가치가 있는가 |

대부분의 아티클은 신흥 용어가 아니라 이미 아는 주제의 설명이므로 Study만
남깁니다. 자료를 보다 새 용어를 발견했을 때에만 Signal을 별도로 만들고
`discovered_signal_refs`로 연결합니다. 같은 판정이 여러 Study에 분산되어 G0–G8
승격 게이트가 무력해지는 것을 막기 위한 경계입니다.

## 6. 상태 모델

```text
read -> applied -> archived
```

| 상태 | 의미 | 필수 조건 |
|---|---|---|
| `read` | 자료를 보고 요약과 적용 판정을 남겼습니다. | `takeaways` 1건 이상, `applicability` |
| `applied` | 실제 업무나 산출물에 반영했습니다. | 위 조건 + `application` + `human_confirmed` 이상 takeaway 1건 이상 |
| `archived` | 더 이상 활성 참조하지 않으며 이력만 보존합니다. | 없음 |

`read`에서 `applied`로 올릴 때 사람 확인을 요구하는 이유는 자동 자막과 Whisper의
오인식·환각, 그리고 프레임 해석 오류가 실재하기 때문입니다. AI가 정리한 요약만
근거로 업무 반영을 표시하지 않습니다.

`status_history`는 두지 않습니다. Signal이 그것을 갖는 이유는 승격 게이트 감사
때문이며, Study의 단순 전이에는 `lifecycle`의 날짜로 충분합니다.

## 7. `schemas/learning-study.schema.json`

### 7.1 최상위 필드

| 필드 | 필수 | 설명 |
|---|---|---|
| `schema_version` | 예 | SemVer |
| `id` | 예 | `^study\.[a-z0-9]+(?:[.-][a-z0-9]+)*$` |
| `version` | 예 | SemVer |
| `title` | 예 | 최소 1자 |
| `status` | 예 | `read` \| `applied` \| `archived` |
| `source` | 예 | 7.2 |
| `media` | 아니오 | 7.3. `source.kind`가 `video` 또는 `podcast`일 때만 허용 |
| `taxonomy_refs` | 예 | Registry node ID 배열, `minItems` 1, `uniqueItems`. domain과 subdomain 모두 허용하며 Unit의 `taxonomy.major_domain`·`taxonomy.subdomains`와 같은 ID 공간을 씁니다. |
| `taxonomy_gap` | 아니오 | 분류에 없을 때의 메모 |
| `takeaways` | 예 | 7.4, `minItems` 1 |
| `applicability` | 예 | `high` \| `medium` \| `low` \| `none` |
| `applicability_note` | 아니오 | 문자열 |
| `outcome_coverage` | 아니오 | 7.5. 기본값 빈 배열 |
| `related_unit_refs` | 아니오 | 7.6. 기본값 빈 배열 |
| `discovered_signal_refs` | 아니오 | `{id, version}` 배열. 기본값 빈 배열 |
| `application` | 아니오 | 7.7. `status`가 `applied`일 때 검증기가 필수로 강제 |
| `lifecycle` | 예 | 7.8 |

`additionalProperties`는 모든 객체에서 `false`로 둡니다.

### 7.2 `source`

| 필드 | 필수 | 값 |
|---|---|---|
| `kind` | 예 | `article` \| `video` \| `podcast` \| `private_document` |
| `title` | 예 | 최소 1자 |
| `publisher` | 아니오 | 문자열 |
| `url` | 아니오 | `^https://` |
| `private_source_ref` | 아니오 | `{id, version}`. `id`는 `^private-source\.` |
| `published_at` | 아니오 | `date` |
| `checked_at` | 예 | `date` |
| `language` | 아니오 | 문자열 |

`url`과 `private_source_ref` 중 최소 하나가 있어야 합니다. 스키마의 `anyOf`로
표현하고 검증기에서도 동일 규칙을 확인합니다. 공개 저장소에는 Vault의 실제
파일명이나 경로를 기록하지 않으며 불투명 원천 ID만 둡니다.

### 7.3 `media`

| 필드 | 필수 | 값 |
|---|---|---|
| `duration_minutes` | 아니오 | 1 이상 정수 |
| `watched_segments` | 아니오 | `"MM:SS-MM:SS"` 또는 `"HH:MM:SS-HH:MM:SS"` 문자열 배열 |
| `transcript_source` | 예 | `official_caption` \| `auto_caption` \| `whisper_groq` \| `whisper_openai` \| `none` |
| `frame_coverage` | 아니오 | `{frames_retained, resolution_px, sampling_note}` |
| `corrections` | 아니오 | `{at, heard, confirmed, basis}` 배열 |

`corrections[].basis`는 `frame` \| `official_doc` \| `domain_knowledge`입니다.

`transcript_source`를 필수로 두는 이유는 공식 자막·자동 자막·Whisper의 신뢰도가
서로 다르기 때문입니다. `frame_coverage`는 희소 샘플링으로 보지 못한 구간이
있는지 사후에 판단하기 위한 기록입니다.

### 7.4 `takeaways`

| 필드 | 필수 | 값 |
|---|---|---|
| `claim` | 예 | 최소 1자 |
| `basis` | 예 | `transcript` \| `frame` \| `official_doc` \| `own_reasoning` |
| `verification` | 예 | `{status, source_url?, checked_at}` |

`verification.status`는 `ai_derived` \| `human_confirmed` \| `cross_checked`입니다.
`cross_checked`일 때 `source_url`이 필수이며 `^https://`를 만족해야 합니다.
`checked_at`은 항상 필수입니다.

### 7.5 `outcome_coverage`

| 필드 | 필수 | 값 |
|---|---|---|
| `outcome_id` | 예 | `^outcome\.[a-z0-9]+(?:[.-][a-z0-9]+)*$` |
| `coverage` | 예 | `full` \| `partial` \| `contradicts` |
| `basis` | 아니오 | 문자열 |
| `mapped_at` | 예 | `date` |
| `note` | 아니오 | 문자열 |

이 배열은 Study 작성 시점에 비어 있습니다. 해당 분야 Unit 학습을 시작할 때
기존 Study를 훑으며 채웁니다. 작성 순간에 Unit의 학습성과를 알 수 없거나 Unit
자체가 아직 없을 수 있으므로, 읽는 순간의 부담을 만들지 않기 위한 설계입니다.

### 7.6 `related_unit_refs`

| 필드 | 필수 | 값 |
|---|---|---|
| `id` | 예 | `^unit\.` |
| `observed_at_version` | 아니오 | SemVer |
| `note` | 아니오 | 문자열 |

**정확한 버전 참조 규칙의 의도적 예외입니다.** Study는 과거 시점의 기록이므로
Unit 버전이 올라가도 따라 올리지 않습니다. 정확한 버전으로 고정하면 Unit이
1.1.0이 될 때 조인이 끊기므로, 조인은 ID로 하고 당시 버전은
`observed_at_version`에 참고로만 남깁니다. 검증기는 해당 ID의 Unit이 어느
버전으로든 존재하는지만 확인합니다.

### 7.7 `application`

| 필드 | 필수 | 값 |
|---|---|---|
| `task` | 예 | 최소 1자 |
| `evidence_paths` | 예 | 작업공간 기준 상대경로 배열, `minItems` 1 |
| `completed_at` | 예 | `date` |

`evidence_paths`는 기존 로컬 경로 규칙과 동일하게 절대경로·역슬래시·`..`를
거부합니다.

### 7.8 `lifecycle`

| 필드 | 필수 | 값 |
|---|---|---|
| `owner` | 예 | 문자열 |
| `last_reviewed_at` | 예 | `date` |
| `review_due_at` | 아니오 | `date` |
| `note` | 아니오 | 문자열 |

## 8. `schemas/private-source-manifest.schema.json` 확장

### 8.1 현재 제약

`files[]`의 여섯 필드가 모두 필수이고 `path`가 `.pdf$`를 강제하므로 영상·자막·
이미지를 표현할 수 없습니다.

### 8.2 변경

`files[]`에 `media_kind`를 **선택 필드**로 추가하고, 미지정 시 `document`로
해석합니다. 이렇게 하면 기존 `private-source.ontology-lecture` manifest가 수정
없이 그대로 통과합니다. 하위호환은 이 설계의 제약조건입니다.

| `media_kind` | `path` 확장자 | 추가 필수 필드 |
|---|---|---|
| `document`(기본값) | `.pdf` | `page_count` |
| `transcript` | `.vtt` `.srt` `.txt` `.md` | 없음 |
| `frame` | `.jpg` `.jpeg` `.png` | `captured_at_seconds` |
| `audio` | `.m4a` `.mp3` `.wav` | `duration_seconds` |
| `video` | `.mp4` `.webm` `.mkv` | `duration_seconds` |

`page_count`는 더 이상 무조건 필수가 아니며 `document`일 때만 필수입니다.
`allOf` + `if`/`then`으로 표현합니다. `captured_at_seconds`와
`duration_seconds`는 0 이상 정수입니다.

### 8.3 Vault 배치

```text
ax-learning-vault/sources/
  documents/private-source.<id>/     기존, 무변경
  media/private-source.<id>/         신설
    source.json
    transcripts/<slug>.<lang>.vtt
    frames/t-<mmss>.jpg
  articles/                          이제 검증 범위에 포함
```

## 9. 검증기 변경

### 9.1 `tools/validate_catalog.py`

레지스트리 네 곳에 `study`를 추가합니다.

- `SCHEMA_FILES`에 `"study": "learning-study.schema.json"`
- `METADATA_FILENAMES`에 `"study.json": "study"`
- `ValidationReport.counts`에 `"study": 0`
- `build_parser`의 `roots` 기본값에 `"studies"`
- `validate()`의 `indexes` 초기화에 `"study": {}`
- `main()`의 SUMMARY에 `studies={n}`

`UNSUPPORTED_METADATA_FILE` 메시지의 파일명 목록에도 `study.json`을 추가합니다.

교차 검증 규칙을 추가합니다.

| 코드 | 심각도 | 조건 |
|---|---|---|
| `STUDY_TAXONOMY_UNKNOWN` | ERROR | `taxonomy_refs`의 node가 활성 Registry에 없습니다. |
| `STUDY_TAXONOMY_DEPRECATED` | ERROR | 참조한 node가 `deprecated`입니다. |
| `STUDY_SOURCE_MISSING` | ERROR | `url`과 `private_source_ref`가 모두 없습니다. |
| `STUDY_APPLIED_WITHOUT_APPLICATION` | ERROR | `status`가 `applied`인데 `application`이 없습니다. |
| `STUDY_APPLIED_WITHOUT_CONFIRMATION` | ERROR | `status`가 `applied`인데 `human_confirmed` 이상 takeaway가 없습니다. |
| `STUDY_CONTRADICTS_WITHOUT_EVIDENCE` | ERROR | `coverage`가 `contradicts`인데 `cross_checked` takeaway가 없습니다. |
| `STUDY_OUTCOME_UNKNOWN` | ERROR | `outcome_id`가 어떤 Unit의 학습성과에도 없습니다. |
| `STUDY_UNIT_UNKNOWN` | ERROR | `related_unit_refs`의 ID를 가진 Unit이 없습니다. |
| `STUDY_SIGNAL_UNKNOWN` | ERROR | `discovered_signal_refs`의 정확한 `(id, version)` Signal이 없습니다. |
| `STUDY_MEDIA_ON_NON_MEDIA` | ERROR | `source.kind`가 `video`·`podcast`가 아닌데 `media`가 있습니다. |
| `STUDY_MEDIA_MISSING` | ERROR | `source.kind`가 `video`·`podcast`인데 `media`가 없습니다. |
| `STUDY_INVALID_PATH` | ERROR | `application.evidence_paths`가 경로 규칙을 위반합니다. |
| `DUPLICATE_ID` | ERROR | 기존 규칙과 동일하게 `(study, id, version)` 중복 |

기존 `_validate_lifecycle`, `_validate_supersession`, `_validate_references`가
Study를 잘못 처리하지 않도록 확인합니다. Study는 `superseded_by`를 갖지 않고
`resource_refs` 역참조 대상도 아닙니다.

### 9.2 `tools/validate_private_sources.py`

- `validate()`의 순회 기준을 `sources/documents`에서 `sources` 전체로 넓힙니다.
  기존 경로는 그대로 포함되므로 회귀가 없으며, 지금까지 한 번도 검사되지 않던
  `sources/articles/`가 검증 범위에 들어옵니다.
- `_validate_file()`에서 `media_kind`를 읽어 분기합니다. 미지정은 `document`로
  해석합니다.
- `_pdf_page_count()`는 `document`일 때만 호출합니다. 다른 미디어는 크기와
  SHA-256만 확인합니다.
- `frame`은 `captured_at_seconds`, `audio`와 `video`는 `duration_seconds`가
  manifest에 있는지 확인합니다. 파일에서 실제 재생시간을 추출하지는 않습니다.
  외부 도구 의존을 늘리지 않기 위한 결정이며, 이 값은 사람이 기록한 참고값으로
  다룹니다.
- `manifest_only` 판정과 `--require-files` 동작은 그대로 유지합니다.

## 10. 테스트

### 10.1 `tests/test_validate_study.py` 신설

- 최소 유효 Study가 오류 없이 통과합니다.
- `taxonomy_refs` 누락과 미등록 node를 각각 오류로 잡습니다.
- `url`과 `private_source_ref`가 모두 없으면 오류입니다.
- `status`가 `applied`인데 `application`이 없으면 오류입니다.
- `status`가 `applied`인데 모든 takeaway가 `ai_derived`이면 오류입니다.
- `coverage`가 `contradicts`인데 `cross_checked` takeaway가 없으면 오류입니다.
- 존재하지 않는 `outcome_id`·Unit ID·Signal 참조를 각각 오류로 잡습니다.
- `cross_checked`인데 `source_url`이 없으면 스키마 단계에서 오류입니다.
- `article` 자료에 `media`가 있으면 오류이고, `video` 자료에 `media`가 없으면
  오류입니다.

### 10.2 `tests/test_validate_private_sources.py` 갱신

기존 테스트를 삭제하지 않고 다음을 추가합니다.

- `media_kind`가 없는 기존 형식 manifest가 그대로 통과합니다(하위호환).
- `transcript`는 `page_count` 없이 통과하고 pypdf를 호출하지 않습니다.
- `frame`에 `captured_at_seconds`가 없으면 오류입니다.
- `video`에 `duration_seconds`가 없으면 오류입니다.
- `document`인데 확장자가 `.pdf`가 아니면 오류입니다.
- `sources/articles/` 아래의 manifest가 검출됩니다.

### 10.3 회귀 기준

- 기존 테스트 64건이 모두 통과해야 합니다.
- `python tools/validate_catalog.py`가 오류 0, 경고 0을 유지해야 합니다.
- 기존 `private-source.ontology-lecture` manifest는 한 글자도 수정하지 않습니다.

## 11. 예제와 디렉터리 실재화

### 11.1 `examples/valid/studies/`

검증기와 테스트가 사용할 가상 표본 Study를 최소 1건 둡니다. 기존
`examples/valid`의 Unit·Set 예제와 같은 성격이며 사용자의 실제 학습을 뜻하지
않습니다. 표본은 다음을 함께 보여야 합니다.

- 공개 URL 자료 1건, `status`는 `read`
- `taxonomy_refs`는 실재하는 canonical node
- `takeaways`에 서로 다른 `verification.status` 값

### 11.2 `studies/README.md`

`studies/`를 검증기 `roots` 기본값에 넣으면 디렉터리가 없을 때
`ROOT_NOT_FOUND`가 발생합니다. Git은 빈 디렉터리를 추적하지 않으므로
`studies/README.md`로 디렉터리를 실재화합니다. 이 파일에는 Study의 목적, 상태
모델, 작성 절차와 검증 명령을 적습니다. 실제 Study 카드는 자료를 학습할 때마다
추가합니다.

### 11.3 템플릿

`templates/metadata/learning-study.template.json`을 기존 템플릿 규칙에 맞춰
작성합니다. 모든 자리표시자에 `replace-me` 또는 `교체:` 접두사를 둡니다.

## 12. 문서 갱신

| 파일 | 변경 |
|---|---|
| `docs/architecture/learning-system.md` | 논리 구조 다이어그램과 권장 물리 구조에 `studies/` 추가, Study의 지위와 Signal과의 경계를 절로 추가 |
| `docs/metadata/README.md` | 정본과 역할 목록, ID 규칙, 검증 범위, 작성 절차에 Study 추가 |
| `docs/architecture/public-private-storage.md` | `sources/media/` 배치, `media_kind` 계약, `sources` 전체 순회로의 변경 반영 |
| `README.md` | 메타데이터 스키마 목록에 Learning Study 추가 |

## 13. 작업 흐름

### 13.1 영상 자료

```text
1차   /watch <URL> --detail transcript
      트랜스크립트만 확보하고 오인식 의심 지점을 표시합니다.
2차   /watch <로컬 파일> --timestamps <t1,t2> --resolution 1024
      해당 지점만 고해상도로 재추출하여 화면 표기로 확정합니다.
3     Vault에 트랜스크립트와 선별 프레임, source.json을 둡니다.
4     공개 저장소에 study.json을 작성합니다.
5     tools/verify.ps1을 실행합니다.
```

1차에서 전체 프레임을 뽑지 않는 이유는 기본 512px 해상도로는 화면의 작은
글씨를 판독할 수 없기 때문입니다. 필요한 지점만 선별해 크게 뽑습니다.

`/watch`는 작업 디렉터리를 임시 경로에 만들고 종료 시 삭제를 권합니다. 보존할
파일은 명시적으로 Vault로 옮깁니다. 자막이 없는 자료는 오디오가 외부 Whisper
API로 전송되므로, 회사 내부 자료에는 사전에 전송 범위와 권한을 확인합니다.

### 13.2 Unit 학습 시작 시

```text
1  해당 Unit의 taxonomy node로 Study를 검색합니다.
2  관련 Study의 takeaway를 Unit 학습성과에 대응시켜 outcome_coverage를 채웁니다.
3  full로 표시된 학습성과는 사전진단에서 축약합니다.
```

## 14. 되돌리기 어려운 결정과 근거

| 결정 | 근거 |
|---|---|
| Study를 이수 대상에서 제외 | 자료 소비량이 숙련도 주장으로 바뀌는 것을 차단 |
| `taxonomy_refs` 필수 | 분류 없는 기록이 축적되어 검색 불가능해지는 것을 차단 |
| Study에서 Unit으로의 단방향 참조 | Study 작성마다 Unit 수정을 요구하면 기록이 축적되지 않음 |
| Unit 참조에 정확 버전 대신 ID 조인 | Unit 버전 상승 시 과거 기록과의 연결이 끊기는 것을 방지 |
| `applied` 승격에 사람 확인 요구 | 자동 자막·Whisper 환각·프레임 오독이 실재하는 오류원 |
| `contradicts`에 공식 근거 요구 | 검증을 거친 Unit이 미확인 자료 한 건으로 흔들리는 것을 방지 |
| `media_kind` 선택 필드화 | 기존 manifest 무수정 통과라는 하위호환 제약 |

## 15. 완료 조건

- `tools/verify.ps1`의 네 단계가 모두 통과합니다.
- 카탈로그 검증이 오류 0, 경고 0이며 SUMMARY에 `studies` 항목이 나타납니다.
- 기존 테스트 64건에 신규 테스트가 더해져 전부 통과합니다.
- 기존 `private-source.ontology-lecture` manifest가 수정되지 않았습니다.
- 공개 저장소에 Vault의 실제 파일명·경로·절대경로가 없습니다.
