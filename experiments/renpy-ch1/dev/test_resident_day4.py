"""4일 주민 발췌는 현재 들은 말 뒤에 붙고 생사·목격·자료 상태를 바꾸지 않는다."""
import ast
import copy
import itertools
import json
import re
import unittest

from test_newworld_text import Layer, ROOT


MATCHING=ROOT/'docs/design/resident-reactions-day456-20261106/day4_매칭.json'


class ResidentDay4(Layer):
    def label(self,name):
        source=(ROOT/'game/room13_v111_days45.rpy').read_text()
        return re.search(r'^label '+name+r':\n(.*?)(?=^label |\Z)',source,re.M|re.S).group(1)

    def rows(self,env,label):
        result=[]
        for found in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)',self.label(label)):
            result.extend(env['r13_v111_lines'](ast.literal_eval(found.group(1))))
        return result

    def row_text(self,entry,prefix):
        data=json.loads((ROOT/'game/v111/newworld/d04.json').read_text())
        return [r['text'] for r in data['after'][entry] if r['id'].startswith(prefix)]

    def test_excerpt_keeps_all_day4_life_attempt_and_waiting_place_branches(self):
        for alive,bound,cold in itertools.product((False,True),repeat=3):
            with self.subTest(piko_alive=alive,lamp_bound2=bound,bami_cold4=cold):
                env=self.load()
                self.state.room13.update(day=4,period=2,location='gate')
                for key,value in [('piko_alive',alive),('lamp_bound2',bound),('bami_cold4',cold)]:
                    env['r13_v111_set'](key,value)
                before=copy.deepcopy(self.state.room13)
                for anchor,prefix in [('MS14_D04_S03_L0007','NW_RR4_G'),('MS14_D04_S04_L0027','NW_RR4_B')]:
                    rows=env['r13_v111_lines']([anchor])
                    texts=[r[1] for r in rows]
                    self.assertEqual([t for t in texts if t in self.row_text(anchor,prefix)],self.row_text(anchor,prefix))
                    self.assertNotIn('resident_piko',[r[0] for r in rows])
                self.assertEqual(before,self.state.room13,'대사 조회가 자료·생사·시간·보고를 완료하지 않는다')
                self.assertFalse(env['r13_v111_owned']('E20'))
                self.assertFalse(env['r13_v111_owned']('E21'))
                # 기존 냉기 분기의 위치 진술을 공통 발췌로 덮어쓰지 않는다.
                testimony=env['r13_v111_lines'](['MS14_D04_S04_L0008'])[0][1]
                self.assertIn('울타리 옆' if cold else '저 처마',testimony)

    def test_guard_seat_follows_injury_and_precedes_identity_questions(self):
        env=self.load()
        rows=self.rows(env,'r13_v111_bite4');texts=[r[1] for r in rows]
        injury=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D04_S03_L0005')
        question=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D04_S03_L0008')
        added=[texts.index(t) for t in self.row_text('MS14_D04_S03_L0007','NW_RR4_G')]
        self.assertTrue(all(injury<i<question for i in added))
        self.assertTrue(all(rows[i][0] in ('guard','dad',None) for i in added))
        self.assertFalse(env['r13_v111_owned']('E20'))
        env['r13_v111_commit']('MS14_D04_S03_L0003')
        self.assertTrue(env['r13_v111_owned']('E20'),'최초 진술의 획득은 원래 커밋만 맡는다')
        self.assertIn('키는 모른다',env['R13_V111']['evidence']['E20']['variants']['observed'])

    def test_bami_request_follows_admission_and_does_not_finish_public_correction(self):
        env=self.load();rows=self.rows(env,'r13_v111_bami_night4');texts=[r[1] for r in rows]
        admission=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D04_S04_L0027')
        public=next(i for i,r in enumerate(rows) if r[2].get('line_id')=='MS14_D04_S04_L0028')
        added=[texts.index(t) for t in self.row_text('MS14_D04_S04_L0027','NW_RR4_B')]
        self.assertTrue(all(admission<i<public for i in added))
        self.assertEqual([rows[i][0] for i in added],[None,'bami','resident_kongi'])
        self.assertFalse(env['r13_v111_value']('rumor_not_eyewitness'))
        env['r13_v111_commit']('MS14_D04_S04_L0018')
        self.assertTrue(env['r13_v111_owned']('E21'))
        self.assertIn('얼굴과 키는 모른다',env['R13_V111']['evidence']['E21']['variants']['observed'])
        env['r13_v111_commit']('MS14_D04_S04_L0032')
        self.assertTrue(env['r13_v111_value']('rumor_not_eyewitness'))

    def test_manuscript_matching_separates_whole_scene_from_actual_excerpt(self):
        matching=json.loads(MATCHING.read_text())
        data=json.loads((ROOT/'game/v111/newworld/d04.json').read_text())
        self.assertEqual([e['id'] for e in matching],['RR4_01','RR4_02'])
        for entry in matching:
            self.assertEqual(entry['day'],4)
            self.assertTrue(entry['known'] and entry['unknown'])
            self.assertEqual(entry['branch']['piko_alive'],[True,False])
            body=self.label(entry['label'])
            self.assertIn(entry['anchor'],body)
            excerpt=entry['game_excerpt']
            self.assertIn(excerpt['anchor'],body)
            self.assertNotEqual(entry['anchor'],excerpt['anchor'],'원고 전체와 짧은 발췌의 공개 하한은 다르다')
            rows=data[excerpt['position']][excerpt['anchor']]
            self.assertEqual([r['id'] for r in rows],entry['game_added_line_ids'])
            self.assertFalse(any(set(r)&{'operations','effects','acquire','set','when'} for r in rows))


if __name__=='__main__':unittest.main()
