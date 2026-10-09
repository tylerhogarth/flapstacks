#!/usr/bin/env python3
"""Generate share images, icons and web variants.

Share images and the page hero come from src/hero.png. Favicons and PWA icons
come from src/logo-transparent.png (the logo on a transparent background).

Usage (from repo root):
    python3 -m venv .venv && .venv/bin/pip install pillow
    .venv/bin/python scripts/generate-assets.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
SRC = Image.open(ROOT / "src" / "hero.png").convert("RGB")
LOGO = Image.open(ROOT / "src" / "logo-transparent.png").convert("RGBA")
W = SRC.size[0]
BG = (5, 2, 1)       # sampled from the hero's corners
GLOW = (40, 18, 5)   # sampled from the hero's edge glow


def radial_bg(w, h, radius=None):
    """Dark canvas with a warm radial glow matching the hero's vignette."""
    cx, cy = w / 2, h / 2
    radius = radius or max(w, h) * 0.6
    small = Image.new("RGB", (w // 8, h // 8), BG)
    d = ImageDraw.Draw(small)
    steps = 40
    for i in range(steps, 0, -1):
        t = i / steps
        r = radius * t / 8
        col = tuple(int(BG[k] + (GLOW[k] - BG[k]) * (1 - t)) for k in range(3))
        d.ellipse([cx / 8 - r, cy / 8 - r, cx / 8 + r, cy / 8 + r], fill=col)
    return small.resize((w, h), Image.LANCZOS).filter(ImageFilter.GaussianBlur(8))


def compose(w, h, hero_size, out):
    canvas = radial_bg(w, h)
    hero = SRC.resize((hero_size, hero_size), Image.LANCZOS)
    canvas.paste(hero, ((w - hero_size) // 2, (h - hero_size) // 2))
    canvas.save(out, quality=85, optimize=True, progressive=True)
    print(out.relative_to(ROOT))


def main():
    compose(1200, 630, 630, ASSETS / "og-image.jpg")
    compose(1200, 1200, 1200, ASSETS / "og-image-square.jpg")

    # Square the transparent logo on a transparent canvas, trimmed to content.
    logo = LOGO.crop(LOGO.getbbox())
    side = max(logo.size)
    square = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    square.paste(logo, ((side - logo.width) // 2, (side - logo.height) // 2), logo)

    def logo_at(size):
        return square.resize((size, size), Image.LANCZOS)

    for size, name in [(512, "icon-512.png"), (192, "icon-192.png"), (32, "favicon-32.png"), (16, "favicon-16.png")]:
        logo_at(size).save(ASSETS / name, optimize=True)
        print(name)

    logo_at(48).save(ROOT / "favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)])
    print("favicon.ico")

    # iOS ignores alpha and renders it black, so the touch icon gets the page background.
    touch = radial_bg(180, 180)
    touch.paste(logo_at(160), (10, 10), logo_at(160))
    touch.save(ASSETS / "apple-touch-icon.png", optimize=True)
    print("apple-touch-icon.png")

    # Maskable icon keeps content inside the inner 80% safe zone.
    maskable = radial_bg(512, 512)
    maskable.paste(logo_at(400), (56, 56), logo_at(400))
    maskable.save(ASSETS / "icon-maskable-512.png", optimize=True)
    print("icon-maskable-512.png")

    SRC.save(ASSETS / "hero.webp", quality=88, method=6)
    SRC.resize((800, 800), Image.LANCZOS).save(ASSETS / "hero-800.webp", quality=88, method=6)
    SRC.resize((1024, 1024), Image.LANCZOS).save(
        ASSETS / "hero.jpg", quality=88, optimize=True, progressive=True
    )
    print("hero variants done")


if __name__ == "__main__":
    main()
