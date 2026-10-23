"""A04: final-stage HUD clearance on measured 0.20.14 day-2 actors."""
import ast,copy,json,re,textwrap,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def functions(path,names):
 source=(ROOT/path).read_text();blocks=re.split(r'^init[^\n]*:\n',source,flags=re.M)[1:]
 nodes=[]
 for block in blocks:
  try:tree=ast.parse(textwrap.dedent(block))
  except SyntaxError:continue
  nodes.extend(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in names)
 return ast.Module(body=nodes,type_ignores=[])

def overlap(a,b):
 return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))

def face(a):
 x,y,w,h=a['head_relative'];return [a['x']+x,a['y']+y,w,h]

class AdditionalFieldLayout(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.cases=json.loads((ROOT/'dev/fixtures/additional-field-layout014.json').read_text())['cases']
  cls.ns=dict(r13_actor_face_target=face)
  for path,names in [('game/systems/room13_investigation_balance.rpy',{'r13_balance_translate'}),('game/room13_v111_field_layout.rpy',{'r13_clear_field_hud'})]:
   exec(compile(functions(path,names),path,'exec'),cls.ns)
 def test_measured_faces_clear_largest_dock_at_both_camera_ends(self):
  layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
  for case in self.cases:
   with self.subTest(location=case['location'],large=case['large']):
    original=copy.deepcopy(case['actors'])
    critical=layouts[case['location']].get('critical',[])+([[880,500,220,152]] if case['location']=='forest' else [])
    result=self.ns['r13_clear_field_hud'](original,critical,case['width'])
    self.assertEqual(original,case['actors'])
    for old,new in zip(original,result):
     self.assertEqual([old[k] for k in ('person','pose','width','height')],[new[k] for k in ('person','pose','width','height')])
     for offset in (0,case['width']-1280):
      for hud in [(offset+772,616,480,88),(offset+1020,512,232,112)]:
       self.assertEqual(overlap(face(new),hud),0,(case['location'],new['person'],face(new),hud))
     if (old['x'],old['y'])!=(new['x'],new['y']):
      self.assertEqual(sum(overlap(new['rect'],r) for r in critical),0,new['person'])
 def test_exchange_box_identity_and_picture_share_geometry(self):
  source=(ROOT/'game/room13_v111.rpy').read_text()
  self.assertIn('dict(rect=[880,500,220,152]',source)
  self.assertIn('x,y,w,h=ROOM13["objects"]["forest"]["v111_box"]["rect"]',source)
  self.assertIn('xysize=(w,h),fit="contain",nearest=True),x,y)',source)
  # Upper-left opening remains a continuous 140x116 patch on the left;
  # the right view shows the whole prop. This is not a new marker or hint.
  identifier=(880,500,140,116)
  for width,height in ((1280,720),(844,390),(740,360)):
   self.assertGreaterEqual(min(identifier[2:])*min(width/1280,height/720),44)
   for offset in (0,880):
    projected=(identifier[0]-offset,identifier[1],identifier[2],identifier[3])
    self.assertTrue(0<=projected[0] and projected[0]+projected[2]<=1280)
    for hud in ((772,616,480,88),(1020,512,232,112)):self.assertEqual(overlap(projected,hud),0)
 def test_scope_and_contact_masks(self):
  source=(ROOT/'game/room13_v111_field_layout.rpy').read_text()
  self.assertIn('if location in ("square","forest"):',source)
  actor=dict(x=30,y=40,rect=[30,40,50,60],depth=100,map27_keepouts=[[(35,45)]])
  moved=self.ns['r13_balance_translate'](actor,12,-3)
  self.assertEqual(moved['map27_keepouts'],[[(47,42)]])
  self.assertEqual(actor['map27_keepouts'],[[(35,45)]])

if __name__=='__main__':unittest.main()
