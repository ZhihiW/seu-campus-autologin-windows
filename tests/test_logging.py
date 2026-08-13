"""日志脱敏测试。"""

from seu_autologin import logging_config
from seu_autologin.logging_config import redact_text


def test_redacts_portal_fields() -> None:
    text = "GET /?DDDDD=example_user&upass=example_secret&username=demo&password=test"
    redacted = redact_text(text)
    assert "example_user" not in redacted
    assert "example_secret" not in redacted
    assert "demo" not in redacted
    assert "test" not in redacted
    assert redacted.count("<redacted>") == 4


def test_redacts_headers() -> None:
    redacted = redact_text("Authorization: Bearer-secret Cookie: session=secret")
    assert "Bearer-secret" not in redacted
    assert "session=secret" not in redacted


def test_logger_writes_redacted_rotating_log(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(logging_config, "log_dir", lambda: tmp_path)
    logger = logging_config.build_logger(verbose=True)
    logger.info("DDDDD=student&upass=secret")
    for handler in logger.handlers:
        handler.flush()
    content = (tmp_path / "autologin.log").read_text(encoding="utf-8")
    assert "student" not in content
    assert "secret" not in content
    assert "<redacted>" in content
