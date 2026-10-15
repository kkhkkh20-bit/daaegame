"""Every per-line acting cue still points at its exact line (dev/line_cues.py --reanchor fixes drift)."""
import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import line_cues

class LineCues(unittest.TestCase):
    def test_no_stale_cues(self):
        left=line_cues.stale()
        self.assertEqual([],[(k,i,x,c["text"]) for k,i,x,c in left][:10],"run: python3 dev/line_cues.py --reanchor")

    def test_scenes_are_found(self):
        rows=line_cues.scene_rows()
        self.assertIn("trial:C2:wrong",rows)
        self.assertIn("topic:buri_records",rows)

if __name__=="__main__":
    unittest.main()
