"""TEST ONLY (branch claude/rev13-appearance-test): apply the board revision13 selection.

    python3 dev/apply_rev13_test.py            # apply (idempotent)
    python3 dev/apply_rev13_test.py --revert   # restore every replaced entry (rollback)
    python3 dev/apply_rev13_test.py --check    # verify, change nothing

Registry: art/rev13-test-20261016/rev13.json (31 source PNGs, byte-exact, SHA-256 checked).
Derived from dev/apply_npc_redesign.py; only art data changes. IDs, names, dialogue, clues,
evidence, unlocks, schedules and time costs are untouched.

Per design ("apply"):
  incoming          new species/look: every body state, avatar, portrait and the six dialogue
                    expressions use the one image; the old design's activity, life and event
                    poses are dropped (the person stands in the new design instead of showing
                    the old body); the old round-table seated picture is dropped (stands at the
                    table); the old eye-blink pieces are dropped.
  selected          same character line (remodel / face revision): standing, dialogue, avatar and
                    portrait use the image; existing activity/life/event poses are kept only when
                    drawn in the new body proportions (consistent_pose: head share within 35%,
                    stature_ratio respected, never stretched); the old chibi sheets are dropped
                    and the person stands instead; seated pictures are kept; blink pieces dropped.
  life_action_only  설이 bellrope-v1: nothing changes (it is a life action, not a dialogue default).
  gallery_only      the 3 new designs: game/assets/room13-rev13-gallery-*.webp + gallery json,
                    shown only on the test gallery screen, no gameId, schedule or story.
Everything replaced is saved first to art/rev13-test-20261016/original-entries.json (per person)
and the six data files as a whole to art/rev13-test-20261016/original-files/ (byte-exact
rollback with --revert).
"""
import argparse, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ART = ROOT / "art/rev13-test-20261016"
REGISTRY = ART / "rev13.json"
BACKUP = ART / "original-entries.json"
sys.path.insert(0, str(ROOT / "dev"))

