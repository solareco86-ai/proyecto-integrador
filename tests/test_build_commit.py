from pathlib import Path

import pytest

from src.infrastructure.settings.config import _get_git_commit_sha


@pytest.fixture(autouse=True)
def _aislar_variables_git(monkeypatch: pytest.MonkeyPatch) -> None:
    # git push exporta GIT_DIR al hook pre-push: sin esto, `git -C tmp_path`
    # apuntaría al repo real y devolvería su HEAD en vez de "dev".
    for variable in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_COMMON_DIR"):
        monkeypatch.delenv(variable, raising=False)


def test_prioriza_variable_de_entorno(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("GIT_COMMIT_SHA", "abcdef1234")
    (tmp_path / ".build_commit").write_text("1111111\n", encoding="utf-8")

    assert _get_git_commit_sha(tmp_path) == "abcdef1"


def test_lee_el_archivo_del_despliegue(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("GIT_COMMIT_SHA", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    (tmp_path / ".build_commit").write_text("c20eed7\n", encoding="utf-8")

    assert _get_git_commit_sha(tmp_path) == "c20eed7"


def test_sin_archivo_ni_git_devuelve_dev(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("GIT_COMMIT_SHA", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)

    assert _get_git_commit_sha(tmp_path) == "dev"


def test_archivo_vacio_no_impide_seguir_al_siguiente_mecanismo(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.delenv("GIT_COMMIT_SHA", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    (tmp_path / ".build_commit").write_text("   \n", encoding="utf-8")

    assert _get_git_commit_sha(tmp_path) == "dev"


def test_archivo_con_bytes_invalidos_no_impide_seguir_al_siguiente_mecanismo(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.delenv("GIT_COMMIT_SHA", raising=False)
    monkeypatch.delenv("GITHUB_SHA", raising=False)
    (tmp_path / ".build_commit").write_bytes(b"\xff\xfe\x00\x01")

    assert _get_git_commit_sha(tmp_path) == "dev"
