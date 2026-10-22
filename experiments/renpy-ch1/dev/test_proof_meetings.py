"""0.20.6: R13_PROOF_MEETING matches the meeting whose chances each proof's wrong label spends."""
import re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class ProofMeetings(unittest.TestCase):
    def test_table_matches_wrong_labels(self):
        labels={}
        for f in sorted((ROOT/'game').glob('room13_v111_days*.rpy')):
            for block in re.split(r'\n(?=label )',f.read_text()):
                m=re.match(r'label (\w+)',block)
                if m:labels[m.group(1)]=block
        found={}
        for block in labels.values():
            for key,wrong in re.findall(r"r13_v111_proof\(\s*['\"]([^'\"]+)['\"]\s*,\s*\[[^\]]*\]\s*,\s*['\"]\w+['\"]\s*,\s*['\"](\w+)['\"]",block):
                m=re.search(r"r13_nw_retry\(\s*['\"](\w+)['\"]",labels.get(wrong,''))
                if m:found[key]=m.group(1)
        src=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
        table=src.split('R13_PROOF_MEETING={',1)[1].split('}',1)[0]
        declared=dict(re.findall(r'"([^"]+)":"(\w+)"',table))
        self.assertEqual(declared,found)
if __name__=='__main__':unittest.main()
