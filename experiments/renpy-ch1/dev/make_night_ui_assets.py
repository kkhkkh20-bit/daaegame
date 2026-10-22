"""Night-ink UI assets (owner 2026-10-22: the Notion "shallow dialogue area" mockup and the
settings mockup). Run once; the PNGs are committed under game/assets/ui-night/.

  say_shade.png      bottom gradient behind the dialogue (no box)
  name_ribbon.png    burgundy brush ribbon for the speaker name (Frame, stretches sideways)
  opt_panel.png      settings panel: deep navy, thin gold border, small corner curls
  opt_btn_*.png      segmented choice buttons (idle / hover / selected / insensitive)
  opt_tab.png        burgundy brush under the chosen settings tab
  diamond*.png       small gold diamonds used as markers
  close_x.png        the settings close mark
"""
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

import os
OUT = Path(os.environ.get("R13_UI_OUT") or (Path(__file__).resolve().parents[1] / "game/assets/ui-night"))
# Palette: "night" (navy, 0.19.98) or "brown" (owner idea 2026-10-22: same style, beige/brown tone).
TONE = os.environ.get("R13_UI_TONE", "night")
PAL = {
    "night": dict(shade=(10, 13, 28), shade_top=(6, 6, 8), panel_top=(24, 31, 58), panel_drop=(8, 10, 18),
                  btn=(15, 20, 38), btn_hover=(40, 34, 58), box=(9, 13, 28), box_line=(104, 108, 128)),
    "brown": dict(shade=(26, 16, 11), shade_top=(8, 6, 4), panel_top=(58, 40, 29), panel_drop=(20, 13, 9),
                  btn=(40, 27, 19), btn_hover=(72, 50, 34), box=(30, 20, 14), box_line=(150, 122, 92)),
}[TONE]
OUT.mkdir(parents=True, exist_ok=True)
GOLD = (201, 168, 106)
GOLD_HI = (232, 205, 146)
NAVY = (14, 19, 38)
BURGUNDY = (122, 28, 36)
rng = random.Random(1022)


def save(img, name):
    img.save(OUT / name, optimize=True)


def shade():
    w, h = 8, 320
    img = Image.new("RGBA", (w, h))
    for y in range(h):
        t = y / (h - 1)
        # smoothstep up to ~70%, then flat; keeps the art visible above the text.
        a = 0.0 if t < 0.0 else min(1.0, t / 0.72)
        a = a * a * (3 - 2 * a)
        r, g, b = PAL["shade"]; dr, dg, db = PAL["shade_top"]
        col = (int(r + dr * (1 - t)), int(g + dg * (1 - t)), int(b + db * (1 - t)), int(round(240 * a)))
        for x in range(w):
            img.putpixel((x, y), col)
    save(img, "say_shade.png")


def brush(w, h, seed, flare_left=True):
    """A dry-brush burgundy stroke: ragged top/bottom edges, frayed right end."""
    r = random.Random(seed)
    scale = 4
    W, H = w * scale, h * scale
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    top = []
    bot = []
    for x in range(W + 1):
        u = x / W
        wob = math.sin(u * 9 + seed) * 0.03 + r.uniform(-0.015, 0.015)
        thick = 0.36 + 0.08 * math.sin(u * 3.1)
        if flare_left and u < 0.08:
            thick *= 0.55 + u / 0.08 * 0.45
        if u > 0.86:
            thick *= max(0.25, 1 - (u - 0.86) / 0.14 * 0.7)
        top.append((x, H * (0.5 - thick + wob)))
        bot.append((x, H * (0.5 + thick + wob * 0.6)))
    d.polygon(top + bot[::-1], fill=BURGUNDY + (255,))
    # frayed bristle streaks at the right end and along the edges
    for _ in range(46):
        y = r.uniform(H * 0.18, H * 0.82)
        x0 = r.uniform(W * 0.70, W * 0.92)
        L = r.uniform(W * 0.04, W * 0.12)
        d.line([(x0, y), (min(W - 2, x0 + L), y + r.uniform(-3, 3))], fill=BURGUNDY + (r.randint(150, 255),), width=r.randint(2, 5))
    img = img.filter(ImageFilter.GaussianBlur(1.2))
    # darker lower edge and lighter upper sheen
    px = img.load()
    for y in range(H):
        k = y / H
        for x in range(W):
            c = px[x, y]
            if c[3]:
                f = 1.12 - 0.35 * k + r.uniform(-0.05, 0.05)
                px[x, y] = (min(255, int(c[0] * f)), min(255, int(c[1] * f)), min(255, int(c[2] * f)), c[3])
    return img.resize((w, h), Image.LANCZOS)


