import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from juanig import __version__
from juanig.cli import main, normalize_urls
from juanig.core import (
    InstagramError,
    MediaItem,
    PostInfo,
    anonymous_filename,
    describe_post,
    is_safe_cdn_url,
    parse_instagram_url,
    shortcode_to_pk,
    unique_path,
)


class ParseUrlTests(unittest.TestCase):
    def test_post_and_reel(self) -> None:
        self.assertEqual(
            parse_instagram_url("https://www.instagram.com/p/C5tiphGurNB/"),
            ("p", "C5tiphGurNB"),
        )
        self.assertEqual(
            parse_instagram_url("https://www.instagram.com/reel/DW2QBZ_CSrw/"),
            ("reel", "DW2QBZ_CSrw"),
        )

    def test_query_and_missing_scheme(self) -> None:
        kind, code = parse_instagram_url("www.instagram.com/p/AAAA/?img_index=1")
        self.assertEqual((kind, code), ("p", "AAAA"))

    def test_rejects_garbage(self) -> None:
        with self.assertRaises(InstagramError):
            parse_instagram_url("https://example.com/photo")


class HelperTests(unittest.TestCase):
    def test_normalize_urls_drops_dummy_words(self) -> None:
        self.assertEqual(
            normalize_urls(["urls", "https://www.instagram.com/p/AAAA/"]),
            ["https://www.instagram.com/p/AAAA/"],
        )

    def test_anonymous_names(self) -> None:
        self.assertEqual(anonymous_filename("image", 1, "jpg"), "photo.jpg")
        self.assertEqual(anonymous_filename("video", 2, "mp4"), "video_2.mp4")

    def test_unique_path(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "photo.jpg").write_bytes(b"x")
            self.assertEqual(unique_path(root, "photo.jpg").name, "photo_2.jpg")

    def test_cdn_allowlist(self) -> None:
        self.assertTrue(is_safe_cdn_url("https://scontent.cdninstagram.com/v/t.jpg"))
        self.assertFalse(is_safe_cdn_url("https://evil.example/file.jpg"))

    def test_shortcode_to_pk(self) -> None:
        self.assertGreater(shortcode_to_pk("C5tiphGurNB"), 0)
        with self.assertRaises(InstagramError):
            shortcode_to_pk("***")
        with self.assertRaises(InstagramError):
            shortcode_to_pk("")

    def test_describe_post(self) -> None:
        photo = PostInfo(
            url="https://www.instagram.com/p/AAAA/",
            shortcode="AAAA",
            username=None,
            caption=None,
            product_type=None,
            media=[MediaItem(index=1, kind="image", url="https://scontent.cdninstagram.com/x.jpg")],
        )
        self.assertEqual(describe_post(photo), "Photo")
        photo.product_type = "clips"
        photo.media = [MediaItem(index=1, kind="video", url="https://scontent.cdninstagram.com/x.mp4")]
        self.assertEqual(describe_post(photo), "Reel")
        photo.product_type = None
        photo.media = [
            MediaItem(index=1, kind="image", url="https://scontent.cdninstagram.com/a.jpg"),
            MediaItem(index=2, kind="image", url="https://scontent.cdninstagram.com/b.jpg"),
        ]
        self.assertEqual(describe_post(photo), "Carousel (2 photos)")


class CliTests(unittest.TestCase):
    def test_version_flag(self) -> None:
        with patch("sys.argv", ["juanig", "--version"]):
            with self.assertRaises(SystemExit) as caught:
                main()
        self.assertEqual(caught.exception.code, 0)

    def test_help_without_urls(self) -> None:
        with patch("sys.argv", ["juanig"]):
            self.assertEqual(main(), 2)

    def test_package_version(self) -> None:
        self.assertRegex(__version__, r"^\d+\.\d+\.\d+$")


if __name__ == "__main__":
    unittest.main()
