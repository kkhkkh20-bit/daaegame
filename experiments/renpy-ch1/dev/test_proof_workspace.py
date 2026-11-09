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

    def test_context_table_covers_approved_issues_only(self):
        ctx=self.ns['R13_PW_CONTEXT']
        self.assertEqual(set(ctx),{'함께 들어갈 근거를 고른다','두 편지를 나란히 본다','불이 시작된 곳과 진술을 대조한다','측정 종료와 점검 기록을 대조한다','수리와 반출을 가릴 자료를 낸다','돌과 매입 기록을 낸다','바깥 걸쇠 주장과 발견 위치를 대조한다','마지막 점검과 인수한 돌을 연결한다','수리 뒤 새로 생긴 파손을 가린다','남아 있는 돌과 칼의 사용을 연결한다','밤이 혐의의 근거를 확인한다','두 편지의 초대를 대조한다','불의 원인과 빈 창고 진압을 구분한다','불의 원인과 아이 구조를 구분한다'})
        self.assertEqual(ctx['두 편지를 나란히 본다']['mode'],'compare')
        self.assertEqual(ctx['함께 들어갈 근거를 고른다']['speaker'],'돌목')
        self.assertEqual(ctx['불이 시작된 곳과 진술을 대조한다']['quote_when'],('value','fire_lamp_defense_heard'))
        self.assertIsNone(self.ns['r13_pw_context']('구리선과 수선 출처를 대조한다'))
        # 정답 ID·미획득 자료는 표시 데이터에 없다(인계서 4장·13장).
        for spec in ctx.values():
            for field in ('speaker','quote'):
                self.assertNotRegex(str(spec.get(field) or ''),r'V111:|E0\d|E06_FIRE')
            self.assertNotIn('correct',spec)

    def test_part_one_defaults_and_later_metadata_cover_actual_proof_calls(self):
        paths=['room13_v111_days123.rpy','room13_v111_days45.rpy','room13_lamp_attempt.rpy']
        early='\n'.join((ROOT/'game'/p).read_text() for p in paths)
        middle=(ROOT/'game/room13_v111_days610.rpy').read_text()
        day67,later=middle.split('label r13_v111_day8:',1)
        extract=lambda text:set(re.findall(r'call r13_v111_proof\([\'\"]([^\'\"]+)',text))
        self.assertEqual(extract(early+day67),set(self.ns['R13_PW_CONTEXT']))
        later+='\n'+(ROOT/'game/room13_v111_days1114.rpy').read_text()
        self.assertTrue(extract(later))
        self.assertTrue(extract(later).isdisjoint(self.ns['R13_PW_CONTEXT']))
        import json
        registered={stage['key'] for path in (ROOT/'game/v111').glob('case-hearing*.json') for case in json.loads(path.read_text())['cases'].values() for stage in case['stages']}
        self.assertTrue(extract(later)<=registered)
        # 5일 두 편지는 읽기 쌍과 제출 선택을 분리하는 기존 compare 규칙을 쓴다.
        self.assertEqual(self.ns['R13_PW_CONTEXT']['두 편지의 초대를 대조한다']['mode'],'compare')
        for key in extract((ROOT/'game/room13_lamp_attempt.rpy').read_text())|{'밤이 혐의의 근거를 확인한다','두 편지의 초대를 대조한다','불의 원인과 빈 창고 진압을 구분한다','불의 원인과 아이 구조를 구분한다'}:
            self.assertIsNone(self.ns['R13_PW_CONTEXT'][key]['quote'])
            self.assertIsNone(self.ns['R13_PW_CONTEXT'][key]['speaker'])

    def test_day3_quotes_only_repeat_already_spoken_lines(self):
        import json
        overlay=json.loads((ROOT/'game/v111/newworld/d03.json').read_text())['replace']
        records=json.loads((ROOT/'game/v111/records.json').read_text())['records']
        pairs={'수리와 반출을 가릴 자료를 낸다':'MS14_D03_S05_L0002','돌과 매입 기록을 낸다':'MS14_D03_S05_L0005','바깥 걸쇠 주장과 발견 위치를 대조한다':'MS14_D03_S05_L0017','마지막 점검과 인수한 돌을 연결한다':'MS14_D03_S05_L0025'}
        clean=lambda text:' '.join(re.sub(r'\{[^}]*\}','',text).split())
        for key,line in pairs.items():
            spec=self.ns['R13_PW_CONTEXT'][key]
            rows=overlay[line] if isinstance(overlay[line],list) else [overlay[line]]
            for row in rows:
                self.assertIn(clean(spec['quote']),clean(row['text']))
                self.assertEqual(spec['speaker'],row.get('speaker',records[line]['speaker']))
            self.assertEqual(spec['quote_when'],('flag','v111:entered:MS14_D03_S05'))
        self.assertIsNone(self.ns['R13_PW_CONTEXT']['측정 종료와 점검 기록을 대조한다']['quote'])

    def test_fire_quote_was_spoken_before_evidence_comparison(self):
        import json
        quote=self.ns['R13_PW_CONTEXT']['불이 시작된 곳과 진술을 대조한다']['quote']
        rows=json.loads((ROOT/'game/v111/newworld/d07.json').read_text())['blocks']['nubi_lamp_defense7']
        self.assertIn(quote, [' '.join(r['text'].split()) for r in rows])

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

    def test_gate_acknowledgment_updates_only_its_quote_without_leaking_to_new_games(self):
        import json
        key='함께 들어갈 근거를 고른다'
        context=self.ns['r13_pw_context']
        original=dict(context(key))
        spoken=json.loads((ROOT/'game/v111/newworld/d01.json').read_text())['replace']['MS14_D01_S03_L0010']['text']
        acknowledged=context(key,gate_application_acknowledged=True)
        self.assertEqual(acknowledged['quote'],spoken)
        self.assertNotEqual(acknowledged['quote'],original['quote'])
        self.assertEqual(context(key),original)
        self.assertEqual(context('두 편지를 나란히 본다',True),context('두 편지를 나란히 본다'))
        self.assertEqual({k:v for k,v in acknowledged.items() if k!='quote'},
                         {k:v for k,v in original.items() if k!='quote'})

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

    def test_first_letter_comparison_can_review_even_without_legacy_return_argument(self):
        target=self.ns['r13_pw_review_target']
        self.assertEqual(target('두 편지를 나란히 본다',None),'r13_v111_letter_compare_review')
        self.assertEqual(target('두 편지를 나란히 본다','existing_return'),'existing_return')
        self.assertIsNone(target('두 편지의 초대를 대조한다'))
        self.assertIsNone(target('함께 들어갈 근거를 고른다'))
        self.assertEqual(target('다른 쟁점','existing_return'),'existing_return')
        import json
        binding=json.loads((ROOT/'game/v111/field-bindings.json').read_text())['letter_compare_review']
        self.assertEqual(binding['options'][0],dict(title='편지와 메모를 다시 대조한다',location='room13',object='mother_note',index=0))
        self.assertEqual(binding['options'][1],dict(title='초롱 씨는 지금 어디 계세요?',location='inn',person='granny',index=1))
        self.assertEqual(binding['people_by_location'],dict(room13=['daram'],inn=['granny']))
        flow=(ROOT/'game/room13_v111.rpy').read_text()
        self.assertIn('if _return=="investigate" and r13_pw_review_target(key,review_return):',flow)
        self.assertIn('return r13_pw_review_target(key,review_return)',flow)
        self.assertIn('0 if key=="letter_compare_review" or ',flow)
        early=(ROOT/'game/room13_v111_days123.rpy').read_text()
        review=early.split('label r13_v111_letter_compare_review:',1)[1].split('\nlabel ',1)[0]
        self.assertIn("call r13_v111_wait('letter_compare_review')",review)
        self.assertIn('jump r13_v111_letter_compare',review)
        self.assertNotIn('r13_v111_commit',review)

    def test_explicit_pair_submission_uses_only_current_owned_read_pair(self):
        pair_submit=self.ns['r13_pw_pair_submission']
        owned=['V111:E01','V111:E06','V111:E03']
        self.assertEqual(pair_submit(('V111:E01','V111:E06'),owned,'compare'),['V111:E01','V111:E06'])
        # 읽는 자료를 정답으로 바꾸지 않는다. 잘못 고른 두 장도 기존 판정으로 넘긴다.
        self.assertEqual(pair_submit(('V111:E03','V111:E01'),owned,'compare'),['V111:E03','V111:E01'])
        self.assertEqual(pair_submit(('V111:E06','V111:E01'),owned,'compare'),['V111:E06','V111:E01'])
        for pair in (None,(),('V111:E01',),('V111:E01',None),('V111:E01','V111:E01'),('V111:E01','V111:E99')):
            self.assertIsNone(pair_submit(pair,owned,'compare'))
        self.assertIsNone(pair_submit(('V111:E01','V111:E06'),owned,'proof'))
        self.assertEqual(owned,['V111:E01','V111:E06','V111:E03'])

    def test_pair_submit_action_preserves_original_argument_verdict_boundary(self):
        import ast,textwrap
        from types import SimpleNamespace
        source=re.search(r'^    def r13_pw_submit_pair\([\s\S]*?(?=\n    def |\nscreen )',SRC.read_text(),re.M).group(0)
        tree=ast.parse(textwrap.dedent(source))
        node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_pw_submit_pair')
        writes=[];returns=[]
        namespace=dict(self.ns,r13_pw_entries=lambda:['V111:E01','V111:E06','V111:E03'],
                       r13_pw_set_arguments=lambda claim,pair:writes.append((claim,list(pair))),
                       r13_room_letters_begin_discovery=lambda claim,pair:False,
                       renpy=SimpleNamespace(end_interaction=returns.append))
        exec(compile(ast.Module(body=[node],type_ignores=[]),'읽는 쌍의 명시 제출','exec'),namespace)
        action=namespace['r13_pw_submit_pair']
        action('claim',('V111:E01','V111:E03'),'compare')
        self.assertEqual(writes,[('claim',['V111:E01','V111:E03'])])
        self.assertEqual(returns,['argue'])
        for pair,mode in ((('V111:E01',None),'compare'),(('V111:E01','V111:E99'),'compare'),(('V111:E01','V111:E06'),'proof')):
            action('claim',pair,mode)
        self.assertEqual(len(writes),1)
        self.assertEqual(returns,['argue'])
        # 첫 방의 미관찰 쌍이면 읽는 화면만 열고 제출/상태 쓰기는 멈춘다.
        namespace['r13_room_letters_begin_discovery']=lambda claim,pair:True
        action('claim',('V111:E01','V111:E06'),'compare')
        self.assertEqual(len(writes),1)
        self.assertEqual(returns,['argue'])

    def test_review_button_precedes_other_secondary_controls(self):
        source=SRC.read_text()
        footer=source.split('    $ secondary=[]',1)[1].split('    for si,',1)[0]
        self.assertLess(footer.index('r13_pw_investigate'),footer.index('r13_pw_observe'))
        self.assertLess(footer.index('r13_pw_observe'),footer.index('r13_pw_press'))
        self.assertIn('key "game_menu" action review_action',source)

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
