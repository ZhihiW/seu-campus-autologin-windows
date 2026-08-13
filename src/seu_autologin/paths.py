"""程序路径。"""

import os
from pathlib import Path

from .constants import APP_NAME


def app_data_dir() -> Path:
    """返回公开版独立的数据目录，不与私人版本共用。"""

    override = os.environ.get("SEU_AUTOLOGIN_OSS_DATA_DIR")
    if override:
        return Path(override)
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / APP_NAME
    return Path(__file__).resolve().parent / ".runtime"


def log_dir() -> Path:
    """返回日志目录。"""

    return app_data_dir() / "logs"


def diagnostics_dir() -> Path:
    """返回用户主动生成的脱敏诊断目录。"""

    return app_data_dir() / "diagnostics"
