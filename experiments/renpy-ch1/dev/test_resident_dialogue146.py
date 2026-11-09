"""주민 질문의 개별성·실제 재실·상황별 기억과 피코 전달의 연결을 검사한다."""
import copy
import json
from pathlib import Path
import textwrap
import unittest
from test_resident_chat145 import environment, ROOT

CATALOGUE=json.loads((ROOT/'game/v111/resident-dialogue.json').read_text())['people']


def make(person='nabi',day=2):
    env,state,calls=environment(person,day)
    env['R13_V111_RESIDENT_DIALOGUE']=copy.deepcopy(CATALOGUE)
    return env,state,calls


class ResidentDialogue146(unittest.TestCase):
    def test_every_original_and_added_resident_has_two_distinct_daily_choices(self):
        registered=set(json.loads((ROOT/'game/room13-content.json').read_text())['residents'])
        self.assertTrue(registered<=set(CATALOGUE))
        self.assertEqual(len(CATALOGUE),55)
        for person in CATALOGUE:
            for day in (1,4,5,7):
                with self.subTest(person=person,day=day):
                    env,state,_=make(person,day);before=copy.deepcopy(state.room13)
                    rows=env['r13_v111_resident_topics'](person)
                    self.assertGreaterEqual(len(rows),2)
                    self.assertEqual(len({r['title'] for r in rows}),len(rows))
                    self.assertTrue(all(r['lines'] or r['key']=='hyeoni:song' for r in rows))
                    self.assertEqual(state.room13,before)

    def test_each_child_has_distinct_personal_answers(self):
        children=[p for p in CATALOGUE if p.startswith('kid_')]
        for index in (0,1,2):
            answers=[tuple(tuple(packet) for packet in CATALOGUE[p]['topics'][index]['lines']) for p in children]
            self.assertEqual(len(set(answers)),len(children))

    def test_main_question_and_ordinary_talk_coexist(self):
        env,state,_=make('nabi')
        env['r13_v111_binding']=lambda:dict(options=[dict(person='nabi',location='square')])
        env['_r13_resident_questions']=lambda p:[('정식 질문',env['Return'](7),False)]
        rows=env['r13_v111_questions']('nabi')
        self.assertEqual(rows[0][1].value,7)
        self.assertGreaterEqual(len(rows),3)

    def test_execution_rechecks_death_departure_presence_and_date(self):
        for case in ('death','departed','remote','invisible','day8','notready'):
            env,state,_=make('nabi');key=env['r13_v111_resident_topics']('nabi')[0]['key']
            if case=='death':env['r13_v111_person_alive']=lambda p:False
            if case=='departed':state.room13['v111']['values']['departed:nabi']=True
            if case=='remote':state.room13['v111']['values']['location:nabi']='post'
            if case=='invisible':env['r13_visible_people']=lambda:[]
            if case=='day8':state.room13['day']=8
            if case=='notready':env['r13_v111_actor_ready']=lambda p:False
            self.assertIsNone(env['r13_v111_resident_chat_spec'](key))
            self.assertEqual(env['r13_v111_resident_chat_lines'](key),[])

    def test_busy_current_caretaker_can_answer_without_leaving_child(self):
        env,state,_=make('nabi');v=state.room13['v111']['values']
        v.update({'busy:nabi':'daram_guard','location:nabi':'square'})
        env['r13_v111_actor_ready']=lambda p:False
        rows=env['r13_v111_resident_topics']('nabi')
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['context'],'busy')
        self.assertIn('아이 곁',rows[0]['lines'][-1][1])
        v['location:nabi']='school'
        self.assertEqual(env['r13_v111_resident_topics']('nabi'),[])

    def test_tense_context_replaces_jokes_and_song_but_fire_main_is_immediate(self):
        env,state,_=make('resident_hyeoni',3);env['r13_v111_tense_context']=lambda:'piko'
        rows=env['r13_v111_resident_topics']('resident_hyeoni')
        self.assertEqual(len(rows),1);self.assertEqual(rows[0]['context'],'piko')
        self.assertNotIn('hyeoni:song',[r['key'] for r in rows])
        packets=env['r13_v111_resident_chat_lines'](rows[0]['key'])
        self.assertTrue(all(packet[2]['expression']=='anxious' for packet in packets))
        state.room13['location']='v111_fire'
        env['r13_v111_binding']=lambda:dict(options=[dict(person='resident_hyeoni',location='v111_fire')])
        self.assertEqual(env['r13_v111_resident_topics']('resident_hyeoni'),[])

    def test_companion_daram_only_when_actually_with_dad(self):
        env,state,_=make('daram');env['r13_visible_people']=lambda:[]
        env['r13_v111_actor_ready']=lambda p:False;env['r13_v111_roam_companions']=lambda:['daram']
        self.assertEqual(len(env['r13_v111_resident_topics']('daram')),2)
        for key,value in (('DARAM_DETAINED',True),('location:daram','school'),('busy:nabi','daram_guard'),('busy:mom','daram_guard')):
            state.room13['v111']['values'].clear();state.room13['v111']['values'][key]=value
            self.assertEqual(env['r13_v111_resident_topics']('daram'),[],key)

    def test_known_death_requires_per_resident_report_and_evidence(self):
        for case in ('unheard','alive','no_evidence','other_person','confirmed'):
            person='resident_hyeoni' if case=='other_person' else 'nabi'
            env,state,_=make(person,3);v=state.room13['v111']['values']
            v.update({'piko_alive':case=='alive','piko_news3:'+person:case!='unheard'})
            if case!='no_evidence':state.room13['evidence']=['V111:E09']
            rows=env['r13_v111_resident_topics'](person)
            self.assertEqual(any(r.get('context')=='piko_after' for r in rows),case=='confirmed')
        env,state,_=make('nabi',4);v=state.room13['v111']['values']
        v.update({'piko_alive':False,'piko_news3:nabi':True});state.room13['evidence']=['V111:E09']
        rows=env['r13_v111_resident_topics']('nabi')
        self.assertEqual([r['context'] for r in rows],['piko_after','ordinary'])

    def test_fire_prevention_alone_does_not_claim_a_fire_or_four_rescues(self):
        for variant in ('prevention','safe','lost'):
            env,state,_=make('nabi',6);v=state.room13['v111']['values']
            v.update(FIRE_EVACUATED=True,warehouse_children_school_handover=4,KKOMI_ALIVE=True)
            if variant=='safe':v['D06_S03P_empty_fire_completed']=True
            if variant=='lost':v.update(D06_S03_main_completed=True,warehouse_children_rescued=3,KKOMI_ALIVE=False)
            rows=env['r13_v111_resident_topics']('nabi')
            if variant=='prevention':self.assertTrue(all(r['context']=='ordinary' for r in rows))
            else:
                self.assertEqual(len(rows),1)
                self.assertEqual(rows[0]['context'],'fire_'+variant)
                self.assertIn('네 명' if variant=='safe' else '세 아이',rows[0]['lines'][-1][1])

    def test_day7_can_remember_both_the_fire_and_actually_heard_piko_news(self):
        env,state,_=make('nabi',7)
        state.room13['evidence']=['V111:E09']
        state.room13['v111']['values'].update(piko_alive=False,KKOMI_ALIVE=True,
            D06_S03P_empty_fire_completed=True,warehouse_children_school_handover=4,
            **{'piko_news3:nabi':True})
        before=copy.deepcopy(state.room13)
        rows=env['r13_v111_resident_topics']('nabi')
        self.assertEqual([r['context'] for r in rows],['fire_safe','piko_after','ordinary'])
        self.assertEqual(state.room13,before)

    def test_pure_packets_read_only_commit_and_roundtrip(self):
        env,state,_=make('buri');before=copy.deepcopy(state.room13)
        key=env['r13_v111_resident_topics']('buri')[0]['key']
        packets=env['r13_v111_resident_chat_lines'](key);packets[0][1]='변조'
        self.assertNotEqual(env['r13_v111_resident_chat_lines'](key)[0][1],'변조')
        self.assertEqual(state.room13,before)
        env['r13_v111_resident_chat_read'](key)
        self.assertEqual(set(state.room13['v111']['values']),{'resident_chat_read:'+key})
        self.assertEqual(state.room13,json.loads(json.dumps(state.room13)))

    def test_hyeoni_song_uses_only_completed_quest_hook(self):
        env,state,_=make('resident_hyeoni')
        env['r13_sidequest_song_lines']=lambda:['완료된 부탁의 가사']
        self.assertEqual(env['r13_hyeoni_verses'](),[env['R13_V111_RESIDENT_WINTER_VERSE'],'완료된 부탁의 가사'])
        env['r13_v111_active']=lambda:False
        self.assertEqual(env['r13_hyeoni_verses'](),['old story-dependent verse'])

    def test_late_piko_news_and_echo_survive_optional_business(self):
        env,state,_=make('nabi',4);v=state.room13['v111']['values'];v['piko_alive']=False
        state.room13['evidence']=['V111:E09']
        env.update(r13_v111_owned=lambda e:'V111:'+e in state.room13['evidence'],
                   r13_nw_added_line=lambda r:r,r13_v111_idle_lines=lambda p:[])
        source=(ROOT/'game/room13_piko_reactions.rpy').read_text().split('init 354 python:\n',1)[1].split('\nlabel ',1)[0]
        exec(textwrap.dedent(source),env)
        self.assertTrue(env['r13_v111_has_business']('nabi'))
        self.assertTrue(env['r13_piko_report_due']('nabi'))
        v['piko_news3:nabi']=True
        self.assertTrue(env['r13_piko_echo_lines']('nabi'))
        env['_r13_resident_business']=lambda p:True
        self.assertTrue(env['r13_piko_echo_lines']('nabi'),'선택 자료·재독 업무만으로 잔향을 막지 않는다')
        env['r13_v111_binding']=lambda:dict(people=['nabi'],options=[dict(person='nabi',location=state.room13['location'])])
        self.assertEqual(env['r13_piko_echo_lines']('nabi'),[])
        v.pop('piko_news3:nabi')
        self.assertFalse(env['r13_piko_report_due']('nabi'),'현재 필수 질문은 소식 전달보다 먼저다')


if __name__=='__main__':unittest.main()
