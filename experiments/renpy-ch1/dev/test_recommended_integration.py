"""Cross-plugin state route, not a native walkthrough."""
import unittest
from pathlib import Path
R=Path(__file__).resolve().parents[1]
G={}
for file in ['recommended_model.py','recommended_ep23_model.py']:
 exec(compile((R/'dev'/file).read_text(),file,'exec'),G)

def f(name,*args):return G['r13_rec_'+name](*args)
def actions(s,*keys):
 for key in keys:s=f('apply',s,key)
 return s

def ep1(safe=True,reunion=True):
 s=f('new_state')
 if reunion:s=actions(s,'repair','records','contact','delivery_wait','reply','meet')
 s=actions(s,'piko','heat')
 if reunion:s=f('evening',s);s=actions(s,'room','shelter')
 if safe:s=actions(s,'escort')
 s=f('next_day',s);s=actions(s,'pedestal','chorong','nabi_route','child');s=f('next_day',s)
 for card in ['empty_heat','stone','child']:s,_,_=f('present',s,card)
 return s

class IntegrationTests(unittest.TestCase):
 def test_actual_registry_transition_from_piko_to_bite(self):
  s=ep1();self.assertEqual(f('next_available',s),2)
  s=f('begin_episode',s,2)
  self.assertEqual((s['episode'],s['day'],s['mother'],s['piko'],s['nabi']),(2,4,'M2','safe','supervised_relief'))
  s=actions(s,'e2_report');s=f('next_day',s)
  s=actions(s,'e2_rail','e2_ties','e2_somi','e2_bami','e2_badook')
  s=f('e2_privacy',s,True)
  for card in ['e2_card_rail','e2_card_badook','e2_card_ties','e2_card_dolmok']:s,_,_=f('e2_present',s,card)
  s,_,_=f('e2_reconstruct',s,'restraint_request_reach_bite')
  self.assertEqual(f('next_available',s),3)
  s=f('begin_episode',s,3)
  s=actions(s,'e3_bowls','e3_meet_children','e3_school_place','e3_handoff');s=f('next_day',s)
  self.assertTrue(s['e3_school_handoff']);self.assertEqual(s['episodes']['3']['kkomi'],'alive')
  self.assertEqual((s['mother'],s['piko']),('M2','safe'))
 def test_mother_actions_remain_after_early_case(self):
  s=f('begin_episode',ep1(reunion=False),2)
  self.assertIn('repair',dict(f('available',s)))
  s=actions(s,'repair','records','contact','delivery_wait','reply','meet')
  self.assertEqual(s['mother'],'M2');self.assertEqual(s['episode'],2)
 def test_no_legacy_case_flags_are_reused(self):
  s=ep1()
  self.assertFalse({'lt_dawn','granny_guilty','ws_reunited','tok_detained'}&set(s['done']))
 def test_hypothetical_verified_contact_has_fourth_real_input(self):
  # Simulates a future approved asset. This test does not approve the current art.
  old=G['r13_rec_piko_contact_art_verified'];G['r13_rec_piko_contact_art_verified']=True
  try:
   s=ep1();s=f('piko_hear_defense',s);s=f('apply',s,'contact_match')
   self.assertIsNone(s['verdict']);self.assertEqual(s['hearing'],3)
   s,_,ok=f('present',s,'child');self.assertFalse(ok)
   s,_,ok=f('present',s,'container');self.assertTrue(ok)
   self.assertEqual(s['verdict'],'direct_removal')
  finally:G['r13_rec_piko_contact_art_verified']=old
 def test_story_art_not_marked_verified(self):
  self.assertFalse(G['r13_rec_piko_contact_art_verified']);self.assertFalse(G['r13_rec_e3_geometry_art_verified'])

if __name__=='__main__':unittest.main()

