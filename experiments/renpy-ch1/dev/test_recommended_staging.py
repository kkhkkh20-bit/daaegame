import ast, copy, re, types, unittest
from pathlib import Path
from test_recommended_art import init_body, R
from recommended_meeting_staging_model import *

class FakeCharacter:
    def __init__(self, name=None, **kw): self.name, self.kw = name, kw
class FakeMusic:
    def __init__(self):
        self.channels = {c:dict(path=c+'_before', volume=.63, paused=True) for c in ('music','ambience','typing')}
        self.played=[]
    def get_playing(self, channel='music'): return self.channels[channel]['path']
    def get_pause(self, channel='music'): return self.channels[channel]['paused']
    def set_pause(self, value, channel='music'): self.channels[channel]['paused']=value
    def play(self, path, channel='music', **kw): self.channels[channel]['path']=path; self.played.append(path)
    def stop(self, channel='music', **kw): self.channels[channel]['path']=None
    def set_volume(self, value, channel='music', **kw): self.channels[channel]['volume']=value

class StagingTests(unittest.TestCase):
    def campaign(self, ep=1, **kw):
        return dict(dict(episode=ep,mother='M0',piko='dead',neoul='active',episodes={'3':{'privacy':True,'verdict':'nubi_ignition_bori_afterward'}}), **kw)
    def runtime(self):
        store=types.SimpleNamespace(r13_recommended=self.campaign(),r13_meeting_shot_revision=0,r13_meeting_focus=None)
        for line in (R/'game/systems/room13_recommended_meeting_adapter.rpy').read_text().splitlines():
            if line.startswith('default '):
                name,value=line[8:].split(' = ',1);setattr(store,name,ast.literal_eval(value))
        people=set(p for spec in R13_REC_STAGE_HEARINGS.values() for p in spec['cast'])|{'dad','mom'}
        music=FakeMusic();hidden=[];stack=['before_hearing']
        renpy=types.SimpleNamespace(get_return_stack=lambda:list(stack), pop_call=lambda:stack.pop(), set_return_stack=lambda value:stack.__setitem__(slice(None),list(value)), music=music,hide_screen=hidden.append,hide=lambda x:None,Displayable=object,get_screen=lambda x:None,jump=lambda x:setattr(store,'jumped',x))
        def focus(claim,who): store.r13_meeting_focus=who;store.r13_meeting_shot_revision+=1
        def end(): store.r13_meeting_direction={};store.r13_meeting_direction_return_audio={}
        chars={p:FakeCharacter(p) for p in people}
        store.R13_CHARS=chars;store.source_thought=FakeCharacter()
        g=dict(store=store,renpy=renpy,config=types.SimpleNamespace(after_load_callbacks=[],afm_callback=None),
            CAST={p:{} for p in people},R13_CHARS=chars,source_thought=store.source_thought,Character=FakeCharacter,
            R13_MEETING_VENUES={},R13_EP_MEETING_PLACE={},
            r13_debate_session=lambda c:'legacy:'+c,r13_meeting_cast=lambda c,s,speaker=None:[('legacy',None)],
            r13_meeting_focus_person=lambda c:'legacy-focus',r13_meeting_direct_line=lambda *a:('legacy','pose'),
            r13_speaker=lambda *a:'legacy-speaker',r13_meeting_reaction_art=lambda p,po,h,s:'legacy-art',
            r13_meeting_focus_change=focus,r13_meeting_direct_end=end,
            r13_meeting_channel_gain=lambda c:music.channels[c]['volume'],r13_sound_ambience=lambda x:None,
            R13_BGM=dict(council='approved-council',pressure='approved-pressure'),
            R13_MEETING_BEATS={k:('',.6,.2,0) for k in ('listen','recover','shaken','explain','select','settle')})
        exec(init_body(R/'game/systems/room13_recommended_meeting_adapter.rpy'),g)
        return g,store,music,hidden

    def test_all_six_have_explicit_rosters_and_steps(self):
        self.assertEqual(set(R13_REC_STAGE_HEARINGS),set(range(1,7)))
        self.assertEqual(set(R13_REC_STAGE_STEPS),set(range(1,7)))
        for ep in range(1,7):
            self.assertTrue(R13_REC_STAGE_STEPS[ep]);self.assertTrue(any(c.get('group') for c in R13_REC_STAGE_STEPS[ep].values()))
    def test_no_papa_under_any_roster(self):
        for ep in range(1,7): self.assertNotIn('dad',r13_rec_stage_roster(ep,self.campaign(ep,mother='M2',piko='safe')))
    def test_m0_never_attends(self):
        for ep in range(1,7): self.assertNotIn('mom',r13_rec_stage_roster(ep,self.campaign(ep)))
    def test_m2_not_automatic_every_hearing(self):
        for ep in range(1,6): self.assertNotIn('mom',r13_rec_stage_roster(ep,self.campaign(ep,mother='M2')))
        self.assertIn('mom',r13_rec_stage_roster(6,self.campaign(6,mother='M2')))
    def test_reunited_but_explicitly_absent_mother(self):
        self.assertNotIn('mom',r13_rec_stage_roster(6,self.campaign(6,mother='M2',meeting_present={'6':['granny','daram']})))
    def test_safe_piko_only_actual_hearing(self):
        self.assertIn('resident_piko',r13_rec_stage_roster(1,self.campaign(piko='safe')))
        self.assertNotIn('resident_piko',r13_rec_stage_roster(2,self.campaign(2,piko='safe')))
    def test_dead_piko_never_attends(self):
        for ep in range(1,7): self.assertNotIn('resident_piko',r13_rec_stage_roster(ep,self.campaign(ep)))
    def test_detained_neoul_never_attends(self):
        for ep in range(1,7): self.assertNotIn('neoul',r13_rec_stage_roster(ep,self.campaign(ep,neoul='detained')))
    def test_child_testimony_respects_actual_privacy_choice(self):
        self.assertNotIn('kid_nubi1',r13_rec_stage_roster(3,self.campaign(3,episodes={'3':{'privacy':False}})))
    def test_pressure_accumulates_from_presented_proof(self):
        s=r13_rec_stage_new(1)
        for step, expected in [('empty_heat',1),('child',2),('container',3)]:
            s=r13_rec_stage_reduce(s,step,True,self.campaign());self.assertEqual(s['pressure']['nabi'],expected)
    def test_failed_proof_recovers_not_convicts(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(1),'empty_heat',True,self.campaign())
        s=r13_rec_stage_reduce(s,'child',False,self.campaign())
        self.assertEqual(s['pressure']['nabi'],0);self.assertEqual(s['beat'],'recover');self.assertFalse(s['group'])
    def test_legitimate_teacher_defense_recovers(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(5),'e5_body',True,self.campaign(5))
        s=r13_rec_stage_reduce(s,'e5_original_target',True,self.campaign(5))
        self.assertEqual(s['pressure']['resident_teacher'],0);self.assertEqual(s['beat'],'recover')
    def test_prevention_is_not_a_guilty_shock(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(5),'e5_cabinet_kept',True,self.campaign(5))
        self.assertFalse(s['group']);self.assertEqual(s['pressure']['resident_teacher'],0)
    def test_group_reveal_uses_only_current_attendees(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(1),'child',True,self.campaign())
        self.assertGreater(len(s['group']),1);self.assertNotIn('dad',s['group']);self.assertNotIn('mom',s['group']);self.assertNotIn('resident_piko',s['group'])
    def test_shock_settles_but_nervous_talking_remains(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(1),'child',True,self.campaign())
        s=r13_rec_stage_settle_model(s)
        self.assertEqual(r13_rec_stage_pressure_pose(s['pressure']['nabi']),'anxious')
        self.assertTrue(all(r['phase']=='settled' for r in s['group'].values()));self.assertFalse(s['silence'])
    def test_repeating_proof_does_not_stack_pressure_or_replay_shock(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(1),'child',True,self.campaign());pressure=copy.deepcopy(s['pressure'])
        s=r13_rec_stage_reduce(s,'child',True,self.campaign())
        self.assertEqual(s['pressure'],pressure);self.assertFalse(s['group'])
    def test_unverified_e3_does_not_visually_convict(self):
        s=r13_rec_stage_reduce(r13_rec_stage_new(3),'e3_finish',True,self.campaign(3,episodes={'3':{'privacy':True,'verdict':'handoff_unverified'}}))
        self.assertEqual(s['beat'],'settle');self.assertEqual(s['pressure']['resident_nubi'],0);self.assertFalse(s['group'])
    def test_unknown_step_fails_closed(self):
        s=r13_rec_stage_new(1);self.assertEqual(s,r13_rec_stage_reduce(s,'C1',True,self.campaign()))
    def test_story_state_never_changes(self):
        c=self.campaign();old=copy.deepcopy(c)
        r13_rec_stage_reduce(r13_rec_stage_new(1),'child',True,c);self.assertEqual(old,c)
    def test_default_off_is_true_no_op(self):
        g,s,m,h=self.runtime();before=copy.deepcopy(m.channels)
        self.assertFalse(g['r13_rec_stage_enter'](1));self.assertFalse(s.r13_rec_staging_active);self.assertEqual(before,m.channels);self.assertEqual(h,[])
    def test_legacy_functions_remain_delegated(self):
        g,s,m,h=self.runtime()
        self.assertEqual(g['r13_meeting_cast']('C1','trial'),[('legacy',None)])
        self.assertEqual(g['r13_debate_session']('C1'),'legacy:C1')
        self.assertEqual(g['r13_meeting_focus_person']('C1'),'legacy-focus')
        self.assertEqual(g['r13_meeting_direct_line']('meeting:old',0,('x','y'),'n','n'),('legacy','pose'))
    def test_enter_clears_old_menus_without_importing_claims(self):
        g,s,m,h=self.runtime();s.r13_rec_staging_enabled=True;s.r13_meeting_active=True;s.r13_meeting_claim='C1'
        self.assertTrue(g['r13_rec_stage_enter'](1))
        self.assertFalse(s.r13_meeting_active);self.assertIsNone(s.r13_meeting_claim)
        self.assertTrue(set(g['R13_REC_STAGE_LEGACY_SCREENS'])<=set(h));self.assertEqual(g['r13_debate_session']('REC_HEARING_1'),'rec_hearing_1')
    def test_line_feedback_keeps_reveal_and_papa_off_camera(self):
        g,s,m,h=self.runtime();s.r13_rec_staging_enabled=True;g['r13_rec_stage_enter'](1)
        g['r13_meeting_direct_line']('recommended:hearing:new-defense',0,('nabi','line'),'neutral','neutral')
        g['r13_rec_stage_answer']('child',True)
        g['r13_meeting_direct_line']('recommended:hearing:answer',0,('dad','proof'),'neutral','neutral')
        self.assertTrue(s.r13_rec_stage_session['silence']);self.assertTrue(s.r13_rec_stage_session['group'])
        g['r13_speaker']('dad');self.assertNotEqual(s.r13_meeting_focus,'dad')
    def test_after_load_restores_own_camera_and_settles_one_time_shock(self):
        g,s,m,h=self.runtime();s.r13_rec_staging_enabled=True;g['r13_rec_stage_enter'](1);g['r13_rec_stage_answer']('child',True)
        state=copy.deepcopy(s.r13_recommended);s.r13_meeting_direction={};s.r13_meeting_focus=None
        g['r13_rec_stage_after_load']()
        self.assertEqual(s.r13_meeting_direction['claim'],'REC_HEARING_1');self.assertFalse(s.r13_rec_stage_session['silence'])
        self.assertTrue(all(r['phase']=='settled' for r in s.r13_rec_stage_session['group'].values()));self.assertEqual(state,s.r13_recommended)
    def test_exit_restores_audio_characters_and_no_legacy_state(self):
        g,s,m,h=self.runtime();s.r13_rec_staging_enabled=True;before=copy.deepcopy(m.channels);base=s.R13_CHARS
        g['r13_rec_stage_enter'](1);g['r13_rec_stage_answer']('child',True);g['r13_rec_stage_exit']()
        self.assertFalse(s.r13_rec_staging_active);self.assertIsNone(s.r13_rec_stage_session);self.assertIsNone(s.r13_meeting_claim)
        self.assertEqual(s.R13_CHARS,base)
        for channel in ('music','ambience'):self.assertEqual(m.channels[channel],before[channel])
        self.assertEqual(s.r13_meeting_direction,{})
    def test_interruption_and_reentry_preserve_pressure_not_old_ui(self):
        g,s,m,h=self.runtime();s.r13_rec_staging_enabled=True;g['r13_rec_stage_enter'](1);g['r13_rec_stage_answer']('child',True)
        g['renpy'].set_return_stack(['before_hearing','hearing_line','nested_inspection'])
        g['r13_rec_stage_leave']();self.assertEqual(s.jumped,'r13_recommended_hub')
        self.assertEqual(g['renpy'].get_return_stack(),['before_hearing'])
        g['r13_rec_stage_enter'](1);self.assertEqual(s.r13_rec_stage_session['pressure']['nabi'],1);self.assertFalse(s.r13_meeting_active)
    def test_native_and_source_validation_are_not_conflated(self):
        text=(R/'game/systems/room13_recommended_meeting_adapter.rpy').read_text()
        self.assertIn('default r13_rec_staging_enabled = False',text)
        self.assertIn('use r13_meeting_stage',text)
        self.assertNotIn('R13_DEBATE[',text);self.assertNotIn('r13_debate_run',text);self.assertNotIn('r13_debate_save(',text)
        self.assertIn('call screen r13_recommended_notebook',text)
        self.assertNotIn('Show("r13_book"',text);self.assertNotIn("Show('r13_book'",text)
    def test_typewriter_preserved_and_no_new_impact_sounds(self):
        text=(R/'game/systems/room13_recommended_meeting_adapter.rpy').read_text()
        self.assertIn("kind=char, screen='r13_rec_stage_say'",text);self.assertIn('Function(r13_typing_tick',text)
        self.assertNotIn('gunshot',text);self.assertNotIn('klaxon',text);self.assertNotIn('source_fx(',text)
    def test_all_actual_late_step_ids_have_cues(self):
        text=(R/'game/systems/room13_recommended_ep456.rpy').read_text()
        for step in re.findall(r"q\('(e([456])_[^']+)'",text):self.assertIn(step[0],R13_REC_STAGE_STEPS[int(step[1])])
    def test_generated_adapter_is_reproducible(self):
        from build_meeting_staging import build
        p=R/'game/systems/room13_recommended_meeting_adapter.rpy';before=p.read_bytes();build();self.assertEqual(before,p.read_bytes())

if __name__=='__main__':unittest.main()
