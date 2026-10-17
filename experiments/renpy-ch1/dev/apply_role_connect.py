"""Connect approved / canonical designs to their roles in every art channel (0.18.99).

    python3 dev/apply_role_connect.py            # apply (idempotent)
    python3 dev/apply_role_connect.py --check    # report what would change
    python3 dev/apply_role_connect.py --revert   # restore the saved entries

Registry: art/role-connect-20261016/registry.json (owner approvals 2026-10-16 20:24 / 20:26 PDT).
Only art data changes. IDs, names, dialogue, schedules, evidence and unlocks are untouched.

Channels per role: dialogue full body (room13-fullbody-dialogue.json), world / investigation
standing poses and record avatars (room13-pixel-acting.json, cast.json), profile busts
(room13-portraits.json), meeting seats (room13-meeting-seated.json: old-design seat pictures are
taken out; the meeting then uses the standing picture), eye blink pieces (room13-dot-fx.json:
old faces' pieces are taken out).

Modes
  pixel_set / pixel_single  approved pictures drawn in exact 2x2 cells (부리 v7 six faces, 솔방울,
      굴돌). Stored with their own pixels (lossless WebP). The dialogue entry maps the file onto
      itself (map [1,0,0], cell 2) so the renderer draws whole screen pixels per cell. The world
      standing picture is the neutral file itself.
  canon   the confirmed 48-role originals (art/canonical48-rev45/originals): world / dialogue
      picture at 0.5 scale (same import as dev/apply_npc_redesign.py), one picture for all six
      expressions until expressions are drawn.
  dialogue_neutral   same design, one fixed picture (돌목 mouth fix): only the dialogue neutral is
      replaced (registered on the current neutral so the size class stays); other expressions and
      all world poses stay.
Poses of the old design (living_*, action_*, event_*, sheet activity poses) are removed: the
person stands in the new design until new poses are drawn. Map-action poses drawn for the new
design (dev/apply_map_actions.py registry, not withdrawn / held) are kept.
Everything replaced is saved once to art/role-connect-20261016/original-entries.json.
"""
import argparse, copy, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ASSETS = GAME / "assets"
ART = ROOT / "art/role-connect-20261016"
REGISTRY = ART / "registry.json"
BACKUP = ART / "original-entries.json"
MAP_ACTIONS = ROOT / "art/map-actions-20261015/registry.json"
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

FILES = {
    "cast": ASSETS / "cast.json",
    "acting": ASSETS / "room13-pixel-acting.json",
    "portraits": ASSETS / "room13-portraits.json",
    "fullbody": ASSETS / "room13-fullbody-dialogue.json",
    "meeting": ASSETS / "room13-meeting-seated.json",
    "dotfx": ASSETS / "room13-dot-fx.json",
}
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")
BODY_STATES = ("neutral", "thinking", "distressed", "expressive")


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def indent_of(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("{\n"):
        return None
    second = text.split("\n", 2)[1]
    return len(second) - len(second.lstrip(" "))


def dump(path, data, indent):
    end = "\n" if path.read_text(encoding="utf-8").endswith("\n") else ""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + end, encoding="utf-8")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def write_webp(img, name, lossless, check):
    if not check:
        buf = io.BytesIO()
        img.save(buf, "PNG")
        (ASSETS / name).write_bytes(encode(io.BytesIO(buf.getvalue()), lossless=lossless))
    return "assets/" + name


