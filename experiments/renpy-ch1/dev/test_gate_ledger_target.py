"""입구 그림의 장부 중앙을 누르면 큰 서류 대신 장부가 선택되는지 확인한다."""
import copy
import json
from pathlib import Path
import textwrap
import types
import unittest

ROOT=Path(__file__).resolve().parents[1]


def pointed_object(objects,point):
    x,y=point
    for key,spec in reversed(list(objects.items())):
        ox,oy,ow,oh=spec["rect"]
        if ox<=x<ox+ow and oy<=y<oy+oh:
            return key


class GateLedgerTarget(unittest.TestCase):
    def setup_objects(self):
        content=json.loads((ROOT/'game/room13-content.json').read_text())
        layout=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())['gate']
        objects=copy.deepcopy(content['objects']['gate'])
        for key,rect in layout['objects'].items():
            objects[key]['rect']=list(rect)
        objects['gate_documents']=dict(rect=list(layout['documents']),inspection_bundle='gate_documents')
        return objects

    def install(self,objects):
        callbacks=[]
        env=dict(ROOM13=dict(objects=dict(gate=objects)),
                 config=types.SimpleNamespace(after_load_callbacks=callbacks))
        source=(ROOT/'game/systems/room13_gate_ledger_target.rpy').read_text().split('init 363 python:',1)[1]
        exec(textwrap.dedent(source),env)
        return env,callbacks

    def test_real_layout_book_center_no_longer_opens_the_covering_shelf(self):
        objects=self.setup_objects()
        x,y,w,h=objects['ledger']['rect'];point=(x+w/2,y+h/2)
        self.assertEqual(pointed_object(objects,point),'gate_documents')
        before=copy.deepcopy(objects)
        self.install(objects)
        self.assertEqual(pointed_object(objects,point),'ledger')
        self.assertEqual(objects,before)
        # 원본 묶음의 책 바깥 부분과 규칙판은 여전히 각 지점을 누른다.
        dx,dy,dw,dh=objects['gate_documents']['rect']
        self.assertEqual(pointed_object(objects,(dx+2,dy+2)),'gate_documents')
        rx,ry,rw,rh=objects['rules']['rect']
        self.assertEqual(pointed_object(objects,(rx+rw/2,ry+rh/2)),'rules')

    def test_wide_gate_camera_and_zoom_keep_the_same_book_target(self):
        objects=self.setup_objects()
        # 현행 넓은 입구의 평행이동과 0.75배 현장/오른쪽 카메라를 재현한다.
        for spec in objects.values():
            rect=spec['rect'];spec['rect']=[rect[0]+320,rect[1]+200]+rect[2:]
        self.install(objects)
        point=(752.25,491.25)
        world=(point[0]/.75+760,point[1]/.75)
        self.assertEqual(pointed_object(objects,world),'ledger')

    def test_loaded_old_order_repairs_without_replacing_specs(self):
        objects=self.setup_objects();book=objects['ledger'];shelf=objects['gate_documents']
        env,callbacks=self.install(objects)
        objects['gate_documents']=objects.pop('gate_documents')
        x,y,w,h=book['rect'];point=(x+w/2,y+h/2)
        self.assertEqual(pointed_object(objects,point),'gate_documents')
        callbacks[0]()
        self.assertEqual(pointed_object(objects,point),'ledger')
        self.assertIs(objects['ledger'],book);self.assertIs(objects['gate_documents'],shelf)
        keys=list(objects);callbacks[0]();self.assertEqual(list(objects),keys)

    def test_missing_gate_does_not_add_a_fake_object(self):
        objects={};env,callbacks=self.install(objects);callbacks[0]()
        self.assertEqual(objects,{})


if __name__=='__main__':unittest.main()
