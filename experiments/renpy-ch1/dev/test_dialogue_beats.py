import ast,copy,json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def functions():
 source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:\n',1)[1]
 tree=ast.parse(textwrap.dedent(source));tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
 env={'R13_FULLBODY_PLAIN':{'neutral','joy','angry','anxious','surprise','thinking','flustered'}};exec(compile(tree,'beats','exec'),env);return env
class DialogueBeats(unittest.TestCase):
 def setUp(self):
  self.env=functions();self.cues={'scene':{'0':{'reviewed':True,'person':'guard','text':'그 기록이 바뀌었다고요?','emotion':'surprise','reaction':True}}};self.packet=('guard','그 기록이 바뀌었다고요?')
  self.people={'guard':{'status':'approved_runtime','art_style':'storybook_source','source_kind':'source_master','stance':'standing','gaze':'player','profiles':{str(h):{'frames':{'surprise_talk':{},'surprise_react':{}}} for h in (560,760,840)}}}
 def plan(self):return self.env['r13_dialogue_plan']('scene',0,self.packet,'surprise',self.cues,self.people)
 def test_onset_expires_without_advancing_dialogue(self):
  p=self.plan();phase=self.env['r13_dialogue_phase'];self.assertEqual(phase(p,0),'surprise_react');self.assertEqual(phase(p,.35),'surprise_talk');self.assertEqual(phase(p,100),'surprise_talk')
 def test_skip_and_reduced_motion_bypass_reaction(self):
  for skip,motion in [(True,True),(False,False)]:self.assertEqual(self.env['r13_dialogue_phase'](self.plan(),0,skip,motion),'surprise_talk')
 def test_click_auto_load_settle_same_state(self):
  from types import SimpleNamespace
  for reason in ('click','auto','load','page'):
   self.env['store']=SimpleNamespace(r13_dialogue_beat=self.plan());self.env['r13_dialogue_beat_settle']();self.assertEqual(self.env['r13_dialogue_phase'](self.env['store'].r13_dialogue_beat,0),'surprise_talk',reason)
 def test_stale_text_or_speaker_does_not_apply(self):
  for packet in [('guard','다른 문장'),('daram',self.packet[1])]:
   self.packet=packet;self.assertIsNone(self.plan())
 def test_no_asset_no_activation(self):
  self.people={};self.assertIsNone(self.plan())
 def test_held_or_sideways_or_seated_art_not_accepted(self):
  for field,value in [('status','HOLD'),('stance','crouched'),('gaze','side')]:
   entry=copy.deepcopy(self.people['guard']);self.people['guard'][field]=value;self.assertIsNone(self.plan());self.people['guard']=entry
 def test_missing_reaction_keeps_talk_not_old_art(self):
  del self.people['guard']['profiles']['840']['frames']['surprise_react'];p=self.plan();self.assertTrue(p['settled']);self.assertIsNone(p['react'])
 def test_missing_talk_blocks_person(self):
  del self.people['guard']['profiles']['560']['frames']['surprise_talk'];self.assertIsNone(self.plan())
 def test_investigation_pose_not_replaced(self):
  self.assertIsNone(self.env['r13_dialogue_plan']('scene',0,self.packet,'living_stamp',self.cues,self.people))
 def test_cues_remain_attached_to_actual_context(self):
  import line_cues
  rows=line_cues.scene_rows();data=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())
  for scene,cues in data['lines'].items():
   for i,c in cues.items():self.assertEqual(tuple(rows[scene][int(i)][:2]),(c['person'],c['text']));self.assertTrue(c['reason'])
 def test_scope_classification_separates_non_dialogue(self):
  from audit_dialogue_beats import classify
  people={'guard':{},'dad':{},'daram':{}}
  cases=[((None,'설명'),'narration'),(('dad','질문'),'default_pov_speech'),(('dad','독백',{'thought':True}),'thought'),(('guard','대사'),'dialogue_expression_candidate'),(('guard','작업',{'pose':'living_stamp'}),'authored_action_separate_review')]
  for packet,expected in cases:self.assertEqual(classify('s',0,packet,people,{}),expected)
 def test_every_cue_has_pending_asset_status_and_allowed_reaction(self):
  cues=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
  for entries in cues.values():
   for cue in entries.values():
    self.assertIn(cue['application_status'],('approved_source_master','awaiting_approved_runtime_assets'))
    if cue['reaction']:self.assertEqual(cue['emotion'],'surprise')
 def test_registry_contains_no_held_art(self):
  data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text());self.assertEqual(len(data['people']),59)
