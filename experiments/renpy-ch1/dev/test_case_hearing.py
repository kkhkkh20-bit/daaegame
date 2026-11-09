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


class CaseHearing(unittest.TestCase):
    def environment(self,data=None,values=None,room=True,available=True):
        state=SimpleNamespace(room13=dict(
            day=3,period=1,location='workshop',evidence=['V111:E11','V111:E13'],
            flags=['observed:lamp'],arguments={'v111:수리':['V111:E11']},
            v111=dict(gate='trial_repair',values=dict(values or {},**{'tries:lamp':2,'elapsed_minutes':75}))))
        if not room:state.room13=None
        metadata=fixture() if data is None else data
        renpy=SimpleNamespace(loadable=lambda path:available,
                              file=lambda path:io.BytesIO(json.dumps(metadata,ensure_ascii=False).encode()))
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

    def test_builtin_json_lists_remain_valid_when_renpy_rebinds_the_list_name(self):
        class RevertableListLike(list):
            pass
        env,state=self.environment()
        env['list']=RevertableListLike
        stages=env['R13_CASE_HEARING_DATA']['cases']['lamp']['stages']
        self.assertIs(type(stages),list)
        self.assertNotIsInstance(stages,RevertableListLike)
        self.assertIsNotNone(env['r13_case_hearing_spec']('수리'))
        self.assertTrue(env['r13_case_hearing_heard'](['neoul','실제로 들은 말',dict(line_id='RID_REPAIR')]))
        self.assertEqual([row['target'] for row in env['r13_case_hearing_rows']('수리')],['RID_REPAIR'])
        self.assertEqual(env['r13_case_hearing_press_block']('수리','RID_REPAIR'),'press_repair')
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
            dict(key='수리',target='RID_REPAIR',title='수리 뒤의 돌',speaker='resident_siluk',text=text)])

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
                   lambda stages:stages[0].update(press_block=[])]
        for mutate in mutations:
            data=fixture();mutate(data['cases']['lamp']['stages'])
            env,state=self.environment(data=data)
            self.assertIsNone(env['r13_case_hearing_spec']('수리'))
            self.assertEqual(env['r13_case_hearing_rows']('수리'),[])
            self.assertFalse(self.hear(env,'RID_REPAIR'))

    def test_shipped_targets_point_to_real_speech_and_contain_only_display_metadata(self):
        path=ROOT/'game/v111/case-hearing.json'
        if not path.exists():self.skipTest('표시 메타가 없으면 런타임은 기존 화면으로 돌아간다.')
        data=json.loads(path.read_text())
        env,state=self.environment(data=data)
        records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
        spoken={key:row.get('speaker') for key,row in records.items() if row.get('speaker')}
        for source in (ROOT/'game/v111/newworld').glob('*.json'):
            part=json.loads(source.read_text())
            for group in ('before','after','blocks'):
                for rows in part.get(group,{}).values():
                    for row in rows:
                        if row.get('speaker') and row.get('id'):spoken[row['id']]=row['speaker']
        for case in ('lamp','lamp_attempt'):
            stages=env['r13_case_hearing_stages'](data,case)
            self.assertEqual(len(stages),len(data['cases'][case]['stages']))
            self.assertTrue(stages)
            for stage in stages:
                for target in stage['line_ids']:
                    self.assertIn(target,spoken)
                    self.assertEqual(spoken[target],stage['speaker'])


if __name__=='__main__':unittest.main()
