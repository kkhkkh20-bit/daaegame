"""Add or replace art in game/assets in its final web form.

    python dev/import_art.py path/to/new-art.png [--name room13-pixel-foo.webp] [--lossless]

PNG/WebP input is stored as lossy WebP q95 with lossless alpha (what the web
release ships; visually identical for this art at 3x zoom, about 4x smaller).
--lossless keeps every pixel (use for tiny UI art where 1px matters).
Scripts should reference the .webp name.
"""
import argparse, io
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]

def encode(src, lossless=False):
    im = Image.open(src); im.load()
    if im.mode not in ("RGB", "RGBA"):
        im = im.convert("RGBA")
    buf = io.BytesIO()
    if lossless:
        im.save(buf, "WEBP", lossless=True, method=6, quality=100, exact=True)
    else:
        im.save(buf, "WEBP", quality=95, method=6, alpha_quality=100)
    return buf.getvalue()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("--name")
    ap.add_argument("--lossless", action="store_true")
    a = ap.parse_args()
    name = a.name or (a.source.stem + ".webp")
    assert name.endswith(".webp") and "/" not in name
    out = ROOT / "game/assets" / name
    out.write_bytes(encode(a.source, a.lossless))
    print(out.relative_to(ROOT), out.stat().st_size, "bytes")

if __name__ == "__main__":
    main()
