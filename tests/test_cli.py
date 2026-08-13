"""命令行参数测试。"""

from seu_autologin import cli


def test_negative_timing_is_clamped(monkeypatch) -> None:
    captured = {}
    monkeypatch.setattr(cli, "build_logger", lambda verbose=False: object())

    def fake_run(logger, **kwargs):
        captured.update(kwargs)
        return 0

    monkeypatch.setattr(cli, "run_autologin", fake_run)
    assert (
        cli.main(
            [
                "run-once",
                "--initial-delay",
                "-3",
                "--network-wait-seconds",
                "-10",
            ]
        )
        == 0
    )
    assert captured["initial_delay"] == 0
    assert captured["network_wait_seconds"] == 0


def test_check_can_skip_portal(monkeypatch) -> None:
    captured = {}
    monkeypatch.setattr(cli, "build_logger", lambda verbose=False: object())

    def fake_check(logger, *, inspect_portal):
        captured["inspect_portal"] = inspect_portal
        return 0

    monkeypatch.setattr(cli, "check_environment", fake_check)
    assert cli.main(["check", "--skip-portal"]) == 0
    assert captured["inspect_portal"] is False
