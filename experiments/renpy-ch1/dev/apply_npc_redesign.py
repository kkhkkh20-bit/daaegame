"""Apply the 2026-10-15 NPC redesigns (art only) to existing Room13 NPCs.

    python3 dev/apply_npc_redesign.py            # apply (idempotent)
    python3 dev/apply_npc_redesign.py --revert   # restore the original entries
    python3 dev/apply_npc_redesign.py --check    # verify, change nothing

Registry: art/npc-redesign-20261015/redesign.json (design -> existing NPC id,
source PNG + SHA-256, head and avatar boxes in source pixels).

Only art data changes. IDs, names, dialogue, clues, evidence, unlocks,
schedules and time costs are untouched.

For each NPC:
  - game/assets/room13-redesign-<npc>.webp: the source at 0.5 scale,
    premultiplied resample, WebP q95 with lossless alpha (dev/import_art.py).
  - cast.json: every body state, avatar and portrait points at the new file.
  - room13-pixel-acting.json: neutral/thinking/distressed/expressive standing
    (+ avatar_* head crops). Seated/activity/living_* poses of the old design
    are dropped, so the NPC stands instead of showing the old body.
  - room13-portraits.json: the four bust keys become the full figure.
  - room13-fullbody-dialogue.json: all six expressions use the one image (the
    design has a single expression).
The replaced entries are saved first to art/npc-redesign-20261015/
original-entries.json. The old image files stay in game/assets (old saves can
still draw them); dev/build_web.py fetches them only on demand.
"""
import argparse, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/npc-redesign-20261015"
REGISTRY = ART / "redesign.json"
BACKUP = ART / "original-entries.json"
sys.path.insert(0, str(ROOT / "dev"))

FILES = {
    "cast": GAME / "assets/cast.json",
    "acting": GAME / "assets/room13-pixel-acting.json",
    "portraits": GAME / "assets/room13-portraits.json",
    "fullbody": GAME / "assets/room13-fullbody-dialogue.json",
}
BODY_STATES = ("neutral", "thinking", "distressed", "expressive")
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path, data, indent):
    # Keep each file's own trailing-newline convention (minimal diffs).
    end = "\n" if not path.exists() or path.read_text(encoding="utf-8").endswith("\n") else ""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + end, encoding="utf-8")


