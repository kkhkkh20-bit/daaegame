"""마을 지도(B)의 처음 보이는 화면에서 장소 이름표가 보기 창 가장자리에 걸리지 않는지(2026-10-27 소유자 지적).

이름표는 통째로 보이거나 통째로 숨어야 한다. 어느 장소를 골라 열어도, PC·휴대폰 모두.
"""
import ast
import json
import re
import textwrap
import unittest
from pathlib import Path

from type_stub import r13_type_stub

ROOT = Path(__file__).resolve().parents[1]
GAME = ROOT / 'game'


def load_block():
    source = (GAME / 'room13_map_village_b.rpy').read_text(encoding='utf-8')
    block = source.split('init 65 python:\n', 1)[1].split('\nscreen ', 1)[0]
    tree = ast.parse(textwrap.dedent(block))
    keep = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in
            ('r13_village_b_label_px', 'r13_village_b_label_width', 'r13_village_b_label_boxes',
             'r13_village_b_clean_scrolls', 'r13_village_b_focus')]
    return compile(ast.Module(body=keep, type_ignores=[]), 'map_village_b', 'exec')


class MapLabelEdges(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        layout = json.loads((GAME / 'assets/map-village-b/layout.json').read_text(encoding='utf-8'))
        cls.places = {row['id']: row for row in layout['locations']}
        nav = (GAME / 'room13_navigation.rpy').read_text(encoding='utf-8')
        labels = ast.literal_eval(re.search(r'R13_MAP_LABELS = (\{.*?\})\n', nav, re.S).group(1))
        labels.update(dict(river='강가', forest='숲', market='장터', somi='소미네', laundry='빨래터'))
        cls.labels = labels
        cls.zoom = float(re.search(r'default village_zoom=([0-9.]+)', nav).group(1))
        view = re.search(r'R13_VILLAGE_B_VIEW = \((.*?)\)', (GAME / 'room13_map_village_b.rpy').read_text(encoding='utf-8')).group(1)
        cls.view = tuple(int(v) for v in view.split(','))
        cls.code = load_block()

    def env(self, touch):
        ns = dict(R13_VILLAGE_B_PLACES=self.places, R13_VILLAGE_B_VIEW=self.view, R13_TYPE_V2=True,
                  r13_touch_ui=lambda: touch, r13_type=r13_type_stub(touch=touch), r13_type_pc=r13_type_stub(touch=False),
                  r13_read_size=lambda a, b: a, r13_map_label=lambda key: self.labels[key],
                  R13_V111_MAP_ALIASES={})
        exec(self.code, ns)
        return ns

    def test_every_place_opens_with_whole_labels(self):
        zoom = max(self.zoom, 1136.0 / 1642, 506.0 / 958)
        for touch in (False, True):
            ns = self.env(touch)
            boxes = ns['r13_village_b_label_boxes'](zoom)
            vw, vh = self.view[2] / zoom, self.view[3] / zoom
            for key in self.places:
                with self.subTest(touch=touch, selected=key):
                    fx, fy = ns['r13_village_b_focus'](key, zoom)
                    # 2026-10-30: 뷰포트 xinitial/yinitial 은 정수를 픽셀로 읽는다. 끝(1.0)이 정수 1 로 오면 맨 위가 열린다.
                    self.assertIsInstance(fx, float, key)
                    self.assertIsInstance(fy, float, key)
                    sx = fx * max(0, 1642 - vw); sy = fy * max(0, 958 - vh)
                    # 고른 장소의 이름표는 창 안에 있다.
                    l, t, r, b = boxes[key]
                    self.assertTrue(sx <= l and r <= sx + vw, (key, boxes[key], sx, sx + vw))
                    self.assertTrue(sy <= t and b <= sy + vh, (key, boxes[key], sy, sy + vh))
                    # 다른 이름표는 통째로 보이거나 통째로 숨는다.
                    for other, (ol, ot, orr, ob) in boxes.items():
                        self.assertFalse(ol < sx < orr or ol < sx + vw < orr, (key, other, (ol, orr), (sx, sx + vw)))
                        self.assertFalse(ot < sy < ob or ot < sy + vh < ob, (key, other, (ot, ob), (sy, sy + vh)))

    def test_default_zoom_has_clean_positions_on_both_axes(self):
        # 배율을 올리면 가로 위치가 사라진다(1.15 에서 0개). 기본 배율은 두 축 모두 비어 있지 않아야 한다.
        for touch in (False, True):
            xs, ys = self.env(touch)['r13_village_b_clean_scrolls'](self.zoom)
            self.assertTrue(xs and ys, (touch, len(xs), len(ys)))


if __name__ == '__main__':
    unittest.main()
