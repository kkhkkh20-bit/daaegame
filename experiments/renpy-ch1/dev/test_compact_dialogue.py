"""Two-line panel geometry, independent of the native renderer.
Run native carriage / normal speech / large text checks before release.
"""
from type_stub import r13_type_stub
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
        env = dict(persistent=state, store=types.SimpleNamespace(r13_field_reading=False), r13_touch_ui=lambda:touch, r13_type=r13_type_stub(touch=touch,large=large,small=small),
                   r13_control_y=lambda:624 if large or touch else 640,
                   r13_read_size=lambda base,big:big if large else int(max(base-3,round(base*.9))) if small else base)
        for name in ('R13_SAY_TOP_NORMAL', 'R13_SAY_TOP_LARGE'):
            env[name] = int(re.search(r'define '+name+r' = (\d+)',SOURCE)[1])
        env['R13_LEGACY_SAY_SIZE'] = tuple(map(int,re.search(r'define R13_LEGACY_SAY_SIZE = \((\d+),(\d+),(\d+)\)',SOURCE).groups()))
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
        speech=SOURCE.split('# Approved B notebook dialogue;',1)[1].split('\nscreen choice(items):',1)[0]
        self.assertIn('size r13_night_say_size() line_spacing 4 xsize b_text_width font R13_UI_BOLD_FONT',speech)
        self.assertRegex(speech,r'text who id "who"[^\n]+font R13_UI_BOLD_FONT')
        self.assertIn('$ b_text_top = r13_night_say_top(what)',speech)
        self.assertIn('xpos b_text_x ypos b_text_top',speech)
        # 2026-10-28 소유자 「아빠라는 이름과 대사가 너무 붙어 있다」: 리본 가운데 = 종이 윗변 - 들어올린 만큼. 대사 첫 줄은
        # 윗변 + 리본이 들어온 깊이 + 여백. 리본 아래끝이 첫 줄보다 위다(보통·크게 모두).
        self.assertIn('xpos b_text_x ypos (r13_night_panel_top(what)-R13_SAY_RIBBON_LIFT) yanchor .5',speech)
        night=(ROOT/'game/systems/room13_night_ui.rpy').read_text(encoding='utf-8')
        val=lambda k:int(re.search(k+r'=(\d+)',night).group(1))
        ribbon_in,margin,lift=val('R13_SAY_RIBBON_IN'),val('R13_SAY_MARGIN'),val('R13_SAY_RIBBON_LIFT')
        name=speech.split('if who:',1)[1]
        padding=tuple(map(int,re.search(r'padding \((\d+),(\d+),(\d+),(\d+)\)',name).groups()))
        level=re.search(r'text who[^\n]+size \(?r13_type\("([a-z]+)"\)',name).group(1)
        for size in ({'small':20,'body':22,'emphasis':24,'subtitle':26,'title':28,'display':30}[level],{'small':24,'body':26,'emphasis':28,'subtitle':30,'title':32,'display':34}[level]):
            ribbon_bottom=-lift+(size*1.2+padding[1]+padding[3])/2
            self.assertGreaterEqual(ribbon_in+margin-ribbon_bottom,0)
        self.assertIn('background None padding (0,0)',speech)

if __name__=='__main__':
    unittest.main()
