"""Apply NPC redesigns (art only) to existing Room13 NPCs.

    python3 dev/apply_npc_redesign.py            # apply (idempotent)
    python3 dev/apply_npc_redesign.py --revert   # restore the original entries
    python3 dev/apply_npc_redesign.py --check    # verify, change nothing

Registries, read in order; a later registry replaces an earlier one for the
same NPC (the earlier file stays as history):
  1. art/npc-redesign-20261015/redesign.json      8 NPCs (first redesign)
  2. art/character-remodel-20261015/remodel.json  37 NPCs (remodel 31 + kept 7,
     nabi stays on her original art and has no entry)
Each entry: existing NPC id, source PNG + SHA-256, head and avatar boxes in
source pixels, optional investigation poses.

Only art data changes. IDs, names (kept from the game data), dialogue, clues,
evidence, unlocks, schedules and time costs are untouched.

For each NPC:
  - game/assets/room13-redesign-<npc>.webp: the source at 0.5 scale,
    premultiplied resample, WebP q95 with lossless alpha (dev/import_art.py).
  - cast.json: every body state, avatar and portrait points at the new file.
  - room13-pixel-acting.json: neutral/thinking/distressed/expressive standing
    (+ avatar_* head crops). Seated/activity/living_* poses of the old design
    are dropped, so the NPC stands instead of showing the old body
    (room13_acting.rpy falls back to the standing picture for any old pose key).
  - Investigation poses (field living poses) from the registry are added as
    room13-redesign-<npc>-<pose>.webp with "scale_by_head": the field scales
    them so the head matches the standing head, never to the standing height.
    They are never used in dialogue (the full-body dialogue picture wins).
  - room13-portraits.json: the four bust keys become the full figure.
  - room13-fullbody-dialogue.json: all six expressions use the one image (each
    design has a single expression).
The replaced entries are saved first to art/npc-redesign-20261015/
original-entries.json (the entries from before any redesign). The old image
files stay in game/assets (old saves can still draw them); dev/build_web.py
fetches them only on demand.
"""
import argparse, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/npc-redesign-20261015"
REGISTRIES = [ART / "redesign.json", ROOT / "art/character-remodel-20261015/remodel.json"]
REGISTRY = REGISTRIES[0]
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


def designs():
    """[(design, registry_dir, registry)], later registries win per NPC."""
    chosen = {}
    for path in REGISTRIES:
        if not path.exists():
            continue
        registry = load(path)
        for design in registry["designs"]:
            chosen[design["npc"]] = (design, path.parent, registry)
        # "excluded": the script leaves that NPC exactly as the game has it.
        for item in registry.get("excluded", []):
            chosen.pop(item["npc"], None)
    return list(chosen.values())


def excluded():
    return {item["npc"] for path in REGISTRIES if path.exists() for item in load(path).get("excluded", [])}


