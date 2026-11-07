"""도담은 일반 kid_ 분류보다 먼저 132도트로 분류하고 기존 원화·좌표 비율을 보존한다."""
import ast
import json
from pathlib import Path
import unittest

import numpy as np
from PIL import Image

ROOT=Path(__file__).resolve().parents[1]


class FieldDodamSize(unittest.TestCase):
    def test_small_child_precedes_generic_kid_prefix(self):
        tree=ast.parse((ROOT/'dev/build_field_dot.py').read_text())
        names={'KID','SMALL','OLD','TEEN','BIG','target_dots'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names or
               isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id in names for t in n.targets)]
        env={};exec(compile(ast.Module(body=nodes,type_ignores=[]),'현장 도트 목표 키','exec'),env)
        for person,height in (('kid_dodam',132),('kid_kkomi',165),('kid_nubi1',165),('daram',165),('karo',230),('resident_bori',230),('granny',195)):
            self.assertEqual(env['target_dots'](person),height,person)

    def test_existing_neutral_and_other_standing_poses_share_the_132_dot_height(self):
        data=json.loads((ROOT/'game/assets/room13-field-dot-v2.json').read_text())['people']['kid_dodam']
        self.assertEqual(data['target_dots'],132)
        self.assertEqual(data['poses']['neutral']['size'],[62,132])
        for pose in ('thinking','distressed','expressive','lick_ladle'):
            entry=data['poses'][pose]
            self.assertLessEqual(abs(entry['size'][1]-132),1,pose)
            with Image.open(ROOT/'game'/entry['file']) as source:
                im=source.convert('RGBA');pixels=np.asarray(im)
                self.assertEqual(list(im.size),entry['size'])
                self.assertTrue(set(np.unique(pixels[...,3]))<={0,255})
                self.assertLessEqual(len(np.unique(pixels[pixels[...,3]>0,:3],axis=0)),48)
                self.assertEqual(im.getchannel('A').getbbox(),(0,0,im.width,im.height))

    def test_source_crop_and_relative_head_foot_coordinates_are_preserved(self):
        specs=json.loads((ROOT/'game/assets/room13-pixel-acting.json').read_text())['kid_dodam']
        poses=json.loads((ROOT/'game/assets/room13-field-dot-v2.json').read_text())['people']['kid_dodam']['poses']
        for pose in ('thinking','distressed','expressive','lick_ladle'):
            spec,entry=specs[pose],poses[pose]
            self.assertEqual(entry['source'],dict(file=spec['file'],crop=spec['crop']))
            factor=entry['head'][2]/spec['head'][2]
            self.assertAlmostEqual(entry['head'][3],spec['head'][3]*factor,delta=.2)
            for axis in (0,1):
                # 자르면서 옮겨진 공통 원점은 빼고, 같은 원화의 머리→발 벡터를 비교한다.
                actual=entry['foot'][axis]-entry['head'][axis]
                expected=(spec['foot'][axis]-spec['head'][axis])*factor
                self.assertAlmostEqual(actual,expected,delta=.3,msg=pose)


if __name__=='__main__':unittest.main()
