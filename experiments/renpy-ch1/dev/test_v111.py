"""Author-source invariants and Room13 transactions, separate from actual UI play."""
import ast,copy,json,re,textwrap,unittest
from pathlib import Path
from types import SimpleNamespace
ROOT=Path(__file__).resolve().parents[1]
DATA=json.loads((ROOT/'game/v111/records.json').read_text())
MASTER=json.loads(next((ROOT/'docs/story-v111/source').glob('*.json')).read_text())
class SourceContract(unittest.TestCase):
 def test_source_records_are_exact_and_requirements_not_dropped(self):
  records={c['source_record']['id']:c['source_record'] for s in MASTER['scenes'] for b in s['blocks'] for c in b['cues']}
  for key,r in DATA['records'].items():self.assertEqual({k:v for k,v in r.items() if k not in ('operations','direction')},records[key])
  self.assertEqual(sum(bool(r.get('requires')) for r in records.values()),113)
  self.assertEqual(sum(bool(r.get('requires')) for r in DATA['records'].values()),113)
 def test_full_source_and_all_audits_are_preserved(self):
  self.assertEqual(len(MASTER['scenes']),82)
  self.assertEqual(sum(len(b['cues']) for s in MASTER['scenes'] for b in s['blocks']),3162)
  import csv
  with (ROOT/'docs/story-v111/AUDIT_21_STATUS.csv').open(encoding='utf-8-sig') as f:rows=list(csv.DictReader(f))
  self.assertEqual(len(rows),21);self.assertEqual(len({r['issue_id'] for r in rows}),21)
 def test_registered_records_cannot_overwrite_original_evidence(self):
  old=json.loads((ROOT/'game/room13-content.json').read_text())['evidence']
  self.assertNotEqual(old['E03']['name'],DATA['evidence']['E03']['name'])
  source=(ROOT/'game/room13_v111.rpy').read_text();self.assertIn('rid="V111:"+key',source)
 def test_native_control_flow_has_no_unresolved_jump(self):
  files=sorted((ROOT/'game').glob('room13_v111*.rpy'))
  text='\n'.join(p.read_text() for p in files);labels=set(re.findall(r'^label (\w+)',text,re.M))
  for label in re.findall(r'^\s+jump (r13_v111_\w+)',text,re.M):self.assertIn(label,labels)
  self.assertNotIn('ms14_rt.',text);self.assertNotIn('while ms14',text)
 def test_same_mother_portrait_is_reused_without_new_art(self):
  for name in ('bundle.png','portrait_complete.png','portrait_unfinished.png','portrait_child.png','box.png'):
   self.assertTrue((ROOT/'game/assets/ms14'/name).exists())
