"""Display-only punctuation timing regression checks, without starting Ren'Py."""
import re
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

SOURCE = Path(__file__).resolve().parents[1] / 'game/room13_dialogue_rhythm.rpy'

class RhythmTests(unittest.TestCase):
    def setUp(self):
        self.preferences = SimpleNamespace(text_cps=34)
        self.skipping = False
        self.env = dict(preferences=self.preferences,
                        renpy=SimpleNamespace(is_skipping=lambda: self.skipping))
        exec(textwrap.dedent(SOURCE.read_text().split('init 62 python:\n',1)[1].split('    class R13DialogueText',1)[0]), self.env)
        self.rhythm = self.env['r13_rhythmic_text']

    def added_delays(self, value):
        return [1/float(rate)-1/self.preferences.text_cps
                for rate in re.findall(r'\{cps=([0-9.]+)\}', value)]

    def test_pause_follows_punctuation_and_preserves_text(self):
        text = '응, 알겠어. 다시 볼까? 좋아!'
        out = self.rhythm(text)
        self.assertIn('응,{cps=', out)
        self.assertEqual(re.sub(r'\{/?cps[^}]*\}', '', out), text)
        self.assertEqual([round(x,2) for x in self.added_delays(out)], [.12,.26,.26])
        self.assertNotIn('{w', out)

    def test_ellipsis_and_combined_end_are_single_pauses(self):
        out = self.rhythm('잠깐... 응?! 그래…… 이제.')
        self.assertEqual([round(x,2) for x in self.added_delays(out)], [.30,.26,.30])

    def test_numbers_markup_and_interpolation_are_preserved(self):
        text='1.5와 1,000개 {color=#fff}확인,{/color} [name]에게.'
        out=self.rhythm(text)
        self.assertIn('1.5와 1,000개',out)
        self.assertIn('{color=#fff}',out)
        self.assertIn('[name]',out)
        self.assertEqual(len(self.added_delays(out)),1)

    def test_long_line_delay_is_bounded(self):
        out=self.rhythm('그래. '*40)
        self.assertLessEqual(sum(self.added_delays(out)),1.20001)

    def test_instant_skip_and_authored_speed_are_unchanged(self):
        text='응, 알겠어. 다음.'
        self.preferences.text_cps=0
        self.assertEqual(self.rhythm(text),text)
        self.preferences.text_cps=34
        self.skipping=True
        self.assertEqual(self.rhythm(text),text)
        self.skipping=False
        custom='{cps=12}응, 알겠어.{/cps}'
        self.assertEqual(self.rhythm(custom),custom)

    def test_typing_counts_visible_letters_but_not_spaces_or_future_glyphs(self):
        audible=self.env['r13_typing_glyph']
        self.assertTrue(audible(SimpleNamespace(time=.1,character=ord('가')),.2))
        for char in (' ', '\t', '\n', '\u3000'):
            self.assertFalse(audible(SimpleNamespace(time=.1,character=ord(char)),.2))
        self.assertFalse(audible(SimpleNamespace(time=.3,character=ord('나')),.2))

if __name__=='__main__': unittest.main()
