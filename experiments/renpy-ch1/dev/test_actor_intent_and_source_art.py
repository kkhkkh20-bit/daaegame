import hashlib,json,tempfile,unittest
from pathlib import Path
from PIL import Image
from check_dialogue_bindings import ROOT,OUT,binder
from prepare_dialogue_source_profiles import resize_source,prepare
import test_dialogue_beats

class ActorIntent(unittest.TestCase):
 def test_teacher_both_reassurances_use_composed_surface_not_outcome(self):
  static=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
  cue=static['ws:teacher:alone']['0'];self.assertEqual(cue['emotion'],'neutral')
  dynamic=binder()([('resident_teacher',cue['text'])],'debate:conclusion_wrong:Q5A:weak','dynamic:223')
  self.assertEqual(dynamic['rows']['0']['emotion'],'neutral')
  for scene,index in [('ws:soup:spilled','3'),('ws:soup:tragedy','5')]:self.assertEqual(static[scene][index]['emotion'],'neutral')
 def test_story_source_unchanged_by_semantic_revision(self):
  audit=json.loads((OUT/'actor-intent-audit.json').read_text())
  for name,digest in audit['source_rpy_sha256'].items():
   if name=='game/systems/room13_dialogue_beats.rpy':continue # authorized renderer/style gate update only
   self.assertEqual(hashlib.sha256((ROOT/name).read_bytes()).hexdigest(),digest,name)
 def test_resource_requests_preserve_text_and_separate_body_from_affect(self):
  data=json.loads((OUT/'performance-resource-requests.json').read_text());static=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
  for request in data['requests']:
   self.assertFalse(request['runtime_assets_active']);self.assertFalse(request['dialogue_text_change'])
   self.assertEqual(request['status'],'REQUESTED_NOT_PRODUCED_NOT_APPROVED')
   for field in ('experienced_affect','visible_performance','physical_state'):self.assertTrue(request[field])
   for t in request['targets']:
    if t['kind']=='static':self.assertEqual(static[t['identity']][str(t['index'])]['text'],t['text'])
  injured=next(r for r in data['requests'] if r['id']=='chorong-injured-collapse')
  self.assertIn('injured_collapsed_event_body',injured['requested_resource_kinds']);self.assertIn('pain_expression',injured['requested_resource_kinds'])
 def test_report_uses_real_call_ids(self):
  source=(OUT/'quality-examples-20.md').read_text()
  self.assertIn('dynamic:223 / debate:conclusion_wrong:Q5A:weak / 0',source)
  self.assertIn('dynamic:016 / opening:carriage:daram:v4 / 1',source)
  self.assertNotIn('dynamic:607 / debate:Q5A:conclusion:weak',source)

class SourceMasterArt(unittest.TestCase):
 def test_resize_preserves_alpha_and_odd_dimensions_without_pixel_grid(self):
  im=Image.new('RGBA',(8,8),(0,0,0,0));im.paste((250,100,30,255),(2,2,6,6))
  result=resize_source(im,(17,23))
  self.assertEqual(result.size,(17,23));self.assertEqual(result.mode,'RGBA')
  self.assertTrue(sum(result.getchannel('A').histogram()[1:255])>0)
 def test_profile_builder_is_separate_and_always_hold(self):
  with tempfile.TemporaryDirectory() as tmp:
   source=Path(tmp)/'source.png';Image.new('RGBA',(8,8),'red').save(source)
   layout={'people':{'nabi':{'profiles':{'560':{'canvas':[91,113],'frames':{'neutral':{'source_master':str(source),'size':[17,23],'offset':[3,5]}}}}}}}
   result=prepare(layout,Path(tmp)/'dialogue-source-master');entry=result['people']['nabi']
   self.assertEqual(entry['status'],'HOLD');self.assertEqual(entry['source_kind'],'source_master')
   self.assertTrue(entry['profiles']['560']['frames']['neutral']['file'].startswith('assets/dialogue-source-master/'))
   with self.assertRaises(ValueError):prepare(layout,Path(tmp)/'investigation-art')
 def test_pixel_source_is_rejected(self):
  layout={'people':{'nabi':{'profiles':{'560':{'canvas':[10,10],'frames':{'neutral':{'source_master':'final_pixel/nabi.png','size':[9,9],'offset':[0,0]}}}}}}}
  with tempfile.TemporaryDirectory() as tmp:
   with self.assertRaises(ValueError):prepare(layout,Path(tmp)/'dialogue-source-master')
 def test_runtime_rejects_pixel_entry_even_if_marked_approved(self):
  fixture=test_dialogue_beats.DialogueBeats();fixture.setUp();fixture.people['guard']['art_style']='pixel'
  self.assertIsNone(fixture.plan())
  fixture.people['guard']['art_style']='storybook_source';fixture.people['guard']['source_kind']='final_pixel'
  self.assertIsNone(fixture.plan())
 def test_intermediate_registry_stays_empty_and_renderer_is_smooth(self):
  data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text());self.assertEqual(data['people'],{})
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text()
  self.assertIn('nearest=False,subpixel=True',source);self.assertNotIn('nearest=True',source)
