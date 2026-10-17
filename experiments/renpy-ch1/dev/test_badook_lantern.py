import json,unittest
from test_map_action27 import environment,ROOT
from PIL import Image
from map27_pixel_derivative import validate_map_image
class BadookPatrol(unittest.TestCase):
 def test_night_patrol_preserves_authored_events_and_schedule(self):
  row=next(r for r in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'] if r['request_id']=='VA-1')
  env,actor=environment();actor.update(person='resident_badook',pose='living_bootlace');choose=env['r13_map27_variant'];state=dict(day=2,period=2,location='square',flags=[])
  self.assertIsNotNone(choose(row,actor,state,'evening',1920,False))
  self.assertIsNone(choose(row,actor,state,'evening',1920,True))
  for pose in ('block_cart','neutral','event_guard'):
   self.assertIsNone(choose(row,dict(actor,pose=pose),state,'evening',1920,False))
  for period in (0,1):self.assertIsNone(choose(row,actor,dict(state,period=period),'evening',1920,False))
  self.assertIsNone(choose(row,actor,dict(state,location='school'),'evening',1920,False))
  env['_r13_map27_stage']=lambda entry=False:[];env['R13_MAP_ACTION27']['rows']=[row];self.assertEqual(env['r13_stage_people'](),[])
  with Image.open(ROOT/'game'/row['spec']['file']) as im:validate_map_image(im.convert('RGBA'))
if __name__=='__main__':unittest.main()
