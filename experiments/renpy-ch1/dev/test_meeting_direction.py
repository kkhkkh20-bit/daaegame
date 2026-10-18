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
 def test_c2_third_accusation_has_exact_stern_cue_without_next_line_leak(self):
  direct=self.e['r13_meeting_direct_line'];text='그 방에는 아이 혼자 있었습니다. 다시 휘두를 사람이 누가 있습니까?'
  direct('meeting:live:C2:s3',0,('resident_ppul',text),'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_art_slots,{'resident_ppul':'stern_statement'})
  direct('meeting:live:C2:s3',1,('resident_seori','그때 방에 있던 사람이 누구인지 확인하겠습니다.'),'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_art_slots,{})
  direct('meeting:live:C2:s3',0,('resident_ppul',text,{'expression':'angry'}),'angry','angry')
  self.assertEqual(self.s.r13_meeting_art_slots,{})
 def test_authored_anxious_slot_survives_legacy_avatar_expression(self):
  self.s.r13_meeting_active=True;self.s.r13_meeting_claim='C3'
  text='할머니가 공구를 가지러 주방에 가신 뒤로는…… 저도 못 봤어요.'
  self.e['r13_meeting_direct_line']('debate:break:C3:s2:E12',0,('nabi',text,{'expression':'anxious'}),'distressed','anxious')
  self.assertEqual(self.s.r13_meeting_art_slots,{'nabi':'witness_hesitate'})
 def test_surprise_waits_for_witness_explanation_and_self_reply_finishes(self):
  self.s.r13_meeting_claim='C3'
  self.e['renpy'].display=types.SimpleNamespace(core=types.SimpleNamespace(get_time=lambda:10.0))
  prepare=self.e['r13_meeting_prepare_proof'];direct=self.e['r13_meeting_direct_line']
  rows=[('nabi','공구를 가지러 간 뒤 보지 못했어요.'),('granny','그게 전부잖아요.')]
  prepare('C3','s2','E12',rows)
  direct('debate:break:C3:s2:E12',0,rows[0],'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_direction['beat'],'explain')
  self.assertIsNone(self.s.r13_meeting_shock_target)
  direct('debate:break:C3:s2:E12',1,rows[1],'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_shock_target,'granny')
  self.assertTrue(self.s.r13_meeting_proof_reveal['revealed'])
  self.assertEqual(self.e['r13_meeting_proof_boundary']('C3','s2',[rows[1]]),1)
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
  beat('select');beat('explain');beat('listen');self.assertEqual(self.playing,'pressure')
  beat('listen','C3');self.assertEqual(self.playing,'council')
  self.e['r13_meeting_direct_end']()
  self.assertIn(('volume',1.0),self.calls);self.assertIn(('pause',False),self.calls)
 def test_altar_keeps_its_track_and_wind(self):
  self.e['r13_meeting_direct_beat']('listen','F1')
  self.assertEqual(self.playing,'altar');self.assertIn(('amb','wind'),self.calls)
 def test_culprit_is_not_inferred_and_authored_faces_take_priority(self):
  direct=self.e['r13_meeting_direct_line']
  self.assertEqual(direct('debate:break:C3:s2:E12',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  self.assertEqual(direct('debate:counter:C3:s2',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  p=('granny','reply',{'expression':'flustered'})
  self.assertEqual(direct('debate:break:C3:s2:E12',0,p,'neutral','flustered')[1],'flustered')
  self.assertEqual(direct('meeting:live:C3:s2',0,('granny','reply'),'neutral','neutral')[1],'neutral')
 def test_unbound_new_lines_do_not_inherit_pressure_from_other_statements(self):
  self.s.r13_meeting_claim='C3'
  self.e['r13_debate_mark']('broken','C3','s2')
  direct=self.e['r13_meeting_direct_line']
  self.assertEqual(direct('meeting:live:C3:s3',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  self.assertEqual(direct('debate:counter:C3:s3',0,('granny','reply'),'neutral','neutral')[1],'neutral')
  self.e['r13_debate_mark']('broken','C3','s3')
  self.s.r13_meeting_claim='C4'
  self.assertEqual(direct('meeting:live:C4:s1',0,('granny','reply'),'neutral','neutral')[1],'neutral')
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

 def test_exact_cues_match_real_live_rows_and_never_classify_a_side(self):
  self.e['r13_meeting_cast']=lambda c,s:[(p,0) for p in self.e['CAST']]
  direct=self.e['r13_meeting_direct_line']
  for claim,sid in [('C2','s1'),('C2','s2'),('C2','s3'),('C3','s1')]:
   self.s.r13_meeting_claim=claim
   rows=self.e['r13_meeting_live_rows'](claim,sid)
   for i,row in enumerate(rows):
    direct('meeting:live:'+claim+':'+sid,i,row,'neutral','neutral')
    self.assertLessEqual(len(self.s.r13_meeting_direction_poses),2)
    if self.s.r13_meeting_listener:
     self.assertNotEqual(self.s.r13_meeting_listener,row[0])
   self.assertEqual(self.s.r13_meeting_direction_poses[rows[-1][0]],'neutral')

 def test_text_speaker_index_and_identity_each_guard_listener_cue(self):
  self.e['r13_meeting_cast']=lambda c,s:[(p,0) for p in self.e['CAST']]
  direct=self.e['r13_meeting_direct_line'];identity='meeting:live:C2:s1'
  row=self.e['r13_meeting_live_rows']('C2','s1')[0]
  direct(identity,0,row,'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_listener,'buri')
  for ident,i,p in [(identity,1,row),(identity,0,('nabi',row[1])),(identity,0,(row[0],row[1]+' ')),('meeting:replay:C2:s1',0,row)]:
   direct(ident,i,p,'neutral','neutral')
   self.assertIsNone(self.s.r13_meeting_listener)
   self.assertEqual(len(self.s.r13_meeting_direction_poses),1)

 def test_thought_metadata_is_not_an_authored_face_but_explicit_face_wins(self):
  direct=self.e['r13_meeting_direct_line'];identity='meeting:live:C2:s1'
  row=self.e['r13_meeting_live_rows']('C2','s1')[0]
  self.assertEqual(direct(identity,0,(*row,{'thought':False}),'neutral','neutral')[1],'neutral')
  self.assertEqual(self.s.r13_meeting_art_slots,{'resident_ppul':'stern_statement'})
  self.assertEqual(direct(identity,0,(*row,{'expression':'angry'}),'angry','angry')[1],'angry')
  self.assertEqual(self.s.r13_meeting_art_slots,{})

 def test_new_narration_clears_listener_and_previous_faces(self):
  direct=self.e['r13_meeting_direct_line']
  direct('meeting:live:C2:s1',1,('buri','reply',{'expression':'angry'}),'angry','angry')
  self.assertEqual(self.s.r13_meeting_direction_poses,{'buri':'angry'})
  direct('another',0,(None,'narration'),'neutral','neutral')
  self.assertEqual(self.s.r13_meeting_direction_poses,{})
  self.assertIsNone(self.s.r13_meeting_listener)

 def test_e08_reacts_only_after_proof_and_preserves_authored_anxiety(self):
  rows=self.e['r13_debate_statement']('C2','s1')['broken_by']['E08']
  before=copy.deepcopy(self.s.room13)
  self.e['r13_meeting_prepare_proof']('C2','s1','E08',rows)
  direct=self.e['r13_meeting_direct_line'];identity='debate:break:C2:s1:E08'
  direct(identity,0,rows[0],'neutral','neutral')
  self.assertIsNone(self.s.r13_meeting_reaction)
  direct(identity,1,rows[1],'flustered','flustered')
  self.assertEqual(self.s.r13_meeting_direction_poses,{'resident_ppul':'flustered'})
  self.assertEqual(self.s.r13_meeting_reaction['phase'],'pending')
  self.assertEqual(self.s.r13_meeting_reaction['pose'],'flustered')
  self.assertEqual(self.s.room13,before)
  self.e['r13_meeting_reaction_settle']()
  direct(identity,1,rows[1],'flustered','flustered')
  self.assertEqual(self.s.r13_meeting_reaction['phase'],'settled')
  # Re-selecting the same record does not rearm its one-shot reaction.
  self.e['r13_meeting_prepare_proof']('C2','s1','E08',rows)
  direct(identity,0,rows[0],'neutral','neutral')
  direct(identity,1,rows[1],'flustered','flustered')
  self.assertIsNone(self.s.r13_meeting_reaction)

 def test_wrong_soft_half_never_arm_reaction_or_change_proof(self):
  before=copy.deepcopy(self.s.room13)
  for result in ('wrong','soft','half'):
   self.e['r13_meeting_direct_line']('debate:'+result+':C2:s2:E07',0,('resident_seori','reply'),'neutral','neutral')
   self.assertIsNone(self.s.r13_meeting_reaction)
   self.assertNotIn(self.s.r13_meeting_direction['beat'],('shaken','resolve'))
  self.assertEqual(self.s.room13,before)

 def test_counter_stays_unbroken_until_canonical_answer(self):
  self.s.room13['propositions']=['C1']
  for key in ('E09','E10'):
   rows=self.e['r13_debate_statement']('C2','s3')['broken_by'][key]
   self.e['r13_meeting_prepare_proof']('C2','s3',key,rows)
   for i,row in enumerate(rows):
    self.e['r13_meeting_direct_line']('debate:break:C2:s3:'+key,i,row,'neutral','neutral')
   self.e['r13_meeting_direct_reveal']('C2','s3')
   self.e['r13_meeting_direct_line']('debate:counter:C2:s3',0,('resident_ppul','reply'),'neutral','neutral')
   self.assertEqual(self.s.r13_meeting_direction['beat'],'recover')
   self.assertFalse(self.e['r13_debate_is_broken']('C2','s3'))
   self.assertIsNone(self.s.r13_meeting_reaction)

 def test_end_boundary_can_paint_once_on_first_following_gasp(self):
  rows=self.e['r13_debate_statement']('C2','s2')['broken']
  self.e['r13_meeting_prepare_proof']('C2','s2','E35',rows)
  for i,row in enumerate(rows):
   self.e['r13_meeting_direct_line']('debate:break:C2:s2:E35',i,row,'neutral','neutral')
  self.e['r13_meeting_direct_reveal']('C2','s2')
  self.e['r13_meeting_direct_line']('meeting:gasp:C2:s2',0,('nabi','정말요?',{'pose':'surprise'}),'surprise','surprise')
  self.assertEqual(self.s.r13_meeting_reaction['phase'],'pending')
  self.assertEqual(self.s.r13_meeting_listener,'resident_ppul')
  self.assertEqual(set(self.s.r13_meeting_direction_poses),{'nabi','resident_ppul'})
  self.e['r13_meeting_direct_line']('meeting:gasp:C2:s2',1,('granny','그렇다고요?'),'neutral','neutral')
  self.assertIsNone(self.s.r13_meeting_reaction)

 def test_load_and_cancel_restore_faces_without_replaying_or_reverting_evidence(self):
  self.s.r13_meeting_reaction=dict(token='proof',person='granny',phase='playing',pose='anxious')
  self.s.r13_meeting_direction_poses={'granny':'anxious'}
  self.s.r13_meeting_line_token=('identity',0,'granny','text')
  self.s.r13_meeting_pending_resume={name:copy.deepcopy(getattr(self.s,name,None)) for name in self.e['R13_MEETING_RESUME_FIELDS']}
  self.s.room13['evidence']=['E08']
  self.e['renpy'].hide=lambda *a:None
  self.e['r13_meeting_resume_after_load']()
  self.assertEqual(self.s.r13_meeting_reaction['phase'],'settled')
  self.assertEqual(self.s.r13_meeting_direction_poses,{'granny':'anxious'})
  self.assertEqual(self.s.r13_meeting_line_token,('identity',0,'granny','text'))
  self.assertEqual(self.s.room13['evidence'],['E08'])
  self.e['r13_meeting_direct_after_load']()
  self.assertEqual(self.s.r13_meeting_reaction['phase'],'settled')

 def test_missing_old_save_fields_are_safe(self):
  self.e['r13_meeting_direct_after_load']()
  self.e['r13_meeting_direct_line']('meeting:replay:C2:s1',0,('resident_ppul','text'),'neutral','neutral')
  self.assertIsNone(self.s.r13_meeting_listener)

 def test_every_exact_cue_is_bound_to_current_authored_text(self):
  from meeting_direction_audit import authored_data
  specs=authored_data()['R13_DEBATE']
  for (identity,index,person,text),cue in self.e['R13_MEETING_LINE_CUES'].items():
   parts=identity.split(':');claim=parts[2];sid=parts[3]
   st=next(s for s in specs[claim]['statements'] if s['id']==sid)
   if parts[0]=='meeting':
    rows=[(st['who'],st['text'].replace('【','').replace('】',''))]
    reply=self.e['R13_MEETING_REJOINDERS'].get(claim,{}).get(sid)
    if reply:rows.append(reply)
   elif parts[1]=='press':rows=st['press']
   elif parts[1]=='soft':rows=[st['soft'][parts[4]]]
   else:rows=st.get('broken_by',{}).get(parts[4],st['broken'])
   self.assertEqual(tuple(rows[index][:2]),(person,text),identity)

 def test_nabi_authored_anger_is_not_replaced_by_witness_hesitation(self):
  self.s.r13_meeting_claim='C3'
  for row in (self.e['R13_DEBATE']['C3']['statements'][0]['wrong'],self.e['R13_DEBATE']['C3']['conclusion']['weak']):
   result=self.e['r13_meeting_direct_line']('debate:conclusion_wrong:C3:weak',0,row,'angry','angry')
   self.assertEqual(result,('angry','angry'))
   self.assertEqual(self.s.r13_meeting_art_slots,{})

class WorldCamera(unittest.TestCase):
 def setUp(self):
  self.s=types.SimpleNamespace(r13_meeting_previous_focus='a',r13_meeting_shot_revision=1,r13_meeting_pan_painted_revision=-1,r13_meeting_pan_started=0.0)
  self.clock=[10.0];self.motion=types.SimpleNamespace(room13_motion=True)
  self.e=dict(store=self.s,persistent=self.motion,r13_debate_session=lambda c:'trial',
   r13_meeting_cast=lambda c,s:[('a',0),('b',0),('c',0)],r13_meeting_direct_duration=lambda:.22,
   renpy=types.SimpleNamespace(file=lambda path:__import__("io").StringIO((ROOT/"game"/path).read_text()),Displayable=object,is_skipping=lambda:False,display=types.SimpleNamespace(core=types.SimpleNamespace(get_time=lambda:self.clock[0]))))
  src=(ROOT/'game/room13_meeting_camera.rpy').read_text().split('init 175 python:\n',1)[1]
  exec(textwrap.dedent(src),self.e)
 def test_camera_projects_fixed_seats_together_instead_of_replacing_speaker_cards(self):
  slot=self.e['r13_meeting_world_slot']
  self.assertEqual(slot(0,0,9)[:2],(640,1.0))
  self.assertAlmostEqual(slot(1,0,9)[1],.82)
  # Turning right sends both fixed people left; no independent entrance/exit motion.
  self.assertLess(slot(0,.5,9)[0],slot(0,0,9)[0])
  self.assertLess(slot(1,.5,9)[0],slot(1,0,9)[0])
  self.assertEqual(slot(0,9,9),slot(0,0,9))
 def test_camera_interpolates_one_view_and_reduced_motion_snaps_to_same_destination(self):
  view=self.e['r13_meeting_world_view']
  self.assertEqual(view('C2','b'),(0.0,True))
  self.clock[0]+=.11;self.assertAlmostEqual(view('C2','b')[0],.5)
  self.clock[0]+=.13;self.assertEqual(view('C2','b'),(1.0,False))
  self.motion.room13_motion=False;self.assertEqual(view('C2','b'),(1.0,False))

 def test_phase_uses_token_and_completion_not_wall_clock(self):
  phase=self.e['r13_meeting_reaction_phase']
  r=dict(token='a',phase='pending')
  self.assertEqual(phase(r,'a',False,0),'playing')
  r['phase']='playing'
  self.assertEqual(phase(r,'a',True,.34),'playing')
  self.assertEqual(phase(r,'a',True,.35),'settled')
  self.assertEqual(phase(r,'a',False,0),'settled')
  self.assertEqual(phase(r,'b',True,0),'settled')
  self.assertEqual(phase(r,'a',True,0,True),'settled')
  r['phase']='settled'
  self.assertEqual(phase(r,'a',False,0),'settled')

 def test_renderer_settles_on_reconstruction_skip_rollback_and_motion_off(self):
  self.e['renpy'].predicting=lambda:False
  self.e['renpy'].in_rollback=lambda:False
  self.e['renpy'].redraw=lambda *args:None
  self.e['renpy'].render=lambda art,*args:art
  def settle():self.s.r13_meeting_reaction=dict(self.s.r13_meeting_reaction,phase='settled')
  self.e['r13_meeting_reaction_settle']=settle
  cls=self.e['R13MeetingReaction']
  self.s.r13_meeting_reaction=dict(token='a',phase='pending')
  first=cls('a','react','talk')
  self.assertEqual(first.render(1,1,10,0),'react')
  self.assertEqual(first.render(1,1,10.34,0),'react')
  self.assertEqual(first.render(1,1,10.36,0),'talk')
  self.assertEqual(cls('a','react','talk').render(1,1,0,0),'talk')
  self.s.r13_meeting_reaction=dict(token='a',phase='pending')
  first=cls('a','react','talk');first.render(1,1,0,0)
  self.assertEqual(cls('a','react','talk').render(1,1,0,0),'talk')
  for mode in ('skip','rollback','motion_off'):
   self.s.r13_meeting_reaction=dict(token='a',phase='pending')
   self.e['renpy'].is_skipping=lambda:mode=='skip'
   self.e['renpy'].in_rollback=lambda:mode=='rollback'
   self.motion.room13_motion=mode!='motion_off'
   self.assertEqual(cls('a','react','talk').render(1,1,0,0),'talk')
   self.assertEqual(self.s.r13_meeting_reaction['phase'],'settled')

class AuthoredMeetingInventory(unittest.TestCase):
 def test_all_authored_meetings_have_source_frames_and_no_fixed_ten_person_cast(self):
  from meeting_direction_audit import inventory
  meetings=inventory()['meetings']
  self.assertEqual(len(meetings),15)
  self.assertEqual({m['venue'][1] for m in meetings},{'round','stone','field','room'})
  self.assertGreater(len({len(m['people']) for m in meetings}),1)
  for meeting in meetings:
   for person in meeting['people']:
    self.assertTrue(person['approved'],person['person'])
    self.assertEqual(person['missing_files'],[])
    self.assertTrue({'neutral','angry','anxious','surprise_talk','surprise_react'}<=set(person['frames']))

 def test_six_source_variants_are_original_bytes_and_fit_shared_canvas(self):
  import hashlib,json
  registry=json.loads((ROOT/'game/assets/room13-meeting-source-art.json').read_text())
  profiles=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']
  self.assertEqual(sum(map(len,registry.values())),6)
  for person,slots in registry.items():
   for spec in slots.values():
    self.assertEqual(hashlib.sha256((ROOT/'game'/spec['file']).read_bytes()).hexdigest(),spec['sha256'])
    self.assertEqual(spec['canvas'],profiles[person]['profiles']['840']['canvas'])
