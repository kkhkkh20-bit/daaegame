"""선택 생활 의뢰는 별도 상태만 바꾸며 본편·시간·증거를 건드리지 않는다."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_v111_sidequests.rpy'
DATA=json.loads((ROOT/'game/v111/sidequests146.json').read_text())['quests']


def environment():
    content=json.loads((ROOT/'game/room13-content.json').read_text())
    state=SimpleNamespace(room13=dict(day=2,period=1,location='inn',coins=17,evidence=['V111:E01'],flags=['entry_corrected'],
        case_state='pending',v111=dict(gate='afternoon2',scene='MS14_D02_S04',values=dict(piko_alive=True,meeting_lamp='win'))),
        calm=True,tense=None,options=[],where={q['owner']:('square' if key=='notice' else q['work_place']) for key,q in DATA.items()})
    state.room13['v111']['values']['meeting:lamp']='win'
    env=dict(store=state,json=json,winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
        renpy=SimpleNamespace(file=lambda path:open(ROOT/'game'/path,encoding='utf-8')),
        ROOM13=content,CAST={q['owner']:{} for q in DATA.values()},R13_EVENT_OFFERS={},R13_OFFER_ACTORS={},
        MS14_SPEAKERS={'아빠':'dad',**{q['owner_name']:q['owner'] for q in DATA.values()}},
        r13_v111_active=lambda:bool(state.room13.get('v111')),
        r13_v111_value=lambda key:state.room13['v111']['values'].get(key),
        r13_v111_tense_context=lambda:state.tense,
        r13_v111_revisit_allowed=lambda:state.calm,
        r13_v111_person_alive=lambda p:state.room13['v111']['values'].get('alive:'+p,True) is not False,
        r13_where=lambda p:state.where.get(p),
        r13_v111_actor_ready=lambda p:state.where.get(p)==state.room13['location'],
        r13_visible_people=lambda:[p for p,place in state.where.items() if place==state.room13['location']],
        r13_v111_binding=lambda:dict(options=state.options),
        r13_nw_added_line=lambda row:row,
        r13_places=lambda:[state.room13['location']],r13_v111_questions=lambda p:[],
        r13_v111_has_business=lambda p:False,Return=lambda value:SimpleNamespace(value=value))
    block=SOURCE.read_text().split('init 362 python:\n',1)[1].split('\nlabel ',1)[0]
    exec(textwrap.dedent(block),env)
    return env,state


def story(state):
    result=copy.deepcopy(state.room13);result.get('v111',{}).pop('sidequests',None);return result


class Sidequests146(unittest.TestCase):
    def at_owner(self,state,key):state.room13['location']=state.where[DATA[key]['owner']]
    def at_work(self,state,key):state.room13['location']=DATA[key]['work_place']

    def test_registration_has_three_valid_quests_and_no_new_evidence(self):
        env,state=environment();self.assertEqual(set(env['R13_SIDEQUESTS']),{'seam','notice','parts'})
        self.assertEqual(env['r13_sidequest_problems'](),[])
        self.assertEqual(len(env['R13_EVENT_OFFERS']),3)
        self.assertTrue(all(row[1]==[] for row in env['R13_EVENT_OFFERS'].values()))
        self.assertEqual(state.room13['evidence'],['V111:E01'])

    def test_each_method_can_be_worked_then_reported_once_with_only_optional_state_changes(self):
        for key,spec in DATA.items():
            for choice in spec['choices']:
                with self.subTest(quest=key,result=choice['result']):
                    env,state=environment();self.at_owner(state,key);before=story(state)
                    self.assertTrue(env['r13_sidequest_update'](key,'accept'))
                    self.assertEqual(env['r13_sidequest_status'](key),'accepted');self.assertEqual(story(state),before)
                    self.assertFalse(env['r13_sidequest_update'](key,'report'))
                    self.at_work(state,key);before=story(state)
                    self.assertTrue(env['r13_sidequest_object_actions'](spec['object']))
                    self.assertTrue(env['r13_sidequest_update'](key,'work',choice['result']))
                    self.assertEqual(env['r13_sidequest_status'](key),'worked');self.assertEqual(story(state),before)
                    self.assertEqual(env['r13_sidequest_object_actions'](spec['object']),[])
                    self.at_owner(state,key);before=story(state)
                    self.assertTrue(env['r13_sidequest_update'](key,'report'))
                    self.assertEqual(env['r13_sidequest_status'](key),'done');self.assertEqual(story(state),before)
                    snapshot=copy.deepcopy(state.room13)
                    self.assertFalse(env['r13_sidequest_update'](key,'report'));self.assertFalse(env['r13_sidequest_update'](key,'accept'))
                    self.assertEqual(state.room13,snapshot)
                    self.assertEqual(env['r13_sidequest_song_lines'](),[spec['song']])

    def test_decline_and_defer_can_be_reaccepted_and_late_closure_never_counts_as_help(self):
        for action in ('decline','defer'):
            env,state=environment();before=story(state)
            self.assertTrue(env['r13_sidequest_update']('seam',action))
            self.assertEqual(story(state),before)
            self.assertTrue(any(r['action']=='offer' for r in env['r13_sidequest_person_actions']('resident_yeoni')))
            state.room13['day']=6
            rows=env['r13_sidequest_person_actions']('resident_yeoni')
            self.assertEqual([r['action'] for r in rows],['close'])
            self.assertTrue(env['r13_sidequest_update']('seam','close'))
            self.assertEqual(env['r13_sidequest_status']('seam'),'passed')
            self.assertEqual(env['r13_sidequest_song_lines'](),[])
        env,state=environment();self.assertTrue(env['r13_sidequest_update']('seam','decline'))
        self.assertTrue(env['r13_sidequest_update']('seam','accept'))

    def test_accepted_work_and_report_stay_available_after_new_offer_deadline(self):
        env,state=environment();self.assertTrue(env['r13_sidequest_update']('seam','accept'))
        state.room13['day']=7
        self.assertTrue(env['r13_sidequest_object_actions']('knitting'))
        self.assertTrue(env['r13_sidequest_update']('seam','work','room'))
        self.assertTrue(env['r13_sidequest_update']('seam','report'))
        state.room13['day']=8
        self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[])
        self.assertEqual(env['r13_sidequest_places'](),[])
        self.assertEqual(env['r13_sidequest_song_lines'](),[DATA['seam']['song']])
        env,state=environment();state.room13['day']=6
        self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[],'처음 듣지 않은 부탁의 회상은 만들지 않는다')

    def test_travel_tension_custody_meeting_and_busy_pause_without_losing_progress(self):
        for reason in ('travel','tense','detained','case','meeting','unsafe','busy','dead','departed'):
            with self.subTest(reason=reason):
                env,state=environment();env['r13_sidequest_update']('seam','accept');before=copy.deepcopy(state.room13)
                if reason=='travel':state.room13['v111']['gate']='travel'
                elif reason=='tense':state.tense='piko'
                elif reason=='detained':state.room13['v111']['values']['DARAM_DETAINED']=True
                elif reason=='case':state.room13['case_state']='occurred'
                elif reason=='meeting':state.r13_meeting_active=True
                elif reason=='unsafe':state.calm=False
                elif reason=='busy':state.room13['v111']['values']['busy:resident_yeoni']='medical_call'
                elif reason=='dead':state.room13['v111']['values']['alive:resident_yeoni']=False
                elif reason=='departed':state.room13['v111']['values']['departed:resident_yeoni']=True
                changed=copy.deepcopy(state.room13)
                self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[])
                self.assertEqual(env['r13_sidequest_object_actions']('knitting'),[])
                self.assertFalse(env['r13_sidequest_update']('seam','work','room'))
                self.assertEqual(state.room13,changed)
                self.assertEqual(env['r13_sidequest_state']('seam'),before['v111']['sidequests']['seam'])

    def test_main_object_action_and_unknown_method_have_priority_and_no_side_effect(self):
        env,state=environment();env['r13_sidequest_update']('seam','accept')
        state.options=[dict(object='knitting',location='inn',index=7)]
        before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_sidequest_object_actions']('knitting'),[])
        self.assertFalse(env['r13_sidequest_update']('seam','work','room'))
        state.options=[]
        self.assertFalse(env['r13_sidequest_update']('seam','work','unregistered'))
        self.assertEqual(state.room13,before)
        self.assertFalse(env['r13_sidequest_update']('unknown','accept'))

    def test_query_copies_and_save_roundtrip_preserve_state_and_raw_dialogue(self):
        env,state=environment();self.assertNotIn('sidequests',state.room13['v111'])
        before=copy.deepcopy(state.room13)
        env['r13_sidequest_state']('seam');env['r13_sidequest_tasks']();env['r13_sidequest_song_lines']();env['r13_sidequest_priority_people']()
        self.assertEqual(state.room13,before)
        raw=copy.deepcopy(env['R13_SIDEQUESTS'])
        lines=env['r13_sidequest_lines']('seam','offer');lines[0]['text']='바꾼 문장'
        self.assertEqual(env['R13_SIDEQUESTS'],raw)
        env['r13_sidequest_update']('seam','accept')
        state.room13=json.loads(json.dumps(state.room13,ensure_ascii=False))
        snapshot=copy.deepcopy(state.room13)
        copied=env['r13_sidequest_state']('seam');copied['status']='done'
        self.assertEqual(state.room13,snapshot)
        self.assertEqual(env['r13_sidequest_status']('seam'),'accepted')

    def test_priority_is_pure_and_destination_only_opens_after_acceptance(self):
        env,state=environment();self.at_owner(state,'notice')
        self.assertNotIn('post',env['r13_places']())
        env['r13_sidequest_update']('notice','accept');self.assertIn('post',env['r13_places']())
        before=copy.deepcopy(state.room13)
        for name in ('r13_visible_people','r13_v111_actor_ready','r13_where'):
            env[name]=lambda *a:(_ for _ in ()).throw(AssertionError('배치 우선순위의 재귀 조회'))
        self.assertEqual(env['r13_sidequest_priority_people'](),['resident_seol'])
        self.assertEqual(state.room13,before)
        state.room13['v111']['gate']='travel'
        self.assertNotIn('post',env['r13_places']())

    def test_report_requires_owner_present_and_follows_actual_public_location(self):
        env,state=environment();env['r13_sidequest_update']('seam','accept')
        env['r13_sidequest_update']('seam','work','room')
        state.where['resident_yeoni']='dining'
        before=copy.deepcopy(state.room13)
        self.assertFalse(env['r13_sidequest_update']('seam','report'))
        self.assertEqual(state.room13,before)
        self.assertEqual(env['r13_sidequest_places'](),['dining'])
        self.assertEqual(env['r13_sidequest_tasks']()[0]['place'],'dining')
        state.room13['location']='dining'
        self.assertTrue(env['r13_sidequest_update']('seam','report'))
        env,state=environment();env['r13_sidequest_update']('seam','accept');env['r13_sidequest_update']('seam','work','room')
        state.where['resident_yeoni']='secret_home'
        self.assertEqual(env['r13_sidequest_places'](),[],'보고를 위해 비공개 장소를 해금하지 않는다')

    def test_malformed_optional_save_is_not_overwritten_or_applied(self):
        for group in (None, [], {'seam':'broken'}):
            with self.subTest(group=group):
                env,state=environment();state.room13['v111']['sidequests']=group
                before=copy.deepcopy(state.room13)
                self.assertEqual(env['r13_sidequest_person_actions']('resident_yeoni'),[])
                self.assertFalse(env['r13_sidequest_update']('seam','accept'))
                self.assertEqual(state.room13,before)

    def test_seam_tight_followup_remembers_who_loosened_the_thread(self):
        env,state=environment();env['r13_sidequest_update']('seam','accept');env['r13_sidequest_update']('seam','work','tight');env['r13_sidequest_update']('seam','report')
        lines=env['r13_sidequest_lines']('seam','done');text=' '.join(row['text'] for row in lines)
        self.assertIn('제가 풀었죠',text);self.assertNotIn('남겨 주신 틈',text)

if __name__=='__main__':unittest.main()
