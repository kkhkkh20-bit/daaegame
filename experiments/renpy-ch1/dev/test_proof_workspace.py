"""2026-10-27 UX 인계서 D01~D03: 자료 대조 통합 화면의 표시 문맥 표와 순수 선택 계산.

systems/room13_proof_workspace.rpy 의 첫 블록(init 350)을 Ren'Py 없이 실행한다.
확인하는 것: 정답 함수를 쓰지 않는다 · 목록은 보유 자료만 · 탭을 바꿔도 선택이 남는다 ·
compare 는 둘까지(셋째는 교체 대기) · 빈 제출 불가 · 문맥 표에 정답 ID 가 없다."""
import re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'game'/'systems'/'room13_proof_workspace.rpy'

def load_pure():
    src=SRC.read_text(encoding='utf-8')
    body=src.split('init 350 python:',1)[1].split('\n# store 에 기대는',1)[0]
    code='\n'.join(line[4:] if line.startswith('    ') else line for line in body.splitlines())
    ns={}
    exec(compile(code,str(SRC),'exec'),ns)
    return ns

class ProofWorkspacePure(unittest.TestCase):
    def setUp(self):
        self.ns=load_pure()

    def test_context_table_covers_pilot_issues_only(self):
        ctx=self.ns['R13_PW_CONTEXT']
        self.assertEqual(set(ctx),{'함께 들어갈 근거를 고른다','두 편지를 나란히 본다','불이 시작된 곳과 진술을 대조한다'})
        self.assertEqual(ctx['두 편지를 나란히 본다']['mode'],'compare')
        self.assertEqual(ctx['함께 들어갈 근거를 고른다']['speaker'],'돌목')
        self.assertEqual(ctx['불이 시작된 곳과 진술을 대조한다']['quote_when'],('value','bori_nubi_door_witness_heard'))
        self.assertIsNone(self.ns['r13_pw_context']('구리선과 수선 출처를 대조한다'))
        # 정답 ID·미획득 자료는 표시 데이터에 없다(인계서 4장·13장).
        for spec in ctx.values():
            for field in ('speaker','quote'):
                self.assertNotRegex(str(spec.get(field) or ''),r'V111:|E0\d|E06_FIRE')
            self.assertNotIn('correct',spec)

    def test_quote_visible_follows_flag_or_value(self):
        vis=self.ns['r13_pw_quote_visible'];ctx=self.ns['R13_PW_CONTEXT']
        fire=ctx['불이 시작된 곳과 진술을 대조한다']
        self.assertFalse(vis(fire,lambda f:False,lambda k:None))
        self.assertFalse(vis(fire,lambda f:True,lambda k:False))
        self.assertTrue(vis(fire,lambda f:False,lambda k:True))
        gate=ctx['함께 들어갈 근거를 고른다']
        self.assertTrue(vis(gate,lambda f:f=='v111:entered:MS14_D01_S02',lambda k:None))
        self.assertFalse(vis(gate,lambda f:False,lambda k:True))
        self.assertTrue(vis(ctx['두 편지를 나란히 본다'],lambda f:False,lambda k:None))

    def test_no_answer_function_in_module(self):
        src=SRC.read_text(encoding='utf-8')
        for name in ('r13_v111_proof_accepts','R13_PROOF_ALTERNATES','R13_PROOF_EXTRAS','r13_v111_proof_kept','r13_v111_proof_sets','r13_nw_retry'):
            self.assertNotIn(name+'(',src)
            self.assertNotIn(name+'.',src)
            self.assertNotIn(name+'[',src)

    def test_order_is_latest_first_and_stable(self):
        order=self.ns['r13_pw_order']
        keys=['V111:E01','V111:E02','V111:E03','V111:E07']
        days={'V111:E01':1,'V111:E02':1,'V111:E03':1,'V111:E07':2}
        self.assertEqual(order(keys,days),['V111:E07','V111:E01','V111:E02','V111:E03'])
        self.assertEqual(order(keys,{}),keys)
        self.assertEqual(order(['a','b'],{'a':3}),['a','b'])
        self.assertEqual(order(['a','b'],{'b':3}),['b','a'])

    def test_toggle_uses_owned_only(self):
        toggle=self.ns['r13_pw_toggle']
        owned=['V111:E01','V111:E02']
        self.assertEqual(toggle([],'V111:E99',owned,'proof'),([],None))
        self.assertEqual(toggle([],'V111:E01',owned,'proof'),(['V111:E01'],None))
        self.assertEqual(toggle(['V111:E01'],'V111:E01',owned,'proof'),([],None))
        # 일반 proof 는 개수 제한이 없다.
        chosen=[]
        for k in ('V111:E01','V111:E02'):chosen,_=toggle(chosen,k,owned,'proof')
        self.assertEqual(chosen,['V111:E01','V111:E02'])

    def test_compare_limits_to_two_and_asks_which_to_replace(self):
        toggle=self.ns['r13_pw_toggle'];replace=self.ns['r13_pw_replace']
        owned=['V111:E01','V111:E02','V111:E06']
        chosen,pending=toggle(['V111:E01','V111:E06'],'V111:E02',owned,'compare')
        self.assertEqual(chosen,['V111:E01','V111:E06'])   # 처음 것을 자동으로 버리지 않는다
        self.assertEqual(pending,'V111:E02')
        self.assertEqual(replace(chosen,'V111:E01',pending,owned),['V111:E02','V111:E06'])
        self.assertEqual(replace(chosen,'V111:E09',pending,owned),chosen)
        self.assertEqual(replace(chosen,'V111:E01','V111:E99',owned),chosen)
        # 둘 중 하나를 끄는 것은 compare 에서도 그대로 된다.
        self.assertEqual(toggle(chosen,'V111:E06',owned,'compare'),(['V111:E01'],None))

    def test_submit_requires_selection(self):
        ok=self.ns['r13_pw_submit_ok']
        self.assertFalse(ok([],'proof'));self.assertTrue(ok(['a'],'proof'));self.assertTrue(ok(['a','b','c'],'proof'))
        self.assertFalse(ok([],'compare'));self.assertFalse(ok(['a'],'compare'));self.assertTrue(ok(['a','b'],'compare'));self.assertFalse(ok(['a','b','c'],'compare'))

    def test_reading_pair_is_separate_from_selection(self):
        fill=self.ns['r13_pw_pair_fill'];live=self.ns['r13_pw_pair_live'];from_chosen=self.ns['r13_pw_pair_from_chosen']
        chosen=['a','b','c']
        pair=fill(('a',None),'c')
        self.assertEqual(pair,('a','c'))
        self.assertEqual(chosen,['a','b','c'])      # 읽기 쌍이 제출 묶음을 건드리지 않는다(T09)
        self.assertEqual(fill(('a','c'),'b'),('a','c'))
        self.assertEqual(live(('a','z'),['a','b']),('a',None))
        self.assertIsNone(live(('y','z'),['a','b']))
        self.assertEqual(from_chosen(['a','b'],'compare'),('a','b'))
        self.assertIsNone(from_chosen(['a'],'compare'));self.assertIsNone(from_chosen(['a','b'],'proof'))

    def test_selection_survives_tab_change(self):
        # 탭은 화면 변수고 선택은 room13["arguments"] 에 있다 — 순수 계산에는 탭이 아예 들어가지 않는다.
        import inspect
        for name in ('r13_pw_toggle','r13_pw_replace','r13_pw_remove','r13_pw_submit_ok'):
            self.assertNotIn('tab',inspect.signature(self.ns[name]).parameters)

