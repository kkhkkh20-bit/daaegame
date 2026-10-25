"""공개 전 물건과 감독자 실제 배치로 판정하며 다른 감독 임무를 빼앗지 않는다."""
import ast,itertools,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class CrowdPreparation(unittest.TestCase):
 def setUp(self):
  s=(ROOT/'game/room13_v111_days1114.rpy').read_text().split('init 324 python:',1)[1].split('\n# Reviewed',1)[0]
  tree=ast.parse(textwrap.dedent(s));self.values={};self.alive=True
  self.env=dict(r13_v111_value=self.values.get,r13_v111_set=self.values.__setitem__,r13_v111_person_alive=lambda p:self.alive)
  funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name.startswith('r13_crowd_')]
  exec(compile(ast.Module(body=funcs,type_ignores=[]),'<crowd>','exec'),self.env)
 def test_each_placement_and_current_reserved_supervisor_required(self):
  keys=('crowd_records_spaced13','crowd_cart_spaced13','crowd_supervisor_placed13')
  for bits in itertools.product((None,True),repeat=3):
   self.values.update(zip(keys,bits));self.values['busy:guard']='crowd_supervision'
   self.assertEqual(bool(self.env['r13_crowd_prepared13']()),all(bits))
  self.values['busy:guard']='silluk_supervision';self.assertFalse(self.env['r13_crowd_prepared13']())
 def test_unavailable_guard_cannot_be_reserved(self):
  f=self.env['r13_crowd_guard_available13'];self.assertTrue(f())
  for k,v in [('busy:guard','silluk_supervision'),('location:guard','v111_labor'),('listed:guard',True),('departed:guard',True)]:
   self.values[k]=v;self.assertFalse(f());self.values.pop(k)
  self.alive=False;self.assertFalse(f())
 def test_reservation_is_not_an_extra_free_guard(self):
  self.values['busy:guard']='crowd_supervision'
  self.assertFalse(self.env['r13_crowd_guard_available13']())
  self.assertTrue(self.env['r13_crowd_guard_available13'](True))
 def test_release_never_erases_other_custody(self):
  self.values.update({'busy:guard':'silluk_supervision','crowd_supervisor_placed13':True})
  self.env['r13_crowd_release13']();self.assertEqual(self.values['busy:guard'],'silluk_supervision')
  self.values['busy:guard']='crowd_supervision';self.env['r13_crowd_release13']();self.assertFalse(self.values['busy:guard'])
 def test_preparation_always_allows_publication_or_return(self):
  b=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['crowd_prepare13']
  self.assertFalse(b['options'][3].get('guard'));self.assertFalse(b['options'][4].get('guard'))
  self.assertEqual(len(b['options'][2]['guard']),3)
if __name__=='__main__':unittest.main()
