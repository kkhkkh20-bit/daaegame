import ast
import re
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class ActualTopicReturn(unittest.TestCase):
 def test_delegated_topic_screen_keeps_its_original_return_action(self):
  screens=(ROOT/'game/room13_screens.rpy').read_text()
  side=(ROOT/'game/systems/room13_side_questions.rpy').read_text()
  self.assertIn('use r13_side_question_list(person,pose,entries,ready,return_action,caption)',screens)
  self.assertIn('use r13_notebook_topic_tools(ready,person,present_action)',screens)
  # The return action travels through the same notebook/state component as the
  # other tools. Its coordinates may change; its action and readiness may not.
  match=re.search(r'if return_action is not None:\n\s+use (r13_notebook_topic_action\([^\n]+\))',side)
  self.assertIsNotNone(match)
  call=ast.parse(match.group(1),mode='eval').body
  self.assertEqual(ast.literal_eval(call.args[2]),'돌아가기')
  self.assertEqual(ast.unparse(call.args[3]),'return_action')
  self.assertEqual(ast.unparse(call.args[4]),'ready')
  helper=side.split('screen r13_notebook_topic_action(',1)[1].split('\nscreen ',1)[0]
  state_call=ast.parse(re.search(r'use (r13_state_button\([^\n]+\))',helper).group(1),mode='eval').body
  self.assertEqual(ast.unparse(state_call.args[1]),'command')
  self.assertEqual({k.arg:ast.unparse(k.value) for k in state_call.keywords}['enabled'],'ready')
  state=(ROOT/'game/room13_button_states.rpy').read_text().split('screen r13_state_button(',1)[1]
  self.assertIn('action command sensitive enabled',state)
