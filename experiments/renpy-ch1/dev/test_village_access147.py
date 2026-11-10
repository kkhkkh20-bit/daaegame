"""공공 공간을 일찍 방문해도 미래 사건과 시간 전환은 별도 조건을 지킨다."""
import copy
import textwrap
import unittest
from types import SimpleNamespace
from test_play_review_field import ROOT, load_function


def environment():
    state=SimpleNamespace(room13=dict(day=2,period=0,location='square',evidence=[],flags=[],
        case_state='pending',v111=dict(gate='lamp_rope',scene='MS14_D02_S01',values={},visited_places=[])),
        tense=None,active=True,options=[])
    env=dict(store=state,r13_v111_active=lambda:state.active,
        r13_v111_tense_context=lambda:state.tense,R13_V111_BINDINGS={},
        r13_v111_value=lambda k:state.room13['v111']['values'].get(k),
        r13_v111_owned=lambda k:'V111:'+k in state.room13['evidence'],
        r13_v111_object_key=lambda k:k,r13_v111_binding=lambda:dict(options=state.options),
        R13_V111_RECORD_OBJECTS={('clinic','notes'):'E13',('store','ledger'):'E16'},
        r13_v111_ambient_text=lambda key,spec:spec.get('text'),
        r13_observation_chat_allowed=lambda identity:True,
        r13_observation_key=lambda identity:tuple(identity.split(':')[1:3]),
        r13_v111_goal=lambda:'기존 본편',r13_visible_people=lambda:[],r13_where=lambda p:None)

    source=(ROOT/'game/systems/room13_village_access147.rpy').read_text().split('init 382 python:\n',1)[1]
    exec(textwrap.dedent(source),env)
    return env,state


class VillageAccess147(unittest.TestCase):
    def test_unvisited_public_places_open_without_faking_visits_or_story_progress(self):
        env,state=environment();env['r13_v111_revisit_allowed']=lambda:True
        env['r13_v111_known_public_visits']=lambda:['inn']
        fn=load_function('game/room13_v111.rpy','r13_v111_public_revisit_places',env)
        before=copy.deepcopy(state.room13)
        self.assertEqual(set(fn()),{'inn','hall','room13','dining','square','gate','post','workshop','clinic','school','store'})
        self.assertEqual(state.room13,before)
        state.room13['day']=1;self.assertEqual(fn(),['inn'])
        env['r13_v111_revisit_allowed']=lambda:False;self.assertEqual(fn(),[])

    def test_unowned_records_do_not_reveal_future_title_or_text(self):
        env,state=environment();fn=env['r13_v111_ambient_text']
        for place,key,record in [('clinic','notes','E13'),('store','ledger','E16')]:
            state.room13['location']=place
            before=copy.deepcopy(state.room13)
            text=fn(key,dict(text='미래 증거'))
            self.assertTrue(text);self.assertNotIn('미래',text)
            self.assertNotIn('우박',text);self.assertNotIn('백 부인',text)
            self.assertEqual(state.room13,before)
            state.options=[dict(location=place,object=key,index=6)]
            self.assertEqual(fn(key,dict(text='현재 수사 기록')),'현재 수사 기록')
            state.options=[];state.room13['evidence'].append('V111:'+record)
            self.assertEqual(fn(key,dict(text='이미 읽은 기록')),'이미 읽은 기록')

    def test_early_school_is_classroom_and_future_gate_scene_is_hidden(self):
        env,state=environment();state.room13['location']='school'
        fn=env['r13_v111_ambient_text']
        self.assertNotIn('잠자리',fn('desks',dict(text='잠자리를 나눈다')))
        self.assertFalse(env['r13_observation_chat_allowed']('object:school:desks'))
        state.room13['location']='gate'
        self.assertIsNone(fn('v111_fence',dict(text='미래 천 조각')))
        self.assertIsNone(fn('v111_bucket',dict(text='미래 발자국')))
        state.room13['day']=4
        self.assertEqual(fn('v111_fence',dict(text='현재 현장')),'현재 현장')

    def test_lunch_requires_actual_finished_morning_and_never_advances_on_query(self):
        env,state=environment();ready=env['r13_village147_lunch_ready']
        self.assertFalse(ready());state.room13['v111']['gate']='morning_finish2'
        before=copy.deepcopy(state.room13)
        self.assertTrue(ready());self.assertIn('점심',env['r13_v111_goal']())
        self.assertEqual(state.room13,before)
        for patch in ({'day':1},{'day':3},{'period':1}):
            snapshot=copy.deepcopy(state.room13);state.room13.update(patch)
            self.assertFalse(ready());state.room13=snapshot
        state.tense='event';self.assertFalse(ready())

    def test_afternoon_confirm_is_known_consequence_without_prediction_or_state_write(self):
        env,state=environment();fn=env['r13_village147_move_message']
        before=copy.deepcopy(state.room13)
        self.assertIn('해가 집니다',fn('afternoon2','forest'))
        self.assertIn('아직 마치지 않았습니다',fn('afternoon2','forest'))
        self.assertIn('저녁',fn('shelter_enter','dining'))
        self.assertIsNone(fn('afternoon2','post'))
        self.assertIsNone(fn('lamp_rope','dining'))
        self.assertNotIn('죽',fn('afternoon2','forest'))
        self.assertEqual(state.room13,before)
        state.room13['day']=3;self.assertIsNone(fn('afternoon2','forest'))

    def test_piko_emergency_blocks_public_roam_and_does_not_alter_required_options(self):
        env,state=environment();env['r13_v111_free7_ready']=lambda:False
        fn=load_function('game/room13_v111.rpy','r13_v111_revisit_allowed',env)
        self.assertTrue(fn())
        state.room13.update(day=3,location='square');state.room13['v111']['gate']='piko_clean'
        state.tense='piko';before=copy.deepcopy(state.room13)
        self.assertFalse(fn());self.assertEqual(state.room13,before)

    def test_current_story_actor_is_not_duplicated_at_scheduled_second_place(self):
        env,state=environment()
        env['_r13_village147_visible']=lambda:['resident_lamplighter','buri']
        state.options=[dict(person='resident_lamplighter',location='square')]
        state.room13['location']='workshop'
        self.assertEqual(env['r13_visible_people'](),['buri'])
        state.room13['location']='square'
        self.assertEqual(env['r13_visible_people'](),['resident_lamplighter','buri'])

    def test_nabi_is_out_for_night_delivery_but_required_story_and_next_day_are_preserved(self):
        env,state=environment();state.room13.update(period=2,location='dining')
        env['_r13_village147_visible']=lambda:['nabi','resident_owlgp']
        env['_r13_village147_where']=lambda p:'dining'
        before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_visible_people'](),['resident_owlgp'])
        self.assertIsNone(env['r13_where']('nabi'))
        self.assertEqual(state.room13,before)
        state.options=[dict(person='nabi',location='dining')]
        self.assertIn('nabi',env['r13_visible_people']())
        state.options=[];state.room13['day']=3
        self.assertIn('nabi',env['r13_visible_people']())


if __name__=='__main__':unittest.main()
