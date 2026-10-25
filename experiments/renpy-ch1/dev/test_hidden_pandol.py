"""판돌 가족의 보호는 수리만으로 완성되지 않으며 기존 운명을 바꾸지 않는다."""
import ast,itertools,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class HiddenPandol(unittest.TestCase):
 def setUp(self):
  source=(ROOT/'game/room13_hidden_pandol.rpy').read_text().split('init 324 python:',1)[1].split('\nlabel ',1)[0]
  tree=ast.parse(textwrap.dedent(source));self.values={}
  self.env=dict(r13_v111_value=self.values.get,r13_v111_set=self.values.__setitem__)
  exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)],type_ignores=[]),'<family>','exec'),self.env)
 def put(self,**values):self.values.update({'hidden_pandol:'+k:v for k,v in values.items()})
 def test_heat_requires_each_real_step_and_won_meeting(self):
  keys=('family_seen','stove_seen','consent','wood_delivered','tongs')
  for result in ('win','partial','lose',None):
   for bits in itertools.product((False,True),repeat=len(keys)):
    self.values['meeting:hypothesis']=result;self.put(**dict(zip(keys,bits)))
    self.assertEqual(bool(self.env['r13_hp_heat_ready']()),result=='win' and all(bits))
  self.values['meeting:hypothesis']='win';self.put(**dict.fromkeys(keys,True),heat_replaced=True)
  self.assertFalse(self.env['r13_hp_heat_ready']())
 def test_reserved_wood_requires_actual_school_delivery(self):
  self.put(family_seen=True);self.values['meeting:hypothesis']='win'
  self.assertFalse(self.env['r13_hp_wood_ready']())
  self.values['school_supply_handed']=True;self.assertTrue(self.env['r13_hp_wood_ready']())
 def test_no_handover_to_missing_listed_or_departed_receiver(self):
  self.put(heat_replaced=True)
  self.assertTrue(self.env['r13_hp_receiver_ready']())
  for key,value in [('listed:nabi',True),('departed:nabi',True),('departed:npc_pandol',True),('alive:nabi',False),('hidden_pandol:care_handed',True)]:
   self.values[key]=value;self.assertFalse(self.env['r13_hp_receiver_ready'](),key);del self.values[key]
 def test_map_option_is_locked_until_permission(self):
  b=json.loads((ROOT/'game/v111/field-bindings.json').read_text())
  home=[o for o in b['free_day7']['options'] if o['location']=='hidden_pandol']
  self.assertTrue(home)
  for o in home:self.assertTrue(any(g[1] in ('hidden_pandol:visit_allowed','hidden_pandol:family_seen') and g[2] is True for g in o['guard']))
  for key in ('free_day7','hp_meal6','hp_house11','sleep11_input','blanket_mend13'):
   indices=[o.get('index',i) for i,o in enumerate(b[key]['options'])];self.assertEqual(len(indices),len(set(indices)),key)
 def test_meeting_introduction_matches_prior_acquaintance(self):
  s=(ROOT/'game/room13_v111_newworld_text.rpy').read_text();env=dict(r13_v111_value=self.values.get,R13_NW_WHEN={})
  for known,trusted in itertools.product((False,True),repeat=2):
   self.put(met=known);env['R13_NW_WHEN'].update(town_won_before11=lambda:trusted,town_won_none_before11=lambda:not trusted)
   actual=[]
   for k in ('hp_known_trusted','hp_known_untrusted','hp_unknown_trusted','hp_unknown_untrusted'):
    line=next(l.strip() for l in s.splitlines() if l.strip().startswith('"'+k+'":'))
    if eval(line.split(':',1)[1].rstrip(','),env)():actual.append(k)
   self.assertEqual(actual,['hp_'+('known' if known else 'unknown')+'_'+('trusted' if trusted else 'untrusted')])
if __name__=='__main__':unittest.main()
