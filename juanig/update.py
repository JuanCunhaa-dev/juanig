from __future__ import annotations

import subprocess
import sys

def run_update() -> int:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", "juanig"]
    print(" ".join(cmd))
    return subprocess.call(cmd)
