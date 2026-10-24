"""B 지도(여관 안·숲·산길, 2026-10-24) 원본 고정 시험.

좌표는 납품 manifest/placement 를 그대로 옮겼는지, 수첩 틀이 아래 조작 줄과 겹치지 않는지,
숨은 장소가 기존 판정(r13_map_nodes / r13_map_locked_nodes)만 따르는지를 본다.
실제 입력·떠오름·이동은 game/qa_tests/b_map_inn_forest.rpy 화면 시험이 본다.
"""
import json, textwrap, types, unittest
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / "game"
INTAKE = ROOT.parents[1] / "design/resource-intake-20261024"
SOURCE = (GAME / "room13_map_b.rpy").read_text(encoding="utf-8")


def image_size(path):
    with Image.open(GAME / path) as im:
        return im.size


def namespace(nodes=None, locked=None, places=(), location="inn", touch=False):
    block = SOURCE.split("init 64 python:\n", 1)[1].split("\ntransform ", 1)[0]
    store = types.SimpleNamespace(room13={"location": location})
    renpy = types.SimpleNamespace(image_size=image_size)
    ns = {"store": store, "renpy": renpy, "r13_touch_ui": lambda: touch,
          "r13_places": lambda: list(places),
          "r13_map_nodes": lambda region: [(k, (0, 0)) for k in (nodes or {}).get(region, [])],
          "r13_map_locked_nodes": lambda region: [(k, (0, 0)) for k in (locked or {}).get(region, [])],
          "r13_map_label": lambda key: {"inn": "여관 접수대", "hall": "2층 복도", "guestroom": "임시 객실",
                                        "passage": "숨은 통로", "ancient": "옛 시설", "facility": "보호시설",
                                        "greenhouse": "폐온실", "altar": "산속 제단", "forest": "깊은 숲 · 교환함"}.get(key, "13호실")}
    exec(textwrap.dedent(block), ns)
    return ns


def overlap(a, b):
    return a[0] < b[0]+b[2] and b[0] < a[0]+a[2] and a[1] < b[1]+b[3] and b[1] < a[1]+a[3]


