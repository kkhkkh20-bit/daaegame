import ast,copy,importlib.util,json,pathlib,shutil,textwrap,types
root=pathlib.Path('/workspace/daaegame/reports/dialogue-revision-20261013');base=pathlib.Path('/workspace/work/dialogue-review/base/game');new=pathlib.Path('/workspace/work/dialogue-review/revised/game')
a=json.loads((base/'room13-content.json').read_text());b=json.loads((new/'room13-content.json').read_text());patch=json.loads((root/'content-patch.json').read_text())
# Exact whole-object comparison after undoing the approved prose fields.
restored=copy.deepcopy(b)
for p in patch:
 x=restored
 for k in p['path'][:-1]:x=x[k]
 x[p['path'][-1]]=p['before']
assert restored==a,'Non-dialogue data changed'
names=set()
for t in b['topics'].values(): names.add(t['npc'])
names.update(['dad','daram','mom','granny','buri','bami','nabi','karo'])
for p in patch:
 if p['path'][-1]=='lines':
  for who,text in p['after']:assert (who is None or who in names) and isinstance(text,str) and text.strip(),(who,text)
assert not any('제 식구가 있는 자리부터 확인하려고요' in str(t['lines']) or '말씀하신 건 기억하겠습니다' in str(t['lines']) for t in b['topics'].values())
def functions(path):
 text=path.read_text();block=text.split('init 55 python:\n',1)[1];return ast.parse(textwrap.dedent(block))
oldast=functions(base/'room13_rules.rpy');newast=functions(new/'room13_rules.rpy')
def env(tree,state):
 store=types.SimpleNamespace(room13=copy.deepcopy(state));ns={'store':store,'winter_copy':copy,'R13_CORE_PEOPLE':['granny','buri','nabi','bami','karo'],'R13_RESIDENTS':{},'ROOM13':a}
 ns['r13_has']=lambda k:k in store.room13['flags'] or k in store.room13['evidence']
 def flag(*ks):
  for k in ks:
   if k not in store.room13['flags']:store.room13['flags'].append(k)
 ns['r13_flag']=flag;ns['r13_w2_present']=lambda *args:None
 picked=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name in ['r13_present','r13_dialogue_granny_reply']]
 exec(compile(ast.Module(body=picked,type_ignores=[]),'<runtime-functions>','exec'),ns)
 return ns,store
count=0
for person,keys in [('granny',['E05','E09','E10','E13','E14','E35','E36','E18']),('buri',['E06','E08'])]:
 for key in keys:
  for repeated in [False,True]:
   for identity in [False,True]:
    for flags in [[],['medical_consent'],['buri_refused']]:
     s={'day':5,'evidence':list(a['evidence']),'resident_knowledge':{},'flags':flags[:],'records':{}}
     if repeated:s['resident_knowledge'][person]=[key+(':named' if identity else ':anonymous')]
     n1,s1=env(oldast,s);n2,s2=env(newast,s)
     l1=n1['r13_present'](person,key,identity);l2=n2['r13_present'](person,key,identity)
     assert s1.room13==s2.room13,(person,key,repeated,identity,flags)
     assert l2 and all(isinstance(v,(tuple,list)) and len(v)==2 and isinstance(v[1],str) for v in l2)
     if person=='granny' and key=='E10' and not identity:assert '밤이' not in str(l2),'Anonymous testimony identifies witness'
     count+=1
spec=importlib.util.spec_from_file_location('rev',root/'apply_revision.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
assert m.apply_content(b)==b
bad=copy.deepcopy(a);bad['topics']['buri_records']['lines'][0][1]='다른 개발자가 고친 대사'
try:m.apply_content(bad)
except ValueError:pass
else:raise AssertionError('Concurrent dialogue change was overwritten')
fixture=pathlib.Path('/workspace/work/dialogue-review/generator-fixture');(fixture/'dev').mkdir(parents=True,exist_ok=True);shutil.copytree(base,fixture/'game',dirs_exist_ok=True)
shutil.copy('/workspace/work/room13-recovery/source/experiments/renpy-ch1/dev/build_room13_content.py',fixture/'dev')
m.install(fixture,True)
compile((fixture/'dev/build_room13_content.py').read_text(),'<content-generator>','exec')
# Exercise the installed generation hook on the latest runtime data.
spec=importlib.util.spec_from_file_location('generated',fixture/'dev/room13_dialogue_revision.py');h=importlib.util.module_from_spec(spec);spec.loader.exec_module(h);assert h.apply_content(a)==b
report={'passed':True,'base_commit':pathlib.Path('/workspace/work/dialogue-review/base-commit.txt').read_text(),'content_fields_changed':len(patch),'topics_revised':len([p for p in patch if p['path'][0]=='topics']),'runtime_state_equivalence_cases':count,'non_prose_content_identical':True,'generator_hook_compile_and_apply':True,'idempotent':True,'concurrent_prose_change_rejected':True,'anonymous_witness_not_named':True,'limits':['RenPy SDK unavailable: no engine lint or rebuilt browser playthrough','Generator hook tested with latest runtime data; full regeneration on developer source still required','New branches, costs, evidence and ending conditions not implemented or changed']}
(root/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False))
