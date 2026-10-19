from pathlib import Path
import ast,textwrap,unittest
root=Path(__file__).resolve().parents[1]/'game'
code=textwrap.dedent((root/'qa_tests/character_grid2_contexts.rpy').read_text().split('init 990 python:\n',1)[1].split('\n# Explicit screen fixture',1)[0])
module=ast.parse(code)
functions=ast.Module(body=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='r13_c4_bad'],type_ignores=[])
ns={};exec(compile(functions,'grid-contract','exec'),ns)
bad=ns['r13_c4_bad']
class Contract(unittest.TestCase):
 def test_flat(self): self.assertEqual(bad(bytes([21,32,43,127])*16,(4,4)),0)
 def test_rgba_channels(self):
  for channel in range(4):
   data=bytearray([21,32,43,127]*16);data[4+channel]+=1
   self.assertEqual(bad(data,(4,4)),1)
 def test_even(self):
  with self.assertRaises(AssertionError):bad(bytes(36),(3,3))
 def test_production_not_enabled_by_import(self):
  self.assertNotIn('R13_CHARACTER_GRID2_ENABLED=True',code.split('def r13_c4_begin')[0])
 def test_capture_no_rescale(self):
  self.assertIn('resize=False',code);self.assertNotIn('smoothscale',code)
 def test_real_flow_retained(self):
  cases=(root/'qa_tests/character_grid2_context_cases.rpy').read_text()
  for marker in ['click pos (r13_pd_person_x,r13_pd_person_y)','r13_pd_assert_topic_say','r13_pd_choose_object','room13==r13_qa_admin_before','r13_c4_require_profile_size,(48,48)','r13_c4_require_profile_size,(60,62)']:
   self.assertIn(marker,cases)
if __name__=='__main__':unittest.main()
