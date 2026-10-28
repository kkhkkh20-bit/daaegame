"""2026-10-28 대조 화면 넘침(r13_proof_shown): 자료를 많이 골라도 카드가 패널 안 줄 수만큼만 그려지고 나머지는 한 칸으로 묶인다."""
import re,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def function(path,name,ns):
    # 이 init 블록은 뒤에 screen 이 붙어 통째로 파싱되지 않는다. 함수 하나만 잘라 읽는다.
    src=(ROOT/path).read_text(encoding='utf-8')
    m=re.search(r'^    def '+name+r'\(.*?(?=^    def |^\S)',src,re.M|re.S)
    exec(textwrap.dedent(m.group(0)),ns)

class ProofOverflow(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns=dict(R13_PROOF_CARD_GAP=8)
        function('game/room13_week2_screens.rpy','r13_proof_shown',cls.ns)

    def test_fits_shows_all(self):
        keys=['V111:E%02d'%i for i in range(6)]
        self.assertEqual(self.ns['r13_proof_shown'](keys,2,64,300),(keys,0))

    def test_overflow_keeps_last_cell_for_summary(self):
        keys=['V111:E%02d'%i for i in range(40)]
        shown,hidden=self.ns['r13_proof_shown'](keys,2,64,300)   # 300 칸에 64+8 → 4줄 · 8칸
        self.assertEqual(len(shown),7);self.assertEqual(hidden,33)
        self.assertEqual(shown,keys[:7])
        rows=-(-(len(shown)+1)//2)
        self.assertLessEqual(rows*64+(rows-1)*8,300)

if __name__=='__main__':unittest.main()

class ChipFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ns={}
        function('game/systems/room13_proof_workspace.rpy','r13_pw_chip_fit',cls.ns)
    def test_all_fit(self):
        self.assertEqual(self.ns['r13_pw_chip_fit']([100,100,100],80,60,500),3)
    def test_overflow_leaves_room_for_more_chip(self):
        n=self.ns['r13_pw_chip_fit']([150]*7,90,60,800)
        self.assertEqual(n,4)   # 90+4x158+8+60=790
        self.assertLessEqual(90+n*(150+8)+8+60,800)
