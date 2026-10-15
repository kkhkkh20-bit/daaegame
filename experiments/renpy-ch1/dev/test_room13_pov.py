"""Father viewpoint contract against the actual speaker function, no renderer mocks claimed as visual QA."""
import ast
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / 'game/room13_rules.rpy').read_text()
START = SOURCE.index('    def r13_speaker(')
END = SOURCE.index('\n    def ', START + 1)
CODE = compile(ast.parse(textwrap.dedent(SOURCE[START:END])), str(ROOT / 'game/room13_rules.rpy'), 'exec')

class ViewpointSpeaker(unittest.TestCase):
    def setUp(self):
        self.tags = {'r13_visitor'}
        self.calls = []
        self.store = SimpleNamespace(r13_current_pose='distressed', dialogue_speaker='karo',
            dialogue_expression='distressed', r13_camera='stage', place='눈에 막힌 입구', r13_motion_person='karo')
        def show(name, **kwargs):
            self.calls.append(('show', name, kwargs)); self.tags.add(kwargs.get('tag', name))
        def hide(name):
            self.calls.append(('hide', name)); self.tags.discard(name)
        env = {'store':self.store,
            'renpy':SimpleNamespace(get_showing_tags=lambda:list(self.tags),show=show,hide=hide),
            'CAST':{person:{'avatar_neutral':{},'avatar_thinking':{},'avatar_distressed':{}} for person in ('dad','karo','guard','daram')},
            'r13_conversation_pose':lambda person,pose:pose,
            'r13_acting_spec':lambda person,pose:True,
            'r13_close_art':lambda *args:args,
            'r13_close_y':lambda *args,**kwargs:126,
            'r13_portrait_close':lambda y,x=640:y,
            'r13_close_x':lambda *args,**kwargs:640,
            'r13_carriage_pop':'pop',
            # 0.18.33 expression reactions (systems/room13_dot_fx.rpy): none in this contract.
            'r13_react_kind':lambda *args:None,
            'r13_react':lambda kind,who,pose,what,at_list:(what,at_list)}
        exec(CODE, env)
        self.speak = env['r13_speaker']
    def test_father_reply_retains_target_pose_without_reentry(self):
        self.speak('dad','thinking','thinking')
        self.assertEqual((self.store.r13_motion_person,self.store.r13_current_pose),('karo','distressed'))
        self.assertEqual(self.calls,[])
        self.assertIsNone(self.store.dialogue_speaker) # native Character callback sets Dad later
        self.assertEqual(self.store.dialogue_expression,'thinking')
    def test_target_continues_after_father_without_reentry(self):
        self.speak('dad','thinking','thinking');self.speak('karo','distressed','distressed')
        self.assertEqual(self.calls,[])
    def test_actual_target_change_replaces_visitor(self):
        self.speak('dad','thinking');self.speak('guard','neutral')
        self.assertEqual(self.store.r13_motion_person,'guard')
        self.assertEqual(self.calls[0][0],'show')
        self.assertEqual(self.calls[0][2]['what'][0],'guard')
        self.assertTrue(self.calls[0][2]['what'][-1]) # new-target entrance
    def test_carriage_draws_only_daram(self):
        self.store.place='마차 안';self.speak('dad','thinking')
        self.assertNotIn('r13_visitor',self.tags);self.assertIsNone(self.store.r13_motion_person)
        self.speak('karo','neutral')
        self.assertNotIn('r13_visitor',self.tags)
        self.speak('daram','joy')
        self.assertEqual(self.store.r13_motion_person,'daram')
        self.assertEqual(self.calls[-1][2]['what'][0],'daram')
        self.assertIs(self.calls[-1][2]['at_list'][-1],'pop') # springs up, no fade
        self.assertFalse(self.calls[-1][2]['what'][-1])
        shown=len(self.calls)
        self.speak('dad','thinking');self.speak('karo','neutral')
        self.assertEqual(len(self.calls),shown);self.assertEqual(self.store.r13_motion_person,'daram')
    def test_nonstage_never_keeps_stage_visitor(self):
        self.store.r13_camera='cinematic';self.speak('dad')
        self.assertNotIn('r13_visitor',self.tags);self.assertIsNone(self.store.r13_motion_person)
    def test_father_without_existing_target_never_draws_father(self):
        for person,tags in ((None,set()),('dad',{'r13_visitor'}),('karo',set())):
            with self.subTest(person=person,tags=tags):
                self.calls.clear();self.tags=set(tags);self.store.r13_motion_person=person;self.speak('dad')
                self.assertFalse(any(c[0]=='show' for c in self.calls));self.assertIsNone(self.store.r13_motion_person)

if __name__=='__main__':unittest.main()
