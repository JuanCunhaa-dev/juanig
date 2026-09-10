from __future__ import annotations

import json
import re
import time
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urlparse

import requests

INSTAGRAM_URL_RE = re.compile(
    r"(?:https?://)?(?:www\.)?instagram\.com/"
    r"(?:(?P<user>[^/?#]+)/)?"
    r"(?P<kind>p|tv|reel|reels|share/p|share/reel)/"
    r"(?P<code>[A-Za-z0-9_-]+)",
    re.IGNORECASE,
)
SHORTCODE_ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_"
CDN_HOST_MARKERS = ("instagram.", "cdninstagram.com", "fbcdn.net")
POLARIS_DOC_ID = "27128499623469141"
POLARIS_LOGGED_OUT_DOC_ID = "27130156389949648"
WEB_APP_ID = "936619743392459"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36"
)


class InstagramError(Exception):
    """Erro amigável ao resolver ou baixar um post."""


@dataclass
class MediaItem:
    index: int
    kind: str
    url: str
    thumbnail_url: str | None = None
    width: int | None = None
    height: int | None = None
    filename: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "kind": self.kind,
            "url": self.url,
            "thumbnail_url": self.thumbnail_url,
            "width": self.width,
            "height": self.height,
            "filename": self.filename,
        }


@dataclass
class PostInfo:
    url: str
    shortcode: str
    username: str | None
    caption: str | None
    product_type: str | None
    media: list[MediaItem] = field(default_factory=list)
    method: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "url": self.url,
            "shortcode": self.shortcode,
            "username": self.username,
            "caption": self.caption,
            "product_type": self.product_type,
            "kind_label": describe_post(self),
            "media": [item.to_dict() for item in self.media],
            "method": self.method,
        }


def parse_instagram_url(url: str) -> tuple[str, str]:
    text = (url or "").strip()
    if not text:
        raise InstagramError("Cole um link do Instagram.")
    if not re.match(r"^https?://", text, re.I):
        text = "https://" + text.lstrip("/")
    match = INSTAGRAM_URL_RE.search(text)
    if not match:
        raise InstagramError(
            "Esse link não parece um post, carrossel ou Reel do Instagram."
        )
    return match.group("kind").lower(), match.group("code")


def shortcode_to_pk(shortcode: str) -> int:
    value = 0
    for char in shortcode:
        value = value * 64 + SHORTCODE_ALPHABET.index(char)
    return value


def is_safe_cdn_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
    except Exception:
        return False
    if parsed.scheme not in {"http", "https"}:
        return False
    host = (parsed.hostname or "").lower()
    return any(marker in host for marker in CDN_HOST_MARKERS)


def best_version(versions: Iterable[dict[str, Any]] | None) -> dict[str, Any] | None:
    items = [item for item in (versions or []) if item.get("url")]
    if not items:
        return None
    return max(items, key=lambda item: (item.get("width") or 0) * (item.get("height") or 0))


def guess_extension(url: str, kind: str) -> str:
    path = urlparse(url).path.lower()
    for ext in (".jpg", ".jpeg", ".png", ".webp", ".mp4", ".mov", ".m4v"):
        if path.endswith(ext):
            return "jpg" if ext == ".jpeg" else ext.lstrip(".")
    return "mp4" if kind == "video" else "jpg"


def safe_filename_part(value: str | None, fallback: str) -> str:
    text = re.sub(r"[^A-Za-z0-9._-]+", "_", (value or "").strip())
    return text.strip("._") or fallback


def user_downloads_dir() -> Path:
    if os.name == "nt":
        return Path(os.environ.get("USERPROFILE", Path.home())) / "Downloads"
    return Path.home() / "Downloads"


def anonymous_filename(kind: str, index: int, ext: str) -> str:
    stem = "video" if kind == "video" else "photo"
    if index == 1:
        return f"{stem}.{ext}"
    return f"{stem}_{index}.{ext}"


def unique_path(directory: Path, filename: str) -> Path:
    path = directory / filename
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    number = 2
    while True:
        candidate = directory / f"{stem}_{number}{suffix}"
        if not candidate.exists():
            return candidate
        number += 1


def describe_post(post: PostInfo) -> str:
    kinds = {item.kind for item in post.media}
    if post.product_type == "clips" or all(item.kind == "video" for item in post.media):
        if len(post.media) == 1:
            return "Reel / vídeo"
    if len(post.media) > 1:
        if kinds == {"image"}:
            return f"Carrossel com {len(post.media)} fotos"
        if kinds == {"video"}:
            return f"Carrossel com {len(post.media)} vídeos"
        return f"Carrossel misto com {len(post.media)} itens"
    if "video" in kinds:
        return "Vídeo"
    return "Foto"


def _caption_text(media: dict[str, Any]) -> str | None:
    caption = media.get("caption")
    if isinstance(caption, dict):
        text = caption.get("text")
        return text if isinstance(text, str) and text.strip() else None
    edges = ((media.get("edge_media_to_caption") or {}).get("edges")) or []
    if edges:
        text = ((edges[0] or {}).get("node") or {}).get("text")
        return text if isinstance(text, str) and text.strip() else None
    return None


