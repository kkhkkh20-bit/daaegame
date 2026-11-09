"""독립 검토: 구 저장의 지난 대화 위치가 새 일과의 질문을 막는 반례."""
import ast
import copy
import re
import json
import textwrap
import unittest
from types import SimpleNamespace
from collections.abc import Mapping
from test_population146 import environment, ROOT
from test_play_review_field import load_function


def loaded_talk():
    env, state, binding, _ = environment(place='post')
    binding.update(people=[], options=[])
    state.room13['v111']['people'] = ['doto', 'resident_owlgp']
    state.room13['v111']['values'].update({'location:doto':'square', 'location:resident_owlgp':'square'})
    env.update(MS14_SPEAKERS={}, winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),
        ROOM13={'topics':{}}, r13_hyeoni_verses=lambda:[], r13_v111_questions=lambda p:[],
        r13_v111_has_business=lambda p:False, r13_v111_followups=lambda p:[], Return=lambda x:x)
    # 이 fixture는 분산 후의 실제 재실 목록을 전달한다. 배우/대화 허용은 모두 제품 함수를 실행한다.
    env['r13_visible_people'] = lambda:[p for p in ('doto', 'resident_owlgp')
        if env['r13_where'](p) == state.room13['location']]
    source=(ROOT/'game/systems/room13_v111_resident_talk.rpy').read_text()
    block=source.split('init 358 python:\n',1)[1].split('\nlabel ',1)[0]
    exec(textwrap.dedent(block),env)
    env['R13_V111_RESIDENT_DIALOGUE']=json.loads((ROOT/'game/v111/resident-dialogue.json').read_text())['people']
    return env,state,binding


def loaded_late_news_with_actual_reactions():
    """실제 7일 자유시간 binding과 선택자료 P036을 이전 업무 판정에 함께 공급한다."""
    binding = None
    for path in (ROOT/'game/v111').glob('field-bindings*.json'):
        data=json.loads(path.read_text())
        if 'free_day7' in data:
            binding=copy.deepcopy(data['free_day7'])
            break
    if binding is None:raise AssertionError('실제 free_day7 binding 누락')
    state=SimpleNamespace(room13=dict(day=7,period=1,location='dining',
        evidence=['V111:E09','V111:E06_CONTACT'],v111=dict(gate='free_day7',
        scene='MS14_D07_S03',people=[],values={'piko_alive':False})))
    values=state.room13['v111']['values']
    reactions=json.loads((ROOT/'game/v111/newworld/reactions.json').read_text())
    env=dict(store=state,R13_REACTIONS=reactions,r13_v111_binding=lambda:binding,
        r13_v111_value=values.get,r13_v111_owned=lambda k:'V111:'+k in state.room13['evidence'],
        r13_v111_active=lambda:True,r13_v111_actor_ready=lambda p:p=='nabi',
        r13_visible_people=lambda:['nabi'],r13_v111_person_alive=lambda p:True,
        r13_v111_tense_context=lambda:None,R13_PIKO_NEWS_PEOPLE=('nabi','buri'))
    for name in ('r13_reaction_day_ok','r13_v111_followups'):
        load_function('game/room13_v111_reactions.rpy',name,env)
    for name in ('r13_reaction_spec_id','r13_reaction_seen','r13_v111_has_business'):
        load_function('game/room13_v111_idle.rpy',name,env)
    env['_r13_resident_business']=env['r13_v111_has_business']
    load_function('game/systems/room13_v111_resident_talk.rpy','r13_v111_required_business',env)
    for name in ('r13_piko_resident_available','r13_piko_news_available',
                 'r13_piko_current_activity','r13_piko_required_business','r13_piko_report_due'):
        load_function('game/room13_piko_reactions.rpy',name,env)
    return env,state,binding


def loaded_actual_free7():
    env,state,binding=loaded_late_news_with_actual_reactions()
    state.room13['v111']['scene']='MS14_D07_S02'
    state.room13['v111']['values'].update({'meeting:fire':'win',
        'D07_S02_handover_completed':True,'D07_S02_message_completed':True,
        'D06_S03_main_completed':True,'warehouse_children_rescued':3,'KKOMI_ALIVE':False})
    for name in ('r13_v111_free7_ready','r13_v111_revisit_allowed'):
        load_function('game/room13_v111.rpy',name,env)
    source=(ROOT/'game/room13_v111_idle.rpy').read_text()
    env['R13_TENSE_SCENES']=ast.literal_eval(re.search(r'^    R13_TENSE_SCENES=(.+)$',source,re.M).group(1))
    load_function('game/room13_v111_idle.rpy','r13_v111_tense_context',env)
    env['R13SidequestMapping']=Mapping
    load_function('game/systems/room13_v111_sidequests.rpy','r13_sidequest_calm',env)
    return env,state,binding


