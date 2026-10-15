"""Live statements and public ballots cannot manufacture proof, witnesses or endings."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MeetingFlow(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(propositions=[],flags=[],evidence=[],finale_started=False))
  def edit(**kw):
   s=copy.deepcopy(self.store.room13);s.update(kw);self.store.room13=s
  self.env=dict(store=self.store,winter_copy=copy,r13_edit=edit,r13_has=lambda f:f in self.store.room13['flags'])
  for file,marker in [('systems/room13_debate.rpy','init 98 python:\n'),('systems/room13_meeting_flow.rpy','init 100 python:\n')]:
   src=(ROOT/'game'/file).read_text().split(marker,1)[1].split('\nlabel ',1)[0]
   exec(textwrap.dedent(src),self.env)
 def test_ownership_does_not_cast_votes_or_prove_anything(self):
  self.store.room13['evidence']=['E05','E35','E36']
  before=copy.deepcopy(self.store.room13)
  v=self.env['r13_meeting_vote_snapshot']('C1','correct')
  self.assertEqual(self.store.room13,before)
  self.assertEqual(v['tally'],[8,0,0])
  self.assertEqual(v['propositions'],[])
 def test_votes_follow_actual_existing_proof_model(self):
  self.env['r13_debate_mark']('broken','C1','s2')
  before=self.env['r13_meeting_vote_snapshot']('C1','weak')
  self.store.room13['propositions']=['C1']
  after=self.env['r13_meeting_vote_snapshot']('C1','correct')
  self.assertGreater(after['tally'][2],before['tally'][2])
  self.assertEqual(sum(after['tally']),8)
  self.assertEqual(after['tally'],self.env['r13_debate_tally']('trial'))
 def test_recording_a_vote_changes_only_vote_history(self):
  self.store.room13.update(trial_result='pending',daram_state='with_dad',ending=None)
  before=copy.deepcopy(self.store.room13)
  self.env['r13_meeting_record_vote']('C2','correct')
  self.assertEqual({k:v for k,v in self.store.room13.items() if k!='meeting_votes'},before)
  self.assertNotIn('C2',self.store.room13['propositions'])
 def test_repeat_vote_updates_snapshot_without_duplicate_voters(self):
  f=self.env['r13_meeting_record_vote'];f('C1','weak');f('C1','correct')
  self.assertEqual(len(self.store.room13['meeting_votes']),1)
  voters=self.store.room13['meeting_votes']['C1']['voters']
  self.assertEqual(len({v['person'] for v in voters}),len(voters))
 def test_live_reveal_uses_exact_authored_line(self):
  self.store.r13_meeting_claim='C1';self.store.r13_debate_selected='s1'
  self.store.r13_packet=self.env['R13_DEBATE']['C1']['statements'][0]['press'][-1]
  self.assertEqual(self.env['r13_meeting_live_target'](),'s2')
  self.assertFalse(self.env['r13_debate_visible']('C1',self.env['r13_debate_statement']('C1','s2')))
  self.store.r13_packet=('seryeon','문이라는 말만 나오는 무관한 대사')
  self.assertEqual(self.env['r13_meeting_live_target'](),'s1')
 def test_live_presentation_is_not_reentrant_or_dads_reply(self):
  self.store.r13_meeting_claim='C1';self.store.r13_debate_selected='s1'
  self.store.r13_packet=('seryeon','주장');self.store.r13_meeting_active=True
  f=self.env['r13_meeting_can_interrupt'];self.assertTrue(f())
  self.store.r13_meeting_interrupting=True;self.assertFalse(f())
  self.store.r13_meeting_interrupting=False;self.store.r13_packet=('dad','답');self.assertFalse(f())
 def test_forged_goods_cannot_become_preparation(self):
  result,rows=self.env['r13_debate_judge']('F3','s3','E21')
  self.assertEqual(result,'soft');self.assertEqual(self.store.room13['flags'],[])
  self.assertFalse(self.env['r13_debate_is_broken']('F3','s3'))
 def test_camera_moves_only_for_a_new_real_speaker(self):
  env=self.env;clock=[10.0]
  env.update(CAST={p:{} for p in ['seryeon','resident_ppul','buri','nabi','resident_bori','resident_tori','doto','resident_kongi','granny','resident_seori','mom']},persistent=types.SimpleNamespace(room13_motion=True),renpy=types.SimpleNamespace(Displayable=object,get_game_runtime=lambda:clock[0],is_skipping=lambda:False))
  src=(ROOT/'game/room13_meeting_seating.rpy').read_text().split('init 99 python:\n',1)[1].split('\ntransform ',1)[0]
  exec(textwrap.dedent(src),env)
  self.store.r13_meeting_shot_revision=0
  f=env['r13_meeting_focus_change'];f('C1','seryeon');first=self.store.r13_meeting_shot_revision
  clock[0]+=1;f('C1','seryeon');f('C1','dad')
  self.assertEqual(self.store.r13_meeting_shot_revision,first)
  self.assertEqual(self.store.r13_meeting_pan_started,10.0)
  f('C1','resident_ppul');self.assertEqual(self.store.r13_meeting_shot_revision,first+1)
  trans=types.SimpleNamespace(xoffset=0);tick=env['r13_meeting_pan_tick']
  self.assertIsNotNone(tick(trans,0,0));self.assertNotEqual(trans.xoffset,0)
  clock[0]+=.3;self.assertIsNone(tick(trans,0,0));self.assertEqual(trans.xoffset,0)
  f('C1','buri');env['persistent'].room13_motion=False;tick(trans,0,0);self.assertEqual(trans.xoffset,0)
  people=[p for p,stance in env['r13_meeting_cast']('C1','trial')]
  self.assertNotIn('dad',people)
  for i,person in enumerate(people):
   self.assertEqual(env['r13_meeting_neighbors']('C1',person),(people[i-1],people[(i+1)%len(people)]))
if __name__=='__main__':unittest.main()
