"""Optional local WebP optimizer; never uploads any file."""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Convert local JPEG/PNG images to WebP using Pillow.")
    parser.add_argument("--input", required=True, help="Folder containing source images")
    parser.add_argument("--output", required=True, help="Folder for generated WebP images")
    parser.add_argument("--quality", type=int, default=82, help="WebP quality 1-100 (default 82)")
    args = parser.parse_args()
    if not 1 <= args.quality <= 100:
        parser.error("--quality must be between 1 and 100")
    source = Path(args.input)
    output = Path(args.output)
    if not source.is_dir():
        parser.error(f"input folder does not exist: {source}")
    try:
        from PIL import Image
    except ImportError:
        raise SystemExit("Pillow is required for this optional step. Install locally with: py -m pip install Pillow")

    output.mkdir(parents=True, exist_ok=True)
    found = 0
    converted = 0
    for path in source.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".jpg", ".jpeg", ".png"}:
            continue
        found += 1
        relative = path.relative_to(source).with_suffix(".webp")
        destination = output / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(path) as image:
            if image.mode not in ("RGB", "RGBA"):
                image = image.convert("RGBA" if "transparency" in image.info else "RGB")
            image.save(destination, "WEBP", quality=args.quality, method=6)
        converted += 1
        print(f"{path} -> {destination}")
    print(f"Completed local conversion: {converted} WebP file(s) from {found} source image(s).")
    print("No uploads or AWS API calls were made.")


if __name__ == "__main__":
    main()
