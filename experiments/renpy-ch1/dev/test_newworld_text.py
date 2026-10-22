"""New-world dialogue layer: reviewed revisions by record ID over the exact V1.1.1 source."""
import ast,copy,json,re,tempfile,textwrap,unittest
from pathlib import Path
import test_v111 as source_tests
ROOT=source_tests.ROOT
LAYER=ROOT/'game/room13_v111_newworld_text.rpy'
DAYS=['room13_v111_days123.rpy','room13_v111_days45.rpy','room13_v111_days610.rpy','room13_v111_days1114.rpy']
SPEAKERS=ast.literal_eval(re.search(r'MS14_SPEAKERS = (\{.*?\})\n',(ROOT/'game/ms14_story.rpy').read_text(),re.S).group(1))
# Later layers (init 310/311) add the day 4-14 speakers before the text layer (init 319) runs.
for _m in re.finditer(r'MS14_SPEAKERS\.update\((\{.*?\})\)',(ROOT/'game/room13_v111_later_bindings.rpy').read_text()):SPEAKERS.update(ast.literal_eval(_m.group(1)))
FORBIDDEN=('돌님','겉돌','날돌','말 그릇')
EMOJI=re.compile('[\U0001F300-\U0001FAFF☀-➿]')

class Renpy:
 def __init__(self,base):self.base=Path(base)
 def loadable(self,path):return (self.base/path).exists()
 def file(self,path):return open(self.base/path,'rb')

def call_sites():
 for name in DAYS:
  for m in re.finditer(r'r13_v111_lines\((\[[^\]]*\])\)',(ROOT/'game'/name).read_text()):
   yield name,ast.literal_eval(m.group(1))

class Layer(unittest.TestCase):
 def load(self,base=ROOT/'game',art=None):
  source_tests.Transactions.setUp(self)
  data=copy.deepcopy(source_tests.DATA)
  evidence={'V111:'+k:dict(name=v['name'],establishes='') for k,v in data['evidence'].items()}
  stub=Renpy(base)
  if art is not None:
   real=stub.loadable;stub.loadable=lambda p:real(p) or p in art
  self.env.update(renpy=stub,json=json,R13_V111=data,MS14_SPEAKERS=SPEAKERS,ROOM13=dict(evidence=evidence),R13_RECORD_SHORT={},
   R13_RECORD_CATEGORIES={'물증':'evidence','기록':'evidence','관찰기록':'evidence','증언':'testimony'},
   R13_MEETING_BEATS={k:None for k in re.findall(r'^        "(\w+)": \(',(ROOT/'game/systems/room13_meeting_direction.rpy').read_text(),re.M)},
   R13_FULLBODY_PLAIN={'neutral','joy','anxious','angry','surprise','flustered'},
   R13_DIALOGUE_CONTEXT_ART=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text()))
  ctx=re.search(r'^init 172 python:\n((?:[ \t].*\n|\n)*)',(ROOT/'game/systems/room13_dialogue_context_art.rpy').read_text(),re.M).group(1)
  tree=ast.parse(textwrap.dedent(ctx))
  exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='r13_dialogue_context_match'],type_ignores=[]),'ctx','exec'),self.env)
  self.env['r13_v111_line']=lambda rid:(SPEAKERS.get(data['records'][rid].get('speaker')),data['records'][rid]['text'],{})
  block=re.search(r'^init 319 python:\n((?:[ \t].*\n|\n)*)',LAYER.read_text(),re.M).group(1)
  exec(textwrap.dedent(block),self.env)
  return self.env
 def fixture(self,day,content,art=None):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
  (Path(tmp.name)/'v111/newworld').mkdir(parents=True)
  (Path(tmp.name)/('v111/newworld/%s.json'%day)).write_text(json.dumps(content,ensure_ascii=False))
  return self.load(tmp.name,art)

