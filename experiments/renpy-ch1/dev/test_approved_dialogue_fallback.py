"""Approved close-ups may degrade in resolution, never revert to a legacy design."""
import textwrap,types,unittest
from pathlib import Path
class ApprovedFallback(unittest.TestCase):
 def test_missing_sizes_keep_approved_art_or_explicit_unavailable_state(self):
  source=(Path(__file__).resolve().parents[1]/'game/systems/room13_dialogue_beats.rpy').read_text()
  body=source.split('    def r13_dialogue_source_neutral(person,pose,height):',1)[1].split('    def r13_dialogue_beat_art',1)[0]
  profiles={str(h):dict(canvas=[h,h],frames={'neutral':dict(file='approved/'+str(h),offset=[0,0])}) for h in (560,760,840)}
  available=set();logs=[]
  def node(*args,**kw):return (args,kw)
  env=dict(store=types.SimpleNamespace(r13_meeting_active=False),r13_dialogue_pose_source=lambda *a:{},R13_DIALOGUE_POSE_SOURCE={'people':{}},r13_fullbody_key=lambda p:p,r13_dialogue_source_profile=lambda *a:profiles['840'],R13_DIALOGUE_TALK_ART={'people':{'test':{'profiles':profiles}}},renpy=types.SimpleNamespace(loadable=lambda f:f in available,log=logs.append),Fixed=node,Transform=node,Text=node)
  exec('def r13_dialogue_source_neutral(person,pose,height):\n'+textwrap.indent(textwrap.dedent(body),'    '),env);render=env['r13_dialogue_source_neutral']
  available.add('approved/840');self.assertIn('approved/840',str(render('test','neutral',840)))
  available.clear();available.add('approved/760');self.assertIn('approved/760',str(render('test','neutral',840)))
  available.clear();result=render('test','neutral',840);self.assertIsNotNone(result);self.assertIn('불러오지 못했습니다',str(result));self.assertTrue(logs)
if __name__=='__main__':unittest.main()
