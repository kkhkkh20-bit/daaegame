"""1부 일상 인원 분산과 사건·의뢰 인물 보존을 검사한다."""
import ast
import copy
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_population146.rpy'


def environment(place='square',day=2,period=0):
    state=SimpleNamespace(room13=dict(day=day,period=period,location=place,case_state='pending',v111=dict(gate='chorong_documents2',people=[],values={})))
    values=state.room13['v111']['values'];binding=dict(location='square',people=['daram','resident_lamplighter'],options=[])
    original_where={person:'square' for person in ('doto','resident_owlgp','resident_ppul','resident_badook','resident_seol','resident_hyeoni','resident_yeoni','resident_tori','resident_ttadak')}
    original_where.update(guard='gate',karo='gate',buri='workshop')
    people=list(original_where)
    env=dict(store=state,r13_v111_active=lambda:True,r13_v111_value=values.get,
             r13_v111_person_alive=lambda p:values.get('alive:'+p) is not False,
             r13_v111_binding=lambda:binding,r13_v111_tense_context=lambda:None,
             r13_where=lambda p:original_where.get(p),r13_visible_people=lambda:people)
    # 실제 init311 재실 함수를 먼저 읽어 구 저장의 authored 위치 계약을 재현한다.
    old=(ROOT/'game/room13_v111_later_bindings.rpy').read_text().split('init 311 python:\n',1)[1].split('\ninit ',1)[0]
    tree=ast.parse(textwrap.dedent(old))
    actor=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_v111_actor_ready')
    exec(compile(ast.Module(body=[actor],type_ignores=[]),'기존 실제 재실','exec'),env)
    block=SOURCE.read_text().split('init 374 python:\n',1)[1]
    exec(textwrap.dedent(block),env)
    return env,state,binding,people


