import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock
from PIL import Image
import app
class S3UrlTests(unittest.TestCase):
    def setUp(self):
        self.s3 = Mock()
        self.s3.generate_presigned_url.return_value = (
            "https://example.invalid/signed"
        )
    def test_upload_url_uses_encryption_and_short_expiry(self):
        result = app.generate_upload_url(
            "products/test.jpg", "image/jpeg", self.s3
        )
        self.assertEqual(result, "https://example.invalid/signed")
        self.s3.generate_presigned_url.assert_called_once_with(
            "put_object",
            Params={
                "Bucket": app.BUCKET,
                "Key": "products/test.jpg",
                "ContentType": "image/jpeg",
                "ServerSideEncryption": "AES256",
            },
            ExpiresIn=300,
        )
    def test_download_url(self):
        result = app.generate_download_url("products/test.jpg", self.s3)
        self.assertEqual(result, "https://example.invalid/signed")
        self.s3.generate_presigned_url.assert_called_once_with(
            "get_object",
            Params={
                "Bucket": app.BUCKET,
                "Key": "products/test.jpg",
            },
            ExpiresIn=300,
        )
    def test_invalid_key_rejected(self):
        for key in ("", "/absolute.jpg", "../secret.jpg", "a/../b.jpg"):
            with self.subTest(key=key):
                with self.assertRaises(ValueError):
                    app.generate_download_url(key, self.s3)
    def test_invalid_content_type_rejected(self):
        with self.assertRaises(ValueError):
            app.generate_upload_url(
                "products/test.jpg", "text/html", self.s3
            )
        self.s3.generate_presigned_url.assert_not_called()
class ThumbnailTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.source = self.root / "source.jpg"
        Image.new("RGB", (640, 480), (30, 120, 200)).save(self.source)
    def tearDown(self):
        self.temp.cleanup()
    def test_thumbnail_is_jpeg_within_requested_size(self):
        output = self.root / "nested" / "thumbnail.jpg"
        result = app.create_thumbnail(self.source, output)
        self.assertEqual(result, output)
        with Image.open(output) as image:
            self.assertEqual(image.format, "JPEG")
            self.assertEqual(image.mode, "RGB")
            self.assertLessEqual(max(image.size), 200)
            self.assertEqual(image.size, (200, 150))
    def test_missing_source_rejected(self):
        with self.assertRaises(FileNotFoundError):
            app.create_thumbnail(self.root / "missing.jpg",
                                 self.root / "out.jpg")
    def test_source_and_destination_must_differ(self):
        with self.assertRaises(ValueError):
            app.create_thumbnail(self.source, self.source)
    def test_non_jpeg_destination_rejected(self):
        with self.assertRaises(ValueError):
            app.create_thumbnail(self.source, self.root / "out.png")
    def test_invalid_size_rejected(self):
        with self.assertRaises(ValueError):
            app.create_thumbnail(
                self.source, self.root / "out.jpg", size=0
            )
    def test_invalid_quality_rejected(self):
        with self.assertRaises(ValueError):
            app.create_thumbnail(
                self.source, self.root / "out.jpg", quality=100
            )
if __name__ == "__main__":
    unittest.main()
