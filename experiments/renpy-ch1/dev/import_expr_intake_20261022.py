"""2026-10-22 expression intake: Codex full-body emotion pictures -> dialogue full-body slots.

    python3 dev/import_expr_intake_20261022.py --intake <exprgen dir>   # copy originals once
    python3 dev/import_expr_intake_20261022.py                          # apply (idempotent)
    python3 dev/import_expr_intake_20261022.py --check                  # verify, change nothing
    python3 dev/import_expr_intake_20261022.py --revert                 # restore previous entries

Only game/assets/room13-fullbody-dialogue.json image slots listed in PLAN change, plus new
webp files. Neutral pictures, crops, figures, poses and every other registry stay as they are.
Originals (byte-exact PNG + prompt/report of each job) live in art/expr-intake-20261022/.

Each character follows the convention its existing slots already use:
  batch  (doto, madam, teacher; tosil and siluk had only a neutral and get the same kind as the
         other canonical/role people): lossless copy of the generated picture (alpha 1-3 haze from
         the generator cleared), native_detail, map [u, ox, oy] with u rounded to 0.05,
         ox = figure centre - u*W/2, oy = figure bottom - u*(lowest alpha>=32 row), exactly as
         art/incoming/reviewed-batches-20261017.
  acting (seori, owlgp, guldol): 2x2 pixel cells like their acting neutral. The generated canvas
         is the neutral canvas scaled (Codex was given that canvas), so one uniform scale
         neutral width / generated width, nearest sampling at cell centres, binary alpha,
         canvas centre on canvas centre, lowest row on the neutral's foot row; even offsets,
         canvas grown by whole cells if a hand reaches outside; map u = the neutral's u.
  ep     (kkomi, pandol): premultiplied Lanczos halving of the 1024x1536 canvas (ep-art rule),
         lossy webp q95 like the other ep-art pictures; map [1, 0, dy] puts the feet on the
         neutral's foot row and keeps a wide pose (pointing arm, tail) outside the shared crop.
"""
import argparse, hashlib, io, json, shutil, sys
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
ASSETS = GAME / "assets"
ART = ROOT / "art/expr-intake-20261022"
FULLBODY = ASSETS / "room13-fullbody-dialogue.json"
TAG = "expr-intake-20261022"
VISIBLE, MARGIN, HAZE = 32, 4, 4
sys.path.insert(0, str(ROOT / "dev"))
from import_art import encode  # noqa: E402

# (job, person, emotion, method). Skipped jobs are listed in README.txt with the reason.
PLAN = [
    ("doto", "doto", "flustered", "batch"),
    ("madam", "resident_madam", "flustered", "batch"),
    ("teacher", "resident_teacher", "joy", "batch"),
    *[("tosil", "resident_tosil", e, "batch") for e in ("joy", "flustered", "angry", "anxious", "surprise")],
    *[("siluk", "resident_siluk", e, "batch") for e in ("joy", "flustered", "angry", "anxious", "surprise")],
    *[("seori", "resident_seori", e, "acting") for e in ("joy", "flustered", "surprise")],
    *[("owlgp", "resident_owlgp", e, "acting") for e in ("joy", "flustered", "angry", "surprise")],
    *[("guldol", "resident_guldol", e, "acting") for e in ("joy", "flustered", "angry", "anxious", "surprise")],
    *[("kkomi", "kid_kkomi", e, "ep") for e in ("flustered", "angry", "surprise")],
    *[("pandol", "npc_pandol", e, "ep") for e in ("flustered", "angry", "surprise")],
]
SOURCE_NAME = {"doto": "doto", "madam": "madam", "teacher": "teacher", "tosil": "tosil", "siluk": "siluk",
               "seori": "seori", "owlgp": "owlgp", "guldol": "guldol", "kkomi": "kkomi", "pandol": "pandol"}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def source_path(job, emotion):
    return ART / "originals" / job / ("%s_%s.png" % (SOURCE_NAME[job], emotion))


def rgba(path):
    im = Image.open(path)
    im.load()
    return im.convert("RGBA")


def bbox(alpha):
    ys, xs = np.where((alpha >= VISIBLE).any(1))[0], np.where((alpha >= VISIBLE).any(0))[0]
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


def clear_haze(im):
    a = np.array(im)
    haze = a[..., 3] < HAZE
    a[haze] = 0
    return Image.fromarray(a, "RGBA")


