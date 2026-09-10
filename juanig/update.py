from __future__ import annotations

import subprocess
import sys

from juanig.constants import GITHUB_GIT


def run_update() -> int:
    cmd = [sys.executable, "-m", "pip", "install", "--upgrade", GITHUB_GIT]
    print(" ".join(cmd))
    return subprocess.call(cmd)
