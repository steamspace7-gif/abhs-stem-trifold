#!/usr/bin/env python3
"""Crop and resize Flickr originals for trifold tile slots.

Each tile has a fixed aspect ratio baked into build.py CSS.  Source photos
are center-cropped with per-image focal points so the subject stays in frame.
Output JPEGs land in assets/photos/ at print-friendly resolution (~300 DPI
for the panel width they occupy).
"""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
SRC = ROOT / "assets" / "photos" / "source"
OUT = ROOT / "assets" / "photos"

# (source filename, output filename, target width, aspect w/h, focus_x, focus_y)
TILES = [
    (
        "52210203520_cardboard-topo.jpg",
        "tile-brochurepic.jpg",
        1600,
        16 / 8,  # tile--wide
        0.48,
        0.42,  # painted cardboard topo model + river (not laser-cut)
    ),
    (
        "54946643368_lightburn.jpg",
        "tile-circuits.jpg",
        1200,
        4 / 3,
        0.48,
        0.42,  # LightBurn workspace centred on screen
    ),
    (
        "54957714109_snas25.jpg",
        "tile-vex.jpg",
        1600,
        16 / 8.0,  # crop looser than tile--short (16/6.2); cover + object-position in CSS
        0.5,
        0.40,  # balance faces (upper) with field/robots (lower)
    ),
    (
        "35537136070_vex-iq-chassis.jpg",
        "tile-teamwork.jpg",
        1600,
        16 / 8,  # tile--wide
        0.5,
        0.44,  # hands-on VEX IQ chassis build (not competition)
    ),
]


def crop_to_aspect(
    img: Image.Image, aspect: float, focus_x: float = 0.5, focus_y: float = 0.5
) -> Image.Image:
    """Center-biased crop; focus 0=left/top, 1=right/bottom."""
    w, h = img.size
    current = w / h
    if current > aspect:
        new_w = int(h * aspect)
        x0 = max(0, min(w - new_w, int((w - new_w) * focus_x)))
        return img.crop((x0, 0, x0 + new_w, h))
    new_h = int(w / aspect)
    y0 = max(0, min(h - new_h, int((h - new_h) * focus_y)))
    return img.crop((0, y0, w, y0 + new_h))


def prepare_tile(
    src_name: str,
    out_name: str,
    width: int,
    aspect: float,
    focus_x: float,
    focus_y: float,
) -> None:
    src = SRC / src_name
    img = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    cropped = crop_to_aspect(img, aspect, focus_x, focus_y)
    height = round(width / aspect)
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
    dest = OUT / out_name
    resized.save(dest, "JPEG", quality=92, optimize=True, subsampling=0)
    print(f"  {out_name}: {resized.size[0]}x{resized.size[1]}  (from {src_name})")


def main() -> None:
    print("Preparing trifold photo tiles …")
    for args in TILES:
        prepare_tile(*args)
    print("Done.")


if __name__ == "__main__":
    main()
