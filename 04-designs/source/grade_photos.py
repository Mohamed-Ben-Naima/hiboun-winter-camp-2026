"""Grades the chosen camp photos for the designs: Lanczos upscale, light sharpening,
warm shift (+4% red, -5% blue), +6% contrast, +8% saturation and fine grain that hides
WhatsApp JPEG blocks. Reads 02-photos/<category>/, writes 02-photos/graded/."""
from pathlib import Path
from PIL import Image, ImageEnhance, ImageFilter
import numpy as np

ROOT = Path(__file__).resolve().parents[2]
PHOTOS = ROOT / '02-photos'
OUT = PHOTOS / 'graded'
OUT.mkdir(exist_ok=True)

def grade(src, dst, target_w, warm=1.0, contrast=1.06, sat=1.08, bright=1.0):
    im = Image.open(src).convert('RGB')
    im = im.resize((target_w, int(im.height * target_w / im.width)), Image.LANCZOS)
    im = im.filter(ImageFilter.UnsharpMask(radius=1.6, percent=60, threshold=2))
    im = ImageEnhance.Contrast(im).enhance(contrast)
    im = ImageEnhance.Color(im).enhance(sat)
    im = ImageEnhance.Brightness(im).enhance(bright)
    a = np.asarray(im).astype(np.float32)
    a[..., 0] *= 1.0 + 0.04 * warm
    a[..., 2] *= 1.0 - 0.05 * warm
    g = np.random.default_rng(3).normal(0, 4.0, a.shape[:2])[..., None]
    Image.fromarray(np.clip(a + g, 0, 255).astype(np.uint8)).save(dst, quality=90, optimize=True, progressive=True)
    print(dst.name, Image.open(dst).size)

# graded name            source photo                                   width
JOBS = [
    ('hero-tent-sunset.jpg', 'tents/hero-palm-tent-sunset.jpeg', 1440, {}),
    ('fire-tents.jpg',       'night-and-fire/fire-tents.jpeg',     1296, {}),
    ('night-lights.jpg',     'night-and-fire/night-tents-lights.jpeg', 1440, {'bright': 1.04}),
    ('palm-tent.jpg',        'tents/palm-frond-tent.jpeg',         1350, {}),
    ('well-night.jpg',       'night-and-fire/well-night.jpeg',     1440, {}),
]

if __name__ == '__main__':
    for name, src, w, kw in JOBS:
        grade(PHOTOS / src, OUT / name, w, **kw)
