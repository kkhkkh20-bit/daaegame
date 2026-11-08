"""조연 두 인물의 원본·투명 경계와 기존 근접/질문 크기를 검증한다."""
import hashlib
import json
from pathlib import Path
import unittest

from PIL import Image
from import_support_pixel132 import ART, ROOT, REGISTRY, REVISION, TARGETS, prepare


class SupportPixelDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = prepare()
        cls.receipts = {person: json.loads((ART / person / 'manifest.json').read_text())
                        for person in TARGETS}

    def test_two_separate_identities_and_six_unique_transparent_sources(self):
        self.assertEqual(set(self.entries), {'ms14_clinician', 'kid_nubi1'})
        for person, receipt in self.receipts.items():
            self.assertEqual(len({r['source_sha256'] for r in receipt['frames']}), 6)
            for row in receipt['frames']:
                with self.subTest(person=person, slot=row['slot']):
                    self.assertEqual(hashlib.sha256((ROOT / row['source_master']).read_bytes()).hexdigest(), row['source_sha256'])
                    with Image.open(ROOT / row['source_master']) as im:
                        self.assertEqual(im.mode, 'RGBA')
                        self.assertEqual(im.size, (1024, 1536))
                        box = im.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                        self.assertTrue(0 < box[0] < box[2] < im.width)
                        self.assertTrue(0 < box[1] < box[3] < im.height)
                    self.assertLessEqual(max(row['alpha_notes']['corners']), 4)
                    self.assertLessEqual(row['alpha_notes']['outside_core10px_max_alpha'], 4)

    def test_original_close_height_question_height_and_common_footline(self):
        for person, (visible, question_height) in TARGETS.items():
            entry = self.entries[person]
            self.assertEqual(entry['art_revision'], REVISION)
            for size, height in [('560', question_height), ('760', visible * 760 / 840), ('840', visible)]:
                feet = []
                for slot, frame in entry['profiles'][size]['frames'].items():
                    with Image.open(ROOT / frame['source_master']) as im:
                        box = im.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                    self.assertAlmostEqual((box[3] - box[1]) * frame['scale'], height, delta=.001)
                    feet.append(frame['offset'][1] + box[3] * frame['scale'])
                    self.assertTrue(frame['file'].startswith('assets/dialogue-player-facing/support132-20261108/' + person + '/'))
                    filename = Path(frame['file']).name
                    self.assertEqual(filename, person + '-flustered.webp' if slot == 'flustered' else slot + '.webp')
                self.assertLessEqual(max(feet) - min(feet), 1)
            question = entry['profiles']['560']
            self.assertLessEqual(question['question_top'] + max(
                f['offset'][1] + f['anchor'][1] * f['scale']
                for f in question['frames'].values()), 708)

    def test_prepare_leaves_shared_registry_unmodified(self):
        before = REGISTRY.read_bytes()
        prepare()
        self.assertEqual(REGISTRY.read_bytes(), before)


if __name__ == '__main__':
    unittest.main()