def diamond(size, fill=GOLD_HI, outline=False):
    s = size * 4
    img = Image.new("RGBA", (s, s))
    d = ImageDraw.Draw(img)
    pts = [(s / 2, 0), (s - 1, s / 2), (s / 2, s - 1), (0, s / 2)]
    if outline:
        d.polygon(pts, outline=fill + (255,), width=max(2, s // 6))
    else:
        d.polygon(pts, fill=fill + (255,))
    return img.resize((size, size), Image.LANCZOS)


def rounded(w, h, fill, border, radius=5, width=2):
    s = 4
    img = Image.new("RGBA", (w * s, h * s))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([width * s // 2, width * s // 2, w * s - 1 - width * s // 2, h * s - 1 - width * s // 2],
                        radius=radius * s, fill=fill, outline=border, width=width * s)
    return img.resize((w, h), Image.LANCZOS)


def buttons():
    save(rounded(48, 44, PAL["btn"] + (150,), GOLD + (230,)), "opt_btn_idle.png")
    save(rounded(48, 44, PAL["btn_hover"] + (210,), GOLD_HI + (255,)), "opt_btn_hover.png")
    save(rounded(48, 44, BURGUNDY + (245,), GOLD_HI + (255,)), "opt_btn_selected.png")
    save(rounded(48, 44, PAL["btn"] + (110,), (120, 108, 90, 200)), "opt_btn_insensitive.png")
    save(rounded(48, 44, PAL["box"] + (215,), PAL["box_line"] + (220,), radius=6, width=1), "preview_box.png")


def panel(w=1256, h=696):
    s = 2
    W, H = w * s, h * s
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    # body: deep navy, slightly lighter at the top
    body = Image.new("RGBA", (W, H))
    bp = ImageDraw.Draw(body)
    for y in range(H):
        t = y / H
        tr, tg, tb = PAL["panel_top"]; dr, dg, db = PAL["panel_drop"]
        c = (int(tr - dr * t), int(tg - dg * t), int(tb - db * t), 238)
        bp.line([(0, y), (W, y)], fill=c)
    mask = Image.new("L", (W, H))
    ImageDraw.Draw(mask).rounded_rectangle([14 * s, 14 * s, W - 14 * s, H - 14 * s], radius=10 * s, fill=255)
    img.paste(body, (0, 0), mask)
    d.rounded_rectangle([14 * s, 14 * s, W - 14 * s, H - 14 * s], radius=10 * s, outline=GOLD + (235,), width=2 * s)
    d.rounded_rectangle([20 * s, 20 * s, W - 20 * s, H - 20 * s], radius=7 * s, outline=GOLD + (90,), width=1 * s)
    # corner curls just outside the border
    for cx, cy, sx, sy in ((14, 14, 1, 1), (w - 14, 14, -1, 1), (14, h - 14, 1, -1), (w - 14, h - 14, -1, -1)):
        X, Y = cx * s, cy * s
        r = 9 * s
        box = [X - r if sx > 0 else X - r, Y - r, X + r, Y + r]
        start = {(1, 1): 180, (-1, 1): 270, (1, -1): 90, (-1, -1): 0}[(sx, sy)]
        d.arc([X - sx * 2 * s - r, Y - sy * 2 * s - r, X - sx * 2 * s + r, Y - sy * 2 * s + r], start, start + 270, fill=GOLD + (220,), width=2 * s)
        d.ellipse([X - sx * 2 * s - 2 * s, Y - sy * 2 * s - 2 * s, X - sx * 2 * s + 2 * s, Y - sy * 2 * s + 2 * s], fill=GOLD_HI + (255,))
    save(img.resize((w, h), Image.LANCZOS), "opt_panel.png")


def close_x(size=34):
    s = 4
    img = Image.new("RGBA", (size * s, size * s))
    d = ImageDraw.Draw(img)
    m = 4 * s
    d.line([(m, m), (size * s - m, size * s - m)], fill=(240, 228, 206, 255), width=3 * s)
    d.line([(size * s - m, m), (m, size * s - m)], fill=(240, 228, 206, 255), width=3 * s)
    save(img.resize((size, size), Image.LANCZOS), "close_x.png")


def gold_rule(w=240):
    img = Image.new("RGBA", (w, 9))
    d = ImageDraw.Draw(img)
    d.line([(6, 4), (w - 1, 4)], fill=GOLD + (200,), width=1)
    img.alpha_composite(diamond(9), (0, 0))
    save(img, "gold_rule.png")


if __name__ == "__main__":
    shade()
    save(brush(220, 50, 3), "name_ribbon.png")
    save(brush(200, 64, 7), "opt_tab.png")
    save(diamond(8), "diamond.png")
    save(diamond(14, outline=True), "diamond_outline.png")
    buttons()
    panel()
    close_x()
    gold_rule()
    print("written", sorted(p.name for p in OUT.iterdir()))
