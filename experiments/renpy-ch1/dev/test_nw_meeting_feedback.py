"""제출 연출은 실제 발언을 따르고 자료·기회·결과를 바꾸지 않는다."""
import copy
import textwrap
import types
import unittest
from pathlib import Path

from test_newworld_text import Layer

GAME=Path(__file__).resolve().parents[1]/'game'


class MeetingFeedback(unittest.TestCase):
    def setUp(self):
        self.world={'evidence':['V111:E02','V111:E03'],
            'arguments':{'claim':['V111:E02','V111:E03']},
            'v111':{'values':{'tries:gate':1,'meeting:gate':None}},'day':1,'period':0}
        self.store=types.SimpleNamespace(room13=self.world,r13_meeting_active=True,
            r13_meeting_claim='NW:gate',r13_meeting_line_token=None,
            r13_nw_submit_cue={'accepted':True,'remaining':2},r13_meeting_direction={},
            r13_meeting_reaction=None,r13_meeting_reaction_tokens=[],
            r13_nw_meeting_cast=['guard'],r13_nw_submission_serial=1)
        self.audio=[];self.effects=[]
        self.env={'store':self.store,'CAST':{'guard':{},'resident_siluk':{}},
            'r13_viewpoint':lambda:'dad','r13_v111_person_alive':lambda p:True,
            'r13_nw_meeting_claim':lambda c:c.startswith('NW:'),
            'r13_nw_meeting_key':lambda c:c[3:] if c and c.startswith('NW:') else None,
            'persistent':types.SimpleNamespace(room13_motion=True),
            'renpy':types.SimpleNamespace(is_skipping=lambda:False,show_screen=lambda *a,**k:self.effects.append(a)),
            'r13_meeting_direct_line':lambda i,n,p,e,s:(e,s)}
        source=(GAME/'systems/room13_meeting_direction.rpy').read_text()
        exec(textwrap.dedent(source[source.index('    R13_MEETING_BEATS ='):source.index('    def r13_meeting_startle_pose')]),self.env)
        feedback=(GAME/'systems/room13_nw_meeting_feedback.rpy').read_text()
        exec(textwrap.dedent(feedback[feedback.index('    R13_NW_FEEDBACK_MEETINGS='):feedback.index('\ndefault ')]),self.env)
        self.env['r13_nw_direct_audio']=lambda beat:self.audio.append(beat)
        self.env['r13_meeting_reaction_settle']=lambda:None
        stage=(GAME/'room13_v111_meeting_stage.rpy').read_text()
        exec(textwrap.dedent(stage[stage.index('    _r13_nw_meeting_direct_line='):stage.index('\ndefault r13_nw_pending')]),self.env)

    def line(self,index,person='dad',options=None,pose='neutral'):
        return self.env['r13_meeting_direct_line']('test:reply',index,(person,'발언 '+str(index),options or {}),'neutral',pose)

    def test_submit_emphasis_expires_without_changing_proof_or_chances(self):
        before=copy.deepcopy(self.world)
        self.line(0);self.line(1,'guard');self.line(2,'guard')
        self.assertEqual(self.audio,['explain','reaction','listen'])
        self.assertEqual(self.world,before)
        self.assertIsNone(self.store.r13_meeting_reaction,'제시 직후 일반 증언을 놀란 표정으로 바꾸지 않는다')

    def test_authored_reaction_is_once_and_final_emotion_survives(self):
        self.line(0,'guard',{'beat':'shaken'},'anxious')
        reaction=copy.deepcopy(self.store.r13_meeting_reaction)
        self.assertEqual(reaction['person'],'guard')
        self.assertEqual(reaction['pose'],'anxious')
        self.line(0,'guard',{'beat':'shaken'},'anxious')
        self.assertEqual(self.store.r13_meeting_reaction,reaction)
        self.assertEqual(len(self.store.r13_meeting_reaction_tokens),1)
        result=self.line(1,'guard',{'beat':'shaken','expression':'angry'},'angry')
        self.assertEqual(result[1],'angry')
        self.assertIsNone(self.store.r13_meeting_reaction)

    def test_wrong_reply_and_authored_interrupt_keep_their_own_beats(self):
        self.store.r13_nw_submit_cue={'accepted':False,'remaining':2}
        self.line(0,'guard');self.line(1,'dad',{'beat':'interrupt'})
        self.assertEqual(self.audio,['reversal','interrupt'])
        self.assertEqual(len(self.effects),1)

    def test_close_up_needs_explicit_lamp_line_and_clears_on_next_line(self):
        self.line(0,'guard',{'comparison':'knife_tip'})
        self.assertIsNone(self.store.r13_nw_comparison)
        self.store.r13_meeting_claim='NW:lamp'
        self.line(1,'resident_siluk',{'comparison':'knife_tip'})
        self.assertEqual(self.store.r13_nw_comparison,'knife_tip')
        self.line(2,'resident_siluk')
        self.assertIsNone(self.store.r13_nw_comparison)

    def test_later_meeting_does_not_gain_part_one_reaction(self):
        self.store.r13_meeting_claim='NW:room13'
        self.store.r13_nw_submit_cue=None
        self.line(0,'guard',{'beat':'shaken'},'anxious')
        self.assertIsNone(self.store.r13_meeting_reaction)


class KnifeComparisonRows(Layer):
    def test_close_up_is_after_player_match_and_is_not_a_new_record(self):
        env=self.load();before=copy.deepcopy(self.state.room13)
        rows=env['r13_v111_lines'](['MS14_D03_S05_L0014','MS14_D03_S05_L0016'])
        self.assertTrue(all(r[2].get('comparison')=='knife_tip' for r in rows))
        self.assertEqual(self.state.room13,before)
        self.assertTrue((GAME/'assets/room13-meeting-knife-tip-match.webp').is_file())


if __name__=='__main__':unittest.main()
