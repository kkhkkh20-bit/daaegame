"""요청된 크기별 버튼 원본·네 상태·도구함 표시 계약을 확인한다."""
import json
from pathlib import Path
import sys
import unittest

from PIL import Image, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'game/python-packages'))
from r13_assets import Registry
from asset_toolbox import FIT_BUTTONS, STATES


class ButtonFitAssets(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder=ROOT/'game/asset-toolbox'
        cls.registry=Registry(json.loads((folder/'catalog.json').read_text()),
                              json.loads((folder/'bindings.json').read_text()))

    def test_all_twenty_originals_keep_exact_canvas_and_aligned_outer_bounds(self):
        for family,(_,canvas,crop,safe,gap) in FIT_BUTTONS.items():
            expected=(crop[0],crop[1],crop[0]+crop[2],crop[1]+crop[3])
            boxes=[]
            for state in STATES:
                with self.subTest(family=family,state=state):
                    path=ROOT/'game/assets/ui-button-fit'/('%s_%s.png'%(family,state))
                    with Image.open(path) as im:
                        self.assertEqual(im.mode,'RGBA')
                        self.assertEqual(list(im.size),canvas)
                        boxes.append(im.getchannel('A').getbbox())
            self.assertEqual(boxes,[expected]*4)

    def test_role_state_sets_keep_uniform_crop_safe_area_and_original_families(self):
        for family,(_,canvas,crop,safe,gap) in FIT_BUTTONS.items():
            role='button.'+family
            rule=self.registry.bindings['bindings'][role]
            self.assertEqual(rule['states'],list(STATES))
            self.assertIn('frame',rule['forbid_render'])
            for state in STATES:
                result=self.registry.resolve(role,state)
                self.assertEqual(result['size'],canvas)
                self.assertEqual(result['render']['crop'],crop)
                self.assertEqual(result['render']['safe_size'],safe)
                self.assertEqual(result['render']['icon_gap'],gap)
                self.assertNotIn('frame',result['render'])
                self.assertLessEqual(safe[0],crop[2])
                self.assertLessEqual(safe[1],crop[3])
        for family in ('primary','standard','wide_choice'):
            for state in STATES:
                self.assertTrue(self.registry.resolve('button.'+family,state)['path'].startswith('assets/ui-button-states/'))

    def test_current_main_and_topic_labels_fit_without_font_reduction(self):
        font=ROOT/'game/assets/Pretendard-Bold.otf'
        for size,icon,gap,safe,captions in (
            (28,30,10,164,('이어하기','처음부터','불러오기','설정')),
            (22,24,6,130,('자료 제시','기록','더보기','돌아가기')),
            (24,24,6,130,('자료 제시','기록','더보기','돌아가기')),
        ):
            face=ImageFont.truetype(str(font),size)
            for caption in captions:
                self.assertLessEqual(face.getlength(caption)+icon+gap,safe,(caption,size))


if __name__=='__main__':
    unittest.main()
