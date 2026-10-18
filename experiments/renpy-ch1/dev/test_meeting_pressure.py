import unittest,copy,textwrap,types
from pathlib import Path
import test_meeting_direction as direction
class PressurePilot(unittest.TestCase):
 def setUp(self):
  f=direction.CouncilDirection();f.setUp();self.e=f.e;self.s=f.s
  self.s.room13={'run_token':'test','victim_state':'dead','flags':[]};self.s.r13_meeting_pressure={};self.s.r13_meeting_pressure_events=[];self.s.r13_meeting_collective=None;self.s.r13_meeting_silence_ambience=None;self.s.r13_meeting_quiet_released=[]
  self.e.update(R13_DEATH_FLAGS={'resident_piko':'piko_dead'},r13_mom_absent=lambda:True,r13_has=lambda k:k in self.s.room13['flags'])
  self.e['r13_debate_statement']=lambda c,s:{'who':'resident_ppul'}
  self.e['r13_meeting_cast']=lambda c,s:[('resident_ppul',0),('buri',0),('resident_piko',0),('mom',0),('resident_owlgp',0)]
  self.s.r13_meeting_claim='C2';self.s.r13_meeting_active=True
  src=(Path(__file__).resolve().parents[1]/'game/systems/room13_meeting_pressure.rpy').read_text().split('init 191 python:\n',1)[1].split('\nscreen ',1)[0]
  exec(textwrap.dedent(src),self.e)
 def proof(self,sid):
  self.s.r13_meeting_proof_reveal={'claim':'C2','sid':sid,'identity':'proof:'+sid,'revealed':True}
  self.e['r13_meeting_pressure_proof']('C2',sid)
 def test_only_real_reveal_and_once_per_statement_not_per_evidence(self):
  before=copy.deepcopy(self.s.room13)
  self.s.r13_meeting_proof_reveal=None;self.e['r13_meeting_pressure_proof']('C2','s1');self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul'),0)
  self.proof('s1');self.proof('s1');self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul'),1)
  self.proof('s2');self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul'),2)
  self.assertEqual(self.s.room13,before)
 def test_recovery_once_and_other_claims_unchanged(self):
  self.proof('s1');self.proof('s2');self.e['r13_meeting_pressure_recover']('C2','s2');self.e['r13_meeting_pressure_recover']('C2','s2')
  self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul'),1)
  self.e['r13_meeting_pressure_change']('C3','s1','anything',1);self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul','C3'),0)
 def test_all_present_people_excludes_dead_absent_and_victim(self):
  self.s.room13['flags']=['piko_dead'];self.proof('s1')
  self.assertEqual(self.s.r13_meeting_collective['people'],['resident_ppul','buri'])
 def test_emotion_survives_line_change_and_neutral_slot(self):
  self.proof('s1');self.s.r13_meeting_proof_reveal=None
  fn=self.e['r13_meeting_direct_line']
  line='그 방에는 아이 혼자 있었습니다. 다시 휘두를 사람이 누가 있습니까?'
  ex,pose=fn('meeting:live:C2:s3',0,('resident_ppul',line),'neutral','neutral')
  self.assertEqual(pose,'anxious');self.assertNotIn('resident_ppul',self.s.r13_meeting_art_slots)
  fn('meeting:live:C2:s3',1,('buri','다른 사람의 말'),'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_direction_poses['resident_ppul'],'anxious')
 def test_load_settles_transient_without_losing_pressure(self):
  self.proof('s1');self.s.r13_meeting_active=False
  levels=copy.deepcopy(self.s.r13_meeting_pressure);events=list(self.s.r13_meeting_pressure_events)
  self.e['r13_meeting_pressure_after_load']()
  self.assertEqual(self.s.r13_meeting_collective['phase'],'settled');self.assertEqual(self.s.r13_meeting_pressure,levels);self.assertEqual(self.s.r13_meeting_pressure_events,events)
 def test_new_run_does_not_inherit_pressure(self):
  self.proof('s1');self.s.room13['run_token']='next';self.assertEqual(self.e['r13_meeting_pressure_level']('resident_ppul'),0)
 def test_silence_timeout_restores_ambience_without_touching_preferences(self):
  gains={'music':.8,'ambience':.4};screens={};prefs={'music':.23,'sfx':0.0}
  self.e['_r13_pressure_direct_audio']=lambda:gains.update(music=.58)
  self.e['r13_meeting_channel_gain']=lambda c:gains[c]
  self.e['renpy'].get_screen=lambda name:screens.get(name)
  self.e['renpy'].show_screen=lambda name,**kw:screens.update({name:kw})
  self.e['renpy'].hide_screen=lambda name:screens.pop(name,None)
  self.e['renpy'].music.set_volume=lambda value,channel,**kw:gains.update({channel:value})
  self.s.r13_meeting_proof_reveal={'identity':'real-proof','revealed':False}
  self.e['r13_meeting_direct_audio']();self.assertEqual(gains,{'music':0.0,'ambience':0.0})
  self.e['r13_meeting_quiet_release']('real-proof')
  self.assertEqual(gains,{'music':.58,'ambience':.4});self.assertEqual(prefs,{'music':.23,'sfx':0.0})
  self.e['r13_meeting_direct_audio']();self.assertEqual(gains['music'],.58)

if __name__=='__main__':unittest.main()