FILES = {
    "cast": GAME / "assets/cast.json",
    "acting": GAME / "assets/room13-pixel-acting.json",
    "portraits": GAME / "assets/room13-portraits.json",
    "fullbody": GAME / "assets/room13-fullbody-dialogue.json",
    "seated": GAME / "assets/room13-meeting-seated.json",
    "dotfx": GAME / "assets/room13-dot-fx.json",
}
GALLERY = GAME / "assets/room13-rev13-gallery.json"
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
    # Both feet: the lowest 4% of the figure (a stance with one boot lower
    # than the other would otherwise anchor on that single boot).
    window = max(8, int(0.04 * figure[3]))
    feet = np.where(alpha[max(0, bottom - window):bottom + 1].any(0))[0]
    foot = [int((feet.min() + feet.max() + 1) // 2) - crop[0], bottom + 1 - crop[1]]
    hx, hy, hw, hh = scaled_box(design["head"], scale, img.size)
    head = [hx - crop[0], hy - crop[1], hw, hh]
    head = [max(0, head[0]), max(0, head[1]), min(hw, crop[2] - max(0, head[0])), min(hh, crop[3] - max(0, head[1]))]
    avatar = scaled_box(design["avatar"], scale, img.size)
    return img, dict(crop=crop, figure=figure, foot=foot, head=head, avatar=avatar)


def entries(npc, design, geo, file):
    body = {"file": file, "crop": geo["crop"], "nearest": True, "foot": geo["foot"], "facing": "front",
            "contact": "standing", "head": geo["head"], "reviewed": True, "posture": "standing",
            "rev13_test": design["design_id"]}
    avatar = {"file": file, "crop": geo["avatar"], "nearest": True, "dedicated_avatar": True,
              "facing": "front", "gaze": "viewer", "rev13_test": design["design_id"]}
    portrait = {"file": file, "crop": geo["crop"], "head": geo["head"], "full_body": True, "nearest": True,
                "facing": "front", "gaze": "viewer", "rev13_test": design["design_id"]}
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
                "rev13_test": design["design_id"]}
    return dict(cast=cast, acting=acting, portraits=portraits, fullbody=fullbody)


def section(data, kind):
    if kind == "fullbody":
        return data["people"]
    if kind == "dotfx":
        return data.setdefault("blink", {}).setdefault("people", {})
    return data


MISSING = "__absent__"
BODY_KEYS = set(BODY_STATES) | {"interview_" + s for s in BODY_STATES} | {"avatar_" + s for s in BODY_STATES} \
    | {"portrait_" + s for s in BODY_STATES} | {"world"}


def consistent_pose(spec, neutral):
    """A kept pose must share the new standing figure's head-to-height proportion (within 35%).
    For map-action art the pose height is stature_ratio x standing height, so its expected head
    share is neutral_share / stature_ratio. The old chibi sheets (head ~0.43-0.61 of the height
    against ~0.2-0.3 in the selected art) fail this and are dropped."""
    import math
    if not spec.get("head") or not neutral.get("head"):
        return False
    share = spec["head"][3] / float(spec.get("foot", [0, spec["crop"][3]])[1])
    base = neutral["head"][3] / float(neutral["foot"][1])
    expected = base / float(spec.get("stature_ratio", 1.0))
    return abs(math.log(share / expected)) < math.log(1.35)


def merged(kind, old, new, mode):
    """The entry written for one person (None = remove the entry)."""
    if kind in ("portraits", "fullbody"):
        return new
    if kind == "seated":
        return None if mode == "incoming" else old
    if kind == "dotfx":
        return None
    if mode == "incoming":
        return new
    # selected: keep the existing non-standing poses of the same character line, but only those
    # drawn in the new body proportions (see consistent_pose); the rest would show the old body.
    out = dict(old or {})
    for key, value in new.items():
        if kind == "cast" and key not in BODY_KEYS and key in out:
            continue  # keep the existing activity / inn_activity / avatar_activity
        out[key] = value
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--revert", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    registry = load(REGISTRY)
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    backup = load(BACKUP) if BACKUP.exists() else {"note": "Entries replaced by dev/apply_rev13_test.py, verbatim ('__absent__' = did not exist).", "npcs": {}}

    originals = ART / "original-files"
    if args.revert:
        if originals.exists():
            # byte-exact rollback of the six data files as they were before the first apply
            for kind, path in FILES.items():
                saved_file = originals / path.name
                if saved_file.exists():
                    path.write_bytes(saved_file.read_bytes())
            for d in registry["designs"]:
                if d.get("npc") and d["apply"] in ("incoming", "selected"):
                    (GAME / "assets" / ("room13-rev13-%s.webp" % d["npc"])).unlink(missing_ok=True)
            if GALLERY.exists():
                for g in load(GALLERY)["designs"]:
                    (GAME / g["file"]).unlink(missing_ok=True)
                GALLERY.unlink()
            print("reverted (byte-exact)", sorted(backup["npcs"]))
            return
        for npc, saved in backup["npcs"].items():
            for kind, entry in saved.items():
                sec = section(data[kind], kind)
                if entry == MISSING:
                    sec.pop(npc, None)
                else:
                    sec[npc] = entry
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        for d in registry["designs"]:
            if d.get("npc") and d["apply"] in ("incoming", "selected"):
                (GAME / "assets" / ("room13-rev13-%s.webp" % d["npc"])).unlink(missing_ok=True)
        if GALLERY.exists():
            for g in load(GALLERY)["designs"]:
                (GAME / g["file"]).unlink(missing_ok=True)
            GALLERY.unlink()
        if BACKUP.exists():
            BACKUP.unlink()
        print("reverted", sorted(backup["npcs"]))
        return

    if not args.check and not originals.exists():
        originals.mkdir()
        for kind, path in FILES.items():
            (originals / path.name).write_bytes(path.read_bytes())
    from import_art import encode
    report = []
    gallery = {"note": "TEST ONLY: board revision13 new designs, no gameId/schedule/story.", "designs": []}
    for design in registry["designs"]:
        mode, npc = design["apply"], design.get("npc")
        if mode == "life_action_only":
            gallery.setdefault("unchanged", []).append({"npc": npc, "mode": mode, "design_id": design["design_id"], "name_ko": design["name_ko"]})
            report.append((design["name_ko"], "unchanged (life action only)", None))
            continue
        img, geo = geometry(design, registry)
        geo["size"] = img.size
        if mode == "gallery_only":
            name = "room13-rev13-gallery-%s.webp" % design["design_id"]
            if not args.check:
                buf = io.BytesIO(); img.save(buf, "PNG")
                (GAME / "assets" / name).write_bytes(encode(io.BytesIO(buf.getvalue())))
            gallery["designs"].append({"name_ko": design["name_ko"], "design_id": design["design_id"], "file": "assets/" + name,
                                       "crop": geo["crop"], "foot": geo["foot"], "head": geo["head"], "source_sha256": design["sha256"]})
            report.append((design["name_ko"], "gallery", geo))
            continue
        for kind in ("cast", "acting", "portraits", "fullbody"):
            if npc not in section(data[kind], kind):
                raise SystemExit("unknown NPC %s in %s" % (npc, kind))
        name = "room13-rev13-%s.webp" % npc
        file = "assets/" + name
        new = entries(npc, design, geo, file)
        if npc not in backup["npcs"]:
            backup["npcs"][npc] = {k: section(data[k], k).get(npc, MISSING) for k in FILES}
        saved = backup["npcs"][npc]
        target = {}
        for kind in FILES:
            old = saved[kind] if saved[kind] != MISSING else None
            target[kind] = merged(kind, old, new.get(kind), mode)
        dropped = []
        if mode == "selected":
            neutral = target["acting"]["neutral"]
            for key in [k for k in target["acting"] if k not in BODY_STATES and not k.startswith("avatar_")]:
                if not consistent_pose(target["acting"][key], neutral):
                    dropped.append(key)
                    del target["acting"][key]
            if "activity" in dropped:
                for key in ("activity", "inn_activity"):
                    if key in target["cast"]:
                        target["cast"][key] = dict(new["cast"]["neutral"])
                if "avatar_activity" in target["cast"]:
                    target["cast"]["avatar_activity"] = dict(new["cast"]["avatar_neutral"])
        current = {k: section(data[k], k).get(npc) for k in FILES}
        if args.check:
            report.append((npc, "applied" if current == target else "NOT applied", geo))
            continue
        buf = io.BytesIO()
        img.save(buf, "PNG")
        (GAME / "assets" / name).write_bytes(encode(io.BytesIO(buf.getvalue())))
        for kind in FILES:
            sec = section(data[kind], kind)
            if target[kind] is None:
                sec.pop(npc, None)
            else:
                sec[npc] = target[kind]
        kept = sorted(k for k in target["acting"] if k not in BODY_STATES and not k.startswith("avatar_"))
        gallery.setdefault("applied", []).append({"npc": npc, "mode": mode, "design_id": design["design_id"], "name_ko": design["name_ko"],
                                                  "kept_poses": kept, "dropped_poses": sorted(dropped) if mode == "selected" else
                                                  sorted(k for k in (saved["acting"] if saved["acting"] != MISSING else {}) if k not in BODY_STATES and not k.startswith("avatar_"))})
        report.append((npc, "applied " + mode, geo))

    if not args.check:
        dump(BACKUP, backup, 1)
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        GALLERY.write_text(json.dumps(gallery, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for npc, state, geo in report:
        print(npc, state, "" if geo is None else ("size %s crop %s foot %s head %s" % (tuple(geo["size"]), geo["crop"], geo["foot"], geo["head"])))


if __name__ == "__main__":
    main()
