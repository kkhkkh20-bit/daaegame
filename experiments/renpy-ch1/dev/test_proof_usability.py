"""제시 문맥·출처 표시를 바꿔도 자료나 판정 상태를 수정하지 않는다."""
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'game/systems/room13_proof_usability.rpy').read_text()

class ProofUsability(unittest.TestCase):
    def make(self,source='MS14_D01_S03_L0002',kind='기록',person=None):
        state={'records':{'V111:E03':{'source':source,'place':'gate','day':1}}}
        ns={'store':SimpleNamespace(room13=state),'R13_BOOK_PURPOSE':{},
            'R13_NAMES':{'guard':'돌목'},'ROOM13':{'evidence_sources':{'V111:E03':person}},
            'R13_PLACES':{'gate':('마을 입구','winter')},
            'r13_catalog_title':lambda key:'방문 신청 원본',
            'r13_catalog_record':lambda key:{'kind':kind}}
        exec(textwrap.dedent(SOURCE.split('init 345 python:\n')[1]),ns)
        return ns,state

    def test_zero_one_many_keep_selection(self):
        ns,state=self.make()
        before=copy.deepcopy(state)
        for n in (0,1,4):
            chosen=['V111:E%02d'%i for i in range(n)]
            for purpose in ('proof','compare'):
                result=ns['r13_book_ui_copy'](purpose,chosen)
                self.assertEqual(result['stop'],'선택 마치기 · %d개'%n)
                self.assertIn('고른 자료 %d개'%n,result['note'])
                self.assertIn('아직 제출되지 않습니다',result['help'])
                self.assertNotIn('건넬지',result['help'])
                self.assertEqual(len(chosen),n)
        self.assertEqual(state,before)

    def test_contexts_describe_their_own_actions(self):
        ns,_=self.make(); f=ns['r13_book_ui_copy']
        self.assertEqual(f('compare')['title'],'자료 비교')
        self.assertEqual(f('proof')['title'],'근거 선택')
        self.assertEqual(f('use')['title'],'기록 꺼내기')
        self.assertIn('돌목',f(target='guard')['note'])
        self.assertIn('건넬지',f(target='guard')['help'])
        self.assertNotIn('건넬지',f(hearing=True)['help'])
        self.assertEqual(f()['stop'],'돌아가기')

    def test_chance_explanation_only_when_a_meeting_has_chances(self):
        ns,_=self.make(); f=ns['r13_proof_edit_help']
        self.assertIn('기회를 1회',f('남은 기회 5 / 5'))
        self.assertNotIn('1회',f(None))
        self.assertIn('선택한 근거 제출',f(None))

    def test_source_ids_are_preserved_but_not_displayed(self):
        for source in ('MS14_D01_S03_L0002','v111:gate','NW_D01_A01','option:gate:0','inspect_lamp','기록 MS14_D01_S03_L0002'):
            ns,state=self.make(source=source); before=copy.deepcopy(state)
            self.assertEqual(ns['r13_record_source_label']('V111:E03'),'마을 입구 · 방문 신청 원본')
            self.assertEqual(state,before)

    def test_human_source_and_testimony_stay_useful(self):
        ns,_=self.make(source='창구에서 확인한 신청서')
        self.assertEqual(ns['r13_record_source_label']('V111:E03'),'창구에서 확인한 신청서')
        ns,_=self.make(kind='증언',person='guard')
        self.assertEqual(ns['r13_record_source_label']('V111:E03'),'돌목에게 들은 말')
        self.assertEqual(ns['r13_record_source_label']('missing'),'이번 여정에서 확인한 자료')

    def test_gate_hint_does_not_name_required_material_or_location(self):
        data=json.loads((ROOT/'game/v111/newworld/d01.json').read_text())
        hint=data['replace']['MS14_D01_S03_L0027']['text']
        self.assertIn('기준',hint)
        for word in ('게시판','E04','입장 규칙','정답'):
            self.assertNotIn(word,hint)

if __name__=='__main__':unittest.main()
