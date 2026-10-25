"""Draws the 1200x630 social preview image used by the website (docs/assets/og-image.png).

    python assets/make_og_image.py
"""
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent.parent / "docs" / "assets" / "og-image.png"
PAPER, INK, SOFT, BLUE, YELLOW = "#F7F3EA", "#15171B", "#4C4841", "#3D5AFE", "#FFC300"
FONT = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
FONT_REG = "/System/Library/Fonts/Supplemental/Arial.ttf"

img = Image.new("RGB", (1200, 630), PAPER)
d = ImageDraw.Draw(img)

# A sphere of "training data" with one yellow cluster drifting away, like the home page hero.
cx, cy, R, n, golden = 930, 315, 210, 700, math.pi * (3 - math.sqrt(5))
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

kicker = ImageFont.truetype(FONT, 26)
title = ImageFont.truetype(FONT, 62)
sub = ImageFont.truetype(FONT_REG, 30)
d.rectangle((70, 90, 82, 102), fill=BLUE)
d.text((100, 84), "A FREE COURSE", font=kicker, fill=BLUE)
for i, line in enumerate(["Machine", "Unlearning,", "explained", "simply"]):
    d.text((70, 150 + i * 76), line, font=title, fill=INK)
d.text((70, 490), "Teach a trained model to forget,", font=sub, fill=SOFT)
d.text((70, 530), "and prove that it did.", font=sub, fill=SOFT)
d.text((70, 580), "shreyan1.github.io/machine-unlearning-course", font=ImageFont.truetype(FONT_REG, 22), fill=SOFT)
img.save(OUT, optimize=True)
print("wrote", OUT)
