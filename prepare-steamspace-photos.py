#!/usr/bin/env python3
"""Crop Flickr originals for the STEAMSPACE teacher trifold.

Outputs land in assets/photos/steamspace/ so ABHS STEM tiles in
assets/photos/ stay untouched. Run before build-steamspace.py.

Source files live in assets/photos/source/ (same Flickr originals as the
STEM brochure). Add 54957775725_snas-wide.jpg if missing:

  curl -fsSL -o assets/photos/source/54957775725_snas-wide.jpg \\
    https://live.staticflickr.com/65535/54957775725_65e8519654_o.jpg
"""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
SRC = ROOT / "assets" / "photos" / "source"
OUT = ROOT / "assets" / "photos" / "steamspace"

# (source filename, output filename, target width, aspect w/h, focus_x, focus_y)
TILES = [
    (
        "54946755080_laptop-star.jpg",
        "cover-hero.jpg",
        1100,
        3.6667 / 8.5,  # trifold cover panel (portrait)
        0.5,
        0.34,  # laptop + star project, keep hands low
    ),
    (
        "35537136070_vex-iq-chassis.jpg",
        "tile-workshop.jpg",
        1600,
        16 / 8,
        0.52,
        0.46,  # hands-on chassis build
    ),
    (
        "52210203520_cardboard-topo.jpg",
        "tile-brochurepic.jpg",
        1600,
        4 / 3,  # back cover uses 4:3 via CSS
        0.46,
        0.40,  # painted cardboard topo model
    ),
    (
        "54830501938_alt-build.jpg",
        "tile-lego.jpg",
        1200,
        4 / 3,
        0.48,
        0.42,  # tabletop building / making
    ),
    (
        "35884396266_pink-leds.jpg",
        "tile-circuits.jpg",
        1200,
        4 / 3,
        0.50,
        0.44,  # paper circuits + LEDs
    ),
    (
        "54946750635_laser-cut-box.jpg",
        "tile-lasercut.jpg",
        1200,
        4 / 3,
        0.50,
        0.38,  # laser-cut box on bed
    ),
    (
        "54946643368_lightburn.jpg",
        "tile-microbit.jpg",
        1200,
        4 / 3,
        0.48,
        0.40,  # LightBurn / digital design screen
    ),
    (
        "45440131294_robotic-hand.jpg",
        "tile-puzzle.jpg",
        1200,
        4 / 3,
        0.50,
        0.36,  # mechanical design / puzzle engineering
    ),
    (
        "54957775725_snas-wide.jpg",
        "tile-building106.jpg",
        1600,
        16 / 6.2,  # tile--short
        0.50,
        0.55,  # wide venue context, faces distant
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
    if not src.exists():
        raise FileNotFoundError(f"Missing source photo: {src}")
    img = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    cropped = crop_to_aspect(img, aspect, focus_x, focus_y)
    height = round(width / aspect)
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / out_name
    resized.save(dest, "JPEG", quality=92, optimize=True, subsampling=0)
    print(f"  {out_name}: {resized.size[0]}x{resized.size[1]}  (from {src_name})")


def main() -> None:
    print("Preparing STEAMSPACE trifold photos …")
    for args in TILES:
        prepare_tile(*args)
    print(f"Done — wrote {len(TILES)} files to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
