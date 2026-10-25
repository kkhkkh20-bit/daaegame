"""태그 변경의 전파, 불명확 매칭/상태 누락 차단, 게임 독립 모델 검증."""
import copy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'game/python-packages'))
from r13_assets import Registry, AssetError


def fixture():
    assets={}
    for family in ('red','cream'):
        for state in ('basic','pressed','selected','disabled'):
            key=family+'.'+state
            assets[key]=dict(path='assets/'+key+'.png',size=[160,52],media='image',tags=['pack:'+family,'state:'+state],render={'crop':[12,6,136,40]})
    roles={role:dict(match=['pack:red'],states=['basic','pressed','selected','disabled'],media='image',group='shared.primary') for role in ('main.primary','question.primary','map.primary')}
    return Registry({'version':1,'assets':assets},{'version':1,'bindings':roles})


class AssetToolbox(unittest.TestCase):
    def test_one_family_assignment_updates_every_screen_and_all_states(self):
        registry=fixture()
        changed=registry.assign('main.primary','cream.basic')
        self.assertEqual(set(changed),{'main.primary','question.primary','map.primary'})
        for role in changed:
            for state in ('basic','pressed','selected','disabled'):
                self.assertEqual(registry.resolve(role,state)['id'],'cream.'+state)

    def test_context_tags_keep_size_variants_when_switching_one_theme_group(self):
        registry=fixture()
        registry.catalog['assets']={}
        for family in ('red','cream'):
            for context in ('main','question','map'):
                for state in ('basic','pressed','selected','disabled'):
                    key=family+'.'+context+'.'+state
                    registry.catalog['assets'][key]=dict(path='assets/'+key+'.png',size=[160 if context=='main' else 128,52],media='image',tags=['pack:'+family,'context:'+context,'state:'+state],render={})
        for role,rule in registry.bindings['bindings'].items():rule['requires']=['context:'+role.split('.')[0]]
        registry._index();registry.assign('main.primary','cream.main.basic')
        for context in ('main','question','map'):
            self.assertEqual(registry.resolve(context+'.primary')['id'],'cream.'+context+'.basic')
        self.assertEqual(registry.validate(),[])

    def test_file_aliases_follow_chains_without_inheriting_virtual_crop(self):
        registry=fixture()
        for name in ('red','cream'):
            registry.bindings['bindings']['file:assets/'+name+'.basic.png']=dict(match=['asset:'+name+'.basic'],states=['basic'],media='image')
        registry._index()
        registry.assign('file:assets/red.basic.png','cream.basic')
        self.assertEqual(registry.resolve('main.primary')['path'],'assets/cream.basic.png')
        self.assertEqual(registry.resolve('file:assets/red.basic.png')['render'],{})
        before=copy.deepcopy(registry.bindings)
        with self.assertRaisesRegex(AssetError,'순환'):
            registry.assign('file:assets/cream.basic.png','red.basic')
        self.assertEqual(registry.bindings,before)

    def test_missing_pressed_state_cannot_partially_apply(self):
        registry=fixture();del registry.catalog['assets']['cream.pressed'];registry._index()
        before=copy.deepcopy(registry.bindings)
        with self.assertRaises(AssetError):registry.assign('main.primary','cream.basic')
        self.assertEqual(before,registry.bindings)
        self.assertEqual(registry.resolve('question.primary')['id'],'red.basic')

    def test_ambiguous_tags_are_rejected_instead_of_arbitrary_selection(self):
        registry=fixture();registry.catalog['assets']['another']=copy.deepcopy(registry.catalog['assets']['red.basic']);registry._index()
        with self.assertRaisesRegex(AssetError,'여러 개'):registry.resolve('main.primary')

    def test_state_geometry_mismatch_cannot_apply(self):
        registry=fixture()
        registry.catalog['assets']['cream.pressed']['size']=[180,60]
        before=copy.deepcopy(registry.bindings)
        with self.assertRaisesRegex(AssetError,'상태별'):registry.assign('main.primary','cream.basic')
        self.assertEqual(before,registry.bindings)

    def test_invalid_crop_does_not_damage_existing_binding(self):
        registry=fixture();registry.catalog['assets']['cream.basic']['render']['crop']=[150,0,20,20]
        with self.assertRaises(AssetError):registry.assign('main.primary','cream.basic')
        self.assertEqual(registry.resolve('main.primary')['id'],'red.basic')

    def test_canvas_and_media_contracts_reject_incompatible_replacement(self):
        registry=fixture();rule=registry.bindings['bindings']['main.primary'];rule['canvas_size']=[160,52]
        registry.catalog['assets']['cream.basic']['size']=[128,32]
        with self.assertRaisesRegex(AssetError,'크기'):registry.assign('main.primary','cream.basic')
        registry.catalog['assets']['cream.basic']['size']=[160,52];registry.catalog['assets']['cream.basic']['media']='audio'
        with self.assertRaisesRegex(AssetError,'종류'):registry.assign('main.primary','cream.basic')

    def test_tag_editor_preserves_required_matches_or_rolls_back(self):
        registry=fixture();before=copy.deepcopy(registry.catalog)
        with self.assertRaises(AssetError):registry.set_tags('red.pressed',['state:pressed'])
        self.assertEqual(registry.catalog,before)
        registry.set_tags('red.pressed',registry.catalog['assets']['red.pressed']['tags']+['질감:종이'])
        self.assertIn('질감:종이',registry.resolve('main.primary','pressed')['tags'])

    def test_no_outside_assets_or_nonuniform_scaling(self):
        registry=fixture()
        for path in ('/etc/passwd','assets/../../secret','https://example.com/image.png'):
            data=copy.deepcopy(registry.catalog);data['assets']['red.basic']['path']=path
            with self.assertRaises(AssetError):Registry(data,copy.deepcopy(registry.bindings))
        registry.catalog['assets']['red.basic']['render']['xzoom']=2
        with self.assertRaises(AssetError):registry.resolve('main.primary')

    def test_frame_requires_explicit_approved_policy(self):
        registry=fixture();registry.catalog['assets']['red.basic']['render']['frame']=[10,10]
        with self.assertRaisesRegex(AssetError,'분할'):registry.resolve('main.primary')

    def test_committed_catalog_has_no_missing_file_or_state(self):
        folder=ROOT/'game/asset-toolbox'
        registry=Registry(json.loads((folder/'catalog.json').read_text()),json.loads((folder/'bindings.json').read_text()))
        self.assertEqual(registry.validate(),[])
        for asset in registry.catalog['assets'].values():self.assertTrue((ROOT/'game'/asset['path']).is_file(),asset['path'])

    def test_current_defaults_preserve_original_button_crops_and_fonts(self):
        folder=ROOT/'game/asset-toolbox';registry=Registry(json.loads((folder/'catalog.json').read_text()),json.loads((folder/'bindings.json').read_text()))
        self.assertEqual(registry.resolve('button.primary')['render']['crop'],[12,6,136,40])
        self.assertEqual(registry.resolve('button.wide_choice')['render']['crop'],[4,4,232,52])
        self.assertEqual(registry.resolve('font.body','regular')['path'],'assets/Pretendard-Regular.otf')
        self.assertEqual(registry.resolve('font.bold','bold')['path'],'assets/Pretendard-Bold.otf')

    def test_shared_ui_no_longer_embeds_unmanaged_literal_files(self):
        import re
        pattern=re.compile(r'["\']assets/(?:ui-[A-Za-z0-9_-]+|map-b|map-status|map-village-b)/[A-Za-z0-9_./-]+\.(?:png|webp|jpg)["\']')
        for path in (ROOT/'game').rglob('*.rpy'):
            if 'qa_tests' not in path.parts:
                self.assertIsNone(pattern.search(path.read_text()),str(path))

    def test_font_family_assignment_keeps_regular_and_bold_distinct(self):
        folder=ROOT/'game/asset-toolbox';registry=Registry(json.loads((folder/'catalog.json').read_text()),json.loads((folder/'bindings.json').read_text()))
        changed=registry.assign('font.body','file:assets/Pretendard-Regular.otf')
        self.assertEqual(set(changed),{'font.body','font.bold'})
        self.assertNotEqual(registry.resolve('font.body','regular')['path'],registry.resolve('font.bold','bold')['path'])


if __name__=='__main__':unittest.main()
