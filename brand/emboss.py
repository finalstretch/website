#!/usr/bin/env python3
"""Render the Final Stretch seal with real embossed lighting.

Pipeline: rasterize base coin + height mask, blur mask into a height
map, shade with a directional light (top-left), composite highlight
and shadow onto the coin, cut out the disc with an anti-aliased alpha.

Usage:
  python3 brand/emboss.py          # full seal  -> logo-seal.png
  python3 brand/emboss.py header   # header medallion -> logo-header.png
"""
import subprocess, sys, os
import numpy as np
from PIL import Image, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
N = 2048  # render size (supersampled)

PROFILES = {
    # mask file, output file, output px, broad/tight blur mix, light gain,
    # base brightness multiplier
    "seal":   ("mask.svg",        "logo-seal.png",   1024, (0.45, 8, 0.55, 2.6), 2100.0, 1.0),
    "header": ("mask-header.svg", "logo-header.png",  256, (0.40, 7, 0.60, 2.4), 3400.0, 1.12),
    "hero":   ("mask-hero.svg",   "logo-hero.webp",   560, (0.45, 8, 0.55, 2.6), 2100.0, 1.0),
}
profile = sys.argv[1] if len(sys.argv) > 1 else "seal"
MASK, OUTFILE, OUT, (w1, s1, w2, s2), GAIN, LIFT = PROFILES[profile]

def rasterize(svg, out):
    subprocess.run(["qlmanage", "-t", "-s", str(N), "-o", HERE, svg],
                   check=True, capture_output=True)
    produced = os.path.join(HERE, os.path.basename(svg) + ".png")
    os.replace(produced, out)
    img = Image.open(out).convert("RGB").resize((N, N), Image.LANCZOS)
    arr = np.asarray(img).astype(np.float64)
    os.remove(out)
    return arr

base = rasterize(os.path.join(HERE, "base.svg"), os.path.join(HERE, "_base.png"))
maskimg = rasterize(os.path.join(HERE, MASK), os.path.join(HERE, "_mask.png"))

base = (base * LIFT).clip(0, 255)
mask = maskimg.mean(axis=2) / 255.0  # 0..1, white = raised

def gblur(a, sigma):
    im = Image.fromarray((a * 255).clip(0, 255).astype(np.uint8))
    return np.asarray(im.filter(ImageFilter.GaussianBlur(sigma))).astype(np.float64) / 255.0

# Height map: soft dome on each raised element (two blur scales:
# broad bevel + tight edge definition)
h = w1 * gblur(mask, s1) + w2 * gblur(mask, s2)

# Directional lighting from the top-left
gy, gx = np.gradient(h)
light = (-gx - gy) / np.sqrt(2.0) * GAIN
spec = np.clip(light, 0, None)
shad = np.clip(-light, 0, None)
# soft-knee so peaks don't clip harshly
spec = 255.0 * (1.0 - np.exp(-spec / 110.0))
shad = 255.0 * (1.0 - np.exp(-shad / 110.0))

out = base.copy()
# screen highlights toward warm white
for c, tint in enumerate((255.0, 245.0, 235.0)):
    out[..., c] += spec / 255.0 * (tint - out[..., c]) * 0.85
# multiply shadows toward deep navy
for c, floor in enumerate((3.0, 25.0, 60.0)):
    out[..., c] -= shad / 255.0 * (out[..., c] - floor) * 0.75
# faint ambient lift on raised faces so they catch light overall
out += (mask * 10.0)[..., None]

out = out.clip(0, 255)

# Anti-aliased circular alpha
yy, xx = np.mgrid[0:N, 0:N]
r = np.hypot(xx - (N - 1) / 2.0, yy - (N - 1) / 2.0)
alpha = np.clip(((N / 2.0 - 1.5) - r) / 2.0 + 0.5, 0, 1) * 255.0

rgba = np.dstack([out, alpha]).astype(np.uint8)
dest = os.path.join(ROOT, OUTFILE)
result = Image.fromarray(rgba).resize((OUT, OUT), Image.LANCZOS)
if dest.endswith(".webp"):
    result.save(dest, quality=88, method=6)
else:
    result.save(dest)
print("wrote", dest)
