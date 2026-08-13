"""滚动日志与敏感字段兜底脱敏。"""

import logging
import re
import sys
from logging.handlers import RotatingFileHandler

from .constants import APP_NAME
from .paths import log_dir

_SENSITIVE_PATTERNS = (
    re.compile(r"(?i)(DDDDD|upass|username|password)=([^&\s]+)"),
    re.compile(r"(?i)(Authorization:\s*)(\S+)"),
    re.compile(r"(?i)(Cookie:\s*)(.+)$"),
)


def redact_text(value: str) -> str:
    """清除可能误入日志的常见凭据字段。"""

    result = value
    for pattern in _SENSITIVE_PATTERNS:
        result = pattern.sub(lambda match: f"{match.group(1)}=<redacted>", result)
    return result


class RedactingFormatter(logging.Formatter):
    """在最终写入前再做一层脱敏。"""

    def format(self, record: logging.LogRecord) -> str:
        return redact_text(super().format(record))


def build_logger(verbose: bool = False) -> logging.Logger:
    """创建公开版独立的滚动日志。"""

    destination = log_dir()
    destination.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(APP_NAME)
    logger.handlers.clear()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)
    logger.propagate = False

    formatter = RedactingFormatter(
        "%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    file_handler = RotatingFileHandler(
        destination / "autologin.log",
        maxBytes=512 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if sys.stdout is not None:
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger
