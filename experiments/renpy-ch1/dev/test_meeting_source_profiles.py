import json,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MeetingSources(unittest.TestCase):
 def setUp(self):
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text();block=source.split('    def r13_dialogue_fit_profile',1)[1].split('    def r13_dialogue_source_neutral',1)[0]
  self.env=dict(store=types.SimpleNamespace(r13_meeting_active=True,r13_thought_active=False),R13_DIALOGUE_TALK_ART=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text()),R13_DIALOGUE_POSE_SOURCE=json.loads((ROOT/'game/assets/room13-dialogue-pose-source-art.json').read_text()),R13_FULLBODY_PLAIN={'neutral','joy','angry','anxious','surprise','thinking'},r13_fullbody_key=lambda p:p.removeprefix('interview_'))
  exec(textwrap.dedent('    def r13_dialogue_fit_profile'+block),self.env)
 def test_every_approved_person_supports_all_meeting_heights(self):
  get=self.env['r13_dialogue_source_profile']
  for who in self.env['R13_DIALOGUE_TALK_ART']['people']:
   for height in (740,776,840,876):
    p=get(who,'neutral',height);self.assertIsNotNone(p);self.assertTrue(p['frames']['neutral']['file'].startswith(('assets/dialogue-source-master/','assets/dialogue-source-master-v2/')))
    for n in p['canvas']:self.assertGreater(n,0)
 def test_chair_keys_have_letter_bust_without_changing_field_pose(self):
  get=self.env['r13_dialogue_source_profile'];self.env['store'].r13_meeting_active=False
  for pose in ('chair_listen','chair_read'):
   self.assertIn('/seryeon/'+pose+'/',get('seryeon',pose,840)['frames']['neutral']['file'])
  self.assertIn('/kid_kkomi/door_peek/',get('kid_kkomi','door_peek',840)['frames']['neutral']['file'])
  self.assertIn('/resident_teacher/write_attendance/',get('resident_teacher','write_attendance',840)['frames']['neutral']['file'])
 def test_scale_preserves_aspect_and_frame_offsets(self):
  fit=self.env['r13_dialogue_fit_profile'];p={'840':dict(canvas=[500,900],frames={'neutral':dict(file='x',offset=[20,30])})}
  result=fit(p,876);ratio=876/840
  self.assertAlmostEqual(result['frames']['neutral']['scale'],ratio);self.assertEqual(result['canvas'],[round(500*ratio),round(900*ratio)])
 def test_meeting_variant_offsets_are_pixels_at_every_venue_height(self):
  source=(ROOT/'game/room13_meeting_camera.rpy').read_text()
  block=source.split('    def r13_meeting_slot_art',1)[1].split('    def r13_meeting_reaction_phase',1)[0]
  registry=json.loads((ROOT/'game/assets/room13-meeting-source-art.json').read_text())
  transforms=[]
  env=dict(store=types.SimpleNamespace(r13_meeting_art_slots={}),R13_MEETING_SOURCE_ART=registry,renpy=types.SimpleNamespace(loadable=lambda p:True),Transform=lambda *a,**kw:transforms.append(kw) or kw,Fixed=lambda *a,**kw:kw)
  exec(textwrap.dedent('    def r13_meeting_slot_art'+block),env)
  for who,slots in registry.items():
   for slot,spec in slots.items():
    env['store'].r13_meeting_art_slots={who:slot}
    for height in (740,840):
     env['r13_meeting_slot_art'](who,height)
     for axis in ('xpos','ypos'):
      self.assertIs(type(transforms[-1][axis]),int, 'RenPy floats are relative positions')
      self.assertLess(abs(transforms[-1][axis]),spec["canvas"][0]*height/840)
if __name__=='__main__':unittest.main()
