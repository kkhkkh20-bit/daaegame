import ast,copy,importlib.util,json,pathlib,re,textwrap,types
w=pathlib.Path('/workspace/work/dialogue-review');r=pathlib.Path('/workspace/daaegame/reports/dialogue-revision-20261013');base=w/'base/game';new=w/'revised/game';data=json.loads((new/'room13-content.json').read_text());scenes=json.loads((r/'room13-dialogue-openings.json').read_text())
module=ast.parse(textwrap.dedent((new/'room13_dialogue_openings_20261013.rpy').read_text().split('init 58 python:\n',1)[1]))
helpers=[x for x in module.body if isinstance(x,ast.FunctionDef)]
def treefunc(path,name):
 text=path.read_text();match=re.search(r'^    def '+re.escape(name)+r'\(.*?(?=^    def |\Z)',text,re.M|re.S);assert match,name
 block=match.group().split('\n\n    #',1)[0];return ast.parse(textwrap.dedent(block)).body[0]
core={'granny','nabi','buri','karo','bami','doto','resident_owlgp','resident_tok','resident_lamplighter','seryeon','neoul'}
people=list(scenes['first_meetings'])
def run(path,state,person):
 store=types.SimpleNamespace(room13=copy.deepcopy(state));trace=[]
 ns={'store':store,'room13':store.room13,'winter_copy':copy,'r13_target':person,'R13_CORE_PEOPLE':core,'R13_GREETING':{p:'existing greeting' for p in people},'R13_OPENING_SCENES':scenes,'ROOM13':data}
 exec(compile(ast.Module(body=[treefunc(base/'room13_life.rpy','r13_note_encounter'),treefunc(base/'room13_life.rpy','r13_met_people'),treefunc(base/'room13_rules.rpy','r13_flag'),treefunc(base/'room13_rules.rpy','r13_has')]+helpers,type_ignores=[]),'<functions>','exec'),ns)
 ns['r13_activity_text']=lambda p:data['residents'][p]['activity'];ns['record_lines']=lambda rows,key:trace.append((key,rows))
 code=path.read_text().split('label r13_talk:\n',1)[1].split('label r13_person_actions:',1)[0]
 code=re.sub(r'^(\s*)\$ ',r'\1',code,flags=re.M).replace('call r13_lines(', 'record_lines(')
 # RenPy's `room13` is a store variable. Update it after the actual deepcopy helpers.
 for name in ['r13_note_encounter','r13_flag']:
  f=ns[name]
  def sync(*args,_f=f):
   result=_f(*args);ns['room13']=store.room13;return result
  ns[name]=sync
 exec(compile(textwrap.dedent(code),'<talk-entry>','exec'),ns)
 return store.room13,trace,ns
count=0
for day,case,victim,child,flags in [(1,'pending','alive','with_dad',[]),(5,'occurred','dead','held',[]),(9,'occurred','dead','rescued',[]),(5,'occurred','dead','held',['bami_pressured'])]:
 for person in people:
  for met in [False,True]:
   s={'day':day,'period':1,'location':'square','case_state':case,'victim_state':victim,'daram_state':child,'flags':flags[:],'evidence':[],'encounters':[{'person':person,'day':max(1,day-1),'period':0,'place':'inn'}] if met else []}
   original,_,_=run(base/'room13.rpy',s,person);revised,trace,ns=run(new/'room13.rpy',s,person);assert original==revised,(day,person,met)
   if not met and day==1:assert trace[0][0].endswith(':first'),(person,trace)
   if met and day==1:assert trace[0][0].endswith(':return')
   if person=='bami' and 'bami_pressured' in flags:assert trace[0][0]=='greeting:bami:pressured'
   if person=='buri' and victim=='dead':assert trace[0][0]=='greeting:buri:bereaved'
   # Same-day reopening must not replay introductions or spend time.
   after,again,_=run(new/'room13.rpy',revised,person);assert after==revised and not again
   if day==1 and not met:
    restored=copy.deepcopy(revised);restored['day']=2
    _,nextday,_=run(new/'room13.rpy',restored,person);assert nextday[0][0].endswith(':return')
   count+=1
combo=0
for key,rows in scenes['with_daram'].items():
 for child in ['with_dad','rescued','held','lost']:
  s={'day':1,'case_state':'pending','daram_state':child};_,_,ns=run(new/'room13.rpy',dict(s,period=1,location='square',victim_state='alive',flags=[],evidence=[],encounters=[]),'doto')
  chosen=ns['r13_conversation_topic_lines'](key)
  if child in ['with_dad','rescued']:
   assert any(who=='daram' for who,line in chosen);assert any(who=='dad' for who,line in chosen)
  else:assert chosen==data['topics'][key]['lines'] and not any(who=='daram' for who,line in chosen)
  combo+=1
# Latest code outside the listed replacements must be byte-for-byte preserved.
ps=json.loads((r/'runtime-patch.json').read_text())
for file in {x['file'] for x in ps}:
 text=(new/file).read_text()
 for p in reversed([p for p in ps if p['file']==file]):
  assert text.count(p['after'])==1; text=text.replace(p['after'],p['before'],1)
 assert text==(base/file).read_text()
result={'passed':True,'first_and_repeat_entry_cases':count,'optional_companion_cases':combo,'first_meeting_uses_existing_encounters':True,'same_day_no_repeat':True,'next_day_not_stranger':True,'pressured_and_bereaved_greetings_prioritized':True,'encounters_flags_costs_evidence_identical':True,'child_absence_keeps_adult_topic':True,'latest_other_code_preserved':True,'limits':['Entry-label Python translation and runtime helper execution; not RenPy engine playthrough','First-meeting scene added; no new clues, rewards, costs or biography invented','Main game not rebuilt/deployed']}
(r/'conversation-verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False))
