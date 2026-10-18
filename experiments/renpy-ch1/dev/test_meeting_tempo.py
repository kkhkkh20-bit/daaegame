import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class Tempo(unittest.TestCase):
 def setUp(self):
  self.s=types.SimpleNamespace(room13={'run_token':'run'},r13_meeting_claim='C2',r13_meeting_tempo_milestones=[],r13_meeting_proof_reveal=None,r13_meeting_collective=None)
  self.playing='assets/bgm-council.mp3';self.pos=10;self.calls=[]
  def play(path,**kw):self.playing=path;self.calls.append(('play',path,kw))
  self.e=dict(store=self.s,R13_BGM={n:'assets/bgm-'+n+'.mp3' for n in ('council','pressure','altar')},renpy=types.SimpleNamespace(music=types.SimpleNamespace(get_playing=lambda **kw:self.playing,get_pos=lambda **kw:self.pos,play=play,queue=lambda path,**kw:self.calls.append(('queue',path,kw)))))
  src=(ROOT/'game/systems/room13_meeting_tempo.rpy').read_text().split('init 173 python:\n')[1].split('\ninit 192 python:')[0];exec(textwrap.dedent(src),self.e)
 def mark(self,sid):
  self.s.r13_meeting_proof_reveal=dict(claim='C2',sid=sid,revealed=True);self.e['r13_meeting_tempo_mark']('C2',sid)
 def test_distinct_meeting_milestones_not_person_pressure(self):
  before=copy.deepcopy(self.s.room13);self.mark('s1');self.mark('s1');self.assertEqual(self.e['r13_meeting_tempo_stage'](),1)
  self.mark('s2');self.mark('s3');self.assertEqual(self.e['r13_meeting_tempo_stage'](),2)
  self.s.r13_meeting_pressure={};self.assertEqual(self.e['r13_meeting_tempo_stage'](),2)
  self.assertEqual(before,self.s.room13);self.assertEqual(self.e['r13_meeting_tempo_stage']('C3'),0)
  self.s.room13['run_token']='new';self.assertEqual(self.e['r13_meeting_tempo_stage'](),0)
 def test_quiet_waits_for_collective_and_repeated_calls_do_not_restart(self):
  self.mark('s1');self.s.r13_meeting_collective={'phase':'playing'}
  self.assertEqual(self.e['r13_meeting_tempo_path']('council'),self.playing)
  self.s.r13_meeting_collective={'phase':'settled'};path=self.e['r13_meeting_tempo_path']('council');self.assertIn('tempo1',path)
  self.e['r13_meeting_tempo_play'](path);self.e['r13_meeting_tempo_play'](path)
  self.assertEqual(len(self.calls),1);self.assertIn('<from 9.434 loop 0>',self.calls[0][1]);self.assertTrue(self.calls[0][2]['loop'])
 def test_muted_position_none_safe_and_new_base_not_wrongly_seeked(self):
  self.pos=None;self.e['r13_meeting_tempo_play']('assets/bgm-council-tempo2.ogg');self.assertNotIn('<from',self.playing)
  self.pos=30;self.e['r13_meeting_tempo_play']('assets/bgm-pressure-tempo2.ogg');self.assertNotIn('<from',self.playing)
 def test_load_preserved_path_does_not_restart_and_rollback_can_lower_stage(self):
  self.mark('s1');self.mark('s2');self.playing='<from 12.300>assets/bgm-council-tempo2.ogg'
  self.e['r13_meeting_tempo_play'](self.e['r13_meeting_tempo_path']('council'));self.assertEqual(self.calls,[])
  self.s.r13_meeting_tempo_milestones=self.s.r13_meeting_tempo_milestones[:1]
  self.assertIn('tempo1',self.e['r13_meeting_tempo_path']('council'))
 def test_nested_evidence_context_carries_child_audio_position_back(self):
  values={'volume':.58,'paused':False,'path':'<from 8.000>assets/bgm-council-tempo1.ogg','position':21.5}
  self.e['renpy'].call_in_new_context=lambda *args:values
  self.e['renpy'].music.set_volume=lambda v,**kw:self.calls.append(('volume',v))
  self.e['renpy'].music.set_pause=lambda v,**kw:self.calls.append(('pause',v))
  before=copy.deepcopy(self.s.room13);self.e['r13_meeting_interrupt_with_tempo']('C2','s2')
  self.assertEqual(self.playing,'<from 21.500 loop 0>assets/bgm-council-tempo1.ogg')
  self.assertEqual(self.calls[-2:],[('volume',.58),('pause',False)])
  self.assertEqual(self.s.room13,before)
