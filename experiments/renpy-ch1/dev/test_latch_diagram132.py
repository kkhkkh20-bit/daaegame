"""성공 설명에만 표시되는 위치 스케치가 다음 쟁점으로 새거나 판정을 바꾸지 않는다."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]


class LatchDiagram132(unittest.TestCase):
    def setUp(self):
        source=(ROOT/'game/systems/room13_latch_diagram132.rpy').read_text()
        code=textwrap.dedent(source.split('init 365 python:',1)[1].split('\nscreen ',1)[0])
        self.calls=[]
        self.state=types.SimpleNamespace(r13_packet=None,r13_ep_cut_current=None,room13={'evidence':['V111:E17','V111:E32','V111:E33'],'arguments':{},'v111':{'values':{'tries:lamp':2}}})
        def base_line(packet):
            options=packet[2] if len(packet)>2 else {}
            if 'cut' in options:self.state.r13_ep_cut_current=options['cut']
            return '기존 대사 연출'
        def base_clear():
            self.state.r13_ep_cut_current=None
            return '기존 연출 정리'
        self.env=dict(store=self.state,config=types.SimpleNamespace(after_load_callbacks=[]),r13_v111_active=lambda:True,renpy=types.SimpleNamespace(
            get_screen=lambda name:True,show=lambda name,**kw:self.calls.append(('main_show',name,kw)),hide=lambda name:self.calls.append(('main_hide',name)),
            show_screen=lambda name,**kw:self.calls.append(('show',name,kw)),
            hide_screen=lambda name:self.calls.append(('hide',name))),
            r13_ep_cut_art=lambda name:('기존 컷',name),r13_ep_line_art=base_line,
            r13_ep_line_art_clear=base_clear,Null=lambda:('빈 main 컷',))
        exec(compile(ast.parse(code),'걸쇠 위치 스케치','exec'),self.env)

    def test_same_cut_lifecycle_tracks_outer_then_inner_and_clears_on_next_issue(self):
        before=copy.deepcopy(self.state.room13)
        line=self.env['r13_ep_line_art']
        self.assertEqual(line(('resident_tok','바깥 판',{'cut':'latch132_outer'})),'기존 대사 연출')
        self.assertEqual(self.calls[-1],('show','r13_latch_diagram132',{'kind':'latch132_outer'}))
        line(('resident_tok','계속 설명',{}))
        self.assertEqual(self.calls[-1][2]['kind'],'latch132_outer')
        line(('resident_tok','안쪽 받침',{'cut':'latch132_inner'}))
        self.assertEqual(self.calls[-1][2]['kind'],'latch132_inner')
        line(('resident_siluk','다음 쟁점',{'cut':None}))
        self.assertEqual(self.calls[-1],('hide','r13_latch_diagram132'))
        self.assertEqual(self.state.room13,before)

    def test_block_end_always_removes_diagram_and_preserves_regular_cut_renderer(self):
        self.state.r13_ep_cut_current='latch132_inner'
        self.assertEqual(self.env['r13_ep_line_art_clear'](),'기존 연출 정리')
        self.assertEqual(self.calls[-1],('hide','r13_latch_diagram132'))
        self.assertIsNone(self.state.r13_ep_cut_current)
        self.assertEqual(self.env['r13_ep_cut_art']('piko-death3'),('기존 컷','piko-death3'))
        self.assertEqual(self.env['r13_ep_cut_art']('latch132_outer'),('빈 main 컷',))

    def test_panel_and_focus_stay_above_large_dialogue_and_within_page(self):
        layout=self.env['r13_latch132_layout']()
        self.assertGreaterEqual(layout['x'],780)
        self.assertLessEqual(layout['x']+layout['w'],1280)
        self.assertGreaterEqual(layout['y'],104)
        self.assertLessEqual(layout['y']+layout['h'],504)
        for kind in self.env['R13_LATCH132_CUTS']:
            x,y,w,h=self.env['r13_latch132_focus'](kind)
            self.assertGreaterEqual(min(x,y),0)
            self.assertLessEqual(x+w,layout['w'])
            self.assertLessEqual(y+h,layout['h'])

    def test_legacy_packet_missing_cut_restores_only_the_current_ui_without_story_effects(self):
        self.state.room13['v111']['scene']='MS14_D03_S05'
        before=copy.deepcopy(self.state.room13)
        for rid,expected in self.env['R13_LATCH132_LEGACY_LINES'].items():
            self.state.r13_packet=('resident_tok','기존 설명',{'line_id':rid})
            self.state.r13_ep_cut_current=None
            self.env['r13_latch132_after_load']()
            self.assertEqual(self.state.r13_packet[1],'기존 설명')
            self.assertEqual(self.state.r13_packet[2],{'line_id':rid})
            self.assertEqual(self.calls[-1],('show','r13_latch_diagram132',{'kind':expected}))
            self.assertEqual(self.state.room13,before)

    def test_legacy_precomputed_sequence_updates_outer_inner_clear_without_mutating_packets(self):
        self.state.room13['v111']['scene']='MS14_D03_S05'
        before=copy.deepcopy(self.state.room13)
        packets=[('resident_tok','기존 바깥 판 설명',{'line_id':'MS14_D03_S05_L0021'}),
                 ('resident_tok','기존 안쪽 받침 설명',{'line_id':'MS14_D03_S05_L0023'}),
                 ('resident_siluk','기존 다음 쟁점',{'line_id':'MS14_D03_S05_L0025'})]
        original=copy.deepcopy(packets)
        for packet,expected in zip(packets,['latch132_outer','latch132_inner',None]):
            self.env['r13_ep_line_art'](packet)
            self.assertEqual(self.state.r13_ep_cut_current,expected)
            self.assertEqual(self.calls[-1],('show','r13_latch_diagram132',{'kind':expected}) if expected else ('hide','r13_latch_diagram132'))
        self.assertEqual(packets,original)
        self.assertEqual(self.state.room13,before)
        other=self.env['r13_latch132_packet'](packets[0],True,'MS14_D04_S01')
        self.assertIs(other,packets[0])

    def test_new_saved_diagram_continues_but_next_line_and_field_do_not_keep_it(self):
        self.state.room13['v111']['scene']='MS14_D03_S05'
        self.state.r13_packet=('resident_tok','계속 설명',{'line_id':'NW_D03_S05_T09','cut':'latch132_inner'})
        self.state.r13_ep_cut_current='latch132_inner'
        self.env['r13_latch132_after_load']()
        self.assertEqual(self.calls[-1],('show','r13_latch_diagram132',{'kind':'latch132_inner'}))
        self.state.r13_packet=('resident_siluk','다음 쟁점',{'line_id':'MS14_D03_S05_L0025'})
        self.env['r13_latch132_after_load']()
        self.assertIsNone(self.state.r13_ep_cut_current)
        self.assertIn(('hide','r13_latch_diagram132'),self.calls[-2:])
        self.state.r13_packet=('resident_tok','지나간 설명',{'line_id':'MS14_D03_S05_L0021'})
        self.env['renpy'].get_screen=lambda name:None
        self.env['r13_latch132_after_load']()
        self.assertEqual(self.calls[-1],('hide','r13_latch_diagram132'))
        self.state.r13_ep_cut_current='ev:E01'
        self.env['r13_latch132_after_load']()
        self.assertEqual(self.state.r13_ep_cut_current,'ev:E01')

    def test_authored_success_lines_only_add_presentation_not_new_evidence(self):
        day=json.loads((ROOT/'game/v111/newworld/d03.json').read_text())
        cuts={rid:row['cut'] for rid,row in day['replace'].items() if isinstance(row,dict) and str(row.get('cut','')).startswith('latch132_')}
        self.assertEqual(cuts,{'MS14_D03_S05_L0021':'latch132_outer','MS14_D03_S05_L0023':'latch132_inner'})
        self.assertIsNone(day['replace']['MS14_D03_S05_L0025']['cut'])
        manifest=json.loads((ROOT/'art/latch-diagram132-20261108/manifest.json').read_text())
        for field,digest in (('source_master','source_sha256'),('runtime_file','runtime_sha256')):
            path=ROOT/manifest[field] if field=='source_master' else ROOT/'game'/manifest[field]
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),manifest[digest])
        self.assertEqual(manifest['runtime_file'],self.env['R13_LATCH132_ART'])


if __name__=='__main__':unittest.main()
