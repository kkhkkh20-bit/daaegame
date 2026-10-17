"""Registered fullbody-only actions must survive line direction and speaker routing."""
import json,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def function(path,name):
 text=(ROOT/path).read_text();start=text.index('    def '+name+'(');end=text.find('\n    def ',start+1)
 return textwrap.dedent(text[start:end if end>=0 else None])
class AuthoredRouting(unittest.TestCase):
 def test_teacher_actions_and_unknown_pose(self):
  data=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())
  files={p['file'] for x in data['people'].values() for p in x.get('poses',{}).values() if (ROOT/'game'/p['file']).is_file()}
  env=dict(R13_FULLBODY=data,R13_FULLBODY_FILES=files,R13_FULLBODY_DIALOGUE=True,r13_fullbody_key=lambda p:p.removeprefix('interview_'),R13_ACTING={'resident_teacher':{'neutral':{}}},R13_DIRECTION={},R13_LINE_DIRECTION={},r13_fullbody_line_emotion=lambda *a:None)
  exec(function('game/room13_fullbody_dialogue.rpy','r13_fullbody_authored_pose'),env)
  # Stop before class declaration rather than importing Ren'Py renderer.
  code=function('game/room13_acting.rpy','r13_line_performance').split('class R13FurnitureMask',1)[0]
  exec(code,env)
  for pose in ('write_attendance','collapse_attendance'):
   self.assertEqual(env['r13_line_performance']('fixture',0,('resident_teacher','line',{'pose':pose})),('neutral',pose))
  self.assertEqual(env['r13_line_performance']('fixture',0,('resident_teacher','line',{'pose':'missing_pose'})),('neutral','neutral'))
 def test_ppul_source_opt_in_keeps_original_file_and_crop(self):
  p=json.loads((ROOT/'game/assets/room13-fullbody-dialogue.json').read_text())['people']['resident_ppul']['poses']['kneel_stone']
  self.assertEqual(p['crop'],[18,24,483,713]);self.assertTrue(p['mapped_image']['smooth_source']);self.assertTrue(p['mapped_image']['native_detail'])
if __name__=='__main__':unittest.main()
