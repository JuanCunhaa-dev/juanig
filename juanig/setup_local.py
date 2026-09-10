from __future__ import annotations

import os
import shutil
import sys
from importlib.resources import files
from pathlib import Path


def skill_text() -> str:
    return files("juanig.data").joinpath("SKILL.md").read_text(encoding="utf-8")


def skill_targets() -> list[Path]:
    home = Path.home()
    targets = [
        home / ".cursor" / "skills" / "juanig" / "SKILL.md",
        home / ".claude" / "skills" / "juanig" / "SKILL.md",
        home / ".codeium" / "windsurf" / "skills" / "juanig" / "SKILL.md",
        home / ".continue" / "skills" / "juanig" / "SKILL.md",
        home / ".agents" / "skills" / "juanig" / "SKILL.md",
    ]
    cwd = Path.cwd()
    for relative in (
        Path(".cursor") / "skills" / "juanig" / "SKILL.md",
        Path(".claude") / "skills" / "juanig" / "SKILL.md",
        Path(".agents") / "skills" / "juanig" / "SKILL.md",
    ):
        if (cwd / relative.parts[0]).exists():
            targets.append(cwd / relative)
    return targets


def install_skills() -> list[Path]:
    text = skill_text()
    written: list[Path] = []
    for path in skill_targets():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def install_dir() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "Programs" / "juanig"
    return Path.home() / ".local" / "bin"


def add_windows_user_path(directory: str) -> None:
    import winreg

    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
    try:
        current, _kind = winreg.QueryValueEx(key, "Path")
    except FileNotFoundError:
        current = ""
    parts = [part for part in current.split(";") if part]
    if directory not in parts:
        parts.append(directory)
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, ";".join(parts))
    winreg.CloseKey(key)
    try:
        import ctypes

        ctypes.windll.user32.SendMessageTimeoutW(0xFFFF, 0x001A, 0, "Environment", 0x0002, 5000, None)
    except Exception:
        pass


def install_binary() -> Path | None:
    if not getattr(sys, "frozen", False):
        return None
    source = Path(sys.executable)
    target_dir = install_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ("juanig.exe" if os.name == "nt" else "juanig")
    if source.resolve() != target.resolve():
        shutil.copy2(source, target)
    if os.name == "nt":
        add_windows_user_path(str(target_dir))
    else:
        target.chmod(target.stat().st_mode | 0o111)
    return target


def run_setup() -> int:
    binary = install_binary()
    skills = install_skills()
    if binary:
        print(f"CLI installed: {binary}")
        if os.name == "nt":
            print("Open a new terminal so PATH picks up juanig.")
    else:
        print("Python install detected. Use the juanig command from your environment.")
    print("Skills installed:")
    for path in skills:
        print(f"  {path}")
    return 0
