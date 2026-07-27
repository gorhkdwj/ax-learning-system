# AX 통합 작업공간

공개 가능한 AX 학습 시스템과 개인·비공개 학습 원천을 분리하여 함께 사용하는
상위 작업공간입니다. 이 디렉터리 자체는 Git 저장소로 만들지 않습니다.

## 구성

- `ax-learning-system/`: 공개 Git 저장소로 사용할 학습 시스템
- `ax-learning-vault/`: 비공개 Git 저장소 또는 로컬 전용 Vault
- `.remember/`: 로컬 세션 상태

공개 저장소는 Vault 없이도 실행됩니다. Vault가 있으면 공개 코드가
`AX_VAULT_ROOT`를 통해 비공개 원천과 파생 색인을 선택적으로 찾을 수 있습니다.

## 전체 공개 영역 검증

```powershell
.\ax-learning-system\tools\verify.ps1
```

저장소별 커밋과 원격 연결은 각 하위 디렉터리에서 독립적으로 수행합니다.
