"""주민 생활 동작 A안(흰 테두리 스티커) 그림을 기존 동작 자리에 맞춰 넣는다 (2026-10-24 소유자: "이것들 에셋 매칭해서 적용시켜줘").

    python3 dev/import_resident_poses_a.py          # 그림과 교체표를 다시 만든다
    python3 dev/import_resident_poses_a.py --check  # 지금 파일이 다시 만든 결과와 같은지만 본다

왜 이렇게 하나
- 새 자리는 만들지 않는다. 납품 설명서의 원화 경로와 같은 그림을 지금 쓰는 동작 자리만 바꾼다.
  자리·시간·조건·대사·생사 걸러내기는 기존 배치 코드 그대로 탄다.
- 기존 JSON(room13-map-action27.json 등)은 영수증·지문 시험이 묶여 있어 고치지 않는다.
  대신 교체표 game/assets/room13-resident-poses-a.json 을 만들고 init 186 층
  (systems/room13_resident_poses_a.rpy)이 같은 spec 을 제자리에서 바꾼다.
- 새 그림은 옛 그림을 다시 그린 것이라 몸의 위치가 거의 같다. 옛 그림의 불투명 상자와 새 그림의
  불투명 상자를 맞추는 축별 배율 하나로 잘라내기·발·머리·손·가림 다각형을 모두 옮긴다.
  잘라내기 높이 안에서 몸이 차지하는 비율이 그대로라 화면 크기·발 위치가 기존 인물과 같다.
- 출력 파일은 옮긴 잘라내기 영역만큼의 캔버스다(남는 투명 여백을 버려 파일이 작아지고,
  넘치는 쪽은 투명으로 채운다). 저장은 dev/import_art.py 와 같은 WebP q95 + 무손실 알파.
"""
import argparse, copy, hashlib, io, json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
INTAKE = ROOT / "art/resident-poses-a-20261024/intake"
OUT_DIR = "assets/resident-poses-a"
TABLE = GAME / "assets/room13-resident-poses-a.json"
ALPHA = 64  # 가장자리의 옅은 알파 점(납품 설명서)이 상자를 넓히지 않게 한다

