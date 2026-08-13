#!/usr/bin/env python3
"""Generate the self-contained ABHS STEM trifold brochure.

Images from assets/ are inlined as base64 data URIs so index.html can be
handed to a print shop on its own.
"""

import base64
import mimetypes
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
ASSETS = ROOT / "assets"
OUT = ROOT / "index.html"


def data_uri(relative_path: str) -> str:
    path = ASSETS / relative_path
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


IMG = {
    "logo_stem": data_uri("logo_stem_trimmed.png"),
    # Baked onto the wash-sand bottom color so Chromium print doesn't
    # flatten logo transparency into a white rectangle.
    "logo_abhs": data_uri("abhs_logo_footer.png"),
    "together": data_uri("togetherwebuild_white.png"),
    "icon_science": data_uri("icon_science.png"),
    # T and A shipped without the hand-drawn ring the other three have;
    # these variants have a ring lifted from icon_math.png composited on.
    "icon_technology": data_uri("icon_technology_ringed.png"),
    "icon_engineering": data_uri("icon_engineering.png"),
    "icon_arts": data_uri("icon_arts_ringed.png"),
    "icon_math": data_uri("icon_math.png"),
    # Pre-cropped to the cover panel's aspect, so object-fit trims almost nothing
    # and the full source resolution survives into print.
    "cover": data_uri("photos/cover-floorbuild.jpg"),
    "quote_bg": data_uri("photos/quote-bg.jpg"),
    "tile_lego": data_uri("photos/tile-lego.jpg"),
    "tile_circuits": data_uri("photos/tile-circuits.jpg"),
    "tile_lasercut": data_uri("photos/tile-lasercut.jpg"),
    "tile_microbit": data_uri("photos/tile-microbit.jpg"),
    "tile_puzzle": data_uri("photos/tile-puzzle.jpg"),
    "tile_vex": data_uri("photos/tile-vex.jpg"),
    "tile_building": data_uri("photos/tile-building106.jpg"),
    "tile_teamwork": data_uri("photos/tile-teamwork.jpg"),
    "tile_workshop": data_uri("photos/tile-workshop.jpg"),
    "tile_snapcircuits": data_uri("photos/tile-snapcircuits.jpg"),
    "tile_brochurepic": data_uri("photos/tile-brochurepic.jpg"),
    # Official VEX product-line wordmarks, cropped from each style guide's
    # Logo Colors page. Freely available for promotional/educational use.
    "vex_123": data_uri("vex/vex-123.png"),
    "vex_go": data_uri("vex/vex-GO.png"),
    "vex_iq": data_uri("vex/vex-IQ.png"),
    "vex_v5": data_uri("vex/vex-V5.png"),
}


def icon_row(extra_style: str = "") -> str:
    icons = ("icon_science", "icon_technology", "icon_engineering", "icon_arts", "icon_math")
    imgs = "\n".join(
        f'      <img src="{IMG[name]}" alt="">' for name in icons
    )
    return f'    <div class="icon-row"{extra_style}>\n{imgs}\n    </div>'


def font_faces() -> str:
    """Inline the latin subsets so print output never depends on the network."""
    faces = []
    for family, filename, weights in (
        ("Fredoka", "fonts/fredoka-latin.woff2", "400 700"),
        ("Nunito", "fonts/nunito-latin.woff2", "400 800"),
    ):
        faces.append(
            f"@font-face {{ font-family: '{family}'; font-style: normal; "
            f"font-weight: {weights}; font-display: block; "
            f"src: url({data_uri(filename)}) format('woff2'); }}"
        )
    return "\n".join(faces)