class NewWorldText(Layer):
 def test_every_day_file_goes_through_the_layer(self):
  for name in DAYS:
   text=(ROOT/'game'/name).read_text()
   self.assertNotIn('r13_v111_line(',text,name)
  self.assertEqual(sum(len(r) for _,r in call_sites()),sum(len(r) for _,r in call_sites()))
  self.assertGreater(len(list(call_sites())),1900)
 def test_without_revisions_nothing_changes(self):
  tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
  env=self.load(tmp.name)
  self.assertEqual(env['r13_nw_text_problems'](),[])
  for name,rids in call_sites():
   rows=env['r13_v111_lines'](rids)
   self.assertEqual([r[2]['line_id'] for r in rows],rids,name)
   self.assertEqual([(r[0],r[1],{k:v for k,v in r[2].items() if k!='line_id'}) for r in rows],[env['_r13_nw_authored_line'](r) for r in rids],name)
 def test_shipped_files_are_valid_and_clean(self):
  env=self.load()
  self.assertEqual(env['r13_nw_text_problems'](),[])
  for path in sorted((ROOT/'game/v111/newworld').glob('d*.json')):
   part=json.loads(path.read_text())
   self.assertLessEqual(set(part)-{'new_evidence','blocks'},{'replace','before','after','drop','evidence'},path.name)
   self.assertLessEqual({'replace','before','after','drop','evidence'},set(part),path.name)
   texts=[v['text'] for v in part['replace'].values()]+[r['text'] for rows in list(part['before'].values())+list(part['after'].values())+list(part.get('blocks',{}).values()) for r in rows]+[t for e in part.get('new_evidence',{}).values() for t in [e['name']]+list(e['variants'].values())]
   for t in texts:
    self.assertFalse(any(w in t for w in FORBIDDEN),t);self.assertIsNone(EMOJI.search(t),t)
  self.assertEqual(len(list((ROOT/'game/v111/newworld').glob('d*.json'))),14)
 def test_revisions_attach_only_to_lines_the_game_shows(self):
  # Action/stage records are committed for effects but never displayed; a line
  # attached to one would silently never appear.
  shown={r for _,rids in call_sites() for r in rids}
  for path in sorted((ROOT/'game/v111/newworld').glob('d*.json')):
   part=json.loads(path.read_text())
   anchors=list(part['replace'])+list(part['before'])+list(part['after'])+[d if isinstance(d,str) else d['id'] for d in part['drop']]
   self.assertEqual([a for a in anchors if a not in shown],[],path.name)
  self.assertNotIn('MS14_D01_S05_L0015',shown,'stage line: room opens (not displayed)')
  self.assertIn('MS14_D01_S05_L0016',shown)

 def test_replace_before_after_and_drop(self):
  env=self.fixture('d01',dict(replace={'MS14_D01_S05_L0004':{'text':'고맙습니다, 할머니.'}},
   before={'MS14_D01_S05_L0004':[dict(id='NW_T_B1',speaker=None,text='앞 서술')]},
   after={'MS14_D01_S05_L0004':[dict(id='NW_T_A1',speaker='다람',text='뒤 대사',expression='anxious'),dict(id='NW_T_A2',speaker=None,text='조건 줄',when='owl_dead')]},
   drop=['MS14_D01_S05_L0005']))
  rows=env['r13_v111_lines'](['MS14_D01_S05_L0003','MS14_D01_S05_L0004','MS14_D01_S05_L0005','MS14_D01_S05_L0006'])
  texts=[r[1] for r in rows]
  self.assertEqual(texts[1:4],['앞 서술','고맙습니다, 할머니.','뒤 대사'])
  self.assertNotIn(source_tests.DATA['records']['MS14_D01_S05_L0005']['text'],texts)
  self.assertNotIn('조건 줄',texts,'false condition hides the line')
  self.assertEqual(rows[3][0],'daram');self.assertEqual(rows[3][2]['expression'],'anxious')
  self.env['r13_v111_set']('OWL_ALIVE',False)
  self.assertIn('조건 줄',[r[1] for r in env['r13_v111_lines'](['MS14_D01_S05_L0004'])])
 def test_cut_uses_existing_art_only(self):
  row=dict(id='NW_T_C1',speaker=None,text='벽을 본다',cut='O47-handprints')
  env=self.fixture('d09',dict(after={'MS14_D09_S01_L0001':[row]}),art={'assets/room13-ep-O47-handprints.webp'})
  self.assertEqual(env['r13_v111_lines'](['MS14_D09_S01_L0001'])[1][2]['cut'],'O47-handprints')
  self.assertTrue((ROOT/'game/assets/room13-ep-O47-handprints.webp').exists())
  with self.assertRaisesRegex(Exception,'missing cut art'):self.fixture('d09',dict(after={'MS14_D09_S01_L0001':[dict(row,cut='O99-none')]}),art=set())
 def test_broken_references_stop_the_game_at_start(self):
  bad=[dict(replace={'MS14_NOPE':{'text':'x'}}),dict(drop=['MS14_NOPE']),
   dict(after={'MS14_D01_S05_L0004':[dict(id='X1',speaker=None,text='x')]}),
   dict(after={'MS14_D01_S05_L0004':[dict(id='NW_T_S',speaker='새 인물',text='x')]}),
   dict(after={'MS14_D01_S05_L0004':[dict(id='NW_T_W',speaker=None,text='x',when='no_such')]}),
   dict(after={'MS14_D01_S05_L0004':[dict(id='NW_T_D',speaker=None,text='x'),dict(id='NW_T_D',speaker=None,text='y')]}),
   dict(evidence={'NOPE':{'name':'x'}})]
  for content in bad:
   with self.assertRaisesRegex(Exception,'inconsistent'):self.fixture('d01',dict(dict(replace={},before={},after={},drop=[],evidence={}),**content))
 def test_dead_speaker_cannot_say_an_added_line(self):
  env=self.fixture('d03',dict(after={'MS14_D03_S01_L0001':[dict(id='NW_T_P',speaker='피코',text='x')]}))
  self.env['r13_v111_set']('piko_alive',False)
  with self.assertRaisesRegex(Exception,'dead new-world speaker'):env['r13_v111_lines'](['MS14_D03_S01_L0001'])
 def test_thought_row_is_the_fathers_unspoken_line(self):
  env=self.fixture('d01',dict(after={'MS14_D01_S05_L0004':[dict(id='NW_T_T1',speaker='아빠',kind='thought',text='책상 밑을 다시 보자.')]}))
  out=env['r13_v111_lines'](['MS14_D01_S05_L0004'])
  self.assertEqual(out[-1][:2],('dad','(책상 밑을 다시 보자.)'))
  self.assertTrue(out[-1][2]['thought'])
 def test_thought_row_must_be_the_father_without_brackets(self):
  for row in (dict(id='NW_T_T2',speaker='다람',kind='thought',text='x'),dict(id='NW_T_T3',speaker='아빠',kind='thought',text='(x)')):
   with self.assertRaisesRegex(Exception,"thought must be the father"):self.fixture('d01',dict(after={'MS14_D01_S05_L0004':[row]}))
 def test_evidence_name_and_text_revision(self):
  key=next(iter(source_tests.DATA['evidence']));variant=next(iter(source_tests.DATA['evidence'][key]['variants']))
  env=self.fixture('d01',dict(evidence={key:{'name':'새 이름','variants':{variant:'새 설명'}}}))
  self.assertEqual(env['ROOM13']['evidence']['V111:'+key]['name'],'새 이름')
  self.assertEqual(env['ROOM13']['evidence']['V111:'+key]['establishes'],'새 설명')
  self.assertEqual(source_tests.DATA['evidence'][key]['variants'][variant],next(iter(json.loads((ROOT/'game/v111/records.json').read_text())['evidence'][key]['variants'].values())),'source data untouched')
 def test_new_world_record_joins_the_catalog(self):
  env=self.fixture('d01',dict(new_evidence={'NW_TEST':{'name':'새 자료','kind':'물증','variants':{'observed':'처음 보는 돌'}}}))
  self.assertEqual(env['ROOM13']['evidence']['V111:NW_TEST']['establishes'],'처음 보는 돌')
  self.assertEqual(env['R13_RECORD_SHORT']['V111:NW_TEST'],'새 자료')
  self.assertNotIn('NW_TEST',json.loads((ROOT/'game/v111/records.json').read_text())['evidence'],'source data untouched')
  for bad in ({'E01':{'name':'x','kind':'물증','variants':{'a':'b'}}},{'NW_X':{'name':'x','kind':'소문','variants':{'a':'b'}}},{'NW_Y':{'name':'x','kind':'물증','variants':{}}}):
   with self.assertRaises(Exception):self.fixture('d01',dict(new_evidence=bad))
 def test_acquired_new_world_records_exist(self):
  env=self.load();seen=set()
  for name in DAYS:
   for line in (ROOT/'game'/name).read_text().split('\n'):
    if 'r13_nw_acquire(' not in line:continue
    key=re.search(r'r13_nw_acquire\("(\w+)"',line).group(1);self.assertIn(key,env['R13_NW_TEXT']['new_evidence'],name)
    variants=re.findall(r'(?:,|else )"(\w+)"',line) or ['observed']
    for variant in variants:self.assertIn(variant,env['R13_V111']['evidence'][key]['variants'],key)
    seen.add(key)
  self.assertIn('NW_STONE',seen)
 def test_blocks_are_shown_and_every_block_is_used(self):
  env=self.load()
  used=set()
  for name in DAYS:used|=set(re.findall(r"r13_nw_block\(['\"](\w+)['\"]\)",(ROOT/'game'/name).read_text()))
  self.assertEqual(used,set(env['R13_NW_TEXT']['blocks']))
  env['R13_NW_TEXT']['blocks']['qa_block']=[{'id':'NW_QA_1','speaker':None,'text':'보이는 줄'},{'id':'NW_QA_2','speaker':None,'text':'숨는 줄','when':'owl_dead'}]
  env['R13_NW_WHEN']['owl_dead']=lambda:False
  self.assertEqual([r[1] for r in env['r13_nw_block']('qa_block')],['보이는 줄'])
  with self.assertRaises(Exception):env['r13_nw_block']('no_such_block')
 def test_every_proof_asks_for_known_records(self):
  env=self.load();keys=set(env['R13_V111']['evidence'])
  for name in DAYS:
   for m in re.finditer(r"call r13_v111_proof\([^\[]*(\[[^\]]*\])",(ROOT/'game'/name).read_text()):
    for key in ast.literal_eval(m.group(1)):self.assertIn(key,keys,name)
 def test_every_meeting_loss_comes_after_its_retry(self):
  # Three chances (2026-10-22): no meeting result may be written before the retry check.
  for name in DAYS:
   text=(ROOT/'game'/name).read_text()
   for block in text.split('\nlabel ')[1:]:
    if 'r13_nw_retry(' not in block:continue
    first=block.index('r13_nw_retry(')
    for bad in ("r13_nw_meeting_end(","r13_nw_list("):
     if bad in block:self.assertGreater(block.index(bad),first,(name,block.split(':',1)[0]))
 def test_list_conditions_cover_the_transfer_list(self):
  env=self.load()
  rules=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
  listable=ast.literal_eval(re.search(r'R13_NW_LISTABLE=(\([^)]*\))',rules).group(1))
  self.assertEqual(tuple(env['R13_NW_LIST_NAMES']),listable)
  for p in listable:self.assertIn('listed:'+p,env['R13_NW_WHEN'])
 def test_generators_emit_the_layer_call(self):
  for name in ('build_v111_days45.py','build_v111_labels.py'):
   text=(ROOT/'dev'/name).read_text()
   self.assertIn('r13_v111_lines(',text);self.assertNotIn('[r13_v111_line(',text)

