"""Menu choices stay short (owner, 0.18.4): a summary of the action, not the full line."""
import re,unittest
from pathlib import Path
GAME=Path(__file__).resolve().parents[1]/'game'
LIMIT=24
CHOICE=re.compile(r'^\s+"([^"]+)"( if [^:]*)?:\s*$')
class ChoiceLength(unittest.TestCase):
 def test_choices_fit_one_line(self):
  long=[]
  for f in sorted(GAME.rglob('*.rpy')):
   if 'qa_tests' in f.parts:continue
   for n,line in enumerate(f.read_text(encoding='utf-8').splitlines(),1):
    m=CHOICE.match(line)
    if m:
     text=re.sub(r'\[[^\]]*\]','00',m.group(1))
     if len(text)>LIMIT:long.append('%s:%d %s'%(f.relative_to(GAME),n,m.group(1)))
  self.assertEqual(long,[],'shorten these choices (<=%d chars)'%LIMIT)
if __name__=='__main__':unittest.main()
