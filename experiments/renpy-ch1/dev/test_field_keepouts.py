"""바닥 소품(keepouts)·한 걸음 비킴 상한·월드 가장자리 고정(2026-10-27 소유자 지적: 통 안의 실룩, 소쿠리 위의 여니, 가장자리의 까로)."""
import ast
import json
import re
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def functions(path, names):
    source = (ROOT / path).read_text(encoding='utf-8')
    nodes = []
    for block in re.split(r'^init[^\n]*:\n', source, flags=re.M)[1:]:
        try:
            tree = ast.parse(textwrap.dedent(block))
        except SyntaxError:
            continue
        nodes.extend(n for n in tree.body if isinstance(n, (ast.FunctionDef, ast.Assign)) and
                     (isinstance(n, ast.Assign) and any(getattr(t, 'id', None) in names for t in n.targets) or
                      isinstance(n, ast.FunctionDef) and n.name in names))
    return ast.Module(body=nodes, type_ignores=[])


def face(a):
    return [a['x'] + 20, a['y'], a['width'] - 40, 60]


class FieldKeepouts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns = dict(r13_actor_face_target=face, r13_world_height=lambda: 960,
                      r13_ma_place=lambda actor, pose, fx, fy, height: dict(actor, x=int(fx - actor['width'] / 2),
                                                                             rect=[int(fx - actor['width'] / 2), actor['y'], actor['width'], actor['height']]))
        for path, names in [('game/systems/room13_investigation_balance.rpy', {'r13_balance_translate'}),
                            ('game/room13_v111_field_layout.rpy', {'r13_clear_objects', 'r13_foot_in_keepout', 'r13_clamp_to_world', 'r13_keepout_cover_rects',
                                                                    'r13_clear_critical_x', 'R13_CLEAR_STEP_MAX'})]:
            exec(compile(functions(path, names), path, 'exec'), cls.ns)

    def actor(self, person, x, y=480, w=120, h=210):
        return dict(person=person, pose='neutral', x=x, y=y, width=w, height=h, rect=[x, y, w, h], depth=y + h, contact='standing')

    def test_store_keepouts_are_registered_for_the_floor_props(self):
        store = json.loads((ROOT / 'game/assets/room13-world-layout.json').read_text(encoding='utf-8'))['store']
        self.assertGreaterEqual(len(store['keepouts']), 2)
        # 파란 통(1385~1505)과 소쿠리(1510~1645)는 발을 둘 수 없다. 자리 칸·생활 행도 그 안에 발을 두지 않는다.
        life = json.loads((ROOT / 'game/assets/room13-field-life.json').read_text(encoding='utf-8'))
        feet = [tuple(s[:2]) for s in store['slots']] + [tuple(r['target']) for r in life['rows'] if r.get('location') == 'store']
        for fx, fy in feet:
            for k in store['keepouts']:
                kx, ky, kw, kh = k[:4]
                self.assertFalse(kx <= fx <= kx + kw and ky <= fy <= ky + kh, ((fx, fy), k))

    def test_actor_in_a_bucket_steps_to_the_free_floor(self):
        bucket = (1385, 515, 120, 205)
        rows = [self.actor('resident_siluk', 1390, y=489)]      # 발 (1450,699) 이 통 안
        out = self.ns['r13_clear_objects'](rows, [], 1920, [bucket])
        rect = out[0]['rect']
        self.assertFalse(self.ns['r13_foot_in_keepout'](rect, [bucket]))
        self.assertLessEqual(max(0, min(rect[0] + rect[2], bucket[0] + bucket[2]) - max(rect[0], bucket[0])) * 205, 120 * 205 * .2)
        self.assertEqual(out[0]['y'], rows[0]['y'])              # 발 선은 지킨다
        # 발만 금지하는 칸(앞 큰 상자)은 그 앞 바닥에 서서 몸이 겹쳐도 된다.
        crate = (1655, 430, 265, 200, 'feet')
        yeoni = self.actor('resident_yeoni', 1739, y=490)       # 발 (1799,700): 상자 아래 바닥
        out = self.ns['r13_clear_objects']([yeoni], [], 1920, [crate])
        self.assertEqual(out[0]['rect'], yeoni['rect'])

    def test_worker_may_cover_only_the_object_of_the_row(self):
        woodpile = (1880, 637, 125, 111)
        crates = (1608, 734, 206, 100)
        bori = dict(self.actor('resident_bori', 1957, y=559, w=265, h=307), work_rect=woodpile)
        out = self.ns['r13_clear_objects']([bori], [woodpile, crates], 2560)
        self.assertEqual(out[0]['rect'], bori['rect'])          # 자기 장작더미는 덮어도 된다
        other = dict(bori, work_rect=crates)
        out = self.ns['r13_clear_objects']([other], [woodpile, crates], 2560)
        self.assertNotEqual(out[0]['rect'], other['rect'])      # 남의 물건이면 비킨다

    def test_side_step_does_not_cross_half_a_screen(self):
        self.assertLessEqual(self.ns['R13_CLEAR_STEP_MAX'], 400)
        karo = self.actor('karo', 557, y=462, w=127, h=166)
        road = (216, 469, 413, 127)
        crowd = [self.actor('p%d' % x, x, y=500, w=100, h=170) for x in (700, 800, 900, 1000, 1100, 1200)]
        out = self.ns['r13_clear_critical_x'](karo, [road], [karo] + crowd, 1920)
        # 오른쪽은 끝까지 붐비고 왼쪽 빈자리(128)는 반 화면 너머라 그대로 둔다(사슬 끝 규칙에 맡긴다).
        self.assertEqual(out['rect'], karo['rect'])
        out = self.ns['r13_clear_critical_x'](karo, [road], [karo, crowd[0]], 1920)
        # 가까운 빈자리가 있으면 그리로 한 걸음(상한 안).
        self.assertLessEqual(abs(out['rect'][0] - karo['rect'][0]), self.ns['R13_CLEAR_STEP_MAX'])
        self.assertNotEqual(out['rect'], karo['rect'])

    def test_rects_never_leave_the_world(self):
        rows = [self.actor('a', -30), self.actor('b', 1850)]
        out = self.ns['r13_clamp_to_world'](rows, 1920)
        self.assertEqual(out[0]['rect'][0], 0)
        self.assertEqual(out[1]['rect'][0] + out[1]['rect'][2], 1920)
        self.assertEqual([a['y'] for a in out], [a['y'] for a in rows])


if __name__ == '__main__':
    unittest.main()