class ProofWorkspacePages(unittest.TestCase):
    """2026-10-27: 목록은 숨은 스크롤이 아니라 보이는 쪽으로 나눈다. 자료가 모두 어느 쪽엔가 한 번씩 들어간다."""
    def setUp(self):
        self.pages=load_pure()['r13_pw_pages']
    def test_seven_cards_on_pc_make_visible_pages(self):
        keys=['V111:E%02d'%i for i in (1,2,3,4,5,6,30)]
        pages=self.pages([(None,keys)],1,332,72,28,8,36)
        self.assertGreater(len(pages),1)
        self.assertEqual([k for page in pages for kind,v in page for k in v],keys)
        for page in pages:
            used=sum(72 for kind,v in page)+8*(len(page)-1)
            self.assertLessEqual(used,332-36-8)
    def test_short_list_is_one_page_without_pager(self):
        pages=self.pages([(None,['a','b','c','d'])],1,332,72,28,8,36)
        self.assertEqual(len(pages),1);self.assertEqual(pages[0],[('cards',['a']),('cards',['b']),('cards',['c']),('cards',['d'])])
    def test_headers_count_and_two_columns(self):
        pages=self.pages([('사건 하나',['a','b','c']),('사건 둘',['d'])],2,200,88,28,8,48)
        self.assertEqual(pages[0][0],('header','사건 하나'));self.assertEqual(pages[0][1],('cards',['a','b']))
        self.assertEqual([k for page in pages for kind,v in page if kind=='cards' for k in v],['a','b','c','d'])
    def test_empty_sections_give_one_empty_page(self):
        self.assertEqual(self.pages([(None,[])],1,332,72,28,8,36),[[]])

if __name__=='__main__':unittest.main()
