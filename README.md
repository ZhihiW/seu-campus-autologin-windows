# 东南大学校园网自动登录（Windows 开源版）

一个面向 Windows 10/11 的非官方校园网自动认证工具。Windows 用户登录后，程序会先判断外网和固定认证网关状态，只有确实需要认证时才从 Credential Manager 读取凭据并提交。

> [!IMPORTANT]
> 本项目是学生维护的非官方开源工具，与东南大学及东南大学网络与信息中心无隶属关系。第一版仅验证固定门户 `http://10.9.10.100/`，不代表支持所有校区、网络套餐或接入方式。

> [!WARNING]
> 当前门户使用 HTTP，传输过程不具备 TLS 保护。这是门户本身的网络传输边界，浏览器手动登录也会经过同一入口；本工具无法单方面把它升级为 HTTPS。使用前请了解风险，并优先向学校网信中心确认是否存在官方 HTTPS 或自动认证接口。

## 功能特点

- 已联网时立即退出，不读取密码、不重复认证；
- 只有固定网关可达时才读取公开版专属凭据；
- 浏览器请求只允许访问 `10.9.10.100`，跨主机重定向会被阻止；
- 凭据保存在当前 Windows 用户的 Credential Manager，不写入脚本、配置文件或日志；
- 登录后自适应等待网络就绪，默认最长 60 秒；
- 密码被明确拒绝后不连续重试；
- 支持安装、配置、检查、立即运行、诊断和完整卸载；
- 无遥测、无广告、无自动上传、无自动更新。

## 当前支持范围

| 项目 | 支持情况 |
|---|---|
| 系统 | Windows 10/11 x64 |
| 浏览器 | 已安装的 Microsoft Edge Stable |
| 认证入口 | 仅 `http://10.9.10.100/` |
| 用户类型 | 校园用户，基础账号会由门户按 `@xyw` 方式处理 |
| SEU-WLAN / 同门户有线网 | Beta 验证范围 |
| SEU-ISP、eduroam、其他校区或其他网关 | 尚未验证 |

## 安装发布版

1. 从 GitHub Releases 下载 `SEUCampusAutoLoginOSS-版本-windows-x64.zip` 和对应的 `.sha256`；
2. 校验 SHA256 后完整解压 ZIP；
3. 双击 `安装公开版.cmd`；
4. 阅读 HTTP 风险提示，在本机窗口输入账号和密码；
5. 安装程序会创建当前用户任务计划，并执行一次不会断网、不会重启的状态测试。

Beta 版本暂未进行商业代码签名，Windows SmartScreen 可能显示未知发布者。请只从项目 GitHub Releases 下载，并核对 SHA256。安装脚本使用 PowerShell `ExecutionPolicy Bypass` 仅运行解压目录中的透明脚本，不修改系统级执行策略。

## 日常使用

安装后可以从开始菜单的 `SEU Campus Auto Login OSS` 文件夹运行：

- `配置凭据`：修改公开版账号和密码；
- `手动检查`：检查环境和门户结构，不读取密码、不提交登录；
- `立即运行一次`：执行一次正常认证流程；
- `卸载`：删除公开版任务、凭据、程序和日志。

命令行接口：

```text
SEUCampusAutoLoginOSS.exe configure
SEUCampusAutoLoginOSS.exe check
SEUCampusAutoLoginOSS.exe run-once
SEUCampusAutoLoginOSS.exe diagnose
SEUCampusAutoLoginOSS.exe forget-credential
SEUCampusAutoLoginOSS.exe --version
```

## 与私人版本并存

公开版使用以下独立标识：

```text
程序目录：%LOCALAPPDATA%\SEUCampusAutoLoginOSS
任务计划：SEU Campus Auto Login OSS
凭据目标：SEUCampusAutoLoginOSS/SEU-WLAN
互斥锁：Local\SEUCampusAutoLoginOSS
```

它不会覆盖旧的 `SEUCampusAutoLogin` 文件、任务计划或凭据。为了避免两个版本在每次登录 Windows 时同时启动，完成公开版 Beta 验证后再决定是否停用私人版本。

## 隐私和安全

详细边界见 [SECURITY.md](SECURITY.md) 和 [PRIVACY.md](PRIVACY.md)。报告问题时：

- 不要提供账号或密码；
- 不要上传 Cookie、抓包文件或完整网页源码；
- 只运行 `diagnose` 并分享脱敏 JSON，发送前仍需人工复核；
- 安全漏洞使用 GitHub 私人漏洞报告，不要公开披露可利用细节。

## 从源码开发

需要 Python 3.10–3.12、Microsoft Edge 和 Windows。建议使用独立虚拟环境：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest --cov=seu_autologin --cov-report=term-missing
```

不需要运行 `playwright install`，因为程序调用系统已安装的 Edge，而不是下载 Chromium。

## 构建 Windows 发布包

```powershell
powershell -NoProfile -File .\scripts\build.ps1 -PythonExe .\.venv\Scripts\python.exe
```

构建结果位于 `release`，包含文件夹版应用、安装脚本、ZIP 和 SHA256。当前采用 PyInstaller `onedir`，便于 Beta 阶段排查依赖和杀毒软件误报。

## 维护者发布检查

- 单元测试和 Ruff 全部通过；
- 干净 Windows 10/11 电脑不安装 Python 也能运行；
- 已联网、固定门户不可达、错误密码、门户改版等路径均安全停止；
- 至少 3–5 名志愿者、两个使用相同网关的位置完成 20 次自然启动测试；
- 至少 19/20 次完成预期认证，且没有凭据泄露、未知地址提交或残留卸载项；
- 发布 ZIP、SHA256、更新记录和已知问题。

## 相关项目

- [NN708/seu-wlan-login](https://github.com/NN708/seu-wlan-login)：较早的东南大学校园网 Python 登录与自动重连实现。

本项目采用独立架构和固定网关安全边界；如未来引用其他项目代码，必须保留其许可证和署名。

## 许可证

项目以 [MIT License](LICENSE) 开源。第三方依赖见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。
