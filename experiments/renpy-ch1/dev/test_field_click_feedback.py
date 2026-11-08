"""조사 터치 여백의 반응 위치와 키보드 선택의 fallback을 검증한다."""
import ast
import copy
from pathlib import Path
import textwrap
import types
import unittest

ROOT = Path(__file__).resolve().parents[1]


class FieldClickFeedback(unittest.TestCase):
    def setUp(self):
        self.state = dict(location='room13', day=1, time=18, evidence=['memo'])
        self.calls = []
        self.mouse = (70, 80)
        self.env = dict(
            store=types.SimpleNamespace(room13=self.state),
            ROOM13=dict(objects=dict(room13=dict(mother_note=dict(rect=[200, 100, 120, 60])))),
            renpy=types.SimpleNamespace(get_mouse_pos=lambda: self.mouse,
                show_screen=lambda *args, **kwargs: self.calls.append((args, kwargs))),
            r13_screen_to_world=lambda point: (point[0] / .75 + 100, point[1] / .75),
            r13_world_to_screen=lambda point: ((point[0] - 100) * .75, point[1] * .75),
            r13_object_target_rect=lambda key, spec: (190, 90, 140, 80),
        )
        source = (ROOT / 'game/room13_feedback.rpy').read_text().split('init 69 python:', 1)[1].split('\ntransform ', 1)[0]
        tree = ast.parse(textwrap.dedent(source))
        function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'r13_click_feedback')
        exec(compile(ast.Module(body=[function], type_ignores=[]), '조사 클릭 반응', 'exec'), self.env)

    def test_tap_in_expanded_note_target_stays_at_pressed_screen_point(self):
        before = copy.deepcopy(self.state)
        # world x=193.33은 터치 여백 안, 원래 종이의 x=200 밖이다.
        self.env['r13_click_feedback']('mother_note')
        self.assertEqual(len(self.calls), 1)
        self.assertEqual(self.calls[0][0], ('r13_click_glint',))
        for actual, expected in zip(self.calls[0][1]['point'], self.mouse):
            self.assertAlmostEqual(actual, expected)
        self.assertEqual(self.state, before)

    def test_keyboard_selection_away_from_target_uses_object_center(self):
        self.mouse = (0, 0)
        self.env['r13_click_feedback']('mother_note')
        self.assertEqual(self.calls[0][1]['point'], (120, 97.5))

    def test_unknown_object_has_no_feedback_or_state_change(self):
        before = copy.deepcopy(self.state)
        self.env['r13_click_feedback']('missing')
        self.assertEqual(self.calls, [])
        self.assertEqual(self.state, before)

    def test_current_object_rect_is_used_when_no_touch_override_exists(self):
        del self.env['r13_object_target_rect']
        self.mouse = (0, 0)
        self.env['r13_click_feedback']('mother_note')
        self.assertEqual(self.calls[0][1]['point'], (120, 97.5))

    def test_hover_draws_only_short_corners_without_input_or_story_actions(self):
        operations=[]
        class FakeDisplayable:
            def __init__(self, **kwargs):
                pass
        class FakeRender:
            def __init__(self, width, height):
                self.size=(width,height)
            def canvas(self):
                return types.SimpleNamespace(lines=lambda *args:operations.append(args))
        source=(ROOT/'game/room13_feedback.rpy').read_text().split('init 69 python:',1)[1].split('\ntransform ',1)[0]
        node=next(node for node in ast.parse(textwrap.dedent(source)).body if isinstance(node,ast.ClassDef) and node.name=='R13ObjectHover')
        env=dict(renpy=types.SimpleNamespace(Displayable=FakeDisplayable,Render=FakeRender))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'조사 모서리', 'exec'),env)
        marker=env['R13ObjectHover']((240,160))
        self.assertEqual(marker.render(1280,720,0,0).size,(240,160))
        self.assertEqual(len(operations),4)
        for color,closed,points,thickness in operations:
            self.assertFalse(closed)
            self.assertEqual(thickness,1)
            for a,b in zip(points,points[1:]):
                self.assertLessEqual(abs(a[0]-b[0])+abs(a[1]-b[1]),8)
        self.assertNotIn('event',env['R13ObjectHover'].__dict__)
        self.assertEqual(self.calls,[])

    def test_scene_has_no_mouse_following_name_popup_and_keeps_single_tap_actions(self):
        source=(ROOT/'game/room13_screens.rpy').read_text()
        hub=source.split('screen r13_hub(',1)[1].split('\nscreen ',1)[0]
        world=source.split('screen r13_world_contents(',1)[1].split('\nscreen ',1)[0]
        residents=source.split('screen r13_resident_stage(',1)[1].split('\nscreen ',1)[0]
        self.assertNotIn('GetTooltip()',hub)
        self.assertNotIn('get_mouse_pos()',hub)
        self.assertNotIn('tooltip ',world)
        self.assertNotIn('tooltip ',residents)
        # 앞/뒤 두 물건 경로 모두 기존 한 번 누르기 행동을 그대로 쓴다.
        self.assertEqual(world.count('action [Function(r13_click_feedback,key),Return(("object",key))] sensitive ready'),2)
        self.assertEqual(world.count('alt r13_object_name(key)'),2)
        self.assertIn('alt (R13_EVENT_OFFERS',residents)


if __name__ == '__main__':
    unittest.main()
