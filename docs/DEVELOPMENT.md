# 开发与发布

## 本地开发

需要 Windows 10/11、Python 3.10–3.12 和 Microsoft Edge：

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -U pip
.\.venv\Scripts\python.exe -m pip install -e ".[dev]"
.\.venv\Scripts\python.exe -m ruff check .
.\.venv\Scripts\python.exe -m pytest --cov=seu_autologin --cov-report=term-missing
```

程序调用系统 Edge，不需要运行 `playwright install`。

## 构建

```powershell
powershell -NoProfile -File .\scripts\build.ps1 -PythonExe .\.venv\Scripts\python.exe
```

构建结果位于 `release`，采用 PyInstaller `onedir`，并生成 ZIP 和 SHA256。

## 发布门槛

- Ruff、单元测试和 80% 覆盖率门槛全部通过；
- 干净 Windows 10/11 电脑不安装 Python 也能运行；
- 已联网、门户不可达、错误密码和页面改版均安全停止；
- 3–5 名志愿者在两个使用相同网关的位置完成至少 20 次自然启动；
- 没有凭据泄露、未知地址提交或卸载残留。
