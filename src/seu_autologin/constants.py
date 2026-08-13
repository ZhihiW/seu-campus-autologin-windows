"""程序常量与公开版的安全边界。"""

from pathlib import Path

APP_NAME = "SEUCampusAutoLoginOSS"
DISPLAY_NAME = "东南大学校园网自动登录（开源版）"
MUTEX_NAME = rf"Local\{APP_NAME}"
CREDENTIAL_TARGET = f"{APP_NAME}/SEU-WLAN"
TASK_NAME = "SEU Campus Auto Login OSS"
STARTUP_LINK_NAME = "SEU Campus Auto Login OSS.lnk"

# 第一版只允许这个经过实际验证的门户，不能由用户任意改成其他地址。
PORTAL_URL = "http://10.9.10.100/"
PORTAL_HOST = "10.9.10.100"

EDGE_PATHS = (
    Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"),
    Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"),
)

# 使用多个互相独立的 HTTPS 站点，降低单一站点临时故障造成的误判。
CONNECTIVITY_PROBES = (
    ("https://connectivitycheck.gstatic.com/generate_204", 204),
    ("https://www.baidu.com/favicon.ico", 200),
    ("https://www.bing.com/favicon.ico", 200),
)
