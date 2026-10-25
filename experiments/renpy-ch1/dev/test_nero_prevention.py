"""네로 운반 준비는 각 실제 행동과 받는 사람을 요구한다."""
import ast,itertools,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class NeroPreparation(unittest.TestCase):
 def setUp(self):
  s=(ROOT/'game/room13_v111_days1114.rpy').read_text().split('init 324 python:',1)[1].split('\n# Reviewed',1)[0]
  self.values={};self.actors={'karo':True,'resident_teacher':True,'nabi':False}
  self.env=dict(r13_v111_value=self.values.get,r13_v111_actor_ready=lambda p:self.actors.get(p,False))
  exec(compile(ast.parse(textwrap.dedent(s)),'<nero>','exec'),self.env)
 def test_every_piece_and_receiver_place_required_in_new_runs(self):
  keys=('rescue_cart_ready','rescue_cover_ready','rescue_driver_ready','rescue_lights_ready','rescue_school_ready11')
  self.values['rescue_preparation_schema11']=True
  for bits in itertools.product((None,True),repeat=5):
   self.values.update(zip(keys,bits));self.assertEqual(bool(self.env['r13_nero_transport_ready11']()),all(bits))
  self.actors['karo']=False;self.assertFalse(self.env['r13_nero_transport_ready11']())
 def test_old_ready_save_can_continue_without_new_seat_flag(self):
  self.values.update(dict.fromkeys(('rescue_cart_ready','rescue_cover_ready','rescue_driver_ready','rescue_lights_ready'),True))
  self.assertTrue(self.env['r13_nero_transport_ready11']())
  self.values['departed:karo']=True;self.assertFalse(self.env['r13_nero_transport_ready11']())
 def test_handoff_requires_present_unlisted_receiver(self):
  self.assertTrue(self.env['r13_nero_receiver_ready11']())
  for key in ('departed:resident_teacher','listed:resident_teacher'):
   self.values[key]=True;self.assertFalse(self.env['r13_nero_receiver_ready11']());self.values.pop(key)
  self.actors['resident_teacher']=False;self.assertFalse(self.env['r13_nero_receiver_ready11']())
 def test_bowl_indices_survive_and_always_a_way_to_leave(self):
  b=json.loads((ROOT/'game/v111/field-bindings.json').read_text())
  self.assertEqual([o.get('index',i) for i,o in enumerate(b['rescue_cart11']['options'])][:4],[0,1,2,3])
  self.assertTrue(any(o.get('index')==85 and not o['guard'] for o in b['rescue_cart11']['options']))
  self.assertEqual(len(b['night_rescue_prepare11']['options']),2)
 def test_night_cannot_synthesize_preparation_from_people_or_inventory(self):
  s=(ROOT/'game/room13_v111_days1114.rpy').read_text().split('label r13_v111_night_rescue_choices11:',1)[1].split('label ',1)[0]
  self.assertNotIn('r13_v111_set',s);self.assertIn('r13_v111_late_supply11',s);self.assertIn('r13_v111_late_cart11',s)
if __name__=='__main__':unittest.main()
