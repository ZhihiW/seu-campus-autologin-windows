# SEU Campus Auto Login

适用于 Windows 10/11 的东南大学校园网自动登录工具。


> [!IMPORTANT]
> 仅支持登录页为 `http://10.9.10.100/` 的网络环境。

> [!WARNING]
> 当前门户使用 HTTP，密码传输不具备 TLS 保护。本工具无法改变门户本身的传输方式。

## 使用方法

1. 从 Releases 下载并解压 Windows ZIP；
2. 双击 `安装.cmd`，在本机窗口输入账号和密码；
3. 安装完成后，程序会在每次登录 Windows 时自动检查校园网。

压缩包里只保留三个入口：

```text
安装.cmd    安装并配置开机任务
测试.cmd    检查环境，可选择立即运行一次
卸载.cmd    删除公开版任务、凭据、程序和日志
```

安装后的配置、检查和立即运行功能也可以从开始菜单的 `SEU Campus Auto Login OSS` 中使用。

## 特点

- 无需安装 Python，调用电脑已有的 Microsoft Edge；
- 密码保存在 Windows Credential Manager，不写入脚本和日志；
- 已联网时直接退出，不读取密码、不重复登录；
- 只允许向 `10.9.10.100` 提交凭据；
- 错误密码不会连续重试；
- 无遥测、无广告、无自动上传。


## 隐私与安全

请勿在 Issue 中提交账号、密码、Cookie、学号或完整日志。

- [安全政策](.github/SECURITY.md)
- [隐私说明](docs/PRIVACY.md)

## 开发

- [开发、测试与发布](docs/DEVELOPMENT.md)
- [参与贡献](.github/CONTRIBUTING.md)
- [更新记录](docs/CHANGELOG.md)


项目采用 [MIT License](LICENSE)，第三方组件见 [说明](docs/THIRD_PARTY_NOTICES.md)。
