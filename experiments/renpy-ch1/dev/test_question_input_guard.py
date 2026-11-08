"""A second tap must not consume the first answer; later input must still work."""
import ast,copy,textwrap,types,unittest
from pathlib import Path
class QuestionInputGuard(unittest.TestCase):
    def setUp(self):
        self.now=10.0
        self.engine=types.SimpleNamespace()
        self.store=types.SimpleNamespace(room13_mode=True)
        self.env=dict(renpy=self.engine,store=self.store,config=types.SimpleNamespace(say_allow_dismiss=None),Function=lambda f:f)
        source=(Path(__file__).resolve().parents[1]/'game/systems/room13_input_guard.rpy').read_text().split('init 147 python:\n')[1]
        exec(textwrap.dedent(source),self.env)
        self.env['r13_input_clock']=types.SimpleNamespace(monotonic=lambda:self.now)
    def test_rapid_second_tap_is_blocked_but_normal_reading_resumes(self):
        self.env['r13_mark_question_input']()
        self.now=10.1;self.assertFalse(self.env['r13_question_allow_dismiss']())
        self.now=10.36;self.assertTrue(self.env['r13_question_allow_dismiss']())
    def test_other_games_are_not_blocked(self):
        self.env['r13_mark_question_input']();self.store.room13_mode=False
        self.assertTrue(self.env['r13_question_allow_dismiss']())
    def test_existing_dismiss_restriction_is_preserved(self):
        self.env['_r13_before_question_dismiss']=lambda:False
        self.assertFalse(self.env['r13_question_allow_dismiss']())

    def field_fixture(self):
        self.pointer=(700,610)
        self.restarts=[]
        self.hub=types.SimpleNamespace(scope=dict(world_ready=False,world_moving=False,world_poll_left=12))
        self.engine.get_screen=lambda name:self.hub if name=='r13_hub' else None
        self.engine.get_mouse_pos=lambda:self.pointer
        self.engine.restart_interaction=lambda:self.restarts.append(True)
        self.engine.display=types.SimpleNamespace(interface=types.SimpleNamespace(last_event=types.SimpleNamespace(button=1,pos=self.pointer)))
        self.store.room13=dict(day=1,period=1,location='room13',evidence=['memo'])
        self.env['r13_question_allow_dismiss']()

    def test_same_place_rapid_tap_keeps_existing_guard(self):
        self.field_fixture();self.now=10.16
        self.assertFalse(self.env['r13_wake_field_pointer']())
        self.assertFalse(self.hub.scope['world_ready'])
        self.assertAlmostEqual(self.env['r13_field_ready_delay'](),.44)
        self.assertEqual(self.restarts,[])

    def test_deliberate_move_opens_after_base_delay_without_story_change(self):
        self.field_fixture();before=copy.deepcopy(self.store.room13)
        self.pointer=(540,430);self.now=10.10
        self.assertFalse(self.env['r13_wake_field_pointer']())
        self.now=10.16
        self.assertTrue(self.env['r13_wake_field_pointer']())
        self.assertTrue(self.hub.scope['world_ready'])
        self.assertEqual(self.hub.scope['world_poll_left'],0)
        self.assertEqual(self.restarts,[True])
        self.assertEqual(self.store.room13,before)
        self.assertFalse(self.env['r13_wake_field_pointer']())
        self.assertEqual(self.restarts,[True])

    def test_keyboard_and_modal_pan_do_not_open_from_pointer_motion(self):
        self.field_fixture()
        self.engine.display.interface.last_event=types.SimpleNamespace(key='K_RETURN')
        self.env['r13_question_allow_dismiss']()
        self.pointer=(520,400);self.now=10.16
        self.assertIsNone(self.engine._r13_last_advance_point)
        self.assertFalse(self.env['r13_wake_field_pointer']())
        self.engine._r13_last_advance_point=(700,610)
        self.hub.scope['world_moving']=True
        self.assertFalse(self.env['r13_wake_field_pointer']())
        self.assertFalse(self.hub.scope['world_ready'])

    def test_short_poll_really_stops_and_never_restarts_count(self):
        self.field_fixture();self.now=10.16
        for _ in range(12):self.env['r13_poll_field_pointer']()
        self.assertEqual(self.hub.scope['world_poll_left'],0)
        self.assertEqual(self.restarts,[True])
        for _ in range(20):self.env['r13_poll_field_pointer']()
        self.assertEqual(self.hub.scope['world_poll_left'],0)
        self.assertEqual(self.restarts,[True])
        self.assertFalse(self.hub.scope['world_ready'])

    def test_first_touch_down_can_enable_same_tap_release_without_consuming_it(self):
        self.field_fixture();self.now=10.16;self.pointer=(500,420)
        class Displayable:
            def __init__(self,**kwargs):pass
        self.engine.Displayable=Displayable
        source=(Path(__file__).resolve().parents[1]/'game/room13_feedback.rpy').read_text().split('init 69 python:',1)[1].split('\ntransform ',1)[0]
        node=next(node for node in ast.parse(textwrap.dedent(source)).body if isinstance(node,ast.ClassDef) and node.name=='R13FieldPointerGate')
        exec(compile(ast.Module(body=[node],type_ignores=[]),'현장 첫 터치', 'exec'),self.env)
        gate=self.env['R13FieldPointerGate']()
        self.assertIsNone(gate.event(types.SimpleNamespace(pos=self.pointer,button=1),*self.pointer,0))
        self.assertTrue(self.hub.scope['world_ready'])
        # 감시자가up을소비하지않으므로기존물건버튼이같은탭의up을받는다.
        self.assertIsNone(gate.event(types.SimpleNamespace(pos=self.pointer,button=1),*self.pointer,0))
        self.assertEqual(self.restarts,[True])
if __name__=='__main__':unittest.main()
