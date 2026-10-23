"""0.20.11 적용 때 개발 쪽 보정: 큰 장소(강·숲)의 선택 영역에서 작은 장소(입구·빨래터·학교)와 겹치는 부분을 뺀다.

게임 시험(test_worldmap_v5)은 두 장소의 선택 영역이 겹치지 않아야 한다. 강·숲의 다각형만 고치고,
그 둘의 영역 그림(RGBA)과 윤곽선 그림을 같은 방식(바깥 투명, 밝은 2px 선)으로 다시 만든다.
    python3 fix_overlaps.py
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw
from shapely.geometry import Polygon, Point
from shapely.ops import unary_union

ROOT = Path(__file__).resolve().parents[5]
GAME = ROOT / "experiments/renpy-ch1/game"
CART = GAME / "room13-cartography.json"
data = json.loads(CART.read_text(encoding="utf-8"))
village = data["regions"]["village"]
nodes = village["nodes"]
art = Image.open(GAME / village["art"]).convert("RGBA")
LINE = (255, 248, 228, 255)

def poly(key):
    return Polygon(nodes[key]["polygon"]).buffer(0)

def write(key, shape):
    shape = shape.simplify(1.0)
    if shape.geom_type != "Polygon":
        shape = max(shape.geoms, key=lambda g: g.area)
    pts = [[int(round(x)), int(round(y))] for x, y in list(shape.exterior.coords)[:-1]]
    assert shape.contains(Point(nodes[key]["point"])), key
    xs, ys = zip(*pts)
    x0, y0 = max(0, min(xs) - 3), max(0, min(ys) - 3)
    x1, y1 = min(art.width, max(xs) + 4), min(art.height, max(ys) + 4)
    w, h = x1 - x0, y1 - y0
    local = [(px - x0, py - y0) for px, py in pts]
    mask = Image.new("L", (w, h)); ImageDraw.Draw(mask).polygon(local, fill=255)
    fill = art.crop((x0, y0, x1, y1)); fill.putalpha(mask)
    fill.save(GAME / f"assets/room13-map-village-{key}.webp", lossless=True, method=6)
    outline = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(outline).line(local + [local[0]], fill=LINE, width=2, joint="curve")
    outline.save(GAME / f"assets/room13-map-village-{key}-outline.webp", lossless=True, method=6)
    nodes[key]["polygon"] = pts
    nodes[key]["bounds"] = [x0, y0, w, h]

small_by_big = {"river": ("gate", "laundry"), "forest": ("school",)}
for big, smalls in small_by_big.items():
    cut = unary_union([poly(s).buffer(2) for s in smalls])
    write(big, poly(big).difference(cut))

CART.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print("ok")
