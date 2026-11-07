"""편지의 네 관찰 조작은 그림 밖에서 같은 크기로 보이며, 같은 관찰값을 돌려준다."""
import ast
from pathlib import Path
import re
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'game/systems/room13_proof_workspace.rpy').read_text()


class LetterObservationUI(unittest.TestCase):
    def setUp(self):
        self.env={}
        for block in re.findall(r'^init \d+ python:\n((?:[ \t].*\n|\n)*)',SOURCE,re.M):
            tree=ast.parse(textwrap.dedent(block))
            nodes=[node for node in tree.body if isinstance(node,ast.FunctionDef) and node.name=='r13_pw_observe_spots']
            if nodes:exec(compile(ast.Module(body=nodes,type_ignores=[]),'편지 관찰 버튼','exec'),self.env)

    def test_four_equal_buttons_share_one_row_inside_the_whole_pair(self):
        for width in (508,516,561,1080,1140):
            for height in (64,88):
                spots=self.env['r13_pw_observe_spots'](width,height)
                self.assertEqual([(key,name) for key,name,rect in spots],[('head','머리글'),('body','본문'),('tail','끝부분'),('margin','여백')])
                rects=[rect for key,name,rect in spots]
                for x,y,w,h in rects:
                    self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0)
                    self.assertLessEqual(x+w,width)
                    self.assertEqual(y,0)
                    self.assertLessEqual(y+h,height)
                    self.assertEqual(h,height)
                self.assertLessEqual(max(w for x,y,w,h in rects)-min(w for x,y,w,h in rects),1)
                for i,(ax,ay,aw,ah) in enumerate(rects):
                    for bx,by,bw,bh in rects[i+1:]:
                        self.assertTrue(ax+aw<=bx or bx+bw<=ax or ay+ah<=by or by+bh<=ay)

    def test_picture_has_no_overlapping_red_regions_or_labels(self):
        pair=SOURCE.split('screen r13_pw_pair(',1)[1].split('\nscreen ',1)[0]
        self.assertNotIn('#a63a2e22',pair)
        self.assertNotIn('#a63a2e55',pair)
        self.assertNotIn('text spot_name',pair)
        self.assertIn('ypos (y+h-observe_panel_h)',pair)
        self.assertIn('h-(top-y)-observe_panel_h-observe_gap',pair)
        self.assertIn('use r13_control(spot_name,None,Return(("observe",spot_id)),enabled=ready',pair)
        self.assertIn('control_id=r13_pw_id("r13_pw_spot_0_",spot_id)',pair)
        self.assertIn('observe_panel_h=observe_h if observe else 0',pair)
        self.assertIn('xpos x ypos (y+h-observe_panel_h) xysize (w,observe_panel_h)',pair)
        self.assertNotIn('r13_pw_spot_%d_',pair)


if __name__=='__main__':unittest.main()
