"""Selected gate art and geometry preserve underlying investigation facts."""
import hashlib,json,unittest,os
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class GatePanorama(unittest.TestCase):
 def test_selected_native_art_present_and_uniform_aspect(self):
  # Art lives in game/assets in its web form (dev/import_art.py); the designer
  # originals are recorded in dev/selected_asset_overlay.json for provenance.
  from PIL import Image
  layout=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())['gate']
  self.assertEqual(set(layout['files']),{'morning','afternoon','evening'})
  for rel in layout['files'].values():
   self.assertIn('gate0173',rel)
   with Image.open(ROOT/'game'/rel) as image:w,h=image.size
   self.assertEqual((w,h),(2048,768));self.assertEqual(w*layout['height'],h*layout['width'])
 def test_rectangles_inside_world_and_every_old_object_retained(self):
  layout=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())['gate'];content=json.loads((ROOT/'game/room13-content.json').read_text())
  self.assertEqual(set(layout['objects']),set(content['objects']['gate']))
  for x,y,w,h in list(layout['objects'].values())+[layout['documents'],layout['documents_crop']]:
   self.assertGreater(w,0);self.assertGreater(h,0);self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0);self.assertLessEqual(x+w,layout['width']);self.assertLessEqual(y+h,layout['height'])
 def test_document_and_notice_targets_keep_authoritative_keys(self):
  src=(ROOT/'game/room13_gate_inspection.rpy').read_text();self.assertIn('layout["documents_crop"]',src);self.assertIn('r13_world_background("gate")',src)
  actions=(ROOT/'game/room13_interaction.rpy').read_text();self.assertIn('("gate","rules"):("interview",)',actions)
if __name__=='__main__':unittest.main()
