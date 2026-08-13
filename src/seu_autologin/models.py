"""跨模块使用的数据结构。"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Credential:
    """只在需要提交登录时短暂存在于内存中的凭据。"""

    username: str
    password: str


@dataclass(frozen=True)
class LoginResult:
    """一次浏览器认证尝试的结果。"""

    submitted: bool
    explicit_failure: bool
    message: str
    gateway_authenticated: bool = False
