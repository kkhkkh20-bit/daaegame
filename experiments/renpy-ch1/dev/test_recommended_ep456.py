import unittest, copy, json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
N={}
for name in ('recommended_model.py','recommended_ep456_model.py'):
    exec(compile((ROOT/'dev'/name).read_text(),name,'exec'),N)
globals().update({k:v for k,v in N.items() if k.startswith('r13_rec_')})


def actions(s,*keys):
    for key in keys: s=r13_rec_apply(s,key)
    return s

def seed(ep,mother='M2',detained=True):
    s=r13_rec_new_state()
    if mother=='M2':
        s=actions(s,'piko','heat','repair','records','contact','delivery_wait','reply','meet')
        s=r13_rec_evening(s);s=actions(s,'room','shelter')
    elif mother=='M1':
        s=actions(s,'repair','records','contact','delivery_wait','reply')
    s['neoul']='detained' if detained else 'active';s['piko']='safe';s['nabi']='supervised_relief'
    return r13_rec_e456_state(s,ep)

def e4_prepared(rescue=True, prevention='block', observed=True, discovery='e4_escort',mother='M2'):
    s=actions(seed(4,mother,False),discovery)
    if rescue:s=actions(s,'e4_rescue')
    s=r13_rec_next_day(s)
    s=actions(s,'e4_nabi7','e4_clinic_alive' if rescue else 'e4_clinic_dead','e4_mechanism','e4_plan')
    s=r13_rec_next_day(s)
    if prevention=='block':s=actions(s,'e4_block_lever')
    elif prevention=='wedge':s=actions(s,'e4_wedge')
    if observed:s=actions(s,'e4_watch')
    s=actions(s,'e4_work')
    if observed and prevention!='block':s=actions(s,'e4_nabi9')
    return r13_rec_next_day(s)

def e5_prepared(prevented=True,mother='M2'):
    s=seed(5,mother)
    if prevented:s=actions(s,'e5_school')
    s=r13_rec_next_day(s);s=actions(s,'e5_pots','e5_pharmacy')
    if prevented:s=actions(s,'e5_lock','e5_serve_safe')
    else:s=actions(s,'e5_serve_accident','e5_interview','e5_saemi','e5_bottle')
    s=r13_rec_next_day(s)
    if not prevented:s=actions(s,'e5_care_handoff')
    return s

def e6_prepared(hold=True,full=True,mother='M2'):
    s=actions(seed(6,mother),'e6_board','e6_manifest','e6_pandol','e6_nabi','e6_munchi')
    if hold:s=actions(s,'e6_hold','e6_altar')
    if full:
        if not hold:s=actions(s,'e6_hold','e6_altar')
        s=actions(s,'e6_research','e6_heat','e6_beds','e6_meals','e6_care','e6_route')
    return r13_rec_next_day(s)

def hear(s,stop=None):
    steps=r13_rec_e456_hearing(s)
    for i in range(s['episodes'][str(s['episode'])]['hearing'],len(steps) if stop is None else stop):
        step=steps[i];s,msg,ok=r13_rec_e456_present(s,step['card'],step['right_detail'],step['right_claim'])
        if not ok:raise AssertionError(msg)
    return s