def _username(media: dict[str, Any]) -> str | None:
    user = media.get("user") or media.get("owner") or {}
    name = user.get("username")
    return name if isinstance(name, str) and name.strip() else None


def items_from_v1_media(media: dict[str, Any], shortcode: str) -> list[MediaItem]:
    children = media.get("carousel_media") or [media]
    result: list[MediaItem] = []
    for index, child in enumerate(children, start=1):
        image = best_version(((child.get("image_versions2") or {}).get("candidates")) or [])
        video = best_version(child.get("video_versions") or [])
        if video:
            kind = "video"
            chosen = video
        elif image:
            kind = "image"
            chosen = image
        else:
            continue
        url = chosen["url"]
        ext = guess_extension(url, kind)
        result.append(
            MediaItem(
                index=index,
                kind=kind,
                url=url,
                thumbnail_url=(image or {}).get("url"),
                width=chosen.get("width"),
                height=chosen.get("height"),
                filename=anonymous_filename(kind, index, ext),
            )
        )
    return result


def items_from_legacy_node(node: dict[str, Any], shortcode: str) -> list[MediaItem]:
    children = [
        (edge.get("node") or {})
        for edge in ((node.get("edge_sidecar_to_children") or {}).get("edges") or [])
    ] or [node]
    result: list[MediaItem] = []
    for index, child in enumerate(children, start=1):
        if child.get("is_video") and child.get("video_url"):
            kind = "video"
            url = child["video_url"]
        elif child.get("display_url"):
            kind = "image"
            url = child["display_url"]
        else:
            continue
        ext = guess_extension(url, kind)
        result.append(
            MediaItem(
                index=index,
                kind=kind,
                url=url,
                thumbnail_url=child.get("display_url") or child.get("thumbnail_src"),
                filename=anonymous_filename(kind, index, ext),
            )
        )
    return result


