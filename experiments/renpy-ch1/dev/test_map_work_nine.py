import ast,json,textwrap,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'game/assets/room13-map-work-nine.json').read_text())
class MapWorkNine(unittest.TestCase):
 def test_files_and_map_only_geometry(self):
  self.assertEqual(len(DATA['people']),9)
  for r in DATA['people']:
   s=r['spec'];self.assertNotIn('native_detail',s);self.assertTrue(r['pose'].startswith('map9_'))
   with Image.open(ROOT/'game'/s['file']) as im:
    x,y,w,h=s['crop'];self.assertTrue(0<=x<x+w<=im.width and 0<=y<y+h<=im.height)
   self.assertGreater(s['stature_ratio'],0);self.assertLessEqual(s['stature_ratio'],1)
 def test_context_and_authored_event_guards(self):
  code=(ROOT/'game/systems/room13_map_work_nine.rpy').read_text().split('init 176 python:\n')[1];tree=ast.parse(textwrap.dedent(code));f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_map_work_nine_allowed');env={};exec(compile(ast.Module(body=[f],type_ignores=[]),'guard','exec'),env);allow=env[f.name]
  for r in DATA['people']:
   state=dict(day=11,location=r['location'],period=r['periods'][0]);a={'pose':'neutral'}
   self.assertTrue(allow(r,a,state));self.assertFalse(allow(r,a,state,True));self.assertFalse(allow(r,{'pose':'collapse_attendance'},state));self.assertFalse(allow(r,a,dict(state,location='gate')))
  p=DATA['people'][0];self.assertFalse(allow(p,{'pose':'neutral'},dict(day=10,location='clinic',period=0)))
 def test_piko_uniform_scale_and_shared_blanket_mask(self):
  p=next(r for r in DATA['people'] if r['person']=='resident_piko');c=p['contacts'];self.assertAlmostEqual(c['source_to_world_uniform_scale'],c['source_to_background_uniform_scale']*c['background_original_to_world_uniform_scale']);self.assertEqual(c['foreground_polygon_apply_to_image'],1);self.assertEqual(c['foreground_polygon_subtract_from_hit_mask'],1)
if __name__=='__main__':unittest.main()
