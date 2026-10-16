"""Apply the 2026-10-16 episode art (characters, icons, backgrounds, picture books, overlays).

    python3 dev/apply_ep_art.py            # write game assets + json entries (idempotent)
    python3 dev/apply_ep_art.py --check    # report only

Registry: art/ep-art-20261016/registry.json. Originals (lossless WebP, never
modified) are in art/ep-art-20261016/originals/, derived pictures (the crayon
nose patch, overlay cut-outs) in derived/. sources.json keeps each original's
PNG SHA-256 and the delivery it came from.

Characters
  - Each picture is halved (premultiplied Lanczos, the same as the 43-character
    full-body set and dev/apply_npc_redesign.py) to 512x768, WebP q95 with
    lossless alpha (dev/import_art.py).
  - One crop per character covers every expression, so an expression change never
    moves the body. Missing expressions point at the neutral file (no copies).
  - Poses get their own file and crop under fullbody["poses"] and an acting entry
    with the same name, so a line with {"pose": "door_peek"} shows that picture
    in dialogue (room13_fullbody_dialogue.rpy) and on the map.
  - mode "new": cast.json / acting / portraits / fullbody entries are created.
    mode "replace": the same entries are rewritten; the old ones are saved once to
    art/ep-art-20261016/original-entries.json (like the 2026-10-15 redesign).
    mode "poses": only poses are added; the character's expressions stay.
Icons: 300x300 (contain-fit, premultiplied area resample) + room13-evidence-icons.json.
Backgrounds, picture books and overlays: written at their final size; the
scene keys and hooks that show them are in game/systems/room13_ep_art.rpy.
"""
import argparse, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ASSETS = GAME / "assets"
ART = ROOT / "art/ep-art-20261016"
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

