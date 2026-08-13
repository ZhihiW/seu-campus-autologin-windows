"""允许通过 ``python -m seu_autologin`` 启动。"""

from .cli import main

if __name__ == "__main__":
    raise SystemExit(main())
