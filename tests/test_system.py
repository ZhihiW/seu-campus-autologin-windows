"""公开版系统集成边界测试。"""

from types import SimpleNamespace

from seu_autologin import system


def test_edge_discovery(monkeypatch, tmp_path) -> None:
    existing = tmp_path / "msedge.exe"
    existing.write_bytes(b"")
    monkeypatch.setattr(system, "EDGE_PATHS", (tmp_path / "missing.exe", existing))
    assert system.edge_path() == existing
    assert system.edge_available()


def test_edge_discovery_returns_none(monkeypatch, tmp_path) -> None:
    monkeypatch.setattr(system, "EDGE_PATHS", (tmp_path / "missing.exe",))
    assert system.edge_path() is None
    assert not system.edge_available()


def test_mutex_creation_and_release(monkeypatch) -> None:
    calls = []

    class Kernel32:
        def CreateMutexW(self, *args):
            calls.append("create")
            return 123

        def GetLastError(self):
            return 0

        def ReleaseMutex(self, handle):
            calls.append(("release", handle))

        def CloseHandle(self, handle):
            calls.append(("close", handle))

    monkeypatch.setattr(system.ctypes, "windll", SimpleNamespace(kernel32=Kernel32()))
    handle = system.acquire_single_instance()
    assert handle == 123
    system.release_single_instance(handle)
    assert calls == ["create", ("release", 123), ("close", 123)]


def test_existing_mutex_returns_none(monkeypatch) -> None:
    calls = []

    class Kernel32:
        def CreateMutexW(self, *args):
            return 456

        def GetLastError(self):
            return 183

        def CloseHandle(self, handle):
            calls.append(handle)

    monkeypatch.setattr(system.ctypes, "windll", SimpleNamespace(kernel32=Kernel32()))
    assert system.acquire_single_instance() is None
    assert calls == [456]


def test_open_manual_portal_uses_edge(monkeypatch, tmp_path) -> None:
    executable = tmp_path / "msedge.exe"
    executable.write_bytes(b"")
    captured = {}
    monkeypatch.setattr(system, "edge_path", lambda: executable)
    monkeypatch.setattr(
        system.subprocess,
        "Popen",
        lambda args, **kwargs: captured.update({"args": args}) or object(),
    )
    assert system.open_manual_portal()
    assert captured["args"] == [str(executable), "http://10.9.10.100/"]


def test_open_manual_portal_rejects_modified_constant(monkeypatch) -> None:
    monkeypatch.setattr(system, "PORTAL_URL", "http://example.com/")
    assert not system.open_manual_portal()
