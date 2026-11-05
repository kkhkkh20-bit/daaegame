"""사망 확인 직후의 질문·인사는 생존 장면과 구별하고 진행·증거·시간을 바꾸지 않는다."""
import ast
import copy
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

ROOT=Path(__file__).resolve().parents[1]
IDLE=(ROOT/'game/room13_v111_idle.rpy').read_text()
REACTION=(ROOT/'game/room13_v111_reactions.rpy').read_text()
DATA=json.loads((ROOT/'game/v111/newworld/reactions.json').read_text())
NAMES={'아빠':'dad','다람':'daram','초롱':'resident_lamplighter','톡':'resident_tok','돌목':'guard','너울':'neoul'}

def block(source,priority):
    body=source.split('init %s python:\n'%priority,1)[1].split('\ninit ',1)[0]
    return '\n'.join(line[4:] if line.startswith('    ') else line for line in body.splitlines())

class PikoMourning(unittest.TestCase):
    def make(self,alive=False,day=3,scene='MS14_D03_S02',location='square'):
        state=dict(day=day,location=location,evidence=['V111:E11'],records={},arguments={},
                   v111=dict(scene=scene,people=['resident_lamplighter'],values={'piko_alive':alive,'elapsed_minutes':20}))
        values=state['v111']['values'];calls=[]
        env=dict(store=SimpleNamespace(room13=state),MS14_SPEAKERS=NAMES,
                 r13_v111_value=lambda key:values.get(key),r13_v111_set=lambda key,value:values.__setitem__(key,value),
                 r13_nw_added_line=lambda row:dict(row),r13_day2_idle_guidance=lambda person:None,
                 r13_v111_idle_lines=lambda person:calls.append(person) or [('old',person)],r13_met_people=lambda:[],
                 r13_v111_has_business=lambda person:False)
        exec(compile(block(IDLE,350),'다람의 현장 응답','exec'),env)
        exec(compile(block(IDLE,351),'사건 문맥','exec'),env)
        env.update(R13_REACTIONS=copy.deepcopy(DATA),r13_v111_owned=lambda key:'V111:'+key in state['evidence'],
                   r13_reaction_day_ok=lambda spec:spec['days'][0]<=state['day']<=spec['days'][-1],
                   r13_v111_person_alive=lambda person:True,Return=lambda value:SimpleNamespace(value=value),
                   _r13_reaction_questions=lambda person:[])
        tree=ast.parse(block(REACTION,335))
        names={'r13_followup_read','r13_v111_followups','r13_v111_followup_display','r13_v111_questions','r13_v111_followup_lines','r13_reaction_packets'}
        nodes=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names]
        exec(compile(ast.Module(body=nodes,type_ignores=[]),'사건 후속 질문','exec'),env)
        return env,state,calls

    def test_confirmed_death_only_in_its_day_and_nearby_scenes(self):
        for alive,day,scene,place in [(True,3,'MS14_D03_S02','square'),(None,3,'MS14_D03_S02','square'),
                                     (False,2,'MS14_D03_S02','square'),(False,3,'MS14_D03_S03','clinic'),
                                     (False,4,'MS14_D03_S02','square')]:
            with self.subTest(alive=alive,day=day,scene=scene,place=place):
                env,_,_=self.make(alive,day,scene,place);self.assertIsNone(env['r13_v111_tense_context']())
        env,_,_=self.make();self.assertEqual(env['r13_v111_tense_context'](),'piko')

    def test_new_and_known_residents_do_not_start_workday_chatter_at_body(self):
        env,state,calls=self.make();before=copy.deepcopy(state)
        for person in ['resident_lamplighter','resident_tok','guard','neoul']:
            rows=env['r13_v111_idle_lines'](person)
            self.assertEqual([r['speaker'] for r in rows],['아빠',next(n for n,p in NAMES.items() if p==person)])
            self.assertTrue(all(r['expression']=='anxious' for r in rows))
            self.assertNotIn('안녕하세요',''.join(r['text'] for r in rows))
        self.assertEqual(calls,[])
        self.assertEqual(state['evidence'],before['evidence']);self.assertEqual(state['records'],before['records'])
        self.assertEqual(state['arguments'],before['arguments']);self.assertEqual(state['v111']['values']['elapsed_minutes'],20)
        self.assertFalse(state['v111']['values']['piko_alive'])
        self.assertEqual(env['r13_v111_idle_lines']('resident_lamplighter')[0]['kind'],'thought')

    def test_saved_piko_route_keeps_normal_idle_and_child_response(self):
        env,_,calls=self.make(alive=True)
        self.assertEqual(env['r13_v111_idle_lines']('resident_lamplighter'),[('old','resident_lamplighter')])
        self.assertEqual(calls,['resident_lamplighter'])
        self.assertEqual(env['r13_v111_daram_hello']()[0]['expression'],'neutral')
        env,_,_=self.make();self.assertEqual(env['r13_v111_daram_hello']()[0]['expression'],'anxious')

    def test_other_existing_crisis_stops_first_meeting_chatter_too(self):
        env,state,calls=self.make(alive=True,day=7,scene='MS14_D07_S02',location='square')
        self.assertEqual(env['r13_v111_tense_context'](),'event')
        self.assertEqual(env['r13_v111_idle_lines']('resident_lamplighter')[0]['kind'],'thought')
        self.assertEqual(calls,[])

    def test_mourning_question_keeps_owned_gate_id_and_read_state(self):
        env,state,_=self.make();before=copy.deepcopy(state)
        questions=env['r13_v111_questions']('resident_lamplighter');self.assertEqual(len(questions),1)
        self.assertIn('초롱 씨',questions[0][0]);self.assertEqual(questions[0][1].value,('followup','NW_RX_F008'))
        self.assertEqual(state,before)
        lines=env['r13_v111_followup_lines']('NW_RX_F008')
        self.assertTrue(all(r['expression']=='anxious' for r in lines));self.assertIn('3번, 돌 3',lines[1]['text'])
        self.assertIn('새벽 종 직전 점검 완료',lines[1]['text']);self.assertIn('따로 말씀드린',lines[2]['text'])
        self.assertTrue(state['v111']['values']['followup_read:NW_RX_F008'])
        self.assertTrue(env['r13_v111_questions']('resident_lamplighter')[0][2])
        state['evidence'].clear();self.assertEqual(env['r13_v111_questions']('resident_lamplighter'),[])

    def test_alive_and_later_followup_keep_original_title_and_expression(self):
        for alive,scene,place in [(True,'MS14_D03_S02','square'),(False,'MS14_D03_S03','clinic')]:
            env,_,_=self.make(alive=alive,scene=scene,location=place)
            self.assertIn('종이에 쓴 것만',env['r13_v111_questions']('resident_lamplighter')[0][0])
            self.assertTrue(all(r['expression']=='neutral' for r in env['r13_v111_followup_lines']('NW_RX_F008')))

    def test_generic_lamplighter_reply_loses_smile_only_in_grief_context(self):
        rows=[dict(speaker='초롱',text='그건 제가 확인한 게 아니에요.',expression='neutral')]
        env,_,_=self.make();self.assertEqual(env['r13_reaction_packets'](rows)[0]['expression'],'anxious')
        self.assertEqual(rows[0]['expression'],'neutral')
        env,_,_=self.make(alive=True);self.assertEqual(env['r13_reaction_packets'](rows)[0]['expression'],'neutral')

if __name__=='__main__':unittest.main()
