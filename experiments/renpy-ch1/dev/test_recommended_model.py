import unittest, copy, json
from recommended_model import *

class RouteTests(unittest.TestCase):
 def run_actions(self, seq, s=None):
  s=s or r13_rec_new_state()
  for k in seq:s=r13_rec_apply(s,k)
  return s
 def prepared(self,safe=True):
  s=self.run_actions(['piko','heat']+(['escort'] if safe else []))
  s=r13_rec_next_day(s)
  return self.run_actions(['pedestal','chorong','nabi_route','child'],s)
 def test_initial_questions_are_earned(self):
  self.assertEqual(set(dict(r13_rec_available(r13_rec_new_state()))),{'repair','piko','heat'})
 def test_no_contact_from_number(self):
  s=self.run_actions(['repair','records']); self.assertEqual(s['mother'],'M0')
 def test_delivery_needs_elapsed_action(self):
  s=self.run_actions(['repair','records','contact'])
  self.assertNotIn('reply',dict(r13_rec_available(s)))
  s=r13_rec_apply(s,'delivery_wait');self.assertIn('reply',dict(r13_rec_available(s)))
 def test_early_reunion_no_day11_lock(self):
  s=self.run_actions(['repair','records','contact','delivery_wait','reply','meet'])
  self.assertEqual((s['day'],s['mother']),(2,'M2'))
  self.assertNotIn('meet',dict(r13_rec_available(s)))
 def test_family_success_independent_of_case(self):
  s=self.run_actions(['piko','heat','repair','records','contact','delivery_wait','reply','meet'])
  s=r13_rec_evening(s);s=self.run_actions(['room','shelter'],s)
  self.assertIn('family_shelter',s['done']);self.assertIsNone(s['verdict'])
 def test_promise_not_prevention(self):
  s=r13_rec_next_day(self.run_actions(['piko','heat']))
  self.assertEqual(s['piko'],'dead')
 def test_actual_escort_prevents(self):self.assertEqual(self.prepared()['piko'],'safe')
 def test_survival_does_not_remove_evidence(self):
  self.assertEqual(self.prepared(True)['facts'],self.prepared(False)['facts'])
 def test_wrong_card_not_progress(self):
  s=r13_rec_next_day(self.prepared());n,_,ok=r13_rec_present(s,'child')
  self.assertFalse(ok);self.assertEqual(s,n)
 def test_unearned_card_rejected(self):
  with self.assertRaises(ValueError):r13_rec_present(r13_rec_new_state(),'child')
 def test_partial_responsibility_not_first_removal(self):
  s=r13_rec_next_day(self.prepared())
  for c in ['empty_heat','stone','child']:s,_,_=r13_rec_present(s,c)
  self.assertEqual(s['verdict'],'handoff_responsibility')
  self.assertEqual(s['nabi'],'supervised_relief');self.assertFalse(r13_rec_piko_contact_art_verified)
 def test_repeated_prevention_no_death(self):
  s=r13_rec_next_day(self.prepared());s=r13_rec_next_day(s)
  self.assertEqual(s['piko'],'safe')
 def test_state_not_mutated_in_place(self):
  s=r13_rec_new_state();before=copy.deepcopy(s);r13_rec_apply(s,'piko');self.assertEqual(s,before)
 def test_json_save_resume(self):
  s=self.prepared();self.assertEqual(json.loads(json.dumps(s)),s)
 def test_old_state_not_migrated(self):
  s=r13_rec_new_state();s['revision']='legacy';self.assertEqual(r13_rec_available(s),[])
 def test_mother_never_reverts(self):
  s=self.run_actions(['repair','records','contact','delivery_wait','reply','meet','piko','heat','escort'])
  self.assertEqual(r13_rec_next_day(s)['mother'],'M2')
 def test_no_early_granny(self):
  self.assertNotIn('할머니',str(r13_rec_actions));self.assertNotIn('granny',str(r13_rec_actions))
 def test_required_field_day_is_known(self):
  with self.assertRaises(ValueError):r13_rec_next_day(r13_rec_new_state())

class GuardTests(unittest.TestCase):
 def test_contact_cannot_be_awarded_without_art_review(self):
  s=RouteTests().prepared()
  with self.assertRaises(ValueError):r13_rec_apply(s,'contact_match')
 def test_completed_preventions_are_monotonic(self):
  for key,val in [('mother','M2'),('piko','safe'),('neoul','detained'),('e3_school_handoff',True),('e4_lever_blocked',True),('e5_poison_blocked',True)]:
   before=r13_rec_new_state();before[key]=val;after=copy.deepcopy(before);after[key]=False
   with self.assertRaises(ValueError):r13_rec_validate_transition(before,after)
 def test_portrait_not_death_reward(self):
  a=RouteTests().prepared(True);b=RouteTests().prepared(False)
  self.assertIn('piko_portrait',a['facts']);self.assertIn('piko_portrait',b['facts'])
 def test_nabi_is_known_before_child_questions(self):
  s=r13_rec_next_day(RouteTests().run_actions(['piko','heat']))
  s=r13_rec_apply(s,'pedestal');self.assertNotIn('child',dict(r13_rec_available(s)))
  s=r13_rec_apply(s,'nabi_route');self.assertIn('child',dict(r13_rec_available(s)))

class CurrentContactTests(unittest.TestCase):
 def test_old_reply_requires_actual_refresh(self):
  s=RouteTests().run_actions(['repair','records','contact','delivery_wait','reply','piko','heat'])
  s=r13_rec_next_day(s)
  self.assertNotIn('meet',dict(r13_rec_available(s)))
  s=r13_rec_apply(s,'refresh_reply')
  self.assertIn('meet',dict(r13_rec_available(s)))
  self.assertEqual(r13_rec_apply(s,'meet')['mother'],'M2')
 def test_piko_knows_reunion_when_it_already_happened(self):
  s=r13_rec_new_state();s['mother']='M2'
  self.assertNotIn('찾고 있습니다',r13_rec_action_lines(s,'piko')[0][1])

if __name__=='__main__':unittest.main()

class PikoObjectAccessTests(unittest.TestCase):
 def test_child_does_not_silently_give_owners_current_cloth(self):
  s=RouteTests().prepared()
  self.assertNotIn('container',s['facts'])
  self.assertNotIn('contact_match',dict(r13_rec_available(s)))
 def test_meeting_owner_brings_actual_object(self):
  s=RouteTests().prepared();s=r13_rec_next_day(s)
  s=r13_rec_piko_hear_defense(s)
  self.assertIn('container',s['facts'])
  self.assertIn('contact_match',dict(r13_rec_available(s)))
 def test_prior_consent_is_a_real_available_route(self):
  s=RouteTests().prepared();s=r13_rec_apply(s,'piko_cloth_consent')
  self.assertIn('container',s['facts'])
  self.assertEqual(s['location'],'square')
 def test_same_cloth_has_observed_intact_start_and_continuous_loan(self):
  s=RouteTests().prepared()
  self.assertIn('piko_cloth_intact_at_loan',s['done'])
  text=' '.join(line[1] for line in r13_rec_actions['child']['lines'])
  self.assertIn('직접 펴 넣었어요',text)
  self.assertIn('아직 돌려받지는 않았어요',text)
  self.assertNotIn('자기 천',text)
