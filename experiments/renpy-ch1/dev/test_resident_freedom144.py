"""주민 질문 재독과 기존 협업 장면의 현재 시점 연결을 검사한다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from test_life_groups import environment as life_environment
from test_play_review_field import load_function
from test_newworld_text import SPEAKERS

ROOT=Path(__file__).resolve().parents[1]


def reaction_environment():
    state=SimpleNamespace(room13=dict(day=6,location='inn',evidence=['V111:E06_CONTACT','V111:E06_FIRE'],
                                    v111=dict(gate='sleep6_input',values={})))
    values=state.room13['v111']['values']
    env=dict(store=state,MS14_SPEAKERS=SPEAKERS,
             R13_REACTIONS=json.loads((ROOT/'game/v111/newworld/reactions.json').read_text()),
             r13_v111_value=lambda key:values.get(key),
             r13_v111_set=lambda key,value:values.__setitem__(key,value),
             r13_v111_owned=lambda key:'V111:'+key in state.room13['evidence'],
             r13_v111_person_alive=lambda person:True,r13_v111_actor_ready=lambda person:True,
             r13_v111_binding=lambda:dict(options=[]),r13_reaction_seen=lambda spec:True,
             r13_nw_added_line=lambda row:dict(row),
             _r13_reaction_questions=lambda person:[],Return=lambda value:SimpleNamespace(value=value),
             R13_IDLE_FAMILY=('dad','mom','daram'),r13_v111_active=lambda:True)
    for name in ('r13_reaction_day_ok','r13_reaction_packets','r13_followup_read','r13_v111_followups',
                 'r13_v111_followup_display','r13_v111_questions','r13_v111_followup_lines'):
        load_function('game/room13_v111_reactions.rpy',name,env)
    for name in ('r13_v111_has_business','r13_v111_idle_ok'):
        load_function('game/room13_v111_idle.rpy',name,env)
    return env,state


class ResidentFreedom144(unittest.TestCase):
    def test_two_current_questions_remain_selectable_after_both_are_read(self):
        env,state=reaction_environment();questions=env['r13_v111_questions']('nabi')
        self.assertEqual(len(questions),2)
        self.assertEqual([q[1].value[1] for q in questions],['NW_RX_F016','NW_RX_F017'])
        self.assertFalse(env['r13_v111_idle_ok']('nabi'))
        before=copy.deepcopy(state.room13)
        for q in questions:self.assertTrue(env['r13_v111_followup_lines'](q[1].value[1]))
        read=env['r13_v111_questions']('nabi')
        self.assertEqual([q[0] for q in read],['가져간 사람도 적어 두나요?','등잔은 어디에 두셨습니까?'])
        self.assertTrue(all(q[2] for q in read))
        self.assertFalse(env['r13_v111_idle_ok']('nabi'),'읽은 질문이 있어도 질문 목록을 열어야 한다')
        self.assertEqual(state.room13['evidence'],before['evidence'])
        self.assertEqual(state.room13['day'],6)
        self.assertEqual(set(state.room13['v111']['values']),{'followup_read:NW_RX_F016','followup_read:NW_RX_F017'})
        after=copy.deepcopy(state.room13)
        for q in read:self.assertTrue(env['r13_v111_followup_lines'](q[1].value[1]))
        self.assertEqual(state.room13,after)

    def test_old_read_flags_do_not_hide_the_current_question_sheet(self):
        env,state=reaction_environment()
        values=state.room13['v111']['values']
        values.update({'followup_heard:NW_RX_F016':True,'followup_read:NW_RX_F017':True})
        self.assertTrue(all(q[2] for q in env['r13_v111_questions']('nabi')))
        self.assertTrue(env['r13_v111_has_business']('nabi'))
        self.assertFalse(env['r13_v111_idle_ok']('nabi'))

    def test_stale_followup_never_marks_read_when_its_prerequisite_disappears(self):
        for negative in ('evidence','day','dead','absent','departed'):
            with self.subTest(negative=negative):
                env,state=reaction_environment()
                if negative=='evidence':state.room13['evidence'].clear()
                if negative=='day':state.room13['day']=5
                if negative=='dead':env['r13_v111_person_alive']=lambda p:False
                if negative=='absent':env['r13_v111_actor_ready']=lambda p:False
                if negative=='departed':state.room13['v111']['values']['departed:nabi']=True
                before=copy.deepcopy(state.room13)
                self.assertEqual(env['r13_v111_questions']('nabi'),[])
                self.assertEqual(env['r13_v111_followup_lines']('NW_RX_F016'),[])
                self.assertEqual(state.room13,before)

    def life(self,key):
        env,row,actors=life_environment(key)
        env['store'].room13['v111']=dict(gate='free_day7',values={})
        env.update(r13_v111_active=lambda:True,r13_v111_binding=lambda:dict(options=[]),
                   r13_v111_person_alive=lambda person:True,
                   r13_v111_actor_ready=lambda person:True,
                   r13_v111_value=lambda key:env['store'].room13['v111']['values'].get(key),
                   r13_v111_tense_context=lambda:None)
        return env,row,actors

    def test_two_existing_cooperative_scenes_are_read_only_and_do_not_summon_anyone(self):
        for key in ('workshop_pair','inn_mending'):
            env,row,actors=self.life(key);before=copy.deepcopy(env['store'].room13)
            self.assertTrue(env['r13_life_groups_here']())
            self.assertEqual(env['r13_life_group_lines'](key),row['lines'])
            self.assertEqual(env['r13_life_group_lines'](key),row['lines'])
            self.assertEqual(env['store'].room13,before)
            actors.pop()
            self.assertEqual(env['r13_life_group_lines'](key),[],'자리에서 사라진 사람을 생활대화로 부르지 않는다')

    def test_crisis_story_role_and_unavailable_members_block_ordinary_work_chatter(self):
        for reason in ('travel','crisis','story_question','dead','departed','busy','absent','late'):
            with self.subTest(reason=reason):
                env,row,_=self.life('workshop_pair');s=env['store'].room13
                if reason=='travel':s['v111']['gate']='travel'
                if reason=='crisis':env['r13_v111_tense_context']=lambda:'piko'
                if reason=='story_question':env['r13_v111_binding']=lambda:dict(options=[dict(person='resident_tok',location='workshop')])
                if reason=='dead':env['r13_v111_person_alive']=lambda p:False
                if reason=='departed':s['v111']['values']['departed:resident_tok']=True
                if reason=='busy':s['v111']['values']['busy:resident_tok']='detained'
                if reason=='absent':env['r13_v111_actor_ready']=lambda p:False
                if reason=='late':s['day']=8
                before=copy.deepcopy(s)
                self.assertEqual(env['r13_life_groups_here'](),[])
                self.assertEqual(env['r13_life_group_lines']('workshop_pair'),[])
                self.assertEqual(s,before)

    def test_late_legacy_child_scene_is_not_enabled_in_the_first_part(self):
        env,_,_=self.life('school_play')
        self.assertEqual(env['r13_life_groups_here'](),[])


if __name__=='__main__':unittest.main()