CSS = """
/* Design language ported from steamspace.vercel.app */
:root {
  --pine: #1f6b4a;
  --pine-deep: #145239;
  --sky: #dff0fa;
  --sky-deep: #9fd0e8;
  --sand: #f7f1e6;
  --sand-deep: #e8dcc8;
  --sun: #f0b429;
  --sun-soft: #ffe8a3;
  --coral: #e36b4a;
  --teal: #1a8a8a;
  --ink: #1c2a24;
  --ink-soft: #3d5248;
  --paper: #fffdf8;
  --radius: 13px;
  --card-shadow: 0 5px 14px rgba(28, 42, 36, 0.09);
  --hairline: 1px solid rgba(31, 107, 74, 0.14);
  --font-brand: "Fredoka", "Trebuchet MS", sans-serif;
  --font-body: "Nunito", "Segoe UI", sans-serif;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

@page { size: 11in 8.5in; margin: 0; }

body {
  font-family: var(--font-body);
  color: var(--ink);
  background: #fff;
  line-height: 1.42;
}

.page {
  width: 11in;
  height: 8.5in;
  display: flex;
  flex-direction: row;
  overflow: hidden;
  page-break-after: always;
  position: relative;
}
.page:last-child { page-break-after: auto; }

.panel {
  width: 3.6667in;
  height: 8.5in;
  padding: 0.32in 0.3in;
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Layered gradient wash from the site's body background */
.wash-sand {
  background:
    radial-gradient(ellipse 80% 45% at 8% -8%, var(--sky) 0%, transparent 55%),
    radial-gradient(ellipse 70% 40% at 100% 0%, var(--sun-soft) 0%, transparent 50%),
    linear-gradient(180deg, #f4faf7 0%, var(--sand) 45%, #f8f3ea 100%);
}
.wash-sky {
  background:
    radial-gradient(ellipse 75% 40% at 90% -6%, var(--sun-soft) 0%, transparent 55%),
    linear-gradient(180deg, var(--sky) 0%, #eaf6fb 55%, #f4faf7 100%);
}
.wash-paper {
  background:
    radial-gradient(ellipse 70% 38% at 100% -5%, var(--sky) 0%, transparent 58%),
    linear-gradient(180deg, var(--paper) 0%, #f9f6ef 100%);
}

h1, h2, h3, h4 { font-family: var(--font-brand); line-height: 1.12; }
h1 { font-size: 34pt; font-weight: 700; }
h2 {
  font-size: 16.5pt;
  font-weight: 600;
  color: var(--pine-deep);
  margin-bottom: 0.11in;
}
/* Sun accent rule under section heads, echoing the site's section styling */
h2::after {
  content: "";
  display: block;
  width: 0.42in;
  height: 3px;
  background: var(--sun);
  border-radius: 2px;
  margin-top: 0.05in;
}
h3 { font-size: 11.5pt; font-weight: 700; color: var(--pine-deep); margin-bottom: 0.05in; }
p { font-size: 9.5pt; margin-bottom: 0.09in; }

.kicker {
  display: inline-block;
  align-self: flex-start;
  font-family: var(--font-brand);
  font-size: 9pt;
  font-weight: 600;
  background: var(--sun);
  color: var(--ink);
  padding: 0.045in 0.13in;
  border-radius: 999px;
  margin-bottom: 0.11in;
  box-shadow: 0 3px 8px rgba(240, 180, 41, 0.35);
}

ul.plain { list-style: none; font-size: 9.5pt; }
ul.plain li {
  margin-bottom: 0.05in;
  padding-left: 0.14in;
  position: relative;
}
ul.plain li::before {
  content: "\\2022";
  color: var(--teal);
  position: absolute;
  left: 0;
  font-weight: 800;
}

/* Rounded card treatment used throughout the site */
.card {
  background: var(--paper);
  border: var(--hairline);
  border-radius: var(--radius);
  padding: 0.14in 0.15in;
  box-shadow: var(--card-shadow);
  margin-bottom: 0.12in;
}
.card:last-child { margin-bottom: 0; }
.card > p:last-child, .card > ul:last-child { margin-bottom: 0; }
.card--sky { background: rgba(223, 240, 250, 0.75); }

/* Grade chip, from the site's project tiles */
.chip {
  display: inline-block;
  font-family: var(--font-brand);
  font-size: 7.5pt;
  font-weight: 600;
  color: var(--pine);
  background: rgba(31, 107, 74, 0.1);
  padding: 0.015in 0.07in;
  border-radius: 7px;
}

/* ---------- Front cover photo hero (.hero + .hero-shade) ---------- */
.cover { padding: 0; color: #fff; }
.cover-media { position: absolute; inset: 0; }
.cover-media img { width: 100%; height: 100%; object-fit: cover; object-position: center 38%; }
.cover-shade {
  position: absolute;
  inset: 0;
  /* Follows the site's .hero-shade curve: eased through the middle and
     deepening to the same 0.78 base. Carries extra weight only at the very
     top, where the headline sits over a bright window. */
  background:
    linear-gradient(180deg,
      rgba(20, 50, 40, 0.60) 0%,
      rgba(20, 50, 40, 0.34) 24%,
      rgba(20, 50, 40, 0.30) 50%,
      rgba(20, 45, 36, 0.38) 70%,
      rgba(20, 42, 34, 0.58) 88%,
      rgba(20, 40, 32, 0.78) 100%),
    radial-gradient(circle at 80% 20%, rgba(240, 180, 41, 0.25), transparent 40%);
}
.cover-content {
  position: relative;
  z-index: 1;
  height: 100%;
  padding: 0.62in 0.3in 0.34in;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}
.cover h1, .cover h2, .cover h3 { color: #fff; }
.cover h2::after { display: none; }

.logo {
  width: 100%;
  max-height: 0.72in;
  object-fit: contain;
  display: block;
  margin-bottom: 0.16in;
  filter: drop-shadow(0 3px 10px rgba(0, 0, 0, 0.45));
}

.subtitle {
  font-size: 10.5pt;
  font-weight: 700;
  color: var(--sun-soft);
  letter-spacing: 0.05em;
  text-transform: uppercase;
  margin-bottom: 0.08in;
}

.hero-text {
  font-family: var(--font-brand);
  font-size: 11pt;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.95);
  margin: 0.08in 0;
  white-space: nowrap;
}

.cover-rule {
  width: 1.1in;
  height: 3px;
  background: var(--sun);
  border-radius: 2px;
  margin: 0.1in 0 0.14in;
}

/* Auto margins centre the badge in the space below the headline block. */
.together-logo {
  max-height: 2.1in;
  width: auto;
  margin: auto 0;
  /* Lifted off centre so the mark falls across the subject's face. */
  transform: translateY(-1.4in);
  filter: drop-shadow(0 3px 10px rgba(0, 0, 0, 0.55)) drop-shadow(0 0 22px rgba(0, 0, 0, 0.4));
}

.cover-place {
  font-size: 9.5pt;
  color: rgba(255, 255, 255, 0.92);
  margin-bottom: 0;
}

.icon-row { display: flex; gap: 0.06in; justify-content: center; margin: 0.04in 0 0; }
.icon-row img { height: 0.45in; width: auto; }

/* ---------- Photo tiles with gradient caption (.gallery-item) ---------- */
.tile-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.09in;
  margin-bottom: 0.12in;
}
.tile {
  position: relative;
  border-radius: 11px;
  overflow: hidden;
  aspect-ratio: 4 / 3;
  box-shadow: 0 5px 14px rgba(28, 42, 36, 0.13);
}
.tile img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tile-cap {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  padding: 0.16in 0.07in 0.05in;
  background: linear-gradient(
    180deg,
    transparent 0%,
    rgba(20, 82, 57, 0.55) 35%,
    rgba(16, 58, 40, 0.9) 100%
  );
  color: #fff;
}
.tile-title { font-family: var(--font-brand); font-size: 8pt; font-weight: 600; line-height: 1.15; }
.tile-grade { font-size: 6.5pt; font-weight: 700; color: var(--sun-soft); letter-spacing: 0.03em; }

.tile--wide { aspect-ratio: 16 / 8; }
.tile--short { aspect-ratio: 16 / 6.2; }

/* URL companion for the last row of a tile grid — same footprint as a photo tile. */
.web-tile {
  aspect-ratio: 4 / 3;
  border-radius: 11px;
  background: rgba(240, 180, 41, 0.22);
  border: var(--hairline);
  box-shadow: 0 5px 14px rgba(28, 42, 36, 0.08);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.06in;
  padding: 0.08in 0.05in;
  text-align: center;
}
.web-tile .web-label {
  font-family: var(--font-brand);
  font-size: 7.5pt;
  font-weight: 600;
  color: var(--ink-soft);
  letter-spacing: 0.04em;
  text-transform: uppercase;
}
.web-tile .web-url {
  font-family: var(--font-body);
  font-size: 7.5pt;
  font-weight: 400;
  color: var(--pine-deep);
  letter-spacing: 0;
  line-height: 1.15;
  white-space: nowrap;
}

/* ---------- Service cards with colored bullets (.plan-step) ---------- */
.plan-steps { display: flex; flex-direction: column; gap: 0.075in; }
.plan-step {
  position: relative;
  overflow: hidden;
  background: var(--paper);
  border: var(--hairline);
  border-radius: 11px;
  padding: 0.075in 0.1in 0.075in 0.2in;
  box-shadow: 0 3px 9px rgba(28, 42, 36, 0.06);
  display: flex;
  align-items: flex-start;
  gap: 0.08in;
}
.plan-step::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 5px;
  background: var(--accent, var(--pine));
}
.plan-step:nth-child(1) { --accent: var(--teal); }
.plan-step:nth-child(2) { --accent: var(--sun); }
.plan-step:nth-child(3) { --accent: var(--coral); }
.plan-step:nth-child(4) { --accent: var(--pine); }
.plan-step .bullet {
  /* Border-drawn circle: Chromium print won't stretch this like a flex box. */
  box-sizing: border-box;
  width: 0;
  height: 0;
  margin-top: 0.045in;
  border: 0.033in solid var(--accent, var(--pine));
  border-radius: 50%;
  background: transparent;
  flex: none;
}
.plan-step .step-title { font-family: var(--font-brand); font-size: 9.5pt; font-weight: 600; }
.plan-step .step-note { font-size: 8pt; color: var(--ink-soft); }

/* ---------- Quote band (.quote-band) ---------- */
.quote-band {
  background: linear-gradient(135deg, var(--pine) 0%, var(--pine-deep) 100%);
  color: #fff;
  border-radius: var(--radius);
  padding: 0.15in 0.16in;
  text-align: center;
  margin-bottom: 0.12in;
  box-shadow: 0 8px 20px rgba(20, 82, 57, 0.28);
}
.quote-band blockquote {
  font-family: var(--font-brand);
  font-size: 9.5pt;
  font-weight: 450;
  line-height: 1.3;
}
.quote-band cite {
  display: block;
  margin-top: 0.06in;
  font-style: normal;
  font-size: 7.5pt;
  font-weight: 700;
  opacity: 0.9;
}

/* ---------- Robotics pathway ---------- */
.pathway { display: flex; flex-direction: column; gap: 0.06in; margin: 0.02in 0 0; }
.pathway-row { display: flex; align-items: center; gap: 0.09in; font-size: 9pt; }
.pathway-row .kit { color: var(--ink-soft); }
.pathway-row .chip { min-width: 0.42in; text-align: center; }
.pathway-kits {
  display: flex;
  align-items: center;
  flex-wrap: nowrap;
  gap: 0.04in 0.06in;
  min-width: 0;
  flex: 1;
}
.pathway-kits img {
  height: 0.12in;
  width: auto;
  max-width: 0.72in;
  object-fit: contain;
  display: block;
  flex-shrink: 1;
}
.pathway-kits .amp {
  font-size: 8pt;
  font-weight: 700;
  color: var(--ink-soft);
  flex-shrink: 0;
}

/* Offering rows: centered pills, no bullets */
.offer-list { display: flex; flex-direction: column; gap: 0.05in; }
.offer {
  background: rgba(255, 255, 255, 0.78);
  border: var(--hairline);
  border-radius: 9px;
  padding: 0.05in 0.08in;
  font-size: 8.5pt;
  font-weight: 700;
  color: var(--ink);
  line-height: 1.22;
  text-align: center;
}

.tag { 
  display: inline-block;
  font-family: var(--font-brand);
  font-size: 8.5pt;
  font-weight: 600;
  background: var(--pine);
  color: #fff;
  padding: 0.035in 0.1in;
  border-radius: 7px;
  margin: 0.02in;
}
.tag-row { margin-top: auto; text-align: center; padding-top: 0.12in; }

.cta-box {
  background: linear-gradient(135deg, var(--pine) 0%, var(--pine-deep) 100%);
  color: #fff;
  border-radius: var(--radius);
  padding: 0.16in;
  text-align: center;
  box-shadow: 0 8px 20px rgba(20, 82, 57, 0.28);
}
.cta-box h3 { color: var(--sun-soft); margin-bottom: 0.07in; font-size: 11.5pt; }
.cta-box h3::after { display: none; }
.cta-box p { font-size: 9.5pt; margin-bottom: 0; }
.push { margin-top: auto; }

.skills-block {
  background: rgba(255, 255, 255, 0.82);
  border: var(--hairline);
  border-radius: 11px;
  padding: 0.11in 0.12in;
  margin-bottom: 0.09in;
  box-shadow: 0 3px 10px rgba(28, 42, 36, 0.06);
}
.skills-block h4 {
  font-family: var(--font-brand);
  font-size: 9.5pt;
  color: var(--coral);
  margin-bottom: 0.035in;
}
.skills-block p { font-size: 8pt; margin-bottom: 0; }

/* Opens the inside spread, so it stays light against the pine section heads
   rather than competing with them. The sun edge marks it as the thesis. */
.mission {
  background: rgba(255, 255, 255, 0.86);
  border: var(--hairline);
  border-left: 4px solid var(--sun);
  border-radius: 11px;
  padding: 0.14in 0.15in;
  box-shadow: 0 3px 10px rgba(28, 42, 36, 0.06);
  margin-bottom: 0.15in;
}
.mission h3 { font-size: 11pt; color: var(--pine); margin-bottom: 0.05in; }
.mission p { font-size: 9pt; line-height: 1.4; margin-bottom: 0; }

.abhs-footer { margin-top: auto; text-align: center; padding-top: 0.12in; }
.abhs-footer img { max-height: 0.8in; width: auto; display: inline-block; }

.web-line {
  font-family: var(--font-brand);
  font-size: 9.5pt;
  font-weight: 600;
  color: var(--pine-deep);
  text-align: center;
  background: rgba(240, 180, 41, 0.18);
  border-radius: 9px;
  padding: 0.06in;
  margin-bottom: 0.12in;
}

@media print {
  body { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
"""