class Population146(unittest.TestCase):
    def test_actual_role_routines_disperse_the_square_without_mutating_state(self):
        env,s,b,_=environment();before=copy.deepcopy(s.room13)
        expected={'doto':'post','resident_owlgp':'post','resident_ppul':'gate','resident_badook':'gate',
                  'resident_yeoni':'inn','resident_tori':'inn','resident_seol':'square','resident_hyeoni':'square'}
        self.assertEqual({p:env['r13_where'](p) for p in expected},expected)
        self.assertEqual(s.room13,before)
        s.room13['period']=1
        self.assertEqual(env['r13_where']('doto'),'hall')
        self.assertEqual(env['r13_where']('resident_yeoni'),'inn')
        s.room13['period']=2
        self.assertEqual(env['r13_where']('resident_yeoni'),'dining')

    def test_first_day_and_piko_death_morning_do_not_introduce_the_musician(self):
        env,s,_,_=environment(day=1)
        self.assertEqual(env['r13_where']('resident_hyeoni'),'square')
        s.room13['day']=3
        self.assertIsNone(env['r13_where']('resident_hyeoni'))

    def test_story_options_cast_approach_and_explicit_current_cast_keep_original_routine(self):
        for mode in ('option','cast','by_location','approach','busy','dead','departed'):
            with self.subTest(mode=mode):
                env,s,b,_=environment();p='doto'
                if mode=='option':b['options']=[dict(person=p,location='square')]
                if mode=='cast':b['people'].append(p)
                if mode=='by_location':b['people_by_location']={'square':[p]}
                if mode=='approach':b['approach']={p:dict(object='ledger')}
                if mode=='physical_cast':s.room13['v111'].update(people=[p]);s.room13['v111']['values']['location:'+p]='square'
                if mode=='busy':s.room13['v111']['values']['busy:'+p]='medical_call'
                if mode=='dead':s.room13['v111']['values']['alive:'+p]=False
                if mode=='departed':s.room13['v111']['values']['departed:'+p]=True
                self.assertEqual(env['r13_where'](p),'square')

    def test_past_optional_speakers_do_not_pin_the_nine_daily_roles_to_a_crowded_square(self):
        env,s,b,_=environment();b.update(people=[],options=[])
        s.room13['v111']['people']=list(env['R13_POPULATION146_ROUTINES'])
        s.room13['v111']['values'].update({'location:'+p:'square' for p in env['R13_POPULATION146_ROUTINES']})
        self.assertEqual(env['r13_where']('doto'),'post')
        self.assertEqual(env['r13_where']('resident_owlgp'),'post')
        self.assertEqual(env['r13_where']('resident_yeoni'),'inn')
        self.assertLessEqual(len(env['r13_visible_people']()),5)
        s.room13['v111']['values']['busy:doto']='archive_work'
        self.assertEqual(env['r13_where']('doto'),'square')
        self.assertIn('square',env['r13_population146_needed_places']('doto'))
        s.room13['v111']['people'].append('resident_piko')
        s.room13['v111']['values']['location:resident_piko']='square'
        self.assertIn('square',env['r13_population146_needed_places']('resident_piko'))

    def test_stale_square_cast_uses_the_actual_new_post_schedule_for_readiness(self):
        env,s,b,_=environment(place='post');b.update(people=[],options=[])
        s.room13['v111']['people']=['doto','resident_owlgp']
        s.room13['v111']['values'].update({'location:doto':'square','location:resident_owlgp':'square'})
        before=copy.deepcopy(s.room13)
        self.assertFalse(env['_r13_population146_actor_ready']('doto'))
        self.assertFalse(env['_r13_population146_actor_ready']('resident_owlgp'))
        self.assertEqual(env['r13_where']('doto'),'post')
        self.assertTrue(env['r13_v111_actor_ready']('doto'))
        self.assertTrue(env['r13_v111_actor_ready']('resident_owlgp'))
        self.assertEqual(s.room13,before)
        s.room13['location']='square'
        self.assertFalse(env['r13_v111_actor_ready']('doto'),'지난 자리에 남은 질문을 실행하지 않는다')
        self.assertFalse(env['r13_v111_actor_ready']('resident_owlgp'))

    def test_readiness_override_does_not_boost_main_actors_death_absence_busy_or_crisis(self):
        for reason in ('main','dead','departed','busy','tense','travel','late','custody','other_actor'):
            with self.subTest(reason=reason):
                env,s,b,_=environment(place='post');b.update(people=[],options=[])
                p='doto';s.room13['v111']['people']=[p];values=s.room13['v111']['values'];values['location:'+p]='square'
                if reason=='main':b['options']=[dict(person=p,location='post')]
                if reason=='dead':values['alive:'+p]=False
                if reason=='departed':values['departed:'+p]=True
                if reason=='busy':values['busy:'+p]='medical_call'
                if reason=='tense':env['r13_v111_tense_context']=lambda:'piko'
                if reason=='travel':s.room13['v111']['gate']='travel'
                if reason=='late':s.room13['day']=8
                if reason=='custody':values['DARAM_DETAINED']=True
                if reason=='other_actor':p='resident_piko';s.room13['v111']['people']=[p];values['location:'+p]='square'
                before=copy.deepcopy(s.room13)
                self.assertEqual(env['r13_v111_actor_ready'](p),env['_r13_population146_actor_ready'](p))
                self.assertFalse(env['r13_v111_actor_ready'](p))
                self.assertEqual(s.room13,before)

    def test_inactive_late_travel_crisis_meeting_and_custody_keep_the_existing_population(self):
        for mode in ('inactive','late','travel','tense','occurred','detained','meeting'):
            with self.subTest(mode=mode):
                env,s,_,people=environment()
                if mode=='inactive':env['r13_v111_active']=lambda:False
                if mode=='late':s.room13['day']=8
                if mode=='travel':s.room13['v111']['gate']='travel'
                if mode=='tense':env['r13_v111_tense_context']=lambda:'piko'
                if mode=='occurred':s.room13['case_state']='occurred'
                if mode=='detained':s.room13['v111']['values']['DARAM_DETAINED']=True
                if mode=='meeting':s.r13_meeting_active=True
                self.assertEqual(env['r13_visible_people'](),people)
                self.assertEqual(env['r13_where']('doto'),'square')

    def test_required_and_accepted_sidequest_people_survive_the_five_person_budget(self):
        env,_,_,_=environment();select=env['r13_population146_select']
        people=['a','b','c','d','e','f','g']
        out=select(people,'square',{'f','g'},{'e'})
        self.assertLessEqual(len(out),5)
        self.assertTrue({'e','f','g'}<=set(out))
        self.assertEqual([p for p in people if p in out],out)
        self.assertEqual(select(people,'square',set(people)),people)
        self.assertEqual(select(['a','a','b'],'square',set()),['a','b'])

    def test_the_local_host_is_not_lost_when_another_role_has_the_same_priority_entry(self):
        env,_,_,_=environment();select=env['r13_population146_select']
        guests=list(env['R13_POPULATION146_PRIORITY'])
        out=select(guests,'workshop',set())
        self.assertIn('buri',out)
        self.assertLessEqual(len(out),5)

    def test_quiet_extras_are_only_retired_from_idle_staging(self):
        env,_,_,_=environment();select=env['r13_population146_select'];p='resident_sling'
        self.assertEqual(select([p],'post',set()),[])
        self.assertEqual(select([p],'post',{p}),[p])
        self.assertEqual(select([p],'post',set(),{p}),[p])

    def test_sidequest_priority_does_not_query_visibility_or_move_its_owner(self):
        env,s,_,_=environment();env['r13_sidequest_priority_people']=lambda:['resident_yeoni','buri']
        before=copy.deepcopy(s.room13)
        self.assertEqual(env['r13_population146_side_people'](),{'resident_yeoni','buri'})
        self.assertEqual(s.room13,before)
        self.assertEqual(env['r13_where']('resident_yeoni'),'inn')

    def test_roster_budget_applies_only_to_public_places_and_never_duplicates_people(self):
        env,s,b,people=environment();b.update(people=[],options=[])
        before=copy.deepcopy(s.room13);out=env['r13_visible_people']()
        self.assertLessEqual(len(out),5);self.assertEqual(len(out),len(set(out)))
        self.assertEqual(s.room13,before)
        s.room13['location']='hidden_base14'
        self.assertEqual(env['r13_visible_people'](),people)


if __name__=='__main__':unittest.main()
