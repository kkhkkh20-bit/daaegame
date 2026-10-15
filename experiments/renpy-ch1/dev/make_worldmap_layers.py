"""Pre-cut the village map v5 destination layers (ported from closed PR #8).

    python3 dev/make_worldmap_layers.py

PR #8 built every layer at run time (22 AlphaMask + canvas polygons, redrawn on
each hover). In the web build that made travel ~4x slower and, together with
full-body portraits, crashed a software-rendered browser. The same polygons are
now cut once from the original PNG:

  assets/room13-worldmap-v5-<key>.webp          cut-out (lossless): hover/selected
                                               highlight and pointer focus mask
  assets/room13-worldmap-v5-<key>-outline.webp  7px outline of the polygon

Only the 8 real destinations get files. The 14 scenery polygons (shrine, old
quarry, houses, farm) stay as data in room13-worldmap-v5.json and the SVGs in
design/maps/20261014; they are part of the base picture and never clickable.
The polygons are hand-placed outlines, not pixel-exact building cut-outs.
"""
import hashlib, io, json
from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT.parents[1] / "design/maps/20261014/worldmap-winter-shrine-old-quarry-v5.png"
DATA = json.loads((ROOT / "game/room13-worldmap-v5.json").read_text(encoding="utf-8"))


def webp(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", lossless=True, method=6, quality=100, exact=True)
    return buf.getvalue()


def main():
    assert hashlib.sha256(SOURCE.read_bytes()).hexdigest() == DATA["sha256"]
    art = Image.open(SOURCE).convert("RGBA")
    for key, spec in DATA["layers"].items():
        if not spec["node"]:
            continue
        x, y, w, h = spec["bounds"]
        points = [(px - x, py - y) for px, py in spec["polygon"]]
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).polygon(points, fill=255)
        cut = art.crop((x, y, x + w, y + h))
        cut.putalpha(mask)
        outline = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(outline).polygon(points, outline=(0xff, 0xd5, 0x7b, 255), width=7)
        for suffix, im in (("", cut), ("-outline", outline)):
            out = ROOT / "game/assets" / ("room13-worldmap-v5-%s%s.webp" % (key, suffix))
            out.write_bytes(webp(im))
            print(out.relative_to(ROOT), out.stat().st_size)


if __name__ == "__main__":
    main()