def lossless(im):
    buf = io.BytesIO(); im.save(buf, "PNG")
    return encode(io.BytesIO(buf.getvalue()), lossless=True)


def lossy(im):
    buf = io.BytesIO(); im.save(buf, "PNG")
    return encode(io.BytesIO(buf.getvalue()))


def even(v):
    return int(2 * round(v / 2.0))


def target_name(person, emotion, method):
    if method == "batch":
        return "assets/room13-role-%s-batch-%s-v1.webp" % (person, emotion)
    if method == "acting":
        if person == "resident_guldol":
            return "assets/room13-role-resident_guldol-%s.webp" % emotion
        return "assets/room13-fullbody-%s-%s-acting.webp" % (person, emotion)
    return "assets/room13-fullbody-%s-%s.webp" % (person, emotion)


def build_batch(entry, src):
    im = clear_haze(src)
    w, h = im.size
    fx, fy, fw, fh = entry["figure"]
    neutral = entry["images"]["neutral"]
    u = round(20 * neutral["size"][0] / float(w)) / 20.0
    bottom = bbox(np.asarray(im)[..., 3])[3]
    ox = (fx + fw / 2.0) - u * w / 2.0
    oy = (fy + fh) - u * bottom
    spec = dict(size=[w, h], crop=[0, 0, w, h], map=[u, round(ox, 4), round(oy, 4)], native_detail=True)
    return lossless(im), spec


def build_acting(entry, src):
    neutral = entry["images"]["neutral"]
    nim = rgba(GAME / neutral["file"])
    nw, nh = nim.size
    nb = bbox(np.asarray(nim)[..., 3])
    u, nox, noy = neutral["map"]
    a = np.asarray(src)
    sw, sh = src.size
    s = (nw / float(sw) + nh / float(sh)) / 2.0          # generated canvas = neutral canvas scaled
    cw, ch = int(np.ceil(sw * s / 2)), int(np.ceil(sh * s / 2))
    xs = np.minimum(((np.arange(cw) + .5) * 2 / s).astype(int), sw - 1)
    ys = np.minimum(((np.arange(ch) + .5) * 2 / s).astype(int), sh - 1)
    cells = a[ys][:, xs].copy()
    cells[..., 3] = np.where(cells[..., 3] >= 128, 255, 0)
    cells[cells[..., 3] == 0] = 0
    pic = np.repeat(np.repeat(cells, 2, 0), 2, 1)                       # 2x2 cells, file pixels
    pb = bbox(pic[..., 3])
    # canvas centre on canvas centre; lowest visible row on the neutral's foot row (even px)
    px = even(nw / 2.0 - pic.shape[1] / 2.0)
    py = even(nb[3] - pb[3])
    x0, y0 = px + pb[0] - MARGIN, py + pb[1] - MARGIN
    x1, y1 = px + pb[2] + MARGIN, py + pb[3] + MARGIN
    up = lambda v: max(0, v) + max(0, v) % 2              # grow by whole 2x2 cells only
    left, top, right, bottom = up(-x0), up(-y0), up(x1 - nw), up(y1 - nh)
    W, H = nw + left + right, nh + top + bottom
    canvas = np.zeros((H, W, 4), np.uint8)
    ox, oy = px + left, py + top
    # paste with clipping (only transparent margins can fall outside)
    sx0, sy0 = max(0, -ox), max(0, -oy)
    dx0, dy0 = max(0, ox), max(0, oy)
    ww = min(pic.shape[1] - sx0, W - dx0); hh = min(pic.shape[0] - sy0, H - dy0)
    canvas[dy0:dy0 + hh, dx0:dx0 + ww] = pic[sy0:sy0 + hh, sx0:sx0 + ww]
    if int(pic[..., 3].sum()) != int(canvas[..., 3].sum()):
        raise SystemExit("acting picture clipped")
    cb = bbox(canvas[..., 3])
    crop = [cb[0] - MARGIN, cb[1] - MARGIN, cb[2] - cb[0] + 2 * MARGIN, cb[3] - cb[1] + 2 * MARGIN]
    crop = [max(0, crop[0] - crop[0] % 2), max(0, crop[1] - crop[1] % 2), crop[2] + crop[2] % 2, crop[3] + crop[3] % 2]
    crop[2] = min(crop[2], W - crop[0]); crop[3] = min(crop[3], H - crop[1])
    spec = dict(size=[W, H], crop=crop, map=[u, round(nox - u * left, 5), round(noy - u * top, 5)], cell=2)
    return lossless(Image.fromarray(canvas, "RGBA")), spec