class Transactions(unittest.TestCase):
 def setUp(self):
  self.state=SimpleNamespace(room13=dict(day=1,period=0,evidence=[],flags=[],records={},v111=dict(values=copy.deepcopy(DATA['initial']))))
  def flag(*keys):
   n=copy.deepcopy(self.state.room13);n['flags']+= [k for k in keys if k not in n['flags']];self.state.room13=n
  def grant(keys,source):
   for k in keys:
    if k not in self.state.room13['evidence']:self.state.room13['evidence'].append(k)
  self.env=dict(CAST=json.loads((ROOT/"game/assets/room13-fullbody-dialogue.json").read_text())["people"],store=self.state,winter_copy=SimpleNamespace(deepcopy=copy.deepcopy),R13_V111=DATA,r13_has=lambda k:k in self.state.room13['flags'],r13_flag=flag,r13_grant=grant,MS14_SPEAKERS={'피코':'resident_piko'})
  source=(ROOT/'game/room13_v111.rpy').read_text();wanted={'r13_v111_value','r13_v111_set','r13_v111_owned','r13_v111_apply','r13_v111_commit','r13_v111_option','r13_v111_scene','r13_v111_time','r13_v111_line','r13_v111_person_alive','r13_v111_ambient_text','r13_v111_object_key','r13_v111_present_index','r13_v111_questions','r13_object_visible','r13_visible_people'}
  for block in re.split(r'^init \d+ python:\n',source,flags=re.M)[1:]:
   code=block.split('\nlabel ',1)[0]
   tree=ast.parse(textwrap.dedent(code))
   for node in tree.body:
    if isinstance(node,ast.FunctionDef) and node.name in wanted or isinstance(node,ast.Assign) and any(isinstance(t,ast.Name) and t.id in ('R13_V111_ENTRY','R13_V111_RECORD_OBJECTS','R13_V111_CARRIAGE_TEXT') for t in node.targets):exec(compile(ast.Module(body=[node],type_ignores=[]),'v111','exec'),self.env)
 def test_scenery_reactions_do_not_grant_old_story_evidence(self):
  self.state.room13['location']='gate'
  content=json.loads((ROOT/'game/room13-content.json').read_text())
  self.env.update(ROOM13=content,_r13_v111_object_visible=lambda spec:True,r13_object_name=lambda key:key)
  for key,record in DATA['evidence'].items():content['evidence']['V111:'+key]=dict(name=record['name'],establishes=next(iter(record['variants'].values())))
  before=copy.deepcopy(self.state.room13)
  self.assertEqual(self.env['r13_v111_ambient_text']('road',content['objects']['gate']['road']),content['objects']['gate']['road']['text'])
  self.env['r13_v111_ambient_text']('booth',content['objects']['gate']['booth'])
  self.assertEqual(before,self.state.room13)
 def test_existing_residents_remain_but_story_survival_and_location_win(self):
  self.state.room13['location']='square'
  self.env.update(r13_v111_active=lambda:True,_r13_v111_visible_people=lambda:['resident_kongi','resident_piko','resident_siluk'],r13_v111_binding=lambda:dict(people=['daram']))
  visible=self.env['r13_visible_people']
  self.assertEqual(visible(),['resident_kongi','resident_piko','resident_siluk','daram'])
  self.env['r13_v111_set']('piko.location','clinic')
  self.assertNotIn('resident_piko',visible())
  self.env['r13_v111_set']('silluk_status','detained_work_waiting_station')
  self.assertNotIn('resident_siluk',visible())
  self.env['r13_v111_set']('piko_alive',False)
  self.env['r13_v111_binding']=lambda:dict(people=['resident_piko','daram'])
  self.assertNotIn('resident_piko',visible())
 def test_reserved_blankets_are_not_possession_and_receipt_is_once(self):
  self.env['r13_v111_commit']('MS14_D02_S04_L0083');self.assertEqual(self.env['r13_v111_value']('carried_dry_blankets'),0)
  self.assertTrue(self.env['r13_v111_value']('nero_bedding_reserved'))
  self.env['r13_v111_commit']('MS14_D03_S06_L0041');saved=copy.deepcopy(self.state.room13)
  self.env['r13_v111_commit']('MS14_D03_S06_L0041');self.assertEqual(self.state.room13,saved)
  self.assertEqual(self.env['r13_v111_value']('carried_dry_blankets'),2)
 def test_preconditions_block_scene_before_observation_or_effect(self):
  self.state.room13["day"]=2;self.state.room13["v111"]["values"]["day"]=2
  before=copy.deepcopy(self.state.room13)
  with self.assertRaisesRegex(Exception,'Unmet authored scene entry'):self.env['r13_v111_scene']('MS14_D02_S02')
  self.assertEqual(before,self.state.room13)
 def test_letter_close_option_preserves_declared_effect(self):
  self.env['r13_v111_option']('MS14_D01_S01_L0014_O3');self.assertTrue(self.env['r13_v111_value']('letter_close_selected'))
 def test_repeat_observation_and_reload_do_not_spend_time_twice(self):
  self.env['r13_v111_time']('memo',15);self.state.room13=copy.deepcopy(self.state.room13)
  self.env['r13_v111_time']('memo',15);self.assertEqual(self.env['r13_v111_value']('elapsed_minutes'),15)
 def test_dead_piko_cannot_speak_and_old_world_death_flag_is_synced(self):
  self.env['r13_v111_commit']('MS14_D03_S01_L0021');self.assertIn('piko_dead',self.state.room13['flags'])
  with self.assertRaisesRegex(Exception,'Absent/dead Piko'):self.env['r13_v111_line']('MS14_D03_S06_L0024')
if __name__=='__main__':unittest.main()
