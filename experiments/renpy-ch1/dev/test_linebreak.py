"""Dialogue line breaks: one sentence per line, long lines split near the middle."""
import re,textwrap,types,unittest
from pathlib import Path
src=(Path(__file__).resolve().parents[1]/'game/systems/room13_linebreak.rpy').read_text(encoding='utf-8')
block=textwrap.dedent(src.split('init 112 python:\n',1)[1].split('    _r13_lb_prev_filter')[0])
env={'persistent':types.SimpleNamespace(room13_large_text=False)}
exec(block,env)
f=env['r13_dialogue_lines']
class LineBreak(unittest.TestCase):
 def test_sentences_on_own_lines(self):
  self.assertEqual(f('안에서 잠겨 있었습니다. 안에는 다람 양이 있었습니다.'),'안에서 잠겨 있었습니다.\n안에는 다람 양이 있었습니다.')
 def test_short_untouched(self):
  self.assertEqual(f('……그래서요?'),'……그래서요?')
  self.assertEqual(f('톡의 편을 든다'),'톡의 편을 든다')
 def test_long_sentence_split_in_two(self):
  out=f('까로가 가방을 내려놓고 마차 바퀴 밑을 살피는 동안 나는 다람이의 손을 잡고 조심스럽게 발판에서 내렸다')
  self.assertEqual(out.count('\n'),1)
  self.assertTrue(all(len(l)<=35 for l in out.split('\n')))
 def test_four_lines_paged_two_by_two(self):
  pages=env['r13_dialogue_pages']('첫 문장입니다. 둘째 문장입니다. 셋째 문장입니다. 넷째 문장입니다.')
  self.assertEqual(pages,['첫 문장입니다.\n둘째 문장입니다.','셋째 문장입니다.\n넷째 문장입니다.'])
  # 0.18.39: the window is two lines tall; a third line goes to the next click.
  self.assertEqual(env['r13_dialogue_pages']('하나. 둘. 셋.'),['하나.\n둘.','셋.'])
  long=env['r13_dialogue_pages']('팔의 상처만으로는 목숨을 앗아 간 머리 상처를 설명할 수 없습니다. 떨어져 나간 촛대 윗부분이 다시 쓰였습니다. 그 사이 아이가 어디 있었는지, 누가 다른 길로 드나들었는지 함께 봐야 합니다.')
  self.assertTrue(all(p.count('\n')<=1 for p in long))
  self.assertTrue(long[0].endswith('없습니다.') and long[-1].endswith('합니다.'))
 def test_tags_kept_whole(self):
  out=f('{color=#fff}{b}서리 검사원{/b}{/color}이 장부를 덮고 창밖을 보았다. 바람이 세졌다.')
  self.assertIn('{color=#fff}{b}서리 검사원{/b}{/color}',out)
  self.assertEqual(out.count('\n'),1)
if __name__=='__main__':unittest.main()
