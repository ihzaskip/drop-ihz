#!/usr/bin/env python3
"""Draws the phone page icons in public/: Pulo, a small green hill with a sprout, on a dark tile.

  icon-192.png          rounded dark tile, transparent corners (purpose "any")
  icon-512.png          full-bleed dark, Pulo inside the 40 %-radius circle every mask keeps (purpose "maskable")
  apple-touch-icon.png  180 px, full-bleed square (iOS rounds the corners itself)

The shapes are the same as public/pulo-*.svg. Run: python make_icons.py   (needs Pillow)
"""
from pathlib import Path

from PIL import Image, ImageDraw

OUT = Path(__file__).resolve().parent / "public"
TILE = (0x10, 0x24, 0x1C, 255)
GREEN = (0x1D, 0x9E, 0x75, 255)
DEEP = (0x0F, 0x6E, 0x56, 255)
LEAF = (0x5D, 0xCA, 0xA5, 255)
INK = (0x10, 0x24, 0x1C, 255)
SS = 4  # supersampling


def bez(p0, p1, p2, p3, n=40):
    out = []
    for i in range(n + 1):
        t = i / n
        a, b, c, d = (1 - t) ** 3, 3 * (1 - t) ** 2 * t, 3 * (1 - t) * t * t, t ** 3
        out.append((a * p0[0] + b * p1[0] + c * p2[0] + d * p3[0], a * p0[1] + b * p1[1] + c * p2[1] + d * p3[1]))
    return out


# Pulo in its own units: ground at y = 0, sprout tip near y = -192, x from -90 to 90.
BODY = bez((-90, 0), (-90, -70), (-50, -118), (0, -118)) + bez((0, -118), (50, -118), (90, -70), (90, 0))
STEM = bez((0, -116), (-3, -134), (4, -148), (2, -164), 12)
LEFT = bez((1, -158), (-20, -182), (-52, -178), (-60, -158)) + bez((-60, -158), (-40, -144), (-15, -144), (1, -158))
RIGHT = bez((2, -162), (22, -192), (56, -192), (66, -170)) + bez((66, -170), (46, -154), (18, -150), (2, -162))


def draw_pulo(img, cx, base, scale):
    d = ImageDraw.Draw(img)
    f = lambda pts: [(cx + x * scale, base + y * scale) for x, y in pts]
    d.ellipse([cx - 96 * scale, base - 9 * scale, cx + 96 * scale, base + 11 * scale], fill=DEEP)
    d.polygon(f(BODY), fill=GREEN)
    d.line(f(STEM), fill=DEEP, width=round(8 * scale), joint="curve")
    for leaf in (LEFT, RIGHT):
        d.polygon(f(leaf), fill=LEAF)
        d.line(f(leaf + leaf[:1]), fill=DEEP, width=round(4 * scale), joint="curve")
    for ex in (-28, 28):
        r = 8 * scale
        d.ellipse([cx + ex * scale - r, base - 58 * scale - r, cx + ex * scale + r, base - 58 * scale + r], fill=INK)


def icon(size, content, rounded):
    big = size * SS
    img = Image.new("RGBA", (big, big), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    if rounded:
        d.rounded_rectangle([0, 0, big - 1, big - 1], radius=round(big * 0.22), fill=TILE)
    else:
        d.rectangle([0, 0, big, big], fill=TILE)
    scale = content * big / 200  # Pulo is about 200 units tall with its shadow
    draw_pulo(img, big / 2, big / 2 + 98 * scale, scale)
    return img.resize((size, size), Image.LANCZOS)


def main() -> None:
    icon(192, 0.66, True).save(OUT / "icon-192.png", optimize=True)
    icon(512, 0.56, False).convert("RGB").save(OUT / "icon-512.png", optimize=True)
    icon(180, 0.64, False).convert("RGB").save(OUT / "apple-touch-icon.png", optimize=True)
    for name in ("icon-192.png", "icon-512.png", "apple-touch-icon.png"):
        print(OUT / name, Image.open(OUT / name).size)


if __name__ == "__main__":
    main()
