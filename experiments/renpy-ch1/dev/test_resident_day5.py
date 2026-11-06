"""5일 주민 발췌는 실제 증언·승패 경로와 기존 자료·명단 상태를 보존한다."""
import ast
import copy
import json
import re
import textwrap
import unittest

from test_newworld_text import Layer, ROOT


class ResidentDay5(Layer):
    def label(self, name):
        source=(ROOT/'game/room13_v111_days45.rpy').read_text()
        return re.search(r'^label '+name+r':\n(.*?)(?=^label |\Z)',source,re.M|re.S).group(1)

    def lines(self, env, label):
        rows=[]
        for m in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)',self.label(label)):
            rows+=env['r13_v111_lines'](ast.literal_eval(m.group(1)))
        return rows

    def test_nabi_leaves_after_request_without_granting_an_alibi_or_testifying_on_loss(self):
        env=self.load()
        before=copy.deepcopy(self.state.room13)
        rows=env['r13_nw_block']('nabi_confirm5')
        texts=[r[1] for r in rows]
        self.assertTrue(any('빈 물통을 문 안쪽에 세운다' in t for t in texts))
        self.assertTrue(any('제가 본 건 제가 가서 말할게요' in t for t in texts))
        self.assertEqual(self.state.room13,before)
        # 증언자 합류와 실제 식당 알리바이 발언은 기존 성공 라벨에서만 한다.
        win=self.label('r13_v111_bami_clear5')
        self.assertLess(win.index("r13_v111_join(['nabi'])"),win.index("r13_nw_block('nabi_hearing5')"))
        self.assertNotIn("r13_nw_block('nabi_hearing5')",self.label('r13_v111_wrong5'))
        hearing=env['r13_nw_block']('nabi_hearing5')
        self.assertTrue(any('그 시각엔 네로 씨가 제 물통을' in r[1] for r in hearing))

    def test_bami_takes_paper_only_after_existing_name_check_and_original_commit(self):
        env=self.load()
        env['r13_v111_set']('meeting:gate_post','win')
        before=copy.deepcopy(self.state.room13)
        rows=self.lines(env,'r13_v111_bami_clear5')
        texts=[r[1] for r in rows]
        name=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D05_S03_L0036')
        fold=next(i for i,t in enumerate(texts) if '종이 접어 줘요' in t)
        pocket=next(i for i,t in enumerate(texts) if '작아진 종이를 받아 외투 안쪽' in t)
        self.assertLess(name,fold)
        self.assertLess(fold,pocket)
        self.assertEqual(before,self.state.room13,'종이 동작으로 보증·혐의 판정을 적용하지 않는다')
        self.assertFalse(env['r13_v111_owned']('E26'))
        env['r13_v111_commit']('MS14_D05_S03_L0037')
        self.assertTrue(env['r13_v111_owned']('E25'))
        self.assertTrue(env['r13_v111_owned']('E26'))
        self.assertEqual(env['r13_v111_value']('bami_status'),'cleared')
        self.assertEqual(env['r13_v111_value']('musoe_care'),'nero_badugi_night_rotation')

    def test_bami_demands_record_on_loss_but_remains_listed_without_a_guarantee(self):
        env=self.load()
        # 공통 오프라인 층 로더는 init319만 읽으므로 부분 제출 판별의 실제 선행 함수를 함께 적재한다.
        source=(ROOT/'game/room13_v111_newworld_text.rpy').read_text()
        helper=re.search(r'^init -1 python:\n((?:[ \t].*\n|\n)*)',source,re.M).group(1)
        exec(textwrap.dedent(helper),env)
        env['r13_nw_tries_left']=lambda meeting:3
        for outcome in (None,'win','lose'):
            with self.subTest(outcome=outcome):
                env['r13_v111_set']('meeting:gate_post',outcome)
                env['r13_v111_set']('listed:bami',outcome=='lose')
                env['r13_v111_set']('bami_status','listed' if outcome=='lose' else 'temporarily_with_badugi')
                before=copy.deepcopy(self.state.room13)
                rows=self.lines(env,'r13_v111_wrong5')
                texts=[r[1] for r in rows]
                self.assertEqual(any('내 말도 거기 적어요' in t for t in texts),outcome=='lose')
                self.assertFalse(any('종이 접어 줘요' in t for t in texts))
                self.assertEqual(before,self.state.room13)
                self.assertFalse(env['r13_v111_owned']('E26'))
        self.assertTrue(env['r13_v111_value']('listed:bami'))
        self.assertEqual(env['r13_v111_value']('bami_status'),'listed')

    def test_manuscripts_and_matching_keep_three_separate_scenes_and_exact_sources(self):
        folder=ROOT/'docs/design/resident-reactions-day456-20261106'
        matching=json.loads((folder/'day5_매칭.json').read_text())
        self.assertEqual([s['id'] for s in matching['scenes']],['RR5_01','RR5_02','RR5_03'])
        manuscript=(folder/'day5_원고.md').read_text()
        parts=re.findall(r'^## (0[345])\. (.*?)(?=^## |\Z)',manuscript,re.M|re.S)
        self.assertEqual([n for n,_ in parts],['03','04','05'])
        for _,body in parts:
            self.assertTrue(700<=len(body)<=1200,len(body))
            self.assertNotIn('MS14_',body)
            self.assertNotIn('NW_',body)
        data=json.loads((ROOT/'game/v111/newworld/d05.json').read_text())
        rows=[r for section in ('before','after','blocks') for rs in data[section].values() for r in rs]
        by_id={r['id']:r for r in rows}
        for scene in matching['scenes']:
            for key in scene['game_added_ids']+scene['game_revised_ids']:
                self.assertIn(key,by_id)
        self.assertEqual(by_id['NW_D05_S03_C03']['when'],'gate_post_lose')
        # 주민 반응은 아직 가족도 읽지 않은 엄마의 첫 답장을 앞당겨 말하지 않는다.
        selected=[by_id[k]['text'] for s in matching['scenes'] for k in s['game_added_ids']+s['game_revised_ids']]
        for text in selected:
            self.assertNotIn('편지',text)
            self.assertNotIn('마차',text)

    def test_letter_privacy_departure_never_changes_lives_or_grants_contact_knowledge(self):
        env=self.load()
        before=copy.deepcopy(self.state.room13)
        rows=env['r13_nw_block']('warning_private5')
        self.assertEqual(len(rows),2)
        self.assertEqual(rows[0][0],'resident_lamplighter')
        self.assertIsNone(rows[1][0])
        self.assertIn('초롱이 자리를 뜬 뒤',rows[1][1])
        self.assertEqual(before,self.state.room13)
        self.assertIsNot(env['r13_v111_value']('mother_first_contact_read5'),True)


if __name__=='__main__':unittest.main()
