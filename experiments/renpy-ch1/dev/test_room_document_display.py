"""편지 끝그림이 읽히고, 원문·획득 상태·기존 자료를 바꾸지 않는지 확인한다."""
import ast
import copy
import json
from pathlib import Path
import re
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]


class RoomDocumentDisplay(unittest.TestCase):
    def environment(self,records):
        source=(ROOT/'game/systems/room13_room_documents.rpy').read_text().split('init 356 python:',1)[1]
        tree=ast.parse(textwrap.dedent(source))
        functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)]
        env=dict(_r13_room_document_re=re,r13_catalog_record=lambda key:records.get(key),
            r13_material_body=lambda record:record.get('establishes',''),r13_v111_active=lambda:True,
            _r13_room_documents_evidence_art_path=lambda key:'old:'+key,
            _r13_room_documents_material_art=lambda key:'old:'+key,
            _r13_room_documents_object_visible=lambda spec:True,
            Transform=lambda file,**kw:(file,kw))
        exec(compile(ast.Module(body=functions,type_ignores=[]),'방 서류 표시','exec'),env)
        return env

    def test_owned_memo_displays_its_mark_without_rewriting_record(self):
        records={'V111:E06':dict(establishes='초롱에게 물어봐. {image=assets/room13-acorn-ink-crooked.png}'),
                 'V111:E01':dict(establishes='다람이를 데리고 와 줘.')}
        before=copy.deepcopy(records);env=self.environment(records)
        memo=env['r13_room_document_original']('V111:E06')
        self.assertEqual(memo['text'],'초롱에게 물어봐.')
        self.assertEqual(memo['mark'],'assets/room13-acorn-ink-crooked.png')
        self.assertIsNone(env['r13_room_document_original']('V111:E01')['mark'])
        self.assertEqual(records,before)

    def test_missing_memo_has_no_marker_and_other_records_keep_their_text(self):
        env=self.environment({'V111:E27':dict(establishes='다른 원문 {image=example.png}')})
        self.assertEqual(env['r13_room_document_original']('V111:E06'),dict(text='',mark=None))
        self.assertEqual(env['r13_room_document_original']('V111:E27')['text'],'다른 원문 {image=example.png}')

    def test_removed_prop_has_no_phantom_target_and_family_art_matches(self):
        env=self.environment({})
        layout=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())['room13']
        self.assertFalse(any(p['file']=='assets/room13-under-desk-cloth-bundle.webp' for p in layout.get('props',[])))
        self.assertFalse(env['r13_object_visible'](dict(retired_room_bundle=True)))
        self.assertTrue(env['r13_object_visible'](dict(mother_note_spot=True)))
        self.assertEqual(env['r13_evidence_art_path']('V111:E30'),'assets/evidence/D01_FAMILY_DRAWING.webp')
        self.assertEqual(env['r13_material_art']('V111:E30')[0],'assets/evidence/D01_FAMILY_DRAWING.webp')
        env['r13_v111_active']=lambda:False
        self.assertTrue(env['r13_object_visible'](dict(retired_room_bundle=True)))
        self.assertEqual(env['r13_evidence_art_path']('legacy'),'old:legacy')


if __name__=='__main__':unittest.main()
