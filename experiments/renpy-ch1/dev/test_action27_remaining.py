"""Source integrity, variable-canvas contacts, and activation boundaries."""
import hashlib,json,unittest
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import validate_map_image
from test_map_action27 import environment
ROOT=Path(__file__).resolve().parents[1]
class RemainingActions(unittest.TestCase):
 def setUp(self):self.rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows']
 def test_all_sources_preserved_and_variable_dimensions_supported(self):
  receipt=json.loads((ROOT/'art/approved-action27-remaining/receipt.json').read_text())['rows'];self.assertEqual(len(receipt),19);self.assertEqual(len({r['request_id'] for r in self.rows}),27)
  for r in receipt:
   src=ROOT/r['source'];self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),r['source_sha256']);self.assertEqual(src.stat().st_size,r['source_bytes'])
   with Image.open(src) as im:self.assertEqual(list(im.size),r['source_size'])
   dest=ROOT/'game'/r['export'];self.assertEqual(hashlib.sha256(dest.read_bytes()).hexdigest(),r['export_sha256'])
   with Image.open(dest) as im:validate_map_image(im.convert('RGBA'))
   row=next(x for x in self.rows if x['request_id']==r['request_id']);self.assertEqual(row['spec']['crop'][2:],r['transform']['export_size'])
 def test_reviewed_contacts_use_one_scale(self):
  env,actor=environment()
  for row in self.rows:
   for v in row['variants'].values():
    out=env['r13_map27_geometry'](actor,row['spec'],v,v['world_width']);self.assertGreater(out['rect'][2],0)
    self.assertLessEqual(out['rect'][0]+out['rect'][2],v['world_width'])
 def test_nabi_has_no_schedule_and_neoul_is_map_only(self):
  nabi=next(r for r in self.rows if r['request_id']=='KI-1');self.assertEqual(nabi['periods'],[]);self.assertEqual(nabi['activation'],'preview_only_no_existing_kitchen_schedule')
  for r in self.rows:
   if r['person']=='neoul':self.assertIn(r['location'],['gate','facility']);self.assertEqual(r['usage'],'map_only')
   self.assertFalse(any(p.startswith('event_') for p in r['replace_poses']))
  piko=next(r for r in self.rows if r['request_id']=='CL-1');self.assertEqual(piko['min_day'],11)
  for v in piko['variants'].values():self.assertEqual(v['anchor'],'seat');self.assertEqual(v['occlusion'],[])
if __name__=='__main__':unittest.main()
