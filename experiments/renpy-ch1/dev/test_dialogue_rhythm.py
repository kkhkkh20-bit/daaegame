"""Display-only punctuation timing regression checks, without starting Ren'Py."""
import ast
import copy
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


class TypingLifecycleTests(unittest.TestCase):
    """음향 작업만 줄인다. Character의 글자 표시·입력·대사는 건드리지 않는다."""
    def setUp(self):
        self.restarts=[]
        self.played=[]
        self.stopped=[]
        self.screens={'say'}
        self.layout_reads=0
        self.preferences=SimpleNamespace(text_cps=34)
        self.persistent=SimpleNamespace(room13_typing_sound=True)
        self.store=SimpleNamespace(room13_mode=True,r13_typing_active=False,typing_allowed=True,
                                   room13={'day':1,'evidence':['E01'],'flags':[]})
        self.layout=SimpleNamespace(paragraph_glyphs=[[SimpleNamespace(time=t) for t in (.1,.2,.3,.4)]])
        owner=self
        class Text:
            def __init__(self,*args,**kwargs):
                self.text=list(args)
                self.slow=True
            def per_interact(self):pass
            def render(self,*args):return '그림'
            def get_layout(self):
                owner.layout_reads+=1
                return owner.layout
        self.renpy=SimpleNamespace(
            text=SimpleNamespace(text=SimpleNamespace(Text=Text)),
            get_screen=lambda name:name in self.screens,
            get_displayable=lambda *args:self.text,
            is_skipping=lambda:False,
            restart_interaction=lambda:self.restarts.append(True),
            music=SimpleNamespace(play=lambda *args,**kw:self.played.append((args,kw)),
                                  stop=lambda **kw:self.stopped.append(kw)))
        self.env=dict(renpy=self.renpy,preferences=self.preferences,persistent=self.persistent,store=self.store)
        tree=ast.parse(textwrap.dedent(SOURCE.read_text().split('init 62 python:\n',1)[1]))
        names={'R13DialogueText','r13_typing_visual_enabled','r13_typing_timer_needed',
               'r13_typing_lifecycle','r13_typing_after_load','r13_typing_tick'}
        nodes=[node for node in tree.body if isinstance(node,(ast.FunctionDef,ast.ClassDef)) and node.name in names]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'타이핑 표시 수명','exec'),self.env)
        self.text=self.env['R13DialogueText']('응, 알겠어.')

    def event(self,name,**kwargs):self.env['r13_typing_lifecycle'](name,**kwargs)
    def wanted(self):return self.env['r13_typing_timer_needed']()
    def draw(self,t):return self.text.render(700,100,t,t)

    def test_timer_exists_only_while_characters_are_appearing(self):
        before=copy.deepcopy(self.store.room13)
        self.assertFalse(self.wanted())
        self.event('show');self.assertTrue(self.wanted())
        self.event('slow_done');self.assertFalse(self.wanted())
        self.event('slow_done');self.event('end')
        self.assertEqual(self.restarts,[True])
        self.assertEqual(self.store.room13,before)

    def test_wait_fragment_rearms_without_changing_dialogue(self):
        self.event('show');self.event('slow_done');self.assertFalse(self.wanted())
        self.event('show');self.assertTrue(self.wanted())
        self.event('slow_done');self.assertEqual(len(self.restarts),2)
        self.assertEqual(self.text.text,['응, 알겠어.'])

    def test_muted_instant_skipped_or_overlay_never_requests_timer(self):
        self.event('show')
        self.persistent.room13_typing_sound=False;self.assertFalse(self.wanted())
        self.persistent.room13_typing_sound=True;self.preferences.text_cps=0;self.assertFalse(self.wanted())
        self.preferences.text_cps=34;self.renpy.is_skipping=lambda:True;self.assertFalse(self.wanted())
        self.renpy.is_skipping=lambda:False;self.screens.add('pause_menu');self.assertFalse(self.wanted())
        self.screens.remove('pause_menu');self.assertTrue(self.wanted())

    def test_no_glyph_count_after_completion_or_when_muted(self):
        self.event('show');self.persistent.room13_typing_sound=False
        self.assertEqual(self.draw(.2),'그림');self.assertEqual(self.layout_reads,0)
        self.persistent.room13_typing_sound=True;self.event('slow_done');self.draw(.5)
        self.assertEqual(self.layout_reads,0)

    def test_reenabled_sound_does_not_replay_old_glyphs(self):
        self.event('show');self.persistent.room13_typing_sound=False;self.draw(.2)
        self.persistent.room13_typing_sound=True;self.draw(.3);self.env['r13_typing_tick']()
        self.assertEqual(self.played,[])
        self.draw(.4);self.env['r13_typing_tick']();self.assertEqual(len(self.played),1)

    def test_menu_reentry_keeps_already_shown_glyphs_silent(self):
        self.event('show');self.draw(.2);self.env['r13_typing_tick']();self.played.clear()
        self.screens.add('pause_menu');self.text.per_interact()
        self.screens.remove('pause_menu');self.text.per_interact();self.draw(.3)
        self.env['r13_typing_tick']();self.assertFalse(self.played)
        self.draw(.4);self.env['r13_typing_tick']();self.assertEqual(len(self.played),1)

    def test_load_handles_completed_and_unfinished_text_without_replay(self):
        self.text.r13_revealed=3;self.text.slow=False
        self.env['r13_typing_after_load']();self.assertFalse(self.wanted())
        self.text.slow=True;self.env['r13_typing_after_load']();self.assertTrue(self.wanted())
        self.assertFalse(self.text.r13_audio_enabled)
        self.draw(.3);self.env['r13_typing_tick']();self.assertFalse(self.played)
        self.draw(.4);self.env['r13_typing_tick']();self.assertEqual(len(self.played),1)

    def test_noninteractive_character_and_legacy_mode_are_untouched(self):
        self.event('show',interact=False);self.assertFalse(self.store.r13_typing_active)
        self.store.room13_mode=False;self.event('show');self.assertFalse(self.store.r13_typing_active)

    def test_all_say_branches_gate_audio_timer(self):
        screens=(SOURCE.parent/'screens.rpy').read_text()
        timer='timer .02 repeat True action Function(r13_typing_tick, _update_screens=False)'
        self.assertEqual(screens.count('if r13_typing_timer_needed():\n            '+timer),3)

if __name__=='__main__': unittest.main()