def even_down(v):
    return (int(v) // 2) * 2


def geometry(img, margin, cell):
    """Crop / figure / foot / head / avatar in file pixels. With cell 2 every box starts and
    ends on even pixels so the 2x2 cells stay whole."""
    a = np.asarray(img)[..., 3] >= 32
    ys, xs = np.where(a.any(1))[0], np.where(a.any(0))[0]
    x0, y0 = max(0, int(xs.min()) - margin), max(0, int(ys.min()) - margin)
    x1, y1 = min(img.width, int(xs.max()) + 1 + margin), min(img.height, int(ys.max()) + 1 + margin)
    if cell == 2:
        x0, y0 = even_down(x0), even_down(y0)
        x1, y1 = min(img.width, -(-x1 // 2) * 2), min(img.height, -(-y1 // 2) * 2)
    crop = [x0, y0, x1 - x0, y1 - y0]
    top, bottom = int(ys.min()), int(ys.max())
    figure = [int(xs.min()), top, int(xs.max()) + 1 - int(xs.min()), bottom + 1 - top]
    window = max(4, int(0.04 * figure[3]))
    feet = np.where(a[max(0, bottom - window):bottom + 1].any(0))[0]
    foot = [int((feet.min() + feet.max() + 1) // 2) - x0, bottom + 1 - y0]
    # Head: the top 28% of the figure, as wide as the picture is there (ears and hair included).
    hh = max(8, int(0.28 * figure[3]))
    band = np.where(a[top:top + hh].any(0))[0]
    hx0, hx1 = int(band.min()), int(band.max()) + 1
    head = [hx0 - x0, top - y0, hx1 - hx0, hh]
    side = int(max(hx1 - hx0, hh) * 1.05)
    cx = (hx0 + hx1) // 2
    ax, ay = max(0, cx - side // 2), max(0, top - int(0.03 * side))
    side = min(side, img.width - ax, img.height - ay)
    avatar = [ax, ay, side, side]
    return dict(crop=crop, figure=figure, foot=foot, head=head, avatar=avatar)


def world_entries(file, geo, version):
    body = {"file": file, "crop": geo["crop"], "nearest": True, "foot": geo["foot"], "facing": "front",
            "contact": "standing", "head": geo["head"], "reviewed": True, "posture": "standing", "role_connect": version}
    avatar = {"file": file, "crop": geo["avatar"], "nearest": True, "dedicated_avatar": True,
              "facing": "front", "gaze": "viewer", "role_connect": version}
    portrait = {"file": file, "crop": geo["crop"], "head": geo["head"], "full_body": True, "nearest": True,
                "facing": "front", "gaze": "viewer", "role_connect": version}
    cast = {}
    for state in BODY_STATES:
        cast[state] = dict(body)
        cast["interview_" + state] = dict(body)
        cast["avatar_" + state] = dict(avatar)
        cast["portrait_" + state] = dict(portrait)
    for state in ("world", "activity", "inn_activity"):
        cast[state] = dict(body)
    cast["avatar_activity"] = dict(avatar)
    acting = {}
    for state in BODY_STATES:
        acting[state] = dict(body)
        acting["avatar_" + state] = {"file": file, "crop": geo["avatar"]}
    portraits = {state: dict(portrait) for state in BODY_STATES}
    return cast, acting, portraits


def pixel_fullbody(name_ko, images, version):
    """images: {emotion: (file, PIL image, sha)}; maps each file onto itself (cell 2)."""
    out, boxes = {}, []
    for e, (file, img, digest) in images.items():
        g = geometry(img, 2, 2)
        out[e] = {"file": file, "size": list(img.size), "crop": g["crop"], "map": [1.0, 0.0, 0.0], "cell": 2,
                  "source_sha256": digest}
        fx, fy, fw, fh = g["figure"]
        boxes.append((fx, fy, fx + fw, fy + fh, img.size))
    W = max(b[4][0] for b in boxes)
    H = max(b[4][1] for b in boxes)
    fx0, fy0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    fx1, fy1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    crop = [max(0, fx0 - 4), max(0, fy0 - 4)]
    crop += [min(W, fx1 + 4) - crop[0], min(H, fy1 + 4) - crop[1]]
    return {"name_ko": name_ko, "crop": crop, "figure": [fx0, fy0, fx1 - fx0, fy1 - fy0], "images": out,
            "pixel": {"u": 1.0, "cell": 2}, "role_connect": version}


def canon_fullbody(name_ko, file, img, geo, digest, version):
    images = {e: {"file": file, "size": list(img.size), "source_sha256": digest} for e in EMOTIONS}
    return {"name_ko": name_ko, "crop": geo["crop"], "figure": geo["figure"], "images": images, "role_connect": version}


def kept_map_actions(person, current):
    """Map-action poses drawn for the new design (registry entries not withdrawn / held)."""
    reg = load(MAP_ACTIONS)
    live = {(e["person"], e["pose"], e["sha256"]) for e in reg["poses"] if not (e.get("withdrawn") or e.get("hold"))}
    return {k: v for k, v in current.items()
            if v.get("map_action") and (person, k, v.get("source_sha256")) in live}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    reg = load(REGISTRY)
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    people = data["fullbody"]["people"]
    blink = data["dotfx"].setdefault("blink", {}).setdefault("people", {})
    backup = load(BACKUP) if BACKUP.exists() else {"note": "Entries replaced by dev/apply_role_connect.py, verbatim (null = absent).", "roles": {}}

    def current(rid):
        return {"cast": data["cast"].get(rid), "acting": data["acting"].get(rid), "portraits": data["portraits"].get(rid),
                "fullbody": people.get(rid), "meeting": data["meeting"].get(rid), "blink": blink.get(rid)}

    def put(rid, saved):
        for kind, table in (("cast", data["cast"]), ("acting", data["acting"]), ("portraits", data["portraits"]),
                            ("fullbody", people), ("meeting", data["meeting"]), ("blink", blink)):
            if saved[kind] is None:
                table.pop(rid, None)
            else:
                table[rid] = saved[kind]

    if a.revert:
        for rid, saved in backup["roles"].items():
            put(rid, saved)
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        print("reverted", sorted(backup["roles"]))
        return

    report = []
    for rid, spec in reg["roles"].items():
        if rid not in backup["roles"]:
            backup["roles"][rid] = copy.deepcopy(current(rid))
        orig = backup["roles"][rid]
        version = spec["version"]
        if spec["mode"] == "dialogue_neutral":
            new = copy.deepcopy(orig)
            src = ART / spec["source"]
            if sha(src) != spec["sha256"]:
                raise SystemExit("hash mismatch " + str(src))
            img = Image.open(src).convert("RGBA")
            file = write_webp(img, "room13-role-%s-neutral.webp" % rid, True, a.check)
            from apply_expression_acting import register, ref_box, file_crop
            ref = Image.open(GAME / orig["fullbody"]["images"]["neutral"]["file"]).convert("RGBA")
            iou, u, ox, oy = register(ref, img)
            fb = new["fullbody"]
            fb["images"]["neutral"] = {"file": file, "size": list(img.size), "crop": file_crop(img),
                                       "map": [round(u, 5), float(ox), float(oy)], "cell": 2,
                                       "source_sha256": spec["sha256"], "role_connect": version}
            boxes = [ref_box(fb["images"][e], img if e == "neutral" else Image.open(GAME / fb["images"][e]["file"]).convert("RGBA"))
                     for e in EMOTIONS]
            fx0, fy0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
            fx1, fy1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
            W, H = ref.size
            crop = [max(0, int(np.floor(fx0)) - 4), max(0, int(np.floor(fy0)) - 4)]
            crop += [min(W, int(np.ceil(fx1)) + 4) - crop[0], min(H, int(np.ceil(fy1)) + 4) - crop[1]]
            fb["crop"] = crop
            fb["figure"] = [int(np.floor(fx0)), int(np.floor(fy0)), int(np.ceil(fx1 - np.floor(fx0))), int(np.ceil(fy1 - np.floor(fy0)))]
            fb["pixel"] = {"u": round(u, 5), "cell": 2}
            fb["role_connect"] = version
            # same face: blink pieces of the old neutral are not this mouth/eyes picture
            if new["blink"] and "neutral" in new["blink"]:
                new["blink"] = {k: v for k, v in new["blink"].items() if k != "neutral"} or None
            report.append((rid, "dialogue neutral", "overlap %.3f u %.4f" % (iou, u)))
        else:
            if spec["mode"] == "canon":
                src = ART / spec["source"]
                if sha(src) != spec["sha256"]:
                    raise SystemExit("hash mismatch " + str(src))
                from apply_npc_redesign import resample
                img = resample(Image.open(src).convert("RGBA"), reg["scale_from_source"])
                file = write_webp(img, "room13-role-%s.webp" % rid, False, a.check)
                geo = geometry(img, reg["margin"], 1)
                fb = canon_fullbody(spec["name_ko"], file, img, geo, spec["sha256"], version)
            else:
                faces = {}
                sources = spec["dialogue"] if spec["mode"] == "pixel_set" else {"neutral": {"source": spec["source"], "sha256": spec["sha256"]}}
                for e, s in sources.items():
                    src = ART / s["source"]
                    if sha(src) != s["sha256"]:
                        raise SystemExit("hash mismatch " + str(src))
                    img = Image.open(src).convert("RGBA")
                    file = write_webp(img, "room13-role-%s-%s.webp" % (rid, e), True, a.check)
                    faces[e] = (file, img, s["sha256"])
                fb = pixel_fullbody(spec["name_ko"], faces, version)
                for e in EMOTIONS:
                    if e not in fb["images"]:
                        fb["images"][e] = dict(fb["images"]["neutral"], fallback="neutral")
                file, img, _ = faces["neutral"]
                geo = geometry(img, 4, 2)
            cast, acting, portraits = world_entries(file, geo, version)
            now = data["acting"].get(rid) or {}
            acting.update(kept_map_actions(rid, now))
            if orig["fullbody"] and orig["fullbody"].get("name_ko"):
                fb["name_ko"] = orig["fullbody"]["name_ko"]
            new = {"cast": cast, "acting": acting, "portraits": portraits, "fullbody": fb, "meeting": None, "blink": None}
            dropped = sorted(k for k in (orig["acting"] or {}) if k not in acting and not k.startswith("avatar_"))
            report.append((rid, spec["mode"], "old poses dropped: %s%s%s" % (
                ", ".join(dropped) or "-", "; meeting seat removed" if orig["meeting"] else "",
                "; blink removed" if orig["blink"] else "")))
        if not a.check:
            put(rid, new)
    if not a.check:
        BACKUP.write_text(json.dumps(backup, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
    for r in report:
        print(*r)


if __name__ == "__main__":
    main()
