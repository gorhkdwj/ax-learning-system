"""공개 저장소와 선택적 비공개 Vault의 경로 계약을 제공합니다.

경로는 현재 셸 위치에 의존하지 않고 이 파일이 속한 공개 저장소를 기준으로
계산합니다. 공개 시스템은 Vault가 없어도 정상 작동해야 합니다.
"""

from __future__ import annotations

import os
from pathlib import Path


VAULT_ENV_VAR = "AX_VAULT_ROOT"


def public_root() -> Path:
    """현재 공개 저장소의 루트를 반환합니다."""

    return Path(__file__).resolve().parents[1]


def resolve_vault_root(
    configured_path: str | None = None,
    *,
    repository_root: Path | None = None,
) -> Path:
    """설정값을 공개 저장소 루트 기준의 절대 경로로 해석합니다.

    `configured_path`가 없으면 환경변수를 확인하고, 환경변수도 없으면 공개
    저장소의 형제 `ax-learning-vault`를 선택적 기본 위치로 사용합니다.
    Vault가 공개 저장소 내부를 가리키면 경계가 무너지므로 거부합니다.
    """

    root = (repository_root or public_root()).resolve()
    raw_path = configured_path
    if raw_path is None:
        raw_path = os.environ.get(VAULT_ENV_VAR)

    candidate = Path(raw_path) if raw_path else root.parent / "ax-learning-vault"
    if not candidate.is_absolute():
        candidate = root / candidate
    resolved = candidate.resolve()

    if resolved == root or root in resolved.parents:
        raise ValueError("Vault 경로는 공개 저장소 내부를 가리킬 수 없습니다.")
    return resolved


def vault_available(configured_path: str | None = None) -> bool:
    """선택적 Vault 디렉터리가 현재 사용 가능한지 반환합니다."""

    return resolve_vault_root(configured_path).is_dir()


def main() -> int:
    root = public_root()
    vault = resolve_vault_root()
    try:
        display_vault = vault.relative_to(root.parent).as_posix()
        display_vault = f"../{display_vault}" if vault.parent == root.parent else display_vault
    except ValueError:
        display_vault = "<external-path>"

    print("PUBLIC_ROOT=.")
    print(f"VAULT_ROOT={display_vault}")
    print(f"VAULT_AVAILABLE={'yes' if vault.is_dir() else 'no'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
