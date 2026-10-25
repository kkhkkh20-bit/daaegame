"""수리 부탁·실제 작업·수리공 가용성을 구분한다."""
import ast,itertools,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class OwlRepair(unittest.TestCase):
 def setUp(self):
  src=(ROOT/'game/room13_v111_owl_prevent.rpy').read_text().split('init 322 python:',1)[1].split('\nlabel ',1)[0]
  src="\n".join(line for line in src.splitlines() if line.strip() and not line.lstrip().startswith("#"))
  tree=ast.parse(textwrap.dedent(src));self.values={};self.env=dict(r13_v111_value=self.values.get,r13_v111_set=self.values.__setitem__)
  exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<repair>','exec'),self.env)
 def test_available_requires_free_acquitted_living_tok(self):
  for meeting,alive,listed,departed,busy in itertools.product((None,'lose','partial','win'),(False,True),(False,True),(False,True),(None,'other','owl_repair7')):
   self.values.update({'meeting:lamp':meeting,'TOK_ALIVE':alive,'listed:resident_tok':listed,'departed:resident_tok':departed,'busy:resident_tok':busy})
   self.assertEqual(self.env['r13_owl_tok_available7'](),meeting in ('partial','win') and alive and not listed and not departed and busy in (None,'owl_repair7'))
 def test_only_our_reservation_is_released(self):
  for busy in ('owl_repair7','other',None):
   self.values.update({'busy:resident_tok':busy,'location:resident_tok':'room13'})
   self.env['r13_owl_tok_release7']()
   self.assertEqual(self.values['busy:resident_tok'],False if busy=='owl_repair7' else busy)
   self.assertEqual(self.values['location:resident_tok'],None if busy=='owl_repair7' else 'room13')
 def test_agreement_does_not_finish_work(self):
  s=(ROOT/'game/room13_v111_owl_prevent.rpy').read_text()
  agreed=s.split('elif n==111',1)[1].split('elif n==112',1)[0]
  self.assertNotIn("set('owl_tok_work7'",agreed)
  b=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['free_day7']['options']
  work=next(o for o in b if o.get('index')==112)
  self.assertIn(['state','owl_tok_agreed7',True],work['guard'])
  self.assertEqual(len({o.get('index',i) for i,o in enumerate(b)}),len(b))
if __name__=='__main__':unittest.main()
