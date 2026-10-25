"""미수판은 실재하는 자료만 쓰며 준비·채취·매입을 섞지 않는다."""
import ast,itertools,json,re,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class LampAttempt(unittest.TestCase):
    def setUp(self):
        self.bindings=json.loads((ROOT/'game/v111/field-bindings.json').read_text())
        self.data=json.loads((ROOT/'game/v111/newworld/lamp_attempt.json').read_text())
    def visible(self,key,values):
        return [o for o in self.bindings[key]['options'] if all(values.get(k)==want for kind,k,want in o.get('guard',[]))]
    def test_cord_and_inspection_both_required_to_bind(self):
        for cord,seen in itertools.product((None,True),repeat=2):
            options=self.visible('lamp_prep2',dict(lamp_cord2=cord,lamp_latch_seen2=seen))
            self.assertEqual(any('감아' in o['title'] for o in options),cord is True and seen is True)
    def test_meeting_waits_for_all_actual_investigation(self):
        for bits in itertools.product((None,True),repeat=3):
            values=dict(zip(('lamp_field_done3','lamp_knife_done3','lamp_store_done3'),bits))
            self.assertEqual(any('공방' in o['title'] for o in self.visible('lamp_attempt_field3',values)),all(bits))
    def test_original_stolen_records_cannot_prove_attempt(self):
        text=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text().split('init 318 python:',1)[-1]
        tree=ast.parse(textwrap.dedent(text.split('\nlabel ',1)[0]))
        funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ('r13_v111_proof_sets','r13_v111_proof_accepts')]
        env=dict(R13_PROOF_ALTERNATES={},R13_PROOF_EXTRAS={})
        exec(compile(ast.Module(body=funcs,type_ignores=[]),'<proof>','exec'),env)
        need=['NW_LA_CHECK','NW_LA_FIELD','NW_LA_KNIFE'];f=env['r13_v111_proof_accepts']
        self.assertTrue(f('남아 있는 돌과 칼의 사용을 연결한다',need,['V111:'+k for k in need]))
        self.assertFalse(f('남아 있는 돌과 칼의 사용을 연결한다',need,['V111:E15','V111:E16']))
        self.assertFalse(f('남아 있는 돌과 칼의 사용을 연결한다',need,['V111:'+k for k in need]+['V111:E16']))
    def test_attempt_does_not_grant_stolen_records(self):
        s=(ROOT/'game/room13_lamp_attempt.rpy').read_text()
        self.assertNotRegex(s,r"(?:key=|r13_nw_acquire\()['\"]E1[56]")
        self.assertIn("jump r13_lamp_attempt_repair3",(ROOT/'game/room13_v111_days123.rpy').read_text().split('label r13_v111_trial_repair:',1)[1].split('label ',1)[0])
    def test_13th_day_uses_actual_unpaid_offer(self):
        s=(ROOT/'game/room13_v111_days1114.rpy').read_text()
        self.assertIn("['NW_LA_OFFER']",s)
        self.assertIn('인수·대금 지급은 없다',self.data['new_evidence']['NW_LA_OFFER']['variants']['observed'])
if __name__=='__main__':unittest.main()
