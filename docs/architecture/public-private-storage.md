# Public·Private 저장 구조

## 1. 목적

공개 가능한 AX 학습 시스템과 개인 사용 원천을 물리적으로 분리합니다. 공개
HUB나 HTML에 Markdown·PDF 전문을 삽입하지 않고, 원천 변경 때마다 전체 HTML을
재생성하지 않아도 되는 데이터 경계를 제공합니다.

## 2. 물리 경계

```text
AX/
  ax-learning-system/       # 공개 저장소
  ax-learning-vault/        # 비공개 저장소 또는 로컬 전용
  .remember/                # 로컬 세션 상태
```

`ax-learning-system/`은 Vault가 없는 독립 복제본에서도 검증기, 테스트와 공개
예제가 작동해야 합니다. `ax-learning-vault/`은 없어도 되는 선택적 의존성입니다.

## 3. 데이터 배치

### 공개 저장소

- 거버넌스, 아키텍처와 실행 계획
- 스키마와 정규 메타데이터
- 공개가 허용된 학습자료와 비식별 예제
- 출처 URL, 확인일, 공개 가능한 요약과 검증 결과
- 생성기, 검증기와 테스트

### Vault

- 수집한 아티클·문서·교재의 전문과 원본 파일
- 저작권이나 재배포 권한이 불명확한 자료
- 비공개 Git으로 동기화하는 직접 작성 업무 Overlay·개인 학습 기록·원천 manifest
- 임베딩, 청크, 검색 인덱스와 비공개 HUB 산출물
- 인증정보가 아니라도 공개하면 안 되는 로컬 운영 데이터

Vault의 원천은 `sources/` 아래에 종류별로 배치합니다.

```text
ax-learning-vault/sources/
  documents/   PDF 등 문서 원천 패키지
  media/       영상·팟캐스트의 트랜스크립트·선별 프레임·오디오·영상 패키지
  articles/    수집한 아티클 원문
```

각 원천 패키지는 불투명 원천 ID를 이름으로 하는 디렉터리에 `source.json`
manifest와 원본·파생 파일을 둡니다.

비밀정보와 인증정보는 Vault에도 평문으로 기록하지 않고 운영체제의 비밀정보
저장소나 환경변수를 사용합니다.

## 4. 경로 계약

공개 코드가 Vault를 찾는 유일한 설정 키는 `AX_VAULT_ROOT`입니다. 값이 없으면
공개 저장소의 형제 디렉터리인 `../ax-learning-vault`를 선택적 기본값으로
해석합니다.

```dotenv
AX_VAULT_ROOT=../ax-learning-vault
```

상대경로는 현재 셸 위치가 아니라 `ax-learning-system/` 루트를 기준으로
해석합니다. 공개 코드에서는 `tools/workspace_paths.py`의 해석 함수를 재사용하며,
사용자 컴퓨터의 절대경로를 소스나 메타데이터에 저장하지 않습니다.

현재 해석기는 프로세스 환경변수만 읽고 `.env.local`을 자동으로 로드하지
않습니다. `.env.example`은 설정 계약의 예시이며, 향후 각 런타임이 명시적으로
로더를 채택하기 전까지는 셸이나 실행 환경에서 값을 주입합니다.

Vault가 없으면 공개 모드로 계속 실행하고, 필요한 비공개 기능만
`unavailable`로 표시합니다. Vault 누락을 공개 시스템 전체의 오류로 취급하지
않습니다.

## 5. 원천 참조 계약

공개 메타데이터는 Vault 파일의 실제 상대경로나 파일명을 직접 참조하지 않습니다.
향후 원천 Registry를 추가할 때에는 다음을 분리합니다.

- 공개 측: 안정적인 불투명 `source_id`, URL, 권리 상태, 공개 가능한 요약
- Vault 측: `source_id`와 실제 로컬 파일·청크·인덱스의 매핑

원문을 이동해도 공개 메타데이터와 학습 Unit ID가 바뀌지 않게 하기 위한
경계입니다. Registry를 도입할 때에는 별도 JSON Schema와 참조 검증을 먼저
추가합니다.

Vault의 원천 패키지는 `source.json`에 불투명 원천 ID, 패키지 기준 상대경로,
파일 크기, SHA-256, PDF 페이지 수, 검토일, 권리 상태와 선정·제외 범위를
기록합니다. 일반화된 계약은
`schemas/private-source-manifest.schema.json`, 선택형 검증기는
`tools/validate_private_sources.py`에 있습니다. 공개 Unit과 Resource는 이
manifest의 실제 파일명·경로·추출 텍스트를 참조하지 않습니다.

manifest의 `files[]`는 선택 필드 `media_kind`로 파일 종류를 구분합니다.
미지정 시 `document`로 해석하므로 기존 manifest는 수정 없이 그대로 통과하며,
이 하위호환은 계약의 제약조건입니다.

| `media_kind` | `path` 확장자 | 추가 필수 필드 |
|---|---|---|
| `document`(기본값) | `.pdf` | `page_count` |
| `transcript` | `.vtt` `.srt` `.txt` `.md` | 없음 |
| `frame` | `.jpg` `.jpeg` `.png` | `captured_at_seconds` |
| `audio` | `.m4a` `.mp3` `.wav` | `duration_seconds` |
| `video` | `.mp4` `.webm` `.mkv` | `duration_seconds` |

