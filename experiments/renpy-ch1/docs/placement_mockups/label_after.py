"""Label the in-game placement renders for docs/placement_mockups/after/<place>.png.

1) xvfb-run -a -s "-screen 0 2560x1440x24" $RENPY_SDK/renpy.sh . test placement_after
   (a screen larger than 1280x720 so the window is 1:1; output in $ROOM13_QA_OUT/placement)
2) python3 docs/placement_mockups/label_after.py [that folder]
"""
import json, os, sys
from PIL import Image, ImageDraw, ImageFont
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("ROOM13_QA_OUT", "/tmp/room13-qa"), "placement")
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "after")
FONT = os.path.join(HERE, "..", "..", "game", "assets", "Galmuri11.ttf")
PER = ["오전", "오후", "저녁"]
os.makedirs(OUT, exist_ok=True)
font = ImageFont.truetype(FONT, 16); big = ImageFont.truetype(FONT, 20); small = ImageFont.truetype(FONT, 12)
for fn in sorted(os.listdir(SRC)):
    if not fn.endswith(".json"): continue
    place = fn[:-5]
    meta = json.load(open(os.path.join(SRC, fn)))
    im = Image.open(os.path.join(SRC, place + ".png")).convert("RGB")
    dr = ImageDraw.Draw(im)
    for a in meta["actors"]:
        fx, fy, fw, fh = a["face"]
        cx = fx + fw / 2; top = a["y"]
        t = a["name"]; tw = dr.textlength(t, font=font)
        x0 = int(cx - tw / 2 - 7); y0 = int(max(60, top - 30))
        fill = (255, 214, 110) if a["occlusion"] else (250, 248, 240)
        dr.rounded_rectangle([x0, y0, x0 + tw + 14, y0 + 24], 6, fill=fill, outline=(40, 30, 20), width=2)
        dr.text((x0 + 7, y0 + 3), t, font=font, fill=(25, 22, 20))
    head = "%s · 게임 화면 배치 (%d일 %s%s, 실제로 있는 %d명)" % (place, meta["day"], PER[meta["period"]], " · 2주차" if meta.get("week2") else "", len(meta["actors"]))
    sub = "game/qa_tests/placement_after.rpy 로 게임 렌더러에서 전체 폭을 그림 · 금색 이름표 = 매대·창구·책상 뒤(하반신 가림)"
    tw = max(dr.textlength(head, font=big), dr.textlength(sub, font=small)) + 24
    dr.rectangle([0, 0, tw, 52], fill=(20, 18, 24))
    dr.text((12, 4), head, font=big, fill=(255, 236, 190))
    dr.text((12, 32), sub, font=small, fill=(220, 220, 230))
    im.save(os.path.join(OUT, place + ".png"), optimize=True)
    print(place, meta["day"], meta["period"], [a["name"] for a in meta["actors"]])
