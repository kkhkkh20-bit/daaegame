"""Apply the 2026-10-16 dialogue expression package (owner 17:05 PDT): upper-body acting.

    python3 dev/apply_expression_acting.py            # apply (idempotent)
    python3 dev/apply_expression_acting.py --check    # report only, change nothing
    python3 dev/apply_expression_acting.py --revert   # byte-exact rollback of the data files

Sources (byte-exact, SHA-256 checked against the package map):
  art/expression-acting-20261016/pack68/<id>/<emotion>.png + current-selection-map.csv (68 PNG)
  art/expression-acting-20261016/second-fixes/  2nd art-fix delivery; its 10 lion/Neoul PNG are the
      same bytes as pack68 (checked) and are stored once.
Decisions per character: art/expression-acting-20261016/registry.json.

Dialogue full-body close-ups only. World sprites, meeting seats, profile avatars, story,
schedules and evidence are not touched. One key = one picture (the map's file).

Geometry (no resampling of the package pictures):
  - Each character keeps its present reference canvas (the current dialogue neutral), so the
    on-screen size class stays. A package picture is stored with its own pixels (lossless WebP)
    and a map [u, ox, oy]: file pixel (x, y) sits at reference (ox + u*x, oy + u*y).
  - u and the offset come from overlaying the package neutral on the current neutral (same
    character; scale search around the height ratio, then the best alpha overlap, feet first).
    Package pictures on the neutral's canvas size share its map (the package registered them);
    others are placed by canvas centre and lowest foot row in even package pixels, so 2x2 cells
    stay aligned and a crouch keeps its drawn height.
  - pixel pictures: entry["pixel"] = {"u": u, "cell": 2}; the renderer picks the character scale
    so one art cell is a whole number of screen pixels (room13_fullbody_dialogue.rpy).
  - Keys the package does not have keep the current game picture (same design: their neutral is
    the existing artwork re-registered), unless registry "package_only" says the package redraws
    the outfit; then the package neutral stands in, so one conversation never switches designs.
  - Lion teacher / Neoul: the new five are halved exactly (one sample per 2x2 cell). Neoul shares
    the neutral's canvas. The teacher's five are drawn ~9.5% smaller than the neutral, so they
    get a map with u = 1.095 placed by the legs (the neutral and world sprite are unchanged).
  - Authored poses keep their files and size; eye-blink pieces of replaced pictures are removed
    (they belong to the old faces; an automatic pixel-art blink was tried and looked wrong, so the
    new faces need hand-drawn half/shut eye pieces).
Everything replaced: art/expression-acting-20261016/original-files/ (whole data files) and
original-entries.json (entries); acting pictures are new files (room13-fullbody-*-acting.webp).
"""
import argparse, csv, hashlib, io, json, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ASSETS = GAME / "assets"
ART = ROOT / "art/expression-acting-20261016"
PACK = ART / "pack68"
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

FILES = {
    "fullbody": ASSETS / "room13-fullbody-dialogue.json",
    "dotfx": ASSETS / "room13-dot-fx.json",
}
EMOTIONS = ("neutral", "joy", "flustered", "angry", "anxious", "surprise")
MARGIN = 4
VISIBLE = 32


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


