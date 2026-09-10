from __future__ import annotations

import subprocess
import sys

REPO = "git+https://github.com/JuanCunhaa-dev/juanig.git"


def run_update() -> int:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", REPO]
    print(" ".join(cmd))
    return subprocess.call(cmd)
