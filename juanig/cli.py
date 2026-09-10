from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from juanig import __version__
from juanig.core import InstagramClient, InstagramError, user_downloads_dir
from juanig.setup_local import run_setup

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

DUMMY_TOKENS = {"url", "urls", "link", "links"}


def normalize_urls(values: list[str]) -> list[str]:
    return [value for value in values if value.lower() not in DUMMY_TOKENS]


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
        help="Instagram post, carousel, or Reel link. Do not type the word urls.",
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
        help="Upgrade juanig to the latest version from GitHub",
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

    args.urls = normalize_urls(args.urls)
    if not args.urls:
        parser.print_help()
        return 2

    client = InstagramClient(sessionid=args.sessionid)
    output = Path(args.output).expanduser().resolve()
    posts: list[dict] = []
    errors: list[dict] = []

    for url in args.urls:
        try:
            post = client.resolve(url)
            saved = client.download_post(post, output)
            posts.append(
                {
                    "url": url,
                    "kind": post.to_dict()["kind_label"],
                    "files": [str(path) for path in saved],
                }
            )
            if not args.json:
                print(f"{len(saved)} file(s)")
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
