#!/usr/bin/env python3
"""Crop source photos for the STEAMSPACE teacher trifold.

Outputs land in assets/photos/steamspace/ so ABHS STEM tiles in
assets/photos/ stay untouched. Run before build-steamspace.py.

Flickr originals: assets/photos/source/
Official site images: assets/photos/steamspace/source/
  puzzlepic1_edited.jpg          — 6th grade Puzzle Design (steamspace.vercel.app)
  gallery-building-106-clean.png — Building 106 (steamspace.vercel.app)
"""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
FLICKR_SRC = ROOT / "assets" / "photos" / "source"
SITE_SRC = ROOT / "assets" / "photos" / "steamspace" / "source"
OUT = ROOT / "assets" / "photos" / "steamspace"

# (source dir, source filename, output filename, target width, aspect w/h, focus_x, focus_y)
TILES = [
    (
        FLICKR_SRC,
        "54946755080_laptop-star.jpg",
        "cover-hero.jpg",
        1100,
        3.6667 / 8.5,  # trifold cover panel (portrait)
        0.5,
        0.34,  # laptop + star project, keep hands low
    ),
    (
        FLICKR_SRC,
        "35537136070_vex-iq-chassis.jpg",
        "tile-workshop.jpg",
        1600,
        16 / 8,
        0.52,
        0.46,  # hands-on chassis build
    ),
    (
        FLICKR_SRC,
        "52210203520_cardboard-topo.jpg",
        "tile-brochurepic.jpg",
        1600,
        4 / 3,  # back cover uses 4:3 via CSS
        0.46,
        0.40,  # painted cardboard topo model
    ),
    (
        FLICKR_SRC,
        "54830501938_alt-build.jpg",
        "tile-lego.jpg",
        1200,
        4 / 3,
        0.48,
        0.42,  # tabletop building / making
    ),
    (
        FLICKR_SRC,
        "35884396266_pink-leds.jpg",
        "tile-circuits.jpg",
        1200,
        4 / 3,
        0.50,
        0.44,  # paper circuits + LEDs
    ),
    (
        FLICKR_SRC,
        "54946750635_laser-cut-box.jpg",
        "tile-lasercut.jpg",
        1200,
        4 / 3,
        0.50,
        0.38,  # laser-cut box on bed
    ),
    (
        FLICKR_SRC,
        "54946643368_lightburn.jpg",
        "tile-microbit.jpg",
        1200,
        4 / 3,
        0.48,
        0.40,  # LightBurn / digital design screen
    ),
    (
        SITE_SRC,
        "puzzlepic1_edited.jpg",
        "tile-puzzle.jpg",
        1200,
        4 / 3,
        0.50,
        0.45,  # official site — 6th grade puzzle design
    ),
    (
        SITE_SRC,
        "gallery-building-106-clean.png",
        "tile-building106.jpg",
        1600,
        16 / 6.2,  # tile--short
        0.50,
        0.48,  # official site — Building 106 exterior
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
    src_dir: Path,
    src_name: str,
    out_name: str,
    width: int,
    aspect: float,
    focus_x: float,
    focus_y: float,
) -> None:
    src = src_dir / src_name
    if not src.exists():
        raise FileNotFoundError(f"Missing source photo: {src}")
    img = ImageOps.exif_transpose(Image.open(src).convert("RGB"))
    cropped = crop_to_aspect(img, aspect, focus_x, focus_y)
    height = round(width / aspect)
    resized = cropped.resize((width, height), Image.Resampling.LANCZOS)
    OUT.mkdir(parents=True, exist_ok=True)
    dest = OUT / out_name
    resized.save(dest, "JPEG", quality=92, optimize=True, subsampling=0)
    label = "site" if src_dir == SITE_SRC else "flickr"
    print(f"  {out_name}: {resized.size[0]}x{resized.size[1]}  ({label}: {src_name})")


def main() -> None:
    print("Preparing STEAMSPACE trifold photos …")
    for args in TILES:
        prepare_tile(*args)
    print(f"Done — wrote {len(TILES)} files to {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
