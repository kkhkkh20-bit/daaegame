"""Scale check (owner 2026-10-17: "원근법 적용하되 맵에 있는 사물 크기와 맞춰야 함").

For each place, draws on the in-game render (docs/placement_mockups/after source PNG) the background objects that were
measured for scale (scale_objects.json): an orange bracket over the object (top..floor contact) and, beside it,
a red bar = adult standing height the game now uses at that floor y (room13-world-layout.json "perspective"),
and a thin green bar = adult height the object implies (object height / its share of an adult).
Output: docs/placement_mockups/scale_check/<place>.jpg

python3 docs/placement_mockups/scale_check.py [render folder, default $ROOM13_QA_OUT/placement]
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(HERE, "..", "..", "game")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("ROOM13_QA_OUT", "/tmp/room13-qa"), "placement")
OUT = os.path.join(HERE, "scale_check")
os.makedirs(OUT, exist_ok=True)
LAYOUT = json.load(open(os.path.join(GAME, "assets", "room13-world-layout.json")))
OBJ = json.load(open(os.path.join(HERE, "scale_objects.json")))
FONT = os.path.join(GAME, "assets", "Galmuri11.ttf")
font = ImageFont.truetype(FONT, 15); big = ImageFont.truetype(FONT, 20); small = ImageFont.truetype(FONT, 12)

def background(place, spec):
    files = spec.get("files") or spec["state_files"]["before"]
    path = files.get("morning") or list(files.values())[0]
    im = Image.open(os.path.join(GAME, path)).convert("RGB")
    crop = (spec.get("crops") or {}).get("morning")
    if crop: im = im.crop((crop[0], crop[1], crop[0] + crop[2], crop[1] + crop[3]))
    return im.resize((int(spec.get("width", 1920)), 720), Image.NEAREST)

for place, objs in OBJ["places"].items():
    spec = LAYOUT[place]
    a, b = spec["perspective"]
    png = os.path.join(SRC, place + ".png")
    im = Image.open(png).convert("RGB") if os.path.exists(png) else background(place, spec)
    dr = ImageDraw.Draw(im)
    for o in objs:
        label, x0, x1, top, foot, share = o[:6]
        expect = a * foot + b; implied = (foot - top) / share
        dr.rectangle([x0, top, x1, foot], outline=(255, 150, 30), width=3)
        bx = x1 + 6
        dr.rectangle([bx, foot - expect, bx + 9, foot], fill=(220, 40, 40), outline=(40, 0, 0))
        dr.rectangle([bx + 11, foot - implied, bx + 14, foot], fill=(60, 200, 80))
        t = "%s  %d/%d" % (label, round(expect), round(implied))
        tw = dr.textlength(t, font=small)
        ty = max(56, foot - expect - 18)
        dr.rectangle([bx, ty, bx + tw + 8, ty + 16], fill=(20, 18, 24))
        dr.text((bx + 4, ty + 2), t, font=small, fill=(255, 236, 190))
    head = "%s · 사물 기준 원근 확인 · 어른 키 = %.3f×발y %+.0f" % (place, a, b)
    sub = "주황 = 잰 사물(위~바닥) · 빨강 막대 = 그 바닥 y에서 게임이 쓰는 어른 키 · 초록 선 = 사물이 뜻하는 어른 키 (숫자: 게임/사물)"
    tw = max(dr.textlength(head, font=big), dr.textlength(sub, font=small)) + 24
    dr.rectangle([0, 0, tw, 52], fill=(20, 18, 24))
    dr.text((12, 4), head, font=big, fill=(255, 236, 190))
    dr.text((12, 32), sub, font=small, fill=(220, 220, 230))
    if im.width > 2200: im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
    im.save(os.path.join(OUT, place + ".jpg"), quality=85)
    print(place, len(objs))
