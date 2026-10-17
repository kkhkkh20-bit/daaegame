"""Add the 2026-10-15 investigation actions (event, life and map actions) as world poses.

    python3 dev/apply_map_actions.py           # apply (idempotent)
    python3 dev/apply_map_actions.py --check   # verify, change nothing

Registry: art/map-actions-20261015/registry.json (person, pose key, source PNG +
SHA-256, contact, head box / foot / seat in source pixels).

Only investigation-scene poses are added. Dialogue full-body art, portraits,
avatars and every existing pose stay as they are; nothing is removed.

For each pose:
  - game/assets/room13-action-<person>-<pose>.webp: the source at 0.5 scale
    (premultiplied resample, WebP q95 with lossless alpha, dev/import_art.py).
  - room13-pixel-acting.json[person][pose]: crop = visible alpha box + margin,
    foot = middle of both feet at the lowest visible row (or the registry
    foot), head / seat from the registry, all crop-relative after scaling.
"""
import argparse, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/map-actions-20261015"
REGISTRY = ART / "registry.json"
ACTING = GAME / "assets/room13-pixel-acting.json"
sys.path.insert(0, str(ROOT / "dev"))


def resample(img, scale):
    size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def build(entry, reg):
    src = (ART / entry["source"]).resolve()
    data = src.read_bytes()
    if hashlib.sha256(data).hexdigest() != entry["sha256"]:
        raise SystemExit("hash mismatch: %s" % src)
    s = reg["scale_from_source"]
    img = resample(Image.open(io.BytesIO(data)).convert("RGBA"), s)
    alpha = np.asarray(img)[..., 3] >= reg["alpha_visible"]
    ys, xs = np.where(alpha.any(1))[0], np.where(alpha.any(0))[0]
    m = reg["margin"]
    x0, y0 = max(0, int(xs.min()) - m), max(0, int(ys.min()) - m)
    x1, y1 = min(img.width, int(xs.max()) + 1 + m), min(img.height, int(ys.max()) + 1 + m)
    crop = [x0, y0, x1 - x0, y1 - y0]
    if entry.get("foot"):
        foot = [round(entry["foot"][0] * s) - x0, round(entry["foot"][1] * s) - y0]
    else:
        bottom = int(ys.max())
        window = max(8, int(0.04 * (ys.max() - ys.min())))
        feet = np.where(alpha[max(0, bottom - window):bottom + 1].any(0))[0]
        foot = [int((feet.min() + feet.max() + 1) // 2) - x0, bottom + 1 - y0]
    hx, hy, hw, hh = entry["head"]
    head = [max(0, round(hx * s) - x0), max(0, round(hy * s) - y0), round(hw * s), round(hh * s)]
    spec = {"file": "assets/room13-action-%s-%s.webp" % (entry["person"], entry["pose"]), "crop": crop,
            "nearest": True, "foot": foot, "head": head, "contact": entry["contact"], "reviewed": True,
            "map_action": True, "stature_ratio": entry["stature_ratio"], "source_sha256": entry["sha256"]}
    if entry.get("seat"):
        spec["seat"] = [round(entry["seat"][0] * s) - x0, round(entry["seat"][1] * s) - y0]
    return img, spec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    reg = json.loads(REGISTRY.read_text(encoding="utf-8"))
    text = ACTING.read_text(encoding="utf-8")
    acting = json.loads(text)
    bad = []
    for entry in reg["poses"]:
        person, pose = entry["person"], entry["pose"]
        if person not in acting:
            raise SystemExit("unknown person " + person)
        if entry.get("withdrawn"):
            # 0.18.93: the drawing no longer matches the person's confirmed design (e.g. the tiger
            # name-tag pose after 네로 became the silver wolf). The pose is taken out of the game so the
            # person stands in the current design; the file stays on disk for old saves.
            if a.check:
                if pose in acting[person]:
                    bad.append(person + ":" + pose + " (withdrawn, still present)")
                continue
            if acting[person].pop(pose, None) is not None:
                print(person, pose, "withdrawn:", entry["withdrawn"])
            continue
        img, spec = build(entry, reg)
        if a.check:
            if acting[person].get(pose) != spec:
                bad.append(person + ":" + pose)
            continue
        from import_art import encode
        buf = io.BytesIO(); img.save(buf, "PNG")
        (GAME / spec["file"]).write_bytes(encode(io.BytesIO(buf.getvalue())))
        acting[person][pose] = spec
        print(person, pose, "crop", spec["crop"], "foot", spec["foot"], "head", spec["head"], "seat", spec.get("seat"))
    if a.check:
        print("not applied:", bad) if bad else print("all applied")
        sys.exit(1 if bad else 0)
    ACTING.write_text(json.dumps(acting, ensure_ascii=False, indent=2) + ("\n" if text.endswith("\n") else ""), encoding="utf-8")


if __name__ == "__main__":
    main()
