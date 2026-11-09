"""납품 B 버튼의 실제 상태·크기 계약과 공통 판 연결을 검사한다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import sys
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'game/python-packages'))
from r13_assets import Registry


def load_nodes(filename,names,env):
    source=(ROOT/'game'/filename).read_text().split(' python:\n',1)[1].split('\ninit ',1)[0].split('\nscreen ',1)[0]
    tree=ast.parse(textwrap.dedent(source))
    selected=[n for n in tree.body if isinstance(n,(ast.ClassDef,ast.FunctionDef)) and n.name in names]
    exec(compile(ast.Module(body=selected,type_ignores=[]),filename,'exec'),env)


class SuppliedButtons135(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        p=ROOT/'game/asset-toolbox'
        cls.registry=Registry(json.loads((p/'catalog.json').read_text()),json.loads((p/'bindings.json').read_text()))

    def setUp(self):
        self.env=dict(renpy=SimpleNamespace(Displayable=object),r13_asset_revision=lambda:0,
            r13_asset_spec=self.registry.resolve,r13_asset=lambda role,state='basic':dict(role=role,state=state),
            Transform=lambda child,**kw:dict(child=child,**kw))
        load_nodes('room13_button_states.rpy',{'R13ButtonStateVisual'},self.env)
        load_nodes('room13_ui_art.rpy',{'r13_supplied_button_surface','R13ControlSurface','R13SoftButtonSurface'},self.env)

    def test_rectangular_buttons_use_supplied_originals_for_all_states_and_fit_uniformly(self):
        for family,primary,width,height in [('main_primary',True,200,76),('topic_standard',False,162,68),('question_flat_standard',False,162,64),('map_flat_primary',True,250,44),('wide_choice',False,600,70)]:
            with self.subTest(family=family):
                visual=self.env['R13ButtonStateVisual']('자료 제시',family,width,height)
                role='button.'+family
                self.assertEqual(visual.source_role,role)
                spec=self.registry.resolve(role)
                cw,ch=spec['render']['crop'][2:]
                for state,skin in visual.shared_skins.items():
                    self.assertEqual(skin['child'],dict(role=role,state=state))
                    self.assertNotIn('xysize',skin,'원본을 가로·세로 따로 늘리지 않는다')
                    self.assertLessEqual(cw*skin['zoom'],visual.paper_size[0]+.001)
                    self.assertLessEqual(ch*skin['zoom'],visual.paper_size[1]+.001)
                    self.assertTrue(self.registry.resolve(role,state)['path'].startswith('assets/ui-button-states/'))
                self.assertEqual((visual.width,visual.height),(width,height))

    def test_each_semantic_role_rebinding_reaches_the_actual_visual(self):
        changed=Registry(copy.deepcopy(self.registry.catalog),copy.deepcopy(self.registry.bindings))
        changed.assign('button.main_standard','button.primary.basic')
        self.env['r13_asset_spec']=changed.resolve
        visual=self.env['R13ButtonStateVisual']('처음부터','main_standard',200,76)
        self.assertEqual(visual.source_role,'button.main_standard')
        self.assertEqual(changed.resolve(visual.source_role)['path'],'assets/ui-button-states/primary_basic.png')
        self.assertEqual(changed.resolve('button.topic_standard')['path'],'assets/ui-button-states/standard_basic.png')

    def test_square_role_keeps_its_canvas_without_stretching_rectangular_art(self):
        visual=self.env['R13ButtonStateVisual']('', 'square_standard',80,80)
        self.assertEqual(visual.source_role,'button.square_standard')
        self.assertEqual(visual.paper_size[0],visual.paper_size[1])

    def test_surface_role_has_explicit_frame_but_small_buttons_remain_uniform(self):
        for family in ('standard','primary'):
            role='surface.supplied.button.'+family
            self.assertIn('frame',self.registry.bindings['bindings'][role]['requires_render'])
            self.assertIn('frame',self.registry.bindings['bindings']['button.'+family]['forbid_render'])
            for state in ('basic','pressed','selected','disabled'):
                spec=self.registry.resolve(role,state)
                self.assertEqual(spec['path'],'assets/ui-button-states/'+family+'_'+state+'.png')
                self.assertEqual(spec['render']['crop'],[12,6,136,40])
                self.assertEqual(spec['render']['frame'],[12,10,12,10])
                self.assertTrue(spec['render']['allow_frame'])
                self.assertNotIn('frame',self.registry.resolve('button.'+family,state)['render'])
        self.assertEqual(self.registry.validate(),[])

    def test_common_surfaces_preserve_selected_hover_and_disabled_states(self):
        control=self.env['R13ControlSurface'];soft=self.env['R13SoftButtonSurface']
        self.assertEqual(control(primary=True).face,dict(role='surface.supplied.button.primary',state='basic'))
        self.assertEqual(control(chosen=True).face,dict(role='surface.supplied.button.primary',state='selected'))
        self.assertEqual(soft(chosen=True).face,dict(role='surface.supplied.button.standard',state='selected'))
        self.assertEqual(soft(hovered=True).face,dict(role='surface.supplied.button.standard',state='pressed'))
        disabled=soft(hovered=True,chosen=True,disabled=True).face
        self.assertEqual(disabled['child'],dict(role='surface.supplied.button.standard',state='disabled'))
        self.assertLess(disabled['alpha'],1)


if __name__=='__main__':unittest.main()