def build_ep(entry, src):
    w, h = src.size
    if (w, h) != (1024, 1536):
        a = np.zeros((1536, 1024, 4), np.uint8)
        sa = np.asarray(src)[:1536, :1024]
        a[:sa.shape[0], :sa.shape[1]] = sa
        if int(np.asarray(src)[..., 3].astype(np.int64).sum()) != int(a[..., 3].astype(np.int64).sum()):
            raise SystemExit("ep canvas trim would cut the figure")
        src = Image.fromarray(a, "RGBA")
    im = src.convert("RGBa").resize((512, 768), Image.LANCZOS).convert("RGBA")
    fx, fy, fw, fh = entry["figure"]
    b = bbox(np.asarray(im)[..., 3])
    dy = (fy + fh) - b[3]
    crop = [max(0, b[0] - MARGIN), max(0, b[1] - MARGIN)]
    crop += [min(512, b[2] + MARGIN) - crop[0], min(768, b[3] + MARGIN) - crop[1]]
    spec = dict(size=[512, 768], crop=crop, map=[1.0, 0.0, float(dy)], art="ep-art-20261016")
    return lossy(im), spec


BUILD = {"batch": build_batch, "acting": build_acting, "ep": build_ep}


def intake(directory):
    for job in sorted({p[0] for p in PLAN}):
        (ART / "originals" / job).mkdir(parents=True, exist_ok=True)
        for name in ("prompt.md", "report.md"):
            if (directory / job / name).exists():
                shutil.copyfile(directory / job / name, ART / "originals" / job / name)
    for job, person, emotion, method in PLAN:
        src = directory / job / "out" / source_path(job, emotion).name
        dst = source_path(job, emotion)
        if dst.exists() and sha(dst.read_bytes()) != sha(src.read_bytes()):
            raise SystemExit("different original already stored: " + str(dst))
        shutil.copyfile(src, dst)


def dump(data):
    FULLBODY.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def run(check=False, revert=False):
    data = json.loads(FULLBODY.read_text(encoding="utf-8"))
    people = data["people"]
    before_path = ART / "original-entries.json"
    before = json.loads(before_path.read_text(encoding="utf-8")) if before_path.exists() else {}
    report, errors = [], []
    for job, person, emotion, method in PLAN:
        key = person + "/" + emotion
        current = people[person]["images"][emotion]
        if revert:
            if key not in before:
                errors.append("no saved entry: " + key); continue
            if not check:
                people[person]["images"][emotion] = before[key]
                target = GAME / current["file"]
                if current.get("review_batch") == TAG and target.exists():
                    target.unlink()
            elif current != before[key]:
                errors.append("not reverted: " + key)
            continue
        src_file = source_path(job, emotion)
        raw = src_file.read_bytes()
        data_bytes, spec = BUILD[method](people[person], rgba(src_file))
        name = target_name(person, emotion, method)
        image = dict(file=name, **spec, source_sha256=sha(raw), review_batch=TAG)
        report.append(dict(person=person, key=emotion, job=job, method=method,
                           source="art/expr-intake-20261022/originals/%s/%s" % (job, src_file.name),
                           image=image, runtime_sha256=sha(data_bytes)))
        if check:
            if current != image:
                errors.append("entry differs: " + key)
            elif sha((GAME / name).read_bytes()) != sha(data_bytes):
                errors.append("file differs: " + name)
            continue
        if current.get("review_batch") != TAG:
            before.setdefault(key, current)
        (GAME / name).write_bytes(data_bytes)
        people[person]["images"][emotion] = image
    if errors:
        raise SystemExit("\n".join(errors))
    if not check:
        dump(data)
        if not revert:
            before_path.write_text(json.dumps(before, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            (ART / "connection-report.json").write_text(json.dumps(
                dict(status="applied", tag=TAG, expressions=report), ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return len(PLAN)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--intake", type=Path)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--revert", action="store_true")
    args = parser.parse_args()
    if args.intake:
        intake(args.intake)
        print("Stored originals in", ART)
    else:
        count = run(args.check, args.revert)
        print(("Checked" if args.check else "Reverted" if args.revert else "Applied") + " %d slots" % count)