class ContextReviewEvidence(unittest.TestCase):
 def test_dynamic_source_provenance_is_exact(self):
  from audit_dynamic_dialogue import provenance_errors
  self.assertEqual(provenance_errors(),[])
 def test_literal_inventory_has_no_unreviewed_npc_occurrence(self):
  from audit_dynamic_dialogue import literal_inventory
  out=ROOT/'docs/reviews/dialogue-beats'
  inventory=json.loads(json.dumps(literal_inventory()))
  self.assertEqual(inventory,json.loads((out/'dynamic-literal-inventory.json').read_text()))
  review=json.loads((out/'dynamic-context-review.json').read_text())
  for i,row in enumerate(r for r in inventory if not r['already_static_text']):
   if row['person'] in (None,'dad'):continue
   entry=review['rows'].get(str(i)) or review['excluded_rows'].get(str(i))
   self.assertIsNotNone(entry,(i,row))
   for key in ('source','line','person','text','packet'):self.assertEqual(entry[key],row[key])
 def test_opening_review_covers_all_authored_reply_branches(self):
  out=ROOT/'docs/reviews/dialogue-beats'
  rows=list(json.loads((out/'opening-context-review.json').read_text())['rows'].values())+json.loads((out/'supplemental-context-review.json').read_text())['rows']
  paths={tuple(r['path']) for r in rows if r['source']=='game/room13-dialogue-openings.json' and 'path' in r}
  source=json.loads((ROOT/'game/room13-dialogue-openings.json').read_text())
  for person,phases in source['calendar'].items():
   for phase in phases:self.assertIn(('calendar',person,phase,'reply'),paths)
  for section in ('calendar_daily','calendar_outcome'):
   for person,variants in source[section].items():
    for variant in variants:self.assertIn((section,person,variant),paths)
  for section in ('first_meetings','with_daram','calendar_companion'):
   groups=source[section]
   for key,group in groups.items():
    variants=group.items() if section=='first_meetings' else [(None,group)]
    for variant,packets in variants:
     if not isinstance(packets,list):continue
     for index,packet in enumerate(packets):
      if not isinstance(packet,list) or len(packet)<2 or packet[0] in (None,'dad'):continue
      path=(section,key,variant,index) if variant is not None else (section,key,index)
      self.assertIn(path,paths)
 def test_composed_expressions_stay_at_their_source_and_do_not_activate(self):
  rows=json.loads((ROOT/'docs/reviews/dialogue-beats/composed-context-review.json').read_text())['rows']
  for row in rows:
   source=(ROOT/row['source']).read_text().splitlines()
   self.assertIn(row['expression'],'\n'.join(source[row['line']-1:row['line']+5]))
   self.assertEqual(row['runtime_binding'],'local_callsite_snapshot_binding_assets_held')
 def test_new_delivery_is_intermediate_and_only_allowlisted_slots_verified(self):
  data=json.loads((ROOT/'docs/reviews/dialogue-beats/intermediate-resource-receipt.json').read_text())
  self.assertFalse(data['game_applied']);self.assertTrue(data['status'].startswith('HOLD'))
  expected={(person,slot) for person in ('nabi','karo','buri','granny','momo','musoe') for slot in ('neutral','joy','angry','anxious','surprise_talk','surprise_react')}
  self.assertEqual({(r['character'],r['slot']) for r in data['slots_verified']},expected)
if __name__=='__main__':unittest.main()