class LateRoutes(unittest.TestCase):
 def test_all_e4_story_variants(self):
  for mother in ('M0','M1','M2'):
   for rescue in (True,False):
    for prevention in ('block','wedge','none'):
     for observed in (True,False):
      for discovery in ('e4_escort','e4_alone_tool','e4_wait'):
       with self.subTest(mother=mother,rescue=rescue,prevention=prevention,observed=observed,discovery=discovery):
        s=e4_prepared(rescue,prevention,observed,discovery,mother);before=copy.deepcopy(s);s=hear(s)
        self.assertEqual(s['neoul'],'detained');self.assertEqual(s['daram'],'with_parent');self.assertEqual(s['mother'],mother)
        self.assertEqual(s['episodes']['4']['victim'],'recovering' if rescue else 'dead_after_delayed_rescue')
        self.assertEqual(before['episodes']['4']['hearing'],0)
        self.assertEqual('e4_card_nabi9' in s['facts'],observed and prevention!='block')
        self.assertEqual('e4_card_tool' in s['facts'],discovery=='e4_alone_tool')
 def test_full_prevention_has_no_second_crime(self):
  s=e4_prepared(prevention='block');self.assertEqual(s['episodes']['4']['day9'],'prevented');self.assertNotIn('e4_card_nabi9',s['facts'])
  self.assertNotIn('e4_nabi9',dict(r13_rec_available(s)));self.assertEqual(len(r13_rec_e456_hearing(s)),6)
 def test_dates_are_not_interchangeable(self):
  s=e4_prepared(prevention='wedge');self.assertEqual(s['observed']['e4_card_nabi7'],8);self.assertEqual(s['observed']['e4_card_nabi9'],9)
  s=hear(s,4);n,_,ok=r13_rec_e456_present(s,'e4_card_nabi9',0,0);self.assertFalse(ok);self.assertEqual(n,s)
 def test_e4_unearned_card_rejected(self):
  s=e4_prepared()
  with self.assertRaises(ValueError):r13_rec_e456_present(s,'e4_card_tool',0,0)
 def test_e4_early_hearing_does_not_progress(self):
  s=seed(4);n,_,ok=r13_rec_e456_present(s,'e4_card_daram',0,0);self.assertFalse(ok);self.assertEqual(n,s)
 def test_e4_wrong_part_and_overclaim_do_not_progress(self):
  s=e4_prepared();step=r13_rec_e456_hearing(s)[0]
  wrong_detail=next(x[0] for x in step['details'] if x[0]!=step['right_detail'])
  wrong_claim=next(x[0] for x in step['claims'] if x[0]!=step['right_claim'])
  for detail,claim in ((wrong_detail,step['right_claim']),(step['right_detail'],wrong_claim),(wrong_detail,wrong_claim)):
   n,feedback,ok=r13_rec_e456_present(s,step['card'],detail,claim);self.assertFalse(ok);self.assertEqual(n,s);self.assertTrue(feedback)
 def test_e5_prevention_removes_all_dependent_acts(self):
  s=hear(e5_prepared());e=s['episodes']['5'];self.assertEqual(e['event'],'prevented');self.assertEqual(e['lids'],'original');self.assertEqual(e['contents'],'unchanged')
  self.assertNotIn('e5_card_bottle',s['facts']);self.assertNotIn('e5_card_bori',s['facts']);self.assertEqual(e['verdict'],'prevented')
 def test_e5_no_harmful_revival(self):
  s=e5_prepared();s=r13_rec_next_day(s);self.assertEqual(s['episodes']['5']['event'],'prevented')
  with self.assertRaises(ValueError):r13_rec_apply(s,'e5_serve_accident')
 def test_e5_actual_victim_not_original_target(self):
  s=hear(e5_prepared(False));e=s['episodes']['5'];self.assertEqual(e['contents'],'adult_body_contaminated');self.assertEqual(e['children'],'under_care');self.assertEqual(e['lids'],'swapped')
 def test_e5_care_handoff_required(self):
  s=e5_prepared(False);s['done'].remove('e5_care_handed');self.assertIn('돌봄',r13_rec_e456_ready(s))
 def test_e5_lock_requires_actual_pharmacy_and_school_check(self):
  s=seed(5);s=r13_rec_next_day(s);s=actions(s,'e5_pots','e5_pharmacy');self.assertNotIn('e5_lock',dict(r13_rec_available(s)))
 def test_e6_two_documents_not_complete(self):
  s=e6_prepared(False,False,'M0');s=hear(s,4);e=s['episodes']['6'];self.assertEqual(e['verdict'],'exclusion_proven_relief_pending');self.assertFalse(r13_rec_e456_done(s))
  self.assertIn('운행을 멈추자',r13_rec_e456_ready(s))
 def test_e6_no_research_no_forced_sacrifice(self):
  s=e6_prepared(True,False,'M0');s=hear(s,6);self.assertIn('원본',r13_rec_e456_ready(s));self.assertEqual(s['episodes']['6']['transport'],'paused')
  s=r13_rec_next_day(s);self.assertEqual(s['episodes']['6']['transport'],'paused')
 def test_e6_research_requires_actual_reunion(self):
  s=seed(6,'M1');self.assertNotIn('e6_research',dict(r13_rec_available(s)));self.assertNotIn('research',s['facts'])
 def test_e6_missing_resources_no_complete_answer(self):
  s=e6_prepared(True,False);s=actions(s,'e6_research');s=hear(s,7);self.assertIn('빠진 준비',r13_rec_e456_ready(s));self.assertFalse(r13_rec_e456_done(s))
 def test_e6_full_execution_is_not_just_hearing(self):
  s=hear(e6_prepared());e=s['episodes']['6'];self.assertEqual(e['verdict'],'case_proven_execution_pending');self.assertFalse(e['today_sacrifice_stopped']);self.assertFalse(r13_rec_e456_done(s))
  s=actions(s,'e6_cancel','e6_handoff','e6_split_duties','e6_night');e=s['episodes']['6']
  self.assertEqual(e['verdict'],'complete_today');self.assertTrue(e['today_sacrifice_stopped']);self.assertEqual(e['protection'],'housed_fed_cared');self.assertTrue(r13_rec_e456_done(s));self.assertEqual(s['neoul'],'detained')
 def test_e6_cannot_handoff_promised_resources(self):
  s=e6_prepared(True,False);self.assertNotIn('e6_handoff',dict(r13_rec_available(s)))
 def test_e6_stop_after_departure_can_continue(self):
  s=e6_prepared(False,False);self.assertEqual(s['episodes']['6']['transport'],'at_altar_waiting');s=actions(s,'e6_hold','e6_altar');self.assertEqual(s['episodes']['6']['transport'],'paused')
 def test_pure_state_and_save_serialization(self):
  for s in (e4_prepared(),e5_prepared(False),e6_prepared()):self.assertEqual(json.loads(json.dumps(s)),s)
  s=seed(4);b=copy.deepcopy(s);actions(s,'e4_escort');self.assertEqual(s,b)
 def test_stage_start_preserves_shared_success(self):
  s=hear(e4_prepared());s=r13_rec_e456_state(s,5);self.assertEqual((s['mother'],s['neoul'],s['piko']),('M2','detained','safe'))
 def test_no_legacy_story_flags_or_old_case_calls(self):
  source=(ROOT/'dev/recommended_ep456_labels.rpy').read_text()+(ROOT/'dev/recommended_ep456_model.py').read_text()
  for forbidden in ('r13_has(', 'r13_flag(', 'r13_grant(', 'r13_nt_', 'r13_edit(', 'r13_rescue('):self.assertNotIn(forbidden,source)
 def test_episode_entry_and_day_reset_period(self):
  s=seed(4);self.assertEqual(s['period'],0);s=actions(s,'e4_wait');s=r13_rec_evening(s);s=r13_rec_next_day(s);self.assertEqual(s['period'],0)
 def test_cabinet_card_does_not_invent_future_removal(self):
  s=seed(5);s=r13_rec_next_day(s);s=actions(s,'e5_pots','e5_pharmacy')
  self.assertIn('e5_card_cabinet',s['facts']);self.assertNotIn('e5_card_seori',s['facts']);self.assertNotIn('e5_card_bottle',s['facts'])
 def test_departure_plan_is_not_completed_escape(self):
  s=hear(e6_prepared());s=actions(s,'e6_cancel','e6_handoff','e6_split_duties');s=r13_rec_e6_choose_future(s,'departure_pending');s=actions(s,'e6_night')
  self.assertEqual(s['episodes']['6']['family'],'together_departure_unverified');self.assertEqual(s['episodes']['6']['verdict'],'complete_today')
 def test_admin_fixtures_are_disclosed_and_do_not_complete_cases(self):
  for ep in (4,5,6):
   s=r13_rec_e456_admin_seed(ep);self.assertIn('admin_fixture',s);self.assertEqual(s['mother'],'M2');self.assertIn('research',s['facts']);self.assertFalse(r13_rec_e456_done(s))
 def test_unearned_npc_future_actions_not_present(self):
  for ep in (5,6):
   s=seed(ep)
   for key,a in r13_rec_actions.items():
    if a['episode']==ep:
     self.assertNotEqual(a.get('target_person'),'neoul');self.assertFalse(any(who=='neoul' for who,line in a['lines']))
 def test_skipped_day11_school_can_still_prevent_on_day12(self):
  s=seed(5);s=r13_rec_next_day(s);s=actions(s,'e5_pots','e5_pharmacy')
  self.assertIn('e5_school',dict(r13_rec_available(s)));s=actions(s,'e5_school','e5_lock','e5_serve_safe')
  self.assertEqual(s['episodes']['5']['event'],'prevented');self.assertNotIn('e5_school',dict(r13_rec_available(s)))
 def test_granny_knowledge_is_incremental(self):
  s=actions(seed(6),'e6_board','e6_nabi')
  self.assertIn('e6_card_granny',s['facts']);self.assertNotIn('e6_granny_order_heard',s['done'])
  self.assertNotIn('지시자',r13_rec_cards['e6_card_granny'][0]);self.assertIn('이 요청만으로 알 수 없다',r13_rec_cards['e6_card_granny'][1])
  s=actions(s,'e6_munchi');self.assertIn('e6_granny_order_heard',s['done']);self.assertNotIn('e6_exclusion_proven',s['done'])
 def test_early_manifest_only_hold_does_not_claim_unseen_records(self):
  s=actions(seed(6),'e6_manifest');lines=str(r13_rec_e6_hold_lines(s))
  self.assertNotIn('이미 밖',lines);self.assertNotIn('판돌 씨는 아직',lines)
  s=actions(s,'e6_hold');self.assertEqual(s['episodes']['6']['transport'],'paused')
  self.assertNotIn('e6_card_board',s['facts']);self.assertNotIn('e6_card_pandol',s['facts'])
 def test_early_m2_research_prompt_does_not_repeat_reunion(self):
  s=e6_prepared(True,False);s=hear(s,6);text=r13_rec_e456_ready(s)
  self.assertIn('받은 원본',text);self.assertNotIn('재회',text);self.assertEqual(s['mother'],'M2')
 def test_final_first_night_sets_evening(self):
  s=hear(e6_prepared());s=actions(s,'e6_cancel','e6_handoff','e6_split_duties','e6_night');self.assertEqual(s['period'],2)
 def test_admin_seeds_prior_public_custody_procedure(self):
  for ep in (4,5,6):self.assertIn('public_custody_procedure_heard',r13_rec_e456_admin_seed(ep)['done'])
 def test_answers_use_semantic_ids_and_not_first_position_pattern(self):
  for prepared in (e4_prepared(),e5_prepared(),e5_prepared(False),e6_prepared()):
   steps=r13_rec_e456_hearing(prepared);positions=[]
   for step in steps:
    for field,right in (('details','right_detail'),('claims','right_claim')):
     self.assertIsInstance(step[right],str);ids=[x[0] for x in step[field]];self.assertEqual(len(ids),len(set(ids)));self.assertIn(step[right],ids)
     positions.append(ids.index(step[right]))
   self.assertTrue(any(x>0 for x in positions));self.assertGreater(len(set(positions)),1)
 def test_every_wrong_option_has_specific_feedback_and_preserves_progress(self):
  for prepared in (e4_prepared(),e5_prepared(),e5_prepared(False),e6_prepared()):
   s=prepared
   for step in r13_rec_e456_hearing(s):
    for key in ('details','claims'):
     correct_key='right_detail' if key=='details' else 'right_claim'
     for answer_id,caption,feedback in step[key]:
      if answer_id==step[correct_key]:continue
      self.assertTrue(feedback,caption)
      detail=answer_id if key=='details' else step['right_detail'];claim=answer_id if key=='claims' else step['right_claim']
      n,got,ok=r13_rec_e456_present(s,step['card'],detail,claim)
      self.assertFalse(ok);self.assertEqual(n,s);self.assertEqual(got,feedback)
    s,_,ok=r13_rec_e456_present(s,step['card'],step['right_detail'],step['right_claim']);self.assertTrue(ok)
 def test_option_reorder_does_not_change_semantic_answer(self):
  s=e4_prepared();step=r13_rec_e456_hearing(s)[0];right=step['right_claim'];reordered=list(reversed(step['claims']))
  self.assertEqual(next(x[1] for x in step['claims'] if x[0]==right),next(x[1] for x in reordered if x[0]==right))
  n,_,ok=r13_rec_e456_present(s,step['card'],step['right_detail'],right);self.assertTrue(ok);self.assertEqual(n['episodes']['4']['selected'][-1]['claim'],right)
 def test_play_options_do_not_contain_legal_or_developer_jargon(self):
  for s in (e4_prepared(),e5_prepared(),e5_prepared(False),e6_prepared()):
   text=str(r13_rec_e456_hearing(s))
   for word in ('기수로 판정','관찰 범위','실행자 확정','⑤ 이후'):self.assertNotIn(word,text)
 def test_skipped_school_pharmacy_does_not_invent_heard_motive(self):
  s=seed(5);s=r13_rec_next_day(s);s=actions(s,'e5_pots','e5_pharmacy')
  self.assertNotIn('e5_notice_checked',s['done']);self.assertNotIn('걱정하는 말은 들었습니다',str(r13_rec_actions['e5_pharmacy']['lines']))
 def test_source_and_generated_payload_match(self):
  model=(ROOT/'dev/recommended_ep456_model.py').read_text();generated=(ROOT/'game/systems/room13_recommended_ep456.rpy').read_text()
  self.assertIn(''.join('    '+l+'\n' for l in model.splitlines()),generated)
 def test_every_action_has_world_target(self):
  for key,a in r13_rec_actions.items():
   if a['episode'] in (4,5,6):self.assertTrue(a.get('target_person') or a.get('target_object'),key)

if __name__=='__main__':unittest.main(verbosity=2)