def geometry(source, sha256, head_box, avatar_box, folder, registry):
    """Image (scaled) and geometry in game-file pixels for one source picture."""
    src = folder / source
    data = src.read_bytes()
    if hashlib.sha256(data).hexdigest() != sha256:
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
    # Both feet: the lowest 4% of the figure (a stance with one boot lower
    # than the other would otherwise anchor on that single boot).
    window = max(8, int(0.04 * figure[3]))
    feet = np.where(alpha[max(0, bottom - window):bottom + 1].any(0))[0]
    foot = [int((feet.min() + feet.max() + 1) // 2) - crop[0], bottom + 1 - crop[1]]
    hx, hy, hw, hh = scaled_box(head_box, scale, img.size)
    head = [hx - crop[0], hy - crop[1], hw, hh]
    head = [max(0, head[0]), max(0, head[1]), min(hw, crop[2] - max(0, head[0])), min(hh, crop[3] - max(0, head[1]))]
    avatar = scaled_box(avatar_box, scale, img.size) if avatar_box else None
    return img, dict(crop=crop, figure=figure, foot=foot, head=head, avatar=avatar, size=img.size)


def entries(design, geo, file, name_ko, poses):
    tag = design["design_id"]
    body = {"file": file, "crop": geo["crop"], "nearest": True, "foot": geo["foot"], "facing": "front",
            "contact": "standing", "head": geo["head"], "reviewed": True, "posture": "standing",
            "redesign": tag}
    avatar = {"file": file, "crop": geo["avatar"], "nearest": True, "dedicated_avatar": True,
              "facing": "front", "gaze": "viewer", "redesign": tag}
    portrait = {"file": file, "crop": geo["crop"], "head": geo["head"], "full_body": True, "nearest": True,
                "facing": "front", "gaze": "viewer", "redesign": tag}
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
    for key, (pose_file, pose_geo, spec) in poses.items():
        living = {"file": pose_file, "crop": pose_geo["crop"], "nearest": True, "foot": pose_geo["foot"],
                  "facing": "front", "contact": spec.get("contact", "self-contained"), "head": pose_geo["head"],
                  "reviewed": True, "action_ko": spec["action_ko"], "scale_by_head": bool(spec.get("scale_by_head")),
                  "redesign": tag}
        acting[key] = dict(living)
        cast[key] = dict(living)
    portraits = {state: dict(portrait) for state in BODY_STATES}
    images = {e: {"file": file, "size": list(geo["size"]), "source_sha256": design["sha256"]} for e in EMOTIONS}
    fullbody = {"name_ko": name_ko, "crop": geo["crop"], "figure": geo["figure"],
                "images": images, "redesign": tag}
    return dict(cast=cast, acting=acting, portraits=portraits, fullbody=fullbody)


def section(data, kind):
    return data["people"] if kind == "fullbody" else data


def encode_webp(img, name):
    from import_art import encode
    buf = io.BytesIO()
    img.save(buf, "PNG")
    (GAME / "assets" / name).write_bytes(encode(io.BytesIO(buf.getvalue())))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--only", nargs="*", help="limit to these NPC ids")
    args = ap.parse_args()
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    backup = load(BACKUP) if BACKUP.exists() else {"note": "Entries replaced by dev/apply_npc_redesign.py, verbatim.", "npcs": {}}

    if args.revert:
        for npc, saved in backup["npcs"].items():
            if args.only and npc not in args.only:
                continue
            for kind, entry in saved.items():
                section(data[kind], kind)[npc] = entry
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        print("reverted", sorted(n for n in backup["npcs"] if not args.only or n in args.only))
        return

    report = []
    for design, folder, registry in designs():
        npc = design["npc"]
        if args.only and npc not in args.only:
            continue
        for kind in FILES:
            if npc not in section(data[kind], kind):
                raise SystemExit("unknown NPC %s in %s" % (npc, kind))
        current = {k: section(data[k], k)[npc] for k in FILES}
        img, geo = geometry(design["source"], design["sha256"], design["head"], design["avatar"], folder, registry)
        name = "room13-redesign-%s.webp" % npc
        poses = {}
        pose_images = {}
        for key, spec in design.get("poses", {}).items():
            pimg, pgeo = geometry(spec["source"], spec["sha256"], spec["head"], None, folder, registry)
            pname = "room13-redesign-%s-%s.webp" % (npc, key)
            poses[key] = ("assets/" + pname, pgeo, spec)
            pose_images[pname] = pimg
        # The name is the game's original one (from before any redesign).
        name_ko = backup["npcs"].get(npc, current)["fullbody"]["name_ko"]
        new = entries(design, geo, "assets/" + name, name_ko, poses)
        already = all(current[k] == new[k] for k in FILES)
        if args.check:
            report.append((npc, "applied" if already else "NOT applied", geo))
            continue
        if npc not in backup["npcs"]:
            if any(e.get("redesign") for e in current["cast"].values()):
                raise SystemExit("no original backup for already-redesigned " + npc)
            backup["npcs"][npc] = current
        encode_webp(img, name)
        for pname, pimg in pose_images.items():
            encode_webp(pimg, pname)
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
