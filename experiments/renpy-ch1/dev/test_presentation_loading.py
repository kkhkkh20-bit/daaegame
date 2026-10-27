"""Player-facing regressions: startup budget, live daylight and field labels."""
import ast,copy,json,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
from build_web import startup_files,startup_media
ROOT=Path(__file__).resolve().parents[1]

def function(file,name):
 import re
 for block in re.split(r'^init \d+ python:\n',(ROOT/file).read_text(),flags=re.M)[1:]:
  block=re.split(r"^(?=\S)",block,flags=re.M)[0]
  tree=ast.parse(textwrap.dedent(block))
  for node in tree.body:
   if isinstance(node,ast.FunctionDef) and node.name==name:
    return compile(ast.Module(body=[node],type_ignores=[]),str(file),'exec')
 raise AssertionError(name)

class PresentationLoading(unittest.TestCase):
 def test_primary_opening_profiles_are_available_without_legacy_atlases(self):
  early=startup_files(ROOT/'game')
  data=json.loads((ROOT/'game/assets/room13-dialogue-talk-art.json').read_text())['people']['daram']
  for p in data['profiles'].values():
   for f in p['frames'].values():self.assertTrue(startup_media(f['file'],early),f['file'])
  for path in ('assets/room13-pixel-world-daram-gray-gutter.webp','assets/room13-pixel-acting-daram.webp','assets/dialogue-source-master/guard/840/angry.webp','assets/room13-pixel-ready-gate0173-evening.webp','assets/bgm-snow.mp3'):
   self.assertFalse(startup_media(path,early),path)
  for path in ('assets/bgm-title.mp3','assets/bgm-travel.mp3','assets/Pretendard-Regular.otf'):
   self.assertTrue(startup_media(path,early),path)
 def test_dialogue_background_uses_the_live_clock_without_state_writes(self):
  state=SimpleNamespace(room13=dict(location='square',period=0))
  env=dict(store=state,r13_daylight=lambda:('morning','afternoon','evening')[state.room13['period']],r13_world_offset=lambda p:320,r13_field_zoom=lambda p:1.0,r13_world_background=lambda p,t:(p,t),Crop=lambda rect,bg:(rect,bg))
  exec(function('game/room13_world_camera.rpy','r13_camera_background'),env)
  f=env['r13_camera_background']
  for period,expected in enumerate(('morning','afternoon','evening')):
   state.room13['period']=period;before=copy.deepcopy(state.room13)
   self.assertEqual(f(0,0,'square','morning')[0][1],('square',expected))
   self.assertEqual(before,state.room13)
  self.assertEqual(f(0,0,'inn','morning')[0][1],('inn','morning'))
 def test_field_nameplates_keep_clear_of_fixed_ui(self):
  # 이름표는 상단 고정 조작(지도·기록·생각 줄)을 덮지 않는다. 옛 하단 조작 띠는 없어졌다(2026-10-25).
  h=80;face=[300,180,70,70]
  env=dict(r13_touch_ui=lambda:True,r13_actor_face_target=lambda a:face,r13_actor_nameplate=lambda a:(335,144),r13_world_width=lambda:1280,r13_world_offset=lambda:0,r13_view_width=lambda:1280,r13_field_zoom=lambda:1.0,r13_layout=lambda:{},r13_field_ui_rects=lambda o:[(o+24,84,472,88),(o+24,20,400,54)],R13_NAMES={'daram':'다람'},R13_CONTROL={'width':232},r13_control_height=lambda:h,store=SimpleNamespace(R13_LIFE_GROUPS=[]))
  exec(function('game/room13_interaction.rpy','r13_actor_nameplates'),env)
  label=env['r13_actor_nameplates']([dict(person='daram',rect=face)])[0]['rect']
  def overlaps(a,b):return a[0]<b[0]+b[2] and a[0]+a[2]>b[0] and a[1]<b[1]+b[3] and a[1]+a[3]>b[1]
  self.assertFalse(any(overlaps(label,r) for r in env['r13_field_ui_rects'](0)),label)
if __name__=='__main__':unittest.main()
