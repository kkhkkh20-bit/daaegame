"""Pure action/state integration, not native UI playback or geometry approval."""
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1];G={}
for file in ['recommended_model.py','recommended_opening_model.py','recommended_ep23_model.py','recommended_ep456_model.py']:
 exec(compile((R/'dev'/file).read_text(),file,'exec'),G)
def f(name,*args):return G['r13_rec_'+name](*args)
def actions(s,*keys):
 for key in keys:s=f('apply',s,key)
 return s

def late_hear(s):
 for step in f('e456_hearing',s):
  s,message,ok=f('e456_present',s,step['card'],step['right_detail'],step['right_claim'])
  if not ok:raise AssertionError(message)
 return s

class FullRoute(unittest.TestCase):
 def test_six_cases_and_family_safe_route(self):
  s=f('opening_state');s=actions(s,'entry_report','entry_original','entry_present','entry_inn');s=f('next_day',s);s=actions(s,'piko','heat','escort','repair','records','contact','delivery_wait','reply','meet')
  s=f('evening',s);s=actions(s,'room','shelter');s=f('next_day',s)
  s=actions(s,'pedestal','chorong','nabi_route','child');s=f('next_day',s)
  s=f('piko_hear_defense',s)
  for card in ['empty_heat','stone','child']:s,_,ok=f('present',s,card);self.assertTrue(ok)
  self.assertEqual(s['verdict'],'handoff_responsibility')
  s=f('begin_episode',s,2);s=actions(s,'e2_report');s=f('next_day',s)
  s=actions(s,'e2_rail','e2_ties','e2_somi','e2_bami','e2_badook');s=f('e2_privacy',s,True)
  for card in ['e2_card_rail','e2_card_badook','e2_card_ties','e2_card_dolmok']:s,_,ok=f('e2_present',s,card);self.assertTrue(ok)
  s,_,ok=f('e2_reconstruct',s,'restraint_request_reach_bite');self.assertTrue(ok)
  s=f('begin_episode',s,3);s=actions(s,'e3_bowls','e3_meet_children','e3_school_place','e3_handoff');s=f('next_day',s)
  s=actions(s,'e3_outcome_safe','e3_wall','e3_bori_safe','e3_layout','e3_teacher','e3_can','e3_nubi','e3_child_boundary','e3_child_support')
  s=f('e3_privacy',s,True)
  for card in ['e3_card_wall','e3_card_teacher','e3_card_can']:s,_,ok=f('e3_present',s,card);self.assertTrue(ok)
  for answer in ['W','L','L-M','M-W','overlap']:s,_,ok=f('e3_map_answer',s,answer);self.assertTrue(ok)
  s,_,ok=f('e3_finish',s,'e3_card_nubi');self.assertTrue(ok)
  self.assertEqual(s['episodes']['3']['verdict'],'partial_geometry_unverified')
  s=f('begin_episode',s,4);s=actions(s,'e4_escort','e4_rescue');s=f('next_day',s)
  s=actions(s,'e4_nabi7','e4_clinic_alive','e4_mechanism','e4_plan');s=f('next_day',s)
  s=actions(s,'e4_block_lever','e4_watch','e4_work');s=f('next_day',s);s=late_hear(s)
  self.assertEqual(s['neoul'],'detained')
  s=f('begin_episode',s,5);s=actions(s,'e5_school');s=f('next_day',s)
  s=actions(s,'e5_pots','e5_pharmacy','e5_lock','e5_serve_safe');s=f('next_day',s);s=late_hear(s)
  self.assertTrue(s['e5_poison_blocked'])
  s=f('begin_episode',s,6);s=actions(s,'e6_board','e6_manifest','e6_pandol','e6_nabi','e6_munchi','e6_hold','e6_altar','e6_research','e6_heat','e6_beds','e6_meals','e6_care','e6_route')
  s=f('next_day',s);s=late_hear(s)
  self.assertNotEqual(s['episodes']['6']['verdict'],'complete_today')
  s=actions(s,'e6_cancel','e6_handoff','e6_split_duties','e6_night')
  self.assertEqual(s['episodes']['6']['verdict'],'complete_today')
  self.assertEqual((s['day'],s['mother'],s['piko'],s['neoul']),(14,'M2','safe','detained'))
  self.assertTrue(all(s[k] for k in ['e3_school_handoff','e4_lever_blocked','e5_poison_blocked']))
  self.assertIsNone(f('next_available',s))
 def test_all_registered_labels_have_source(self):
  import re
  source='\n'.join(p.read_text() for p in (R/'game/systems').glob('room13_recommended*.rpy'))
  labels=set(re.findall(r'^label (\w+)',source,re.M))
  for ep in G['r13_rec_episodes'].values():self.assertIn(ep['hearing_label'],labels)
  for action in G['r13_rec_actions'].values():
   if action.get('label'):self.assertIn(action['label'],labels)

if __name__=='__main__':unittest.main()