FILES = {
    "cast": ASSETS / "cast.json",
    "acting": ASSETS / "room13-pixel-acting.json",
    "portraits": ASSETS / "room13-portraits.json",
    "fullbody": ASSETS / "room13-fullbody-dialogue.json",
    "icons": ASSETS / "room13-evidence-icons.json",
}
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")
BODY_STATES = ("neutral", "thinking", "distressed", "expressive")
ALPHA_VISIBLE, MARGIN, AVATAR = 32, 4, 384


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def indent_of(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("{\n"):
        return None
    second = text.split("\n", 2)[1]
    return len(second) - len(second.lstrip(" "))


def dump(path, data, indent):
    end = "\n" if not path.exists() or path.read_text(encoding="utf-8").endswith("\n") else ""
    path.write_text(json.dumps(data, ensure_ascii=False, indent=indent) + end, encoding="utf-8")


def source(name):
    for sub in ("originals", "derived"):
        p = ART / sub / (name + ".webp")
        if p.exists():
            im = Image.open(p)
            im.load()
            return im.convert("RGBA")
    raise SystemExit("missing original: " + name)


def resample(img, size):
    return img.convert("RGBa").resize(size, Image.LANCZOS).convert("RGBA")


def half(img):
    return resample(img, (img.width // 2, img.height // 2))


def write(img, name, check, lossless=False):
    if not check:
        buf = io.BytesIO()
        img.save(buf, "PNG")
        (ASSETS / name).write_bytes(encode(io.BytesIO(buf.getvalue()), lossless))
    return "assets/" + name


def extent(img):
    alpha = np.asarray(img)[..., 3] >= ALPHA_VISIBLE
    ys, xs = np.where(alpha.any(1))[0], np.where(alpha.any(0))[0]
    return alpha, int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def box_with_margin(x0, y0, x1, y1, size):
    x0, y0 = max(0, x0 - MARGIN), max(0, y0 - MARGIN)
    x1, y1 = min(size[0], x1 + MARGIN), min(size[1], y1 + MARGIN)
    return [x0, y0, x1 - x0, y1 - y0]


def body_geometry(img, crop, head_ratio):
    """Foot and head inside `crop` (the redesign tool's rules)."""
    alpha, fx0, fy0, fx1, fy1 = extent(img)
    bottom = fy1 - 1
    window = max(8, int(0.04 * (fy1 - fy0)))
    feet = np.where(alpha[max(0, bottom - window):bottom + 1].any(0))[0]
    foot = [int((feet.min() + feet.max() + 1) // 2) - crop[0], bottom + 1 - crop[1]]
    hy1 = fy0 + max(8, int(head_ratio * (fy1 - fy0)))
    cols = np.where(alpha[fy0:hy1].any(0))[0]
    head = [int(cols.min()) - crop[0], fy0 - crop[1], int(cols.max() - cols.min()) + 1, hy1 - fy0]
    return foot, head, [fx0, fy0, fx1 - fx0, fy1 - fy0]


def character(cid, spec, check):
    neutral = half(source(spec["emotions"]["neutral"]))
    pictures = {e: (neutral if e == "neutral" else half(source(n))) for e, n in spec["emotions"].items()}
    boxes = [extent(p)[1:] for p in pictures.values()]
    x0, y0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    x1, y1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    crop = box_with_margin(x0, y0, x1, y1, neutral.size)
    figure = [x0, y0, x1 - x0, y1 - y0]
    # "replace" keeps the old files untouched (old saves, original-entries.json); "poses" adds
    # pose pictures only and never rewrites the character's expression files.
    stem = "room13-epart-%s-%s.webp" if spec["mode"] == "replace" else "room13-fullbody-%s-%s.webp"
    files = {e: ("" if spec["mode"] == "poses" else write(p, stem % (cid, e), check)) for e, p in pictures.items()}
    images = {e: {"file": files.get(e, files["neutral"]), "size": list(neutral.size), "art": "ep-art-20261016"} for e in EMOTIONS}
    foot, head, _ = body_geometry(neutral, crop, spec.get("head_ratio", 0.3))
    poses = {}
    for pose, name in spec.get("poses", {}).items():
        img = half(source(name))
        _, px0, py0, px1, py1 = extent(img)
        pcrop = box_with_margin(px0, py0, px1, py1, img.size)
        pfoot, phead, pfig = body_geometry(img, pcrop, spec.get("head_ratio", 0.3))
        poses[pose] = dict(file=write(img, "room13-fullbody-%s-pose-%s.webp" % (cid, pose), check), size=list(img.size),
                           crop=pcrop, figure=pfig, foot=pfoot, head=phead)
    if spec.get("face"):
        avatar_file = write(resample(source(spec["face"]), (AVATAR, AVATAR)), "room13-face-%s.webp" % cid, check)
        avatar_crop = [0, 0, AVATAR, AVATAR]
    else:
        hx, hy, hw, hh = head
        side = max(hw, hh) + 16
        cx, cy = crop[0] + hx + hw // 2, crop[1] + hy + hh // 2
        ax0 = int(min(max(0, cx - side // 2), neutral.width - side))
        ay0 = int(min(max(0, cy - side // 2), neutral.height - side))
        avatar_file, avatar_crop = files["neutral"], [ax0, ay0, side, side]
    return dict(crop=crop, figure=figure, images=images, poses=poses, foot=foot, head=head,
                file=files["neutral"], avatar_file=avatar_file, avatar_crop=avatar_crop)


def pose_entries(cid, spec, geo):
    """Fullbody pose entries; "fit" < 1 zooms the pose out so a low prop (bowl, book,
    the three pieces) stays above the dialogue panel (registry pose_fit)."""
    fits = REGISTRY_FIT.get(cid, {})
    return {k: dict({key: v[key] for key in ("file", "size", "crop", "figure")}, **({"fit": fits[k]} if k in fits else {}))
            for k, v in geo["poses"].items()}


REGISTRY_FIT = {}


def entries(cid, spec, geo):
    tag = "ep-art-20261016"
    body = {"file": geo["file"], "crop": geo["crop"], "nearest": True, "foot": geo["foot"], "facing": "front",
            "contact": "standing", "head": geo["head"], "reviewed": True, "posture": "standing", "art": tag}
    avatar = {"file": geo["avatar_file"], "crop": geo["avatar_crop"], "nearest": True, "dedicated_avatar": True,
              "facing": "front", "gaze": "viewer", "art": tag}
    portrait = {"file": geo["file"], "crop": geo["crop"], "head": geo["head"], "full_body": True, "nearest": True,
                "facing": "front", "gaze": "viewer", "art": tag}
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
    acting = {state: dict(body) for state in BODY_STATES}
    for state in BODY_STATES:
        acting["avatar_" + state] = {"file": geo["avatar_file"], "crop": geo["avatar_crop"]}
    acting.update(pose_acting(geo["poses"]))
    portraits = {state: dict(portrait) for state in BODY_STATES}
    fullbody = {"name_ko": spec["name_ko"], "crop": geo["crop"], "figure": geo["figure"], "images": geo["images"], "art": tag}
    if geo["poses"]:
        fullbody["poses"] = pose_entries(cid, spec, geo)
    return dict(cast=cast, acting=acting, portraits=portraits, fullbody=fullbody)


def pose_acting(poses):
    return {k: {"file": v["file"], "crop": v["crop"], "nearest": True, "foot": v["foot"], "facing": "front",
                "contact": "standing", "head": v["head"], "reviewed": True, "posture": "standing",
                "art": "ep-art-20261016"} for k, v in poses.items()}


def section(data, kind):
    return data["people"] if kind == "fullbody" else data


def fit_square(img, side):
    _, x0, y0, x1, y1 = extent(img)
    img = img.crop((x0, y0, x1, y1))
    s = side / max(img.width, img.height)
    img = resample(img, (max(1, round(img.width * s)), max(1, round(img.height * s))))
    out = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    out.alpha_composite(img, ((side - img.width) // 2, (side - img.height) // 2))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    reg = load(ART / "registry.json")
    REGISTRY_FIT.update(reg.get("pose_fit", {}))
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    backup_path = ART / "original-entries.json"
    backup = load(backup_path) if backup_path.exists() else {"note": "Entries replaced by dev/apply_ep_art.py, verbatim.", "people": {}}
    report = []

    for cid, spec in reg["characters"].items():
        geo = character(cid, spec, args.check)
        mode = spec["mode"]
        if mode == "poses":
            entry = section(data["fullbody"], "fullbody")[cid]
            entry["poses"] = pose_entries(cid, spec, geo)
            data["acting"].setdefault(cid, {}).update(pose_acting(geo["poses"]))
            report.append((cid, "poses " + ",".join(geo["poses"])))
            continue
        new = entries(cid, spec, geo)
        kinds = ("cast", "acting", "portraits", "fullbody")
        if mode == "replace" and cid not in backup["people"]:
            backup["people"][cid] = {k: section(data[k], k)[cid] for k in kinds}
        for kind in kinds:
            section(data[kind], kind)[cid] = new[kind]
        report.append((cid, "%s crop %s poses %s" % (mode, geo["crop"], ",".join(geo["poses"]) or "-")))

    for key in reg["icons"]:
        name = "room13-ep-icon-%s.webp" % key
        write(fit_square(source("ep-icon-" + key), 300), name, args.check)
        data["icons"][key] = {"key": key, "file": "assets/" + name, "crop": [0, 0, 300, 300], "nearest": True, "art": "ep-art-20261016"}
    report.append(("icons", len(reg["icons"])))

    for out, spec in reg["pictures"].items():
        img = source(spec["source"])
        if spec.get("pad") and img.height == spec["size"][1] and 0 < spec["size"][0] - img.width <= 2:
            # 2171 -> 2172: repeat the last column instead of stretching the picture.
            padded = Image.new("RGBA", tuple(spec["size"]))
            padded.paste(img, (0, 0))
            edge = img.crop((img.width - 1, 0, img.width, img.height))
            for x in range(img.width, spec["size"][0]):
                padded.paste(edge, (x, 0))
            img = padded
        if spec.get("size") and list(img.size) != spec["size"]:
            w, h = spec["size"]
            if abs(img.width / img.height - w / h) > 0.01:
                raise SystemExit("aspect mismatch " + out)
            img = resample(img, (w, h))
        if np.asarray(img)[..., 3].min() == 255:
            img = img.convert("RGB")
        write(img, out, args.check, spec.get("lossless", False))
    report.append(("pictures", len(reg["pictures"])))

    if not args.check:
        dump(backup_path, backup, 1)
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
    for row in report:
        print(*row)


if __name__ == "__main__":
    main()
