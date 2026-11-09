"""실물 조사 그림의 접점·발견 위치와 무료 관찰의 반환 계약을 검증한다."""
import ast
import copy
from pathlib import Path
import textwrap
import unittest


ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'game/systems/room13_case_inspect.rpy'


def contains(rect,point):
    x,y,w,h=rect
    return x<=point[0]<x+w and y<=point[1]<y+h


class CaseInspect(unittest.TestCase):
    def setUp(self):
        source=SOURCE.read_text()
        self.code=source.split('init 353 python:',1)[1].split('\nscreen ',1)[0]
        self.env={}
        exec(compile(ast.parse(textwrap.dedent(self.code)),str(SOURCE),'exec'),self.env)

    def source_point(self,kind,point,layout):
        cx,cy,cw,ch=self.env['R13_CASE_INSPECT_CROP'][kind]
        x,y,w,h=layout['art']
        return (x+(point[0]-cx)*float(w)/cw,y+(point[1]-cy)*float(h)/ch)

    def test_reuses_the_supplied_art_without_new_media(self):
        self.assertEqual(self.env['R13_CASE_INSPECT_ART'],{
            'knife':'assets/room13-meeting-knife-tip-match.webp',
            'latch':'assets/room13-latch-diagram132.webp'})
        for path in self.env['R13_CASE_INSPECT_ART'].values():
            self.assertTrue((ROOT/'game'/path).is_file())

    def test_knife_contact_target_contains_the_actual_broken_edges_only(self):
        layout=self.env['r13_case_inspect_layout']('knife')
        fit=self.env['r13_case_inspect_target_rect']('knife','fit',layout)
        self.assertTrue(contains(fit,self.source_point('knife',(1750,350),layout)))
        for point in ((400,350),(1250,350),(1990,380)):
            self.assertFalse(contains(fit,self.source_point('knife',point,layout)),point)

    def test_latch_targets_separate_the_outside_plate_and_inside_fragment(self):
        for footer in (572,556):
            layout=self.env['r13_case_inspect_layout']('latch',footer)
            outer=self.env['r13_case_inspect_target_rect']('latch','outer',layout)
            inner=self.env['r13_case_inspect_target_rect']('latch','inner',layout)
            outside=self.source_point('latch',(400,500),layout)
            fragment=self.source_point('latch',(1000,730),layout)
            self.assertTrue(contains(outer,outside))
            self.assertTrue(contains(inner,fragment))
            self.assertFalse(contains(outer,fragment))
            self.assertFalse(contains(inner,outside))

    def test_all_inputs_and_copy_fit_inside_the_notebook_and_above_footer(self):
        for footer in (572,556):
            for kind in ('knife','latch'):
                layout=self.env['r13_case_inspect_layout'](kind,footer)
                for rect in (layout['art'],layout['text']):
                    x,y,w,h=rect
                    self.assertGreaterEqual(x,132)
                    self.assertGreaterEqual(y,140)
                    self.assertLessEqual(x+w,1206)
                    self.assertLessEqual(y+h,footer-12)
                ax,ay,aw,ah=layout['art']
                for target,_ in self.env['R13_CASE_INSPECT_TARGETS'][kind]:
                    x,y,w,h=self.env['r13_case_inspect_target_rect'](kind,target,layout)
                    self.assertGreaterEqual(min(w,h),72)
                    self.assertGreaterEqual(x,ax)
                    self.assertGreaterEqual(y,ay)
                    self.assertLessEqual(x+w,ax+aw)
                    self.assertLessEqual(y+h,ay+ah)

    def test_only_knife_contact_can_return_a_finding_and_helpers_never_write_state(self):
        before=copy.deepcopy({k:v for k,v in self.env.items() if k.startswith('R13_CASE_')})
        result=self.env['r13_case_inspect_result']
        observation=self.env['r13_case_inspect_observation']
        for kind in ('knife','latch'):
            for target in [None,'other']+[k for k,_ in self.env['R13_CASE_INSPECT_TARGETS'][kind]]:
                self.assertEqual(result(kind,target),'knife_fit' if (kind,target)==('knife','fit') else None)
                self.assertTrue(observation(kind,target))
        self.assertEqual(before,{k:v for k,v in self.env.items() if k.startswith('R13_CASE_')})
        names={node.id for node in ast.walk(ast.parse(textwrap.dedent(self.code))) if isinstance(node,ast.Name)}
        self.assertTrue(names.isdisjoint({'renpy','store','room13','persistent'}))

    def test_dismiss_does_not_end_inspection_and_hotspots_do_not_reveal_labels(self):
        source=SOURCE.read_text().split('screen r13_case_inspect(kind):',1)[1]
        self.assertIn('modal True',source)
        self.assertIn('key "dismiss" action NullAction()',source)
        self.assertIn('key "game_menu" action Return(None)',source)
        self.assertIn('close_action=Return(None)',source)
        self.assertIn('background None hover_background None',source)
        self.assertIn('alt "그림 조사"',source)
        for effect in ('r13_grant(','r13_v111_set(','r13_v111_commit(','r13_v111_time('):
            self.assertNotIn(effect,source)


if __name__=='__main__':unittest.main()
