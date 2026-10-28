"""2026-10-28 사슬 맨 끝 겹침 풀기(r13_separate_overlaps_final): 물건 회피가 옮긴 사람이 남과 다시 겹치면 평행이동으로 푼다.
기본 길 13일 광장(엄마→까로 옆)·4일 입구(바둑이→초롱 옆) 계측값으로 확인한다."""
import unittest
from pathlib import Path
from test_additional_field_layout import functions
ROOT=Path(__file__).resolve().parents[1]

def heavy(a,b):
    ax,ay,aw,ah=a;bx,by,bw,bh=b
    return min(ax+aw,bx+bw)-max(ax,bx)>0.55*min(aw,bw) and min(ay+ah,by+bh)-max(ay,by)>0.5*min(ah,bh)

def actor(person,rect,slot=False,contact='standing'):
    x,y,w,h=rect
    return dict(person=person,pose='n',x=x,y=y,width=w,height=h,rect=list(rect),depth=y+h,slot=slot,contact=contact)

class OverlapFinal(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns=dict(r13_world_offset=lambda:640,r13_view_width=lambda:1280)
        for path,names in [('game/systems/room13_investigation_balance.rpy',{'r13_balance_translate'}),
                           ('game/room13_v111_field_layout.rpy',{'r13_separate_overlaps_final','r13_foot_in_keepout','r13_keepout_cover_rects'})]:
            exec(compile(functions(path,names),path,'exec'),cls.ns)

    def test_square_day13_mom_leaves_karo(self):
        rows=[actor('mom',(1048,407,128,210),True),actor('resident_hyeoni',(1280,409,132,210)),actor('resident_badook',(1369,480,200,159),True),
              actor('guard',(1162,440,115,210)),actor('resident_seol',(758,456,115,210)),actor('resident_lamplighter',(194,466,101,211),True),
              actor('karo',(1003,525,127,166),True),actor('resident_tosil',(1652,541,82,165),True)]
        critical=[(598,269,170,236),(861,475,121,52),(904,270,187,201),(326,420,282,144)]
        out=self.ns['r13_separate_overlaps_final'](rows,critical,1920)
        self.assertTrue(heavy(rows[0]['rect'],rows[6]['rect']))
        for i,a in enumerate(out):
            for b in out[i+1:]:
                self.assertFalse(heavy(a['rect'],b['rect']),(a['person'],b['person'],a['rect'],b['rect']))
        for old,new in zip(rows,out):
            self.assertEqual(old['y'],new['y']);self.assertEqual(old['height'],new['height'])
        moved=[a['person'] for a,b in zip(rows,out) if a['rect']!=b['rect']]
        self.assertEqual(moved,['mom'])   # 빈 자리(slot) 사람인 엄마가 비키고 까로(고정 자리)는 그대로다

    def test_fixed_contact_person_does_not_move(self):
        rows=[actor('a',(500,400,120,220),contact='bench_sit'),actor('b',(520,410,120,220),True)]
        out=self.ns['r13_separate_overlaps_final'](rows,[],1920)
        self.assertEqual(out[0]['rect'],rows[0]['rect']);self.assertFalse(heavy(out[0]['rect'],out[1]['rect']))

    def test_visible_person_stays_in_view_when_a_spot_exists(self):
        rows=[actor('a',(1800,400,120,220)),actor('b',(1820,410,120,220),True)]
        out=self.ns['r13_separate_overlaps_final'](rows,[],1920)
        self.assertFalse(heavy(out[0]['rect'],out[1]['rect']))
        self.assertLessEqual(out[1]['rect'][0]+out[1]['rect'][2],1920+40)

if __name__=='__main__':unittest.main()