class Event01Gate(Layer):
 RIDS=['MS14_D01_S04_L0002','MS14_D01_S04_L0003','MS14_D01_S04_L0004','MS14_D01_S04_L0005','MS14_D01_S04_L0006','MS14_D01_S04_L0008']
 def test_approved_lines_are_in_place(self):
  env=self.load()
  carriage=[r[1] for r in env['r13_v111_lines'](['MS14_D01_S01_L0019','MS14_D01_S01_L0020','MS14_D01_S01_L0021','MS14_D01_S01_L0022'])]
  self.assertEqual(carriage[-4:],['창밖으로 길을 따라 등이 줄지어 서 있었다. 바람이 부는데 불빛이 하나도 흔들리지 않았다.','예쁘다. 꼭 별 같아. 불이 하나도 안 떨려.','기름이 아니라 돌이 들었대. 엄마가 그래서 여기 온 거야.','우리 동네는 기계 난로잖아.'])
  greet=[(r[0],r[1]) for r in env['r13_v111_lines'](['MS14_D01_S04_L0011'])]
  self.assertEqual(greet[2],('guard','아르카 곁에.'))
  room=env['r13_v111_lines'](['MS14_D01_S05_L0016','MS14_D01_S05_L0017'])
  self.assertIn('돌난로',room[0][1]);self.assertEqual(room[1][1],'엄마?')
  self.assertIn('여관에 먼저 연락',env['ROOM13']['evidence']['V111:E02']['establishes'])
 def test_won_gate_keeps_the_authored_registration(self):
  env=self.load()
  texts=[r[1] for r in env['r13_v111_lines'](self.RIDS)]
  self.assertEqual(texts,[source_tests.DATA['records'][r]['text'] for r in self.RIDS])
  after=[r[1] for r in env['r13_v111_lines'](['MS14_D01_S04_L0021'])]
  self.assertIn('정정한 표',after[1]);self.assertEqual(len(after),3)
 def test_lost_gate_leaves_daram_off_the_record(self):
  env=self.load();self.env['r13_v111_set']('gate_daram_unlisted',True)
  texts=[r[1] for r in env['r13_v111_lines'](self.RIDS)]
  self.assertEqual(texts[3],'그렇소. 일꾼 다돌, 외 한 명.')
  self.assertEqual(texts[4],source_tests.DATA['records']['MS14_D01_S04_L0006']['text'],'Daram still asks for her name')
  self.assertEqual(texts[5],'이름 칸이 없소. 표가 그렇게 생겼소.')
  self.assertIn('정정 없음',env['r13_v111_lines'](['MS14_D01_S04_L9101'])[0][1])
  self.assertIn('고친 건 없소',env['r13_v111_lines'](['MS14_D01_S04_L0016'])[0][1])
  after=[r[1] for r in env['r13_v111_lines'](['MS14_D01_S04_L0021'])]
  self.assertNotIn('정정한 표',' '.join(after));self.assertEqual(len(after),3)
  self.assertTrue(env['R13_V111']['evidence']['E05']['variants']['unlisted'].startswith('정정 없음.'))
 def test_gate_flow_retries_until_chances_run_out(self):
  day=(ROOT/'game/room13_v111_days123.rpy').read_text()
  wrong=day.split('label r13_v111_gate_wrong:\n',1)[1].split('\nlabel ',1)[0]
  self.assertIn("r13_v111_set('gate_daram_unlisted',True)",wrong);self.assertIn('jump r13_v111_registered',wrong)
  retry,final=wrong.split("if r13_nw_retry('gate'):",1)
  self.assertIn('jump r13_v111_gate_investigate',final.split('\n')[1])
  self.assertLess(wrong.index('r13_nw_retry'),wrong.index('gate_daram_unlisted'))
  number=day.split('label r13_v111_gate_number:\n',1)[1].split('\nlabel ',1)[0]
  self.assertIn("r13_v111_set('gate_hardened',True)",number)
  proof=(ROOT/'game/room13_v111.rpy').read_text()
  self.assertIn('==["V111:E03"] and not r13_v111_value("gate_hardened")',proof)
  rules=(ROOT/'game/room13_v111_newworld_rules.rpy').read_text()
  self.assertIn('R13_V111_SCENE_CHECKS["MS14_D01_S04"]=r13_nw_gate_entry_decided',rules)

