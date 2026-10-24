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
# 이번에 다시 쓰이게 한 10건 중 회의에 붙인 것과 새 사실 1건(E09 초상의 바늘):
# (문항, 덧붙인 자료, 그 자료를 짚는 조건 이름). 한 문항에 덧붙임이 둘 이상일 수 있다.
REUSED=[
    ("초롱과 피코의 하루를 대조한다","E28","hyp1_won_with_e28"),
    ("요즘 돌이 어디서 오는지 대조한다","E14","hyp3_won_with_e14"),
    ("반송·필사본·초대 발송을 대조한다","E27","writing_won_with_e27"),
    ("반송·필사본·초대 발송을 대조한다","E09","writing_won_with_e09"),
    ("아내가 봤다는 담요의 시점을 확인한다","E35","blanket_won_with_e35"),
    ("촌장이 어젯밤 있던 곳을 확인한다","E29","badook_won_with_e29"),
    ("장부의 두 배를 실룩에게 보인다","E34","piko_ledger_with_e34"),
    ("맨 처음 이름을 짚는다","NW_BURNT_PAGE","altar4_won_with_burnt_page"),
]
class EvidenceReuse(unittest.TestCase):
    def test_extras_and_alternates_point_at_real_records_and_proofs(self):
        for name in ('R13_PROOF_EXTRAS','R13_PROOF_ALTERNATES'):
            body=table(name)
            for key in re.findall(r'^\s*"([^"]+)":',body,re.M):self.assertIn(key,PROOF_KEYS,(name,key))
            for rec in re.findall(r'"([A-Z][A-Z0-9_]+)"',body):self.assertIn(rec,EV,(name,rec))
    def test_reused_records_are_declared_with_their_line_condition(self):
        extras=table('R13_PROOF_EXTRAS')
        for key,rec,when in REUSED:
            line=next(l for l in extras.splitlines() if l.strip().startswith('"%s":'%key))
            self.assertIn('"%s"'%rec,line,key)
            self.assertRegex(TEXT,r'"%s":lambda:"V111:%s" in \(r13_v111_value\("proof_given:%s"\)'%(re.escape(when),rec,re.escape(key)))
            used=[f.name for f in (GAME/'v111/newworld').glob('d*.json') if '"when": "%s"'%when in f.read_text()]
            self.assertTrue(used,when)
    def test_records_alternate_keeps_invitation_and_mail_order(self):
        body=table('R13_PROOF_ALTERNATES')
        self.assertIn('"반송·필사본·초대 발송을 대조한다":(("E01","E27","E09_MAIL"),)',body)
        # E09(초상)는 덧붙임만이다. 피코는 엄마를 앞에 두고 그리지 않았으므로 대체 세트가 될 수 없다.
        self.assertNotIn('"E09"',body)
    def test_portrait_needle_is_set_up_before_day10(self):
        """2일에 다람이 바늘을 주문하고, 3일 두 판(피코 생존·사망) 모두 그림 속 바늘이 보인 뒤에 10일에 짚는다."""
        def day(n):return json.loads((GAME/('v111/newworld/d%02d.json'%n)).read_text())
        d2,d3,d10=day(2),day(3),day(10)
        self.assertIn('바늘',' '.join(r['text'] for r in d2['after']['MS14_D02_S03_L0018']))
        self.assertIn('바늘을 쥐고',' '.join(r['text'] for r in d3['after']['MS14_D03_S01_L0036']))   # 피코 생존
        self.assertIn('손까지는 다 그려져',' '.join(r['text'] for r in d3['after']['MS14_D03_S01_L9101']))  # 피코 사망
        for v in d3['evidence']['E09']['variants'].values():self.assertIn('바늘',v)
        facts=json.loads((GAME/'v111/evidence-facts.json').read_text())['E09']
        for lines in facts.values():self.assertLessEqual(len(lines),3);self.assertTrue(any('바늘' in l for l in lines))
        rows=d10['after']['MS14_D10_P01_L0032']
        self.assertTrue(rows and all(r.get('when')=='writing_won_with_e09' for r in rows))
        # 그림은 그날의 손을 증명하지 못한다: 아빠는 「그날 아프지 않았다」고 말하지 않는다.
        self.assertNotIn('그날',' '.join(r['text'] for r in rows))
if __name__=='__main__':unittest.main()
