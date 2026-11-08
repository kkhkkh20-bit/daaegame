"""담당자와 물건의 두 진입이 같은 장면 조건과 원래 index를 지키는지 확인한다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import textwrap
import unittest

ROOT=Path(__file__).resolve().parents[1]

class FieldContextActions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        source=(ROOT/'game/room13_v111.rpy').read_text()
        block=source.split('init 301 python:\n',1)[1].split('\nlabel ',1)[0]
        tree=ast.parse(textwrap.dedent(block))
        names={'r13_v111_person_object','r13_v111_object_caption','r13_v111_direct_topic'}
        cls.env={}
        exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names],type_ignores=[]),'조사 연결','exec'),cls.env)
        cls.bindings=json.loads((ROOT/'game/v111/field-bindings.json').read_text())

    def binding(self,gate):
        binding=copy.deepcopy(self.bindings[gate])
        binding['options']=[dict(o,index=o.get('index',i)) for i,o in enumerate(binding['options'])]
        return binding

    def test_person_approach_reuses_original_object_index(self):
        choose=self.env['r13_v111_person_object']
        for gate in ('look_gate4','board6','handoff6','school_names7'):
            b=self.binding(gate)
            before=copy.deepcopy(b)
            for person,entry in b['approach'].items():
                expected=next(o['index'] for o in b['options'] if o.get('object')==entry['object'])
                self.assertEqual(choose(b,person,b['location']),(expected,entry['question']))
                self.assertIsNone(choose(b,person,'elsewhere'))
            self.assertIsNone(choose(b,'not_here',b['location']))
            self.assertEqual(b,before)

    def test_hidden_or_ambiguous_object_cannot_be_started_by_person(self):
        choose=self.env['r13_v111_person_object']
        b=self.binding('handoff6')
        b['options']=[]
        self.assertIsNone(choose(b,'resident_teacher','school'))
        b=self.binding('handoff6')
        b['options']*=2
        self.assertIsNone(choose(b,'resident_teacher','school'))

    def test_context_caption_does_not_rename_other_places_or_old_campaign(self):
        b=self.binding('inspect_gate4')
        self.env.update(store=SimpleNamespace(room13=dict(location='gate',v111=dict(gate='inspect_gate4'))),
                        r13_v111_active=lambda:True,r13_v111_binding=lambda:b,r13_v111_value=lambda key:None)
        caption=self.env['r13_v111_object_caption']
        self.assertEqual(caption('road'),'고갯길 · 겹친 발자국')
        self.assertIsNone(caption('table'))
        self.env['store'].room13['location']='dining'
        self.assertIsNone(caption('road'))
        self.env['r13_v111_active']=lambda:False
        self.assertIsNone(caption('road'))

    def test_can_caption_changes_after_observation_and_recovery(self):
        values={}
        self.env.update(store=SimpleNamespace(room13=dict(location='v111_woodshed',v111=dict(gate='afternoon6'))),
                        r13_v111_active=lambda:True,r13_v111_binding=lambda:self.binding('afternoon6'),
                        r13_v111_value=values.get)
        caption=self.env['r13_v111_object_caption']
        self.assertEqual(caption('v111_can'),'깡통 줄 · 살피기')
        values['kkomi_can_seen6']=True
        self.assertEqual(caption('v111_can'),'깡통 줄 · 풀어 챙기기')
        values['acorn_recovered']=True
        self.assertEqual(caption('v111_can'),'깡통 줄 · 회수함')

    def test_single_opted_in_question_runs_only_its_original_integer_action(self):
        choose=self.env['r13_v111_direct_topic']
        for gate,person in [('bori_witness7','resident_bori'),('nubi_children_receipt7','resident_teacher'),('hp_meal6','daram')]:
            b=self.binding(gate)
            o=next(o for o in b['options'] if o.get('person')==person)
            q=[(o['title'],SimpleNamespace(value=o['index']),False)]
            self.assertEqual(choose(gate,person,b['location'],b['options'],q,b['direct_people']),o['index'])
            self.assertIsNone(choose(gate,person,b['location'],b['options'],q))
            q.append(('추가 질문',SimpleNamespace(value=('followup','new')),False))
            self.assertIsNone(choose(gate,person,b['location'],b['options'],q,b['direct_people']))

    def test_direct_metadata_never_submits_evidence_or_chooses_a_branch(self):
        choose=self.env['r13_v111_direct_topic']
        b=self.binding('reply_handoff5');person='resident_lamplighter'
        q=[(b['options'][0]['title'],SimpleNamespace(value=0),False)]
        self.assertIsNone(choose('reply_handoff5',person,'gate',b['options'],q,[person]))
        b=self.binding('afternoon6');person='kid_kkomi'
        q=[('학교에 같이 가자',SimpleNamespace(value=1),False),('내일 데리러 올게',SimpleNamespace(value=2),False)]
        self.assertIsNone(choose('afternoon6',person,'v111_woodshed',b['options'],q,[person]))

if __name__=='__main__':unittest.main()
