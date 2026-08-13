"""Windows 单实例、浏览器发现与安全打开网页。"""

import ctypes
import os
import subprocess
from pathlib import Path
from urllib.parse import urlsplit

from .constants import EDGE_PATHS, MUTEX_NAME, PORTAL_HOST, PORTAL_URL


def edge_path() -> Path | None:
    """返回本机 Edge 可执行文件路径。"""

    return next((path for path in EDGE_PATHS if path.exists()), None)


def edge_available() -> bool:
    """检查本机 Edge 是否存在。"""

    return edge_path() is not None


def acquire_single_instance() -> object | None:
    """使用公开版专属命名互斥量，避免重复运行。"""

    if os.name != "nt":
        return object()
    kernel32 = ctypes.windll.kernel32
    handle = kernel32.CreateMutexW(None, False, MUTEX_NAME)
    if not handle:
        return None
    if kernel32.GetLastError() == 183:
        kernel32.CloseHandle(handle)
        return None
    return handle


def release_single_instance(handle: object | None) -> None:
    """释放命名互斥量。"""

    if handle and os.name == "nt":
        ctypes.windll.kernel32.ReleaseMutex(handle)
        ctypes.windll.kernel32.CloseHandle(handle)


def open_manual_portal() -> bool:
    """只允许用普通 Edge 打开固定门户。"""

    if urlsplit(PORTAL_URL).hostname != PORTAL_HOST:
        return False
    executable = edge_path()
    try:
        if executable:
            subprocess.Popen(
                [str(executable), PORTAL_URL],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        else:
            os.startfile(PORTAL_URL)  # type: ignore[attr-defined]
    except OSError:
        return False
    return True
