import hashlib,json,tempfile,unittest,subprocess
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
 def test_historical_semantic_revision_preserved_story_source(self):
  audit=json.loads((OUT/'actor-intent-audit.json').read_text())
  for name,digest in audit['source_rpy_sha256'].items():
   if name=='game/systems/room13_dialogue_beats.rpy':continue # authorized renderer/style gate update only
   self.assertEqual(hashlib.sha256(subprocess.check_output(['git','show','2ea4d41:experiments/renpy-ch1/'+name],cwd=ROOT)).hexdigest(),digest,name)
 def test_resource_requests_preserve_text_and_separate_body_from_affect(self):
  data=json.loads((OUT/'performance-resource-requests.json').read_text());static=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
  for request in data['requests']:
   self.assertFalse(request['dialogue_text_change'])
   if request['runtime_assets_active']:
    if request['status']=='APPROVED_CONTEXT_ART':
     context=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())
     self.assertTrue(set(request['approved_context_art'])<=set(context['entries']))
     self.assertEqual(request['source_commit'],context['source_commit'])
    else:
     self.assertEqual(request['status'],'APPROVED_SCENE_CUT')
    scenes=json.loads((ROOT/'game/assets/room13-special-scenes.json').read_text())
    if request['status']=='APPROVED_SCENE_CUT':
     self.assertTrue(set(request['approved_scene_cuts'])<=set(scenes['scenes']))
     self.assertEqual(request['source_commit'],scenes['source_commit'])
   else:self.assertEqual(request['status'],'REQUESTED_NOT_PRODUCED_NOT_APPROVED')
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
 def test_new_delivery_has_all_frames_and_valid_runtime_identities(self):
  data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())
  cast=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
  self.assertEqual(set(data['source_commits']),{'8c80550dda6ecf7af335827bba7e4fa6f4052ddf','f25caf86ded3a8d874c938e353d14c268b23b8e2','438e81fe8d9d5d9a1b9773b6ee9323cbb9f47c35','e523ad0995efa9012780438785e8bb0f1555c628','a59c4fed98b707febd7d9572f4d0bd555f2f194b','1687deb04d44746fa5ca819db72fc03ce3623b8a'})
  self.assertFalse(set(data['people'])-set(cast))
  for person,entry in data['people'].items():
   self.assertEqual(entry['status'],'approved_runtime')
   self.assertEqual(set(entry['profiles']),{'560','760','840'})
   for profile in entry['profiles'].values():
    self.assertEqual(set(profile['frames']),{'neutral','joy','angry','anxious','surprise_talk','surprise_react'})
    hashes=set()
    for frame in profile['frames'].values():
     path=ROOT/'game'/frame['file'];self.assertTrue(path.is_file())
     self.assertEqual(path.suffix,'.webp') # Keep frequently used portraits out of progressive PNG unloading.
     hashes.add(hashlib.sha256(path.read_bytes()).hexdigest())
    self.assertEqual(len(hashes),6,person)
 def test_approved_fifty_source_registry_and_smooth_renderer(self):
  data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text());self.assertEqual(len(data['people']),59)
  fullbody=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']
  self.assertEqual(set(data['people']),set(fullbody)-{'dad','elder','bodum','workshop'})
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text()
  self.assertIn('nearest=False,subpixel=True',source);self.assertNotIn('nearest=True',source)
