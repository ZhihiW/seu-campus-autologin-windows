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

