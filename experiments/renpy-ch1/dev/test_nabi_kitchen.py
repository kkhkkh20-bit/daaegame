"""Approved routine boundaries, one daily action, and immutable originals."""
import copy,hashlib,json,unittest
from pathlib import Path
from PIL import Image
import r13_timeline_env
from qa_room13_rules import load_rules
from map27_pixel_derivative import validate_map_image
from test_map_action27 import environment
ROOT=Path(__file__).resolve().parents[1]
class NabiKitchen(unittest.TestCase):
 def test_arrival_serving_and_evacuation_have_priority(self):
  n=load_rules();s=n['store'];base=copy.deepcopy(s.room13)
  for day in range(1,15):
   for period in range(4):
    for granny,flags in [('trusted',[]),('detained',[]),('trusted',['shelter_ready']),('detained',['shelter_ready'])]:
     s.room13=copy.deepcopy(base);s.room13.update(day=day,period=period,granny_state=granny,flags=flags);before=copy.deepcopy(s.room13)
     actual=n['r13_where']('nabi')
     expected='kitchen' if day>=2 and period==0 else 'dining'
     if day>=11:
      if granny=='detained' and period==0:expected='inn'
      elif 'shelter_ready' in flags:expected='school'
     self.assertEqual(actual,expected,(day,period,granny,flags));self.assertEqual(s.room13,before)
 def test_one_map_pose_per_kitchen_morning_and_no_serving_override(self):
  rows=[r for r in json.loads((ROOT/'game/assets/room13-map-action27.json').read_text())['rows'] if r['person']=='nabi'];self.assertEqual(len(rows),5)
  env,_=environment();select=env['r13_map27_variant'];actor=dict(person='nabi',pose='neutral');seen=set()
  for day in range(1,15):
   for period in range(3):
    state=dict(day=day,period=period,location='kitchen',flags=[])
    chosen=[r for r in rows if select(r,actor,state,['morning','afternoon','evening'][period],2160,False)]
    self.assertEqual(len(chosen),1 if day>=2 and period==0 else 0)
    seen.update(r['request_id'] for r in chosen)
    for r in rows:
     self.assertIsNone(select(r,actor,dict(state,location='dining'),'morning',2160,False))
     self.assertIsNone(select(r,actor,state,'morning',2160,True))
  self.assertEqual(seen,{'KI-1','KI-2','KI-3','KI-4','KI-5'})
 def test_four_exact_originals_and_distinct_outputs(self):
  receipts=json.loads((ROOT/'art/approved-nabi-kitchen-extra4/receipt.json').read_text())['rows'];self.assertEqual(len(receipts),4);self.assertEqual(len({r['source_sha256'] for r in receipts}),4)
  for r in receipts:
   p=ROOT/r['source'];self.assertEqual(p.stat().st_size,r['source_bytes']);self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),r['source_sha256'])
   with Image.open(p) as im:self.assertEqual(list(im.size),r['source_size'])
   out=ROOT/'game'/r['export'];self.assertEqual(hashlib.sha256(out.read_bytes()).hexdigest(),r['export_sha256'])
   with Image.open(out) as im:validate_map_image(im.convert('RGBA'))
  reg=json.loads((ROOT/'game/assets/room13-map-action27.json').read_text());self.assertEqual(len({r['request_id'] for r in reg['rows']}),31)
if __name__=='__main__':unittest.main()