class SunsetTests(unittest.TestCase):
 def test_no_daytime_handoff_after_evening(self):
  s=f('e3_start',f('new_state'))
  s=actions(s,'e3_bowls','e3_meet_children','e3_school_place')
  self.assertIn('e3_handoff',dict(f('available',s)))
  s=f('evening',s)
  self.assertNotIn('e3_handoff',dict(f('available',s)))
  with self.assertRaises(ValueError):f('apply',s,'e3_handoff')

class MissedWarningTests(unittest.TestCase):
 def test_fresh_ep3_can_skip_warning_and_continue_after_fire(self):
  s=f('e3_start',f('new_state'))
  s=f('evening',s)
  self.assertIsNone(f('block_reason',s))
  s=f('next_day',s)
  self.assertIn('e3_outcome_loss',dict(f('available',s)))
  s=actions(s,'e3_outcome_loss','e3_wall')
  self.assertIn('e3_wall_seen',s['done'])
  self.assertFalse(s['e3_school_handoff'])

class PikoMeetingDefenseTests(unittest.TestCase):
 def test_cloth_match_is_not_final_inference_before_new_explanation(self):
  old=G['r13_rec_piko_contact_art_verified'];G['r13_rec_piko_contact_art_verified']=True
  try:
   s=ep1();s['done'].append('piko_cloth_available');s['facts'].append('container');s=f('apply',s,'contact_match')
   self.assertIsNone(s['verdict'])
   s,message,ok=f('present',s,'container')
   self.assertFalse(ok);self.assertEqual(s['hearing'],3)
   s=f('piko_hear_defense',s)
   self.assertIn('piko_nabi_defense',s['facts'])
   s,message,ok=f('present',s,'container')
   self.assertTrue(ok);self.assertEqual(s['verdict'],'direct_removal')
  finally:G['r13_rec_piko_contact_art_verified']=old
 def test_prior_consent_and_comparison_are_remembered_at_meeting(self):
  old=G['r13_rec_piko_contact_art_verified'];G['r13_rec_piko_contact_art_verified']=True
  try:
   s=actions(f('new_state'),'piko','heat');s=f('next_day',s)
   s=actions(s,'pedestal','chorong','nabi_route','child','piko_cloth_consent','contact_match')
   self.assertIn('piko_source_claim_early',s['done'])
   s=f('next_day',s);s=f('piko_summarize_prior',s)
   self.assertEqual(s['hearing'],4);self.assertEqual(s['verdict'],'direct_removal')
  finally:G['r13_rec_piko_contact_art_verified']=old
 def test_prior_summary_cannot_bypass_unreviewed_geometry(self):
  s=ep1();s['done']+=['piko_source_claim_early','cloth_contact_matched']
  with self.assertRaises(ValueError):f('piko_summarize_prior',s)
 def test_verified_art_cannot_skip_intact_before_loan_observation(self):
  old=G['r13_rec_piko_contact_art_verified'];G['r13_rec_piko_contact_art_verified']=True
  try:
   s=ep1();s=f('piko_hear_defense',s);s=f('apply',s,'contact_match')
   s['done'].remove('piko_cloth_intact_at_loan')
   s,_,ok=f('present',s,'container')
   self.assertFalse(ok);self.assertIsNone(s['verdict'])
  finally:G['r13_rec_piko_contact_art_verified']=old
 def test_tear_is_dated_by_delivery_observation_not_confession(self):
  old=G['r13_rec_piko_contact_art_verified'];G['r13_rec_piko_contact_art_verified']=True
  try:
   s=ep1();s=f('piko_hear_defense',s);s=f('apply',s,'contact_match')
   self.assertIn('piko_cloth_torn_at_delivery',s['done'])
   missing=__import__('copy').deepcopy(s);missing['done'].remove('piko_cloth_torn_at_delivery')
   missing,_,ok=f('present',missing,'container');self.assertFalse(ok)
   self.assertIsNone(missing['verdict'])
   s,_,ok=f('present',s,'container');self.assertTrue(ok)
   self.assertEqual(s['verdict'],'direct_removal')
   self.assertNotIn('piko_removal_admitted',s['done'])
  finally:G['r13_rec_piko_contact_art_verified']=old
