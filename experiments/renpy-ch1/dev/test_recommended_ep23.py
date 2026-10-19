"""Source/model regression tests, NOT native gameplay or production-art verification."""
import unittest, copy, json, ast, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
G={}
exec(compile((ROOT/'dev/recommended_model.py').read_text(),'recommended_model.py','exec'),G)
exec(compile((ROOT/'dev/recommended_ep23_model.py').read_text(),'recommended_ep23_model.py','exec'),G)

class Episode23Tests(unittest.TestCase):
 def f(self,name,*args): return G['r13_rec_'+name](*args)
 def actions(self,s,seq):
  for key in seq: s=self.f('apply',s,key)
  return s
 def e2(self):
  s=self.f('new_state');s.update(mother='M2',piko='safe',nabi='supervised_relief',neoul='detained')
  return self.f('e2_start',s)
 def e2prepared(self):
  s=self.actions(self.e2(),['e2_report']);s=self.f('next_day',s)
  return self.actions(s,['e2_rail','e2_ties','e2_somi','e2_bami','e2_badook'])
 def e2resolved(self,consent=True):
  s=self.f('e2_privacy',self.e2prepared(),consent)
  for c in ['e2_card_rail','e2_card_badook','e2_card_ties','e2_card_dolmok']:
   s,_,ok=self.f('e2_present',s,c);self.assertTrue(ok)
  s,_,ok=self.f('e2_reconstruct',s,'restraint_request_reach_bite' if consent else 'restraint_request_cry_unconfirmed')
  self.assertTrue(ok);return s
 def e3(self): return self.f('e3_start',self.e2resolved())
 def e3prepared(self,safe=True,support=True):
  s=self.actions(self.e3(),['e3_bowls'])
  if safe:s=self.actions(s,['e3_meet_children','e3_school_place','e3_handoff'])
  s=self.f('next_day',s)
  s=self.actions(s,['e3_outcome_safe' if safe else 'e3_outcome_loss','e3_wall','e3_bori_safe' if safe else 'e3_bori_loss','e3_layout','e3_teacher','e3_can','e3_nubi'])
  if support:s=self.actions(s,['e3_child_boundary','e3_child_support'])
  return s
 def e3mapped(self,safe=True,consent=True):
  s=self.f('e3_privacy',self.e3prepared(safe,consent),consent)
  for c in ['e3_card_wall','e3_card_teacher','e3_card_can']:s,_,ok=self.f('e3_present',s,c);self.assertTrue(ok)
  if consent:
   for a in ['W','L','L-M','M-W','overlap']:s,_,ok=self.f('e3_map_answer',s,a);self.assertTrue(ok)
  return s
 def test_e2_questions_unlock_from_actual_knowledge(self):
  self.assertEqual({k for k,_ in self.f('available',self.e2()) if k.startswith('e2_')},{'e2_report'})
  with self.assertRaises(ValueError):self.f('apply',self.e2(),'e2_bami')
 def test_e2_day_advance_requires_report_not_every_card(self):
  with self.assertRaises(ValueError):self.f('next_day',self.e2())
  s=self.f('next_day',self.actions(self.e2(),['e2_report']));self.assertEqual(s['day'],5)
 def test_bite_not_admitted_before_boundary(self):
  s=self.e2prepared();self.assertFalse(s['episodes']['2']['bite_admitted']);self.assertIsNone(s['episodes']['2']['privacy'])
 def test_badook_prior_observation_public_before_hearing(self):
  s=self.e2prepared();self.assertIn('e2_card_badook',s['facts']);self.assertIn('비명을',G['r13_rec_cards']['e2_card_badook'][1]);self.assertEqual(s['episodes']['2']['stage'],0)
 def test_e2_full_separates_bite_and_prior_coercion(self):
  s=self.e2resolved();self.assertEqual(s['episodes']['2']['verdict'],'bite_and_prior_coercion')
 def test_e2_refusal_does_not_invent_bite(self):
  s=self.e2resolved(False);self.assertEqual(s['episodes']['2']['verdict'],'prior_coercion_contact_unconfirmed');self.assertFalse(s['episodes']['2']['bite_admitted'])
 def test_e2_wrong_card_does_not_progress(self):
  s=self.f('e2_privacy',self.e2prepared(),True);n,_,ok=self.f('e2_present',s,'e2_card_somi');self.assertFalse(ok);self.assertEqual(n,s)
 def test_e2_wrong_order_not_resolved(self):
  s=self.f('e2_privacy',self.e2prepared(),True)
  for c in ['e2_card_rail','e2_card_badook','e2_card_ties','e2_card_dolmok']:s,_,_=self.f('e2_present',s,c)
  n,_,ok=self.f('e2_reconstruct',s,'bite_then_restraint');self.assertFalse(ok);self.assertIsNone(n['episodes']['2']['verdict'])
 def test_e2_care_not_testimony_payment(self):
  s=self.actions(self.e2prepared(),['e2_care']);self.assertIn('e2_care_complete',s['done']);self.assertIsNone(s['episodes']['2']['privacy'])
 def test_e2_partial_unlocks_next(self):
  self.assertEqual(self.f('next_available',self.e2resolved(False)),3)
 def test_e3_same_day_prevention_window_survives_e2(self):
  s=self.f('begin_episode',self.e2resolved(),3);self.assertEqual(s['day'],5);self.assertIn('e3_bowls',dict(self.f('available',s)))
 def test_e3_promise_is_not_actual_handoff(self):
  s=self.actions(self.e3(),['e3_bowls','e3_meet_children','e3_school_place']);self.assertFalse(s['e3_school_handoff'])
  s=self.f('next_day',s);self.assertEqual(s['episodes']['3']['kkomi'],'dead')
 def test_e3_actual_handoff_keeps_all_children_alive(self):
  s=self.e3prepared();self.assertTrue(s['e3_school_handoff']);self.assertEqual(s['episodes']['3']['children'],'school');self.assertEqual(s['episodes']['3']['kkomi'],'alive')
 def test_e3_prevention_optional(self):
  s=self.e3prepared(False);self.assertEqual(s['episodes']['3']['children'],'three_rescued');self.assertEqual(s['episodes']['3']['kkomi'],'dead')
 def test_safe_branch_has_no_inside_witness_or_rescue(self):
  s=self.f('next_day',self.actions(self.e3(),['e3_bowls','e3_meet_children','e3_school_place','e3_handoff']))
  avail=dict(self.f('available',s));self.assertIn('e3_outcome_safe',avail);self.assertNotIn('e3_outcome_loss',avail)
  s=self.actions(s,['e3_outcome_safe','e3_wall']);self.assertIn('e3_bori_safe',dict(self.f('available',s)));self.assertNotIn('e3_bori_loss',dict(self.f('available',s)))
 def test_survival_not_required_for_core_evidence(self):
  a={x for x in self.e3prepared(True)['facts'] if x.startswith('e3_')};b={x for x in self.e3prepared(False)['facts'] if x.startswith('e3_')};self.assertEqual(a-{'e3_card_handoff'},b)
 def test_fire_not_replayed_or_prevention_revoked(self):
  s=self.e3prepared();n=self.f('next_day',s);self.assertEqual(n,s)
 def test_no_retroactive_handoff(self):
  with self.assertRaises(ValueError):self.f('apply',self.e3prepared(False),'e3_handoff')
 def test_child_support_must_precede_private_testimony(self):
  with self.assertRaises(ValueError):self.f('e3_privacy',self.e3prepared(support=False),True)
 def test_child_refusal_keeps_support_and_no_card(self):
  s=self.f('e3_privacy',self.e3prepared(),False);self.assertIn('e3_child_support_ready',s['done']);self.assertNotIn('e3_card_child',s['facts'])
 def test_wrong_card_not_progress_e3(self):
  s=self.f('e3_privacy',self.e3prepared(),True);n,_,ok=self.f('e3_present',s,'e3_card_nubi');self.assertFalse(ok);self.assertEqual(s,n)
 def test_uneared_card_rejected(self):
  with self.assertRaises(ValueError):self.f('e3_present',self.e3(),'e3_card_teacher')
 def test_can_endpoint_must_be_W(self):
  s=self.f('e3_privacy',self.e3prepared(),True)
  for c in ['e3_card_wall','e3_card_teacher','e3_card_can']:s,_,_=self.f('e3_present',s,c)
  n,_,ok=self.f('e3_map_answer',s,'L');self.assertFalse(ok);self.assertEqual(n['episodes']['3']['map_step'],0)
 def test_map_needs_both_earned_witnesses(self):
  with self.assertRaises(ValueError):self.f('e3_map_answer',self.e3mapped(consent=False),'W')
 def test_required_map_inputs_are_not_auto_completed(self):
  s=self.f('e3_privacy',self.e3prepared(),True)
  for c in ['e3_card_wall','e3_card_teacher','e3_card_can']:s,_,_=self.f('e3_present',s,c)
  with self.assertRaises(ValueError):self.f('e3_finish',s,'e3_card_nubi')
 def test_default_art_gate_blocks_unique_identity(self):
  self.assertFalse(G['r13_rec_e3_geometry_art_verified']);s=self.e3mapped();self.assertFalse(self.f('e3_can_identify',s))
  n,_,ok=self.f('e3_finish',s,'e3_card_nubi');self.assertTrue(ok);self.assertEqual(n['episodes']['3']['verdict'],'partial_geometry_unverified')
 def test_no_testimony_has_honest_partial_resolution(self):
  n,_,ok=self.f('e3_finish',self.e3mapped(consent=False));self.assertTrue(ok);self.assertEqual(n['episodes']['3']['verdict'],'partial_no_child_testimony')
 def test_unique_identity_requires_verified_geometry_and_no_gap(self):
  old=G['r13_rec_e3_geometry_art_verified'];G['r13_rec_e3_geometry_art_verified']=True
  try:
   s=self.e3mapped();n,_,_=self.f('e3_finish',s,'e3_card_nubi');self.assertEqual(n['episodes']['3']['verdict'],'nubi_ignition_bori_afterward')
   s['episodes']['3']['sightline_gap']=True;n,_,_=self.f('e3_finish',s,'e3_card_nubi');self.assertEqual(n['episodes']['3']['verdict'],'partial_sightline_gap')
   s['episodes']['3']['sightline_gap']=False;s['episodes']['3']['other_crossing']=True;self.assertFalse(self.f('e3_can_identify',s))
  finally:G['r13_rec_e3_geometry_art_verified']=old
 def test_wrong_person_not_finalized(self):
  s=self.e3mapped();n,_,ok=self.f('e3_finish',s,'e3_card_bori');self.assertFalse(ok);self.assertEqual(s,n)
 def test_global_state_preserved_across_episodes(self):
  s=self.e3prepared();self.assertEqual((s['mother'],s['piko'],s['nabi'],s['neoul']),('M2','safe','supervised_relief','detained'))
 def test_transitions_pure(self):
  for name,s,args in [('e2_start',self.f('new_state'),()),('e2_privacy',self.e2prepared(),(True,)),('e3_start',self.e2resolved(),()),('e3_privacy',self.e3prepared(),(True,)),('e3_finish',self.e3mapped(),('e3_card_nubi',))]:
   before=copy.deepcopy(s);self.f(name,s,*args);self.assertEqual(s,before,name)
 def test_saved_mid_map_is_resumable(self):
  s=self.e3mapped();s=json.loads(json.dumps(s));n,_,ok=self.f('e3_finish',s,'e3_card_nubi');self.assertTrue(ok)
 def test_source_and_runtime_model_match(self):
  p=(ROOT/'game/systems/room13_recommended_ep23.rpy').read_text();model=(ROOT/'dev/recommended_ep23_model.py').read_text();self.assertIn(''.join('    '+x+'\n' for x in model.splitlines()),p)
 def test_no_unknown_target_actors(self):
  ids={'guard','resident_somi','resident_musoe','bami','resident_badook','dad','daram','nabi','resident_nubi','resident_teacher','resident_bori','kid_kkomi','kid_kkam','kid_mong','kid_bang','kid_nubi1','kid_nubi2',None}
  for k,a in G['r13_rec_actions'].items():
   if a.get('episode') not in (2,3):continue
   self.assertTrue(a.get('target_person') or a.get('target_object'),k)
   for who,line in a['lines']:self.assertIn(who,ids,(k,who))
 def test_ep_actions_have_date_and_place(self):
  places={'gate','square','post','inn','dining','hall','room13','guestroom','kitchen','workshop','passage','clinic','school','store','greenhouse','facility','altar','river','forest','market'}
  for k,a in G['r13_rec_actions'].items():
   if a.get('episode') in (2,3):self.assertIn(a['day'],(4,5,6));self.assertIn(a['place'],places)
 def test_old_story_logic_not_called(self):
  p=(ROOT/'dev/recommended_ep23_model.py').read_text()+(ROOT/'dev/recommended_ep23_ui.rpy').read_text()
  for needle in ['r13_grant(', 'r13_has(', 'r13_upgrade(', 'r13_wf_', 'r13_mark(']:self.assertNotIn(needle,p)
 def test_dev_caveats_not_spoken(self):
  for k,a in G['r13_rec_actions'].items():
   if a.get('episode') in (2,3):
    for who,line in a['lines']:
     for needle in ['검증판','아트 검수','flag','gate']:self.assertNotIn(needle,line,(k,line))
 def test_known_owner_before_nubi_question(self):
  self.assertTrue(any(who=='resident_nubi' for who,line in G['r13_rec_actions']['e3_can']['lines']))
  self.assertIn('e3_can_seen',G['r13_rec_actions']['e3_nubi']['need'])

if __name__=='__main__':unittest.main(verbosity=2)