def plan_steps(items: list[tuple[str, str]]) -> str:
    """Service cards with a colored accent bar and matching bullet.

    Each item is a (title, note) pair; an empty note renders the title alone.
    """
    cards = []
    for title, note in items:
        note_markup = f'\n          <div class="step-note">{note}</div>' if note else ""
        cards.append(
            f"""      <div class="plan-step">
        <div class="bullet" aria-hidden="true"></div>
        <div>
          <div class="step-title">{title}</div>{note_markup}
        </div>
      </div>"""
        )
    return '    <div class="plan-steps">\n' + "\n".join(cards) + "\n    </div>"


def tile(img_key: str, title: str, grade: str, extra_class: str = "") -> str:
    cls = f"tile {extra_class}".strip()
    return f"""      <div class="{cls}">
        <img src="{IMG[img_key]}" alt="{title}">
        <div class="tile-cap">
          <div class="tile-title">{title}</div>
          <div class="tile-grade">{grade}</div>
        </div>
      </div>"""


def build() -> str:
    css = CSS.replace("QUOTE_BG", IMG["quote_bg"])

    # Letter-fold outside: left = tuck-in flap, center = back cover,
    # right = front cover. Fold right over first, then left over top.
    outside_left = f"""  <!-- Tuck-in flap (left when flat; folds inside first) -->
  <div class="panel outside-left wash-sand">
    <div class="kicker">Where We Serve</div>
    <h2>Schools We Serve</h2>

    <div class="card">
      <ul class="plain">
        <li>Cradleboard Elementary</li>
        <li>Seven Mile Elementary</li>
        <li>Whiteriver Elementary</li>
        <li>John F. Kennedy School</li>
        <li>Canyon Day Junior High</li>
        <li>Theodore Roosevelt School</li>
        <li>Alchesay High School</li>
        <li>Dischii'bikoh Community Schools</li>
        <li>McNary School District</li>
      </ul>
    </div>

    <div class="card">
      <h3>Program Offerings</h3>
      <div class="offer-list">
        <div class="offer">Individual Behavioral Health Services</div>
        <div class="offer">Child Family Team Interventions</div>
        <div class="offer">Social Emotional Learning small groups</div>
        <div class="offer">Full Classroom STEM Projects</div>
        <div class="offer">Robotics and other STEM clubs before/during/after school</div>
        <div class="offer">Summer Camp STEM activities</div>
      </div>
    </div>

    <div class="tile-grid" style="grid-template-columns: 1fr; margin-bottom: 0;">
{tile('tile_brochurepic', 'Hands-on STEM in progress', 'MAKING & DISCOVERING', 'tile--wide')}
    </div>
  </div>"""

    outside_center = f"""  <!-- Back cover (center when flat; stays put when folded) -->
  <div class="panel outside-center wash-sand">
    <div class="kicker">Also at Building 106</div>
    <h2>STEAMSPACE Field Trips</h2>
    <p>Elementary and Middle School classes build real projects tied to Arizona grade-level standards at Fort Apache Historic Park.</p>

    <div class="tile-grid">
{tile('tile_lego', 'LEGO Paper Building', '2ND GRADE')}
{tile('tile_circuits', 'Paper Circuits', '3RD GRADE')}
{tile('tile_lasercut', 'Laser-Cut Boxes', '4TH GRADE')}
{tile('tile_microbit', 'micro:bit Games', '5TH GRADE')}
{tile('tile_puzzle', 'Puzzle Design', '6TH GRADE')}
      <div class="web-tile">
        <div class="web-label">Online</div>
        <div class="web-url">steamspace.vercel.app</div>
      </div>
    </div>

    <div class="cta-box">
      <h3>Enroll in ABHS Services<br>STEM Program</h3>
      <p style="font-weight: 700;">Apache Behavioral Health Services<br>928-338-4811<br>249 W Ponderosa Street<br>Whiteriver, Arizona 85941</p>
    </div>

    <div class="abhs-footer">
      <img src="{IMG['logo_abhs']}" alt="Apache Behavioral Health Services">
    </div>
  </div>"""

    outside_right = f"""  <!-- Front cover (right when flat; folds over last) -->
  <div class="panel outside-right cover">
    <div class="cover-media">
      <img src="{IMG['cover']}" alt="">
    </div>
    <div class="cover-shade"></div>
    <div class="cover-content">
      <div class="subtitle">Apache Behavioral Health Services</div>
      <h1 style="font-size: 36pt; margin: 0.04in 0; white-space: nowrap; text-shadow: 0 6px 22px rgba(0,0,0,.4);">ABHS STEM</h1>
      <div class="hero-text">Classroom · Clubs · Camps · Competitions</div>
      <div class="cover-rule"></div>
      <img class="together-logo" src="{IMG['together']}" alt="Together We Build">
      <p class="cover-place">White Mountain Apache Tribe</p>
    </div>
  </div>"""

    inside_left = f"""  <!-- Inside left -->
  <div class="panel inside-left wash-paper">
    <div class="mission">
      <h3>Our Mission</h3>
      <p>Our mission is to provide hope and future opportunities for every child living on the White Mountain Apache Reservation through the development of personal behavioral health skills and exposure to innovative hands-on Science, Technology, Engineering, Art, and Math activities.</p>
    </div>

    <div class="kicker">Contact &amp; Partnership</div>
    <h2>ABHS STEM Services</h2>
    <p><strong>Hands-on STEM and behavioral health education</strong> for school-age children on the White Mountain Apache Reservation.</p>

{plan_steps([
        ("School classroom STEM projects", ""),
        ("Social Emotional Learning and Dialectical Behavior Therapy — behavioral health supports", ""),
        ("Robotics &amp; coding clubs", ""),
        ("Competitions, camps, and workshops", ""),
    ])}

    <div class="card card--sky" style="margin-top: 0.12in;">
      <h3>Get in touch</h3>
      <p style="margin-bottom: 0;"><strong>ABHS STEM</strong><br><strong>stem@wmabhs.org</strong><br><strong>928-933-2957</strong></p>
    </div>
  </div>"""

    inside_center = f"""  <!-- Inside center -->
  <div class="panel inside-center wash-sky">
    <div class="kicker">Learning in Action</div>
    <h2>STEM Projects &amp; Robotics</h2>
    <p>Grade-level projects aligned with educational standards—using everyday materials to 3D printers and laser engraving.</p>

    <div class="tile-grid" style="grid-template-columns: 1fr; margin-bottom: 0.08in;">
{tile('tile_vex', 'VEX robotics build sessions', 'CLUBS &amp; COMPETITIONS', 'tile--short')}
    </div>

    <div class="card">
      <h3>Robotics Pathway</h3>
      <div class="pathway">
        <div class="pathway-row">
          <span class="chip">K–2</span>
          <span class="pathway-kits"><img src="{IMG['vex_123']}" alt="VEX 123"></span>
        </div>
        <div class="pathway-row">
          <span class="chip">4–5</span>
          <span class="pathway-kits"><img src="{IMG['vex_go']}" alt="VEX GO"><span class="amp">&amp;</span><img src="{IMG['vex_iq']}" alt="VEX IQ"></span>
        </div>
        <div class="pathway-row">
          <span class="chip">6–8</span>
          <span class="pathway-kits"><img src="{IMG['vex_iq']}" alt="VEX IQ"><span class="amp">&amp;</span><img src="{IMG['vex_v5']}" alt="VEX V5"></span>
        </div>
        <div class="pathway-row">
          <span class="chip">9–12</span>
          <span class="pathway-kits"><img src="{IMG['vex_v5']}" alt="VEX V5"></span>
        </div>
      </div>
    </div>

    <div class="card" style="margin-bottom: 0.08in;">
      <h3>STEM Events</h3>
      <ul class="plain" style="font-size: 9pt;">
        <li style="margin-bottom: 0.035in;">Local robotics tournaments</li>
        <li style="margin-bottom: 0.035in;">State and national competitions</li>
        <li style="margin-bottom: 0.035in;">Science expos</li>
        <li style="margin-bottom: 0.035in;">Summer camps</li>
        <li style="margin-bottom: 0;">Girl Power trips &amp; workshops</li>
      </ul>
    </div>

    <div class="card" style="margin-top: auto; margin-bottom: 0.06in; padding: 0.1in 0.12in;">
      <h3 style="font-size: 10.5pt; margin-bottom: 0.035in;">Why STEM?</h3>
      <p style="margin-bottom: 0; font-size: 8.5pt; line-height: 1.3;">Science, Technology, Engineering, Arts, Math opportunities can prepare students for future career opportunities.</p>
    </div>

{icon_row()}
  </div>"""

    inside_right = f"""  <!-- Inside right -->
  <div class="panel inside-right wash-sand">
    <div class="kicker">Whole-Child Support</div>
    <h2>Social &amp; Emotional Learning</h2>
    <p>Research-based SEL curriculum delivered through the STEM Program.</p>

    <div class="skills-block">
      <h4>K–5 SEL Skills</h4>
      <p style="font-size: 8pt; font-weight: 700; color: var(--ink); margin-bottom: 0.03in;">Social Decision Making and Problem Solving</p>
      <p>Self-awareness · Self-regulation · Social awareness · Relationship management · Responsible decision making · Critical thinking · Problem solving · Creativity &amp; innovation · Communication &amp; teamwork</p>
    </div>

    <div class="skills-block">
      <h4>5–12 DBT Skills</h4>
      <p style="font-size: 8pt; font-weight: 700; color: var(--ink); margin-bottom: 0.03in;">Dialectical Behavior Therapy Skills</p>
      <p>Mindfulness · Distress tolerance · Emotion regulation · Interpersonal effectiveness. Based on the <em>DBT for Emotional Problem Solving for Adolescents</em> curriculum.</p>
    </div>

    <div class="tile-grid" style="grid-template-columns: 1fr; margin: 0.02in 0 0.12in;">
{tile('tile_teamwork', 'Building together in Robotics &amp; Code Club', 'TEAMWORK IN PRACTICE', 'tile--wide')}
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
<title>ABHS STEM Program — Trifold Brochure</title>
<style>{font_faces()}</style>
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

    subprocess.run(
        [
            "chromium", "--headless", "--disable-gpu", "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={ROOT / 'brochure.pdf'}",
            OUT.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    print(f"Wrote brochure.pdf ({(ROOT / 'brochure.pdf').stat().st_size / 1024:.0f} KB)")

    subprocess.run(
        [
            "chromium", "--headless", "--disable-gpu", "--no-sandbox",
            "--window-size=1056,1632",
            f"--screenshot={ROOT / 'brochure-preview.png'}",
            OUT.as_uri(),
        ],
        check=True,
        capture_output=True,
    )
    print("Wrote brochure-preview.png")


if __name__ == "__main__":
    main()
