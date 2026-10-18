"""Drawer puzzle art (ART_REQUEST_01822 section 1, delivered 2026-10-15 15:46 PDT).

    python3 dev/import_drawer_puzzle.py           # import (idempotent)
    python3 dev/import_drawer_puzzle.py --check   # verify sources and imported files, change nothing

Sources (unchanged, SHA-256 from the handoff MANIFEST.json) live in
art/drawer-puzzle4-20261015/. Display sizes come from the handoff, in the
1280x720 inspection canvas:

  open drawer   1672x941 source  -> shown 1280x720 at (0,0)  (same size as the closed drawer)
  blank paper   1787x880 source  -> shown 305x150 at (435,385)
  rubbing       1786x880 source  -> shown 305x150 at (435,385)
  ruler (held)  1254x1254 source -> shown 120x120, bottom-left tip (source 365,955) on the
                                    groove (963,528): canvas top-left (928.1,436.6)

Both papers go through ONE common canvas (1787x880; the 1786-wide rubbing is
placed at its left edge) and are scaled the same way, never alpha-cropped one by
one, so the paper does not jump when the state changes.

Overlays are stored at twice their display size (premultiplied Lanczos, like
dev/apply_map_actions.py), so the 5-10x reduction does not alias in the browser.
The only correction: stray fringe pixels far from the object with alpha <= 6
(invisible, but they widen the layer) are cleared. Every file is written with
dev/import_art.py encode(lossless=True). The background is stored at its source size.
"""
import argparse, hashlib, io, json, shutil, sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/drawer-puzzle4-20261015"
LAYOUT = GAME / "room13-inspection-layout.json"
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

PAPER_CANVAS = (1787, 880)
SCALE = 2
STATES = {
    # key: (source, asset, display rect in 1280x720)
    "open": ("room13-pixel-inspect-drawer-open.png", "room13-pixel-inspect-drawer-open.webp", [0, 0, 1280, 720]),
    "paper": ("room13-pixel-inspect-rubbing-paper.png", "room13-pixel-inspect-rubbing-paper.webp", [435, 385, 305, 150]),
    "rubbing": ("room13-pixel-inspect-rubbing-done.png", "room13-pixel-inspect-rubbing-done.webp", [435, 385, 305, 150]),
    "held": ("room13-pixel-inspect-drawer-held.png", "room13-pixel-inspect-drawer-held.webp", None),
}
RULER_TIP = (365, 955)      # source px, handoff estimate (checked: middle of the ruler's end face)
GROOVE = (963, 528)         # 1280x720, centre of the drawer "divider" target
RULER_SIZE = 120


def ruler_rect():
    k = RULER_SIZE / 1254.0
    return [round(GROOVE[0] - RULER_TIP[0] * k, 1), round(GROOVE[1] - RULER_TIP[1] * k, 1), RULER_SIZE, RULER_SIZE]


def clean_fringe(img):
    a = np.asarray(img).copy()
    alpha = a[..., 3]
    solid = alpha >= 128
    lab, n = ndimage.label(solid)
    if n:
        sizes = ndimage.sum(solid, lab, range(1, n + 1))
        keep = ndimage.binary_dilation(lab == (int(np.argmax(sizes)) + 1), iterations=6)
        stray = (alpha > 0) & (alpha <= 6) & ~keep
        a[stray] = 0
    return Image.fromarray(a, "RGBA")


def resample(img, size):
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def build(key):
    src_name, asset, rect = STATES[key]
    img = Image.open(ART / src_name)
    img.load()
    if key == "open":
        return img.convert("RGB")
    img = clean_fringe(img.convert("RGBA"))
    if key in ("paper", "rubbing"):
        canvas = Image.new("RGBA", PAPER_CANVAS, (0, 0, 0, 0))
        canvas.paste(img, (0, 0))
        return resample(canvas, (rect[2] * SCALE, rect[3] * SCALE))
    return resample(img, (RULER_SIZE * SCALE, RULER_SIZE * SCALE))


def imported_pixels_match(path, expected):
    """Require exact RGBA pixels, not encoder-version-dependent WebP bytes."""
    try:
        with Image.open(path) as actual:
            return (actual.format == "WEBP" and actual.size == expected.size
                    and actual.convert("RGBA").tobytes() == expected.convert("RGBA").tobytes())
    except (OSError, ValueError):
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--from-dir", type=Path, help="unpacked handoff ZIP to copy the sources from")
    a = ap.parse_args()
    if a.from_dir and not a.check:
        ART.mkdir(parents=True, exist_ok=True)
        for name in ("HANDOFF.txt", "MANIFEST.json", "image-stats.json", "drawer-puzzle-preview.jpg") + tuple(s[0] for s in STATES.values()):
            shutil.copyfile(a.from_dir / name, ART / name)
    manifest = json.loads((ART / "MANIFEST.json").read_text(encoding="utf-8"))
    for item in manifest["assets"]:
        got = hashlib.sha256((ART / item["name"]).read_bytes()).hexdigest()
        if got != item["sha256"]:
            raise SystemExit("hash mismatch: %s" % item["name"])
    layout = json.loads(LAYOUT.read_text(encoding="utf-8"))
    states = {}
    bad = []
    for key, (src, asset, rect) in STATES.items():
        expected = build(key)
        out = GAME / "assets" / asset
        if a.check:
            if not imported_pixels_match(out, expected):
                bad.append(asset)
        else:
            data = encode(io.BytesIO(_png(expected)), lossless=True)
            out.write_bytes(data)
            print(asset, len(data), "bytes")
        states[key] = dict(file="assets/" + asset, rect=rect or ruler_rect(),
                           source=src, source_sha256=next(i["sha256"] for i in manifest["assets"] if i["name"] == src))
    if a.check:
        if layout.get("drawer_states") != states:
            bad.append("room13-inspection-layout.json drawer_states")
        print("not applied:", bad) if bad else print("all applied")
        sys.exit(1 if bad else 0)
    layout["drawer_states"] = states
    LAYOUT.write_text(json.dumps(layout, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _png(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


if __name__ == "__main__":
    main()
