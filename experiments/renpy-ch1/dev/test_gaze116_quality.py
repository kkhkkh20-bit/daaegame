"""새 정면 그림의 실제 해상도·전신 경계·질문창 발선과 기존 키를 확인한다."""
import hashlib
import json
from pathlib import Path
import unittest

from PIL import Image

from import_dialogue_gaze116 import SLOTS,read_source

ROOT=Path(__file__).resolve().parents[1]
TARGETS=json.loads((ROOT/'art/dialogue-gaze-20261107/runtime-fit-targets.json').read_text())


class GazeQuality(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.people=json.loads((ROOT/'game/assets/room13-dialogue-player-facing.json').read_text())['people']

    def test_new_frames_are_full_resolution_transparent_originals_and_matching_runtime_files(self):
        for person in TARGETS:
            entry=self.people[person]
            expected_revision=('nubi-pixel-consistency-20261108' if person=='resident_nubi'
                               else 'neoul-pixel-consistency-20261108' if person=='neoul'
                               else 'chorong-everyday-pixel-20261108' if person=='resident_lamplighter'
                               else 'gaze-quality-20261107')
            self.assertEqual(entry.get('art_revision'),expected_revision)
            self.assertEqual(set(entry['profiles']['840']['frames']),set(SLOTS))
            for slot,frame in entry['profiles']['840']['frames'].items():
                path=ROOT/frame['source_master'];row=read_source(path)
                self.assertEqual(row['source_sha256'],frame['source_sha256'])
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(),frame['source_sha256'])
                with Image.open(ROOT/'game'/frame['file']) as image:
                    self.assertEqual(list(image.size),row['size'])
                    self.assertEqual(image.mode,'RGBA')
                self.assertFalse(frame['nearest'])
                self.assertLessEqual(frame['scale']*1302/840,1.05,(person,slot))

    def test_expression_changes_keep_feet_inside_canvas_and_keep_existing_closeup_height(self):
        for person,target in TARGETS.items():
            for height,profile in self.people[person]['profiles'].items():
                feet=[]
                for slot,frame in profile['frames'].items():
                    self.assertTrue(all(type(v) is int for v in frame['offset']))
                    with Image.open(ROOT/'game'/frame['file']) as image:
                        left,top,right,bottom=image.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
                    x,y=frame['offset'];scale=frame['scale'];foot=y+bottom*scale
                    feet.append(foot)
                    self.assertGreaterEqual(x+left*scale,0)
                    self.assertGreaterEqual(y+top*scale,0)
                    self.assertLessEqual(x+right*scale,profile['canvas'][0])
                    self.assertLessEqual(foot,profile['canvas'][1])
                    if height=='840':
                        self.assertAlmostEqual((bottom-top)*scale,target['visible_height_840'],delta=1,msg=(person,slot))
                    if height=='560':
                        # r13_question_close_y의 일반 원본 top110+12*(560/840)=118.
                        self.assertLessEqual(foot+118,708,(person,slot))
                        self.assertGreaterEqual(y+top*scale+118,130,(person,slot))
                self.assertLessEqual(max(feet)-min(feet),1.1,(person,height))

    def test_all_approved_front_sets_have_pixel_offsets_and_question_feet_inside_screen(self):
        for person,entry in self.people.items():
            if entry.get('status')!='approved_runtime':continue
            for profile in entry['profiles'].values():
                for frame in profile['frames'].values():
                    self.assertTrue(all(type(n) is int for n in frame['offset']),(person,frame['offset']))
            question=entry['profiles']['560']
            self.assertIs(type(question['question_top']),int)
            for slot,frame in question['frames'].items():
                with Image.open(ROOT/'game'/frame['file']) as image:
                    box=image.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
                feet=question['question_top']+frame['offset'][1]+box[3]*frame.get('scale',1)
                self.assertLessEqual(feet,708,(person,slot,feet))


if __name__=='__main__':unittest.main()
