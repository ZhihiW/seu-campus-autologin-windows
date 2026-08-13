"""公开仓库表面保持简约，同时保留维护资料。"""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_root_has_only_three_user_cmd_entries() -> None:
    names = {path.name for path in PROJECT_ROOT.glob("*.cmd")}
    assert names == {"安装.cmd", "测试.cmd", "卸载.cmd"}


def test_maintenance_documents_are_available_without_cluttering_root() -> None:
    expected = (
        PROJECT_ROOT / ".github" / "SECURITY.md",
        PROJECT_ROOT / ".github" / "CONTRIBUTING.md",
        PROJECT_ROOT / "docs" / "PRIVACY.md",
        PROJECT_ROOT / "docs" / "DEVELOPMENT.md",
        PROJECT_ROOT / "docs" / "CHANGELOG.md",
        PROJECT_ROOT / "docs" / "THIRD_PARTY_NOTICES.md",
    )
    assert all(path.is_file() for path in expected)


def test_readme_links_to_three_simple_entries() -> None:
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    for name in ("安装.cmd", "测试.cmd", "卸载.cmd"):
        assert name in readme
