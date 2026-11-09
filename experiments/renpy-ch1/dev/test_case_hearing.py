"""실제 청취 대상·변형 격리·조회 불변·저장 안의 청취 기록을 확인한다."""
import ast
import copy
import io
import json
from pathlib import Path
import re
import textwrap
import unittest
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_case_hearing.rpy'
PREFIX='hearing:heard:'


def fixture():
    return dict(cases=dict(
        lamp=dict(stages=[
            dict(key='수리',speaker='너울',line_ids=['RID_REPAIR'],title='수리 뒤의 돌',press_block='press_repair'),
            dict(key='거래',speaker='실룩',line_ids=['RID_SALE','RID_SALE_SECOND'],title='거래된 돌',press_block='press_sale'),
            dict(key='칼',speaker='실룩',line_ids=['RID_KNIFE'],title='칼 사용',press_block=None),
        ]),
        lamp_attempt=dict(stages=[
            dict(key='미수 파손',speaker='너울',line_ids=['RID_ATTEMPT'],title='남은 돌',press_block='press_attempt'),
        ])))


def other_cases():
    return dict(cases=dict(
        gate=dict(stages=[
            dict(key='입구 등록',speaker='돌목',line_ids=['RID_GATE'],title='빠진 이름',press_block='press_gate'),
            dict(key='입구 규칙',speaker='아빠',line_ids=['RID_GATE_QUESTION'],title='함께 들어갈 조건',
                 kind='question',press_block=None),
        ]),
        fire=dict(stages=[
            dict(key='화재 순서',speaker='너울',line_ids=['RID_FIRE'],title='불이 난 시각',press_block='press_fire'),
        ])))


def conditional_cases():
    def part(evacuated,target):
        return dict(when=dict(key='FIRE_EVACUATED',**{('equals' if evacuated else 'not_equals'):True}),
                    stages=[dict(key='화재 원인',speaker='너울',line_ids=[target],title='화재 원인 발언',press_block=None)])
    return dict(cases=dict(fire_evacuated=part(True,'RID_FIRE_EVACUATED'),
                           fire_not_evacuated=part(False,'RID_FIRE_NOT_EVACUATED')))


