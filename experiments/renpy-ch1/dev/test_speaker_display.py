"""Presentation must not infer masked identities or mutate story/character registries."""
import copy,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class SpeakerDisplay(unittest.TestCase):
 def setUp(self):
  names=dict(resident_nubi='누비 아주머니',resident_momo='모모',resident_musoe='무쇠 할아버지',resident_seori='서리 검사원',resident_ppul='뿔이 촌장',resident_eunho='은호 사장',resident_teacher='사자 선생님',resident_owlgp='부엉이 할아버지',granny='할머니',buri='부리')
  self.original=copy.deepcopy(names)
  self.env=dict(R13_NAMES=names,R13_PUBLIC_ROLES=dict(resident_nubi='세탁',resident_momo='박물관',buri='수리점'))
  src=(ROOT/'game/room13_speaker_display.rpy').read_text().split('init 150 python:\n')[1]
  exec(textwrap.dedent(src),self.env)
 def test_known_labels_and_unchanged_registry(self):
  self.assertEqual(self.env['r13_speaker_label']('누비 아주머니'),'누비')
  self.assertEqual(self.env['r13_speaker_label']('모모 관장'),'모모')
  self.assertEqual(self.env['r13_display_name']('buri'),'부리')
  self.assertEqual(self.env['R13_NAMES'],self.original)
 def test_unknowns_role_only_and_relations_are_preserved(self):
  for label in (None,'','???','낯선 사람','부엉이 할아버지','사자 선생님','할머니','누군가 · ???'):
   self.assertEqual(self.env['r13_speaker_label'](label),label)
 def test_authored_speech_not_rewritten(self):
  for line in ('누비 아주머니, 안녕하세요.','누비 씨에게 물어볼게요.','모모 관장이 건넨 종이'):
   self.assertEqual(self.env['r13_speaker_label'](line),line)
 def test_label_contrast_on_ink_and_paper(self):
  from test_typography_roles import contrast
  self.assertGreaterEqual(contrast('#FFF0CC','#352c27'),7)
  self.assertGreaterEqual(contrast('#493421','#efe7d2'),7)
 def test_roles_remain_separate(self):
  for person,role in [('resident_nubi','세탁'),('resident_momo','박물관'),('buri','수리점')]:
   self.assertEqual(self.env['r13_display_role'](person),role)
   self.assertNotIn(role,self.env['r13_display_name'](person))
if __name__=='__main__':unittest.main()
