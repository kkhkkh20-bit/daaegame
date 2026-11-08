"""회의의 원본 여백이 아이 얼굴을 가리지 않고, 실제 장소 밖을 비추지 않는지 검증한다."""
import ast
import math
from pathlib import Path
import textwrap
import types
import unittest

from PIL import Image
import test_dialogue_size_fit as fitting

ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'


class MeetingPortraitGeometry(unittest.TestCase):
    def setUp(self):
        helper=fitting.DialogueSizeFit()
        helper.table=fitting.data('room13-dialogue-size-fit.json')
        self.env=helper.environment()
        self.env['store'].r13_meeting_active=True
        self.loads=[]
        def load(path):
            self.loads.append(path)
            with Image.open(GAME/path) as image:
                bounds=image.getchannel('A').point(lambda a:255 if a>=40 else 0).getbbox()
            rect=types.SimpleNamespace(top=bounds[1],bottom=bounds[3],height=bounds[3]-bounds[1])
            return types.SimpleNamespace(get_bounding_rect=lambda **kw:rect)
        self.env.update(_R13_MEETING_SOURCE_BOUNDS={},r13_fullbody_close_y=lambda *a:108,
                        r13_orbit_math=math)
        self.env['renpy'].display=types.SimpleNamespace(im=types.SimpleNamespace(Image=lambda path:types.SimpleNamespace(load=lambda:load(path))))
        source=(GAME/'room13_meeting_camera.rpy').read_text().split('init 175 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in {'r13_meeting_portrait_y','r13_meeting_background_x'}]
        exec(compile(ast.Module(body=funcs,type_ignores=[]),'회의 배치','exec'),self.env)

    def geometry(self,who):
        self.env['store'].r13_meeting_focus=who
        p=self.env['r13_dialogue_source_profile'](who,'neutral',840)
        f=p['frames']['neutral'];bounds=fitting.alpha_bounds(f['file'])
        y=self.env['r13_meeting_portrait_y'](who,840,96,'neutral')
        return p,y,f['offset'][1]+bounds[1]*f.get('scale',1),f['offset'][1]+bounds[3]*f.get('scale',1)

    def test_kongi_padding_cannot_place_face_below_dialogue(self):
        p,y,head,feet=self.geometry('resident_kongi')
        self.assertGreater(p['frames']['neutral']['offset'][1],300,'원래 여백을 가진 회귀 자료여야 한다')
        # 실제 solo 투영(1.06배)과 대사판 윗변 560을 함께 확인한다.
        projected_head=(y+head)*1.06+(1-1.06)*240
        self.assertGreater(projected_head,100)
        self.assertLess(projected_head,300)
        self.assertAlmostEqual(y+feet,760,delta=.51)

    def test_children_keep_authored_size_and_share_adult_floor(self):
        heads={}
        for who in ('resident_kongi','daram','bami','kid_kkomi','kid_dodam','v111_child','neoul','karo','resident_bori'):
            with self.subTest(person=who):
                p,y,head,feet=self.geometry(who)
                heads[who]=y+head
                self.assertGreaterEqual(heads[who],119.49)
                self.assertLess(heads[who],410)
                self.assertGreaterEqual(y+feet,759.49)
                # 위치 보정이 이미 승인된 source의 배율을 변경하지 않는다.
                original=self.env['R13_DIALOGUE_SIZE_FIT']['people'][who]['profiles']['840']
                self.assertIs(p,original)
        self.assertGreater(heads['resident_kongi'],heads['neoul']+100)
        self.assertGreater(heads['kid_dodam'],heads['resident_kongi'])

    def test_web_uses_shipped_bounds_when_surface_access_is_unavailable(self):
        def unsupported(*args):raise RuntimeError('웹 Surface 직접 읽기 불가')
        self.env['renpy'].display.im.Image=unsupported
        path=self.env['R13_DIALOGUE_SIZE_FIT']['people']['resident_kongi']['profiles']['840']['frames']['neutral']['file']
        self.env['_R13_MEETING_SOURCE_BOUNDS'][path]=None
        self.geometry('resident_kongi');self.geometry('resident_kongi')
        self.assertEqual(self.loads,[])
        for height in (740,840,876):
            self.env['store'].r13_meeting_focus='resident_kongi'
            profile=self.env['r13_dialogue_source_profile']('resident_kongi','neutral',height)
            frame=profile['frames']['neutral'];bounds=frame['source_alpha_bounds']
            y=self.env['r13_meeting_portrait_y']('resident_kongi',height,96,'neutral')
            feet=frame['offset'][1]+bounds[3]*frame.get('scale',1)
            self.assertAlmostEqual(y+feet,96+664*height/840,delta=.51)

    def test_pose_and_meeting_slot_placements_are_preserved(self):
        self.geometry('resident_kongi')
        self.env['store'].r13_meeting_art_slots={'resident_kongi':'reaction'}
        self.assertEqual(self.env['r13_meeting_portrait_y']('resident_kongi',840,96,'neutral'),108)
        self.env['store'].r13_meeting_art_slots={}
        self.env['r13_dialogue_source_profile']=lambda *a:{'frames':{}}
        self.assertEqual(self.env['r13_meeting_portrait_y']('seryeon',840,96,'chair_read'),108)

    def test_place_pan_stays_inside_one_picture_and_wraps_continuously(self):
        pan=self.env['r13_meeting_background_x']
        for count in (1,2,4,7,12):
            for n in range(-100,101):
                view=n/13
                x=pan(view,count,1440)
                self.assertLessEqual(x,0)
                self.assertGreaterEqual(x+1440,1280)
                self.assertAlmostEqual(x,pan(view+count,count,1440))
        self.assertAlmostEqual(pan(0,7,1440),pan(7,7,1440))


if __name__=='__main__':unittest.main()
