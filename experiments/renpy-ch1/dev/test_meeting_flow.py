"""Live statements and public ballots cannot manufacture proof, witnesses or endings."""
import copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class MeetingFlow(unittest.TestCase):
 def setUp(self):
  self.store=types.SimpleNamespace(room13=dict(propositions=[],flags=[],evidence=[],finale_started=False))
  def edit(**kw):
   s=copy.deepcopy(self.store.room13);s.update(kw);self.store.room13=s
  self.env=dict(config=types.SimpleNamespace(after_load_callbacks=[]),store=self.store,winter_copy=copy,r13_edit=edit,r13_has=lambda f:f in self.store.room13['flags'])
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
 def test_opinion_changes_compare_with_claim_entry_then_last_public_result(self):
  self.env['r13_meeting_begin_opinions']('C1')
  self.env['r13_debate_mark']('broken','C1','s2')
  self.store.room13['propositions']=['C1']
  vote=self.env['r13_meeting_record_vote']('C1','correct')
  self.assertEqual({row['person'] for row in vote['changed']},{'resident_tori','doto'})
  self.assertTrue(all(row['before']==0 and row['to']==2 for row in vote['changed']))
  before=copy.deepcopy(self.store.room13)
  lines=self.env['r13_meeting_reaction_lines'](vote)
  self.assertEqual({row[0] for row in lines},{'resident_tori','doto'})
  self.assertEqual(self.store.room13,before)
  self.assertEqual(self.env['r13_meeting_record_vote']('C1','correct')['changed'],[])
 def test_replay_cannot_interrupt_or_change_evidence(self):
  self.store.r13_meeting_claim='C1';self.store.r13_debate_selected='s1'
  self.store.r13_meeting_active=True;self.store.r13_packet=('seryeon','주장')
  self.store.r13_meeting_replaying=True
  self.assertFalse(self.env['r13_meeting_can_interrupt']())
 def test_finding_is_not_visible_before_actual_rebuttal(self):
  self.store.r13_meeting_findings={'C1:s2':'주방에서 통로를 열었다.'}
  self.assertIsNone(self.env['r13_meeting_finding']('C1','s2'))
  self.env['r13_debate_mark']('broken','C1','s2')
  self.assertEqual(self.env['r13_meeting_finding']('C1','s2'),'주방에서 통로를 열었다.')
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
 def test_loading_in_live_picker_restores_outer_cursor_and_preserves_proof(self):
  calls=[];self.env['renpy']=types.SimpleNamespace(hide_screen=lambda name:calls.append(name),hide=lambda name:calls.append(name))
  self.store.r13_meeting_pending_resume={'r13_index':2,'r13_page_i':1,'r13_read_id':'outer','r13_packet':('seryeon','원래 문장'),'r13_meeting_focus':'seryeon'}
  self.store.r13_index=99;self.store.r13_page_i=0;self.store.r13_read_id='child';self.store.r13_meeting_interrupting=True
  self.store.room13['propositions']=['C1']
  self.env['r13_meeting_resume_after_load']()
  self.assertEqual((self.store.r13_index,self.store.r13_page_i,self.store.r13_read_id),(2,1,'outer'))
  self.assertEqual(self.store.room13['propositions'],['C1'])
  self.assertIsNone(self.store.r13_meeting_pending_resume);self.assertFalse(self.store.r13_meeting_interrupting)
  self.assertIn('r13_book',calls)
  self.env['r13_meeting_resume_after_load']();self.assertEqual(self.store.r13_index,2)
 def test_camera_moves_only_for_a_new_real_speaker(self):
  env=self.env;clock=[10.0]
  env.update(CAST={p:{} for p in ['seryeon','resident_ppul','buri','nabi','resident_bori','resident_tori','doto','resident_kongi','granny','resident_seori','mom']},persistent=types.SimpleNamespace(room13_motion=True),renpy=types.SimpleNamespace(Displayable=object,loadable=lambda path:False,display=types.SimpleNamespace(core=types.SimpleNamespace(get_time=lambda:clock[0])),is_skipping=lambda:False))
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
  next_statement=env['r13_meeting_next_statement']
  self.assertEqual(next_statement('C1','s1',step=-1),'s1')
  env['r13_debate_mark']('pressed','C1','s1')
  self.assertEqual(next_statement('C1','s1',step=-1),'s2')
  self.assertEqual(next_statement('C1','s2'),'s1')
if __name__=='__main__':unittest.main()
