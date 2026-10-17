"""O46 mountain ropes, 2nd art fix (owner 2026-10-16 17:05 PDT).

    python3 dev/extract_o46_ropes.py           # write derived overlay + game asset
    python3 dev/extract_o46_ropes.py --check   # report only

The delivered guide is an opaque full picture whose background drifted slightly while it was
made, so it is NOT used as a background and NOT differenced against the old one. Only the four
short ropes and the wooden toggle in the upper-left pine branches are taken: inside hand-drawn
regions (checked on a 4x zoom) a rope-colour test keeps the rope pixels. They are composited onto
the existing O46 overlay, so the empty cart stays exactly as it was. No loops (owner).

Inputs : art/expression-acting-20261016/second-fixes/manual-extraction-guide/room13-ep-O46-mountain-ropes.png
         art/ep-art-20261016/derived/ep-O46-mountain-ropes-cart.webp (the cart-only overlay, kept)
Outputs: art/ep-art-20261016/derived/ep-O46-mountain-ropes.webp (cart + ropes, lossless)
         game/assets/room13-ep-O46-mountain-ropes.webp (same picture; dev/apply_ep_art.py writes
         the same file from the derived picture)
"""
import argparse, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

GUIDE = ROOT / "art/expression-acting-20261016/second-fixes/manual-extraction-guide/room13-ep-O46-mountain-ropes.png"
CART = ROOT / "art/ep-art-20261016/derived/ep-O46-mountain-ropes-cart.webp"
DERIVED = ROOT / "art/ep-art-20261016/derived/ep-O46-mountain-ropes.webp"
ASSET = ROOT / "game/assets/room13-ep-O46-mountain-ropes.webp"
# Hand-drawn rope strips in guide pixels (2048x768).
ROPES = [
    [(85, 136), (94, 136), (99, 170), (100, 186), (88, 187), (87, 160)],             # 1 over the orange trunk
    [(175, 138), (184, 138), (197, 196), (188, 199)],                                # 2 diagonal
    [(282, 84), (290, 83), (292, 138), (300, 140), (299, 146), (281, 146), (284, 138)],  # 3 frayed end
    [(371, 166), (380, 166), (380, 214), (371, 214)],                                # 4 rope above the toggle
]
TOGGLE = (364, 214, 388, 219)   # wooden toggle bar on rope 4 (x0, y0, x1, y1), inclusive
REGION = (60, 70, 410, 240)     # nothing outside this box is ever taken


def ropes():
    g = np.asarray(Image.open(GUIDE).convert("RGB")).astype(int)
    H, W = g.shape[:2]
    mask = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(mask)
    for poly in ROPES:
        d.polygon(poly, fill=255)
    m = np.asarray(mask) > 0
    r, gg, b = g[..., 0], g[..., 1], g[..., 2]
    keep = m & (r > 130) & (gg > 95) & (b < gg) & (gg > 0.66 * r)
    t = np.zeros_like(keep)
    x0, y0, x1, y1 = TOGGLE
    t[y0:y1 + 1, x0:x1 + 1] = True
    keep |= t & (r > 150) & (gg > 95) & (b < 110)
    box = np.zeros_like(keep)
    box[REGION[1]:REGION[3], REGION[0]:REGION[2]] = True
    keep &= box
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = g
    rgba[..., 3] = np.where(keep, 255, 0)
    return Image.fromarray(rgba, "RGBA"), keep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    if not CART.exists():
        if a.check:
            raise SystemExit("cart-only overlay not saved yet")
        CART.write_bytes(DERIVED.read_bytes())   # first run: keep the cart-only overlay
    cart = Image.open(CART).convert("RGBA")
    rope, keep = ropes()
    if np.asarray(cart)[..., 3][keep].any():
        raise SystemExit("ropes overlap the cart")
    out = cart.copy()
    out.alpha_composite(rope)
    ys, xs = np.where(keep)
    print(json.dumps({"rope_pixels": int(keep.sum()), "bbox": [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]}))
    if a.check:
        return
    buf = io.BytesIO()
    out.save(buf, "PNG")
    DERIVED.write_bytes(encode(io.BytesIO(buf.getvalue()), lossless=True))
    ASSET.write_bytes(encode(io.BytesIO(buf.getvalue()), False))   # same encoding as dev/apply_ep_art.py


if __name__ == "__main__":
    main()