`page_count`는 더 이상 모든 파일의 필수가 아니며 `document`일 때만 필수입니다.
`captured_at_seconds`와 `duration_seconds`는 0 이상 정수이며, 파일에서
추출하지 않고 사람이 기록한 참고값으로 다룹니다.

## 6. HUB와 임베딩

HUB는 두 실행 모드를 가집니다.

1. 공개 모드: 공개 메타데이터와 공개 콘텐츠만 읽습니다.
2. 개인 모드: 런타임에 Vault의 검색 결과를 추가하지만 비공개 데이터를 공개
   생성 디렉터리에 쓰지 않습니다.

공개 정적 HTML에는 문서 전문, 전체 청크 배열이나 임베딩을 넣지 않습니다.
검색 인덱스와 임베딩은 Vault 아래에서 증분 갱신합니다. 공개 화면에는 검색 결과의
허용된 미리보기와 원천 ID만 전달합니다.

## 7. Git 정책

- 상위 `AX/`는 Git 저장소로 만들지 않습니다.
- 두 하위 저장소는 별도 `.git`, 원격과 커밋 이력을 가집니다.
- 공개 저장소의 `.gitignore`는 알려진 비공개 디렉터리와 로컬 설정을 차단합니다.
- Vault의 직접 작성 Overlay·개인 진행 기록과 `source.json` manifest는 비공개
  Git으로 추적하여 다른 로컬에서도 이어갈 수 있게 합니다.
- Vault의 원문·대용량 파일, 임베딩·색인과 재생성 가능한 생성물은 Git에서
  제외합니다.
- 공개 전 `python tools/check_public_boundary.py`와 전체 검증을 실행합니다.

대용량 또는 재배포 권한이 불명확한 파일은 비공개 Git이라도 일반 Git 객체로
저장하지 않습니다. 별도 백업이나 권한을 확인한 저장 수단을 사용합니다.

## 8. 검증

공개 저장소 루트 또는 상위 작업공간에서 다음을 실행합니다.

```powershell
./tools/verify.ps1
```

```powershell
./ax-learning-system/tools/verify.ps1
```

검증은 공개 경계, 카탈로그, 선택적 Vault 원천 manifest와 단위 테스트를
순서대로 확인합니다. Vault가 없으면 manifest 단계는 `skipped`로 성공하며,
Vault clone에 manifest만 있고 해당 package의 원문이 전혀 없으면 `manifest_only`로
성공합니다. 원문이 하나라도 복원된 package는 누락·크기·SHA-256·페이지 수 불일치를
실패로 처리합니다. 모든 원문 복원을 강제하려면 다음을 별도로 실행합니다.

```powershell
python tools/validate_private_sources.py --require-files
```

원천 manifest 검증의 순회 범위는 `sources/documents`만이 아니라 `sources`
전체입니다. 따라서 `sources/articles/`와 `sources/media/`의 manifest도 같은
규칙으로 검사합니다. `document`가 아닌 미디어 파일은 크기와 SHA-256만
확인하며, 재생시간과 프레임 시각은 manifest에 기록된 값의 존재만 확인합니다.

## 9. 새 컴퓨터 부트스트랩

Public 저장소를 먼저 복제하면 Vault가 없는 상태에서도 작업공간 경계와 검증
도구를 확보할 수 있습니다. Public 저장소의 스크립트는 현재 셸 위치가 아니라
스크립트 경로를 기준으로 상위 작업공간을 계산합니다.

```powershell
New-Item -ItemType Directory -Path AX
Set-Location ./AX
git clone https://github.com/gorhkdwj/ax-learning-system.git
./ax-learning-system/tools/bootstrap-workspace.ps1
```

`templates/workspace-root/`가 상위 `AGENTS.md`, `CLAUDE.md`, `README.md`의
배포 정본입니다. 대상이 없으면 만들고, 템플릿과 같으면 no-op으로 처리합니다.
대상 내용이 다르거나 상위에 `.git`이 있거나 기존 Vault 폴더·`origin`이 예상과
다르면 자동 수정·덮어쓰기·삭제 없이 중단합니다. `-PlanOnly`는 변경 없이 예정
작업과 충돌을 점검하며, `-SkipVaultClone`은 상위 파일만 배치합니다. 따라서
정상 완료 후 같은 명령을 반복 실행해도 추가 변경이 없습니다.

Private 저장소 인증이 필요하면 사용자의 Git 자격 증명 구성을 마친 뒤 명령을 다시
실행합니다. 토큰이나 인증정보를 스크립트 인자 또는 파일에 기록하지 않습니다.

Vault를 clone하면 직접 작성한 Overlay·개인 진행 기록과 원천 manifest는
복원됩니다. Git에서 제외된 원문 PDF·아티클은 별도의 개인 백업에서 복원하고,
파생 임베딩과 인덱스는 복원된 원문을 바탕으로 로컬에서 재생성해야 합니다.
