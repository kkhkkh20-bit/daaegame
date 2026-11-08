"""한 사람 회의에서 숨긴 좌석을 생성/예측하지 않는지 확인한다."""
import ast
from pathlib import Path
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]


class Node:
    def __init__(self,*args,**kwargs):self.args=args;self.kwargs=kwargs


class SoloLoading(unittest.TestCase):
    def environment(self,solo=True):
        people=['guard','daram','resident_kongi','neoul','resident_badook','resident_nero']
        built=[]
        def portrait(person,pose,height):built.append(person);return Node(person)
        env=dict(renpy=types.SimpleNamespace(Displayable=Node),R13_MEETING_SOLO=solo,
            R13_MEETING_BEATS={'listen':(0,0,0,0)},
            r13_debate_session=lambda claim:'field',r13_meeting_kind=lambda session:'field',
            r13_meeting_cast=lambda *args:[(person,'') for person in people],
            r13_meeting_plate=lambda *args:Node(),Transform=Node,Crop=Node,
            TintMatrix=lambda *args:1,SaturationMatrix=lambda *args:1,BrightnessMatrix=lambda *args:1,
            r13_meeting_orbit_height=lambda *args:840,r13_meeting_slot_art=lambda *args:None,
            r13_fullbody_close_art=portrait,r13_meeting_reaction_art=lambda person,pose,h,art:art,
            r13_dialogue_source_profile=lambda *args:{},r13_close_x=lambda *args:640,
            r13_meeting_portrait_y=lambda *args:100)
        source=(ROOT/'game/room13_meeting_camera.rpy').read_text().split('init 175 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        node=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='R13MeetingOrbit')
        exec(compile(ast.Module(body=[node],type_ignores=[]),'회의 그림 생성', 'exec'),env)
        return env,built,people

    def test_solo_builds_and_predicts_only_visible_person_but_keeps_seating_order(self):
        env,built,people=self.environment()
        shot=env['R13MeetingOrbit']('claim','resident_kongi',1,'listen',{})
        self.assertEqual(built,['resident_kongi'])
        self.assertEqual(shot.people,people)
        self.assertEqual(set(shot.art),{'resident_kongi'})
        self.assertEqual(set(shot.offsets),{'resident_kongi'})
        self.assertEqual(shot.visit(),[shot.pan_plate,shot.art['resident_kongi']])
        second=env['R13MeetingOrbit']('claim','guard',2,'listen',{})
        self.assertEqual(set(second.art),{'guard'})
        self.assertEqual(second.people,people)

    def test_multi_person_and_missing_focus_keep_existing_visible_cast(self):
        for solo,focus in ((False,'resident_kongi'),(True,'missing')):
            env,built,people=self.environment(solo)
            shot=env['R13MeetingOrbit']('claim',focus,1,'listen',{})
            self.assertEqual(built,people)
            self.assertEqual(set(shot.art),set(people))
            self.assertTrue(all(art in shot.visit() for art in shot.art.values()))


if __name__=='__main__':unittest.main()
