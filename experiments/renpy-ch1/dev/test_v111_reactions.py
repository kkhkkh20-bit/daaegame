"""Owner plan item 3 (2026-10-22): residents react to found evidence. Data checks, offline."""
import json,re,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'game/v111/newworld/reactions.json').read_text())
REC=json.loads((ROOT/'game/v111/records.json').read_text())
EV=set(REC['evidence'])
for f in (ROOT/'game/v111/newworld').glob('d*.json'):EV|=set(json.loads(f.read_text()).get('new_evidence',{}))
NAMES={}
for f in ('game/ms14_story.rpy','game/room13_v111_later_bindings.rpy'):
 for block in re.findall(r'MS14_SPEAKERS(?: = |\.update\()\{(.*?)\}',(ROOT/f).read_text(),re.S):NAMES.update(dict(re.findall(r'"([^"]+)":"([a-z0-9_]+)"',block)))
class Reactions(unittest.TestCase):
 def test_references_exist(self):
  people=set(NAMES.values())
  for spec in DATA['present']+DATA['followups']:
   self.assertIn(spec['person'],people);self.assertIn(spec.get('evidence',spec.get('after')),EV)
   self.assertTrue(1<=spec['days'][0]<=spec['days'][-1]<=14,spec)
   for row in spec['lines']:
    self.assertTrue(row['speaker'] is None or row['speaker'] in NAMES,row);self.assertTrue(row['text'])
  for person in DATA['generic']:self.assertIn(person,people)
 def test_followup_ids_unique_and_titles_short(self):
  ids=[s['id'] for s in DATA['followups']];self.assertEqual(len(ids),len(set(ids)))
  for s in DATA['followups']:self.assertLessEqual(len(s['title']),30,s['title'])
 def test_no_line_points_at_the_acorn(self):
  # Owner: the player finds the acorn on mom's letters; nobody points at it.
  for spec in DATA['present']+DATA['followups']:
   for row in spec['lines']+[dict(text=spec.get('title',''))]:self.assertNotIn('도토리',row['text'],spec)
   self.assertFalse(spec.get('after')=='E06' and '그림' in spec.get('title',''),spec)
 def test_engine_hooks_in_place(self):
  src=(ROOT/'game/room13_v111.rpy').read_text()
  self.assertIn('r13_v111_present_reaction(v111_person,v111_shown)',src)
  self.assertIn('r13_v111_followup_lines(v111_follow)',src)
if __name__=='__main__':unittest.main()
