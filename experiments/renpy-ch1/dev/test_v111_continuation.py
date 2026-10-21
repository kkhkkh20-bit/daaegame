"""Changed V1.1.1 guards and source bindings, without retesting Ren'Py saves."""
import ast,copy,json,re,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
import test_v111 as source_tests
DATA=source_tests.DATA;ROOT=source_tests.ROOT
class ContinuationGuards(unittest.TestCase):
 def setUp(self):
  source_tests.Transactions.setUp(self)
  state=self.state
  class RoomProxy:
   def __getitem__(self,key):return state.room13[key]
  self.env["room13"]=RoomProxy()
  source=(ROOT/'game/room13_v111_later_bindings.rpy').read_text()
  for block in re.split(r'^init \d+ python:\n',source,flags=re.M)[1:]:
   tree=ast.parse(textwrap.dedent(block))
   for node in tree.body:
    if isinstance(node,ast.FunctionDef) or isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='R13_V111_SCENE_CHECKS' for t in node.targets):exec(compile(ast.Module(body=[node],type_ignores=[]),'late-bindings','exec'),self.env)
  source=(ROOT/'game/room13_v111_days1114.rpy').read_text().split('init 315 python:\n',1)[1]
  exec(textwrap.dedent(source),self.env)
  self.env['r13_v111_binding']=lambda:dict(people=self.state.room13['v111'].get('people',[]))
  self.state.room13.update(location='school');self.state.room13['v111']['people']=[]
 def test_continuation_evidence_uses_existing_notebook_categories(self):
  source=(ROOT/'game/room13_notebook.rpy').read_text()
  categories=ast.literal_eval(re.search(r'R13_RECORD_CATEGORIES=(\{[^\n]+\})',source).group(1))
  self.assertFalse({v['kind'] for v in DATA['evidence'].values()}-set(categories))
 def test_hearing_entry_rejects_missing_material_chain_without_marking_scene(self):
  self.env['r13_v111_set']('day',10);self.env['r13_v111_set']('route7','murder')
  before=copy.deepcopy(self.state.room13)
  with self.assertRaisesRegex(Exception,'Unmet authored scene state'):self.env['r13_v111_scene']('MS14_D10_S01')
  self.assertEqual(before,self.state.room13)
 def test_late_medical_aftermath_never_opens_for_prevention(self):
  self.env['r13_v111_set']('day',12)
  for route in ('early_prevented','premeal_stopped'):
   self.env['r13_v111_set']('route12',route)
   with self.assertRaisesRegex(Exception,'Unmet authored scene state'):self.env['r13_v111_scene']('MS14_D12_S05')
 def test_record_guard_rejects_unmet_soup_path_before_presentation(self):
  check=self.env['r13_v111_record_allowed'];setv=self.env['r13_v111_set']
  for path in ('early_prevented','premeal_stopped','uncommitted'):
   setv('route12',path);self.assertFalse(check('MS14_D12_S04_L0046'))
  setv('route12','late_exposure');self.assertTrue(check('MS14_D12_S04_L0046'))
 def test_record_does_not_summon_missing_dead_or_reassigned_carrier(self):
  check=self.env['r13_v111_record_allowed'];setv=self.env['r13_v111_set'];rid='MS14_D11_S00_L0002'
  self.assertFalse(check(rid))
  self.state.room13['v111']['people']=['karo'];self.assertTrue(check(rid))
  setv('location:karo','forest');self.assertFalse(check(rid))
  setv('location:karo','school');setv('alive:karo',False);self.assertFalse(check(rid))
 def test_child_after_school_move_cannot_speak_from_the_square(self):
  check=self.env['r13_v111_record_allowed'];setv=self.env['r13_v111_set']
  self.state.room13['location']='square';self.state.room13['v111']['people']=['daram'];setv('location:daram','square')
  self.assertTrue(check('MS14_D13_S04_L0028'))
  setv('location:daram','school');self.assertFalse(check('MS14_D13_S04_L0028'))
 def test_tosil_listening_and_outside_report_are_exclusive(self):
  check=self.env['r13_v111_record_allowed'];setv=self.env['r13_v111_set']
  self.state.room13['v111']['people']=['resident_tosil'];setv('tosil_listen','inside')
  self.assertTrue(check('MS14_D14_S03_L0013'));self.assertFalse(check('MS14_D14_S03_L0038'))
  setv('tosil_listen','outside');setv('adult_interview_done',True)
  self.assertFalse(check('MS14_D14_S03_L0013'));self.assertTrue(check('MS14_D14_S03_L0038'))
 def test_mortality_preserves_distinct_children(self):
  setv=self.env['r13_v111_set'];alive=self.env['r13_v111_person_alive']
  setv('KKOMI_ALIVE',True);setv('alive:kid_dodam',False)
  self.assertTrue(alive('kid_kkomi'));self.assertFalse(alive('kid_dodam'))
 def test_later_arrival_does_not_relocate_a_dead_rescuer(self):
  setv=self.env['r13_v111_set']
  setv('nero_alive',False);setv('location:resident_nero','forest')
  self.env['r13_v111_arrive'](['resident_nero','karo'])
  self.assertEqual(self.env['r13_v111_value']('location:resident_nero'),'forest')
  self.assertNotIn('resident_nero',self.state.room13['v111']['people'])
  self.assertEqual(self.env['r13_v111_value']('location:karo'),'school')
 def test_unnamed_offscreen_staff_does_not_require_a_new_character_sprite(self):
  self.env.update(r13_v111_active=lambda:True,_r13_v111_visible_people=lambda:['daram'],r13_v111_binding=lambda:dict(people=['daram','v111_patrol']))
  self.env['r13_v111_arrive'](['daram','v111_patrol'])
  self.assertNotIn('v111_patrol',self.env['r13_visible_people']())
  self.assertIn('daram',self.env['r13_visible_people']())
  self.assertEqual(self.env['r13_v111_value']('location:v111_patrol'),'school')
 def test_repair_material_survives_all_four_independent_attendance_combinations(self):
  setv=self.env['r13_v111_set'];attends=self.env['r13_v111_tok_attends']
  for workshop in (False,True):
   for hearing in (False,True):
    with self.subTest(workshop=workshop,hearing=hearing):
     self.state.room13['evidence']=[];self.state.room13['flags']=[]
     setv('TOK_ALIVE',True);setv('tok_workshop_present',workshop);setv('tok_hearing_present',hearing)
     self.assertEqual(attends('workshop'),workshop)
     self.env['r13_v111_commit']('MS14_D09_S02_L0018' if workshop else 'MS14_D09_S02_L0026')
     self.assertTrue(self.env['r13_v111_owned']('E09_PIN_OWNER'))
     self.assertTrue(self.env['r13_v111_value']('tok_repair_copy_owned'))
     self.assertEqual(attends('hearing'),hearing)
     setv('TOK_ALIVE',False)
     self.assertFalse(attends('workshop'));self.assertFalse(attends('hearing'))
 def test_existing_kitchen_variant_cannot_cover_the_authored_rear_door(self):
  self.state.room13['location']='kitchen'
  objects={'rear':dict(rect=[20,30,80,160],text='문'),'rear_after':dict(rect=[20,30,80,160],give=['OLD']), 'rear_after_known':dict(rect=[20,30,80,160],give=['OLD'])}
  self.env.update(ROOM13=dict(objects=dict(kitchen=objects)),r13_v111_active=lambda:True,r13_v111_binding=lambda:dict(options=[dict(location='kitchen',object='rear')]))
  self.assertEqual(self.env['r13_v111_object_key']('rear_after'),'rear')
  self.assertTrue(self.env['r13_object_visible'](objects['rear']))
  self.assertFalse(self.env['r13_object_visible'](objects['rear_after']))
  self.assertFalse(self.env['r13_object_visible'](objects['rear_after_known']))
 def test_observer_arrival_requires_actual_prior_consent_and_life(self):
  setv=self.env['r13_v111_set'];arrive=self.env['r13_v111_arrive']
  self.state.room13['location']='altar';self.state.room13['v111']['scene']='MS14_D14_S02'
  setv('location:resident_madam','store');arrive(['mom','resident_badook'])
  self.assertNotIn('resident_madam',self.state.room13['v111']['people'])
  self.assertEqual(self.env['r13_v111_value']('location:resident_madam'),'store')
  setv('madam_observer_consent',True);arrive(['mom','resident_badook'])
  self.assertIn('resident_madam',self.state.room13['v111']['people'])
  setv('alive:resident_madam',False);setv('location:resident_madam','store');arrive(['mom','resident_badook'])
  self.assertNotIn('resident_madam',self.state.room13['v111']['people'])
  self.assertEqual(self.env['r13_v111_value']('location:resident_madam'),'store')
 def test_showing_the_same_portrait_to_a_bystander_cannot_advance_nero(self):
  self.state.room13['evidence']=['V111:E09'];self.state.room13['location']='ms14_somi'
  binding=dict(options=[dict(index=3,person='resident_nero',location='ms14_somi',present='V111:E09')])
  choose=self.env['r13_v111_present_index']
  binding['options'][0]['title']='이분을 보셨습니까?'
  self.env.update(Return=lambda value:value,r13_v111_binding=lambda:binding)
  self.assertEqual(self.env['r13_v111_questions']('resident_nero')[0][1],'present')
  self.assertIsNone(choose(binding,'resident_somi','V111:E09'))
  self.assertEqual(choose(binding,'resident_nero','V111:E09'),3)
  self.state.room13['location']='gate'
  self.assertIsNone(choose(binding,'resident_nero','V111:E09'))
  self.state.room13['location']='ms14_somi';self.state.room13['evidence']=[]
  self.assertIsNone(choose(binding,'resident_nero','V111:E09'))
 def test_night_testimony_unlocks_missing_e21_only_at_completion(self):
  self.assertFalse(self.env['r13_v111_owned']('E21'))
  self.env['r13_v111_commit']('MS14_D04_S04_L0018')
  self.assertTrue(self.env['r13_v111_owned']('E21'))
 def test_nero_partial_does_not_grant_the_completed_record(self):
  self.env['r13_v111_commit']('MS14_D05_S01_L0024')
  self.assertEqual(self.env['r13_v111_value']('E24.status'),'partial')
  self.assertFalse(self.env['r13_v111_owned']('E24'))
  self.env['r13_v111_commit']('MS14_D05_S02_L0025')
  self.assertEqual(self.env['r13_v111_value']('E24.status'),'complete');self.assertTrue(self.env['r13_v111_owned']('E24'))
if __name__=='__main__':unittest.main()
