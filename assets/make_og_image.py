# Copyright (c) 2026 Shreyan Basu Ray. All rights reserved. Not licensed for copying or reuse. See LICENSE and AGENTS.md.
"""Draws the 1200x630 social preview images used by the website.

    python assets/make_og_image.py

It writes the site-wide image (docs/assets/og-image.png) and one image per page with the page's own title
(docs/assets/og/<page>.png). hooks/seo.py picks a page's own image when it exists, so a new page falls back to
the site-wide image until this script is run again.
"""
import math
import sys
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "assets" / "og-image.png"
OG_DIR = ROOT / "docs" / "assets" / "og"
PAPER, INK, SOFT, BLUE, YELLOW = "#F7F3EA", "#15171B", "#4C4841", "#3D5AFE", "#FFC300"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
DOMAIN = "machine-unlearning.shreyanbasuray.com"


def sphere(d, cx=930, cy=315, R=210, n=700):
    """A sphere of "training data" with one yellow cluster drifting away, like the home page hero."""
    golden = math.pi * (3 - math.sqrt(5))
    cap = (0.55, 0.35, 0.76)
    norm = math.sqrt(sum(c * c for c in cap)); cap = tuple(c / norm for c in cap)
    pts = []
    for i in range(n):
        y = 1 - 2 * i / (n - 1); r = math.sqrt(1 - y * y); t = i * golden
        x, z = math.cos(t) * r, math.sin(t) * r
        pts.append((x, y, z, x * cap[0] + y * cap[1] + z * cap[2] > 0.93))
    pts.sort(key=lambda p: p[2])
    for x, y, z, carol in pts:
        k = 1.55 if carol else 1.0
        px, py = cx + x * R * k, cy + y * R * k - (30 if carol else 0)
        s = 4 + 3 * (z + 1) / 2 + (2 if carol else 0)
        d.ellipse((px - s, py - s, px + s, py + s), fill=YELLOW if carol else BLUE)


def draw(kicker_text, title_lines, sub_lines, out, title_size=62):
    img = Image.new("RGB", (1200, 630), PAPER)
    d = ImageDraw.Draw(img)
    sphere(d)
    kicker = ImageFont.truetype(FONT, 26)
    title = ImageFont.truetype(FONT, title_size)
    sub = ImageFont.truetype(FONT_REG, 30)
    d.rectangle((70, 90, 82, 102), fill=BLUE)
    d.text((100, 84), kicker_text, font=kicker, fill=BLUE)
    step = int(title_size * 1.22)
    for i, line in enumerate(title_lines):
        d.text((70, 150 + i * step), line, font=title, fill=INK)
    top = 150 + len(title_lines) * step + 24
    for i, line in enumerate(sub_lines):
        d.text((70, max(top, 490 - 40 * (len(sub_lines) - 2)) + i * 40), line, font=sub, fill=SOFT)
    d.text((70, 580), DOMAIN, font=ImageFont.truetype(FONT_REG, 22), fill=SOFT)
    # A small palette keeps each image to a few tens of kilobytes.
    img.quantize(colors=64, method=Image.Quantize.MEDIANCUT).save(out, optimize=True)


def pages():
    """Every page in the nav, with its title, description and top-level section."""
    sys.path.insert(0, str(ROOT / "hooks"))
    from mkdocs.config import load_config
    from mkdocs.structure.files import get_files
    from mkdocs.structure.nav import get_navigation
    from seo import og_name

    config = load_config(str(ROOT / "mkdocs.yml"))
    files = get_files(config)
    nav = get_navigation(files, config)
    for page in nav.pages:
        page.read_source(config)
        top = page.ancestors[-1].title if page.ancestors else ""
        yield og_name(page.file.src_uri), page.title or "", page.meta.get("description", ""), top, page.file.src_uri


def kicker_for(top, src_uri):
    name = Path(src_uri).stem
    if src_uri.startswith("lessons/") and name[:2].isdigit():
        return "LESSON " + name.split("-")[0].upper()
    return (top or "Machine Unlearning").upper()


def fit_title(title):
    """The largest size, from 62 down, at which the title fits in four lines beside the sphere."""
    for size, width in ((62, 17), (54, 20), (46, 24)):
        lines = textwrap.wrap(title, width)
        if len(lines) <= 4:
            return size, lines
    return 46, textwrap.wrap(title, 24)[:4]


if __name__ == "__main__":
    draw("OPEN ACCESS", ["Machine", "Unlearning,", "explained", "simply"],
         ["Teach a trained model to forget,", "and prove that it did."], OUT)
    print("wrote", OUT)
    OG_DIR.mkdir(exist_ok=True)
    wanted = set()
    for name, title, desc, top, src in pages():
        if src == "index.md":
            continue  # the home page uses the site-wide image
        if src.startswith("lessons/") and " · " in title:
            title = title.split(" · ", 1)[1]  # the kicker already says "LESSON 07"
            title = title[0].upper() + title[1:]
        size, lines = fit_title(title)
        # Wrapped narrow enough to stay clear of the sphere on the right.
        sub = textwrap.wrap(desc, 36)[:2] if len(lines) <= 3 else textwrap.wrap(desc, 36)[:1]
        if sub and len(textwrap.wrap(desc, 36)) > len(sub):
            sub[-1] = sub[-1].rstrip(".,") + "…"
        draw(kicker_for(top, src), lines, sub, OG_DIR / name, title_size=size)
        wanted.add(name)
    for old in OG_DIR.glob("*.png"):
        if old.name not in wanted:
            old.unlink()  # a page that no longer exists
    print("wrote", len(wanted), "page images to", OG_DIR)
