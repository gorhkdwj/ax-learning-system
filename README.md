# AX Learning System

AI Agent와 바이브 코딩을 포함한 전사적 AI Transformation 역량을
학습하기 위한 공개 가능한 학습 시스템 저장소입니다.

현재 단계는 커리큘럼 콘텐츠를 대량 제작하기 전, 학습 범위·메타데이터·검증과
탐색 구조를 확립하는 기반 단계입니다.

## 새 컴퓨터에서 작업공간 구성

Public 저장소에는 작업공간 구조, 경계 규칙과 부트스트랩 도구가 있으므로 먼저
복제합니다. 그다음 스크립트가 상위 진입점 파일을 정본 템플릿에서 만들고 Private
Vault를 형제 디렉터리에 복제합니다.

```powershell
New-Item -ItemType Directory -Path AX
Set-Location ./AX
git clone https://github.com/gorhkdwj/ax-learning-system.git
./ax-learning-system/tools/bootstrap-workspace.ps1
```

반복 실행 시 템플릿과 같은 파일 및 올바른 Vault는 변경하지 않습니다. 상위
진입점의 내용이 템플릿과 다르거나 Vault 폴더·원격이 예상과 다르면 기존 항목을
덮어쓰거나 삭제하지 않고 중단합니다. 변경 없이 점검하려면 `-PlanOnly`, Vault
복제를 생략하려면 `-SkipVaultClone`을 사용합니다.

Vault Git 저장소를 복제하면 직접 작성한 업무 Overlay·개인 진행 기록과 원천
manifest는 복원됩니다. 원문 PDF·아티클, 임베딩과 검색 인덱스는 Git에서 제외되므로
원문은 별도의 개인 백업에서 복원하고 파생 데이터는 로컬에서 다시 생성해야 합니다.

## 문서

- [에이전트 작업 지침](AGENTS.md)
- [상세 학습 거버넌스](docs/governance/learning-governance.md)
- [4층 학습 시스템 아키텍처](docs/architecture/learning-system.md)
- [Public·Private 저장 구조](docs/architecture/public-private-storage.md)
- [Trend Signal 연구 인입 거버넌스](docs/research/trend-signal-governance.md)
- [Claude Phase 2 온보딩](docs/research/claude-phase2-onboarding.md)
- [Phase 2 전수조사 Runbook](docs/research/phase2-capability-survey-runbook.md)
- [AX 역량 분류 Registry](taxonomy/README.md)
- [커리큘럼 기반 구축 계획](docs/plans/curriculum-foundation-plan.md)

## 메타데이터 스키마

- [Learning Unit](schemas/learning-unit.schema.json)
- [Learning Set](schemas/learning-set.schema.json)
- [Learning Resource](schemas/learning-resource.schema.json)
- [Trend Signal](schemas/trend-signal.schema.json)
- [Capability Survey Candidate](schemas/capability-candidate.schema.json)
- [Phase 2 Claude→Codex Handoff](schemas/phase2-handoff.schema.json)
- [Capability Taxonomy Registry](schemas/capability-taxonomy.schema.json)
- [Private Source Manifest](schemas/private-source-manifest.schema.json)
- [메타데이터 작성·검증 안내](docs/metadata/README.md)

## 검증

```powershell
./tools/verify.ps1
```

이 명령은 공개 저장소 경계, 카탈로그, 선택적 Vault 원천 manifest와 단위 테스트를
순서대로 검사합니다. Vault가 없으면 원천 manifest 검사는 정상적으로 건너뜁니다.
상위 통합 작업공간에서는 다음과 같이 실행할 수 있습니다.

```powershell
./ax-learning-system/tools/verify.ps1
```

## 선택적 비공개 Vault

원문, 개인 기록, 임베딩과 비공개 생성물은 형제 디렉터리
`../ax-learning-vault/`에 둡니다. 이 저장소는 Vault 없이도 독립적으로
작동합니다.

다른 위치를 사용할 때에는 `.env.example`을 참고하여 `AX_VAULT_ROOT`를
프로세스 환경변수로 설정하십시오. 현재 경로 해석기는 `.env.local`을 자동으로
읽지 않습니다. 향후 런타임이 이를 사용하면 실제 `.env.local`은 Git에 포함하지
않습니다.

## Claude Code에서 Phase 2 인수

작업공간 루트에서 일반 Claude 세션을 시작합니다.

```powershell
claude
```

세션 안에서 `/memory`, `/agents`, `/doctor`로 `CLAUDE.md`와 프로젝트 조사
agent가 로드되었는지 확인한 뒤,
`docs/research/claude-phase2-onboarding.md`의 프롬프트를 전달합니다. 프로젝트
기본 agent는 별도로 변경하지 않습니다.

## 현재 상태

- Phase 0 거버넌스와 스키마 등록 완료
- Phase 1 예제 메타데이터, 템플릿, 참조·DAG 검증기와 회귀검사 완료
- Trend Signal 연구 인입 스키마·검증기와 최초 사례 3개 등록 완료
- 공개 학습 시스템과 개인 Vault의 저장·Git·경로 경계 분리 완료
- Phase 2 Wave 1~7 조사·승격·Coverage·정규화·독립 QA와 최종 역량지도 완료
- Phase 2 사용자 완료 승인: `2026-08-02` (`phase_complete`)
- 다음 단계: Phase 3 역할별 학습 우선순위와 비즈니스 임팩트 평가
