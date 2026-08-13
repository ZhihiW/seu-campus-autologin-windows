"""自动认证编排的安全门测试。"""

import logging

from seu_autologin import runner
from seu_autologin.models import Credential, LoginResult


def _logger() -> logging.Logger:
    logger = logging.getLogger("runner-tests")
    logger.handlers.clear()
    logger.addHandler(logging.NullHandler())
    return logger


def _disable_mutex(monkeypatch) -> None:
    monkeypatch.setattr(runner, "acquire_single_instance", lambda: object())
    monkeypatch.setattr(runner, "release_single_instance", lambda handle: None)


def test_online_path_never_loads_credential(monkeypatch) -> None:
    _disable_mutex(monkeypatch)
    monkeypatch.setattr(runner, "internet_available", lambda timeout=3: True)

    def forbidden_load():
        raise AssertionError("联网状态不应读取凭据")

    monkeypatch.setattr(runner, "load_credential", forbidden_load)
    assert runner.run_autologin(_logger(), initial_delay=0) == 0


def test_unreachable_portal_never_loads_credential(monkeypatch) -> None:
    _disable_mutex(monkeypatch)
    monkeypatch.setattr(runner, "internet_available", lambda timeout=3: False)
    monkeypatch.setattr(runner, "portal_network_ready", lambda timeout=2: False)
    monkeypatch.setattr(runner, "open_manual_portal", lambda: True)

    def forbidden_load():
        raise AssertionError("固定门户不可达时不应读取凭据")

    monkeypatch.setattr(runner, "load_credential", forbidden_load)
    assert (
        runner.run_autologin(
            _logger(), initial_delay=0, network_wait_seconds=0, browser_fallback=False
        )
        == 4
    )


def test_missing_credential_stops_before_browser_submission(monkeypatch) -> None:
    _disable_mutex(monkeypatch)
    monkeypatch.setattr(runner, "internet_available", lambda timeout=3: False)
    monkeypatch.setattr(runner, "portal_network_ready", lambda timeout=2: True)
    monkeypatch.setattr(runner, "load_credential", lambda: None)

    def forbidden_submit(*args, **kwargs):
        raise AssertionError("没有凭据时不应启动提交")

    monkeypatch.setattr(runner, "submit_login", forbidden_submit)
    assert runner.run_autologin(_logger(), initial_delay=0) == 3


def test_gateway_authenticated_prevents_resubmission(monkeypatch) -> None:
    _disable_mutex(monkeypatch)
    calls = {"internet": 0, "submit": 0}

    def offline(timeout=3):
        calls["internet"] += 1
        return False

    def authenticated(credential, logger):
        calls["submit"] += 1
        return LoginResult(False, False, "already", gateway_authenticated=True)

    monkeypatch.setattr(runner, "internet_available", offline)
    monkeypatch.setattr(runner, "portal_network_ready", lambda timeout=2: True)
    monkeypatch.setattr(runner, "load_credential", lambda: Credential("u", "p"))
    monkeypatch.setattr(runner, "submit_login", authenticated)
    assert runner.run_autologin(_logger(), initial_delay=0) == 0
    assert calls["submit"] == 1


def test_explicit_failure_is_not_retried(monkeypatch) -> None:
    _disable_mutex(monkeypatch)
    calls = {"submit": 0, "fallback": 0}
    monkeypatch.setattr(runner, "internet_available", lambda timeout=3: False)
    monkeypatch.setattr(runner, "portal_network_ready", lambda timeout=2: True)
    monkeypatch.setattr(runner, "load_credential", lambda: Credential("u", "p"))

    def rejected(credential, logger):
        calls["submit"] += 1
        return LoginResult(True, True, "rejected")

    def fallback():
        calls["fallback"] += 1
        return True

    monkeypatch.setattr(runner, "submit_login", rejected)
    monkeypatch.setattr(runner, "open_manual_portal", fallback)
    assert runner.run_autologin(_logger(), initial_delay=0) == 4
    assert calls == {"submit": 1, "fallback": 1}


def test_second_instance_exits_without_network_or_credentials(monkeypatch) -> None:
    monkeypatch.setattr(runner, "acquire_single_instance", lambda: None)
    assert runner.run_autologin(_logger()) == 0
