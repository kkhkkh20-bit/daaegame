"""배식 전 중단은 관찰만으로 확정하지 않고 실제 분리·확인까지 요구한다."""
import ast,itertools,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SoupPreparation(unittest.TestCase):
 def setUp(self):
  s=(ROOT/'game/room13_v111_days1114.rpy').read_text().split('init 324 python:',1)[1].split('\n# Reviewed',1)[0]
  tree=ast.parse(textwrap.dedent(s));self.values={}
  self.env=dict(r13_v111_value=self.values.get)
  exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_soup_inspect_ready12'],type_ignores=[]),'<soup>','exec'),self.env)
 def test_all_three_actual_observations_required(self):
  keys=('soup_smallpot_seen12','soup_bowls_seen12','soup_bottle_seen12')
  for bits in itertools.product((None,True),repeat=3):
   self.values.update(zip(keys,bits));self.assertEqual(self.env['r13_soup_inspect_ready12'](),all(bits))
 def test_early_preparation_does_not_synthesize_inspection(self):
  self.values.update(dict.fromkeys(('medicine_locked','warm_seat_ready','carrier_arrived','warm_support_arrived'),True))
  self.assertFalse(self.env['r13_soup_inspect_ready12']())
 def test_observing_never_mutates_route_or_legacy_flags(self):
  self.values.update(route12='uncommitted',medicine_locked=True,daram_fever12=True)
  before=dict(self.values);self.env['r13_soup_inspect_ready12']();self.assertEqual(self.values,before)
 def test_finish_option_requires_observations_and_exit_remains(self):
  b=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['meal_inspect12']['options']
  self.assertEqual(len(b[3]['guard']),3)
  self.assertTrue(all(g[2] is True for g in b[3]['guard']))
  self.assertFalse(b[4].get('guard'))
 def test_cabinet_lock_does_not_claim_outside_bottle_returned(self):
  j=json.loads((ROOT/'game/v111/newworld/d12.json').read_text());text=j['replace']['MS14_D12_S01_L0025']['text']
  self.assertIn('밖으로 나간 병은 별개',text);self.assertIn('따로 확인',text)
if __name__=='__main__':unittest.main()
