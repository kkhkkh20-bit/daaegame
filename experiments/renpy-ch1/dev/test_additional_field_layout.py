"""조사 물건 회피(r13_clear_objects): 0.20.14 2일 광장·숲 계측 인물로 규칙을 확인한다."""
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
  cls.ns=dict(r13_actor_face_target=face,r13_world_height=lambda:720)
  for path,names in [('game/systems/room13_investigation_balance.rpy',{'r13_balance_translate'}),('game/room13_v111_field_layout.rpy',{'r13_clear_objects','r13_foot_in_keepout','r13_keepout_cover_rects'})]:
   exec(compile(functions(path,names),path,'exec'),cls.ns)
 def test_measured_actors_do_not_stand_on_objects(self):
  layouts=json.loads((ROOT/'game/assets/room13-world-layout.json').read_text())
  for case in self.cases:
   with self.subTest(location=case['location'],large=case['large']):
    original=copy.deepcopy(case['actors'])
    critical=layouts[case['location']].get('critical',[])+([[880,500,220,152]] if case['location']=='forest' else [])
    result=self.ns['r13_clear_objects'](original,critical,case['width'])
    self.assertEqual(original,case['actors'])
    for old,new in zip(original,result):
     self.assertEqual([old[k] for k in ('person','pose','width','height')],[new[k] for k in ('person','pose','width','height')])
     # 규칙: 몸이 조사 물건을 1/5 넘게 덮거나 물건 가운데를 밟지 않는다.
     self.assertEqual(old['y'],new['y'],new['person'])   # 발 선은 지킨다
     for r in critical:
      area=r[2]*r[3];cx,cy=r[0]+r[2]/2.0,r[1]+r[3]/2.0
      inside=new['rect'][0]<=cx<=new['rect'][0]+new['rect'][2] and new['rect'][1]<=cy<=new['rect'][1]+new['rect'][3]
      self.assertFalse(inside or overlap(new['rect'],r)>area*0.2,(case['location'],new['person'],r))
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
 def test_scope_and_contact_masks(self):
  source=(ROOT/'game/room13_v111_field_layout.rpy').read_text()
  # 회피는 배치 사슬의 맨 끝(도트 환산 뒤) 한 곳에서만 돈다.
  self.assertNotIn('r13_clear_objects(',source.split('def r13_clear_objects(')[0])
  dot=(ROOT/'game/systems/room13_field_dot.rpy').read_text()
  self.assertIn('return r13_clear_objects_last(result,location)',dot)
  self.assertIn('return r13_clear_objects_last(actors,location)',dot)
  actor=dict(x=30,y=40,rect=[30,40,50,60],depth=100,map27_keepouts=[[(35,45)]])
  moved=self.ns['r13_balance_translate'](actor,12,-3)
  self.assertEqual(moved['map27_keepouts'],[[(47,42)]])
  self.assertEqual(actor['map27_keepouts'],[[(35,45)]])

if __name__=='__main__':unittest.main()
