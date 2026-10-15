"""A second tap must not consume the first answer; later input must still work."""
import textwrap,types,unittest
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
if __name__=='__main__':unittest.main()
