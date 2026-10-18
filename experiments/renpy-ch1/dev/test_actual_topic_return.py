from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ActualTopicReturn(unittest.TestCase):
 def test_delegated_topic_screen_uses_reserved_right_slot(self):
  screens=(ROOT/'game/room13_screens.rpy').read_text()
  side=(ROOT/'game/systems/room13_side_questions.rpy').read_text()
  self.assertIn('use r13_side_question_list(person,pose,entries,ready,return_action,caption)',screens)
  self.assertIn('reserve_return=True',screens)
  self.assertIn('use r13_concept_action(R13_CONCEPT_RIGHT-232,232,"돌아가기"',side)
  self.assertNotIn('use r13_concept_action(28,192,"돌아가기"',side)
