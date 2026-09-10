from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from juanig import __version__
from juanig.core import (
    InstagramClient,
    InstagramError,
    PostInfo,
    planned_paths,
    select_media,
    user_downloads_dir,
)
from juanig.setup_local import run_setup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DUMMY_TOKENS = {"url", "urls", "link", "links"}


def normalize_urls(values: list[str]) -> list[str]:
    return expand_urls(values)


def _urls_from_text(text: str) -> list[str]:
    found: list[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#") or line.lower() in DUMMY_TOKENS:
            continue
        found.append(line)
    return found


def expand_urls(values: list[str]) -> list[str]:
    found: list[str] = []
    for value in values:
        if value.lower() in DUMMY_TOKENS:
            continue
        if value == "-":
            found.extend(_urls_from_text(sys.stdin.read()))
            continue
        if value.startswith("@") and len(value) > 1:
            path = Path(value[1:]).expanduser()
            try:
                found.extend(_urls_from_text(path.read_text(encoding="utf-8")))
            except OSError as exc:
                raise InstagramError(f"Could not read URL list {path}: {exc}") from exc
            continue
        found.append(value)
    return found


def selected_index(first: bool, index: int | None) -> int | None:
    if first and index is not None:
        raise InstagramError("Use --first or --index, not both.")
    if first:
        return 1
    return index


def post_payload(url: str, post: PostInfo, saved: list[Path]) -> dict:
    media = []
    for item, path in zip(post.media, saved):
        media.append(
            {
                "index": item.index,
                "kind": item.kind,
                "path": str(path),
                "filename": path.name,
                "width": item.width,
                "height": item.height,
            }
        )
    return {
        "url": url,
        "shortcode": post.shortcode,
        "kind": post.to_dict()["kind_label"],
        "caption": post.caption,
        "files": [str(path) for path in saved],
        "media": media,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="juanig",
        usage="juanig URL [URL ...] [options]",
        description="Download Instagram photos, carousels, videos, and Reels from a link.",
    )
    parser.add_argument(
        "urls",
        nargs="*",
        metavar="URL",
        help="Instagram link, @links.txt, or - to read URLs from stdin",
    )
    parser.add_argument(
        "-o",
        "--output",
        default=os.environ.get("JUANIG_OUTPUT", str(user_downloads_dir())),
        help="Folder to save files (default: the user Downloads folder)",
    )
    parser.add_argument(
        "--sessionid",
        default=os.environ.get("JUANIG_SESSIONID"),
        help="Instagram sessionid cookie when a post requires login",
    )
    parser.add_argument("--first", action="store_true", help="Download only the first carousel item")
    parser.add_argument(
        "--index",
        type=int,
        metavar="N",
        help="Download only carousel item N (1-based)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Resolve the post and print paths without downloading",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON (best for agents)")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--setup",
        action="store_true",
        help="Put juanig on PATH and copy the skill only into IDEs already installed",
    )
    modes.add_argument(
        "--install-skills",
        action="store_true",
        help="Write the skill only into IDEs already installed on this machine",
    )
    modes.add_argument(
        "--update",
        action="store_true",
        help="Upgrade juanig to the latest version from PyPI",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    args = parser.parse_args()

    if args.setup:
        return run_setup()
    if args.install_skills:
        from juanig.setup_local import install_skills

        for path in install_skills():
            print(path)
        return 0
    if args.update:
        from juanig.update import run_update

        return run_update()

    try:
        args.urls = expand_urls(args.urls)
        index = selected_index(args.first, args.index)
    except InstagramError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    if not args.urls:
        parser.print_help()
        return 2

    from juanig.notice import maybe_warn_update

    maybe_warn_update()

    client = InstagramClient(sessionid=args.sessionid)
    output = Path(args.output).expanduser().resolve()
    posts: list[dict] = []
    errors: list[dict] = []

    for url in args.urls:
        try:
            post = select_media(client.resolve(url), index)
            saved = planned_paths(post, output) if args.dry_run else client.download_post(post, output)
            posts.append(post_payload(url, post, saved))
            if not args.json:
                label = "would save" if args.dry_run else "file(s)"
                print(f"{len(saved)} {label}")
                for path in saved:
                    print(f"  {path}")
        except InstagramError as exc:
            errors.append({"url": url, "error": str(exc)})
            if not args.json:
                print(f"Error: {url}\n  {exc}", file=sys.stderr)

    if args.json:
        print(
            json.dumps(
                {
                    "ok": not errors,
                    "dry_run": args.dry_run,
                    "output": str(output),
                    "posts": posts,
                    "errors": errors,
                },
                ensure_ascii=False,
                indent=2,
            )
        )

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
