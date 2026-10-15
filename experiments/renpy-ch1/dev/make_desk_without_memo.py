"""Desk close-up after Mom's memo is picked up (0.18.48, owner: the memo must disappear).

The envelope is painted into room13-pixel-inspect-desk.webp. This fills its rectangle (with the
drop shadow) row by row: a straight blend between the wood just left and right of it, plus the
grain of the same rows taken from clean wood further right, so planks and lighting continue.
Writes assets/room13-pixel-inspect-desk-nomemo.webp. Run: python3 dev/make_desk_without_memo.py
"""
from pathlib import Path
import numpy as np
from PIL import Image
GAME = Path(__file__).resolve().parents[1] / "game"
src = Image.open(GAME / "assets/room13-pixel-inspect-desk.webp").convert("RGB")
a = np.asarray(src).astype(float)
x0, x1, y0, y1 = 405, 790, 90, 362          # envelope + shadow, source pixels (1672x941)
g0, g1 = 796, 926                             # clean wood strip between the hole and the case
w = x1 - x0
out = a.copy()
strip = a[:, g0:g1]
grain_rows = np.concatenate([strip, strip[:, ::-1]] * (w // (2 * (g1 - g0)) + 1), axis=1)[:, :w]
feather = 14
for y in range(y0 - feather, y1 + feather):
    left = a[y, x0 - 6:x0].mean(0)
    right = a[y, x1:x1 + 6].mean(0)
    t = np.linspace(0, 1, w)[:, None]
    base = left * (1 - t) + right * t
    grain = grain_rows[y] - grain_rows[y].mean(0)
    fill = np.clip(base + grain * .9, 0, 255)
    # Soft edges: blend into the original near the rectangle's border.
    edge = np.minimum(np.arange(w), np.arange(w)[::-1])[:, None]
    k = np.clip(edge / feather, 0, 1)
    if y < y0 or y >= y1:
        k = k * (1 - min(abs(y - (y0 if y < y0 else y1 - 1)), feather) / feather)
    out[y, x0:x1] = a[y, x0:x1] * (1 - k) + fill * k
img = Image.fromarray(out.astype("uint8"))
img.save(GAME / "assets/room13-pixel-inspect-desk-nomemo.webp", "WEBP", lossless=True)
print("written")
