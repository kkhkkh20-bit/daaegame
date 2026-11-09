"""획득 알림의 순서·숨김 중 만료 방지·중복 없는 기록 획득을 검증한다."""
import ast
import copy
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/room13_feedback.rpy'

def load_function(path,name,env):
    source=Path(path).read_text()
    block=source.split('init ',1)[1].split(' python:\n',1)[1]
    # 함수가 있는 첫 python 블록만 읽는다. 아래 screen 문법은 Python이 아니다.
    block=block.split('\ntransform ',1)[0]
    tree=ast.parse(textwrap.dedent(block))
    node=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name==name)
    exec(compile(ast.Module(body=[node],type_ignores=[]),str(path),'exec'),env)
    return env[name]

class EvidenceNotice134(unittest.TestCase):
    def setUp(self):
        self.shown=[]
        self.current=None
        self.updates=[]
        self.restarts=[]
        self.blocked=set()
        self.showing=set()
        self.store=SimpleNamespace(r13_nw_comparison=None,r13_ep_cut_current=None)
        self.env=dict(store=self.store,r13_feedback_in_conversation=lambda:False,
            renpy=SimpleNamespace(get_screen=lambda name:self.current if name=='r13_evidence_found' else name in self.blocked,
                showing=lambda name:name in self.showing,
                show_screen=lambda name,**kwargs:self.shown.append((name,kwargs)),
                set_screen_variable=lambda name,value,**kw:self.updates.append((name,value,kw)),
                restart_interaction=lambda:self.restarts.append(True)))
        self.merge=load_function(SOURCE,'r13_evidence_notice_keys',self.env)
        self.visible=load_function(SOURCE,'r13_evidence_notice_visible',self.env)
        self.acquire=load_function(SOURCE,'r13_evidence_acquired',self.env)
    def test_batch_order_is_stable_and_deduplicated(self):
        self.assertEqual(self.merge(['V111:E02'],['V111:E03','V111:E02','V111:E05']),['V111:E02','V111:E03','V111:E05'])
    def test_active_notice_keeps_completed_prefix_and_current_index(self):
        self.current=SimpleNamespace(scope=dict(keys=['V111:E02','V111:E03'],item_index=1))
        self.acquire(['V111:E05'])
        self.assertEqual(self.updates,[('notice_keys',['V111:E02','V111:E03','V111:E05'],{'screen':'r13_evidence_found'})])
        self.assertEqual(self.shown,[])
        self.assertEqual(self.restarts,[True])
        self.assertEqual(self.current.scope['item_index'],1)
        self.assertEqual(self.current.scope['keys'],['V111:E02','V111:E03'])
    def test_separate_grants_before_first_render_preserve_show_arguments(self):
        self.current=SimpleNamespace(scope={'_kwargs':{'keys':['V111:E02']}})
        self.acquire(['V111:E03','V111:E05'])
        self.assertEqual(self.updates,[('notice_keys',['V111:E02','V111:E03','V111:E05'],{'screen':'r13_evidence_found'})])
        self.assertEqual(self.shown,[])
        self.assertEqual(self.current.scope,{'_kwargs':{'keys':['V111:E02']}})

    def test_duplicate_call_never_restarts_current_notice(self):
        self.current=SimpleNamespace(scope=dict(keys=['V111:E02','V111:E03'],item_index=1))
        self.acquire(['V111:E02','V111:E03'])
        self.assertEqual(self.shown,[])
    def test_hidden_panes_and_menus_block_visibility(self):
        for name in ('r13_proof_workspace','r13_fire_links','r13_fire_recheck','r13_record_compare','r13_map','r13_records','pause_menu','main_menu','save','load','confirm','r13_latch_diagram132'):
            self.blocked={name};self.assertFalse(self.visible(),name)
        self.blocked=set();self.assertTrue(self.visible())
        self.store.r13_nw_comparison='knife_tip';self.assertFalse(self.visible())
    def test_fire_reading_defers_queued_notice_until_return_to_scene(self):
        self.acquire(['V111:E06_FIRE'])
        self.current=SimpleNamespace(scope=dict(notice_keys=['V111:E06_FIRE'],item_index=0))
        self.blocked={'r13_fire_links'}
        self.assertFalse(self.visible())
        self.acquire(['V111:E06_RESCUE'])
        self.assertEqual(self.updates[0][1],['V111:E06_FIRE','V111:E06_RESCUE'])
        self.assertEqual(self.current.scope['item_index'],0)
        self.blocked.clear()
        self.assertTrue(self.visible())
    def test_family_focus_defers_notice_until_picture_is_folded(self):
        self.acquire(['V111:E30'])
        self.store.r13_ep_cut_current='focus:D01_FAMILY_DRAWING'
        self.showing={'r13_ep_cut'}
        self.assertFalse(self.visible())
        self.assertEqual(self.shown[0][1]['keys'],['V111:E30'])
        self.showing.clear()
        self.assertTrue(self.visible(),'컷을 접으면 대기 중인 획득 알림이 같은 자료로 이어진다.')
        self.store.r13_ep_cut_current='ev:E06';self.showing={'r13_ep_cut'}
        self.assertTrue(self.visible(),'작은 일반 증거 컷은 기존처럼 알림과 함께 표시한다.')
    def test_only_visible_branch_owns_expiry_timer(self):
        screen=SOURCE.read_text().split('screen r13_evidence_found(',1)[1].split('\n# A quiet',1)[0]
        self.assertIn('if r13_evidence_notice_visible():',screen)
        self.assertIn('        for notice_index index notice_index in [item_index]:\n            timer 3.2',screen)
        self.assertEqual(screen.count('timer 3.2 action'),1,'각 index의 시계는 하나다. append는 action만 바꾼다.')
        self.assertIn('notice_index+1<len(notice_keys) else Hide("r13_evidence_found")',screen)
        self.assertNotIn('\n    timer ',screen)
        self.assertNotIn('repeat True',screen)
    def test_notification_uses_authored_icon_and_explicit_acquisition_label(self):
        card=SOURCE.read_text().split('screen r13_evidence_card(',1)[1].split('screen r13_evidence_found(',1)[0]
        self.assertIn('r13_record_icon(key)',card)
        self.assertIn('text "증거 획득"',card)
        self.assertIn('R13_EVIDENCE_NOTICE_SIZE if notice else R13_EVIDENCE_HELD_SIZE',card)
        self.assertIn('                if notice:\n                    vbox:',card)
        self.assertIn('r13_catalog_title(key)',card)
    def test_grant_of_owned_record_does_not_enqueue_again(self):
        calls=[]
        store=SimpleNamespace(room13=dict(evidence=[],records={},flags=[],day=1,period=0,location='gate'))
        source=(ROOT/'game/room13_rules.rpy').read_text()
        start=source.index('    def r13_grant(');end=source.index('\n    def ',start+5)
        env=dict(store=store,winter_copy=copy,persistent=SimpleNamespace(room13_knowledge=[]),
            ROOM13=dict(evidence={'V111:E02':{'name':'초소 처리 명단'}}),r13_evidence_acquired=lambda keys:calls.append(list(keys)))
        exec(textwrap.dedent(source[start:end]),env)
        env['r13_grant'](['V111:E02'],'gate');snapshot=copy.deepcopy(store.room13)
        env['r13_grant'](['V111:E02'],'gate')
        self.assertEqual(calls,[['V111:E02']]);self.assertEqual(store.room13,snapshot)
    def test_no_notification_awards_or_load_replay_hooks(self):
        body=SOURCE.read_text().split('    def r13_evidence_notice_keys',1)[1].split('    def r13_click_feedback',1)[0]
        for forbidden in ('r13_grant(','r13_v111_set(','after_load_callbacks.append','room13['):self.assertNotIn(forbidden,body)
        self.acquire([]);self.assertEqual(self.shown,[])

if __name__=='__main__':unittest.main()
