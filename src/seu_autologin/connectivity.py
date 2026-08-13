"""外网与固定校园网网关连通性检测。"""

from urllib.parse import urlsplit

import requests

from .constants import APP_NAME, CONNECTIVITY_PROBES, PORTAL_URL


def _session() -> requests.Session:
    """创建不继承代理环境变量的短生命周期会话。"""

    session = requests.Session()
    session.trust_env = False
    return session


def internet_available(timeout: float = 3.0) -> bool:
    """用多个 HTTPS 探针判断是否已获得真实外网访问能力。"""

    headers = {"User-Agent": f"{APP_NAME}/0.1"}
    with _session() as session:
        for url, expected_status in CONNECTIVITY_PROBES:
            try:
                response = session.get(
                    url,
                    timeout=timeout,
                    allow_redirects=True,
                    headers=headers,
                )
            except requests.RequestException:
                continue
            # 即使被认证页劫持并返回 200，也不能误判为真正联网。
            final_host = urlsplit(response.url).hostname
            expected_host = urlsplit(url).hostname
            if response.status_code == expected_status and final_host == expected_host:
                return True
    return False


def portal_network_ready(timeout: float = 2.0) -> bool:
    """判断网卡、DHCP 与校内路由是否已经能到达固定认证入口。"""

    headers = {"User-Agent": f"{APP_NAME}/0.1"}
    with _session() as session:
        try:
            response = session.get(
                PORTAL_URL,
                timeout=timeout,
                allow_redirects=False,
                headers=headers,
            )
        except requests.RequestException:
            return False
    return response.status_code < 500