def floor_even(v):
    return (int(np.floor(v)) // 2) * 2


def ceil_even(v):
    return -((-int(np.ceil(v))) // 2) * 2


def alpha(img):
    return np.asarray(img.convert("RGBA"))[..., 3] >= VISIBLE


def bbox(a):
    ys, xs = np.where(a.any(1))[0], np.where(a.any(0))[0]
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def pack_rows():
    rows = list(csv.DictReader((PACK / "current-selection-map.csv").open(encoding="utf-8")))
    out = {}
    for r in rows:
        if hashlib.sha256((PACK / r["file"]).read_bytes()).hexdigest() != r["sha256"]:
            raise SystemExit("hash mismatch " + r["file"])
        key = (r["character"], r["expression"])
        if key in out:
            raise SystemExit("duplicate key %s" % (key,))
        out[key] = r
    return out


def write(img, name, check):
    if not check:
        buf = io.BytesIO()
        img.save(buf, "PNG")
        (ASSETS / name).write_bytes(encode(io.BytesIO(buf.getvalue()), lossless=True))
    return "assets/" + name


def scaled_alpha(img, u):
    w, h = max(1, round(img.width * u)), max(1, round(img.height * u))
    return alpha(img.resize((w, h), Image.NEAREST))


def place(target, s, ox, oy):
    """Scaled alpha s at (ox, oy) on target's canvas."""
    h, w = s.shape
    H, W = target.shape
    out = np.zeros_like(target)
    y0, y1, x0, x1 = max(0, oy), min(H, oy + h), max(0, ox), min(W, ox + w)
    if y1 > y0 and x1 > x0:
        out[y0:y1, x0:x1] = s[y0 - oy:y1 - oy, x0 - ox:x1 - ox]
    return out


def register(ref_img, img, band=None, u_range=None):
    """Map img -> ref: ref = (ox, oy) + u * img. Feet aligned, then best alpha overlap.
    band: only the lowest fraction of the figure counts (legs), for redrawn upper bodies."""
    ar = alpha(ref_img)
    rx0, ry0, rx1, ry1 = bbox(ar)
    ai = alpha(img)
    ix0, iy0, ix1, iy1 = bbox(ai)
    if band:
        cut = ry1 - int(band * (ry1 - ry0))
        ar = ar.copy()
        ar[:cut] = False
    u0 = (ry1 - ry0) / float(iy1 - iy0)
    us = u_range or np.arange(u0 * 0.96, u0 * 1.0401, u0 * 0.004)
    best = (-1, 0, 0, 0)
    for u in us:
        sa = scaled_alpha(img, u)
        oy0 = int(round(ry1 - iy1 * u))
        ox0 = int(round((rx0 + rx1) / 2.0 - (ix0 + ix1) / 2.0 * u))
        for dy in range(-6, 7, 2):
            for dx in range(-30, 31, 2):
                m = place(ar, sa, ox0 + dx, oy0 + dy)
                if band:
                    m[:cut] = False
                iou = (m & ar).sum() / max(1, (m | ar).sum())
                if iou > best[0]:
                    best = (iou, float(u), ox0 + dx, oy0 + dy)
    return best


def file_crop(img):
    x0, y0, x1, y1 = bbox(alpha(img))
    return [floor_even(x0 - 2), floor_even(y0 - 2), min(img.width, ceil_even(x1 + 2)) - floor_even(x0 - 2),
            min(img.height, ceil_even(y1 + 2)) - floor_even(y0 - 2)]


def ref_box(entry_img, img):
    """Visible box of an image in reference pixels."""
    x0, y0, x1, y1 = bbox(alpha(img))
    m = entry_img.get("map")
    if not m:
        return x0, y0, x1, y1
    u, ox, oy = m
    return ox + u * x0, oy + u * y0, ox + u * x1, oy + u * y1


def character(cid, spec, rows, old, check, report):
    keys = [e for (c, e) in rows if c == cid]
    ref_file = old["images"]["neutral"]["file"]
    ref_img = Image.open(GAME / ref_file).convert("RGBA")
    images, pictures = {}, {}
    if spec["kind"] == "pixel":
        pack = {e: Image.open(PACK / rows[(cid, e)]["file"]).convert("RGBA") for e in keys}
        neutral = pack["neutral"]
        iou, u, ox, oy = register(ref_img, neutral)
        report["neutral_overlap"] = round(float(iou), 3)
        report["u"] = round(u, 4)
        nfeet = bbox(alpha(neutral))[3]
        for e, im in pack.items():
            if im.size == neutral.size:
                dxp = dyp = 0
            else:
                dxp = int(round((neutral.width - im.width) / 4.0)) * 2
                dyp = int(round((nfeet - bbox(alpha(im))[3]) / 2.0)) * 2
            name = "room13-fullbody-%s-%s-acting.webp" % (cid, e)
            images[e] = {"file": write(im, name, check), "size": list(im.size), "crop": file_crop(im),
                         "map": [round(u, 5), round(ox + u * dxp, 2), round(oy + u * dyp, 2)], "cell": 2,
                         "source_sha256": rows[(cid, e)]["sha256"], "stage": rows[(cid, e)]["stage"]}
            pictures[e] = im
        pixel = {"u": round(u, 5), "cell": 2}
    else:
        new = {}
        for e in keys:
            a = np.asarray(Image.open(PACK / rows[(cid, e)]["file"]).convert("RGBA"))
            new[e] = Image.fromarray(np.ascontiguousarray(a[0::2, 0::2]), "RGBA")  # one sample per 2x2 cell
        m = None
        if spec.get("scale"):
            u = float(spec["scale"])
            iou, u, ox, oy = register(ref_img, new[spec.get("register_with", "anxious")], band=.42, u_range=[u])
            report["leg_overlap"] = round(float(iou), 3)
            m = [round(u, 5), ox, oy]
        for e, im in new.items():
            name = "room13-fullbody-%s-%s-acting.webp" % (cid, e)
            images[e] = {"file": write(im, name, check), "size": list(im.size), "source_sha256": rows[(cid, e)]["sha256"],
                         "stage": rows[(cid, e)]["stage"]}
            if m:
                images[e].update(crop=file_crop(im), map=m)
            pictures[e] = im
        pixel = None
    for e in EMOTIONS:
        if e in images:
            continue
        if spec.get("package_only"):
            images[e] = dict(images["neutral"], fallback="neutral")
        else:
            images[e] = dict(old["images"][e], kept="current")
            pictures[e] = Image.open(GAME / old["images"][e]["file"]).convert("RGBA")
    if "neutral" not in pictures:
        pictures["neutral"] = ref_img
    # Union of everything shown, in reference pixels.
    boxes = [ref_box(images[e], pictures[e]) for e in pictures]
    fx0, fy0 = min(b[0] for b in boxes), min(b[1] for b in boxes)
    fx1, fy1 = max(b[2] for b in boxes), max(b[3] for b in boxes)
    W, H = ref_img.size
    crop = [max(0, int(np.floor(fx0)) - MARGIN), max(0, int(np.floor(fy0)) - MARGIN)]
    crop += [min(W, int(np.ceil(fx1)) + MARGIN) - crop[0], min(H, int(np.ceil(fy1)) + MARGIN) - crop[1]]
    figure = [int(np.floor(fx0)), int(np.floor(fy0)), int(np.ceil(fx1 - np.floor(fx0))), int(np.ceil(fy1 - np.floor(fy0)))]
    entry = {"crop": crop, "figure": figure, "images": images}
    if pixel:
        entry["pixel"] = pixel
    report["figure_h"] = {e: round(ref_box(images[e], pictures[e])[3] - ref_box(images[e], pictures[e])[1], 1) for e in pictures}
    return entry


def redesign_reference(cid):
    import apply_npc_redesign as rd
    registry = rd.load(rd.REGISTRY)
    design = next(d for d in registry["designs"] if d["npc"] == cid)
    img, geo = rd.geometry(design, registry)
    geo["size"] = img.size
    entry = rd.entries(cid, design, geo, "assets/room13-redesign-%s.webp" % cid)["fullbody"]
    on_disk = Image.open(GAME / entry["images"]["neutral"]["file"]).size
    if tuple(on_disk) != tuple(img.size):
        raise SystemExit("run dev/apply_npc_redesign.py --only %s first" % cid)
    return entry


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--revert", action="store_true")
    a = ap.parse_args()
    reg = load(ART / "registry.json")
    originals = ART / "original-files"
    if a.revert:
        for kind, path in FILES.items():
            saved = originals / path.name
            if saved.exists():
                path.write_bytes(saved.read_bytes())
        for f in ASSETS.glob("room13-fullbody-*-acting.webp"):
            f.unlink()
        print("reverted (byte-exact data files; acting pictures removed)")
        return
    rows = pack_rows()
    if not a.check and not originals.exists():
        originals.mkdir()
        for kind, path in FILES.items():
            (originals / path.name).write_bytes(path.read_bytes())
    # The registry's characters always start from their entries as they were before the first
    # apply (idempotent). 0.18.93: everyone else keeps the current file's entries, so later changes
    # by other scripts are not undone.
    src = {k: (originals / p.name if originals.exists() else p) for k, p in FILES.items()}
    orig = {k: load(src[k]) for k in FILES}
    data = {k: load(p) for k, p in FILES.items()}
    indents = {k: indent_of(p) for k, p in FILES.items()}
    people = data["fullbody"]["people"]
    orig_blink = orig["dotfx"].get("blink", {}).get("people", {})
    backup = {"note": "fullbody entries before dev/apply_expression_acting.py", "people": {}}
    out = {"applied": {}, "held": reg["held"]}
    for cid, spec in reg["apply"].items():
        old = orig["fullbody"]["people"][cid]
        backup["people"][cid] = old
        if spec.get("reference") == "npc_redesign":
            # 0.18.93: the design itself changed (네로 tiger -> silver wolf). The reference canvas is
            # the current redesign picture of the same design (dev/apply_npc_redesign.py), not the
            # superseded one, so registration overlays like with like.
            old = redesign_reference(cid)
        blink = data["dotfx"].setdefault("blink", {}).setdefault("people", {})
        if cid in orig_blink:
            blink[cid] = json.loads(json.dumps(orig_blink[cid]))
        else:
            blink.pop(cid, None)
        report = {}
        entry = character(cid, spec, rows, old, a.check, report)
        for key in ("name_ko", "redesign", "art"):
            if key in old:
                entry[key] = old[key]
        if old.get("poses"):
            entry["poses"] = old["poses"]   # same reference canvas: poses keep their size
        entry["acting_package"] = "expression-acting-20261016"
        people[cid] = entry
        if cid in blink:
            for e in list(blink[cid]):
                if entry["images"].get(e, {}).get("file") != old["images"].get(e, {}).get("file"):
                    del blink[cid][e]
            if not blink[cid]:
                del blink[cid]
        out["applied"][cid] = {"kind": spec["kind"], "package_keys": sorted(e for (c, e) in rows if c == cid),
                               "kept_current": sorted(e for e in EMOTIONS if entry["images"][e].get("kept")),
                               "neutral_fallback": sorted(e for e in EMOTIONS if entry["images"][e].get("fallback")),
                               "figure": entry["figure"], "crop": entry["crop"], **report}
    if not a.check:
        (ART / "original-entries.json").write_text(json.dumps(backup, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        for kind, path in FILES.items():
            dump(path, data[kind], indents[kind])
        (ART / "apply-report.json").write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    for cid, r in out["applied"].items():
        print(cid, r["kind"], "pkg", r["package_keys"], "kept", r["kept_current"], "fallback", r["neutral_fallback"],
              "u", r.get("u"), "overlap", r.get("neutral_overlap", r.get("leg_overlap")), "figH", r["figure_h"])
    print("held", sorted(reg["held"]))


if __name__ == "__main__":
    main()
