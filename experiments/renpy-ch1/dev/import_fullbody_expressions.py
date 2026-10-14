"""Import the 43-character full-body dialogue expression package.

    python3 dev/import_fullbody_expressions.py /path/daram-fullbody-expressions-43-v3

Input: the v3 full package (characters/<id>/<emotion>.png + manifest.json,
258 PNG). Every PNG is checked against the package manifest SHA-256 first.

Output (game/assets):
  room13-fullbody-<id>-<emotion>.webp   WebP q95, alpha lossless (dev/import_art.py)
  room13-fullbody-dialogue.json         per-character fixed crop and figure box

The crop is the union of all six expressions' visible area (alpha >= 32) plus
a small margin, so one character uses one crop and one scale for every
expression: switching expression never moves or resizes the body.

Existing dialogue busts, profile avatars and world sprites are not touched.
Per-line emotions live in room13-fullbody-line-emotions.json (hand-authored).
"""
import argparse, hashlib, io, json, multiprocessing, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")
ALPHA_VISIBLE = 32
MARGIN = 4
# The dialogue renders through a 3px pixel grid (R13_CLOSE_PIXEL_GRID): the
# source is shown at about 0.6x and then sampled at 1/3 of that. Half-size
# copies are still ~2.5x the sampled resolution, decode 4x faster and use a
# quarter of the texture memory (full-size copies stalled the web build).
SCALE = 0.5

# guard/anxious and guard/joy: v1 left a semi-transparent hole where the tail
# meets the coat (background showed through the body). Only that junction box
# is repaired, by copying the matching opaque pixels of guard/neutral. Faces
# and every pixel outside the box are unchanged. See RELEASE_0185.md.
GUARD_JUNCTION = {"box": (690, 925, 800, 1160), "threshold": 245, "grow": 4}


def repair_guard_junction(img, neutral):
    from scipy.ndimage import binary_dilation, binary_erosion, label
    a = np.asarray(img.convert("RGBA")).copy()
    n = np.asarray(neutral.convert("RGBA"))
    x0, y0, x1, y1 = GUARD_JUNCTION["box"]
    core = binary_erosion(n[..., 3] >= 200, iterations=4)
    hole = core & (a[..., 3] < GUARD_JUNCTION["threshold"])
    box = np.zeros_like(hole)
    box[y0:y1, x0:x1] = True
    hole &= box
    lab, count = label(hole, structure=np.ones((3, 3), bool))
    sizes = np.bincount(lab.ravel())[1:]
    keep = np.isin(lab, [i + 1 for i in range(count) if sizes[i] >= 20])
    mask = binary_dilation(keep, iterations=GUARD_JUNCTION["grow"]) & (n[..., 3] >= 200)
    a[mask] = n[mask]
    return Image.fromarray(a, "RGBA"), int(mask.sum())


def resample(img, scale):
    # Premultiplied resampling keeps transparent edges free of dark fringes.
    if scale == 1:
        return img
    size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def write_webp(job):
    name, png = job
    (ROOT / "game/assets" / name).write_bytes(encode(io.BytesIO(png)))
    return name


def visible_box(img):
    alpha = img.getchannel("A").point(lambda v: 255 if v >= ALPHA_VISIBLE else 0)
    return alpha.getbbox()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("package", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--json-only", action="store_true", help="rewrite the JSON, keep existing WebP files")
    ap.add_argument("--scale", type=float, default=SCALE, help="resample factor for the game copy (default %(default)s)")
    args = ap.parse_args()
    pkg = args.package
    manifest = json.loads((pkg / "manifest.json").read_text(encoding="utf-8"))
    files = {(f["id"], f["expression"]): f for f in manifest["files"]}
    ids = sorted({f["id"] for f in manifest["files"]})
    assert len(ids) == 43 and len(files) == 258, (len(ids), len(files))
    for (cid, emo), f in files.items():
        data = (pkg / f["path"]).read_bytes()
        if hashlib.sha256(data).hexdigest() != f["sha256"]:
            raise SystemExit("hash mismatch: " + f["path"])

    people = {}
    repairs = {}
    jobs = []
    for cid in ids:
        neutral = Image.open(pkg / files[(cid, "neutral")]["path"]); neutral.load()
        images = {}
        for emo in EMOTIONS:
            img = Image.open(pkg / files[(cid, emo)]["path"]); img.load()
            img = img.convert("RGBA")
            if cid == "guard" and emo in ("anxious", "joy"):
                img, count = repair_guard_junction(img, neutral)
                repairs["guard/" + emo] = count
            images[emo] = resample(img, args.scale)
        boxes = [visible_box(images[e]) for e in EMOTIONS]
        width = min(images[e].width for e in EMOTIONS)
        height = min(images[e].height for e in EMOTIONS)
        x0 = max(0, min(b[0] for b in boxes) - MARGIN)
        y0 = max(0, min(b[1] for b in boxes) - MARGIN)
        x1 = min(width, max(b[2] for b in boxes) + MARGIN)
        y1 = min(height, max(b[3] for b in boxes) + MARGIN)
        figure = visible_box(images["neutral"])
        entry = {
            "name_ko": files[(cid, "neutral")]["name_ko"],
            "crop": [x0, y0, x1 - x0, y1 - y0],
            "figure": [figure[0], figure[1], figure[2] - figure[0], figure[3] - figure[1]],
            "images": {},
        }
        for emo in EMOTIONS:
            name = "room13-fullbody-%s-%s.webp" % (cid, emo)
            entry["images"][emo] = {
                "file": "assets/" + name,
                "size": [images[emo].width, images[emo].height],
                "source_sha256": files[(cid, emo)]["sha256"],
            }
            if not args.dry_run and not args.json_only:
                buf = io.BytesIO()
                images[emo].save(buf, "PNG")
                jobs.append((name, buf.getvalue()))
        people[cid] = entry

    # WebP method 6 is slow (~10 s per 1024x1536 image): use every core.
    with multiprocessing.Pool() as pool:
        for name in pool.imap_unordered(write_webp, jobs):
            pass

    out = {
        "version": 1,
        "source_package": pkg.name,
        "source_status": manifest.get("status"),
        "emotions": list(EMOTIONS),
        "alpha_visible": ALPHA_VISIBLE,
        "scale_from_source": args.scale,
        "margin": MARGIN,
        "repairs": {k: {"method": "copy guard/neutral opaque pixels into tail-coat junction hole",
                        "box": list(GUARD_JUNCTION["box"]), "pixels": v} for k, v in repairs.items()},
        "people": people,
    }
    target = ROOT / "game/assets/room13-fullbody-dialogue.json"
    if not args.dry_run:
        target.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(len(people), "characters,", sum(len(p["images"]) for p in people.values()), "images; repairs", repairs)


if __name__ == "__main__":
    main()