# (납품 파일, 옛 그림, 출력 이름). 옛 그림을 쓰는 모든 동작 자리를 바꾼다.
APPLY = [
    ("A1/piko_paint_sketchboard_A.webp", "assets/investigation-canonical-20261018/resident_piko--map27_paint_sketchboard_v2.webp", "piko-paint-sketchboard"),
    ("A1/mungchi_store_boxes_A.webp", "assets/map-work-nine/resident_mungchi--store_sort_boxes.webp", "mungchi-store-boxes"),
    ("A3/doto_write_ledger_A.webp", "assets/investigation-canonical-20261018/doto--map27_write_ledger_v2.webp", "doto-write-ledger"),
    ("A3/jongjong_sort_letters_A.webp", "assets/investigation-canonical-20261018/resident_jongjong--map27_sort_letters_v2.webp", "jongjong-sort-letters"),
    ("A3/musoe_inspect_tool_A.webp", "assets/investigation-jobs-20261018/musoe-inspect-old-tool-v1.webp", "musoe-inspect-tool"),
    ("A3/nubi_tie_laundry_A.webp", "assets/map-work-nine/resident_nubi--inn_sort_tie_laundry.webp", "nubi-tie-laundry"),
    ("A3/buri_A.webp", "assets/room13-action-buri-event_toolbox.webp", "buri-event-toolbox"),
    ("A3/siluk_A.webp", "assets/room13-action-resident_siluk-event_whisper.webp", "siluk-event-whisper"),
    ("A3/sling_A.webp", "assets/room13-action-resident_sling-event_steam.webp", "sling-event-steam"),
    # 따닥·토실은 2026-10-18 에 같은 동작의 새 원화(investigation-source2)로 이미 바뀌어 있다. 구도가 같아 그 자리에 넣는다.
    ("A3/ttadak_A.webp", "assets/investigation-source2/ttadak-doorframe-v1.webp", "ttadak-doorframe"),
    ("A3/resident_teacher--wet_coat--A.webp", "assets/map-work-nine/resident_teacher--school_spread_wet_coat.webp", "teacher-wet-coat"),
    ("A3/resident_solbang--herb_bundle--A.webp", "assets/solbang-chinchilla-map/work_herb_bundle.webp", "solbang-herb-bundle"),
    ("A3/resident_kongi--meeting_seated--A.webp", "assets/room13-meeting-seated-resident_kongi068.webp", "kongi-meeting-seated"),
    ("A3/resident_lamplighter--lightstone--A.webp", "assets/investigation-jobs-20261018/chorong-replace-lightstone-v1.webp", "lamplighter-lightstone"),
    ("A4/tok_repair_lantern_A.webp", "assets/map-action27/WS-1--resident_tok.webp", "tok-repair-lantern"),
    ("A4/neoul_point_documents_A.webp", "assets/map-action27/GA-1--neoul.webp", "neoul-point-documents"),
    ("A4/kalbaram_examine_ground_A.webp", "assets/map-action27/FO-1--resident_kalbaram.webp", "kalbaram-examine-ground"),
    ("A4/nabi_slice_carrot_A.webp", "assets/map-action27/KI-1--nabi.webp", "nabi-slice-carrot"),
    ("A4/eunho_A.webp", "assets/map-action27/MK-2--resident_eunho.webp", "eunho-ledger"),
    ("A4/guseul_A.webp", "assets/map-action27/MK-3--resident_guseul.webp", "guseul-scale"),
    ("A4/hyeoni_A.webp", "assets/map-action27/MK-8--resident_hyeoni.webp", "hyeoni-lute"),
    ("A4/badook_A.webp", "assets/map-action27/VA-1--resident_badook.webp", "badook-lantern-patrol"),
    ("A4/resident_ppul--meeting_seated--A.webp", "assets/room13-meeting-seated-resident_ppul068.webp", "ppul-meeting-seated"),
    ("A4/resident_seori--meeting_seated--A.webp", "assets/room13-meeting-seated-resident_seori068.webp", "seori-meeting-seated"),
    ("A4/resident_tori--meeting_seated--A.webp", "assets/room13-meeting-seated-resident_tori068.webp", "tori-meeting-seated"),
    ("A4/seryeon--meeting_seated--A.webp", "assets/room13-meeting-seated-seryeon068.webp", "seryeon-meeting-seated"),
    ("A5/bang_A.webp", "assets/room13-group-kid_bang-play.webp", "kid-bang-play"),
    ("A5/kid_kkam--play_wave--A.webp", "assets/room13-group-kid_kkam-play.webp", "kid-kkam-play"),
    ("A5/kid_mong--play_skip--A.webp", "assets/room13-group-kid_mong-play.webp", "kid-mong-play"),
    # 밤이·보듬은 여러 칸짜리 판의 한 칸만 같은 동작이다. 그 칸을 잘라 쓰는 자세 하나만 바꾼다.
    ("A5/bami--seated_writing--A.webp", "assets/room13-pixel-acting-bami.webp", "bami-seated-writing", {"bami": ["action_2"]}),
    ("A5/bodum--basket_cloth_opening--A.webp", "assets/room13-pixel-acting-bodum.webp", "bodum-basket-cloth", {"bodum": ["activity"]}),
    ("A12/dalgeurak_pots_display_A.webp", "assets/map-work-nine/resident_dalgeurak--pots_display.webp", "dalgeurak-pots-display"),
    ("A12/guldol_stone_tapping_A.webp", "assets/map-work-nine/resident_guldol--stone_tapping.webp", "guldol-stone-tapping"),
    ("A12/kkwak_haul_net_A.webp", "assets/map-work-nine/resident_kkwak--river_haul_net.webp", "kkwak-haul-net"),
    ("A12/mulgyeol_rope_coiling_A.webp", "assets/map-work-nine/resident_mulgyeol--rope_coiling.webp", "mulgyeol-rope-coiling"),
    ("A12/granny_keyledger_A.webp", "assets/room13-action-granny-living_keyledger.webp", "granny-keyledger"),
    ("A12/karo_axlewrap_A.webp", "assets/room13-action-karo-living_axlewrap.webp", "karo-axlewrap"),
    ("A12/resident_librarian_bookpaper_A.webp", "assets/room13-action-resident_librarian-living_bookpaper.webp", "librarian-bookpaper"),
    ("A12/resident_momo_lampnumber_A_v2.webp", "assets/room13-action-resident_momo-living_lampnumber.webp", "momo-lampnumber"),
    ("A12/resident_owlgp--notebook--A.webp", "assets/room13-action-resident_owlgp-living_notebook.webp", "owlgp-notebook"),
    ("A12/resident_seol--bellrope--A-v2-margin.webp", "assets/room13-action-resident_seol-living_bellrope.webp", "seol-bellrope"),
    ("A12/resident_tosil--thermos--A.webp", "assets/investigation-source2/tosil-thermos-v1.webp", "tosil-thermos"),
    ("A12/resident_yeoni--mend--A.webp", "assets/room13-action-resident_yeoni-living_mend.webp", "yeoni-mend"),
    ("A6/bori_tie_firewood_A.webp", "assets/room13-action-resident_bori-living_firewood.webp", "bori-tie-firewood"),
    ("A6/doto_compare_ration_slips_A.webp", "assets/investigation-canonical-20261018/doto--map27_compare_ration_slips_v2.webp", "doto-compare-ration-slips"),
    ("A6/jongjong_pack_mailbag_A.webp", "assets/investigation-canonical-20261018/resident_jongjong--map27_pack_satchel_v2.webp", "jongjong-pack-mailbag"),
]

