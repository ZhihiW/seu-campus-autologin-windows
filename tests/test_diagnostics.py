"""诊断报告最小化与隐私边界测试。"""

import json

from seu_autologin import diagnostics


def test_diagnostics_contains_no_identity_fields(monkeypatch) -> None:
    monkeypatch.setattr(diagnostics, "edge_available", lambda: True)
    monkeypatch.setattr(diagnostics, "credential_exists_without_secret", lambda: True)
    monkeypatch.setattr(diagnostics, "internet_available", lambda timeout=2: True)
    monkeypatch.setattr(diagnostics, "portal_network_ready", lambda timeout=2: True)
    monkeypatch.setattr(diagnostics, "scheduled_task_exists", lambda: False)
    report = diagnostics.collect_diagnostics()
    serialized = json.dumps(report, ensure_ascii=False).casefold()
    for forbidden in ("username", "password", "mac", "ssid", "cookie"):
        assert forbidden not in serialized
    assert report["telemetry_enabled"] is False
    assert report["fixed_portal_host"] == "10.9.10.100"


def test_write_diagnostics_uses_utf8_json(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(diagnostics, "diagnostics_dir", lambda: tmp_path)
    monkeypatch.setattr(
        diagnostics,
        "collect_diagnostics",
        lambda: {"status": "正常", "telemetry_enabled": False},
    )
    output = diagnostics.write_diagnostics()
    assert json.loads(output.read_text(encoding="utf-8"))["status"] == "正常"
