import ast, re, unittest, os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(os.environ.get('R13_BASE_GAME',str(ROOT/'base-game')))
if not BASE.exists(): BASE=ROOT/'game'
class SourceTests(unittest.TestCase):
 def test_init_blocks_compile_and_legal_priority(self):
  for p in (ROOT/'game/systems').glob('room13_recommended*.rpy'):
   lines=p.read_text().splitlines();i=0
   while i<len(lines):
    m=re.match(r'init (\d+) python:',lines[i])
    if not m:i+=1;continue
    self.assertLessEqual(int(m[1]),999);i+=1;body=[]
    while i<len(lines) and (lines[i].startswith('    ') or not lines[i].strip()):
     body.append(lines[i][4:]);i+=1
    ast.parse('\n'.join(body),filename=str(p))
 def test_declared_speakers_exist(self):
  import recommended_model as m
  base='\n'.join(p.read_text() for p in BASE.rglob('*.rpy'))
  residents=(BASE/'village-residents.json').read_text()
  for action in m.r13_rec_actions.values():
   for who,*rest in action['lines']:
    if who:self.assertIn(who,base+residents)
 def test_native_and_story_separate(self):
  p=ROOT/'game/qa_tests/recommended_story.rpy'
  self.assertIn('testcase recommended_story_first_slice',p.read_text())
  self.assertNotIn('testcase ',(ROOT/'game/systems/room13_recommended_story.rpy').read_text())
 def test_legacy_starts_not_replaced(self):
  before=(BASE/'screens.rpy').read_text();after=(ROOT/'game/screens.rpy').read_text()
  self.assertEqual(before.count('action Start()'),after.count('action Start()'))
  self.assertIn('Start("r13_recommended_start")',after)
 def test_no_reserved_init_priority(self):
  for p in (ROOT/'game').rglob('*.rpy'):
   for v in re.findall(r'^init (-?\d+)',p.read_text(),re.M):self.assertTrue(-999<=int(v)<=999)
 def test_generation_is_exact(self):
  s=(ROOT/'game/systems/room13_recommended_story.rpy').read_text()
  body='\n'.join('    '+l for l in (ROOT/'dev/recommended_model.py').read_text().splitlines())
  self.assertIn(body,s)
 def test_no_meta_notes_in_player_dialogue(self):
  s=(ROOT/'game/systems/room13_recommended_story.rpy').read_text()
  self.assertNotIn('이후 사건의 증언에서 사라지거나 구금된 상태로 현장에 다시 등장하지 않는다',s)
  self.assertIn('call screen r13_recommended_setup',s)
 def test_field_reuses_scene_and_question_ui(self):
  s=(ROOT/'game/systems/room13_recommended_field.rpy').read_text()
  self.assertIn('call r13_scene(',s);self.assertIn('use r13_question_list(',s)
  self.assertIn('r13_staged_visible_art(',s);self.assertIn('target:',s)

if __name__=='__main__':unittest.main()

class ReviewRegressionGuards(unittest.TestCase):
 def test_care_before_empty_cart_and_prior_custody_procedure(self):
  s=(ROOT/'game/systems/room13_recommended_ep23.rpy').read_text()
  self.assertLess(s.index("if 'e2_care_complete' not in"),s.index('빈 수레의 끈'))
  self.assertIn("r13_rec_apply(r13_recommended,'e2_care')",s)
  self.assertIn('public_custody_procedure_heard',s)
 def test_no_development_verdict_in_dad_voice(self):
  s=(ROOT/'dev/recommended_ep23_model.py').read_text()
  self.assertNotIn('부분 해결로 다음 사건을 진행',s)
  self.assertNotIn('검증된 연속 시야와 실제 입력',s)
 def test_world_targets_paginate_without_offscreen_fifth_actor(self):
  s=(ROOT/'game/systems/room13_recommended_field.rpy').read_text()
  self.assertIn('targets[page_start:page_start+4]',s)
  self.assertIn('190+slot*290',s)
