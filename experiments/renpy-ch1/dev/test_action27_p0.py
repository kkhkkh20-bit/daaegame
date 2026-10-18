import hashlib,json,unittest
from pathlib import Path
from PIL import Image
from map27_pixel_derivative import validate_map_image
ROOT=Path(__file__).resolve().parents[1]
class Action27P0(unittest.TestCase):
 def test_originals_export_and_registry_match(self):
  receipt=json.loads((ROOT/'art/approved-action27-p0/receipt.json').read_text());reg=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text());self.assertEqual(len(receipt['rows']),8);self.assertEqual({r['request_id'] for r in reg['rows'] if r['request_id'] in {x['request_id'] for x in receipt['rows']}},{'MK-2','MK-3','MK-4','MK-5','MK-6','PO-1','SQ-2','WS-1'})
  for r in receipt['rows']:
   src=ROOT/r['source'];self.assertEqual(hashlib.sha256(src.read_bytes()).hexdigest(),r['source_sha256']);self.assertEqual(src.stat().st_size,r['source_bytes']);self.assertEqual(Image.open(src).size,(1024,1536))
   out=ROOT/'game'/r['export'];self.assertEqual(hashlib.sha256(out.read_bytes()).hexdigest(),r['export_sha256']);validate_map_image(Image.open(out).convert('RGBA'))
   row=next(x for x in reg['rows'] if x['request_id']==r['request_id']);self.assertEqual(row['spec']['source_sha256'],r['source_sha256']);self.assertEqual(bool(row['spec'].get('native_detail',False)),r['request_id']=='SQ-2');self.assertEqual(row['spec']['crop'],[0,0,512,768])
 def test_scene_variants_and_prior_action_scope(self):
  rows=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'];sling=next(r for r in rows if r['request_id']=='PO-1')
  self.assertEqual([sling['variants'][p]['world_width'] for p in ['morning','afternoon','evening']],[2160,1280,1280])
  self.assertEqual(next(r for r in rows if r['request_id']=='SQ-2')['max_day'],10)
  for r in rows:
   if r['request_id'] not in {'MK-2','MK-3','MK-4','MK-5','MK-6','PO-1','SQ-2','WS-1'}:continue
   self.assertNotIn('event_steam',r['replace_poses']);self.assertNotIn('event_paintwipe',r['replace_poses']);self.assertNotIn('work_herb_bundle',r['replace_poses'])
   self.assertNotIn(r['person'],['neoul','nabi'])
   for v in r['variants'].values():
    self.assertTrue(0<=v['target'][0]<v['world_width']);self.assertTrue(0<=v['target'][1]<720);self.assertTrue(v['occlusion']);self.assertIn(v['anchor'],r['spec']['anchors'])
 def test_green_cravat_retained_without_palette_reduction(self):
  row=next(r for r in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'] if r['request_id']=='MK-2');im=Image.open(ROOT/'game'/row['spec']['file']).convert('RGBA')
  # Actual approved scarf region, before the smaller map renderer. Keep chromatic green.
  pixels=list(im.crop((250,140,370,300)).getdata());greens=[p for p in pixels if p[3]>128 and p[1]>p[0]*1.15 and p[1]>p[2]*1.15]
  self.assertGreater(len(greens),40)
if __name__=='__main__':unittest.main()