class InstagramClient:
    def __init__(self, sessionid: str | None = None) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": USER_AGENT,
                "Accept": "*/*",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            }
        )
        self.sessionid = (sessionid or "").strip() or None
        if self.sessionid:
            self.session.cookies.set(
                "sessionid", self.sessionid, domain=".instagram.com", path="/"
            )
        self._bootstrapped = False
        self._csrf = ""
        self._lsd = ""

    def _bootstrap(self) -> None:
        if self._bootstrapped:
            return
        response = self.session.get("https://www.instagram.com/", timeout=30)
        response.raise_for_status()
        self._csrf = self.session.cookies.get("csrftoken") or ""
        match = re.search(r'\["LSD",\[\],\{"token":"([^"]+)"', response.text)
        self._lsd = match.group(1) if match else ""
        self._bootstrapped = True

    def _graphql_headers(self, shortcode: str) -> dict[str, str]:
        self._bootstrap()
        return {
            "x-ig-app-id": WEB_APP_ID,
            "x-asbd-id": "359341",
            "x-ig-www-claim": "0",
            "x-csrftoken": self._csrf,
            "x-requested-with": "XMLHttpRequest",
            "origin": "https://www.instagram.com",
            "referer": f"https://www.instagram.com/p/{shortcode}/",
            "content-type": "application/x-www-form-urlencoded",
        }

    def _follow_share(self, url: str, kind: str, shortcode: str) -> tuple[str, str]:
        if not kind.startswith("share/"):
            return kind, shortcode
        response = self.session.get(url, timeout=30, allow_redirects=True)
        match = INSTAGRAM_URL_RE.search(response.url)
        if not match:
            raise InstagramError("Não consegui abrir esse link de compartilhamento.")
        return match.group("kind").lower(), match.group("code")

    def resolve(self, url: str) -> PostInfo:
        kind, shortcode = parse_instagram_url(url)
        canonical = f"https://www.instagram.com/{'reel' if 'reel' in kind else 'p'}/{shortcode}/"
        try:
            kind, shortcode = self._follow_share(canonical if kind.startswith("share/") else url, kind, shortcode)
            canonical = f"https://www.instagram.com/{'reel' if 'reel' in kind else 'p'}/{shortcode}/"
        except requests.RequestException as exc:
            raise InstagramError(f"Falha ao abrir o link: {exc}") from exc

        errors: list[str] = []
        for method, loader in (
            ("graphql_polaris", self._resolve_polaris),
            ("graphql_media_id", self._resolve_logged_out),
            ("media_info", self._resolve_media_info),
        ):
            try:
                post = loader(canonical, shortcode)
                if post and post.media:
                    post.method = method
                    return post
                errors.append(f"{method}: sem mídia")
            except InstagramError as exc:
                errors.append(f"{method}: {exc}")
            except (requests.RequestException, ValueError, KeyError, TypeError) as exc:
                errors.append(f"{method}: {exc}")

        raise InstagramError(
            "This post looks private, restricted, or Instagram blocked anonymous access. "
            "Use --sessionid (or the JUANIG_SESSIONID env var) with the sessionid cookie "
            "from a logged-in Instagram browser session."
        )

    def _resolve_polaris(self, url: str, shortcode: str) -> PostInfo:
        response = self.session.post(
            "https://www.instagram.com/graphql/query",
            data={
                "variables": json.dumps(
                    {
                        "shortcode": shortcode,
                        "__relay_internal__pv__PolarisAIGMMediaWebLabelEnabledrelayprovider": False,
                    },
                    separators=(",", ":"),
                ),
                "doc_id": POLARIS_DOC_ID,
                "server_timestamps": "true",
            },
            headers=self._graphql_headers(shortcode),
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        items = (
            ((payload.get("data") or {}).get("xdt_api__v1__media__shortcode__web_info") or {}).get("items")
            or []
        )
        if not items:
            raise InstagramError("GraphQL não devolveu o post.")
        return self._post_from_v1(url, shortcode, items[0])

    def _resolve_logged_out(self, url: str, shortcode: str) -> PostInfo:
        self._bootstrap()
        headers = self._graphql_headers(shortcode)
        headers["X-FB-Friendly-Name"] = "PolarisLoggedOutDesktopWWWPostRootContentQuery"
        headers["X-FB-LSD"] = self._lsd
        headers["X-CSRFToken"] = self._csrf
        response = self.session.post(
            "https://www.instagram.com/graphql/query",
            data={
                "lsd": self._lsd,
                "fb_api_caller_class": "RelayModern",
                "fb_api_req_friendly_name": "PolarisLoggedOutDesktopWWWPostRootContentQuery",
                "server_timestamps": "true",
                "variables": json.dumps(
                    {"media_id": str(shortcode_to_pk(shortcode))}, separators=(",", ":")
                ),
                "doc_id": POLARIS_LOGGED_OUT_DOC_ID,
            },
            headers=headers,
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()
        media = ((payload.get("data") or {}).get("xig_polaris_media")) or {}
        inner = media.get("if_not_gated_logged_out") or media
        if not inner:
            raise InstagramError("Post indisponível sem login.")
        if inner.get("image_versions2") or inner.get("video_versions") or inner.get("carousel_media"):
            return self._post_from_v1(url, shortcode, inner)
        items = items_from_legacy_node(inner, shortcode)
        if not items:
            raise InstagramError("Resposta sem arquivos de mídia.")
        return PostInfo(
            url=url,
            shortcode=shortcode,
            username=_username(inner),
            caption=_caption_text(inner),
            product_type=inner.get("product_type"),
            media=items,
        )

    def _resolve_media_info(self, url: str, shortcode: str) -> PostInfo:
        if not self.sessionid:
            raise InstagramError("Sem sessionid.")
        self._bootstrap()
        pk = shortcode_to_pk(shortcode)
        response = self.session.get(
            f"https://www.instagram.com/api/v1/media/{pk}/info/",
            headers={
                "x-ig-app-id": WEB_APP_ID,
                "x-asbd-id": "359341",
                "x-ig-www-claim": "0",
                "x-csrftoken": self._csrf,
                "referer": "https://www.instagram.com/",
            },
            timeout=30,
        )
        if "accounts/login" in response.url:
            raise InstagramError("O sessionid expirou ou é inválido.")
        response.raise_for_status()
        payload = response.json()
        items = payload.get("items") or []
        if not items:
            raise InstagramError("A API logada não devolveu o post.")
        return self._post_from_v1(url, shortcode, items[0])

    def _post_from_v1(self, url: str, shortcode: str, media: dict[str, Any]) -> PostInfo:
        items = items_from_v1_media(media, shortcode)
        if not items:
            raise InstagramError("O post veio sem foto ou vídeo.")
        return PostInfo(
            url=url,
            shortcode=media.get("code") or shortcode,
            username=_username(media),
            caption=_caption_text(media),
            product_type=media.get("product_type"),
            media=items,
        )

    def fetch_bytes(self, url: str) -> tuple[bytes, str]:
        if not is_safe_cdn_url(url):
            raise InstagramError("URL de mídia inválida.")
        response = self.session.get(
            url,
            headers={"Referer": "https://www.instagram.com/", "User-Agent": USER_AGENT},
            timeout=60,
            stream=True,
        )
        response.raise_for_status()
        return response.content, response.headers.get("content-type") or "application/octet-stream"

    def download_post(self, post: PostInfo, output_dir: Path) -> list[Path]:
        output_dir.mkdir(parents=True, exist_ok=True)
        saved: list[Path] = []
        for item in post.media:
            data, _content_type = self.fetch_bytes(item.url)
            path = unique_path(output_dir, item.filename)
            item.filename = path.name
            path.write_bytes(data)
            saved.append(path)
            time.sleep(0.15)
        return saved