class IndependentBranchReview146(unittest.TestCase):
    def test_old_square_speaker_can_answer_at_current_post_routine(self):
        env,state,_=loaded_talk();before=copy.deepcopy(state.room13)
        for person in ('doto','resident_owlgp'):
            with self.subTest(person=person):
                self.assertTrue(env['r13_v111_actor_ready'](person))
                self.assertTrue(env['r13_v111_resident_talk_available'](person),
                    '새 일과의 우체국에 실제로 서 있는 주민의 질문이 과거 광장 위치로 차단됨')
                self.assertGreaterEqual(len(env['r13_v111_resident_topics'](person)),2)
        self.assertEqual(state.room13,before,'질문 조회가 구 저장 상태를 고쳐 쓰지 않음')

    def test_optional_daily_questions_do_not_silence_late_piko_news(self):
        env,state,binding=loaded_talk()
        state.room13.update(day=4,location='inn')
        state.room13['v111']['values']['piko_alive']=False
        env['r13_v111_actor_ready']=lambda p:p=='nabi'
        env['r13_visible_people']=lambda:['nabi']
        env['r13_v111_owned']=lambda key:key=='E09'
        env['r13_v111_idle_lines']=lambda person:[]
        source=(ROOT/'game/room13_piko_reactions.rpy').read_text()
        block=source.split('init 354 python:\n',1)[1].split('\nlabel ',1)[0]
        exec(textwrap.dedent(block),env)
        self.assertTrue(env['r13_v111_has_business']('nabi'),'새로운 평시 선택 질문이 존재하는 준비 상태')
        self.assertTrue(env['r13_piko_news_available']('nabi'))
        self.assertFalse(env['r13_piko_current_activity']('nabi'))
        self.assertTrue(env['r13_piko_report_due']('nabi'),
            '3일 식당을 건너뛴 유저에게도 선택 일상질문 때문에 피코의 늦은 소식이 차단되지 않음')

    def test_actual_unheard_p036_keeps_optional_business_but_allows_late_news(self):
        env,state,binding=loaded_late_news_with_actual_reactions()
        before=copy.deepcopy(state.room13)
        spec=next(s for s in env['R13_REACTIONS']['present']
                  if any(row.get('id')=='NW_RX_P036_01' for row in s['lines']))
        self.assertEqual(spec['person'],'nabi');self.assertEqual(spec['evidence'],'E06_CONTACT')
        self.assertTrue(env['r13_reaction_day_ok'](spec))
        self.assertFalse(env['r13_reaction_seen'](spec))
        self.assertEqual(env['r13_v111_followups']('nabi'),[])
        self.assertTrue(env['r13_v111_has_business']('nabi'),
            'P036 선택 자료반응은 계속 대화업무로 남아 목록을 유지한다')
        self.assertFalse(env['r13_piko_current_activity']('nabi'))
        self.assertFalse(env['r13_piko_required_business']('nabi'))
        self.assertTrue(env['r13_piko_report_due']('nabi'),
            '아직 제시하지 않은 선택 자료반응이 늦은 피코 소식을 막지 않는다')
        self.assertEqual(state.room13,before)

    def test_actual_required_person_option_defers_news_until_that_option_is_absent(self):
        env,state,binding=loaded_late_news_with_actual_reactions()
        # 다른 장소의 필수 질문은 이곳에서 직접 전할 말을 막지 않는다.
        binding['options'].append(dict(person='nabi',location='school',title='학교의 필수 질문'))
        self.assertFalse(env['r13_piko_required_business']('nabi'))
        self.assertTrue(env['r13_piko_report_due']('nabi'))
        required=dict(person='nabi',location='dining',title='지금 현장에서 먼저 할 질문')
        binding['options'].append(required)
        before=copy.deepcopy(state.room13)
        self.assertTrue(env['r13_piko_required_business']('nabi'))
        self.assertFalse(env['r13_piko_report_due']('nabi'),'현재 필수 질문은 소식 전달보다 먼저')
        binding['options'].remove(required)
        self.assertTrue(env['r13_v111_has_business']('nabi'),'선택 P036은 읽음 처리하지 않았다')
        self.assertFalse(env['r13_piko_required_business']('nabi'))
        self.assertTrue(env['r13_piko_report_due']('nabi'),'필수 질문이 사라지면 선택자료가 남아도 소식 전달')
        self.assertEqual(state.room13,before)

    def test_new_routine_does_not_offer_remote_or_main_assigned_speakers(self):
        env,state,binding=loaded_talk();state.room13['location']='square'
        self.assertEqual(env['r13_v111_resident_topics']('doto'),[])
        state.room13['location']='post'
        binding['options']=[dict(person='doto',location='square')]
        self.assertEqual(env['r13_v111_resident_topics']('doto'),[])
        self.assertEqual(state.room13['v111']['values']['location:doto'],'square')


