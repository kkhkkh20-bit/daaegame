"""Direction follows canonical outcomes; it cannot prove a claim or fabricate a voter."""
import copy,textwrap,types,unittest
from pathlib import Path
import test_meeting_flow as flow_tests
ROOT=Path(__file__).resolve().parents[1]
class CouncilDirection(unittest.TestCase):
 def setUp(self):
  fixture=flow_tests.MeetingFlow();fixture.setUp();self.s=fixture.store;self.e=fixture.env
  self.calls=[];self.playing=None
  def play(path,**kw):self.playing=path;self.calls.append(('play',path))
  self.e.update(CAST={p:{} for p in ('granny','nabi','resident_ppul','resident_seori','buri','dad')},
   r13_viewpoint=lambda:'dad',R13_BGM={k:k for k in ('council','pressure','altar')},
   r13_meeting_kind=lambda session:'stone' if session=='finale' else 'round',
   r13_meeting_cast=lambda c,s:[('resident_ppul',0),('granny',0),('nabi',1)],
   r13_sound_ambience=lambda k:self.calls.append(('amb',k)),
   renpy=types.SimpleNamespace(audio=types.SimpleNamespace(audio=types.SimpleNamespace(get_channel=lambda channel:types.SimpleNamespace(context=types.SimpleNamespace(secondary_volume=1.0)))),music=types.SimpleNamespace(play=play,get_playing=lambda **kw:self.playing,get_pause=lambda **kw:False,
    stop=lambda **kw:self.calls.append(("stop",kw.get("channel"))),
    set_pause=lambda v,**kw:self.calls.append(('pause',v)),set_volume=lambda v,**kw:self.calls.append(('volume',v))),
    hide_screen=lambda n:self.calls.append(('hide',n))))
  src=(ROOT/'game/systems/room13_meeting_direction.rpy').read_text().split('init 174 python:\n',1)[1].split('\n# Brief impact',1)[0]
  exec(textwrap.dedent(src),self.e)
  self.s.r13_meeting_active=True;self.s.r13_meeting_claim='C2'
 def test_every_hearing_identity_and_counter_result_get_distinct_beats(self):
  phase=self.e['r13_meeting_direct_phase']
  for c in ('C1','F4','Q1','Q2','Q3','Q4','Q5A','Q5','Q6'):
   self.assertEqual(phase('meeting:live:'+c+':s1',0,'granny'),'listen')
   self.assertEqual(phase('meeting:live:'+c+':s1',1,'nabi'),'reaction')
   self.assertEqual(phase('debate:break:'+c+':s1:E01',0,'dad'),'explain')
   self.assertEqual(phase('debate:counter:'+c+':s1',0,'granny'),'recover')
   self.assertEqual(phase('debate:counter_wrong:'+c+':s1:weak',0,'granny'),'reversal')
  self.assertEqual(phase('debate:unanswerable:C2',0,'resident_ppul'),'loss')
 def test_direction_does_not_mutate_case_proof_votes_or_clock(self):
  before=copy.deepcopy(self.s.room13)
  for beat in self.e['R13_MEETING_BEATS']:
   self.e['r13_meeting_direct_beat'](beat,'C2','s1','E06')
  self.assertEqual(self.s.room13,before)
 def test_audio_ducks_without_restart_and_counter_reclaims_pressure(self):
  beat=self.e['r13_meeting_direct_beat']
  beat('listen','C2');beat('select');beat('explain');beat('shaken')
  self.assertEqual([c for c in self.calls if c[0]=='play'],[('play','council')])
  beat('recover');self.assertEqual(self.playing,'pressure')
  beat('select');beat('explain');self.assertEqual(self.playing,'pressure')
  self.e['r13_meeting_direct_end']()
  self.assertIn(('volume',1.0),self.calls);self.assertIn(('pause',False),self.calls)
 def test_altar_keeps_its_track_and_wind(self):
  self.e['r13_meeting_direct_beat']('listen','F1')
  self.assertEqual(self.playing,'altar');self.assertIn(('amb','wind'),self.calls)
 def test_culprit_is_not_inferred_and_authored_faces_take_priority(self):
  direct=self.e['r13_meeting_direct_line']
  self.assertEqual(direct('debate:break:C3:s2:E12',0,('granny','reply'),'neutral','neutral')[1],'surprise')
  self.assertEqual(direct('debate:counter:C3:s2',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  p=('granny','reply',{'expression':'flustered'})
  self.assertEqual(direct('debate:break:C3:s2:E12',0,p,'neutral','flustered')[1],'flustered')
  self.assertEqual(direct('meeting:live:C3:s2',0,('granny','reply'),'neutral','neutral')[1],'neutral')
 def test_pressure_carries_across_proved_claims_but_opponent_can_recover(self):
  self.s.r13_meeting_claim='C3'
  self.e['r13_debate_mark']('broken','C3','s2')
  direct=self.e['r13_meeting_direct_line']
  self.assertEqual(direct('meeting:live:C3:s3',0,('granny','reply'),'neutral','neutral')[1],'flustered')
  self.assertEqual(direct('debate:counter:C3:s3',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  self.e['r13_debate_mark']('broken','C3','s3')
  self.s.r13_meeting_claim='C4'
  self.assertEqual(direct('meeting:live:C4:s1',0,('granny','reply'),'neutral','neutral')[1],'anxious')
 def test_skipped_statement_does_not_telegraph_a_new_rebuttal(self):
  self.s.r13_meeting_claim='F4';self.s.room13['propositions']=['C4']
  pose=self.e['r13_meeting_direct_line']('meeting:live:F4:s1',0,('granny','reply'),'neutral','neutral')[1]
  self.assertEqual(pose,'neutral')
 def test_chatter_uses_attendees_once_and_never_changes_suspicion(self):
  before=copy.deepcopy(self.s.room13);m=self.e['r13_meeting_direct_murmurs']
  lines=m('C2','s1','countered')
  self.assertEqual(len(lines),1);self.assertIn(lines[0][0],('granny','nabi'))
  self.assertEqual(m('C2','s1','countered'),[])
  self.assertEqual(m('C2','s1','wrong'),[])
  self.assertEqual(self.s.room13,before)
 def test_cleanup_without_ownership_does_not_change_quiet_scene_audio(self):
  self.s.r13_meeting_direction_return_audio={}
  self.e['r13_meeting_direct_end']()
  self.assertFalse(any(c[0] in ('volume','pause','play','stop') for c in self.calls))
 def test_loading_explanation_unpauses_and_restores_quiet_audio(self):
  self.e['r13_meeting_direct_beat']('explain','C2')
  self.calls.clear();self.e['r13_meeting_direct_after_load']()
  self.assertIn(('pause',False),self.calls)
  self.assertIn(('volume',.58),self.calls)
  self.assertEqual(self.s.r13_meeting_direction['beat'],'explain')
