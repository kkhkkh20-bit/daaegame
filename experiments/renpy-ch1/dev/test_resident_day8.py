"""8일 진료·생존·봉투 인수의 주민 행동은 기존 갈래와 정보 범위를 보존한다."""
import ast
import copy
import json
import re
import unittest

from test_newworld_text import Layer, ROOT


class ResidentDay8(Layer):
    def test_new_owl_and_child_exchange_does_not_survive_the_owl(self):
        env=self.load()
        env['r13_v111_set']('OWL_ALIVE',False)
        before=copy.deepcopy(self.state.room13)
        rows=env['r13_v111_lines'](['MS14_D08_P01_L0014'])
        self.assertFalse(any('내가 들고 있을 테니' in r[1] or '그럼 제가 이쪽으로' in r[1] for r in rows))
        self.assertEqual(before,self.state.room13)

    def label(self,name,filename='room13_v111_days610.rpy'):
        source=(ROOT/'game'/filename).read_text()
        return re.search(r'^label '+name+r'(?:\([^\n]*\))?:\n(.*?)(?=^label |\Z)',source,re.M|re.S).group(1)

    def lines(self,env,label):
        rows=[]
        for m in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)',self.label(label)):
            rows+=env['r13_v111_lines'](ast.literal_eval(m.group(1)))
        return rows

    def test_custody_exam_allows_sleeve_action_after_existing_bruise_record_only(self):
        env=self.load()
        env['r13_v111_set']('route7','murder')
        env['r13_v111_set']('OWL_ALIVE',False)
        env['r13_v111_set']('DARAM_DETAINED',True)
        before=copy.deepcopy(self.state.room13)
        rows=env['r13_v111_lines'](['MS14_D08_S01_L0015','MS14_D08_S01_L0016'])
        original=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D08_S01_L0015')
        pause=next(i for i,r in enumerate(rows) if '편히 앉은 다음' in r[1])
        next_statement=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D08_S01_L0016')
        self.assertLess(original,pause)
        self.assertLess(pause,next_statement)
        self.assertEqual(before,self.state.room13)
        self.assertTrue(env['r13_v111_value']('DARAM_DETAINED'))
        self.assertFalse(env['r13_v111_value']('OWL_ALIVE'))
        self.assertFalse(env['r13_v111_owned']('E08_CHILD_ACCOUNT'))
        env['r13_v111_commit']('MS14_D08_S01_L0025')
        self.assertTrue(env['r13_v111_owned']('E08_CHILD_ACCOUNT'))
        self.assertTrue(env['r13_v111_value']('DARAM_DETAINED'))

    def test_recovered_owl_holds_paper_without_changing_recovery_or_missing_records(self):
        env=self.load()
        for prevention in ('B','promise','repair'):
            with self.subTest(prevention=prevention):
                env['r13_v111_set']('route7','prevented')
                env['r13_v111_set']('prevention',prevention)
                env['r13_v111_set']('OWL_ALIVE',True)
                env['r13_v111_set']('DARAM_DETAINED',False)
                before=copy.deepcopy(self.state.room13)
                rows=self.lines(env,'r13_v111_care8')
                texts=[r[1] for r in rows]
                self.assertTrue(any('내가 들고 있을 테니' in t for t in texts))
                self.assertTrue(any('무리하시면 안 돼요' in t for t in texts))
                self.assertFalse(any('숨진' in t or '구금' in t for t in texts))
                self.assertEqual(before,self.state.room13)
                env['r13_v111_commit']('MS14_D08_P01_L0017')
                self.assertEqual(env['r13_v111_value']('E08_prevention_experience'),'함께_의료진_왕복')
                self.assertTrue(env['r13_v111_value']('OWL_ALIVE'))
                self.assertFalse(env['r13_v111_value']('DARAM_DETAINED'))
        # 종이 누락과 명단 위협은 여전히 다음 원래 라벨에서 이어진다.
        missing=self.label('r13_v111_missing_pages8')
        self.assertIn("r13_nw_block('neoul_list8')",missing)
        self.assertIn("r13_v111_commit('MS14_D08_P01_L0026')",missing)

    def test_stone_prevention_does_not_replay_medical_care_or_new_owl_exchange(self):
        env=self.load()
        env['r13_v111_set']('prevention','stone')
        env['r13_v111_set']('OWL_ALIVE',True)
        branch=self.label('r13_v111_prevention_story8')
        self.assertIn("if r13_v111_value('prevention')=='stone':",branch)
        self.assertIn('jump r13_v111_owl_well8',branch)
        stone=self.label('r13_v111_owl_well8','room13_v111_owl_prevent.rpy')
        self.assertIn("r13_nw_block('owl_well8')",stone)
        self.assertNotIn('r13_v111_care8',stone)
        before=copy.deepcopy(self.state.room13)
        rows=env['r13_nw_block']('owl_well8')
        self.assertFalse(any(r[0]=='resident_seori' for r in rows))
        self.assertFalse(any('내가 들고 있을 테니' in r[1] for r in rows))
        self.assertEqual(before,self.state.room13)

    def test_actual_escort_receipt_keeps_secret_unshared_with_child_absent_on_both_routes(self):
        env=self.load()
        escort=self.label('r13_v111_escort_done8')
        self.assertLess(escort.index('public_road_escort_completed'),escort.index("r13_v111_lines(['MS14_D08_S04_L0031'])"))
        for route in ('murder','prevented'):
            with self.subTest(route=route):
                env['r13_v111_set']('route7',route)
                env['r13_v111_set']('OWL_ALIVE',route!='murder')
                env['r13_v111_set']('DARAM_DETAINED',route=='murder')
                before=copy.deepcopy(self.state.room13)
                rows=self.lines(env,'r13_v111_escort_done8')
                new=[r for r in rows if '봉투는 잘 받으신' in r[1] or '제가 잘 챙기겠습니다' in r[1] or '안주머니를 손바닥으로' in r[1]]
                self.assertEqual(len(new),3)
                self.assertFalse(any(r[0]=='daram' for r in new))
                self.assertFalse(any('6일' in r[1] or '발소리' in r[1] or '부엉이' in r[1] for r in new))
                self.assertEqual(before,self.state.room13)
                env['r13_v111_commit']('MS14_D08_S04_L0033')
                self.assertIs(env['r13_v111_value']('mother_secret_shared'),False)
                self.assertEqual(env['r13_v111_value']('mother_location'),'unknown')
                self.assertTrue(env['r13_v111_owned']('E08_RECENT_LETTER'))
                self.assertEqual(env['r13_v111_value']('OWL_ALIVE'),route!='murder')

    def test_three_manuscripts_have_branch_headers_and_nine_traceable_game_lines(self):
        folder=ROOT/'docs/design/resident-reactions-day789-20261106'
        data=json.loads((folder/'day8_매칭.json').read_text())
        self.assertEqual(data['day'],8)
        self.assertEqual([s['id'] for s in data['scenes']],['RR8_01','RR8_02','RR8_03'])
        manuscript=(folder/'day8_원고.md').read_text()
        parts=re.findall(r'^## (0[456])\. (.*?)(?=^## |\Z)',manuscript,re.M|re.S)
        self.assertEqual([n for n,_ in parts],['04','05','06'])
        for _,body in parts:
            self.assertTrue(800<=len(body)<=1300,len(body))
            self.assertIn('8일',body.splitlines()[2])
            self.assertNotIn('MS14_',body)
        overlay=json.loads((ROOT/'game/v111/newworld/d08.json').read_text())
        rows=[r for section in ('before','after','blocks') for rs in overlay[section].values() for r in rs]
        by_id={r['id']:r for r in rows}
        ids=[key for s in data['scenes'] for key in s['game_added_ids']]
        self.assertEqual(len(ids),9)
        self.assertEqual(len(set(ids)),9)
        for scene in data['scenes']:
            self.assertEqual(set(scene['scene_extent']),{'full_manuscript','short_extract'})
            for key in scene['game_added_ids']:
                self.assertIn(key,by_id)
                self.assertNotEqual(by_id[key].get('kind'),'thought','주민 독백은 게임에 삽입하지 않는다')


if __name__=='__main__':unittest.main()
