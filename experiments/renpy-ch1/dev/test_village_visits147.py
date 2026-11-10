"""방문 순서·참여 기억과 기존 수사/의뢰의 분리를 확인한다."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_village_visits147.rpy'
DATA=json.loads((ROOT/'game/v111/village-visits147.json').read_text())['events']


def environment():
    state=SimpleNamespace(room13=dict(day=2,period=0,location='post',coins=17,evidence=['V111:E01'],flags=['gate_registered'],
        case_state='pending',v111=dict(scene='MS14_D02_S01',gate='lamp_rope',values={},sidequests={})),
        calm=True,companion=True,hidden=set(),unready=set(),options=[],questions=[],
        where={'resident_owlgp':'post','seryeon':'post','resident_yeoni':'inn','resident_tori':'inn'})
    speakers={'아빠':'dad','다람':'daram','부엉이':'resident_owlgp','세련':'seryeon','여니':'resident_yeoni','토리':'resident_tori'}
    def sq_status(key):return state.room13['v111']['sidequests'].get(key,{}).get('status','unseen')
    def quest_actions(person):
        if person!='resident_yeoni':return []
        status=sq_status('seam')
        action={'unseen':'offer','accepted':'status','worked':'report','done':'done'}.get(status)
        return [dict(quest='seam',action=action)] if action else []
    env=dict(store=state,json=json,winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
        renpy=SimpleNamespace(file=lambda path:open(ROOT/'game'/path,encoding='utf-8')),
        ROOM13=json.loads((ROOT/'game/room13-content.json').read_text()),CAST={who:{} for who in speakers.values()},MS14_SPEAKERS=speakers,
        r13_sidequest_calm=lambda:state.calm and 2<=state.room13['day']<=7 and state.room13['v111']['gate']!='travel',
        r13_v111_value=lambda key:state.room13['v111']['values'].get(key),r13_sidequest_status=sq_status,
        r13_v111_actor_ready=lambda p:p not in state.unready and state.where.get(p)==state.room13['location'],
        r13_v111_person_alive=lambda p:state.room13['v111']['values'].get('alive:'+p,True) is not False,
        r13_visible_people=lambda:[p for p,place in state.where.items() if place==state.room13['location'] and p not in state.hidden],
        r13_v111_binding=lambda:dict(options=state.options),
        r13_nw_added_line=lambda row:row,r13_v111_resident_companion_ok=lambda p:state.companion,
        r13_population146_side_people=lambda:{'buri'},r13_sidequest_person_actions=quest_actions,
        r13_sidequest_lines=lambda key,phase:[dict(id='existing',speaker='여니',text='기존 의뢰 대사')],
        r13_v111_questions=lambda p:list(state.questions),r13_v111_has_business=lambda p:False,
        Return=lambda value:SimpleNamespace(value=value))
    block=SOURCE.read_text().split('init 384 python:\n',1)[1].split('\nlabel ',1)[0]
    exec(textwrap.dedent(block),env)
    return env,state


def main_state(state):
    result=copy.deepcopy(state.room13);result['v111'].pop('village_visits',None)
    return result


class VillageVisits147(unittest.TestCase):
    def at(self,state,key):state.room13['location']=DATA[key]['source_place']
    def evening(self,state,key):
        state.room13['period']=2;state.room13['location']='dining';state.where[DATA[key]['owner']]='dining'

    def test_registration_dialogue_and_all_choices_are_valid(self):
        env,state=environment()
        self.assertEqual(env['r13_visit147_problems'](),[])
        self.assertEqual(set(env['R13_VISITS147']),{'postcard','sleeve'})
        for event in DATA.values():
            for choice in event['choices']:self.assertLessEqual(len(choice['title']),24)
        self.assertEqual(state.room13['evidence'],['V111:E01'])

    def test_two_visit_orders_and_all_choices_preserve_main_story(self):
        for order in (('postcard','sleeve'),('sleeve','postcard')):
            for result in ('help','watch','decline'):
                with self.subTest(order=order,result=result):
                    env,state=environment()
                    for key in order:
                        self.at(state,key);before=main_state(state)
                        self.assertTrue(env['r13_visit147_record'](key,'noticed'))
                        self.assertTrue(env['r13_visit147_record'](key,'complete',result))
                        self.assertEqual(main_state(state),before)
                        self.assertEqual(env['r13_visit147_state'](key)['result'],result)
                        snapshot=copy.deepcopy(state.room13)
                        self.assertFalse(env['r13_visit147_record'](key,'complete','help'))
                        self.assertEqual(state.room13,snapshot)

    def test_every_result_has_separate_evening_memory_and_replay_does_not_replace_it(self):
        for key in DATA:
            for result in ('help','watch','decline'):
                with self.subTest(event=key,result=result):
                    env,state=environment();self.at(state,key)
                    env['r13_visit147_record'](key,'complete',result)
                    self.assertFalse(env['r13_visit147_memory_allowed'](key))
                    self.evening(state,key);before=main_state(state)
                    self.assertEqual(env['r13_visit147_memory_phase'](key),'memory_'+result)
                    self.assertTrue(env['r13_visit147_record'](key,'memory'))
                    self.assertEqual(main_state(state),before)
                    self.assertEqual(env['r13_visit147_state'](key)['result'],result)
                    actions=env['r13_visit147_person_actions'](DATA[key]['owner'])
                    self.assertTrue(actions[0]['read'])
                    self.assertTrue(env['r13_visit147_record'](key,'memory'))
                    self.assertEqual(env['r13_visit147_memory_phase'](key),'memory_'+result)

    def test_missed_visit_is_told_as_residents_own_work_not_players_help(self):
        for key in DATA:
            env,state=environment();self.evening(state,key);before=main_state(state)
            self.assertEqual(env['r13_visit147_memory_phase'](key),'passed')
            self.assertEqual(env['r13_visit147_person_actions'](DATA[key]['owner'])[0]['title'],DATA[key]['passed_title'])
            self.assertTrue(env['r13_visit147_record'](key,'memory'))
            memory=env['r13_visit147_state'](key)
            self.assertEqual(memory['status'],'passed');self.assertNotIn('result',memory)
            self.assertEqual(main_state(state),before)

    def test_heard_intro_without_a_choice_remembers_the_meeting_but_never_invents_help(self):
        for key in DATA:
            env,state=environment();self.at(state,key)
            self.assertTrue(env['r13_visit147_record'](key,'noticed'))
            self.evening(state,key)
            self.assertEqual(env['r13_visit147_memory_phase'](key),'noticed')
            self.assertEqual(env['r13_visit147_person_actions'](DATA[key]['owner'])[0]['title'],DATA[key]['memory_title'])
            self.assertTrue(env['r13_visit147_record'](key,'memory'))
            self.assertEqual(env['r13_visit147_memory_phase'](key),'noticed')
            self.assertNotIn('result',env['r13_visit147_state'](key))

    def test_entry_render_and_queries_never_consume_an_event(self):
        env,state=environment();before=copy.deepcopy(state.room13)
        for _ in range(3):
            self.assertTrue(env['r13_visit147_notice']())
            env['r13_visit147_pending_here']();env['r13_visit147_person_actions']('resident_owlgp')
            env['r13_v111_questions']('resident_owlgp');env['r13_population146_side_people']()
        self.assertEqual(state.room13,before)
        state.room13['period']=2;state.where['resident_owlgp']='dining';state.room13['location']='dining'
        before=copy.deepcopy(state.room13)
        env['r13_visit147_person_actions']('resident_owlgp')
        self.assertEqual(state.room13,before)

    def test_required_actor_absence_busy_death_and_main_question_pause_without_consuming(self):
        for reason in ('hidden','unready','elsewhere','busy','departed','dead','main','unsafe','travel'):
            env,state=environment();key='postcard';partner='seryeon'
            if reason=='hidden':state.hidden.add(partner)
            elif reason=='unready':state.unready.add(partner)
            elif reason=='elsewhere':state.where[partner]='inn'
            elif reason=='busy':state.room13['v111']['values']['busy:'+partner]='medical_call'
            elif reason=='departed':state.room13['v111']['values']['departed:'+partner]=True
            elif reason=='dead':state.room13['v111']['values']['alive:'+partner]=False
            elif reason=='main':state.options=[dict(person=partner,location='post',index=5)]
            elif reason=='unsafe':state.calm=False
            elif reason=='travel':state.room13['v111']['gate']='travel'
            before=copy.deepcopy(state.room13)
            self.assertFalse(env['r13_visit147_record'](key,'complete','help'),reason)
            self.assertIsNone(env['r13_visit147_notice'](),reason)
            self.assertEqual(state.room13,before)

    def test_source_only_on_second_day_and_memory_only_through_part_one(self):
        for day in (1,3,7,8):
            env,state=environment();state.room13['day']=day
            self.assertFalse(env['r13_visit147_source_allowed']('postcard'))
        env,state=environment();self.evening(state,'postcard')
        for day in (2,4,5,7):
            state.room13['day']=day;self.assertTrue(env['r13_visit147_memory_allowed']('postcard'))
        state.room13['day']=8;self.assertFalse(env['r13_visit147_memory_allowed']('postcard'))

    def test_known_loss_and_fire_day_defer_calm_memory_until_next_day(self):
        env,state=environment();self.evening(state,'postcard')
        state.room13['day']=3;state.room13['v111']['values']['piko_alive']=False
        self.assertTrue(env['r13_visit147_memory_allowed']('postcard'),'모르는 사망을 말하지 않고 평상 대화 가능')
        state.room13['evidence'].append('V111:E09');before=copy.deepcopy(state.room13)
        self.assertFalse(env['r13_visit147_memory_allowed']('postcard'))
        self.assertEqual(state.room13,before)
        state.room13['day']=4;self.assertTrue(env['r13_visit147_memory_allowed']('postcard'))
        for flag in ('D06_S03P_empty_fire_completed','D06_S03_main_completed'):
            state.room13['day']=6;state.room13['v111']['values'][flag]=True
            self.assertFalse(env['r13_visit147_memory_allowed']('postcard'))
            state.room13['day']=7;self.assertTrue(env['r13_visit147_memory_allowed']('postcard'))

    def test_sleeve_source_takes_only_unheard_quest_offer_and_never_completes_sewing(self):
        env,state=environment();self.at(state,'sleeve')
        self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[])
        self.assertTrue(env['r13_visit147_record']('sleeve','complete','help'))
        self.assertEqual(state.room13['v111']['sidequests'],{})
        self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[dict(quest='seam',action='offer')])
        self.assertEqual(env['r13_sidequest_lines']('seam','offer')[1]['text'],DATA['sleeve']['blocks']['quest_offer'][1]['text'])
        for status in ('accepted','worked','done','declined','deferred','passed'):
            env,state=environment();self.at(state,'sleeve')
            state.room13['v111']['sidequests']['seam']=dict(status=status)
            self.assertFalse(env['r13_visit147_source_allowed']('sleeve'))
            self.evening(state,'sleeve');self.assertFalse(env['r13_visit147_memory_allowed']('sleeve'))
            if status in ('accepted','worked','done'):self.assertTrue(env['r13_sidequest_person_actions']('resident_yeoni'))

    def test_companion_lines_and_reply_disappear_together_when_daram_is_not_with_dad(self):
        env,state=environment();with_child=env['r13_visit147_lines']('sleeve','help')
        self.assertTrue(any(row['speaker']=='다람' for row in with_child))
        self.assertTrue(any('장갑은 아빠' in row['text'] for row in with_child))
        state.companion=False;alone=env['r13_visit147_lines']('sleeve','help')
        self.assertFalse(any(row['speaker']=='다람' or '장갑은 아빠' in row['text'] for row in alone))
        self.assertTrue(all('companion' not in row for row in with_child+alone))

    def test_priority_does_not_call_presence_and_questions_keep_main_indices(self):
        env,state=environment()
        env['r13_visible_people']=lambda:(_ for _ in ()).throw(AssertionError('우선배치에서 표시 조회'))
        env['r13_v111_actor_ready']=lambda p:(_ for _ in ()).throw(AssertionError('우선배치에서 재실 조회'))
        self.assertEqual(set(env['r13_population146_side_people']()),{'buri','resident_owlgp','seryeon','resident_yeoni','resident_tori'})
        env,state=environment();state.questions=[('본편 질문',SimpleNamespace(value=7),False),('개인 질문',SimpleNamespace(value=('resident_chat','x')),False)]
        rows=env['r13_v111_questions']('resident_owlgp')
        self.assertEqual(rows[0][1].value,7)
        self.assertEqual(rows[1][1].value,('village_visit',('postcard','visit')))
        self.assertEqual(rows[2][1].value,('resident_chat','x'))
        state.questions=[('빈 반환',SimpleNamespace(value=()),False)]
        self.assertTrue(env['r13_v111_questions']('resident_owlgp'))

    def test_save_roundtrip_query_copies_unknown_results_and_malformed_state(self):
        env,state=environment();env['r13_visit147_record']('postcard','complete','watch')
        state.room13=json.loads(json.dumps(state.room13,ensure_ascii=False))
        row=env['r13_visit147_state']('postcard');row['result']='help'
        self.assertEqual(env['r13_visit147_state']('postcard')['result'],'watch')
        raw=copy.deepcopy(env['R13_VISITS147']);env['r13_visit147_lines']('postcard','intro')[0]['text']='변경'
        self.assertEqual(env['R13_VISITS147'],raw)
        for group in (None,[],{'postcard':'손상'}):
            env,state=environment();state.room13['v111']['village_visits']=group;before=copy.deepcopy(state.room13)
            self.assertFalse(env['r13_visit147_record']('postcard','complete','help'))
            self.assertEqual(state.room13,before)
        env,state=environment();before=copy.deepcopy(state.room13)
        self.assertFalse(env['r13_visit147_record']('postcard','complete','unknown'))
        self.assertFalse(env['r13_visit147_record']('missing','complete','help'))
        self.assertEqual(state.room13,before)


if __name__=='__main__':unittest.main()
