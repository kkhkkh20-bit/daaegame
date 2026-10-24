"""Approved dialogue frames must not leak into authored actions or meetings."""
import ast,json,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class BDialogueArt(unittest.TestCase):
 def setUp(self):
  self.old=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
  self.new=json.loads((ROOT/'game/assets/room13-dialogue-b-primary50.json').read_text())
  source=(ROOT/'game/systems/room13_dialogue_beats.rpy').read_text().split('init 170 python:\n',1)[1]
  tree=ast.parse(textwrap.dedent(source));tree.body=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
  self.env=dict(store=SimpleNamespace(r13_meeting_active=False,r13_thought_active=False),R13_DIALOGUE_B_ART=self.new,R13_DIALOGUE_TALK_ART={'people':self.old},R13_DIALOGUE_POSE_SOURCE=json.loads((ROOT/'game/assets/room13-dialogue-pose-source-art.json').read_text()),R13_FULLBODY_PLAIN={'neutral','joy','angry','anxious','surprise'},r13_fullbody_key=lambda p:p)
  exec(compile(tree,'beats','exec'),self.env)
 def test_meeting_uses_original_profiles(self):
  self.env['store'].r13_meeting_active=True
  for person,entry in self.old.items():self.assertIs(self.env['r13_dialogue_render_profiles'](person,entry),entry.get('profiles',{}))
 def test_authored_pose_precedes_b_emotions(self):
  p=self.env['r13_dialogue_source_profile']('granny','withdraw_hand',840)
  self.assertIn('dialogue-pose-source/granny/withdraw_hand',p['frames']['neutral']['file'])
 def test_neutral_and_held_frames_unchanged(self):
  for person,profiles in self.new.items():
   for h,p in profiles.items():
    self.assertEqual(p['canvas'],self.old[person]['profiles'][h]['canvas'])
    self.assertEqual(p['frames']['neutral'],self.old[person]['profiles'][h]['frames']['neutral'])
  for person,emotion in [('resident_lamplighter','angry'),('resident_lamplighter','joy'),('resident_lamplighter','surprise_talk'),('resident_teacher','surprise_talk')]:
   for h,p in self.new[person].items():self.assertEqual(p['frames'][emotion],self.old[person]['profiles'][h]['frames'][emotion])
 def test_all_46_frames_preserve_visible_height_bottom_and_center(self):
  count=0
  for person,profiles in self.new.items():
   for h,p in profiles.items():
    for emotion,f in p['frames'].items():
     if not f['file'].startswith('assets/dialogue-b-primary50/'):continue
     count+=1;self.assertTrue(all(type(v) is int for v in f['offset']));old=self.old[person]['profiles'][h]['frames'][emotion]
     with Image.open(ROOT/'game'/old['file']) as im:ob=im.getbbox()
     with Image.open(ROOT/'game'/f['file']) as im:nb=im.getbbox()
     os=old.get('scale',1);ns=f['scale']
     self.assertAlmostEqual((ob[3]-ob[1])*os,(nb[3]-nb[1])*ns)
     self.assertAlmostEqual(old['offset'][1]+ob[3]*os,f['offset'][1]+nb[3]*ns,delta=.51)
     self.assertAlmostEqual(old['offset'][0]+(ob[0]+ob[2])*os/2,f['offset'][0]+(nb[0]+nb[2])*ns/2,delta=.51)
     self.assertGreaterEqual(f['offset'][0]+nb[0]*ns,0)
     self.assertLessEqual(f['offset'][0]+nb[2]*ns,p['canvas'][0]+.001)
     self.assertLessEqual(f['offset'][1]+nb[3]*ns,p['canvas'][1]+.001)
  self.assertEqual(count,138)
 def test_thought_and_unknown_pose_keep_existing_guards(self):
  self.env['store'].r13_thought_active=True
  self.assertIsNone(self.env['r13_dialogue_source_profile']('granny','joy',840))
  self.env['store'].r13_thought_active=False
  self.assertIsNone(self.env['r13_dialogue_source_profile']('granny','unapproved_new_pose',840))
