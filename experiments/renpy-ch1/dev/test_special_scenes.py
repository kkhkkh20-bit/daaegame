"""Scene-only art must preserve the authored branches and dialogue verbatim."""
import hashlib,json,re,unittest
from pathlib import Path
from PIL import Image
ROOT=Path(__file__).resolve().parents[1]
MAP={'nt:night8:half':'chorong_injured_alive','ws:morning:nero_alive':'nero_weakened_alive','ws:decision:gone_one':'teacher_blanket_dodam_only','ws:decision:gone':'teacher_blanket_four_children','ws:after:bori':'bori_cares_three_after_dodam_loss','ws:after:bori_home':'bori_adopts_four_alive','ws:after:bori_silent':'bori_silent_single_shoe','ws:meeting:open':'bori_kneels_holding_dodam_hand'}
def scene_calls():
 import ast
 result={}
 for name in ('room13_ep4_night13.rpy','room13_ep5_soup.rpy'):
  lines=(ROOT/'game/systems'/name).read_text().splitlines()
  for n,line in enumerate(lines):
   if not line.lstrip().startswith('call r13_lines('):continue
   for end in range(n+1,min(n+60,len(lines))+1):
    code='\n'.join(lines[n:end]).lstrip()[5:]
    try:node=ast.parse(code).body[0].value
    except SyntaxError:continue
    if isinstance(node,ast.Call) and len(node.args)>1 and isinstance(node.args[1],ast.Constant) and node.args[1].value in MAP:
     result[node.args[1].value]=ast.literal_eval(node.args[0])
    break
 return result
class SpecialScenes(unittest.TestCase):
 def test_exact_eight_source_call_sites(self):
  calls=scene_calls();self.assertEqual(set(calls),set(MAP))
  for identity,rows in calls.items():self.assertEqual(rows[0][2]['cut'],MAP[identity])
 def test_sources_conditions_and_dialogue_unchanged(self):
  baselines=json.loads((ROOT/'docs/reviews/special-scenes/preservation.json').read_text())['source_hashes_before_metadata']
  for name,sha in baselines.items():
   text=(ROOT/name).read_text();text=re.sub(r',\{"cut":"(?:'+ '|'.join(MAP.values()) +r')","no_lead":True\}', '',text)
   self.assertEqual(hashlib.sha256(text.encode()).hexdigest(),sha)
 def test_asset_paths_and_attendance(self):
  d=json.loads((ROOT/'game/assets/room13-special-scenes.json').read_text());self.assertEqual(set(d['scenes']),set(MAP.values()))
  for spec in d['scenes'].values():
   p=ROOT/'game'/spec['file'];self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),spec['display_sha256'])
   with Image.open(p) as im:self.assertEqual(list(im.size),spec['size'])
  one,four=d['attendance_overlays'];self.assertEqual(one['circled_names'],['도담']);self.assertEqual(four['uncircled_names'],['새미']);self.assertEqual(four['circled_names'],['깜이','몽이','방울','도담'])
 def test_renderer_only_overrides_registered_cuts(self):
  import textwrap,types
  data=json.loads((ROOT/'game/assets/room13-special-scenes.json').read_text())
  block=(ROOT/'game/systems/room13_special_scenes.rpy').read_text().split('init 162 python:\n',1)[1]
  env=dict(json=json,renpy=types.SimpleNamespace(file=lambda p:open(ROOT/'game'/p)),store=types.SimpleNamespace(r13_scene_bg='original-scene'),r13_ep_cut_art=lambda name:('original-cut',name),r13_background=lambda key:('background',key),_r13_ep_art_world_background=lambda key:('background',key),Crop=lambda *a:('crop',a),Fixed=lambda *a,**k:(a,k),Transform=lambda *a,**k:(a,k))
  exec(textwrap.dedent(block),env)
  self.assertEqual(env['r13_ep_cut_art']('bell'),('original-cut','bell'))
  env['store'].r13_scene_bg='r13_river'
  river=env['r13_ep_cut_art']('nero_weakened_alive')[0][0]
  self.assertEqual(river[0][0],('crop',((0,270,800,450),('background','river'))))
  env['store'].r13_scene_bg='original-scene'
  for name,spec in data['scenes'].items():
   args,kw=env['r13_ep_cut_art'](name);self.assertEqual(args[0][0][0],('crop',((240,270,800,450),('background','original-scene'))));w,h=args[1][1]['size'];self.assertLessEqual(w,900);self.assertLessEqual(h,spec['cut_max_height']);self.assertEqual(args[1][1]['ypos']+h,490);left,top,right,bottom=spec['visible_bounds'];self.assertAlmostEqual(w/h,(right-left)/(bottom-top),delta=.006)
if __name__=='__main__':unittest.main()
