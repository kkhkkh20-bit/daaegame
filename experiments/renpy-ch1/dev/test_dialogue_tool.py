"""Dialogue export/import keeps sources intact and refuses unsafe edits."""
import json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import dialogue_tool as tool
class DialogueTool(unittest.TestCase):
 def test_collects_lines_and_choices(self):
  rows=tool.collect()
  self.assertGreater(sum(r['kind']=='대사' for r in rows),3000)
  self.assertGreater(sum(r['kind']=='선택지' for r in rows),100)
  self.assertEqual(len({tool.row_id(r) for r in rows}),len(rows))
 def test_json_roundtrip_is_byte_identical(self):
  for name in tool.JSON_FILES:
   raw=(tool.GAME/name).read_text(encoding='utf-8')
   self.assertEqual(json.dumps(json.loads(raw),ensure_ascii=False,indent=2)+('\n' if raw.endswith('\n') else ''),raw)
 def test_unsafe_edits_rejected(self):
  nm=tool.names()
  self.assertEqual(nm.get('neoul'),'너울')
  self.assertIsNotNone(tool.check('[r13_pay]냥','(r13_pay)냥','대사',nm))
  self.assertIsNotNone(tool.check('너울이 왔다.','경비가 왔다.','대사',nm))
  self.assertIsNotNone(tool.check('짧다','가나다라마바사아자차카타파하가나다라마바사아자차카타','선택지',nm))
  self.assertIsNotNone(tool.check('한 줄','두\n줄','대사',nm))
  self.assertIsNone(tool.check('너울이 문을 연다.','너울이 문을 연다!','대사',nm))
if __name__=='__main__':unittest.main()
