"""Authored icon coverage, cell isolation/alpha, and pure lookup contract."""
import copy,json,textwrap,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
class MaterialArt(unittest.TestCase):
 def setUp(self):
  self.data=json.loads((ROOT/'game/assets/room13-material-icons079.json').read_text())
 def test_covers_catalog_objects_and_records_without_replacing_portraits(self):
  catalog=json.loads((ROOT/'art/material-icons-20261016/catalog.json').read_text())
  expected={k for k,v in catalog['evidence'].items() if v['kind']!='증언' and k!='P01'}
  expected|={'bag:'+k for k in set(catalog['shop'])|set(catalog['borrow'])}
  expected|={'tool:'+k for k in catalog['tools']}
  self.assertEqual(set(self.data['icons']),expected)
  self.assertNotIn('P01',self.data['icons'])
  self.assertTrue(all(k not in self.data['icons'] for k,v in catalog['evidence'].items() if v['kind']=='증언'))
 def test_rectangles_are_unique_in_bounds_and_have_transparent_margins(self):
  seen=set()
  for key,spec in self.data['icons'].items():
   x,y,w,h=spec['crop'];signature=(spec['file'],x,y,w,h)
   self.assertNotIn(signature,seen,key);seen.add(signature)
   with Image.open(ROOT/'game'/spec['file']) as im:
    self.assertGreaterEqual(x,0);self.assertGreaterEqual(y,0);self.assertGreater(w,40);self.assertGreater(h,40)
    self.assertLessEqual(x+w,im.width);self.assertLessEqual(y+h,im.height)
    self.assertIn('A',im.getbands(),key)
    alpha=im.crop((x,y,x+w,y+h)).getchannel('A')
    self.assertEqual(alpha.getextrema(),(0,255),key)
    coverage=sum(alpha.histogram()[1:])/(w*h)
    self.assertGreater(coverage,.025,key);self.assertLess(coverage,.995,key)
    for point in ((0,0),(w-1,0),(0,h-1),(w-1,h-1)):
     self.assertLess(alpha.getpixel(point),128,(key,point))
 def test_art_lookup_is_read_only_and_unknown_keys_keep_fallback(self):
  icons=self.data['icons'];before=copy.deepcopy(icons)
  env=dict(R13_MATERIAL_ART=icons,Crop=lambda rect,file:(rect,file),Transform=lambda art,**options:(art,options))
  src=(ROOT/'game/systems/room13_material_art.rpy').read_text().split('    def r13_material_art',1)[1]
  exec(textwrap.dedent('    def r13_material_art'+src),env)
  for key,spec in icons.items():self.assertEqual(env['r13_material_art'](key),((tuple(spec['crop']),spec['file']),dict(xysize=(64,64),fit='contain',nearest=True)))
  self.assertIsNone(env['r13_material_art']('unknown:new-future-item'))
  self.assertEqual(icons,before)
if __name__=='__main__':unittest.main()
