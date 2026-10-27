"""Two-line panel geometry, independent of the native renderer.
Run native carriage / normal speech / large text checks before release.
"""
import re
import textwrap
import types
import unittest
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT/'game/screens.rpy').read_text(encoding='utf-8')
block = SOURCE.split('    def _r13_say_size():', 1)[1].split('\nscreen say(', 1)[0]
block = '    def _r13_say_size():' + block

class CompactDialogue(unittest.TestCase):
    def env(self, large=False, touch=False, small=False):
        state = types.SimpleNamespace(room13_large_text=large)
        env = dict(persistent=state, store=types.SimpleNamespace(r13_field_reading=False), r13_touch_ui=lambda:touch, R13_TYPE_V2=False,
                   r13_control_y=lambda:624 if large or touch else 640,
                   r13_read_size=lambda base,big:big if large else int(max(base-3,round(base*.9))) if small else base)
        for name in ('R13_SAY_TOP_NORMAL', 'R13_SAY_TOP_LARGE'):
            env[name] = int(re.search(r'define '+name+r' = (\d+)',SOURCE)[1])
        exec(textwrap.dedent(block),env)
        return env

    def test_two_line_baseline_and_footer_clearance(self):
        for large,touch,small,size,height in ((False,False,False,28,104),(False,True,False,31,112),(True,False,False,31,112),(False,False,True,25,104)):
            with self.subTest(large=large,touch=touch,small=small):
                env=self.env(large,touch,small)
                top=env['_r13_say_top']('첫 줄입니다.\n둘째 줄입니다.')
                self.assertEqual(env['_r13_say_size'](),size)
                self.assertEqual(env['r13_control_y']()-16-top,height)
                self.assertLessEqual(2*size+7+24,height)
                self.assertEqual(top,env['_r13_say_top']('한 줄입니다.'))

    def test_direct_say_overflow_is_not_cropped(self):
        env=self.env()
        self.assertEqual(env['_r13_say_top']('첫 줄.\n둘째 줄.\n셋째 줄.'),env['_r13_say_top']('첫 줄.')-35)

    def test_same_font_and_name_anchor(self):
        # Approved B dialogue: the real Bold font is shared by text and name;
        # the ribbon stays anchored to the text as long lines move upward.
        speech=SOURCE.split('# Approved B notebook dialogue;',1)[1].split('\nstyle legacy_choice_frame',1)[0]
        self.assertIn('size r13_night_say_size() line_spacing 4 xsize b_text_width font R13_UI_BOLD_FONT',speech)
        self.assertRegex(speech,r'text who id "who"[^\n]+font R13_UI_BOLD_FONT')
        self.assertIn('$ b_text_top = r13_night_say_top(what)',speech)
        self.assertIn('xpos b_text_x ypos b_text_top',speech)
        offset=int(re.search(r'xpos b_text_x ypos \(r13_night_say_top\(what\)-(\d+)\)',speech).group(1))
        name=speech.split('if who:',1)[1]  # 2026-10-26 이름표 페이드를 뺐다. 이름표 덩어리는 if who: 뒤에 있다
        padding=tuple(map(int,re.search(r'padding \((\d+),(\d+),(\d+),(\d+)\)',name).groups()))
        sizes=tuple(map(int,re.search(r'text who[^\n]+size r13_read_size\((\d+),(\d+)\)',name).groups()))
        for size in sizes:self.assertGreaterEqual(offset-size-padding[1]-padding[3],8)
        self.assertIn('background None padding (0,0)',speech)

if __name__=='__main__':
    unittest.main()
