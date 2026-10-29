"""Selected panorama artifacts and new geometry retain all original investigation targets."""
import unittest,json,hashlib,os
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
PLACES=('clinic','store','greenhouse','facility','altar')
class SelectedWorlds(unittest.TestCase):
 def test_all_original_object_keys_and_bounds(self):
  content=json.loads((ROOT/'game/room13-content.json').read_text());layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
  for place in PLACES:
   spec=layouts[place];self.assertEqual(set(spec['objects']),set(content['objects'][place]));self.assertEqual(set(spec['files']),{'morning','afternoon','evening'})
   for rect in list(spec['objects'].values())+spec['critical']:
    self.assertTrue(all(isinstance(v,(int,float)) for v in rect))
    x,y,w,h=rect;self.assertTrue(x>=0 and y>=0 and w>0 and h>0 and x+w<=1920 and y+h<=720,(place,rect))
 def test_selected_art_present_and_uniform_fit(self):
  layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
  rels=[layouts[place]['files'][t] for place in PLACES for t in ('morning','afternoon','evening')];self.assertEqual(len(rels),15)
  for rel in rels:
   # 2026-10-29: 창고는 다시 그린 BG-STORE-2(바닥선·소품 크기)로 바꿨다. 같은 2048x768·같은 조사 물건 자리.
   self.assertTrue('0177' in rel or rel.startswith('assets/room13-bg-store-2-'),rel)
   with Image.open(ROOT/'game'/rel) as im:self.assertEqual(im.size,(2048,768))
 def test_held_room_assets_not_selected(self):
  rows=json.loads((ROOT/'dev/selected_asset_overlay.json').read_text())['files'];self.assertFalse(any('room-after' in r['source'] or 'room-before' in r['source'] for r in rows))
if __name__=='__main__':unittest.main()
