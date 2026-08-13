"""联网探针和固定门户就绪测试。"""

from types import SimpleNamespace

import requests

from seu_autologin import connectivity


class FakeSession:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.trust_env = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, traceback):
        return False

    def get(self, *args, **kwargs):
        outcome = next(self.outcomes)
        if isinstance(outcome, Exception):
            raise outcome
        requested_url = args[0]
        if isinstance(outcome, tuple):
            status_code, final_url = outcome
        else:
            status_code, final_url = outcome, requested_url
        return SimpleNamespace(status_code=status_code, url=final_url)


def test_session_disables_environment_proxy() -> None:
    session = connectivity._session()
    try:
        assert session.trust_env is False
    finally:
        session.close()


def test_internet_probe_falls_through_until_success(monkeypatch) -> None:
    fake = FakeSession([requests.ConnectionError(), 302, 200])
    monkeypatch.setattr(connectivity, "_session", lambda: fake)
    assert connectivity.internet_available(timeout=0.1)


def test_internet_probe_returns_false_when_all_fail(monkeypatch) -> None:
    fake = FakeSession([500, 404, requests.Timeout()])
    monkeypatch.setattr(connectivity, "_session", lambda: fake)
    assert not connectivity.internet_available(timeout=0.1)


def test_captive_portal_redirect_is_not_treated_as_internet(monkeypatch) -> None:
    fake = FakeSession(
        [
            (200, "http://10.9.10.100/"),
            (200, "http://10.9.10.100/"),
            (200, "http://10.9.10.100/"),
        ]
    )
    monkeypatch.setattr(connectivity, "_session", lambda: fake)
    assert not connectivity.internet_available(timeout=0.1)


def test_portal_ready_uses_fixed_url_without_redirect(monkeypatch) -> None:
    fake = FakeSession([200])
    monkeypatch.setattr(connectivity, "_session", lambda: fake)
    assert connectivity.portal_network_ready(timeout=0.1)


def test_portal_ready_handles_network_error(monkeypatch) -> None:
    fake = FakeSession([requests.ConnectionError()])
    monkeypatch.setattr(connectivity, "_session", lambda: fake)
    assert not connectivity.portal_network_ready(timeout=0.1)
