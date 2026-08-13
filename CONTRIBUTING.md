# 参与贡献

感谢帮助改进本项目。提交代码前请遵守以下规则：

1. 不要提交真实账号、密码、Cookie、抓包文件或未经脱敏的日志。
2. 不要把登录地址改成任意可配置 URL；新增网关必须经过单独审核并加入固定允许列表。
3. 不要复制学校门户的完整 JavaScript、HTML、图标或校徽；测试使用最小化的合成页面。
4. 新功能应附带测试，安全保护逻辑不得降低覆盖率。
5. 新增注释、文档和用户提示默认使用简体中文。

本地检查：

```powershell
python -m pip install -e ".[dev]"
python -m ruff check .
python -m pytest --cov=seu_autologin --cov-report=term-missing
```

提交 Issue 前请先运行 `SEUCampusAutoLoginOSS.exe diagnose`，只粘贴生成的脱敏报告，并再次人工检查其中没有个人信息。
