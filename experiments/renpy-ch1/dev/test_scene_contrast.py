"""Presentation reads existing case state; it never selects new facts or sounds."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SceneContrast(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(case_state='pending',evidence=['E01'],flags=[],period=1,location='inn'))
  self.audio=[]
  self.e=dict(store=self.store,renpy=types.SimpleNamespace(music=types.SimpleNamespace(set_volume=lambda *a,**kw:self.audio.append((a,kw)))),r13_sound_scene_music=lambda bg,title,mood:'authored-track',r13_sound_choice=lambda bg,title,mood:('inn','fire'),Transform=lambda source,**kw:(source,kw),TintMatrix=lambda tint:1,SaturationMatrix=lambda value:1)
  src=(ROOT/'game/systems/room13_scene_contrast.rpy').read_text().split('init 163 python:\n')[1];exec(textwrap.dedent(src),self.e)
 def test_only_existing_occurred_state_in_three_interiors_is_treated(self):
  for location in ('inn','hall','room13','square','school','altar',None):
   self.assertIsNone(self.e['r13_scene_contrast_key'](location,'afternoon'))
  self.store.room13['case_state']='occurred';before=copy.deepcopy(self.store.room13)
  for location in ('inn','hall','room13'):
   self.assertEqual(self.e['r13_scene_contrast_key'](location,'afternoon'),'after')
  for location in ('square','school','altar',None):self.assertIsNone(self.e['r13_scene_contrast_key'](location,'evening'))
  self.assertEqual(self.store.room13,before)
 def test_scripted_heartbeat_keeps_original_strength(self):
  self.store.room13['case_state']='occurred'
  self.e['r13_sound_choice']=lambda bg,title,mood:(None,'heartbeat')
  self.e['r13_sound_scene_music']('hall','연기가 새는 문','search')
  self.assertEqual(self.audio[-1][0][0],1.)
 def test_unaffected_background_is_identical_and_treatment_does_not_crop(self):
  source=object();self.assertIs(self.e['r13_scene_treatment']('inn','morning',source),source)
  self.store.room13['case_state']='occurred'
  painted,properties=self.e['r13_scene_treatment']('inn','morning',source)
  self.assertIs(painted,source);self.assertEqual(set(properties),{'matrixcolor'})
 def test_tracks_stay_authored_only_ambience_channel_gain_changes_and_resets(self):
  self.store.room13['case_state']='occurred';before=copy.deepcopy(self.store.room13)
  self.assertEqual(self.e['r13_sound_scene_music']('front','여관 접수대','calm'),'authored-track')
  self.assertEqual(self.audio[-1][0][0],.65);self.assertEqual(self.audio[-1][1]['channel'],'ambience')
  for bg,mood in [('front','hearing'),('hall','quiet'),('room','travel'),('winter_square','search')]:
   self.e['r13_sound_scene_music'](bg,'기존 장면',mood);self.assertEqual(self.audio[-1][0][0],1.)
  self.assertEqual(self.store.room13,before)
