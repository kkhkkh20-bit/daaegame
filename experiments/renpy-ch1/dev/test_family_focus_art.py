"""가족의 첫 발견만 큰 컷으로 읽고, 자료 제시와 선택창의 수명은 유지한다."""
import ast
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FamilyFocusArt(unittest.TestCase):
    def setUp(self):
        source = (ROOT / 'game/systems/room13_ep_art.rpy').read_text()
        block = source.split('init 160 python:', 1)[1].split('\ntransform ', 1)[0]
        tree = ast.parse(textwrap.dedent(block))
        names = {'R13_EV_CUT_BOX', 'R13_FAMILY_FOCUS_BOX', 'R13_FAMILY_FOCUS_KEYS', 'R13_FAMILY_DRAWING_ART',
                 'R13_EV_CUT_PX', 'R13_EV_CUT_FRAMES', 'R13_EV_CUT_FRAME',
                 'r13_ev_pixel_frame', 'r13_ev_pixel_panel', 'r13_ep_cut_art'}
        selected = [node for node in tree.body if
                    isinstance(node, ast.FunctionDef) and node.name in names or
                    isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets)]
        self.env = dict(Fixed=lambda *items, **kw: dict(items=items, **kw),
                        Transform=lambda art=None, **kw: dict(art=art, **kw),
                        Solid=lambda color, **kw: dict(color=color, **kw),
                        Frame=lambda *args: dict(frame=args), Crop=lambda *args: dict(crop=args),
                        r13_asset_path=lambda role: role[5:], Null=lambda: dict(empty=True))
        exec(compile(ast.Module(body=selected, type_ignores=[]), '가족 첫 발견 컷', 'exec'), self.env)

    def test_existing_evidence_presentation_size_and_asset_are_preserved(self):
        for key in self.env['R13_FAMILY_FOCUS_KEYS']:
            regular = self.env['r13_ep_cut_art']('ev:' + key)
            self.assertEqual(regular['items'][1]['xysize'], (180, 180))
            self.assertEqual(regular['items'][1]['art'], self.env['R13_FAMILY_DRAWING_ART'] if key=='D01_FAMILY_DRAWING' else 'assets/evidence/' + key + '.webp')

    def test_authored_family_focus_is_preserved_and_placeholder_bag_is_hidden(self):
        self.assertEqual(set(self.env['R13_FAMILY_FOCUS_KEYS']), {'E06', 'D01_FAMILY_DRAWING', 'D01_SNACK_BAG'})
        for key in ('E06','D01_FAMILY_DRAWING'):
            focused = self.env['r13_ep_cut_art']('focus:' + key)['items'][1]
            self.assertEqual(focused['art'], self.env['R13_FAMILY_DRAWING_ART'] if key=='D01_FAMILY_DRAWING' else 'assets/evidence/' + key + '.webp')
            self.assertTrue((ROOT / 'game' / focused['art']).is_file())
            self.assertEqual(focused['xysize'], (372, 372))
            self.assertEqual(focused['fit'], 'contain')
            self.assertTrue(focused['nearest'])
        self.assertEqual(self.env['r13_ep_cut_art']('focus:D01_SNACK_BAG'), dict(empty=True))
        x, y, side = self.env['R13_FAMILY_FOCUS_BOX']
        self.assertGreaterEqual(x, 740)  # 왼쪽 대화 인물을 비운다.
        self.assertLessEqual(x + side, 1280)
        self.assertGreaterEqual(y, 90)  # 날짜판 아래에 둔다.
        self.assertLessEqual(y + side, 504)  # 큰 글씨 대사판·이름 리본 위에서 끝난다.

    def test_focus_hides_for_choice_and_resumes_the_same_cut(self):
        source = (ROOT / 'game/systems/room13_ep_art.rpy').read_text()
        block = source.split('init 162 python:', 1)[1].split('\ndefault ', 1)[0]
        tree = ast.parse(textwrap.dedent(block))
        selected = [node for node in tree.body if isinstance(node, ast.FunctionDef)
                    and node.name in {'r13_ep_cut_suspend', 'r13_ep_cut_resume'}]
        shown, hidden = [], []
        state = types.SimpleNamespace(r13_ep_cut_current='focus:E06', r13_ep_cut_suspended=None)
        self.env.update(store=state, renpy=types.SimpleNamespace(
            showing=lambda tag: True, hide=lambda tag: hidden.append(tag),
            show=lambda tag, **kw: shown.append((tag, kw))))
        exec(compile(ast.Module(body=selected, type_ignores=[]), '선택창 뒤 가족 컷 복원', 'exec'), self.env)
        self.env['r13_ep_cut_suspend']()
        self.assertEqual(hidden, ['r13_ep_cut'])
        self.assertEqual(state.r13_ep_cut_suspended, 'focus:E06')
        self.env['r13_ep_cut_resume']()
        self.assertIsNone(state.r13_ep_cut_suspended)
        self.assertEqual(shown[0][1]['what']['items'][1]['art'], 'assets/evidence/E06.webp')
        self.assertEqual(state.r13_ep_cut_current, 'focus:E06')

    def test_action_closeups_downscale_smoothly_without_changing_existing_scene_cuts(self):
        for key in ('d07-nubi-fold', 'd07-sleeve-hold'):
            cut = self.env['r13_ep_cut_art'](key)
            self.assertFalse(cut['nearest'])
            self.assertEqual(cut['size'], (1280, 720))
            self.assertTrue((ROOT / 'game' / cut['art']).is_file())
        self.assertTrue(self.env['r13_ep_cut_art']('piko-death3')['nearest'])

    def test_authored_action_hides_only_the_listener_for_that_narration(self):
        source = (ROOT / 'game/systems/room13_ep_art.rpy').read_text()
        tree = ast.parse(textwrap.dedent(source.split('init 160 python:', 1)[1].split('\ntransform ', 1)[0]))
        node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'r13_ep_line_art')
        hidden = []
        env = dict(renpy=types.SimpleNamespace(hide=lambda tag: hidden.append(tag)))
        exec(compile(ast.Module(body=[node], type_ignores=[]), '행동 지문의 인물 그림', 'exec'), env)
        env['r13_ep_line_art']((None, '다람이 과자 봉지 끝을 접는다.', {'hide_listener': True}))
        self.assertEqual(hidden, ['r13_visitor'])
        hidden.clear()
        env['r13_ep_line_art']((None, '다람이 봉지를 바라본다.', {}))
        env['r13_ep_line_art'](('daram', '엄마 몫이야.', {'hide_listener': True}))
        self.assertEqual(hidden, [], '인물의 다음 발화나 지정하지 않은 지문에는 숨김을 적용하지 않는다.')

    def test_authored_cut_validation_requires_a_known_family_prop_and_real_asset(self):
        source = (ROOT / 'game/room13_v111_newworld_text.rpy').read_text()
        tree = ast.parse(textwrap.dedent(source.split('init 319 python:', 1)[1]))
        node = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'r13_nw_text_problems')
        row = dict(id='NW_FOCUS_TEST', speaker=None, text='접힌 종이를 본다.', kind='narration', cut='focus:E06')
        self.env.update(R13_V111={'records': {}}, R13_NW_TEXT=dict(replace={}, drop=[], before={}, after={}, blocks={'test': [row]}, evidence={}),
                        R13_NW_CUT_SPECIAL=(), MS14_SPEAKERS={}, R13_NW_WHEN={'always': True},
                        R13_MEETING_BEATS={}, R13_NW_FX={},
                        renpy=types.SimpleNamespace(loadable=lambda path: (ROOT / 'game' / path).is_file()))
        exec(compile(ast.Module(body=[node], type_ignores=[]), '가족 컷 자료 검증', 'exec'), self.env)
        self.assertEqual(self.env['r13_nw_text_problems'](), [])
        row['cut']='focus:E06_FIRE'  # 파일이 있어도 첫 발견 세 물건 외에는 허용하지 않는다.
        self.assertTrue(any('missing cut art' in problem for problem in self.env['r13_nw_text_problems']()))
        row['cut']='focus:E06'
        self.env['renpy'].loadable=lambda path: False
        self.assertTrue(any('missing cut art' in problem for problem in self.env['r13_nw_text_problems']()))


if __name__ == '__main__':
    unittest.main()
