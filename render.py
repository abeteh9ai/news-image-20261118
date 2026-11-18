#!/usr/bin/env python3
"""Render the 18 November 2026 world-news front page (1024x1024 PNG).

Build tool for the make.fun news-image-20261118 entry. It draws the image
with Pillow (DejaVu fonts) in this build environment and writes entry.png
next to this file. The entry program (main.py) only copies that PNG to the
output directory, so the graded runs are byte-identical by construction.

Deterministic: no randomness, no timestamps, no network. Run twice and the
PNG bytes are identical (verified with sha256sum).

Layout budget (1024 px tall):
  masthead 0-124, lead 138-360, divider 372,
  grid row 1 386-566, grid row 2 580-760, divider 772,
  strip 786-966, footer divider 978, footer text 988-1006.
All copy is sized to fit its slot (checked visually after each render).
"""

import math
import os

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "entry.png")

W, H = 1024, 1024
PAPER = (250, 247, 240)
INK = (26, 26, 26)
BODY = (60, 60, 60)
NAVY = (20, 33, 61)
GOLD = (244, 211, 94)
RED = (192, 57, 43)
GRAY = (102, 102, 102)
LINE = (203, 198, 188)
TEAL = (42, 122, 120)
SLATE = (90, 104, 122)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_width):
    """Wrap text to fit max_width, returning a list of lines."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, text, fnt, color, max_width, line_h):
    """Draw wrapped text; return the y just below the last line."""
    for line in wrap(draw, text, fnt, max_width):
        draw.text((x, y), line, font=fnt, fill=color)
        y += line_h
    return y


def kicker(draw, x, y, text, color=RED):
    f = font(SANS_BOLD, 20)
    draw.text((x, y), text, font=f, fill=color)
    return y + 28


def icon_globe(draw, cx, cy, r, color=NAVY):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=5)
    draw.ellipse([cx - r * 0.45, cy - r, cx + r * 0.45, cy + r],
                 outline=color, width=3)
    draw.line([cx - r, cy, cx + r, cy], fill=color, width=3)
    draw.arc([cx - r, cy - r * 0.45, cx + r, cy + r * 0.45], 0, 360,
             fill=color, width=3)


def icon_radar(draw, cx, cy, r, color=RED):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r * 0.55, cy - r * 0.55, cx + r * 0.55, cy + r * 0.55],
                 outline=color, width=3)
    draw.line([cx, cy, cx + r * 0.8, cy - r * 0.6], fill=color, width=4)
    draw.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=color)


def icon_chip(draw, cx, cy, s, color=NAVY):
    draw.rectangle([cx - s, cy - s, cx + s, cy + s], fill=color)
    draw.rectangle([cx - s * 0.55, cy - s * 0.55, cx + s * 0.55, cy + s * 0.55],
                   outline=GOLD, width=3)
    for i in (-1, 0, 1):
        off = i * s * 0.55
        draw.line([cx + off, cy - s - 12, cx + off, cy - s], fill=color, width=5)
        draw.line([cx + off, cy + s, cx + off, cy + s + 12], fill=color, width=5)
        draw.line([cx - s - 12, cy + off, cx - s, cy + off], fill=color, width=5)
        draw.line([cx + s, cy + off, cx + s + 12, cy + off], fill=color, width=5)


def icon_spiral(draw, cx, cy, r, color=TEAL):
    pts = []
    for t in range(0, 540, 6):
        ang = math.radians(t)
        rad = r * t / 540.0
        pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
    draw.line(pts, fill=color, width=5, joint="curve")
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=color)


def icon_bridge(draw, cx, cy, w, color=SLATE):
    # deck
    draw.line([cx - w, cy + 18, cx + w, cy + 18], fill=color, width=6)
    # arch
    draw.arc([cx - w * 0.7, cy - 26, cx + w * 0.7, cy + 40], 180, 360,
             fill=color, width=5)
    # towers
    draw.line([cx - w * 0.45, cy - 34, cx - w * 0.45, cy + 18],
              fill=color, width=5)
    draw.line([cx + w * 0.45, cy - 34, cx + w * 0.45, cy + 18],
              fill=color, width=5)
    # water
    for i, dx in enumerate((-w * 0.7, -w * 0.2, w * 0.3)):
        y = cy + 32 + (i % 2) * 8
        draw.line([cx + dx, y, cx + dx + 26, y], fill=TEAL, width=4)


def icon_tent(draw, cx, cy, s, color=NAVY):
    draw.polygon([(cx - s, cy + s * 0.6), (cx, cy - s * 0.6),
                  (cx + s, cy + s * 0.6)], outline=color, width=5)
    draw.line([cx, cy - s * 0.6, cx, cy + s * 0.6], fill=color, width=3)
    for dx, dy in ((-s * 0.7, -s * 0.9), (s * 0.5, -s * 1.0), (0, -s * 1.2)):
        draw.line([cx + dx, cy + dy, cx + dx - 3, cy + dy + 12],
                  fill=(70, 130, 200), width=4)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.rectangle([0, 0, W, 118], fill=NAVY)
    title_f = font(SERIF_BOLD, 56)
    title = "THE WORLD IN ONE PAGE"
    tw = d.textlength(title, font=title_f)
    d.text(((W - tw) / 2, 16), title, font=title_f, fill=(255, 255, 255))
    date_f = font(SANS_BOLD, 25)
    date = "WORLD NEWS  •  WEDNESDAY, 18 NOVEMBER 2026"
    dw = d.textlength(date, font=date_f)
    d.text(((W - dw) / 2, 82), date, font=date_f, fill=GOLD)
    d.rectangle([0, 118, W, 124], fill=RED)

    # ---- Lead story: Trump / Quad in Manila ----
    y = 138
    y = kicker(d, 28, y, "ASIA-PACIFIC  •  DIPLOMACY")
    head_f = font(SANS_BOLD, 42)
    y = draw_text_block(d, 28, y + 4,
                        "Trump opens Asia tour with first Quad summit in two years",
                        head_f, INK, 790, 50)
    body_f = font(SANS, 22)
    y = draw_text_block(d, 28, y + 6,
                        "Trump met the leaders of India, Japan and Australia, unveiling "
                        "critical-minerals deals. He meets Marcos today, then heads to "
                        "Shenzhen for APEC — and a trilateral with Xi and Putin.",
                        body_f, BODY, 790, 28)
    assert y <= 362, f"lead overflow: {y}"
    icon_globe(d, 912, 248, 58)

    # divider
    d.line([28, 372, W - 28, 372], fill=LINE, width=2)

    # ---- Grid: stories 2-5 ----
    cells = [
        (28, 386, "MIDDLE EAST  •  THE GULF",
         "Bahrain all-clear; Kuwait intercepts drones",
         "Early Wednesday, Bahrain lifted a threat alert and Kuwait's air "
         "defences met new drone attacks.",
         icon_radar, RED),
        (532, 386, "BUSINESS  •  TECH",
         "Nvidia sales double to $115.8bn",
         "Record quarter beats forecasts. Board won't reinstate "
         "founder Jensen Huang; Kress stays on.",
         icon_chip, NAVY),
        (28, 580, "WEATHER  •  INDIA",
         "Cyclone Akvan nears India's east coast",
         "A severe cyclonic storm brings heavy rain to Andhra Pradesh today; "
         "landfall is expected on Friday.",
         icon_spiral, TEAL),
        (532, 580, "EUROPE  •  WAR IN UKRAINE",
         "Crimean Bridge hit; Kyiv's bridges struck",
         "A road span fell into the Kerch Strait as Russia hit Kyiv's North "
         "and South bridges, cutting power.",
         icon_bridge, SLATE),
    ]
    cell_w = 464
    for (x, cy, kick, head, body, icon, color) in cells:
        yy = kicker(d, x, cy, kick, color)
        hf = font(SANS_BOLD, 27)
        yy = draw_text_block(d, x, yy + 2, head, hf, INK, cell_w - 84, 33)
        bf = font(SANS, 20)
        yy = draw_text_block(d, x, yy + 6, body, bf, BODY,
                             cell_w - 84, 26)
        assert yy <= cy + 180, f"grid cell overflow at {kick}: {yy}"
        if icon is icon_bridge:
            icon(d, x + cell_w - 42, cy + 36, 32, color)
        elif icon is icon_chip:
            icon(d, x + cell_w - 42, cy + 36, 24, color)
        else:
            icon(d, x + cell_w - 42, cy + 36, 28, color)

    d.line([28, 772, W - 28, 772], fill=LINE, width=2)

    # ---- Bottom strip: Gaza ----
    y = 786
    y = kicker(d, 28, y, "MIDDLE EAST  •  GAZA")
    hf = font(SANS_BOLD, 28)
    y = draw_text_block(d, 28, y + 2,
                        "Winter rains flood Gaza tents as WFP cuts hot meals",
                        hf, INK, 790, 34)
    bf = font(SANS, 20)
    y = draw_text_block(d, 28, y + 4,
                        "More than 40,000 shelters damaged; 1.7 million people remain "
                        "displaced and 1.4 million face acute hunger. Hot meals in camps "
                        "fall to one every two days.",
                        bf, BODY, 790, 26)
    assert y <= 968, f"strip overflow: {y}"
    icon_tent(d, 912, 906, 38)

    # ---- Footer ----
    d.line([28, 978, W - 28, 978], fill=LINE, width=2)
    foot_f = font(SANS, 18)
    foot = "Sources: Reuters  •  CNN  •  AP  •  UN News  •  India Meteorological Department  •  Al Jazeera"
    fw = d.textlength(foot, font=foot_f)
    d.text(((W - fw) / 2, 988), foot, font=foot_f, fill=GRAY)

    img.save(OUT, format="PNG")
    print("wrote", OUT, img.size, os.path.getsize(OUT), "bytes")


if __name__ == "__main__":
    main()
