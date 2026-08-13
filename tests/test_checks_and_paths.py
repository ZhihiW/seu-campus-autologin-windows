"""环境检查和独立数据目录测试。"""

import logging
from pathlib import Path

from seu_autologin import checks, paths


def _logger() -> logging.Logger:
    logger = logging.getLogger("checks-tests")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    return logger


def test_data_path_override_has_highest_priority(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("SEU_AUTOLOGIN_OSS_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path / "other"))
    assert paths.app_data_dir() == tmp_path
    assert paths.log_dir() == tmp_path / "logs"
    assert paths.diagnostics_dir() == tmp_path / "diagnostics"


def test_data_path_uses_public_app_name(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("SEU_AUTOLOGIN_OSS_DATA_DIR", raising=False)
    monkeypatch.setenv("LOCALAPPDATA", str(tmp_path))
    assert paths.app_data_dir() == tmp_path / "SEUCampusAutoLoginOSS"


def test_data_path_has_source_fallback(monkeypatch) -> None:
    monkeypatch.delenv("SEU_AUTOLOGIN_OSS_DATA_DIR", raising=False)
    monkeypatch.delenv("LOCALAPPDATA", raising=False)
    assert paths.app_data_dir().name == ".runtime"
    assert isinstance(paths.app_data_dir(), Path)


def test_check_accepts_online_machine_without_opening_portal(monkeypatch) -> None:
    monkeypatch.setattr(checks, "credential_exists_without_secret", lambda: True)
    monkeypatch.setattr(checks, "internet_available", lambda timeout=3: True)
    monkeypatch.setattr(checks, "edge_available", lambda: True)
    assert checks.check_environment(_logger(), inspect_portal=False) == 0


def test_check_recognizes_login_portal_while_offline(monkeypatch) -> None:
    monkeypatch.setattr(checks, "credential_exists_without_secret", lambda: False)
    monkeypatch.setattr(checks, "internet_available", lambda timeout=3: False)
    monkeypatch.setattr(checks, "edge_available", lambda: True)
    monkeypatch.setattr(checks, "inspect_portal_state", lambda: "login")
    assert checks.check_environment(_logger(), inspect_portal=True) == 0


def test_check_fails_safely_when_edge_and_portal_are_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(checks, "credential_exists_without_secret", lambda: False)
    monkeypatch.setattr(checks, "internet_available", lambda timeout=3: False)
    monkeypatch.setattr(checks, "edge_available", lambda: False)
    monkeypatch.setattr(checks, "inspect_portal_state", lambda: "edge-missing")
    assert checks.check_environment(_logger(), inspect_portal=True) == 5
