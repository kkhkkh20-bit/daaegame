"""Pure source/logic regression. No RenPy import or SDK execution."""
import ast
import os
from pathlib import Path
import textwrap
import unittest

ROOT=Path(os.environ.get('R13_HINT_SOURCE_ROOT',Path(__file__).resolve().parents[1]/'game'))
FIELD=ROOT/'systems/room13_field_views.rpy'
CAMERA=ROOT/'room13_world_camera.rpy'

class FieldHintUnification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.field=FIELD.read_text();cls.camera=CAMERA.read_text()
        block=cls.field.split('init 85 python:\n',1)[1].split('\nscreen ',1)[0]
        tree=ast.parse(textwrap.dedent(block))
        fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_field_hint_state')
        namespace={};exec(compile(ast.Module(body=[fn],type_ignores=[]),'<pure hint function>','exec'),namespace)
        cls.state=staticmethod(namespace['r13_field_hint_state'])

    def test_new_narrow_scene_does_not_consume_wide_discovery(self):
        self.assertEqual(self.state('inn',False,(),False),(True,False))
        self.assertEqual(self.state('inn',False,('inn',),False),(False,False))
        self.assertEqual(self.state('workshop',True,('inn',),False),(True,True))

    def test_scene_seen_old_save_still_gets_first_wide_instruction(self):
        self.assertEqual(self.state('inn',True,('inn',),False),(False,True))

    def test_pan_seen_old_save_keeps_new_place_instruction(self):
        self.assertEqual(self.state('inn',True,(),True),(True,False))
        self.assertEqual(self.state('inn',True,('inn',),True),(False,False))

    def test_three_second_scene_expiry_leaves_six_second_pan_instruction(self):
        self.assertEqual(self.state('post',True,(),False),(True,True))
        self.assertEqual(self.state('post',True,('post',),False),(False,True))
        self.assertEqual(self.state('post',True,('post',),True),(False,False))

    def test_single_panel_owner_and_existing_state_timers(self):
        screen=self.field.split('screen r13_field_view_controls(ready):',1)[1]
        self.assertEqual(screen.count('        frame:'),1)
        self.assertIn('if scene_hint or pan_hint:',screen)
        self.assertIn('timer 3.0 action SetVariable("r13_scene_hint_seen"',screen)
        self.assertIn('timer 6.0 action SetField(persistent,"r13_pan_hint_seen",True)',screen)
        self.assertNotIn('화면을 좌우로 끌면 옆을 둘러볼 수 있다',self.camera)
        self.assertNotIn('timer 6.0 action SetField(persistent,"r13_pan_hint_seen"',self.camera)
        self.assertIn('default persistent.r13_pan_hint_seen = False',self.camera)
        self.assertIn('default r13_scene_hint_seen = ()',self.field)

if __name__=='__main__':unittest.main()
