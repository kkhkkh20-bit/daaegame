"""Execute real dialogue expressions/calendar selectors over bounded state matrices."""
import hashlib,ast,copy,itertools,json,textwrap,types
from pathlib import Path
from build_dialogue_bindings import ROOT,OUT,read,dump

def load_functions(path):
 source=path.read_text();parts=[]
 import re
 for m in re.finditer(r'^init(?: -?\d+)? python:\n((?:[ \t].*\n|\n)*)',source,re.M):
  tree=ast.parse(textwrap.dedent(m[1]));parts += [n for n in tree.body if isinstance(n,ast.FunctionDef)]
 env={};exec(compile(ast.Module(body=parts,type_ignores=[]),str(path),'exec'),env);return env

def binder():
 env=load_functions(ROOT/'game/systems/room13_dialogue_bindings.rpy')
 registry=json.loads((ROOT/'game/assets/room13-dialogue-bindings.json').read_text())
 return lambda rows,identity,route:env['r13_bind_dialogue_rows'](rows,identity,route,registry)

def inline_cases():
 q=read('runtime-binding-queue')
 for i,r in enumerate(q):
  if r['binding_status']=='static_exact_binding_available':continue
  from build_dialogue_bindings import PROVIDERS
  if i in PROVIDERS:continue
  node=ast.parse('f('+r['call_expression']+')',mode='eval').body
  flags=sorted({n.args[0].value for n in ast.walk(node) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='r13_has' and n.args and isinstance(n.args[0],ast.Constant)})
  for bits in itertools.product((False,True),repeat=len(flags)):
   for child in ('with_dad','held','rescued'):
    active={f for f,b in zip(flags,bits) if b};state=dict(daram_state=child,location='plaza',day=7,period=1,granny_state='detained')
    env=dict(presentation_rows="독백",ROOM13=json.loads((ROOT/"game/room13-content.json").read_text()),r13_item=next(iter(json.loads((ROOT/"game/room13-content.json").read_text())["sensitive"])),room13=state,r13_has=lambda f:f in active,r13_cv_daram=lambda:child!='held',r13_ws_daram=lambda:child!='held',late=False,_gain=['transport_terms'] if child=='with_dad' else [],_r='rumor:fair',R13_RUMOR_WHISPERS={'rumor:fair':'소문'},R13_CARRIAGE_IDENTITY='carriage:intro',r13_target='granny',R13_GREETING={'granny':'인사'},person='daram' if child=='with_dad' else 'buri',key='bag:spool',_who='buri',r13_activity_text=lambda p:'작업',r13_evening_missions=lambda:[],_news=['소식'],_gcost=20,_gk='buri',_eh_where='식량',r13_point={'ask':'확인'},claim='C1',sid='s1',r13_claim='C1',r13_debate_st={'who':'granny'},observed_identity='observed')
    args=[eval(compile(ast.Expression(a),'call-expression','eval'),env) for a in node.args]
    yield 'dynamic:%03d'%i,args[1],args[0],dict(flags=sorted(active),daram_state=child)

def opening_cases():
 env=load_functions(ROOT/'game/room13_dialogue_openings_20261013.rpy');data=json.loads((ROOT/'game/room13-dialogue-openings.json').read_text());state={};flags=set()
 env.update(r13_hashlib=hashlib,r13_opening_json=json,ROOM13=json.loads((ROOT/"game/room13-content.json").read_text()),store=types.SimpleNamespace(room13=state),R13_OPENING_SCENES=data,R13_CALENDAR=data['calendar'],R13_WEEK2_DAY=7,r13_tl=lambda n:n,r13_has=lambda f:f in flags)
 for person in data['first_meetings']:
  for day,case,trial,child in itertools.product(range(1,15),('pending','occurred','prevented'),('pending','cleared'),('with_dad','held','rescued')):
   for bits in itertools.product((False,True),repeat=3 if person=='bami' else 2 if person=='buri' else 1):
    flags.clear();ready=data['calendar_ready'].get(person)
    if bits[0] and ready:flags.add(ready[0])
    if len(bits)>1 and bits[1]:flags.add('buri_refused' if person=='buri' else 'bami_protected')
    if person=='bami' and bits[2]:flags.add('bami_pressured')
    state.clear();state.update(day=day,period=2,case_state=case,trial_result=trial,trial_ended=trial!='pending',daram_state=child,victim_state='dead' if case=='occurred' else 'alive',dialogue_dates={'life:'+person+':work':{'day':day-1}})
    for first in (False,True):
     rows=env['r13_conversation_opening'](person,first)
     identity='greeting:opening:calendar:'+person+':'+str(day)+':'+str(first)
     yield 'dynamic:022',identity,rows,dict(person=person,first=first,flags=sorted(flags),**state)
     yield 'dynamic:077','notice:resident:'+person,env['r13_resident_notice'](person),dict(person=person,**state)

def audit():
 bind=binder();unresolved={};count=0;lines=0
 for route,identity,rows,state in itertools.chain(inline_cases(),opening_cases()):
  result=bind(rows,identity,route);count+=1;lines+=len(result['rows'])
  for u in result['unresolved']:
   key=(route,u['person'],u['text'],u['reason'])
   unresolved.setdefault(key,dict(route=route,identity=identity,state=state,**u))
 result=dict(evaluated_cases=count,bound_npc_occurrences=lines,unresolved=list(unresolved.values()),scope='Inline branch expressions and real calendar/opening/notice selectors. Provider matrices tracked separately.')
 dump(OUT/'binding-state-results.json',result);print('cases',count,'bound',lines,'unique unresolved',len(unresolved))
 for r in list(unresolved.values())[:30]:print(r['route'],r['reason'],r['person'],r['text'][:80])
 return result
if __name__=='__main__':audit()