POINT_KEYS = ("foot", "seat", "hand")
RECT_KEYS = ("head",)


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def alpha_box(im, region=None):
    a = im.getchannel("A")
    if region:
        x, y, w, h = region
        a = a.crop((x, y, x + w, y + h))
    box = a.point(lambda v: 255 if v >= ALPHA else 0).getbbox()
    if not box:
        raise SystemExit("빈 그림: %s" % (region,))
    if region:
        box = (box[0] + region[0], box[1] + region[1], box[2] + region[0], box[3] + region[1])
    return box


def collect_slots(old_file, only):
    """옛 그림을 쓰는 모든 자리를 (종류, 위치, spec) 로 모은다. 같은 dict 를 두 번 세지 않는다."""
    slots = []
    acting = load(GAME / "assets/room13-pixel-acting.json")
    cast = load(GAME / "assets/cast.json")
    for kind, doc in (("acting", acting), ("cast", cast)):
        for person, poses in doc.items():
            if not isinstance(poses, dict):
                continue
            for pose, spec in poses.items():
                if isinstance(spec, dict) and spec.get("file") == old_file and "crop" in spec:
                    if only is not None and pose not in only.get(person, []):
                        continue
                    slots.append(dict(kind=kind, person=person, pose=pose, spec=spec))
    for row in load(GAME / "assets/room13-map-action27.json")["rows"]:
        if row["spec"].get("file") == old_file:
            slots.append(dict(kind="map27", person=row["person"], pose=row["pose"], request_id=row["request_id"], spec=row["spec"]))
    for row in load(GAME / "assets/room13-map-work-nine.json")["people"]:
        if row["spec"].get("file") == old_file:
            slots.append(dict(kind="map9", person=row["person"], pose=row["pose"], spec=row["spec"], row=row))
    for group in load(GAME / "assets/room13-life-groups.json")["groups"]:
        for member in group["members"]:
            if (member.get("spec") or {}).get("file") == old_file:
                slots.append(dict(kind="life_group", group=group["id"], person=member["person"], pose=member["pose"], spec=member["spec"]))
    for who, spec in load(GAME / "assets/room13-meeting-seated.json").items():
        if spec.get("file") == old_file:
            slots.append(dict(kind="meeting", person=who, pose="meeting_seated", spec=spec))
    return slots


def encode(im):
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=95, method=6, alpha_quality=100)
    return buf.getvalue()


