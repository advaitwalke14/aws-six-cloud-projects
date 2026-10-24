import argparse
import os
import sys
from pathlib import Path
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from PIL import Image, ImageOps, UnidentifiedImageError
BUCKET = os.getenv(
    "S3_BUCKET",
    "product-images-809772106173-20261017",
)
REGION = os.getenv("S3_REGION", "ap-south-1")
MAX_URL_SECONDS = 300
ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/webp"}
ALLOWED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "BMP", "TIFF", "GIF"}
def validate_key(key):
    if not key or not key.strip():
        raise ValueError("S3 object key cannot be empty.")
    if key.startswith("/") or "\x00" in key:
        raise ValueError("S3 object key must be a relative, non-empty key.")
    if any(part in {".", ".."} for part in key.split("/")):
        raise ValueError("S3 object key cannot contain . or .. path segments.")
    return key
def get_s3_client():
    return boto3.client("s3", region_name=REGION)
def generate_upload_url(key, content_type="image/jpeg", s3_client=None):
    key = validate_key(key)
    if content_type not in ALLOWED_CONTENT_TYPES:
        raise ValueError(
            "Unsupported content type. Use image/jpeg, image/png, or image/webp."
        )
    client = s3_client if s3_client is not None else get_s3_client()
    return client.generate_presigned_url(
        "put_object",
        Params={
            "Bucket": BUCKET,
            "Key": key,
            "ContentType": content_type,
            "ServerSideEncryption": "AES256",
        },
        ExpiresIn=MAX_URL_SECONDS,
    )
def generate_download_url(key, s3_client=None):
    key = validate_key(key)
    client = s3_client if s3_client is not None else get_s3_client()
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": BUCKET, "Key": key},
        ExpiresIn=MAX_URL_SECONDS,
    )
def create_thumbnail(source, destination, size=200, quality=85):
    source_path = Path(source)
    output_path = Path(destination)
    if not source_path.is_file():
        raise FileNotFoundError(f"Source image not found: {source_path}")
    if source_path.resolve() == output_path.resolve():
        raise ValueError("Source and destination must be different files.")
    if output_path.suffix.lower() not in {".jpg", ".jpeg"}:
        raise ValueError("Thumbnail destination must end in .jpg or .jpeg.")
    if not 1 <= size <= 2000:
        raise ValueError("Thumbnail size must be between 1 and 2000 pixels.")
    if not 1 <= quality <= 95:
        raise ValueError("JPEG quality must be between 1 and 95.")
    with Image.open(source_path) as opened:
        if opened.format not in ALLOWED_IMAGE_FORMATS:
            raise ValueError(f"Unsupported image format: {opened.format}")
        image = ImageOps.exif_transpose(opened)
        image.thumbnail((size, size), Image.Resampling.LANCZOS)
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            rgba = image.convert("RGBA")
            result = Image.new("RGB", rgba.size, "white")
            result.paste(rgba, mask=rgba.getchannel("A"))
        else:
            result = image.convert("RGB")
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.save(output_path, format="JPEG", quality=quality, optimize=True)
    return output_path
def build_parser():
    parser = argparse.ArgumentParser(
        description="Private S3 product-image utilities."
    )
    sub = parser.add_subparsers(dest="action", required=True)
    upload = sub.add_parser("upload-url", help="Generate a presigned upload URL.")
    upload.add_argument("key")
    upload.add_argument("--type", default="image/jpeg",
                        choices=sorted(ALLOWED_CONTENT_TYPES))
    download = sub.add_parser(
        "download-url", help="Generate a presigned download URL."
    )
    download.add_argument("key")
    thumbnail = sub.add_parser(
        "thumbnail", help="Create a local JPEG thumbnail."
    )
    thumbnail.add_argument("source")
    thumbnail.add_argument("destination")
    thumbnail.add_argument("--size", type=int, default=200)
    thumbnail.add_argument("--quality", type=int, default=85)
    return parser
def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.action == "upload-url":
            print(generate_upload_url(args.key, args.type))
        elif args.action == "download-url":
            print(generate_download_url(args.key))
        elif args.action == "thumbnail":
            output = create_thumbnail(
                args.source,
                args.destination,
                size=args.size,
                quality=args.quality,
            )
            print(f"Thumbnail saved: {output}")
        return 0
    except (
        ValueError,
        FileNotFoundError,
        OSError,
        UnidentifiedImageError,
        BotoCoreError,
        ClientError,
    ) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
if __name__ == "__main__":
    sys.exit(main())
