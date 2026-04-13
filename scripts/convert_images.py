"""Generate WebP versions of raster images; skip SVG. Skip elementor/thumbs (legacy copies)."""
from __future__ import annotations

import os
import shutil
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "images"
def should_skip(path: Path) -> bool:
    s = str(path).replace("\\", "/")
    return "elementor/thumbs/" in s


def to_webp(src: Path) -> None:
    if should_skip(src):
        return
    dst = src.with_suffix(".webp")
    try:
        im = Image.open(src)
        if im.mode == "P":
            im = im.convert("RGBA" if "transparency" in im.info else "RGB")
        elif im.mode == "RGBA":
            pass
        else:
            im = im.convert("RGB")
        im.save(dst, "WEBP", quality=85, method=6)
        print(f"OK {dst.relative_to(ROOT)}")
    except Exception as e:
        print(f"FAIL {src}: {e}")


def main() -> None:
    for path in ASSETS.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        if should_skip(path):
            continue
        to_webp(path)

    # Clean brand filenames from Elementor thumbs
    thumbs = ASSETS / "wp-content" / "uploads" / "elementor" / "thumbs"
    brand_dir = ASSETS / "wp-content" / "uploads" / "2024" / "03"
    brand_dir.mkdir(parents=True, exist_ok=True)
    cibc = next(thumbs.glob("CIBC-Logo-1-*.png"), None)
    tmu = next(thumbs.glob("TMU-rgb-*.png"), None)
    if cibc and cibc.is_file():
        dest = brand_dir / "cibc-logo.png"
        shutil.copy2(cibc, dest)
        to_webp(dest)
        print(f"Brand {dest.name}")
    if tmu and tmu.is_file():
        dest = brand_dir / "tmu-logo.png"
        shutil.copy2(tmu, dest)
        to_webp(dest)
        print(f"Brand {dest.name}")


if __name__ == "__main__":
    main()
