"""1부의 종료 자격·현재 사실 요약·완료 저장은 원래 분기 결과를 보존한다."""
import ast
import copy
import json
import textwrap
import unittest
from pathlib import Path
from types import SimpleNamespace

ROOT=Path(__file__).resolve().parents[1]
SOURCE=(ROOT/'game/room13_part1.rpy').read_text()


def helpers(values=None,day=7):
    values=copy.deepcopy(values or {})
    room={'day':day,'v111':{'values':values}}
    ns=dict(store=SimpleNamespace(room13=room),R13_PART1_PUBLIC=True,r13_v111_active=lambda:True,
            r13_v111_value=lambda k:values.get(k),r13_v111_set=lambda k,v:values.__setitem__(k,v),
            r13_v111_binding=lambda:{'options':[]})
    tree=ast.parse(textwrap.dedent(SOURCE.split('init 370 python:\n',1)[1].split('\nlabel ',1)[0]))
    nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name!='r13_v111_binding']
    exec(compile(ast.Module(body=nodes,type_ignores=[]),'1부 도우미','exec'),ns)
    return ns,room,values


class Part1Boundary(unittest.TestCase):
    def complete(self,**overrides):
        return dict({'meeting:fire':'win','D07_S02_handover_completed':True,'D07_S02_message_completed':True},**overrides)

    def test_only_settled_fire_and_actual_handover_reach_the_boundary(self):
        for outcome in ('win','partial','lose'):
            ns,room,v=helpers(self.complete(**{'meeting:fire':outcome}))
            before=copy.deepcopy(room)
            self.assertTrue(ns['r13_part1_ready']())
            self.assertEqual(room,before)
        for missing in ('meeting:fire','D07_S02_handover_completed','D07_S02_message_completed'):
            v=self.complete();v.pop(missing)
            self.assertFalse(helpers(v)[0]['r13_part1_ready']())
        for day in (1,6,8,14):self.assertFalse(helpers(self.complete(),day)[0]['r13_part1_ready']())

    def test_summaries_respect_verdict_and_empty_warehouse(self):
        for outcome in ('win','partial','lose'):
            for evacuated in (False,True):
                ns,room,v=helpers(self.complete(**{'meeting:fire':outcome,'FIRE_EVACUATED':evacuated,'E07_OWL_CONTACT':'13호_부엉이','KKOMI_ALIVE':False}))
                before=copy.deepcopy(room);text=' '.join(ns['r13_part1_records'](v))
                if outcome=='partial':self.assertIn('감춘 죄',text)
                elif outcome=='lose':self.assertIn('자백을 얻지 못했다',text)
                elif evacuated:self.assertIn('빈 창고의 불을 끈 것',text);self.assertNotIn('아이들을 구하고',text)
                else:self.assertIn('아이들을 구하고 불을 끈 것',text)
                self.assertNotIn('네 아이 모두',text)
                self.assertNotIn('저녁을 먹었다',text)
                self.assertIn('현재 위치는 아직 모른다',text)
                self.assertEqual(room,before)

    def test_grand_proof_needs_actual_document_flag(self):
        ns,_,v=helpers(self.complete())
        self.assertNotIn('배급표',' '.join(ns['r13_part1_records'](v)))
        v['neoul_promise_proven']=True
        self.assertIn('배급표',' '.join(ns['r13_part1_records'](v)))

    def test_finished_save_is_written_once_and_failure_does_not_claim_success(self):
        ns,room,v=helpers(self.complete(part1_completed=True));saved=[]
        ns['renpy']=SimpleNamespace(retain_after_load=lambda:None,take_screenshot=lambda:None,save=lambda *a,**kw:saved.append(a[0]),restart_interaction=lambda:None,log=lambda x:None)
        ns['r13_part1_save']();ns['r13_part1_save']()
        self.assertEqual(saved,['part1-clear']);self.assertTrue(v['part1_checkpoint_written'])
        v['part1_checkpoint_written']=False
        def fail(*args,**kwargs):raise OSError('시험용 저장 실패')
        ns['renpy'].save=fail;ns['r13_part1_save']()
        self.assertFalse(v['part1_checkpoint_written']);self.assertTrue(ns['store'].r13_part1_save_failed)

    def test_incomplete_story_cannot_write_a_finished_save(self):
        ns,_,v=helpers(self.complete());saved=[]
        ns['renpy']=SimpleNamespace(retain_after_load=lambda:None,take_screenshot=lambda:None,save=lambda *a,**kw:saved.append(a),restart_interaction=lambda:None)
        ns['r13_part1_save']();self.assertEqual(saved,[])
        self.assertNotIn('part1_checkpoint_written',v)

    def test_continuation_stays_before_the_existing_night(self):
        source=(ROOT/'game/room13_v111_owl_prevent.rpy').read_text().split('label r13_v111_free_evening7:',1)[1].split('\n# ',1)[0]
        self.assertLess(source.index('call r13_part1_finish'),source.index("r13_nw_block('free_evening7')"))
        self.assertNotIn('day8',source)
        data=json.loads((ROOT/'game/v111/newworld/d07.json').read_text())
        self.assertNotIn('곧 데리러',str(data['replace']['MS14_D07_S02_L0022']))
        self.assertNotIn('저녁을 먹는 것',str(data['replace']['MS14_D07_S02_L0010']))

if __name__=='__main__':unittest.main()
