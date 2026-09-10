from __future__ import annotations

import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from juanig import __version__

PYPI_JSON = "https://pypi.org/pypi/juanig/json"
CACHE_TTL_SECONDS = 24 * 60 * 60
FETCH_TIMEOUT_SECONDS = 2


def cache_path() -> Path:
    if os.name == "nt":
        base = Path(os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local"))
        return base / "juanig" / "update-check.json"
    xdg = os.environ.get("XDG_CACHE_HOME")
    base = Path(xdg) if xdg else Path.home() / ".cache"
    return base / "juanig" / "update-check.json"


def parse_version(text: str) -> tuple[int, ...]:
    parts: list[int] = []
    for chunk in (text or "").split("."):
        digits = "".join(char for char in chunk if char.isdigit())
        parts.append(int(digits) if digits else 0)
    return tuple(parts) or (0,)


def is_newer(latest: str, current: str) -> bool:
    return parse_version(latest) > parse_version(current)


def _read_cache() -> tuple[float, str] | None:
    path = cache_path()
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    checked = payload.get("checked_at")
    version = payload.get("version")
    if not isinstance(checked, (int, float)) or not isinstance(version, str) or not version:
        return None
    return float(checked), version


def _write_cache(version: str) -> None:
    path = cache_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps({"checked_at": time.time(), "version": version}),
        encoding="utf-8",
    )


def fetch_latest() -> str | None:
    request = urllib.request.Request(
        PYPI_JSON,
        headers={"User-Agent": f"juanig/{__version__}", "Accept": "application/json"},
    )
    with urllib.request.urlopen(request, timeout=FETCH_TIMEOUT_SECONDS) as response:
        payload = json.load(response)
    version = (payload.get("info") or {}).get("version")
    return version if isinstance(version, str) and version.strip() else None


def latest_version() -> str | None:
    cached = _read_cache()
    if cached and (time.time() - cached[0]) < CACHE_TTL_SECONDS:
        return cached[1]
    latest = fetch_latest()
    if latest:
        _write_cache(latest)
        return latest
    return cached[1] if cached else None


def maybe_warn_update(current: str | None = None) -> None:
    if os.environ.get("JUANIG_NO_UPDATE_CHECK", "").strip().lower() in {"1", "true", "yes"}:
        return
    installed = current or __version__
    try:
        latest = latest_version()
        if latest and is_newer(latest, installed):
            print(
                f"juanig {installed} is installed; {latest} is available. Run: juanig --update",
                file=sys.stderr,
            )
    except (OSError, ValueError, urllib.error.URLError, TimeoutError):
        return
    except Exception:
        return
