from __future__ import annotations

import os
import sys
from importlib.resources import files
from pathlib import Path


def skill_text() -> str:
    return files("juanig.data").joinpath("SKILL.md").read_text(encoding="utf-8")


def skill_targets() -> list[Path]:
    home = Path.home()
    candidates = [
        (home / ".cursor", home / ".cursor" / "skills" / "juanig" / "SKILL.md"),
        (home / ".claude", home / ".claude" / "skills" / "juanig" / "SKILL.md"),
        (home / ".codeium", home / ".codeium" / "windsurf" / "skills" / "juanig" / "SKILL.md"),
        (home / ".continue", home / ".continue" / "skills" / "juanig" / "SKILL.md"),
        (home / ".agents", home / ".agents" / "skills" / "juanig" / "SKILL.md"),
    ]
    targets = [path for marker, path in candidates if marker.exists()]
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


def install_launcher() -> Path:
    target_dir = install_dir()
    target_dir.mkdir(parents=True, exist_ok=True)
    stale_exe = target_dir / "juanig.exe"
    if stale_exe.exists():
        stale_exe.unlink()
    if os.name == "nt":
        python = Path(sys.executable)
        target = target_dir / "juanig.cmd"
        target.write_text(f'@echo off\r\n"{python}" -m juanig %*\r\n', encoding="ascii")
        add_windows_user_path(str(target_dir))
        return target
    target = target_dir / "juanig"
    target.write_text(f"#!/usr/bin/env bash\nexec {sys.executable!s} -m juanig \"$@\"\n", encoding="utf-8")
    target.chmod(target.stat().st_mode | 0o111)
    return target


def run_setup() -> int:
    if getattr(sys, "frozen", False):
        print(
            "This unsigned .exe is blocked by Windows Smart App Control. "
            "Use the PowerShell installer instead:"
        )
        print(
            "  irm https://github.com/JuanCunhaa-dev/juanig/releases/latest/download/install.ps1 | iex"
        )
        return 2
    launcher = install_launcher()
    skills = install_skills()
    print(f"CLI installed: {launcher}")
    if skills:
        print("Skills installed for IDEs already present on this machine:")
        for path in skills:
            print(f"  {path}")
    else:
        print("No AI/IDE skill folder found. The CLI still works; paste AI-SETUP.md if you want a skill.")
    if os.name == "nt":
        print("Open a new terminal so PATH picks up juanig.")
    return 0