class ActualFree7Boundary146(unittest.TestCase):
    def test_completed_school_scene_supports_each_decided_fire_result_without_rewriting_scene(self):
        for result in ('win','partial','lose'):
            for fire in ('rescued_three','evacuated_four'):
                with self.subTest(result=result,fire=fire):
                    env,state,_=loaded_actual_free7();v=state.room13['v111']['values']
                    v['meeting:fire']=result
                    if fire=='evacuated_four':
                        v.pop('D06_S03_main_completed');v.pop('warehouse_children_rescued')
                        v.update(D06_S03P_empty_fire_completed=True,warehouse_children_school_handover=4,KKOMI_ALIVE=True)
                    before=copy.deepcopy(state.room13)
                    self.assertTrue(env['r13_v111_free7_ready']())
                    self.assertIsNone(env['r13_v111_tense_context']())
                    self.assertTrue(env['r13_v111_revisit_allowed']())
                    self.assertTrue(env['r13_sidequest_calm'](),'기수락 생활의뢰의 7일 마무리 진입 가능')
                    self.assertTrue(env['r13_piko_report_due']('nabi'),'S02 완료 저장에서도 늦은 소식을 전달 가능')
                    self.assertEqual(state.room13,before,'판정 조회는 장면·기록·분기 결과를 쓰지 않는다')

    def test_school_handover_and_message_in_progress_remain_tense_and_closed(self):
        for reason in ('handover','message','meeting','school_names','responsibility','day6','day8'):
            with self.subTest(reason=reason):
                env,state,_=loaded_actual_free7();v=state.room13['v111']['values']
                if reason=='handover':v.pop('D07_S02_handover_completed')
                elif reason=='message':v.pop('D07_S02_message_completed')
                elif reason=='meeting':v.pop('meeting:fire')
                elif reason=='school_names':state.room13['v111']['gate']='school_names7'
                elif reason=='responsibility':state.room13['v111']['gate']='responsibility7'
                elif reason=='day6':state.room13['day']=6
                elif reason=='day8':state.room13['day']=8
                before=copy.deepcopy(state.room13)
                self.assertFalse(env['r13_v111_free7_ready']())
                self.assertEqual(env['r13_v111_tense_context'](),'event')
                self.assertFalse(env['r13_v111_revisit_allowed']())
                self.assertFalse(env['r13_sidequest_calm']())
                self.assertEqual(state.room13,before)

    def test_completed_flags_do_not_open_custody_or_later_murder_routes(self):
        for reason in ('custody','murder','owl_dead','case_occurred','prevented_route'):
            with self.subTest(reason=reason):
                env,state,_=loaded_actual_free7();v=state.room13['v111']['values']
                if reason=='custody':v['DARAM_DETAINED']=True
                elif reason=='murder':v['route7']='murder'
                elif reason=='owl_dead':v['OWL_ALIVE']=False
                elif reason=='case_occurred':state.room13['case_state']='occurred'
                elif reason=='prevented_route':v['route7']='prevented'
                self.assertFalse(env['r13_v111_free7_ready']())
                self.assertEqual(env['r13_v111_tense_context'](),'event')
                self.assertFalse(env['r13_v111_revisit_allowed']())
                self.assertFalse(env['r13_sidequest_calm']())


if __name__=='__main__':unittest.main()
