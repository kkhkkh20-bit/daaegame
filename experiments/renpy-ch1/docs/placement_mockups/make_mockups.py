#!/usr/bin/env python3
"""Room13 장소별 인물 배치·원근 시안 (2026-10-17, 시안 전용).

게임 파일을 읽기만 하고 고치지 않는다. 결과: docs/placement_mockups/<장소>.png
실행: python3 docs/placement_mockups/make_mockups.py  (experiments/renpy-ch1 에서)

깊이 규칙: 발 y 에서 서 있는 어른 키 h(y) = H700 * (y - yv) / (700 - yv)
  yv = 그 장소에서 키가 0이 되는 가상의 y(멀수록 작아지는 정도), H700 = 화면 아래쪽(y=700) 어른 키.
  인물 키 = h(y) * 체격(아이 0.76, 청소년 0.90, 어른 1.00, 노년 0.95, 일부 개별 보정).
  앉음·웅크림 동작은 게임과 같이 머리 크기를 맞춰 줄인다(stature_ratio 가 있으면 그 값).
매대·창구 뒤 인물은 배경의 '가림 다각형'을 다시 덮어 하반신을 가린다.
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
GAME = os.path.join(ROOT, "game")
OUT = os.path.dirname(os.path.abspath(__file__))
LAYOUT = json.load(open(os.path.join(GAME, "assets/room13-world-layout.json")))
ACT = json.load(open(os.path.join(GAME, "assets/room13-pixel-acting.json")))
SCHED = json.load(open(os.path.join(ROOT, "qa_schedule.json")))
NAMES = dict(SCHED["names"]); NAMES.update(dad="아빠", mom="엄마", daram="다람")
FONT = os.path.join(GAME, "assets/Room13Sans.ttf")

AGE = {  # docs/CAST_BIBLE.md 나이
    "child": ["daram", "bami", "resident_kongi", "resident_somi", "resident_tosil", "resident_jongjong"],
    "teen": ["buri", "nabi", "doto", "resident_tori", "resident_kkwak", "resident_mungchi", "resident_ubak", "resident_guseul"],
    "elder": ["granny", "resident_owlgp", "resident_ppul", "resident_musoe", "resident_guldol"],
}
STATURE_BASE = {"child": 0.76, "teen": 0.90, "elder": 0.95}
STATURE_FIX = {"resident_bori": 1.06, "resident_tok": 1.04, "resident_teacher": 1.04, "resident_mungchi": 0.96}

def stature(pid):
    if pid in STATURE_FIX: return STATURE_FIX[pid]
    for k, v in AGE.items():
        if pid in v: return STATURE_BASE[k]
    return 1.0

# 장소별 깊이 규칙(yv, H700). 기존 perspective 가 자연스러운 곳은 그대로 옮겼다.
RULE = {
    "market": (163, 251), "post": (119, 234), "inn": (0, 265), "school": (100, 271),
    "workshop": (0, 277), "square": (60, 267), "gate": (130, 246), "clinic": (130, 250),
    "store": (196, 362), "greenhouse": (130, 250), "facility": (130, 255), "altar": (0, 268),
    "kitchen": (72, 262), "dining": (130, 265), "passage": (237, 253), "hall": (-71, 267),
    "room13": (-88, 241), "river": (395, 246), "forest": (324, 250), "ancient": (236, 255),
    "guestroom": (130, 270),
}
TITLE = {
    "gate": "눈에 막힌 입구", "square": "돌이 있는 광장", "post": "우체국", "inn": "여관 접수대",
    "dining": "여관 식당", "hall": "여관 2층 복도", "room13": "13호실", "guestroom": "임시 객실",
    "kitchen": "여관 주방", "workshop": "수리점", "passage": "서비스 통로", "clinic": "임시 진료실",
    "school": "마을 학교", "store": "공동 물품 창고", "greenhouse": "폐온실 지하 작업실",
    "facility": "보호시설 접견실", "altar": "숲속 제단", "river": "큰 강가", "forest": "길 없는 숲",
    "market": "장터", "ancient": "지하 옛 시설",
}

def P(pid, x, y, pose="neutral", role="guest", occ=None, new=None, hand=None):
    return dict(pid=pid, x=x, y=y, pose=pose, role=role, occ=occ, new=new, hand=hand)

# 가림 다각형(배경을 다시 덮는 영역). 좌표는 장소 그림(가로 W x 720) 기준.
OCC = {
    "market": {
        "prod": [(560, 452), (600, 440), (650, 432), (700, 437), (755, 445), (765, 425), (800, 410), (840, 412),
                 (860, 422), (880, 413), (930, 418), (950, 470), (950, 610), (560, 610)],
        "cheese": [(1225, 448), (1265, 430), (1270, 415), (1345, 415), (1352, 438), (1360, 423), (1435, 420),
                   (1440, 440), (1490, 440), (1500, 420), (1550, 423), (1565, 448), (1565, 525), (1225, 525)],
        "cloth": [(1715, 455), (1735, 425), (1830, 418), (1890, 425), (1940, 420), (1960, 440), (1958, 480),
                  (2012, 485), (2015, 560), (1715, 560)],
        "pots": [(2010, 505), (2035, 452), (2075, 432), (2120, 440), (2160, 440), (2160, 600), (2010, 600)],
    },
    "post": {"counter": [(1100, 560), (1135, 515), (1500, 500), (1600, 492), (1700, 480), (2160, 470),
                         (2160, 720), (1100, 720)]},
    "inn": {"desk": [(1395, 402), (1440, 392), (1560, 395), (1700, 400), (1840, 410), (1862, 420), (1862, 700),
                     (1395, 545)]},
    "store": {"table": [(275, 505), (420, 490), (560, 472), (700, 455), (880, 440), (890, 620), (880, 720),
                        (275, 720)]},
    "square": {
        "ration": [(0, 468), (90, 462), (280, 460), (290, 480), (345, 520), (345, 600), (0, 600)],
        "cart": [(330, 472), (420, 465), (560, 480), (600, 505), (600, 565), (330, 565)],
        "bench": [(870, 545), (900, 520), (1000, 515), (1060, 540), (1065, 605), (870, 605)],
    },
    "workshop": {
        "bench": [(331, 460), (470, 439), (683, 441), (1060, 483), (1060, 624), (890, 678), (350, 604)],
        "rbench": [(1250, 426), (1505, 426), (1505, 570), (1250, 570)],
    },
    "clinic": {"table": [(420, 500), (500, 482), (700, 474), (1090, 478), (1100, 520), (1100, 720), (420, 720)]},
    "school": {"desks": [(185, 412), (450, 408), (470, 440), (470, 570), (185, 570)]},
    "facility": {"desk": [(720, 432), (800, 425), (1450, 430), (1462, 445), (1462, 612), (720, 612)]},
    "dining": {
        "front": [(950, 500), (1100, 488), (1400, 470), (1700, 468), (2160, 480), (2160, 720), (950, 720)],
        "back1": [(645, 356), (965, 356), (965, 445), (645, 445)],
        "back3": [(1855, 356), (2085, 356), (2085, 445), (1855, 445)],
    },
    "kitchen": {"table": [(600, 522), (700, 515), (760, 500), (820, 482), (860, 458), (905, 447), (1000, 462),
                          (1025, 470), (1180, 470), (1200, 452), (1295, 460), (1300, 472), (1500, 482),
                          (1550, 520), (1600, 600), (1600, 720), (600, 720)]},
}

# 배치. role: staff=매대·창구·책상 뒤, work=제자리 작업, guest=손님·방문, seat=앉음.
# new=동작 요청서(ACTION_REQUEST_20261017.md) 번호. 시안에는 지금 그림을 두고 표시만 한다.
PLACE = {
    "market": [
        P("resident_solbang", 705, 505, "neutral", "staff", "prod", "MK-1"),
        P("resident_eunho", 1262, 500, "living_prices", "staff", "cheese", "MK-2"),
        P("resident_guseul", 1525, 500, "living_stamp", "staff", "cheese", "MK-3"),
        P("resident_nubi", 1772, 497, "neutral", "staff", "cloth", "MK-4"),
        P("resident_yeoni", 1915, 497, "neutral", "staff", "cloth", "MK-5"),
        P("resident_dalgeurak", 2040, 500, "neutral", "staff", "pots", "MK-6"),
        P("resident_tori", 1675, 600, "activity", "work"),
        P("resident_kongi", 870, 640, "activity", "work"),
        P("resident_mulgyeol", 660, 660, "neutral", "guest"),
        P("resident_ppul", 1120, 605, "activity", "guest"),
        P("resident_madam", 1330, 625, "neutral", "guest"),
        P("resident_mungchi", 1455, 655, "neutral", "guest", None, "MK-7"),
        P("resident_hyeoni", 1010, 695, "neutral", "work", None, "MK-8"),
        P("resident_tosil", 470, 690, "living_thermos", "guest"),
        P("resident_jongjong", 1890, 690, "neutral", "guest"),
    ],
    "post": [
        P("seryeon", 1270, 503, "action_1", "staff", "counter"),
        P("resident_sling", 1460, 499, "neutral", "staff", "counter", "PO-1"),
        P("resident_librarian", 560, 600, "living_bookpaper", "work", None, "PO-2"),
        P("resident_momo", 285, 640, "living_lampnumber", "work"),
        P("resident_jongjong", 1040, 640, "neutral", "work", None, "PO-3"),
        P("resident_ppul", 880, 692, "neutral", "guest"),
        P("resident_eunho", 690, 705, "neutral", "guest"),
        P("resident_guseul", 110, 690, "neutral", "guest"),
        P("resident_kongi", 430, 712, "neutral", "guest"),
    ],
    "inn": [
        P("granny", 1610, 470, "living_keyledger", "staff", "desk"),
        P("resident_tosil", 1300, 640, "living_thermos", "work"),
        P("resident_nubi", 420, 655, "neutral", "work", None, "IN-1"),
        P("resident_owlgp", 300, 650, "living_notebook", "seat"),
        P("resident_tori", 820, 690, "activity", "seat"),
        P("resident_ttadak", 1043, 472, "living_doorframe", "work"),
        P("resident_eunho", 1185, 600, "neutral", "guest"),
        P("resident_guseul", 1090, 560, "neutral", "guest"),
        P("resident_madam", 950, 592, "neutral", "guest"),
        P("resident_ubak", 1440, 700, "living_measure", "work"),
        P("resident_yeoni", 640, 612, "neutral", "guest"),
    ],
    "store": [
        P("resident_eunho", 365, 585, "living_prices", "staff", "table"),
        P("resident_guseul", 795, 568, "living_stamp", "staff", "table"),
        P("resident_madam", 1130, 650, "neutral", "guest"),
        P("resident_mungchi", 990, 560, "neutral", "work", None, "ST-1"),
        P("resident_siluk", 1385, 690, "neutral", "work", None, "ST-2"),
        P("resident_nero", 1620, 700, "activity", "work"),
        P("resident_bori", 1250, 600, "neutral", "guest"),
        P("resident_kkwak", 1520, 640, "neutral", "guest"),
        P("resident_kongi", 1060, 705, "neutral", "guest"),
        P("resident_yeoni", 1770, 690, "neutral", "guest"),
        P("resident_nubi", 1830, 612, "neutral", "guest"),
        P("resident_seori", 960, 712, "living_notes", "work"),
    ],
    "square": [
        P("doto", 150, 525, "action_1", "staff", "ration"),
        P("resident_ppul", 335, 645, "activity", "work"),
        P("resident_dalgeurak", 470, 505, "neutral", "staff", "cart", "SQ-1"),
        P("resident_piko", 965, 585, "neutral", "staff", "bench", "SQ-2"),
        P("resident_seol", 1225, 560, "living_bellrope", "work"),
        P("resident_lamplighter", 1095, 645, "living_inspectlamp", "work"),
        P("resident_owlgp", 700, 600, "living_notebook", "seat"),
        P("resident_tori", 1840, 568, "world_bench_left", "seat"),
        P("resident_yeoni", 1765, 566, "living_mend", "seat"),
        P("resident_jongjong", 1350, 705, "neutral", "guest"),
        P("resident_badook", 1500, 645, "neutral", "work"),
        P("resident_bori", 120, 690, "living_firewood", "work"),
        P("resident_hyeoni", 1310, 615, "neutral", "work", None, "MK-8"),
        P("resident_guldol", 1460, 705, "neutral", "guest"),
        P("resident_sling", 610, 700, "neutral", "guest"),
        P("resident_somi", 1650, 700, "living_bootice", "guest"),
        P("resident_tosil", 1150, 705, "neutral", "guest"),
    ],
    "gate": [
        P("guard", 1365, 602, "action_1", "work"),
        P("karo", 560, 615, "living_axlewrap", "work"),
        P("neoul", 1070, 620, "neutral", "work", None, "GA-1"),
        P("resident_badook", 900, 625, "neutral", "work"),
        P("resident_bori", 1625, 600, "living_firewood", "work"),
        P("resident_nero", 420, 685, "activity", "work"),
        P("resident_siluk", 1195, 690, "neutral", "guest"),
        P("resident_kalbaram", 780, 702, "neutral", "guest"),
        P("resident_kkwak", 1000, 705, "neutral", "guest"),
        P("resident_lamplighter", 1265, 680, "living_inspectlamp", "work"),
    ],
    "workshop": [
        P("buri", 0, 0, "action_1", "staff", "bench", hand=(620, 421, 208)),
        P("resident_tok", 1380, 470, "neutral", "staff", "rbench", "WS-1"),
        P("resident_guldol", 1120, 690, "neutral", "work"),
        P("resident_lamplighter", 1700, 700, "living_inspectlamp", "work"),
        P("resident_musoe", 150, 660, "living_foldmap", "guest"),
        P("resident_ttadak", 1580, 640, "living_repair", "work"),
        P("resident_ubak", 1250, 600, "living_measure", "work"),
        P("resident_bori", 270, 560, "living_firewood", "work"),
        P("resident_nubi", 1820, 600, "neutral", "guest"),
        P("resident_yeoni", 960, 705, "neutral", "guest"),
        P("resident_tori", 1400, 708, "neutral", "guest"),
    ],
    "clinic": [
        P("resident_seori", 960, 545, "living_notes", "staff", "table"),
        P("resident_piko", 1190, 560, "distressed", "seat", None, "CL-1"),
        P("resident_solbang", 1450, 690, "neutral", "guest"),
        P("resident_ubak", 1700, 660, "living_measure", "work"),
    ],
    "school": [
        P("resident_teacher", 330, 452, "neutral", "staff", "desks", "SC-1"),
        P("resident_bori", 1120, 640, "living_firewood", "work"),
        P("resident_tok", 790, 600, "activity", "work"),
        P("resident_yeoni", 1370, 690, "neutral", "guest"),
        P("resident_nubi", 180, 690, "neutral", "work", None, "IN-1"),
        P("resident_seori", 1660, 688, "living_notes", "work"),
    ],
    "facility": [
        P("neoul", 1250, 482, "neutral", "staff", "desk", "FA-1"),
        P("resident_nubi", 400, 680, "neutral", "work", None, "IN-1"),
    ],
    "dining": [
        P("nabi", 1080, 520, "action_2", "staff", "front"),
        P("resident_owlgp", 230, 662, "living_notebook", "seat"),
        P("resident_tok", 800, 445, "activity", "seat", "back1", "DI-1"),
        P("resident_dalgeurak", 1965, 440, "neutral", "seat", "back3", "DI-1"),
        P("resident_hyeoni", 540, 682, "neutral", "work", None, "MK-8"),
        P("resident_mulgyeol", 360, 640, "neutral", "guest"),
    ],
    "kitchen": [P("nabi", 700, 560, "neutral", "staff", "table", "KI-1")],
    "hall": [
        P("doto", 1471, 616, "action_1", "work"),
        P("bami", 1760, 662, "action_2", "seat"),
        P("resident_owlgp", 1017, 669, "neutral", "guest"),
    ],
    "room13": [P("daram", 1420, 662, "neutral", "guest")],
    "guestroom": [P("daram", 835, 674, "neutral", "guest")],
    "greenhouse": [P("mom", 1650, 661, "action_1", "work")],
    "river": [
        P("resident_kkwak", 260, 705, "neutral", "work", None, "RI-1"),
        P("resident_mulgyeol", 520, 712, "neutral", "work", None, "RI-2"),
        P("resident_nero", 660, 712, "activity", "work"),
    ],
    "forest": [
        P("resident_kalbaram", 1450, 706, "neutral", "work", None, "FO-1"),
        P("resident_solbang", 1000, 700, "neutral", "work"),
        P("resident_badook", 1900, 712, "living_bootlace", "work"),
        P("resident_bori", 820, 708, "living_firewood", "work"),
        P("resident_siluk", 1700, 705, "neutral", "guest"),
        P("resident_tosil", 1200, 712, "neutral", "guest"),
    ],
    "passage": [], "altar": [], "ancient": [],
}

def background(place):
    if place == "guestroom":
        im = Image.open(os.path.join(GAME, "assets/room13-pixel-room-before-morning.webp")).convert("RGB")
        return im.resize((1280, 720), Image.NEAREST), 1280
    lay = LAYOUT[place]
    files = lay.get("files") or lay["state_files"]["before"]
    path = files.get("morning") or list(files.values())[0]
    im = Image.open(os.path.join(GAME, path)).convert("RGB")
    crop = (lay.get("crops") or {}).get("morning")
    if crop: im = im.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
    W = int(lay.get("width", 1920))
    return im.resize((W, 720), Image.NEAREST), W

def h_at(place, y):
    yv, H = RULE[place]
    return max(40.0, H * (y - yv) / (700.0 - yv))

def spec_of(pid, pose):
    s = ACT[pid].get(pose) or ACT[pid]["neutral"]
    return s

def foot_of(s):
    c = s.get("crop")
    return s.get("foot") or (s.get("anchor") or {}).get("foot") or [c[2] / 2.0, c[3]]

def sprite(pid, pose, target):
    s = spec_of(pid, pose); n = ACT[pid]["neutral"]
    im = Image.open(os.path.join(GAME, s["file"])).convert("RGBA")
    c = s["crop"]; im = im.crop((c[0], c[1], c[0] + c[2], c[1] + c[3]))
    nh = n["crop"][3]
    if s.get("stature_ratio") is not None:
        disp = target * s["stature_ratio"]
    elif pose == "neutral":
        disp = target
    else:
        ratio = (c[3] / float(s["head"][3])) / (nh / float(n["head"][3])) if s.get("head") and n.get("head") else c[3] / float(nh)
        disp = target * ratio
    sc = disp / c[3]
    return im, sc, foot_of(s), s

def poly_mask(size, polys):
    m = Image.new("L", size, 0); d = ImageDraw.Draw(m)
    for p in polys: d.polygon(p, fill=255)
    return m

def label(dr, cx, top, text, sub, fill, edge, font, sfont):
    tw = dr.textlength(text, font=font)
    sw = dr.textlength(sub, font=sfont) if sub else 0
    w = max(tw, sw) + 14; hgt = 24 + (18 if sub else 0)
    x0 = int(cx - w / 2); y0 = int(max(4, top - hgt - 4))
    dr.rounded_rectangle([x0, y0, x0 + w, y0 + hgt], 6, fill=fill, outline=edge, width=2)
    dr.text((cx - tw / 2, y0 + 3), text, font=font, fill=(25, 22, 20))
    if sub: dr.text((cx - sw / 2, y0 + 24), sub, font=sfont, fill=(140, 50, 0))

def render(place):
    bg, W = background(place)
    canvas = bg.convert("RGBA")
    people = PLACE.get(place, [])
    occ = OCC.get(place, {})
    items = []
    for p in people:
        pid = p["pid"]
        if p["hand"]:
            tx, ty, dh = p["hand"]
            s = spec_of(pid, p["pose"]); c = s["crop"]
            im = Image.open(os.path.join(GAME, s["file"])).convert("RGBA").crop((c[0], c[1], c[0] + c[2], c[1] + c[3]))
            sc = dh / float(c[3]); hx, hy = s["hand"]
            x = tx - hx * sc; y = ty - hy * sc; zy = y + c[3] * sc
            target = dh
        else:
            target = h_at(place, p["y"]) * stature(pid)
            im, sc, foot, s = sprite(pid, p["pose"], target)
            x = p["x"] - foot[0] * sc; y = p["y"] - foot[1] * sc; zy = p["y"]
        im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.NEAREST)
        items.append((zy, p, im, int(x), int(y), target))
    items.sort(key=lambda t: t[0])
    boxes = []
    for zy, p, im, x, y, target in items:
        canvas.alpha_composite(im, (x, y)) if x >= 0 and y >= 0 else canvas.paste(im, (x, y), im)
        if p["occ"]:
            m = poly_mask(canvas.size, [occ[p["occ"]]])
            box = Image.new("L", canvas.size, 0); ImageDraw.Draw(box).rectangle([x, y, x + im.width, y + im.height], fill=255)
            from PIL import ImageChops
            m = ImageChops.multiply(m, box)
            canvas.paste(bg.convert("RGBA"), (0, 0), m)
        # visible top (first non-transparent row)
        bb = im.getbbox() or (0, 0, im.width, im.height)
        boxes.append((p, x + bb[0], y + bb[1], x + bb[2], y + bb[3], target))
    dr = ImageDraw.Draw(canvas)
    font = ImageFont.truetype(FONT, 17); sfont = ImageFont.truetype(FONT, 14); big = ImageFont.truetype(FONT, 22)
    # occluder outlines (thin) so the cut line can be reviewed
    for name, poly in occ.items():
        dr.line(poly + [poly[0]], fill=(255, 210, 60, 255), width=1)
    for p, x0, y0, x1, y1, target in boxes:
        if p["new"]:
            for i in range(x0, x1, 10): dr.line([(i, y0), (min(i + 5, x1), y0)], fill=(255, 120, 0), width=3); dr.line([(i, y1), (min(i + 5, x1), y1)], fill=(255, 120, 0), width=3)
            for j in range(y0, y1, 10): dr.line([(x0, j), (x0, min(j + 5, y1))], fill=(255, 120, 0), width=3); dr.line([(x1, j), (x1, min(j + 5, y1))], fill=(255, 120, 0), width=3)
        fill = {"staff": (255, 214, 110), "work": (190, 230, 255), "seat": (210, 240, 200), "guest": (250, 248, 240)}[p["role"]]
        sub = ("새 동작 " + p["new"]) if p["new"] else None
        label(dr, (x0 + x1) / 2, y0, NAMES.get(p["pid"], p["pid"]), sub, fill, (40, 30, 20), font, sfont)
    # depth ruler at left: standing adult height at y=500/600/700
    yv, H = RULE[place]
    for i, yy in enumerate((520, 610, 700)):
        hh = h_at(place, yy); xx = 14 + i * 16
        if yy - hh < 0: continue
        dr.line([(xx, yy), (xx, yy - hh)], fill=(255, 255, 255), width=5)
        dr.line([(xx, yy), (xx, yy - hh)], fill=(220, 40, 60), width=3)
    # header
    n = len(people)
    head = "%s (%s)  깊이: 어른 키 = %d x (발y - %d) / (700 - %d)" % (TITLE[place], place, H, yv, yv)
    sub = "가로 %dpx 파노라마(화면 1280x720 비율 그대로) · 전원 지정 자리 %d명(동시에 다 있지 않음) · 금색=매대·창구 뒤 / 하늘=일하는 자리 / 연두=앉음 / 흰색=손님 · 주황 점선=새 동작 필요" % (W, n)
    tw = max(dr.textlength(head, font=big), dr.textlength(sub, font=sfont)) + 24
    dr.rectangle([0, 0, tw, 56], fill=(20, 18, 24, 255))
    dr.text((12, 4), head, font=big, fill=(255, 236, 190))
    dr.text((12, 34), sub, font=sfont, fill=(220, 220, 230))
    if not people:
        dr.text((12, 62), "일정상 머무는 주민 없음 — 왼쪽 빨간 막대가 이 장소의 어른 키 기준(발 y=520/610/700)", font=sfont, fill=(255, 255, 255))
    canvas.convert("RGB").save(os.path.join(OUT, place + ".png"), optimize=True)
    return n, sum(1 for p in people if p["new"])

if __name__ == "__main__":
    places = sys.argv[1:] or list(PLACE)
    for pl in places:
        print(pl, render(pl))
