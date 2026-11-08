"""너울 납품의 투명 경계·감정 묶음·세 프로필의 원래 키와 발선을 확인한다."""
import hashlib
import json
from pathlib import Path
import unittest

from PIL import Image
from import_neoul_pixel131 import ART, ROOT, REVISION, prepare


class NeoulPixelDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((ART / 'manifest.json').read_text())
        cls.entry = prepare()

    def test_six_distinct_authored_expressions_with_original_alpha_margins(self):
        rows = self.receipt['frames']
        self.assertEqual(len({row['source_sha256'] for row in rows}), 6)
        for row in rows:
            source = ROOT / row['source_master']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), row['source_sha256'])
            with Image.open(source) as image:
                self.assertEqual(image.mode, 'RGBA')
                self.assertEqual(image.size, (1024, 1536))
                box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                self.assertGreater(box[0], 0)
                self.assertGreater(box[1], 0)
                self.assertLess(box[2], 1024)
                self.assertLess(box[3], 1536)
            self.assertLessEqual(max(row['alpha_notes']['corners']), 4)
            self.assertLessEqual(row['alpha_notes']['outside_core10px_max_alpha'], 4)

    def test_existing_close_and_question_heights_and_footline_are_preserved(self):
        self.assertEqual(self.entry['art_revision'], REVISION)
        for size, visible in [('560', 560), ('760', 848 * 760 / 840), ('840', 848)]:
            profile = self.entry['profiles'][size]
            feet = []
            for frame in profile['frames'].values():
                with Image.open(ROOT / frame['source_master']) as image:
                    box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                self.assertAlmostEqual((box[3] - box[1]) * frame['scale'], visible, delta=.001)
                feet.append(frame['offset'][1] + box[3] * frame['scale'])
                self.assertTrue(frame['file'].startswith('assets/dialogue-player-facing/neoul20261108/'))
            self.assertLessEqual(max(feet) - min(feet), 1)
        question = self.entry['profiles']['560']
        self.assertLessEqual(question['question_top'] + max(
            frame['offset'][1] + frame['anchor'][1] * frame['scale']
            for frame in question['frames'].values()), 708)


if __name__ == '__main__':
    unittest.main()
