import ast,copy,json,pickle,re,unittest
from pathlib import Path
from check_dialogue_bindings import ROOT,OUT,binder,load_functions
from test_dialogue_beats import functions

class DynamicBindings(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.bind=staticmethod(binder());cls.registry=json.loads((ROOT/'game/assets/room13-dialogue-bindings.json').read_text())
 def test_original_119_and_two_explicit_providers_have_exact_routes_and_arguments(self):
  import line_cues
  queue=json.loads((OUT/'runtime-binding-queue.json').read_text())
  checked=set();held=set();retired=set()
  for i,row in enumerate(queue):
   if row.get('active') is False:
    retired.add(i)
    self.assertEqual(i,238);self.assertEqual(row['identity'],'ep1:dawn:thought')
    self.assertEqual(row['binding_status'],'retired_removed_source_call')
    self.assertNotIn('dynamic:%03d'%i,self.registry['routes'])
    self.assertNotIn('"ep1:dawn:thought"',(ROOT/row['source']).read_text())
    continue
   if row.get('emit_binding') is False:
    held.add(i)
    self.assertEqual(row['assets'],'HOLD');self.assertNotIn('dynamic:%03d'%i,self.registry['routes']);continue
   if row['binding_status']=='static_exact_binding_available':continue
   checked.add('dynamic:%03d'%i)
   self.assertIn('call r13_lines(', (ROOT/row['source']).read_text().splitlines()[row['line']-1])
   source=(ROOT/row['source']).read_text();offset=sum(len(s) for s in source.splitlines(True)[:row['line']-1]);start=source.index('call r13_lines(',offset)+len('call r13_lines');end=line_cues._match_bracket(source,start)
   actual=ast.parse('f'+source[start:end+1],mode='eval').body;original=ast.parse('f('+row['call_expression']+')',mode='eval').body
   self.assertEqual([ast.dump(a) for a in actual.args],[ast.dump(a) for a in original.args]);self.assertEqual(actual.keywords[-1].value.value,'dynamic:%03d'%i)
  self.assertEqual(checked,set(self.registry['routes']))
  self.assertEqual(retired,{238});self.assertEqual(held,{803,804,806,807,808,809,810,811,812,813,814})
  original_routes=['dynamic:013', 'dynamic:016', 'dynamic:019', 'dynamic:022', 'dynamic:023', 'dynamic:024', 'dynamic:028', 'dynamic:029', 'dynamic:035', 'dynamic:077', 'dynamic:081', 'dynamic:086', 'dynamic:096', 'dynamic:097', 'dynamic:102', 'dynamic:103', 'dynamic:105', 'dynamic:109', 'dynamic:168', 'dynamic:169', 'dynamic:170', 'dynamic:171', 'dynamic:172', 'dynamic:173', 'dynamic:192', 'dynamic:194', 'dynamic:199', 'dynamic:202', 'dynamic:203', 'dynamic:209', 'dynamic:211', 'dynamic:212', 'dynamic:213', 'dynamic:214', 'dynamic:215', 'dynamic:216', 'dynamic:217', 'dynamic:218', 'dynamic:219', 'dynamic:220', 'dynamic:221', 'dynamic:222', 'dynamic:223', 'dynamic:224', 'dynamic:225', 'dynamic:226', 'dynamic:227', 'dynamic:262', 'dynamic:275', 'dynamic:290', 'dynamic:291', 'dynamic:303', 'dynamic:320', 'dynamic:324', 'dynamic:335', 'dynamic:342', 'dynamic:344', 'dynamic:351', 'dynamic:354', 'dynamic:369', 'dynamic:385', 'dynamic:388', 'dynamic:389', 'dynamic:392', 'dynamic:393', 'dynamic:402', 'dynamic:404', 'dynamic:405', 'dynamic:411', 'dynamic:412', 'dynamic:415', 'dynamic:416', 'dynamic:418', 'dynamic:426', 'dynamic:438', 'dynamic:439', 'dynamic:452', 'dynamic:454', 'dynamic:455', 'dynamic:463', 'dynamic:466', 'dynamic:467', 'dynamic:468', 'dynamic:469', 'dynamic:470', 'dynamic:471', 'dynamic:472', 'dynamic:475', 'dynamic:482', 'dynamic:530', 'dynamic:540', 'dynamic:544', 'dynamic:551', 'dynamic:565', 'dynamic:575', 'dynamic:576', 'dynamic:578', 'dynamic:579', 'dynamic:592', 'dynamic:596', 'dynamic:600', 'dynamic:601', 'dynamic:604', 'dynamic:605', 'dynamic:606', 'dynamic:607', 'dynamic:608', 'dynamic:609', 'dynamic:610', 'dynamic:611', 'dynamic:612', 'dynamic:658', 'dynamic:664', 'dynamic:665', 'dynamic:718', 'dynamic:739', 'dynamic:743', 'dynamic:768', 'dynamic:781']
  self.assertEqual(len(original_routes),119)
  self.assertEqual(set(self.registry['routes']),set(original_routes)|{'dynamic:805','dynamic:857'})
  for index,provider in ((805,'r13_piko_notice_lines'),(857,'r13_sling_confront_lines')):
   self.assertEqual(queue[index]['provider_scope']['function'],provider)
   self.assertEqual(queue[index]['provider_group'],'explicit_function')
 def test_same_text_in_different_scene_has_different_decision(self):
  packet=('daram','아빠!');b=self.bind([packet],'ev:visit:open','dynamic:544')
  self.assertEqual(b['rows']['0']['emotion'],'joy')
  static=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
  self.assertEqual(static['finale:child_on_convoy']['0']['emotion'],'anxious')
  self.assertFalse(self.bind([packet],'wrong-scene','dynamic:016')['rows'])
 def test_teacher_reassurance_uses_surface_intent_in_both_branches(self):
  p=('resident_teacher','고맙습니다. 걱정 마세요.')
  b=self.bind([p],'debate:conclusion_wrong:Q5A:weak','dynamic:223')
  self.assertEqual(b['rows']['0']['emotion'],'neutral')
 def test_saved_evaluated_rows_do_not_follow_later_state(self):
  first=self.bind([('daram','아빠!')],'ev:visit:open','dynamic:544');saved=pickle.dumps(first)
  second=self.bind([('neoul','시간 됐소.')],'ev:visit:end','dynamic:551')
  restored=pickle.loads(saved)
  self.assertEqual(restored['rows']['0']['person'],'daram');self.assertEqual(second['rows']['0']['person'],'neoul');self.assertEqual(first,restored)
 def test_dynamic_miss_never_falls_through_to_same_id_static_cue(self):
  env=functions();p=('guard','본문');static={'scene':{'0':dict(person='guard',text='본문',reviewed=True,emotion='joy')}}
  self.assertIsNone(env['r13_dialogue_plan']('scene',0,p,'neutral',static,{},dict(identity='scene',rows={})))
 def test_narration_thought_and_unknown_callsite_fail_closed(self):
  for rows in [[(None,'설명')],[('daram','아빠!',{'thought':True})],[('dad','아빠!')]]:
   self.assertEqual(self.bind(rows,'ev:visit:open','dynamic:544')['rows'],{})
  self.assertEqual(self.bind([('daram','아빠!')],'ev:visit:open','absent')['rows'],{})
 def test_original_packets_and_action_metadata_are_unchanged(self):
  rows=[('resident_teacher','깜이, 몽이, 방울, 도담, 새미. 하나도 안 틀렸지요.',{'pose':'write_attendance'})];before=copy.deepcopy(rows)
  self.bind(rows,'ws:teacher:count','dynamic:418');self.assertEqual(before,rows)
 def test_topic_record_never_replays_startle(self):
  data=json.loads((ROOT/'game/room13-dialogue-expand.json').read_text())
  for key,spec in data.items():
   b=self.bind(spec['new'],'topic:record_full:'+key.split('#')[0],'dynamic:664')
   self.assertFalse(b['unresolved'],key);self.assertTrue(all(not c['reaction'] for c in b['rows'].values()))
 def test_saved_binding_rejects_changed_speaker_text_and_index(self):
  env=functions();binding=dict(identity='scene',rows={'0':dict(person='guard',text='본문',reviewed=True,emotion='joy')})
  people={'guard':dict(status='approved_runtime',art_style='storybook_source',source_kind='source_master',stance='standing',gaze='player',profiles={str(h):dict(frames={'joy':{}}) for h in (560,760,840)})}
  plan=env['r13_dialogue_plan'];self.assertIsNotNone(plan('scene',0,('guard','본문'),'neutral',{},people,binding))
  for identity,index,packet in [('other',0,('guard','본문')),('scene',1,('guard','본문')),('scene',0,('guard','수정')),('scene',0,('daram','본문'))]:self.assertIsNone(plan(identity,index,packet,'neutral',{},people,binding))
 def test_rollback_and_load_settle_at_runtime_entry_and_render(self):
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text()
  self.assertIn('renpy.is_skipping() or renpy.in_rollback()',source)
  self.assertEqual(source.count('renpy.in_rollback()'),2)
  # Execute real begin/load functions with controlled engine state.
  from types import SimpleNamespace
  env=functions();env.update(store=SimpleNamespace(r13_dialogue_beat=None,r13_dialogue_binding=None),persistent=SimpleNamespace(room13_motion=True),R13_DIALOGUE_BEATS={'lines':{}},R13_DIALOGUE_TALK_ART={'people':{'guard':{'profiles':{}}}})
  env['r13_dialogue_plan']=lambda *a:dict(person='guard',talk='surprise_talk',react='surprise_react',settled=False,duration=.35)
  for rollback,skipping in [(True,False),(False,True),(False,False)]:
   env['renpy']=SimpleNamespace(in_rollback=lambda:rollback,is_skipping=lambda:skipping,loadable=lambda p:True)
   env['r13_dialogue_beat_begin']('scene',0,('guard','본문'),'surprise')
   self.assertEqual(env['store'].r13_dialogue_beat['settled'],rollback or skipping)
   env['r13_dialogue_beat_after_load']();self.assertTrue(env['store'].r13_dialogue_beat['settled'])
 def test_nested_meeting_resume_preserves_binding_snapshot(self):
  source=(ROOT/'game/systems/room13_meeting_flow.rpy').read_text();self.assertIn('R13_MEETING_RESUME_FIELDS=("r13_dialogue_binding","r13_dialogue_beat",',source)
 def test_generated_state_evidence_and_hold(self):
  for name in ['binding-state-results.json','provider-state-results.json']:
   result=json.loads((OUT/name).read_text());self.assertEqual(result['unresolved'],[])
  self.assertEqual(len(json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']),59)
if __name__=='__main__':unittest.main()

