"""自动认证流程编排。"""

import logging
import time

from .connectivity import internet_available, portal_network_ready
from .credentials import load_credential
from .portal import submit_login
from .system import acquire_single_instance, open_manual_portal, release_single_instance


def run_autologin(
    logger: logging.Logger,
    *,
    initial_delay: int = 3,
    network_wait_seconds: int = 60,
    browser_fallback: bool = True,
) -> int:
    """检查网络并在确有需要时读取凭据、执行认证。"""

    mutex = acquire_single_instance()
    if mutex is None:
        logger.info("已有一个开源版实例正在运行，本次退出。")
        return 0

    try:
        # 已联网时尽快退出，而且完全不读取 Credential Manager 中的密码。
        if internet_available(timeout=2):
            logger.info("外网已经可用，无需认证。")
            return 0

        if initial_delay > 0:
            logger.info("网络尚未就绪，%d 秒后复查。", initial_delay)
            time.sleep(initial_delay)
            if internet_available(timeout=2):
                logger.info("外网已经可用，无需认证。")
                return 0

        deadline = time.monotonic() + max(network_wait_seconds, 0)
        waiting_logged = False
        while not portal_network_ready(timeout=2):
            if time.monotonic() >= deadline:
                logger.error("固定认证网关在 %d 秒内未就绪。", network_wait_seconds)
                if browser_fallback:
                    open_manual_portal()
                return 4
            if not waiting_logged:
                logger.info("每 2 秒检查一次固定认证网关，最长等待 %d 秒。", network_wait_seconds)
                waiting_logged = True
            time.sleep(2)
            if internet_available(timeout=2):
                logger.info("外网已经可用，无需认证。")
                return 0

        # 只有确认离线且固定门户可达后才读取密码。
        credential = load_credential()
        if credential is None:
            logger.error("公开版尚未配置凭据，请先运行 configure。")
            return 3

        attempt = 0
        while True:
            attempt += 1
            result = submit_login(credential, logger)
            logger.info(result.message)

            if internet_available(timeout=3):
                logger.info("外网连通性复核通过。")
                return 0
            if result.gateway_authenticated:
                logger.warning("网关已确认会话认证，不再重复提交。")
                return 0
            if result.explicit_failure:
                break
            if attempt >= 2 or time.monotonic() >= deadline:
                break
            logger.info("等待 15 秒后进行最后一次技术性重试。")
            time.sleep(15)

        logger.error("自动认证未完成。")
        if browser_fallback:
            if open_manual_portal():
                logger.info("已打开固定门户供手动处理。")
            else:
                logger.warning("无法打开固定门户。")
        return 4
    finally:
        release_single_instance(mutex)
