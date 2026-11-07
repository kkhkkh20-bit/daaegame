"""휴대폰 질문은 같은 크기로 재고 그리며 원래 PC 배치와 질문을 보존한다."""
import ast
from pathlib import Path
import textwrap
import types
import unittest
from test_type_scale import load_scale

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'game/systems/room13_side_questions.rpy').read_text()


class SideQuestionMobile(unittest.TestCase):
    def env(self, touch=False, large=False):
        env = load_scale(touch=touch, large=large)
        calls = []

        def text(label, **kw):
            calls.append(kw)
            # 실제 글꼴 캡처는 native 시험으로 확인한다. 여기서는 폭·크기에 비례하는 줄바꿈을 재현한다.
            lines = max(1, (len(label) * kw['size'] + kw['xsize'] - 1) // kw['xsize'])
            return types.SimpleNamespace(height=lines * int(kw['size'] * 1.4))

        env.update(Text=text, renpy=types.SimpleNamespace(render=lambda obj, *args: types.SimpleNamespace(get_size=lambda: (538, obj.height))),
                   R13_UI_BOLD_FONT='font', r13_question_caption=lambda label, *a, **kw: label)
        code = SOURCE.split('init 80 python:\n', 1)[1].split('\nscreen ', 1)[0]
        exec(textwrap.dedent(code), env)
        env['text_calls'] = calls
        return env

    def test_mobile_uses_larger_body_and_footer_without_changing_pc(self):
        pc = self.env()['r13_side_question_layout']()
        self.assertEqual(pc, dict(left=572, width=608, text_left=82, text_width=506, tool_width=146, body_size=24, tool_size=22))
        for large in (False, True):
            env = self.env(touch=True, large=large)
            layout = env['r13_side_question_layout']()
            self.assertEqual(layout['body_size'], env['r13_type']('subtitle'))
            self.assertEqual(layout['tool_size'], env['r13_type']('subtitle'))
            self.assertGreater(layout['body_size'], env['r13_type']('emphasis'))
            self.assertGreaterEqual(layout['body_size'] * 390 / 720, 17)
            self.assertEqual(layout['left'] + layout['width'], 1192)
            self.assertEqual(4 * layout['tool_width'] + 3 * 8, layout['width'])

    def test_measurement_and_rendering_share_size_width_and_complete_rows(self):
        entries = [('이 긴 질문도 앞뒤가 잘리지 않고 온전히 보여야 합니다. ' + str(i), i, False) for i in range(18)]
        for touch in (False, True):
            for large in (False, True):
                env = self.env(touch=touch, large=large)
                layout = env['r13_side_question_layout']()
                pages = env['r13_side_question_pages'](entries)
                self.assertEqual([entry for page in pages for entry, height in page], entries)
                bottom = env['r13_notebook_topic_y']() - (96 if touch else 60) - 12
                for page in pages:
                    self.assertLessEqual(228 + sum(height for entry, height in page) + 8 * (len(page) - 1), bottom)
                self.assertTrue(all(call['size'] == layout['body_size'] and call['xsize'] == layout['text_width'] for call in env['text_calls']))
        self.assertIn('xsize L["text_width"] size L["body_size"]', SOURCE)

    def test_mobile_footer_keeps_actions_and_uses_common_paper_without_text_fit(self):
        helper = SOURCE.split('screen r13_notebook_topic_action(', 1)[1].split('\nscreen ', 1)[0]
        mobile, pc = helper.split('if r13_touch_ui():', 1)[1].split('\n        else:', 1)
        self.assertIn('action command sensitive ready', mobile)
        self.assertIn('text caption xsize (w-8)', mobile)
        self.assertIn('size r13_side_question_layout()["tool_size"]', mobile)
        self.assertNotIn('R13ButtonStateVisual', mobile)
        self.assertIn('use r13_state_button(caption,command,w,64', pc)
        self.assertIn('R13SoftButtonSurface(hovered=hovered,disabled=not enabled)', SOURCE)


if __name__ == '__main__':
    unittest.main()
