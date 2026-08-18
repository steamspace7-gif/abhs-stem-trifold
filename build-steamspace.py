#!/usr/bin/env python3
"""Generate a teacher-facing STEAMSPACE trifold brochure.

Same print setup as the ABHS STEM brochure (letter-size, 3-panel fold),
but the copy is only about STEAMSPACE field trips — no ABHS STEM program
content. The live site URL is printed on the cover, back, and inside.
"""

import base64
import io
import subprocess
from pathlib import Path

from PIL import Image

import build as abhs

ROOT = Path(__file__).parent
OUT = ROOT / "steamspace-brochure.html"
PDF = ROOT / "steamspace-brochure.pdf"
PREVIEW = ROOT / "steamspace-brochure-preview.png"
COVER = ROOT / "steamspace-brochure-cover.png"

SITE_URL = "steamspace.vercel.app"


def png_uri(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    encoded = base64.b64encode(buf.getvalue()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def knock_out_black(path: Path, threshold: int = 28) -> Image.Image:
    """Make near-black logo pixels transparent so the mark sits on photos."""
    im = Image.open(path).convert("RGBA")
    pixels = im.load()
    width, height = im.size
    for y in range(height):
        for x in range(width):
            r, g, b, _a = pixels[x, y]
            if r <= threshold and g <= threshold and b <= threshold:
                pixels[x, y] = (0, 0, 0, 0)
    return im


def logo_on_sand(path: Path) -> Image.Image:
    """Composite the knocked-out logo onto opaque sand.

    Chrome print flattens <img> alpha against the page photo, not the parent
    box, so a transparent PNG makes the framed sand look ~40% even when the
    CSS fill is 100%.
    """
    logo = knock_out_black(path)
    canvas = Image.new("RGBA", logo.size, (247, 241, 230, 255))
    canvas.alpha_composite(logo)
    return canvas.convert("RGB")


LOGO_CLEAR = png_uri(logo_on_sand(abhs.ASSETS / "logo_stem_trimmed.png"))
COVER_HERO = abhs.data_uri("photos/cover-hero.jpg")

EXTRA_CSS = """
.cover-logo-wrap {
  width: 92%;
  margin: 0 auto 0.16in;
  padding: calc(0.08in + 5px) 0.1in 0.07in;
  /* Solid sand. CSS rgba over the darkened cover photo reads far thinner
     than the alpha number (75% looked like ~40% in print). */
  background: var(--sand);
  border: 2.5px solid var(--pine);
  border-radius: 12px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.35);
}
.cover-logo {
  width: 100%;
  max-height: 1.42in;
  object-fit: contain;
  display: block;
  margin: 0;
  background: var(--sand);
}
.cover-url {
  margin-top: auto;
  font-family: var(--font-brand);
  font-size: 13.5pt;
  font-weight: 600;
  background: var(--sun);
  color: var(--ink);
  padding: 0.09in 0.16in;
  border-radius: 12px;
  box-shadow: 0 8px 18px rgba(240, 180, 41, 0.45);
  letter-spacing: 0.01em;
}
.cover-place {
  margin-top: 0.12in;
  font-size: 9.5pt;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.94);
}
.fact-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.08in;
  margin-bottom: 0.12in;
}
.fact {
  background: var(--paper);
  border: var(--hairline);
  border-radius: 11px;
  padding: 0.1in 0.08in;
  text-align: center;
  box-shadow: var(--card-shadow);
}
.fact strong {
  display: block;
  font-family: var(--font-brand);
  font-size: 10.5pt;
  color: var(--pine-deep);
  line-height: 1.15;
  margin-bottom: 0.02in;
}
.fact span {
  font-size: 7.5pt;
  color: var(--ink-soft);
  line-height: 1.25;
}
.logo-footer {
  max-width: 2.35in;
  width: 100%;
  height: auto;
  display: block;
  margin: 0.12in auto 0;
  filter: drop-shadow(0 2px 8px rgba(28, 42, 36, 0.18));
}
.url-line {
  font-family: var(--font-brand);
  font-size: 12pt;
  font-weight: 600;
  color: var(--pine-deep);
  text-align: center;
  background: rgba(240, 180, 41, 0.22);
  border: var(--hairline);
  border-radius: 10px;
  padding: 0.08in 0.1in;
  margin: 0.08in 0 0.12in;
}
.faq-item {
  margin-bottom: 0.09in;
}
.faq-item:last-child { margin-bottom: 0; }
.faq-item h4 {
  font-family: var(--font-brand);
  font-size: 9pt;
  color: var(--pine-deep);
  margin-bottom: 0.02in;
}
.faq-item p {
  font-size: 8pt;
  color: var(--ink-soft);
  margin-bottom: 0;
  line-height: 1.32;
}
.cover-media img { object-position: center 42%; }
"""


def build() -> str:
    css = abhs.CSS.replace("QUOTE_BG", abhs.IMG["quote_bg"]) + EXTRA_CSS
    img = abhs.IMG
    tile = abhs.tile
    plan_steps = abhs.plan_steps
    icon_row = abhs.icon_row

    outside_left = f"""  <!-- Tuck-in flap: teacher planning checklist -->
  <div class="panel outside-left wash-sand">
    <div class="kicker">For Teachers</div>
    <h2>Plan Your Visit</h2>
    <p>Bring a class to Building 106 for a hands-on field trip tied to Arizona grade-level standards.</p>

    <div class="fact-grid">
      <div class="fact"><strong>Tue &amp; Thu</strong><span>During the school year</span></div>
      <div class="fact"><strong>3–4 hours</strong><span>Typical field trip</span></div>
      <div class="fact"><strong>20 students</strong><span>Split larger classes</span></div>
      <div class="fact"><strong>1 adult / 10</strong><span>Chaperones required</span></div>
    </div>

    <div class="card">
      <h3>Schools provide</h3>
      <ul class="plain">
        <li>Signed permission slips</li>
        <li>Transportation</li>
        <li>Sack lunch if staying through lunch</li>
        <li>Weather-appropriate clothing</li>
      </ul>
    </div>

    <div class="card">
      <h3>STEAMSPACE provides</h3>
      <ul class="plain">
        <li>All project materials and tools</li>
        <li>Grade-level making, coding, and design</li>
        <li>Optional Apache Cultural Center and Museum time</li>
        <li>Optional Field Trip Prep interest inventory</li>
      </ul>
    </div>

    <div class="tile-grid" style="grid-template-columns: 1fr; margin-bottom: 0; margin-top: auto;">
{tile('tile_workshop', 'Making at Building 106', 'FORT APACHE HISTORIC PARK', 'tile--wide')}
    </div>
  </div>"""

    outside_center = f"""  <!-- Back cover: how to book -->
  <div class="panel outside-center wash-sand">
    <div class="kicker">Book a Field Trip</div>
    <h2>Ready for your class?</h2>
    <p>Choose a project, pick a Tuesday or Thursday, and confirm arrival details with our team.</p>

{plan_steps([
        ("Choose a grade-level project", "2nd LEGO Paper Building · 3rd Paper Circuits · 4th Laser-Cut Boxes · 5th micro:bit Games · 6th Puzzle Design"),
        ("Schedule your trip", "Check open dates and send the Field Trip Interest Form."),
        ("Confirm with our team", "Finalize timing, museum visit options, and arrival."),
    ])}

    <div class="url-line">{SITE_URL}</div>

    <div class="cta-box">
      <h3>Contact STEAMSPACE</h3>
      <p style="font-weight: 700; margin-bottom: 0.06in;">steamspace@wmabhs.org</p>
      <p>Call or text<br>928-299-0027<br>928-221-1934</p>
      <p style="margin-top: 0.07in; margin-bottom: 0;">Building 106<br>Fort Apache Historic Park</p>
    </div>

    <img class="logo-footer" src="{LOGO_CLEAR}" alt="STEAMSPACE at Fort Apache — Hands-on Field Trips">
  </div>"""

    outside_right = f"""  <!-- Front cover -->
  <div class="panel outside-right cover">
    <div class="cover-media">
      <img src="{COVER_HERO}" alt="">
    </div>
    <div class="cover-shade"></div>
    <div class="cover-content">
      <div class="cover-logo-wrap">
        <img class="cover-logo" src="{LOGO_CLEAR}" alt="STEAMSPACE at Fort Apache — Hands-on Field Trips">
      </div>
      <div class="hero-text">2nd through 6th Grade</div>
      <div class="cover-rule"></div>
      <p class="hero-text" style="white-space: normal; max-width: 22ch;">Students build real projects tied to Arizona grade-level standards.</p>
      <div class="cover-url">{SITE_URL}</div>
      <p class="cover-place">Building 106 · Fort Apache Historic Park</p>
    </div>
  </div>"""

    inside_left = f"""  <!-- Inside left: what STEAMSPACE is -->
  <div class="panel inside-left wash-paper">
    <div class="mission">
      <h3>Field Trips with a Purpose</h3>
      <p>At STEAMSPACE, students build hands-on projects tied to their grade-level Arizona standards while being introduced to new experiences and possible lifelong interests — laser cutting and engraving, 3D design and printing, electronic circuits, micro:bit and VEX robotics, and other making at Building 106 on the Fort Apache Historic Park.</p>
    </div>

    <div class="kicker">Choose · Schedule · Confirm</div>
    <h2>Planning a Hands-on Field Trip</h2>

{plan_steps([
        ("Choose a Field Trip Project", "Pick a grade-level project designed for your class."),
        ("Schedule Your Trip", "Trips run Tuesdays and Thursdays. Check the calendar and submit the interest form."),
        ("Contact Us and Confirm", "Finalize timing, museum visit options, and arrival details."),
    ])}

    <div class="card card--sky" style="margin-top: 0.12in;">
      <h3>Before you visit</h3>
      <p style="margin-bottom: 0;">Optional Field Trip Prep — a short interest inventory for students. Helpful if you have time, never required.</p>
    </div>

    <div class="url-line" style="margin-top: auto; margin-bottom: 0;">{SITE_URL}</div>
  </div>"""

    inside_center = f"""  <!-- Inside center: grade-level projects -->
  <div class="panel inside-center wash-sky">
    <div class="kicker">2nd–6th Grade</div>
    <h2>Field Trip Projects</h2>
    <p>Each project is designed for a grade band and tied to Arizona standards. More projects coming soon.</p>

    <div class="tile-grid">
{tile('tile_lego', 'LEGO Paper Building', '2ND GRADE')}
{tile('tile_circuits', 'Paper Circuits', '3RD GRADE')}
{tile('tile_lasercut', 'Laser-Cut Boxes', '4TH GRADE')}
{tile('tile_microbit', 'micro:bit Games', '5TH GRADE')}
{tile('tile_puzzle', 'Puzzle Design', '6TH GRADE')}
      <div class="web-tile">
        <div class="web-label">Book online</div>
        <div class="web-url">{SITE_URL}</div>
      </div>
    </div>

    <div class="tile-grid" style="grid-template-columns: 1fr; margin-bottom: 0.1in;">
{tile('tile_building', 'Building 106 workshop', 'FORT APACHE HISTORIC PARK', 'tile--short')}
    </div>

    <div class="card" style="margin-top: auto; margin-bottom: 0.06in; padding: 0.1in 0.12in;">
      <h3 style="font-size: 10.5pt; margin-bottom: 0.035in;">Why making?</h3>
      <p style="margin-bottom: 0; font-size: 8.5pt; line-height: 1.3;">Hands-on Science, Technology, Engineering, Arts, and Math can spark interests students carry into future classes and careers.</p>
    </div>

{icon_row()}
  </div>"""

    inside_right = f"""  <!-- Inside right: teacher FAQ -->
  <div class="panel inside-right wash-sand">
    <div class="kicker">Teachers</div>
    <h2>Quick Answers</h2>
    <p>What to know before you bring a class.</p>

    <div class="card">
      <div class="faq-item">
        <h4>What grades can attend?</h4>
        <p>Hands-on projects for 2nd–6th grade. 2nd LEGO Paper Building, 3rd Paper Circuits, 4th Laser-Cut Boxes, 5th micro:bit, 6th Puzzle Design.</p>
      </div>
      <div class="faq-item">
        <h4>How long is a typical trip?</h4>
        <p>3–4 hours on Tuesdays and Thursdays during the school year.</p>
      </div>
      <div class="faq-item">
        <h4>How many students can attend?</h4>
        <p>Projects are designed for groups of 20 or fewer. Larger classes can rotate.</p>
      </div>
      <div class="faq-item">
        <h4>Are chaperones required?</h4>
        <p>Yes. We recommend at least one adult per 10 students. Schools provide permission slips, transportation, and supervision.</p>
      </div>
      <div class="faq-item">
        <h4>What should students bring?</h4>
        <p>A signed permission slip, a water bottle, and a sack lunch if staying through lunch. We provide all project materials.</p>
      </div>
      <div class="faq-item">
        <h4>How do I schedule?</h4>
        <p>Go to {SITE_URL}, choose a project, then send the Field Trip Interest Form. We follow up to confirm.</p>
      </div>
    </div>

    <div class="push"></div>

    <div class="quote-band">
      <blockquote>“The best moments usually occur when a person’s body or mind is stretched to its limits in a voluntary effort to accomplish something difficult and worthwhile.”</blockquote>
      <cite>Mihaly Csikszentmihalyi</cite>
    </div>
  </div>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>STEAMSPACE Field Trips — Teacher Brochure</title>
<style>{abhs.font_faces()}</style>
<style>{css}</style>
</head>
<body>

<!-- OUTSIDE PAGE -->
<div class="page">

{outside_left}

{outside_center}

{outside_right}

</div>

<!-- INSIDE PAGE -->
<div class="page">

{inside_left}

{inside_center}

{inside_right}

</div>

</body>
</html>
"""


def main() -> None:
    OUT.write_text(build())
    size_kb = OUT.stat().st_size / 1024
    print(f"Wrote {OUT} ({size_kb:.0f} KB)")

    chrome = "google-chrome"
    for candidate in ("google-chrome", "chromium", "chromium-browser"):
        if subprocess.run(["which", candidate], capture_output=True).returncode == 0:
            chrome = candidate
            break

    before = PDF.stat().st_mtime if PDF.exists() else 0
    try:
        subprocess.run(
            [
                chrome, "--headless", "--disable-gpu", "--no-sandbox",
                "--no-pdf-header-footer",
                f"--print-to-pdf={PDF}",
                OUT.as_uri(),
            ],
            check=True,
            capture_output=True,
            timeout=90,
        )
    except subprocess.TimeoutExpired:
        if not PDF.exists() or PDF.stat().st_mtime <= before:
            raise
        print("Chrome hung after writing PDF; continuing")
    print(f"Wrote {PDF.name} ({PDF.stat().st_size / 1024:.0f} KB)")

    try:
        import pypdfium2 as pdfium
        doc = pdfium.PdfDocument(str(PDF))
        page = doc[0]
        img = page.render(scale=2.5).to_pil()
        img.save(PREVIEW)
        width, height = img.size
        img.crop((round(width * 2 / 3), 0, width, height)).save(COVER)
        print(f"Wrote {PREVIEW.name} and {COVER.name}")
    except Exception as exc:
        print(f"Preview raster skipped ({type(exc).__name__}: {exc})")


if __name__ == "__main__":
    main()