class ContextArtByRecord(Layer):
 def test_approved_cue_survives_added_lines_and_revised_text(self):
  identity='v111:letter_read:MS14_D01_S01_L9101'
  rids=['MS14_D01_S01_L9101','MS14_D01_S01_L0011','MS14_D01_S01_L0012','MS14_D01_S01_L0013','MS14_D01_S01_L0014']
  env=self.load()
  rows=env['r13_v111_lines'](rids)
  # 2026-10-22 script v5 adds the narration 'NW_D01_S01_P01' before the letter, so L0013 is row 4.
  self.assertEqual(env['r13_dialogue_context_match'](identity,4,rows[4],'neutral')['line_id'],'MS14_D01_S01_L0013')
  env=self.fixture('d01',dict(replace={'MS14_D01_S01_L0013':{'text':'십삼 호. 다 외웠어.'}},
   before={'MS14_D01_S01_L0011':[dict(id='NW_T_X1',speaker=None,text='끼운 줄')]}))
  rows=env['r13_v111_lines'](rids)
  self.assertEqual(rows[4][1],'십삼 호. 다 외웠어.')
  self.assertEqual(env['r13_dialogue_context_match'](identity,4,rows[4],'neutral')['line_id'],'MS14_D01_S01_L0013')
  self.assertIsNone(env['r13_dialogue_context_match'](identity,1,rows[1],'neutral'),'added line has no cue')

 def test_approved_day13_cues_have_record_ids_and_match_by_record(self):
  art=json.loads((ROOT/'game/assets/room13-dialogue-context-art.json').read_text())
  cues=[c for c in art['bindings'] if c['identity'].startswith('v111:')]
  self.assertEqual(len(cues),11)
  records=source_tests.DATA['records']
  for c in cues:
   self.assertIn(c['line_id'],records);self.assertEqual(records[c['line_id']]['text'],c['text'])
  layer=LAYER.read_text()
  self.assertIn('cue.get("line_id")==rid and cue["identity"]==identity',layer)

if __name__=='__main__':unittest.main()
