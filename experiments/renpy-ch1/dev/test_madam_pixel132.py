"""백 부인 일반 원화의 투명 경계·표정·기존 표시 키를 검사한다."""
import hashlib
import json
import unittest

from PIL import Image
from import_madam_pixel132 import ART, ROOT, REVISION, RUNTIME_PREFIX, prepare


class MadamPixelDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.receipt = json.loads((ART / 'manifest.json').read_text())
        cls.entry = prepare()

    def test_six_distinct_full_resolution_expressions_and_alpha_margins(self):
        rows = self.receipt['frames']
        self.assertEqual(len(rows), 6)
        self.assertEqual(len({r['source_sha256'] for r in rows}), 6)
        for row in rows:
            source = ROOT / row['source_master']
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), row['source_sha256'])
            with Image.open(source) as image:
                self.assertEqual(image.mode, 'RGBA')
                self.assertEqual(image.size, (1024, 1536))
                box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                self.assertGreater(box[0], 0)
                self.assertGreater(box[1], 0)
                self.assertLess(box[2], image.width)
                self.assertLess(box[3], image.height)
            self.assertLessEqual(max(row['alpha_notes']['corners']), 4)
            self.assertLessEqual(row['alpha_notes']['outside_core10px_max_alpha'], 4)

    def test_source_proportions_existing_height_and_feet_are_preserved(self):
        self.assertEqual(self.entry['art_revision'], REVISION)
        self.assertEqual(self.entry['gaze'], 'player')
        for size, visible in [('560', 557.3333333333334), ('760', 627 * 760 / 840), ('840', 627)]:
            profile = self.entry['profiles'][size]
            feet = []
            for slot, frame in profile['frames'].items():
                self.assertTrue(frame['file'].startswith(RUNTIME_PREFIX))
                with Image.open(ROOT / frame['source_master']) as image:
                    box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                self.assertAlmostEqual((box[3] - box[1]) * frame['scale'], visible, delta=.001)
                self.assertLessEqual(frame['scale'] * 1302 / 840, 1.05)
                feet.append(frame['offset'][1] + box[3] * frame['scale'])
            self.assertLessEqual(max(feet) - min(feet), 1)
        question = self.entry['profiles']['560']
        self.assertLessEqual(question['question_top'] + max(
            f['offset'][1] + f['anchor'][1] * f['scale']
            for f in question['frames'].values()), 708)


if __name__ == '__main__':
    unittest.main()
