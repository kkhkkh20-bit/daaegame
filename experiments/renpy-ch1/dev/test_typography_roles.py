"""0.18.23 typography handoff: roles, thought parentheses once, authored item spans only, no bold."""
import json,re,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TOK=json.loads((ROOT/'game/assets/room13-typography-tokens.json').read_text())
def lum(h):
    rgb=[int(h[i:i+2],16)/255 for i in (1,3,5)]
    return sum(w*(x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4) for w,x in zip((.2126,.7152,.0722),rgb))
def contrast(a,b):
    la,lb=sorted((lum(a),lum(b)),reverse=True);return (la+.05)/(lb+.05)
class TypographyRoles(unittest.TestCase):
    def setUp(self):
        src=(ROOT/'game/systems/room13_typography_roles.rpy').read_text().split('init 140 python:\n')[1].split('\ninit 141:')[0]
        self.store=types.SimpleNamespace(room13_mode=True,r13_thought_active=False,r13_packet=('karo','x'))
        renpy=types.SimpleNamespace(loadable=lambda p:True,file=lambda p:open(ROOT/'game'/p,'rb'))
        self.env=dict(store=self.store,renpy=renpy,R13_UI_COLORS={},persistent=types.SimpleNamespace(room13_window_alpha='d4'),Frame=lambda *a,**k:('Frame',a))
        exec(textwrap.dedent(src),self.env)
        self.fn=self.env['r13_semantic_text']
    def test_no_automatic_names_and_no_bold(self):
        text='까로에게 초대 편지를 보여주자. 여관에서 밤이를 찾자.'
        self.assertEqual(self.fn(text),text)
        self.assertNotIn('{b}',self.fn('「예약 원본」에는 다람이 이름도 있다.'))
    def test_item_span_takes_entity_colour_only(self):
        out=self.fn('「예약 원본」에는 다람이 이름도 적혀 있습니다.')
        self.assertTrue(out.startswith('{color='+TOK['roles']['entity']['dark']+'}「예약 원본」{/color}'))
        self.assertEqual(re.sub(r'\{[^}]*\}','',out),'「예약 원본」에는 다람이 이름도 적혀 있습니다.')
    def test_long_quotes_stay_body_text(self):
        letter='「나는 편지를 보내 달라고 부탁한 적 없어. 내가 어디로 가는지 여관에는 말하지 마.」'
        self.assertEqual(self.fn(letter),letter)
    def test_thought_parentheses_exactly_once(self):
        self.store.r13_thought_active=True
        self.assertEqual(self.fn('(원본과 명부가 다르다.)'),'(원본과 명부가 다르다.)')
        self.assertEqual(self.fn('원본과 명부가 다르다.'),'(원본과 명부가 다르다.)')
        # a thought split across two pages keeps one pair per page
        self.assertEqual(self.fn('(첫 줄'),'(첫 줄)');self.assertEqual(self.fn('둘째 줄)'),'(둘째 줄)')
        self.assertNotIn('{color',self.fn('「예약 원본」을 다시 보자.'))
    def test_say_colour_by_role(self):
        c=self.env['r13_say_color'];roles=TOK['roles']
        self.assertEqual(c(),roles['speech']['dark'])
        self.store.r13_packet=(None,'x');self.assertEqual(c(),roles['narration']['dark'])
        self.store.r13_thought_active=True;self.assertEqual(c(),roles['thought']['dark'])
    def test_role_contrast_on_both_surfaces(self):
        for role,v in TOK['roles'].items():
            self.assertGreaterEqual(contrast(v['dark'],'#193a35'),4.5,role)
            self.assertGreaterEqual(contrast(v['paper'],'#efe7d2'),4.5,role)
    def test_no_synthetic_bold_in_room13_sources(self):
        hits=[]
        for p in list((ROOT/'game').glob('room13*.rpy'))+list((ROOT/'game/systems').glob('*.rpy')):
            for i,line in enumerate(p.read_text().splitlines(),1):
                if line.lstrip().startswith('#'):continue
                if '{b}' in line or re.search(r'\bbold\s*(True|=\s*True)',line):hits.append('%s:%d'%(p.name,i))
        self.assertEqual(hits,[])
if __name__=='__main__':unittest.main()
