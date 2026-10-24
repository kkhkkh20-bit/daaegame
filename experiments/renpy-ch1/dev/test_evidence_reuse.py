"""2026-10-24 자료 재사용(docs/design/EVIDENCE_CLUTTER_PLAN.md 2부): 덧붙임·대체 세트가 실제 자료와
실제 회의 문항을 가리키는지, 덧붙인 자료를 짚는 줄의 조건이 정의돼 있는지 오프라인으로 확인한다."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
GAME=ROOT/'game'
RULES=(GAME/'room13_v111_newworld_rules.rpy').read_text()
TEXT=(GAME/'room13_v111_newworld_text.rpy').read_text()
EV=set(json.loads((GAME/'v111/records.json').read_text())['evidence'])
for f in (GAME/'v111/newworld').glob('d*.json'):EV|=set(json.loads(f.read_text()).get('new_evidence',{}))
def table(name):
    return RULES.split(name+'={',1)[1].split('\n    }',1)[0]
PROOF_KEYS=set(re.findall(r"call r13_v111_proof\(\s*['\"]([^'\"]+)['\"]",''.join(f.read_text() for f in GAME.glob('room13_v111_days*.rpy'))))
# 이번에 다시 쓰이게 한 10건 중 회의에 붙인 것: 문항 -> 덧붙인 자료와 그 자료를 짚는 조건 이름
REUSED={
    "초롱과 피코의 하루를 대조한다":("E28","hyp1_won_with_e28"),
    "요즘 돌이 어디서 오는지 대조한다":("E14","hyp3_won_with_e14"),
    "반송·필사본·초대 발송을 대조한다":("E27","writing_won_with_e27"),
    "아내가 봤다는 담요의 시점을 확인한다":("E35","blanket_won_with_e35"),
    "촌장이 어젯밤 있던 곳을 확인한다":("E29","badook_won_with_e29"),
    "장부의 두 배를 실룩에게 보인다":("E34","piko_ledger_with_e34"),
    "맨 처음 이름을 짚는다":("NW_BURNT_PAGE","altar4_won_with_burnt_page"),
}
class EvidenceReuse(unittest.TestCase):
    def test_extras_and_alternates_point_at_real_records_and_proofs(self):
        for name in ('R13_PROOF_EXTRAS','R13_PROOF_ALTERNATES'):
            body=table(name)
            for key in re.findall(r'^\s*"([^"]+)":',body,re.M):self.assertIn(key,PROOF_KEYS,(name,key))
            for rec in re.findall(r'"([A-Z][A-Z0-9_]+)"',body):self.assertIn(rec,EV,(name,rec))
    def test_reused_records_are_declared_with_their_line_condition(self):
        extras=table('R13_PROOF_EXTRAS')
        for key,(rec,when) in REUSED.items():
            line=next(l for l in extras.splitlines() if l.strip().startswith('"%s":'%key))
            self.assertIn('"%s"'%rec,line,key)
            self.assertRegex(TEXT,r'"%s":lambda:"V111:%s" in \(r13_v111_value\("proof_given:%s"\)'%(re.escape(when),rec,re.escape(key)))
            used=[f.name for f in (GAME/'v111/newworld').glob('d*.json') if '"when": "%s"'%when in f.read_text()]
            self.assertTrue(used,when)
    def test_records_alternate_keeps_invitation_and_mail_order(self):
        body=table('R13_PROOF_ALTERNATES')
        self.assertIn('"반송·필사본·초대 발송을 대조한다":(("E01","E27","E09_MAIL"),)',body)
if __name__=='__main__':unittest.main()