def indent_of(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("{\n"):
        return None
    second = text.split("\n", 2)[1]
    return len(second) - len(second.lstrip(" "))


def resample(img, scale):
    size = (max(1, round(img.width * scale)), max(1, round(img.height * scale)))
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def scaled_box(box, scale, size):
    x, y, w, h = [v * scale for v in box]
    x0, y0 = max(0, round(x)), max(0, round(y))
    x1, y1 = min(size[0], round(x + w)), min(size[1], round(y + h))
    return [x0, y0, x1 - x0, y1 - y0]


def geometry(design, registry):
    """Image (scaled) and per-NPC geometry, all in game-file pixels."""
    src = ART / design["source"]
    data = src.read_bytes()
    if hashlib.sha256(data).hexdigest() != design["sha256"]:
        raise SystemExit("hash mismatch: " + str(src))
    scale = registry["scale_from_source"]
    img = resample(Image.open(io.BytesIO(data)).convert("RGBA"), scale)
    alpha = np.asarray(img)[..., 3] >= registry["alpha_visible"]
    ys, xs = np.where(alpha.any(1))[0], np.where(alpha.any(0))[0]
    m = registry["margin"]
    x0, y0 = max(0, xs.min() - m), max(0, ys.min() - m)
    x1, y1 = min(img.width, xs.max() + 1 + m), min(img.height, ys.max() + 1 + m)
    crop = [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]
    figure = [int(xs.min()), int(ys.min()), int(xs.max() + 1 - xs.min()), int(ys.max() + 1 - ys.min())]
    bottom = int(ys.max())
    feet = np.where(alpha[max(0, bottom - 8):bottom + 1].any(0))[0]
    foot = [int((feet.min() + feet.max() + 1) // 2) - crop[0], bottom + 1 - crop[1]]
    hx, hy, hw, hh = scaled_box(design["head"], scale, img.size)
    head = [hx - crop[0], hy - crop[1], hw, hh]
    head = [max(0, head[0]), max(0, head[1]), min(hw, crop[2] - max(0, head[0])), min(hh, crop[3] - max(0, head[1]))]
    avatar = scaled_box(design["avatar"], scale, img.size)
    return img, dict(crop=crop, figure=figure, foot=foot, head=head, avatar=avatar)


def entries(npc, design, geo, file):
    body = {"file": file, "crop": geo["crop"], "nearest": True, "foot": geo["foot"], "facing": "front",
            "contact": "standing", "head": geo["head"], "reviewed": True, "posture": "standing",
            "redesign": design["design_id"]}
    avatar = {"file": file, "crop": geo["avatar"], "nearest": True, "dedicated_avatar": True,
              "facing": "front", "gaze": "viewer", "redesign": design["design_id"]}
    portrait = {"file": file, "crop": geo["crop"], "head": geo["head"], "full_body": True, "nearest": True,
                "facing": "front", "gaze": "viewer", "redesign": design["design_id"]}
    cast = {}
    for state in BODY_STATES:
        cast[state] = dict(body)
        cast["interview_" + state] = dict(body)
        cast["avatar_" + state] = dict(avatar)
    for state in ("world", "activity", "inn_activity"):
        cast[state] = dict(body)
    cast["avatar_activity"] = dict(avatar)
    for state in BODY_STATES:
        cast["portrait_" + state] = dict(portrait)
    acting = {}
    for state in BODY_STATES:
        acting[state] = dict(body)
        acting["avatar_" + state] = {"file": file, "crop": geo["avatar"]}
    portraits = {state: dict(portrait) for state in BODY_STATES}
    images = {e: {"file": file, "size": list(geo["size"]), "source_sha256": design["sha256"]} for e in EMOTIONS}
    fullbody = {"name_ko": design["name_ko"], "crop": geo["crop"], "figure": geo["figure"], "images": images,
                "redesign": design["design_id"]}
    return dict(cast=cast, acting=acting, portraits=portraits, fullbody=fullbody)


def section(data, kind):
    return data["people"] if kind == "fullbody" else data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    registry = load(REGISTRY)
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    backup = load(BACKUP) if BACKUP.exists() else {"note": "Entries replaced by dev/apply_npc_redesign.py, verbatim.", "npcs": {}}

    if args.revert:
        for npc, saved in backup["npcs"].items():
            for kind, entry in saved.items():
                section(data[kind], kind)[npc] = entry
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        print("reverted", sorted(backup["npcs"]))
        return

    report = []
    for design in registry["designs"]:
        npc = design["npc"]
        for kind in FILES:
            if npc not in section(data[kind], kind):
                raise SystemExit("unknown NPC %s in %s" % (npc, kind))
        img, geo = geometry(design, registry)
        geo["size"] = img.size
        name = "room13-redesign-%s.webp" % npc
        file = "assets/" + name
        new = entries(npc, design, geo, file)
        already = all(section(data[k], k)[npc] == new[k] for k in FILES)
        if args.check:
            report.append((npc, "applied" if already else "NOT applied", geo))
            continue
        if npc not in backup["npcs"]:
            current = {k: section(data[k], k)[npc] for k in FILES}
            if any(e.get("redesign") for e in current["cast"].values()):
                raise SystemExit("no original backup for already-redesigned " + npc)
            backup["npcs"][npc] = current
        from import_art import encode
        buf = io.BytesIO()
        img.save(buf, "PNG")
        (GAME / "assets" / name).write_bytes(encode(io.BytesIO(buf.getvalue())))
        for kind in FILES:
            section(data[kind], kind)[npc] = new[kind]
        report.append((npc, "applied", geo))

    if not args.check:
        dump(BACKUP, backup, 1)
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
    for npc, state, geo in report:
        print(npc, state, "size", tuple(geo["size"]), "crop", geo["crop"], "foot", geo["foot"], "head", geo["head"])


if __name__ == "__main__":
    main()