class CaseHearing(unittest.TestCase):
    def environment(self,data=None,values=None,room=True,available=True,files=None):
        state=SimpleNamespace(room13=dict(
            day=3,period=1,location='workshop',evidence=['V111:E11','V111:E13'],
            flags=['observed:lamp'],arguments={'v111:수리':['V111:E11']},
            v111=dict(gate='trial_repair',values=dict(values or {},**{'tries:lamp':2,'elapsed_minutes':75}))))
        if not room:state.room13=None
        metadata=fixture() if data is None else data
        files={'v111/case-hearing.json':metadata} if files is None else files
        def open_metadata(path):
            payload=files[path]
            return io.BytesIO(payload if isinstance(payload,bytes) else json.dumps(payload,ensure_ascii=False).encode())
        renpy=SimpleNamespace(loadable=lambda path:available and path in files,file=open_metadata)
        env=dict(store=state,renpy=renpy,json=json,winter_copy=copy)
        for block in re.finditer(r'^init \d+ python:\n((?:[ \t].*\n|\n)*)',SOURCE.read_text(),re.M):
            exec(compile(ast.parse(textwrap.dedent(block.group(1))),'실제 청취 대상','exec'),env)
        return env,state

    def hear(self,env,rid,text='실제로 들은 말',speaker='neoul'):
        return env['r13_case_hearing_heard']((speaker,text,dict(line_id=rid)))

    def test_missing_metadata_or_unknown_key_falls_back_without_state_changes(self):
        for data,available in (({},True),(fixture(),False),({'cases':None},True)):
            env,state=self.environment(data=data,available=available)
            before=copy.deepcopy(state.room13)
            self.assertIsNone(env['r13_case_hearing_spec']('수리'))
            self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
            self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))
            self.assertIsNone(env['r13_case_hearing_press_block']('수리','RID_REPAIR'))
            self.assertFalse(self.hear(env,'RID_REPAIR'))
            self.assertEqual(state.room13,before)

    def test_valid_metadata_does_not_make_unheard_quotes_visible(self):
        env,state=self.environment()
        self.assertEqual(env['r13_case_hearing_spec']('v111:수리')['title'],'수리 뒤의 돌')
        before=copy.deepcopy(state.room13)
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
        self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))
        self.assertIsNone(env['r13_case_hearing_press_block']('수리','RID_REPAIR'))
        self.assertEqual(state.room13,before)

    def test_added_dialogue_source_ids_are_recorded_without_relabeling_the_text(self):
        env,state=self.environment(values={'lamp_bound2':True})
        packet=('neoul','실제로 들은 미수판의 말',dict(source_id='RID_ATTEMPT'))
        self.assertTrue(env['r13_case_hearing_heard'](packet))
        self.assertEqual(env['r13_case_hearing_quote']('RID_ATTEMPT'),
                         dict(speaker='neoul',text=packet[1]))

    def test_both_actual_packet_ids_are_checked_instead_of_shadowing_the_source_id(self):
        data=fixture();data['cases'].update(other_cases()['cases'])
        env,state=self.environment(data=data)
        for line_id in ('UNKNOWN',None,False):
            packet=('neoul','실제로 들은 원문',dict(line_id=line_id,source_id='RID_FIRE'))
            changed=env['r13_case_hearing_heard'](packet)
            self.assertEqual(changed,line_id=='UNKNOWN')
            self.assertEqual(env['r13_case_hearing_quote']('RID_FIRE'),dict(speaker='neoul',text=packet[1]))
        self.assertTrue(env['r13_case_hearing_heard'](('neoul','같은 완료 발화',dict(line_id='RID_GATE',source_id='RID_FIRE'))))
        self.assertEqual(env['r13_case_hearing_quote']('RID_GATE'),env['r13_case_hearing_quote']('RID_FIRE'))
        before=state.room13
        self.assertFalse(env['r13_case_hearing_heard'](('neoul','같은 완료 발화',dict(line_id='RID_GATE',source_id='RID_FIRE'))))
        self.assertIs(state.room13,before)

    def test_builtin_json_lists_remain_valid_when_renpy_rebinds_the_list_name(self):
        class RevertableListLike(list):
            pass
        env,state=self.environment(files={
            'v111/case-hearing.json':fixture(),
            'v111/case-hearing-early.json':other_cases(),
        })
        env['list']=RevertableListLike
        stages=env['R13_CASE_HEARING_DATA']['cases']['lamp']['stages']
        self.assertIs(type(stages),list)
        self.assertNotIsInstance(stages,RevertableListLike)
        self.assertIsNotNone(env['r13_case_hearing_spec']('수리'))
        self.assertTrue(env['r13_case_hearing_heard'](['neoul','실제로 들은 말',dict(line_id='RID_REPAIR')]))
        self.assertEqual([row['target'] for row in env['r13_case_hearing_rows']('수리')],['RID_REPAIR'])
        self.assertEqual(env['r13_case_hearing_press_block']('수리','RID_REPAIR'),'press_repair')
        self.assertTrue(self.hear(env,'RID_GATE_QUESTION',speaker='dad'))
        self.assertEqual(env['r13_case_hearing_rows']('입구 규칙')[0]['kind'],'question')
        for value in ('RID_REPAIR',b'RID_REPAIR',bytearray(b'RID_REPAIR')):
            self.assertFalse(env['r13_case_hearing_sequence'](value))

    def test_heard_records_only_the_actual_packet_in_the_room_save_state(self):
        env,state=self.environment()
        before=copy.deepcopy(state.room13)
        text='아니요.{w=.3}\n방금 실제로 한 말입니다.'
        self.assertTrue(self.hear(env,'RID_REPAIR',text,'resident_siluk'))
        expected=copy.deepcopy(before)
        expected['v111']['values'][PREFIX+'RID_REPAIR']=dict(speaker='resident_siluk',text=text)
        self.assertEqual(state.room13,expected)
        self.assertEqual(env['r13_case_hearing_quote']('RID_REPAIR'),dict(speaker='resident_siluk',text=text))
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[
            dict(key='수리',target='RID_REPAIR',title='수리 뒤의 돌',kind='statement',speaker='resident_siluk',text=text)])

    def test_revisiting_an_earlier_issue_keeps_actually_heard_later_statements(self):
        env,state=self.environment()
        self.hear(env,'RID_KNIFE','칼에 관해 실제로 말한 내용','resident_siluk')
        self.hear(env,'RID_REPAIR')
        rows=env['r13_case_hearing_rows']('수리')
        self.assertEqual([row['target'] for row in rows],['RID_REPAIR','RID_KNIFE'])
        self.assertNotIn('RID_SALE',[row['target'] for row in rows])
        self.assertEqual(env['r13_case_hearing_rows']('칼'),rows)

    def test_attempt_and_theft_never_share_unique_statement_targets(self):
        env,state=self.environment(values={'lamp_bound2':False})
        self.hear(env,'RID_REPAIR')
        self.assertFalse(self.hear(env,'RID_ATTEMPT','남아 있는 돌'))
        state.room13['v111']['values']['lamp_bound2']=True
        self.assertIsNone(env['r13_case_hearing_spec']('수리'))
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
        self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))
        self.assertIsNone(env['r13_case_hearing_press_block']('미수 파손','RID_REPAIR'))
        self.assertTrue(self.hear(env,'RID_ATTEMPT','남아 있는 돌'))
        self.assertEqual([row['target'] for row in env['r13_case_hearing_rows']('미수 파손')],['RID_ATTEMPT'])
        self.assertFalse(self.hear(env,'RID_KNIFE'))

    def test_press_uses_only_the_selected_heard_targets_own_block(self):
        env,state=self.environment()
        self.hear(env,'RID_REPAIR')
        self.hear(env,'RID_SALE','돌을 팔았습니다.','resident_siluk')
        self.assertEqual(env['r13_case_hearing_press_block']('수리','RID_SALE'),'press_sale')
        self.assertEqual(env['r13_case_hearing_press_block']('거래','RID_REPAIR'),'press_repair')
        self.assertIsNone(env['r13_case_hearing_press_block']('수리','RID_SALE_SECOND'))
        self.assertIsNone(env['r13_case_hearing_press_block']('없는 쟁점','RID_REPAIR'))
        self.hear(env,'RID_KNIFE')
        self.assertIsNone(env['r13_case_hearing_press_block']('칼','RID_KNIFE'))

    def test_queries_and_returned_rows_do_not_mutate_domain_or_cached_quotes(self):
        env,state=self.environment()
        self.hear(env,'RID_REPAIR')
        before=copy.deepcopy(state.room13)
        metadata=copy.deepcopy(env['R13_CASE_HEARING_DATA'])
        for key in ('수리','거래','칼','v111:수리','다른 사건'):
            env['r13_case_hearing_spec'](key)
            env['r13_case_hearing_rows'](key)
            env['r13_case_hearing_quote']('RID_REPAIR')
            env['r13_case_hearing_press_block'](key,'RID_REPAIR')
        env['r13_case_hearing_spec']('수리')['line_ids'].append('FAKE')
        env['r13_case_hearing_spec']('수리')['target_titles']['RID_REPAIR']='가짜 제목'
        env['r13_case_hearing_rows']('수리')[0]['text']='가짜 말'
        env['r13_case_hearing_quote']('RID_REPAIR')['speaker']='fake'
        self.assertEqual(state.room13,before)
        self.assertEqual(env['R13_CASE_HEARING_DATA'],metadata)

    def test_duplicate_hearing_is_a_noop_and_a_revised_actual_line_replaces_only_itself(self):
        env,state=self.environment()
        self.hear(env,'RID_REPAIR','첫 발언')
        previous=state.room13
        self.assertFalse(self.hear(env,'RID_REPAIR','첫 발언'))
        self.assertIs(state.room13,previous)
        before=copy.deepcopy(state.room13)
        self.assertTrue(self.hear(env,'RID_REPAIR','수정해서 실제로 한 발언'))
        before['v111']['values'][PREFIX+'RID_REPAIR']['text']='수정해서 실제로 한 발언'
        self.assertEqual(state.room13,before)

    def test_unregistered_narrative_or_malformed_packets_do_not_write(self):
        env,state=self.environment()
        before=copy.deepcopy(state.room13)
        packets=[None,(),('neoul','말'),('neoul','말',None),('neoul','말',{}),
                 ('neoul','말',dict(line_id='UNKNOWN')),(None,'지문',dict(line_id='RID_REPAIR')),
                 ('neoul','',dict(line_id='RID_REPAIR')),('neoul',None,dict(line_id='RID_REPAIR'))]
        for packet in packets:
            with self.subTest(packet=packet):self.assertFalse(env['r13_case_hearing_heard'](packet))
        self.assertEqual(state.room13,before)

    def test_unregistered_packets_return_before_reading_room_or_scanning_cases(self):
        def unexpected_lookup(*args,**kwargs):
            self.fail('미등록 대사에서 저장 상태나 전체 사건을 조회했다.')
        for has_room in (False,True):
            env,state=self.environment(room=has_room)
            self.assertIsInstance(env['R13_CASE_HEARING_REGISTERED_TARGETS'],frozenset)
            before=copy.deepcopy(state.room13)
            env['r13_case_hearing_values']=unexpected_lookup
            env['r13_case_hearing_eligible_cases']=unexpected_lookup
            env['r13_case_hearing_stages']=unexpected_lookup
            for options in (dict(line_id='UNKNOWN'),dict(source_id='UNKNOWN'),
                            dict(line_id='UNKNOWN',source_id='OTHER_UNKNOWN'),
                            dict(line_id=['RID_REPAIR'],source_id={})):
                self.assertFalse(env['r13_case_hearing_heard'](('dad','일반 대사를 끝까지 읽었다.',options)))
            self.assertEqual(state.room13,before)

    def test_invalid_or_cross_case_cached_data_does_not_become_a_quote(self):
        for record in (None,True,'말',{},dict(speaker='neoul'),dict(speaker='neoul',text=None),dict(speaker=None,text='말')):
            env,state=self.environment(values={PREFIX+'RID_REPAIR':record})
            self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))
            self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
        env,state=self.environment(values={PREFIX+'UNKNOWN':dict(speaker='neoul',text='누출 금지')})
        self.assertIsNone(env['r13_case_hearing_quote']('UNKNOWN'))

    def test_old_or_restored_room_without_heard_cache_is_not_reconstructed_from_metadata(self):
        env,state=self.environment()
        checkpoint=copy.deepcopy(state.room13)
        self.hear(env,'RID_REPAIR')
        self.assertTrue(env['r13_case_hearing_rows']('수리'))
        state.room13=checkpoint
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
        self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))

    def test_missing_room_is_safe_for_all_runtime_entrypoints(self):
        env,state=self.environment(room=False)
        self.assertIsNone(env['r13_case_hearing_spec']('수리'))
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
        self.assertIsNone(env['r13_case_hearing_quote']('RID_REPAIR'))
        self.assertIsNone(env['r13_case_hearing_press_block']('수리','RID_REPAIR'))
        self.assertFalse(self.hear(env,'RID_REPAIR'))
        self.assertIsNone(state.room13)

    def test_ambiguous_or_unapproved_stage_metadata_falls_back(self):
        mutations=[lambda stages:stages[0].update(correct=['E11','E13']),
                   lambda stages:stages[0].update(line_ids=['RID_REPAIR','RID_REPAIR']),
                   lambda stages:stages[1].update(line_ids=['RID_REPAIR']),
                   lambda stages:stages[1].update(key='수리'),
                   lambda stages:stages[0].update(line_ids=[]),
                   lambda stages:stages[0].update(title=''),
                   lambda stages:stages[0].update(press_block=[]),
                   lambda stages:stages[0].update(kind='thought'),
                   lambda stages:stages[0].update(latest_only='false'),
                   lambda stages:stages[0].update(latest_only=1),
                   lambda stages:stages[0].update(latest_only=None),
                   lambda stages:stages[0].update(target_titles=[]),
                   lambda stages:stages[0].update(target_titles=None),
                   lambda stages:stages[0].update(target_titles={'UNKNOWN':'다른 대상의 제목'}),
                   lambda stages:stages[0].update(target_titles={'RID_REPAIR':''}),
                   lambda stages:stages[0].update(target_titles={'RID_REPAIR':False})]
        for mutate in mutations:
            data=fixture();mutate(data['cases']['lamp']['stages'])
            env,state=self.environment(data=data)
            self.assertIsNone(env['r13_case_hearing_spec']('수리'))
            self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
            self.assertFalse(self.hear(env,'RID_REPAIR'))

    def test_fixed_metadata_files_merge_without_requiring_the_original_file(self):
        env,state=self.environment(files={
            'v111/case-hearing-early.json':other_cases(),
            'v111/case-hearing-ending.json':fixture(),
            'v111/case-hearing-unregistered.json':dict(cases=dict(ignored=other_cases()['cases']['gate'])),
        })
        self.assertEqual(set(env['R13_CASE_HEARING_DATA']['cases']),{'gate','fire','lamp','lamp_attempt'})
        self.assertEqual(env['R13_CASE_HEARING_DATA']['conflicts'],[])
        self.assertIsNotNone(env['r13_case_hearing_spec']('입구 등록'))
        self.assertTrue(self.hear(env,'RID_GATE'))
        self.assertEqual([row['target'] for row in env['r13_case_hearing_rows']('입구 등록')],['RID_GATE'])

    def test_malformed_optional_file_does_not_disable_other_files(self):
        for malformed in (b'{bad json',None,{},dict(cases=None)):
            env,state=self.environment(files={
                'v111/case-hearing.json':fixture(),
                'v111/case-hearing-mid.json':malformed,
                'v111/case-hearing-late.json':other_cases(),
            })
            self.assertIsNotNone(env['r13_case_hearing_spec']('수리'))
            self.assertIsNotNone(env['r13_case_hearing_spec']('화재 순서'))

    def test_duplicate_case_definitions_are_disabled_without_selecting_one_arbitrarily(self):
        duplicate=dict(cases=dict(lamp=fixture()['cases']['lamp']))
        env,state=self.environment(files={
            'v111/case-hearing.json':fixture(),
            'v111/case-hearing-early.json':other_cases(),
            'v111/case-hearing-mid.json':duplicate,
            'v111/case-hearing-ending.json':duplicate,
        })
        self.assertEqual(env['R13_CASE_HEARING_DATA']['conflicts'],['lamp'])
        self.assertNotIn('lamp',env['R13_CASE_HEARING_DATA']['cases'])
        self.assertIsNone(env['r13_case_hearing_spec']('수리'))
        self.assertFalse(self.hear(env,'RID_REPAIR'))
        self.assertIsNotNone(env['r13_case_hearing_spec']('입구 등록'))
        state.room13['v111']['values']['lamp_bound2']=True
        self.assertIsNotNone(env['r13_case_hearing_spec']('미수 파손'))

    def test_key_selects_one_case_and_rows_do_not_mix_other_cached_cases(self):
        data=fixture();data['cases'].update(other_cases()['cases'])
        env,state=self.environment(data=data)
        for target in ('RID_REPAIR','RID_GATE','RID_FIRE'):
            self.assertTrue(self.hear(env,target))
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('수리')],['RID_REPAIR'])
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('v111:입구 등록')],['RID_GATE'])
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('화재 순서')],['RID_FIRE'])
        self.assertIsNone(env['r13_case_hearing_press_block']('입구 등록','RID_FIRE'))
        self.assertEqual(env['r13_case_hearing_press_block']('화재 순서','RID_FIRE'),'press_fire')

    def test_packet_registration_does_not_depend_on_the_previous_case_claim(self):
        data=fixture();data['cases'].update(other_cases()['cases'])
        env,state=self.environment(data=data)
        state.v111_claim='v111:수리'
        state.room13['v111']['values']['current_case']='lamp'
        before=copy.deepcopy(state.room13)
        self.assertTrue(env['r13_case_hearing_heard'](('neoul','방금 들은 화재 발언',dict(source_id='RID_FIRE'))))
        expected=copy.deepcopy(before)
        expected['v111']['values'][PREFIX+'RID_FIRE']=dict(speaker='neoul',text='방금 들은 화재 발언')
        self.assertEqual(state.room13,expected)
        self.assertEqual(env['r13_case_hearing_quote']('RID_FIRE'),dict(speaker='neoul',text='방금 들은 화재 발언'))
        self.assertEqual(env['r13_case_hearing_rows']('수리'),[])

    def test_same_actual_target_may_belong_to_distinct_cases_but_not_distinct_stages_in_one_case(self):
        data=other_cases()
        data['cases']['fire']['stages'][0]['line_ids']=['RID_GATE']
        env,state=self.environment(data=data)
        self.assertTrue(self.hear(env,'RID_GATE'))
        self.assertEqual([r['key'] for r in env['r13_case_hearing_rows']('입구 등록')],['입구 등록'])
        self.assertEqual([r['key'] for r in env['r13_case_hearing_rows']('화재 순서')],['화재 순서'])
        self.assertEqual(env['r13_case_hearing_press_block']('입구 등록','RID_GATE'),'press_gate')
        self.assertEqual(env['r13_case_hearing_press_block']('화재 순서','RID_GATE'),'press_fire')
        data['cases']['gate']['stages'][1]['line_ids']=['RID_GATE']
        env,state=self.environment(data=data)
        self.assertIsNone(env['r13_case_hearing_spec']('입구 등록'))
        self.assertIsNotNone(env['r13_case_hearing_spec']('화재 순서'))

    def test_same_key_in_distinct_eligible_cases_falls_back_instead_of_merging_rows(self):
        data=other_cases()
        data['cases']['fire']['stages'][0]['key']='입구 등록'
        env,state=self.environment(data=data)
        self.hear(env,'RID_GATE');self.hear(env,'RID_FIRE')
        self.assertIsNone(env['r13_case_hearing_case_for'](data,'입구 등록',{}))
        self.assertIsNone(env['r13_case_hearing_spec']('입구 등록'))
        self.assertEqual(env['r13_case_hearing_rows']('입구 등록'),[])
        self.assertIsNone(env['r13_case_hearing_press_block']('입구 등록','RID_GATE'))
        self.assertIsNotNone(env['r13_case_hearing_spec']('입구 규칙'))

    def test_lamp_variant_isolation_does_not_hide_other_case_quotes(self):
        data=fixture();data['cases'].update(other_cases()['cases'])
        cached={PREFIX+'RID_REPAIR':dict(speaker='neoul',text='기존 도난판 말'),
                PREFIX+'RID_ATTEMPT':dict(speaker='neoul',text='기존 미수판 말'),
                PREFIX+'RID_FIRE':dict(speaker='neoul',text='다른 사건 말')}
        for attempt in (False,True):
            env,state=self.environment(data=data,values=dict(cached,lamp_bound2=attempt))
            allowed='RID_ATTEMPT' if attempt else 'RID_REPAIR'
            forbidden='RID_REPAIR' if attempt else 'RID_ATTEMPT'
            self.assertIsNotNone(env['r13_case_hearing_quote'](allowed))
            self.assertIsNone(env['r13_case_hearing_quote'](forbidden))
            self.assertIsNotNone(env['r13_case_hearing_quote']('RID_FIRE'))
            self.assertFalse(self.hear(env,forbidden,'새 오염 발언'))
            self.assertEqual(env['r13_case_hearing_case'](dict(lamp_bound2=attempt)),
                             env['r13_case_hearing_legacy_case'](dict(lamp_bound2=attempt)))

    def test_question_kind_preserves_the_actual_questioner_and_text(self):
        env,state=self.environment(data=other_cases())
        self.assertEqual(env['r13_case_hearing_spec']('입구 규칙')['kind'],'question')
        self.assertEqual(env['r13_case_hearing_rows']('입구 규칙'),[])
        question='이 이름만 빠져 있는데, 왜 함께 못 들어갑니까?'
        self.hear(env,'RID_GATE_QUESTION',question,'dad')
        self.assertEqual(env['r13_case_hearing_rows']('입구 규칙'),[
            dict(key='입구 규칙',target='RID_GATE_QUESTION',title='함께 들어갈 조건',kind='question',speaker='dad',text=question)])
        self.assertEqual(env['r13_case_hearing_quote']('RID_GATE_QUESTION'),dict(speaker='dad',text=question))

    def test_latest_only_replaces_a_quote_only_after_the_revised_actual_line_is_heard(self):
        data=other_cases()
        stage=data['cases']['gate']['stages'][0]
        stage.update(line_ids=['RID_GATE','RID_GATE_REVISED'],latest_only=True)
        env,state=self.environment(data=data)
        self.assertEqual(env['r13_case_hearing_rows']('입구 등록'),[])
        self.hear(env,'RID_GATE','지금 명단에는 이름이 없습니다.','resident_dolmok')
        before=copy.deepcopy(state.room13)
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('입구 등록')],['RID_GATE'])
        self.assertIsNone(env['r13_case_hearing_quote']('RID_GATE_REVISED'))
        self.assertEqual(state.room13,before)
        revised='신청서에 이름이 있네요. 명단에 옮겨 적지 않았습니다.'
        self.hear(env,'RID_GATE_REVISED',revised,'resident_dolmok')
        self.assertEqual(env['r13_case_hearing_rows']('입구 등록'),[
            dict(key='입구 등록',target='RID_GATE_REVISED',title='빠진 이름',kind='statement',
                 speaker='resident_dolmok',text=revised)])
        self.assertEqual(env['r13_case_hearing_quote']('RID_GATE')['text'],'지금 명단에는 이름이 없습니다.')
        self.hear(env,'RID_GATE','실제로 다시 들은 이전 거절','resident_dolmok')
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('입구 등록')],['RID_GATE_REVISED'])
        self.assertEqual(env['r13_case_hearing_quote']('RID_GATE')['text'],'실제로 다시 들은 이전 거절')

    def test_latest_only_defaults_to_false_and_keeps_all_heard_targets(self):
        env,state=self.environment()
        self.assertIs(env['r13_case_hearing_spec']('거래')['latest_only'],False)
        self.hear(env,'RID_SALE','처음 들은 거래 발언')
        self.hear(env,'RID_SALE_SECOND','두 번째 거래 발언')
        self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('거래')],['RID_SALE','RID_SALE_SECOND'])

    def test_each_target_title_is_used_only_for_its_actually_heard_line(self):
        data=fixture();stage=data['cases']['lamp']['stages'][1]
        stage['target_titles']={'RID_SALE':'돌을 받았다는 말','RID_SALE_SECOND':'돌을 팔았다는 말'}
        env,state=self.environment(data=data)
        self.assertEqual(env['r13_case_hearing_rows']('거래'),[])
        self.hear(env,'RID_SALE','받았다고 실제로 한 말','resident_siluk')
        before=copy.deepcopy(state.room13)
        rows=env['r13_case_hearing_rows']('거래')
        self.assertEqual([(r['target'],r['title'],r['text']) for r in rows],
                         [('RID_SALE','돌을 받았다는 말','받았다고 실제로 한 말')])
        self.assertNotIn('돌을 팔았다는 말',json.dumps(rows,ensure_ascii=False))
        self.assertEqual(state.room13,before)
        self.hear(env,'RID_SALE_SECOND','팔았다고 실제로 한 말','resident_siluk')
        rows=env['r13_case_hearing_rows']('거래')
        self.assertEqual([(r['target'],r['title']) for r in rows],
                         [('RID_SALE','돌을 받았다는 말'),('RID_SALE_SECOND','돌을 팔았다는 말')])
        self.assertEqual(env['r13_case_hearing_press_block']('거래','RID_SALE'),'press_sale')
        self.assertEqual(env['r13_case_hearing_press_block']('거래','RID_SALE_SECOND'),'press_sale')
        env['r13_case_hearing_spec']('거래')['target_titles']['RID_SALE']='가짜 제목'
        self.assertEqual(env['r13_case_hearing_rows']('거래')[0]['title'],'돌을 받았다는 말')

    def test_legacy_metadata_and_partial_target_titles_keep_the_stage_title_as_fallback(self):
        data=fixture();stage=data['cases']['lamp']['stages'][1]
        stage['target_titles']={'RID_SALE':'받았다는 대목'}
        cached={PREFIX+'RID_SALE':dict(speaker='resident_siluk',text='구 저장의 첫 원문'),
                PREFIX+'RID_SALE_SECOND':dict(speaker='resident_siluk',text='구 저장의 두 번째 원문')}
        env,state=self.environment(data=data,values=cached)
        before=copy.deepcopy(state.room13)
        self.assertEqual([r['title'] for r in env['r13_case_hearing_rows']('거래')],['받았다는 대목','거래된 돌'])
        self.assertEqual(env['r13_case_hearing_quote']('RID_SALE_SECOND')['text'],'구 저장의 두 번째 원문')
        self.assertEqual(state.room13,before)
        env,state=self.environment(values=cached)
        self.assertEqual(env['r13_case_hearing_spec']('거래')['target_titles'],{})
        self.assertEqual([r['title'] for r in env['r13_case_hearing_rows']('거래')],['거래된 돌','거래된 돌'])

    def test_case_condition_uses_only_values_and_treats_missing_as_not_true(self):
        for values,expected in (({},'fire_not_evacuated'),({'FIRE_EVACUATED':None},'fire_not_evacuated'),
                                ({'FIRE_EVACUATED':False},'fire_not_evacuated'),
                                ({'FIRE_EVACUATED':True},'fire_evacuated')):
            env,state=self.environment(data=conditional_cases(),values=values)
            state.v111_claim='v111:수리'
            before=copy.deepcopy(state.room13)
            self.assertEqual(env['r13_case_hearing_case_for'](env['R13_CASE_HEARING_DATA'],'화재 원인',values),expected)
            self.assertIsNotNone(env['r13_case_hearing_spec']('화재 원인'))
            allowed='RID_FIRE_EVACUATED' if expected=='fire_evacuated' else 'RID_FIRE_NOT_EVACUATED'
            blocked='RID_FIRE_NOT_EVACUATED' if expected=='fire_evacuated' else 'RID_FIRE_EVACUATED'
            self.assertFalse(self.hear(env,blocked))
            self.assertEqual(state.room13,before)
            self.assertTrue(self.hear(env,allowed))
            self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('화재 원인')],[allowed])

    def test_inactive_condition_does_not_expose_an_existing_cached_quote(self):
        cached={PREFIX+'RID_FIRE_EVACUATED':dict(speaker='neoul',text='대피한 분기에서 들은 말'),
                PREFIX+'RID_FIRE_NOT_EVACUATED':dict(speaker='neoul',text='대피 못 한 분기에서 들은 말')}
        for evacuated in (False,True):
            env,state=self.environment(data=conditional_cases(),values=dict(cached,FIRE_EVACUATED=evacuated))
            allowed='RID_FIRE_EVACUATED' if evacuated else 'RID_FIRE_NOT_EVACUATED'
            blocked='RID_FIRE_NOT_EVACUATED' if evacuated else 'RID_FIRE_EVACUATED'
            self.assertIsNotNone(env['r13_case_hearing_quote'](allowed))
            self.assertIsNone(env['r13_case_hearing_quote'](blocked))
            self.assertIsNone(env['r13_case_hearing_press_block']('화재 원인',blocked))
            self.assertEqual([r['target'] for r in env['r13_case_hearing_rows']('화재 원인')],[allowed])
            inactive='fire_not_evacuated' if evacuated else 'fire_evacuated'
            values=state.room13['v111']['values'];data=env['R13_CASE_HEARING_DATA']
            self.assertIsNone(env['r13_case_hearing_quote_for'](data,inactive,blocked,values))
            self.assertEqual(env['r13_case_hearing_rows_for'](data,inactive,'화재 원인',values),[])
            self.assertIsNone(env['r13_case_hearing_press_for'](data,inactive,'화재 원인',blocked,values))

    def test_piko_branch_first_keys_and_shared_last_key_select_only_the_eligible_case(self):
        def case(attempt,first_key,target):
            return dict(when=dict(key='lamp_bound2',**{('equals' if attempt else 'not_equals'):True}),stages=[
                dict(key=first_key,speaker='실룩',line_ids=[target],title='값에 관한 실제 말',press_block=None),
                dict(key='피코가 막혀야 했던 까닭을 보인다',speaker='너울',line_ids=['RID_PIKO_LAST'],
                     title='진술을 믿을 수 없다는 반응',press_block='press_piko_last')])
        stolen_key='장부의 두 배를 실룩에게 보인다'
        attempt_key='인수하지 않은 돌의 약속 값을 보인다'
        shared_key='피코가 막혀야 했던 까닭을 보인다'
        data=dict(cases=dict(piko13_stolen=case(False,stolen_key,'RID_PIKO_STOLEN'),
                             piko13_attempt=case(True,attempt_key,'RID_PIKO_ATTEMPT')))
        cached={PREFIX+rid:dict(speaker='resident_siluk' if rid!='RID_PIKO_LAST' else 'neoul',text=rid+' 실제 말')
                for rid in ('RID_PIKO_STOLEN','RID_PIKO_ATTEMPT','RID_PIKO_LAST')}
        for bound in ('missing',None,False,True):
            values=dict(cached)
            if bound!='missing':values['lamp_bound2']=bound
            env,state=self.environment(data=data,values=values)
            active='piko13_attempt' if bound is True else 'piko13_stolen'
            active_key=attempt_key if bound is True else stolen_key
            blocked_key=stolen_key if bound is True else attempt_key
            active_target='RID_PIKO_ATTEMPT' if bound is True else 'RID_PIKO_STOLEN'
            blocked_target='RID_PIKO_STOLEN' if bound is True else 'RID_PIKO_ATTEMPT'
            before=copy.deepcopy(state.room13)
            for key in (active_key,shared_key):
                self.assertEqual(env['r13_case_hearing_case_for'](data,key,values),active)
                self.assertEqual({r['target'] for r in env['r13_case_hearing_rows'](key)},
                                 {active_target,'RID_PIKO_LAST'})
            self.assertIsNone(env['r13_case_hearing_spec'](blocked_key))
            self.assertEqual(env['r13_case_hearing_rows'](blocked_key),[])
            self.assertIsNone(env['r13_case_hearing_quote'](blocked_target))
            self.assertIsNotNone(env['r13_case_hearing_quote']('RID_PIKO_LAST'))
            self.assertFalse(self.hear(env,blocked_target,'다른 분기 발언'))
            self.assertEqual(state.room13,before)

    def test_ambiguous_or_malformed_case_conditions_fail_closed(self):
        for condition in ('FIRE_EVACUATED',True,{},dict(key='FIRE_EVACUATED'),
                          dict(key='FIRE_EVACUATED',equals=True,not_equals=False),
                          dict(key='',equals=True),dict(key='FIRE_EVACUATED',equals=[]),
                          dict(key='FIRE_EVACUATED',equals=True,eval='unsafe')):
            data=other_cases();data['cases']['gate']['when']=condition
            env,state=self.environment(data=data,values={'FIRE_EVACUATED':True})
            before=copy.deepcopy(state.room13)
            self.assertIsNone(env['r13_case_hearing_spec']('입구 등록'))
            self.assertFalse(self.hear(env,'RID_GATE'))
            self.assertIsNotNone(env['r13_case_hearing_spec']('화재 순서'))
            self.assertEqual(state.room13,before)

    def test_shipped_targets_point_to_real_speech_and_contain_only_display_metadata(self):
        names=('case-hearing.json','case-hearing-early.json','case-hearing-mid.json',
               'case-hearing-late.json','case-hearing-ending.json')
        files={'v111/'+name:json.loads(path.read_text()) for name in names
               if (path:=ROOT/'game/v111'/name).exists()}
        if not files:self.skipTest('표시 메타가 없으면 런타임은 기존 화면으로 돌아간다.')
        env,state=self.environment(files=files)
        data=env['R13_CASE_HEARING_DATA']
        self.assertEqual(data['conflicts'],[])
        records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
        spoken={key:row.get('speaker') for key,row in records.items() if row.get('speaker')}
        source_text={key:row.get('text') for key,row in records.items()}
        blocks=set()
        for source in (ROOT/'game/v111/newworld').glob('*.json'):
            part=json.loads(source.read_text())
            blocks.update(part.get('blocks',{}))
            for rid,row in part.get('replace',{}).items():
                if isinstance(row,dict):
                    if 'speaker' in row:spoken[rid]=row['speaker']
                    if 'text' in row:source_text[rid]=row['text']
            for group in ('before','after','blocks'):
                for rows in part.get(group,{}).values():
                    for row in rows:
                        if row.get('speaker') and row.get('id'):
                            spoken[row['id']]=row['speaker'];source_text[row['id']]=row['text']
        for case in data['cases']:
            stages=env['r13_case_hearing_stages'](data,case)
            self.assertEqual(len(stages),len(data['cases'][case]['stages']))
            self.assertTrue(stages)
            for stage in stages:
                if stage['press_block'] is not None:self.assertIn(stage['press_block'],blocks)
                for target in stage['line_ids']:
                    self.assertIn(target,spoken)
                    self.assertEqual(spoken[target],stage['speaker'])
                # 같은 단계의 서로 다른 실제 발언은 같은 선택 제목을 쓰지 않는다.
                # latest_only는 한 행만 보이고, 같은 원문의 배타적 경로 RID는 구별할 내용을 만들지 않는다.
                targets=stage['line_ids']
                if len(targets)>1 and not stage['latest_only'] and len({source_text[t] for t in targets})>1:
                    titles=[stage['target_titles'].get(t,stage['title']) for t in targets]
                    self.assertEqual(len(set(titles)),len(titles),(case,stage['key'],titles))
        cached={PREFIX+target:dict(speaker=spoken[target],text='실제 청취 캐시를 보존한 저장 예시')
                for case in data['cases'] for stage in env['r13_case_hearing_stages'](data,case)
                for target in stage['line_ids']}
        for attempt in (False,True):
            for fire in (None,False,True):
                values=dict(cached,lamp_bound2=attempt,FIRE_EVACUATED=fire)
                env,state=self.environment(files=files,values=values)
                eligible=env['r13_case_hearing_eligible_cases'](data,values)
                registered={target for case in eligible for stage in env['r13_case_hearing_stages'](data,case)
                            for target in stage['line_ids']}
                for case in eligible:
                    targets={target for stage in env['r13_case_hearing_stages'](data,case)
                             for target in (stage['line_ids'][-1:] if stage['latest_only'] else stage['line_ids'])}
                    for stage in env['r13_case_hearing_stages'](data,case):
                        self.assertEqual(env['r13_case_hearing_case_for'](data,stage['key'],values),case)
                        self.assertEqual({r['target'] for r in env['r13_case_hearing_rows'](stage['key'])},targets)
                for cache_key in cached:
                    target=cache_key[len(PREFIX):]
                    if target not in registered:self.assertIsNone(env['r13_case_hearing_quote'](target))

    def test_every_production_proof_call_key_has_metadata_and_no_extra_key_is_registered(self):
        names=('case-hearing.json','case-hearing-early.json','case-hearing-mid.json',
               'case-hearing-late.json','case-hearing-ending.json')
        files={'v111/'+name:json.loads(path.read_text()) for name in names
               if (path:=ROOT/'game/v111'/name).exists()}
        if not files:self.skipTest('표시 메타를 납품하지 않은 구 판은 기존 화면을 쓴다.')
        env,state=self.environment(files=files)
        data=env['R13_CASE_HEARING_DATA']
        metadata_keys={stage['key'] for case in data['cases']
                       for stage in env['r13_case_hearing_stages'](data,case)}
        proof_keys=set()
        pattern=re.compile(r'''^\s*call\s+r13_v111_proof\(\s*(['"])(.*?)\1\s*,''',re.M)
        for path in (ROOT/'game').rglob('*.rpy'):
            if 'qa_tests' in path.relative_to(ROOT/'game').parts:continue
            proof_keys.update(match.group(2) for match in pattern.finditer(path.read_text()))
        self.assertTrue(proof_keys)
        self.assertEqual(proof_keys,metadata_keys)


if __name__=='__main__':unittest.main()