def build_one(entry):
    src, old_file, name = entry[:3]
    only = entry[3] if len(entry) > 3 else None
    new = Image.open(INTAKE / src).convert("RGBA")
    old = Image.open(GAME / old_file).convert("RGBA")
    slots = collect_slots(old_file, only)
    if not slots:
        raise SystemExit("쓰는 자리가 없다: " + old_file)
    crops = {tuple(s["spec"]["crop"]) for s in slots}
    # 여러 칸짜리 판은 자리마다 잘라내기 안의 몸만 본다. 한 장짜리는 모든 자리의 잘라내기가 같은 몸을 담는다.
    ob = alpha_box(old, list(crops)[0]) if len(crops) == 1 else alpha_box(old)
    nb = alpha_box(new)
    sx = (nb[2] - nb[0]) / float(ob[2] - ob[0])
    sy = (nb[3] - nb[1]) / float(ob[3] - ob[1])

    def to_new(x, y):
        return nb[0] + (x - ob[0]) * sx, nb[1] + (y - ob[1]) * sy

    # 옮긴 잘라내기들을 모두 담는 캔버스. 새 그림 밖으로 나가는 쪽은 투명으로 채운다.
    mapped = []
    for c in crops:
        x0, y0 = to_new(c[0], c[1]); x1, y1 = to_new(c[0] + c[2], c[1] + c[3])
        mapped.append((x0, y0, x1, y1))
    left = int(round(min(m[0] for m in mapped))); top = int(round(min(m[1] for m in mapped)))
    right = int(round(max(m[2] for m in mapped))); bottom = int(round(max(m[3] for m in mapped)))
    canvas = Image.new("RGBA", (right - left, bottom - top), (0, 0, 0, 0))
    canvas.paste(new, (-left, -top))  # 마스크 없이 그대로 옮긴다(마스크를 쓰면 알파가 두 번 곱해진다)
    data = encode(canvas)
    out_rel = "%s/%s.webp" % (OUT_DIR, name)
    sha = hashlib.sha256(data).hexdigest()

    def rel_point(p, crop):
        # 잘라내기 기준 좌표는 축별 배율만 곱하면 된다(잘라내기도 같은 배율로 옮겼으므로).
        return [round(p[0] * sx, 2), round(p[1] * sy, 2)]

    rows = []
    for s in slots:
        spec = s["spec"]; c = spec["crop"]
        x0, y0 = to_new(c[0], c[1])
        crop = [int(round(x0)) - left, int(round(y0)) - top, int(round(c[2] * sx)), int(round(c[3] * sy))]
        crop[2] = min(crop[2], canvas.width - crop[0]); crop[3] = min(crop[3], canvas.height - crop[1])
        fields = dict(file=out_rel, crop=crop, source_sha256=sha, native_detail=True, resident_pose_a=True)
        for k in POINT_KEYS:
            if isinstance(spec.get(k), list) and len(spec[k]) == 2:
                fields[k] = rel_point(spec[k], c)
        for k in RECT_KEYS:
            if isinstance(spec.get(k), list) and len(spec[k]) == 4:
                h = spec[k]
                fields[k] = [round(h[0] * sx, 2), round(h[1] * sy, 2), round(h[2] * sx, 2), round(h[3] * sy, 2)]
        if isinstance(spec.get("anchors"), dict):
            fields["anchors"] = {n: rel_point(p, c) for n, p in spec["anchors"].items()}
        if spec.get("foreground_parts"):
            fields["foreground_parts"] = [[rel_point(p, c) for p in poly] for poly in spec["foreground_parts"]]
        if s["kind"] == "meeting":
            fields = dict(file=out_rel, crop=crop, source_sha256=sha, resident_pose_a=True)
        row = dict(kind=s["kind"], person=s["person"], pose=s["pose"], old_file=old_file, fields=fields)
        for k in ("request_id", "group"):
            if k in s:
                row[k] = s[k]
        if s["kind"] == "map9":
            # 굴돌은 원본 전체 캔버스 기준 정규화 좌표(작업대 접점)로 놓인다. 같은 배율로 옮긴다.
            r = s["row"]; ow, oh = r["source_size"]
            norm = {}
            for n, p in r.get("contacts", {}).get("contacts_normalized_full_canvas", {}).items():
                if isinstance(p, list) and len(p) == 2:
                    ax, ay = to_new(p[0] * ow, p[1] * oh)
                    norm[n] = [round((ax - left) / canvas.width, 5), round((ay - top) / canvas.height, 5)]
                else:
                    norm[n] = p
            row["row_fields"] = dict(source_size=[canvas.width, canvas.height], contacts_normalized_full_canvas=norm)
        rows.append(row)
    info = dict(intake=src, old_file=old_file, file=out_rel, canvas=list(canvas.size), scale=[round(sx, 4), round(sy, 4)],
                aspect_gap=round(abs(sx / sy - 1), 4), old_body=list(ob), new_body=list(nb))
    return data, out_rel, rows, info


def build():
    files, slots, report = {}, [], []
    for entry in APPLY:
        data, out_rel, rows, info = build_one(entry)
        files[out_rel] = data; slots += rows; report.append(info)
    table = dict(schema=1, note="주민 생활 동작 A안 교체표. dev/import_resident_poses_a.py 가 만든다. 손으로 고치지 않는다.",
                 intake="art/resident-poses-a-20261024/intake", slots=slots, assets=report)
    return files, table


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--check", action="store_true"); a = ap.parse_args()
    files, table = build()
    text = json.dumps(table, ensure_ascii=False, indent=2) + "\n"
    if a.check:
        bad = [p for p, d in files.items() if not (GAME / p).exists() or (GAME / p).read_bytes() != d]
        if TABLE.read_text(encoding="utf-8") != text:
            bad.append(str(TABLE))
        print("다름: %s" % bad if bad else "같음"); return 1 if bad else 0
    (GAME / OUT_DIR).mkdir(parents=True, exist_ok=True)
    for p, d in files.items():
        (GAME / p).write_bytes(d)
    TABLE.write_text(text, encoding="utf-8")
    for r in table["assets"]:
        print(r["file"], r["canvas"], "배율", r["scale"], "가로세로차", r["aspect_gap"])
    print("그림 %d, 자리 %d" % (len(files), len(table["slots"])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
