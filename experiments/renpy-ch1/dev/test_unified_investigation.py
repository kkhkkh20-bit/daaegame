import ast,copy,textwrap,types,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
FIELD=(ROOT/'game/systems/room13_field_views.rpy').read_text()
SCREEN=(ROOT/'game/room13_screens.rpy').read_text()
class UnifiedInvestigation(unittest.TestCase):
 def test_saved_scene_mode_normalizes_without_story_change(self):
  tree=ast.parse(textwrap.dedent(FIELD.split('init 85 python:\n',1)[1].split('\nscreen ',1)[0]))
  f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_field_sync')
  for location in ('inn','kitchen'):
   story={'location':location,'day':2,'evidence':['E01'],'flags':[]};before=copy.deepcopy(story)
   store=types.SimpleNamespace(room13=story,r13_field_view='scene',r13_field_location=location,r13_field_pick=None)
   env=dict(store=store,r13_field_selection=lambda:None)
   exec(compile(ast.Module(body=[f],type_ignores=[]),'field-sync','exec'),env);env['r13_field_sync']()
   self.assertEqual(store.r13_field_view,'people');self.assertEqual(story,before)
 def test_objects_keep_gates_and_existing_actions(self):
  world=SCREEN.split('screen r13_world_contents(',1)[1].split('\nscreen r13_resident_stage',1)[0]
  self.assertIn('if r13_object_visible(spec):',world)
  self.assertEqual(world.count('Return(("object",key))] sensitive ready'),2)
  self.assertIn('area rect focus_mask mask',world)
  self.assertNotIn('r13_field_view',world)
  self.assertEqual(world.count('tooltip r13_object_name(key) alt r13_object_name(key)'),2)
 def test_masked_objects_keep_faces_and_names_reachable(self):
  world=SCREEN.split('screen r13_world_contents(',1)[1].split('\nscreen r13_resident_stage',1)[0]
  self.assertLess(world.index('for key,spec in ROOM13'),world.index('use r13_resident_stage(entry,ready)'))
  self.assertGreater(world.index('for key,rect,mask'),world.index('use r13_resident_stage(entry,ready)'))
  self.assertLess(world.index('for key,rect,mask'),world.index('for nameplate in r13_actor_nameplates'))
  acting=(ROOT/'game/room13_acting.rpy').read_text()
  # 0.19.97 (owner): a resident's whole box talks to them; objects keep only the area outside it.
  self.assertIn('r13_object_mask(spec["rect"],[tuple(a["rect"]) for a in actors]+later)',acting)
  self.assertIn('focus_mask r13_actor_hit_mask(actor)',SCREEN)
  self.assertIn('and not r13_point_on_face(point,entry)',world)
 def test_toggle_removed_but_hint_and_callback_retained(self):
  self.assertNotIn('주변 살피기',FIELD);self.assertNotIn('사람 보기',FIELD)
  self.assertIn('config.after_load_callbacks.append(r13_field_sync)',FIELD)
  self.assertIn('timer (6.0 if room13["location"]=="gate" else 3.0) action SetVariable',FIELD)
  self.assertNotIn('use r13_field_notebook_surface()',SCREEN)
  self.assertNotIn('text "조사"',FIELD)
 def test_no_new_story_or_travel_side_effects(self):
  self.assertNotIn('r13_tick(',FIELD);self.assertNotIn('r13_grant(',FIELD)
  self.assertIn('Function(r13_empty_tap_feedback) sensitive ready',SCREEN)
if __name__=='__main__':unittest.main()
