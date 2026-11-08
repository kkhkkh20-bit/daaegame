"""초롱 평상6/작업1 분리 납품의 투명 경계·키·선택 범위 계약."""
import ast
import copy
import hashlib
import textwrap
from pathlib import Path
import unittest
from PIL import Image

from import_chorong_calm132 import ART, ROOT, PERSON, REVISION, WORK_POSE, prepare, prepare_work_pose, receipt


class ChorongCalmDelivery(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.row = receipt()
        cls.entry = prepare()
        cls.work = prepare_work_pose()

    def test_six_distinct_transparent_whole_body_sources(self):
        frames = self.row['frames']
        self.assertEqual(len({f['source_sha256'] for f in frames}), 6)
        for frame in frames:
            with self.subTest(slot=frame['slot']):
                path = ROOT / frame['source_master']
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), frame['source_sha256'])
                with Image.open(path) as image:
                    self.assertEqual(image.mode, 'RGBA')
                    self.assertEqual(image.size, (1024, 1536))
                    self.assertTrue(all(a <= 4 for a in frame['alpha_notes']['corners']))
                    self.assertLessEqual(frame['alpha_notes']['outside_core10px_max_alpha'], 4)
                    box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                    self.assertGreater(box[0], 0)
                    self.assertGreater(box[1], 0)
                    self.assertLess(box[2], image.width)
                    self.assertLess(box[3], image.height)

    def test_closeup_and_question_height_contracts(self):
        self.assertEqual(self.entry['art_revision'], REVISION)
        for height in ('560', '760', '840'):
            visible = 560 if height == '560' else 528.584071 * int(height) / 840
            profile = self.entry['profiles'][height]
            feet = []
            for frame in profile['frames'].values():
                with Image.open(ROOT / frame['source_master']) as image:
                    box = image.getchannel('A').point(lambda a: 255 if a >= 40 else 0).getbbox()
                self.assertAlmostEqual((box[3] - box[1]) * frame['scale'], visible, delta=.001)
                feet.append(frame['offset'][1] + box[3] * frame['scale'])
            self.assertLessEqual(max(feet) - min(feet), 1)
        question = self.entry['profiles']['560']
        self.assertLessEqual(question['question_top'] + max(
            f['offset'][1] + f['anchor'][1] * f['scale'] for f in question['frames'].values()), 708)

    def test_work_profiles_are_frozen_old_sources_not_new_general_art(self):
        for profile in self.work['profiles'].values():
            self.assertEqual(set(profile['frames']), {'neutral', 'flustered'})
            for frame in profile['frames'].values():
                self.assertIn('/gaze116/resident_lamplighter/', frame['file'])
                self.assertNotIn('/chorong20261108/', frame['file'])
        # 첫 실행과 일반 연결 교체 후 재실행은 같은 동결 영수증을 읽는다.
        self.assertEqual(prepare_work_pose(), copy.deepcopy(self.work))

    def test_work_pose_is_only_selected_for_one_authored_request(self):
        source = (ROOT / 'game/systems/room13_chorong_work132.rpy').read_text().split('init 391 python:', 1)[1]
        tree = ast.parse(textwrap.dedent(source))
        original = lambda rid: ('resident_lamplighter', '문장 ' + rid, {'pose': 'anxious', 'expression': 'flustered'})
        env = {'r13_v111_line': original, 'r13_fullbody_authored_pose': lambda *args: False, 'r13_dialogue_pose_source': lambda *args: self.work}
        exec(compile(tree, '초롱 작업 한 줄 범위', 'exec'), env)
        line = env['r13_v111_line']
        working = line('MS14_D02_S01_L0011')
        self.assertEqual(working[2]['pose'], WORK_POSE)
        self.assertEqual(working[2]['expression'], 'flustered')
        self.assertTrue(env['r13_fullbody_authored_pose'](PERSON,WORK_POSE))
        self.assertFalse(env['r13_fullbody_authored_pose'](PERSON,'neutral'))
        self.assertFalse(env['r13_fullbody_authored_pose']('resident_tok',WORK_POSE))
        env['r13_dialogue_pose_source']=lambda *args: {}
        self.assertFalse(env['r13_fullbody_authored_pose'](PERSON,WORK_POSE))
        for rid in ('MS14_D02_S01_L0014', 'MS14_D02_S01_L0016', 'MS14_D02_S01_L0041', 'MS14_D03_S01_L0002'):
            self.assertEqual(line(rid), original(rid))
        self.assertEqual(original('MS14_D02_S01_L0011')[2]['pose'], 'anxious')


if __name__ == '__main__':
    unittest.main()
