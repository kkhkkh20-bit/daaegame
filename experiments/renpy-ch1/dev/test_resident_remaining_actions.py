import json,unittest,hashlib
from PIL import Image
from test_map_action27 import environment,ROOT
from map27_pixel_derivative import validate_map_image
class ResidentActions(unittest.TestCase):
 def setUp(self):
  self.rows=[r for r in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'] if r['spec'].get('source_commit')=='69e8e718959253743e4440e71d47c6676ec581b1']
 def test_seven_originals_and_exports_no_duplicate_patrol(self):
  manifest=json.loads((ROOT/'art/approved-resident-actions-remaining7/manifest.json').read_text());self.assertEqual(len(manifest),7)
  files=set()
  for r in self.rows:
   m=next(m for m in manifest if m['sha256']==r['spec']['source_sha256']);p=ROOT/'art/approved-resident-actions-remaining7/originals'/m['file'].split('/')[-1]
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),m['sha256']);files.add(r['spec']['file'])
   with Image.open(ROOT/'game'/r['spec']['file']) as im:validate_map_image(im.convert('RGBA'))
  self.assertEqual(len(files),7)
  reg=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())
  self.assertEqual(sum(r['pose']=='map27_lantern_patrol' for r in reg['rows']),1)
 def test_all_variants_select_without_replacing_events_or_absent_people(self):
  env,a=environment();select=env['r13_map27_variant'];world=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
  for row in self.rows:
   for period in row['periods']:
    daylight=('morning','afternoon','evening')[period];v=row['variants'][daylight];layout=world[row['location']];width=layout['width'] if daylight in layout.get('periods',[daylight]) else 1280
    self.assertEqual(v['world_width'],width)
    state=dict(day=2,period=period,location=row['location'],flags=[]);actor=dict(a,person=row['person'],pose=row['replace_poses'][0])
    self.assertIsNotNone(select(row,actor,state,daylight,width,False))
    self.assertIsNone(select(row,actor,state,daylight,width,True))
    self.assertIsNone(select(row,dict(actor,pose='block_cart'),state,daylight,width,False))
  env['_r13_map27_stage']=lambda entry=False:[];env['R13_MAP_ACTION27']['rows']=self.rows;self.assertEqual(env['r13_stage_people'](),[])
if __name__=='__main__':unittest.main()