class MapB(unittest.TestCase):
    def setUp(self):
        self.ns = namespace()
        self.B = self.ns["R13_BMAP"]

    def test_assets_exist_with_alpha_and_names_appear_in_script(self):
        frame = GAME / (self.ns["R13_BMAP_ART"] + "notebook_frame.webp")
        self.assertEqual(image_size(frame), (1280, 720))
        self.assertIn("notebook_frame.webp", SOURCE)
        for region, spec in self.B.items():
            with Image.open(GAME / spec["base"]) as im:
                self.assertEqual(im.size, (1136, 570))
            arts = [p["art"] for p in spec["places"].values() if p["art"]] + [c["art"] for c in spec["covers"].values()]
            for art in arts:
                with Image.open(GAME / art) as im:
                    self.assertIn("A", im.getbands(), art)
                    self.assertLess(im.getchannel("A").getextrema()[0], 10, art)
                # dev/build_web.py 는 이름이 스크립트에 그대로 적힌 자산만 싣는다.
                self.assertIn(art.split("/")[-1], SOURCE)

    def test_every_map_node_has_a_place(self):
        nav = (GAME / "room13_navigation.rpy").read_text(encoding="utf-8")
        self.assertEqual(set(self.B), {"inn", "mountain"})
        self.assertEqual(set(self.B["inn"]["places"]),
                         {"inn", "dining", "kitchen", "hall", "room13", "passage", "guestroom", "ancient"})
        self.assertEqual(set(self.B["mountain"]["places"]), {"forest", "facility", "greenhouse", "altar"})
        self.assertEqual(set(self.B["mountain"]["covers"]), {"greenhouse", "altar"})
        self.assertEqual(self.B["inn"]["covers"], {})
        self.assertIn('use r13_map_b(region,selected,ready,map_hover,map_notice)', nav)

    def test_coordinates_follow_delivery(self):
        manifest = json.loads((INTAKE / "b-ui-map-forest/manifest.proposed.json").read_text(encoding="utf-8"))
        names = {"forest_path": "forest", "protection_facility": "facility",
                 "abandoned_greenhouse": "greenhouse", "mountain_altar": "altar"}
        for row in manifest["placements"]:
            place = self.B["mountain"]["places"][names[row["id"]]]
            self.assertEqual(list(place["box"]), row["box"])
            self.assertEqual(list(place["label"]), row["label_center"])
            if "cover_box" in row:
                self.assertEqual(list(self.B["mountain"]["covers"][names[row["id"]]]["box"]), row["cover_box"])
        placement = json.loads((INTAKE / "b-ui-map-inn/placement_proposal.json").read_text(encoding="utf-8"))
        names = {"corridor": "hall", "room13": "room13", "temporary_guestroom": "guestroom", "reception": "inn",
                 "dining": "dining", "kitchen": "kitchen", "hidden_passage": "passage"}
        for row in placement["items"]:
            place = self.B["inn"]["places"][names[row["id"]]]
            self.assertEqual(tuple(place["box"]), (row["x"], row["y"], row["width"], row["height"]))
            self.assertEqual(place["z"], row["z_index"])
            self.assertEqual(row["id"] == "hidden_passage", not row["default_visible"])
        self.assertEqual(manifest["map_offset"], [88, 58])
        self.assertEqual(tuple(self.ns["R13_BMAP_WINDOW"]), (88, 58, 1136, 570))

    def test_notebook_sits_above_footer(self):
        s = self.ns["R13_BMAP_SCALE"]
        fx, fy = self.ns["R13_BMAP_FRAME_POS"]
        self.assertLessEqual(fy + 690*s, 602, "수첩 아래 띠가 조작 줄(y602) 위에서 끝난다")
        self.assertGreaterEqual(fy + 16*s, 0)
        self.assertGreaterEqual(fx, 0)
        self.assertLessEqual(fx + 1280*s, 1280)

    def test_targets_inside_window_and_labels_apart(self):
        for touch in (False, True):
            ns = namespace(touch=touch)
            left, top = ns["r13_bmap_screen"](0, 0)
            right, bottom = ns["r13_bmap_screen"](1136, 570)
            for region, spec in ns["R13_BMAP"].items():
                labels = []
                for key, place in spec["places"].items():
                    t = ns["r13_bmap_target"](region, key)
                    for rect in filter(None, (t["sticker"], t["label"])):
                        self.assertTrue(left-1 <= rect[0] and rect[0]+rect[2] <= right+1, (region, key, rect))
                        self.assertTrue(top-1 <= rect[1] and rect[1]+rect[3] <= bottom+1, (region, key, rect))
                    if t["sticker"]:
                        # 휴대폰 360px 높이에서 44 CSS px = 가상 88px.
                        self.assertGreaterEqual(min(t["sticker"][2:]), 88, (region, key))
                    for other, rect in labels:
                        self.assertFalse(overlap(t["label"], rect), (region, key, other, touch))
                    labels.append((key, t["label"]))

    def test_hidden_places_follow_existing_gates_only(self):
        # 숨은 곳은 r13_map_nodes 에 없으면 아예 돌아오지 않는다(이름표·버튼·접근성 이름 없음).
        ns = namespace(nodes={"inn": ["inn", "dining", "room13"], "mountain": ["forest"]},
                       locked={"mountain": ["facility"]}, places=("inn", "dining", "forest"), location="room13")
        self.assertEqual(ns["r13_bmap_places"]("inn"), [("inn", "open"), ("dining", "open"), ("room13", "shown")])
        self.assertEqual(ns["r13_bmap_places"]("mountain"), [("forest", "open"), ("facility", "locked")])
        self.assertEqual([k for k, c in ns["r13_bmap_covers"]("mountain")], ["greenhouse", "altar"])
        self.assertEqual(ns["r13_bmap_covers"]("inn"), [])
        ns = namespace(nodes={"inn": ["passage", "ancient"], "mountain": ["forest", "greenhouse", "altar"]},
                       places=("passage", "ancient", "forest", "greenhouse"), location="altar")
        self.assertEqual(ns["r13_bmap_places"]("inn"), [("passage", "open"), ("ancient", "open")])
        self.assertEqual(ns["r13_bmap_covers"]("mountain"), [])
        self.assertIsNone(ns["r13_bmap_target"]("inn", "ancient")["sticker"])

    def test_screen_draws_only_from_gated_lists(self):
        screen = SOURCE.split("screen r13_map_b(", 1)[1]
        self.assertIn("$ rows = r13_bmap_places(region)", screen)
        self.assertIn("for key, cover in r13_bmap_covers(region):", screen)
        self.assertNotIn('spec["places"].items()', screen)
        self.assertNotIn("r13_map_discovered(key)", SOURCE.split("def r13_bmap_places", 1)[1].split("def ", 1)[0])
        self.assertIn("r13_map_nodes(region)", SOURCE.split("def r13_bmap_places", 1)[1].split("def r13_bmap_hint", 1)[0])
        # 떠오름: 기존 지도와 같은 r13_map_pop, 터치는 올림 단계를 쓰지 않음.
        self.assertIn("At(art, r13_map_pop)", screen)
        self.assertEqual(screen.count('hovered (None if r13_touch_ui() else SetScreenVariable("map_hover", key))'), 1)
        self.assertIn('id (("map_room_" if region == "inn" else "map_building_")+key)', screen)


if __name__ == "__main__":
    unittest.main()
