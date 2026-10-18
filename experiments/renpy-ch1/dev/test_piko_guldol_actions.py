import json,unittest,hashlib
from PIL import Image
from test_map_action27 import environment,ROOT
from map27_pixel_derivative import validate_map_image
from investigation_canonical_overlay import receipt, restored_registries, run as validate_canonical_overlay
class OccupationActions(unittest.TestCase):
 def setUp(self):
  # Verify current14 exact source/export hashes and18 specs before legacy reconstruction.
  validate_canonical_overlay(ROOT)
  current={name:json.loads((ROOT/'game'/name).read_text()) for name in ('assets/room13-pixel-acting.json','assets/room13-map-action27.json')}
  legacy=restored_registries(current,receipt(ROOT))['assets/room13-map-action27.json']['rows']
  self.rows=[r for r in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'] if r['request_id'] in ('VA-2','VA-3','VA-4','VA-5')]
  self.legacy_rows=[r for r in legacy if r['request_id'] in ('VA-2','VA-3','VA-4','VA-5')]
 def test_originals_and_common_pixel_exports(self):
  manifest=json.loads((ROOT/'art/approved-piko-guldol-four/manifest.json').read_text());self.assertEqual(len(self.rows),4)
  for r in self.legacy_rows:
   m=next(m for m in manifest if m['sha256']==r['spec']['source_sha256'])
   p=ROOT/'art/approved-piko-guldol-four/originals'/m['file'].split('/')[-1]
   self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),m['sha256'])
   with Image.open(ROOT/'game'/r['spec']['file']) as im:validate_map_image(im.convert('RGBA'))
 def test_day_variation_and_patient_event_protection(self):
  env,a=environment();choose=env['r13_map27_variant'];seen=set()
  for day in range(1,15):
   state=dict(day=day,period=1,location='square',flags=[]);actor=dict(a,person='resident_piko',pose='neutral')
   selected=[r for r in self.rows if choose(r,actor,state,'afternoon',1920,False)]
   self.assertEqual(len(selected),1 if day<=10 else 0)
   seen.update(r['request_id'] for r in selected)
   for r in self.rows:
    self.assertIsNone(choose(r,actor,state,'afternoon',1920,True))
    self.assertIsNone(choose(r,dict(actor,pose='map27_cl_1'),dict(state,location='clinic'),'afternoon',1920,False))
  self.assertEqual(seen,{'VA-2','VA-3'})
 def test_guldol_uses_only_existing_square_idle_and_workshop_job(self):
  env,a=environment();choose=env['r13_map27_variant'];state=dict(day=2,period=0,location='workshop',flags=[])
  r=next(r for r in self.rows if r['request_id']=='VA-5');actor=dict(a,person='resident_guldol',pose='map9_stone_tapping')
  self.assertIsNotNone(choose(r,actor,state,'morning',1800,False))
  self.assertIsNone(choose(r,dict(actor,pose='event_stone'),state,'morning',1800,False))
  self.assertIsNone(choose(r,actor,state,'morning',1800,True))
  env['_r13_map27_stage']=lambda entry=False:[];env['R13_MAP_ACTION27']['rows']=self.rows;self.assertEqual(env['r13_stage_people'](),[])
if __name__=='__main__':unittest.main()

