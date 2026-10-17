"""Compile reviewed cues into call-site scopes. Does not infer emotions.

Inline scopes are exact source spans. Provider scopes are explicitly declared
below; only reviewed full text is accepted. Conflicting cues fail closed.
"""
import ast, collections, itertools, json, re, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reviews/dialogue-beats'
def read(name):return json.loads((OUT/(name+'.json')).read_text())
def dump(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
def rows(name):
 d=read(name)['rows'];return list(d.values()) if isinstance(d,dict) else d

def variants(node):
 """Finite authored string/conditional alternatives, never evaluate game state."""
 if isinstance(node,ast.Constant):return [node.value]
 if isinstance(node,ast.IfExp):return variants(node.body)+variants(node.orelse)
 if isinstance(node,ast.BinOp) and isinstance(node.op,ast.Add):
  return [a+b for a,b in itertools.product(variants(node.left),variants(node.right))]
 return []

# Calls whose first argument is a data provider rather than inline packets.
PROVIDERS={
 13:'present',22:'opening',24:'greeting',29:'present',35:'topics',77:'notice',81:'activities',86:'topics',96:'observations',97:'topics',109:'activities',
 169:'alibi',170:'alibi',172:'scale',173:'scale',192:'topics',194:'topics',199:'topics',202:'carry',203:'carry',
 211:'debate',213:'debate',214:'debate',215:'debate',216:'fake',217:'unenforced',218:'debate',219:'debate',220:'debate',221:'debate',222:'debate',223:'debate',224:'debate',226:'debate',227:'debate',
 369:'present',575:'activities',576:'activities',578:'activities',579:'activities',592:'jobs',596:'jobs',605:'topics',606:'debate',607:'debate',609:'opinions',611:'grudges',612:'song',664:'topics',665:'topics',718:'kongi',739:'topics',743:'topics'}
FILES={
 'observations':['room13_thoughts.rpy'], 'alibi':['systems/room13_alibi.rpy'], 'scale':['systems/room13_bundle3.rpy','systems/room13_items.rpy'],
 'carry':['systems/room13_carryover.rpy','systems/room13_week1_cases.rpy'], 'jobs':['systems/room13_new_places.rpy'], 'fake':['systems/room13_week1_cases.rpy'],
 'unenforced':['systems/room13_episodes.rpy'], 'grudges':['systems/room13_memory.rpy'], 'song':['systems/room13_new_cast.rpy'],
 'kongi':['systems/room13_town_events.rpy'], 'opinions':['systems/room13_meeting_flow.rpy'],
 'debate':['systems/room13_debate.rpy','systems/room13_debate_points.rpy','systems/room13_meeting_flow.rpy','systems/room13_episodes.rpy','systems/room13_week1_cases.rpy','systems/room13_story_continuity.rpy']+['systems/room13_ep%d_%s.rpy'%(n,s) for n,s in enumerate(['lamp_thief','kids','woodfire','night13','soup','cart'],1)]}

def compile_registry():
 q=read('runtime-binding-queue'); static=json.loads((ROOT/'game/assets/room13-dialogue-beats.json').read_text())['lines']
 reviews=[]
 for name in ('dynamic-context-review','dynamic-expression-review','opening-context-review','supplemental-context-review','dynamic-duplicate-review','expanded-context-review','binding-additional-review'):
  for n,r in enumerate(rows(name)):
   reviews.append(dict(r,review_ref=name+':'+str(n)))
 # Exact static packet reuse is only permitted within its source call span or topic.
 for call in q:
  if call.get('identity') in static:
   for r in static[call['identity']].values():
    reviews.append(dict(r,source=call['source'],line=call['line'],context_identity=call['identity'],review_ref='static:'+call['identity']))
 for identity,rr in static.items():
  if identity.startswith('topic:'):
   for r in rr.values():reviews.append(dict(r,source='static_topic',context_identity=identity,review_ref='static:'+identity))
 # Expand only finite composed alternatives; runtime output selects the actual one.
 for n,r in enumerate(read('composed-context-review')['rows']):
  for who,text in itertools.product(variants(ast.parse(r['who_expression'],mode='eval').body),variants(ast.parse(r['text_expression'],mode='eval').body)):
   reviews.append(dict(r,person=who,text=text,review_ref='composed:'+str(n)))
 # Four reviewed components make one complete postal reply, never four cues.
 base='그분이 남긴 글씨군요. 맡아 둔 것을 찾아볼게요. '
 for day in ('내일','모레'):
  reviews.append(dict(source='game/systems/room13_first_day_flow.rpy',line=61,person=None,text=base+day+' 다시 와 주시겠어요?',emotion='neutral',reaction=False,reviewed=True,review_ref='expression:assembled-postal-reply'))
 routes={}
 for i,call in enumerate(q):
  if call['binding_status']=='static_exact_binding_available':continue
  group=PROVIDERS.get(i,'inline'); start=call['line'];end=start+call['call_expression'].count('\n')
  def allowed(r):
   source=r['source'];line=r.get('line',-1)
   if source==call['source'] and start<=line<=end:return True
   if group=='scale' and r.get('context_identity') in ('topic:eunho_scale','topic:review:eunho_scale'):return True
   if group in FILES:
    if source not in ['game/'+f for f in FILES[group]]:return False
    if group=='debate' and line>0:
     first_label=next((j for j,l in enumerate((ROOT/source).read_text().splitlines(),1) if l.startswith('label ')),100000)
     if line>=first_label:return False
    return True
   if group in ('opening','notice'):return source in ('game/room13-dialogue-openings.json','game/room13_dialogue_openings_20261013.rpy')
   if group=='greeting':return 'GREETING' in r.get('lookup','') or (source in ('game/room13_life.rpy','game/room13_home.rpy','game/room13_gate_continuity.rpy'))
   if group=='present':
    if source.endswith(('room13_items.rpy','room13_new_cast.rpy')):return True
    if 'r13_present(' in r.get('context','') or 'r13_dialogue_granny_reply(' in r.get('context',''):return True
    if source.endswith('.rpy') and line>0:
     lines=(ROOT/source).read_text().splitlines();headers=[x.strip() for x in lines[:line] if re.match(r'\s*(def |label )',x)]
     return bool(headers and ('def r13_present(' in headers[-1] or 'def r13_dialogue_granny_reply(' in headers[-1]))
    return source.endswith('room13-content.json') and r.get('path',[''])[0] in ('present','presentations','residents')
   if group=='activities':return (r.get('path',[''])[0]=='activities' or source.endswith('room13_items.rpy') or source==call['source'])
   if group=='topics':
    # Topic key narrowing happens again at runtime; no unrelated static scenes.
    return source in ('static_topic','game/room13-dialogue-expand.json') or r.get('path',[''])[0] in ('with_daram','calendar_companion') or (source.endswith('.rpy') and not r.get('context','').startswith('label '))
   return False
  selected=[r for r in reviews if allowed(r)]
  # Full-text variants for calendar composed replies, retaining explicit refusal dominance.
  if group=='opening':
   for person in sorted({r.get('person') for r in selected} - {None,'dad'}):
    own=[r for r in selected if r.get('person')==person]
    heads=[r for r in own if r.get('path',[''])[0]=='calendar_ready' or (r['source'].endswith('.rpy') and r.get('line')==117)]
    tails=[r for r in own if r.get('path',[''])[0] in ('calendar_daily','calendar_ready_late','calendar')]
    for h,t in itertools.product(heads,tails):
     selected.append(dict(t,text=h['text']+' '+t['text'],review_ref=h['review_ref']+'+'+t['review_ref']))
    if person=='buri':
     suffix=next(r for r in own if r.get('line')==127)
     for r in list(selected):
      if r.get('person')==person and r!=suffix:
       selected.append(dict(r,text=r['text']+suffix['text'],emotion='angry',reaction=False,review_ref=r['review_ref']+'+refused'))
  compact=[];seen=set()
  for r in selected:
   # Metadata fragments are not allowed to stand alone at runtime.
   if not r.get('reviewed') or not r.get('text'):continue
   c={k:r[k] for k in ('person','text','emotion','reaction','review_ref') if k in r}
   c['person']=r.get('person')
   if 'context_identity' in r:c['context_identity']=r['context_identity']
   c['source']=r['source'];c['source_line']=r.get('line');c['path']=r.get('path')
   key=json.dumps(c,sort_keys=True)
   if key not in seen:compact.append(c);seen.add(key)
  route='dynamic:%03d'%i
  routes[route]=dict(source=call['source'],line=start,group=group,cues=compact)
 pool={}
 for route in routes.values():
  refs=[]
  for cue in route['cues']:
   key=hashlib.sha256(json.dumps(cue,sort_keys=True,ensure_ascii=False).encode()).hexdigest()[:20]
   pool[key]=cue;refs.append(key)
  route['cues']=refs
 sequences=[]
 for name in ('expanded-context-review','supplemental-context-review'):
  grouped=collections.defaultdict(list)
  for r in rows(name):
   path=r.get('path',[])
   if name=='expanded-context-review':key=path[0].split('#')[0]; container=path[:-1]
   elif path and path[0]=='with_daram':key=path[1];container=path[:-1]
   else:continue
   grouped[(r['source'],tuple(container),key)].append(r)
  for (source,path,key),rr in grouped.items():
   packets=json.loads((ROOT/source).read_text())
   for part in path:packets=packets[part]
   mapped={str(r['path'][-1]):dict(person=r['person'],text=r['text'],emotion=r['emotion'],reaction=r['reaction'],review_ref=name+':'+str(r['path']),reviewed=True) for r in rr}
   sequences.append(dict(topic=key,packets=[list(p[:2]) for p in packets],cues=mapped))
 return dict(status='local_binding_assets_held',routes=routes,cues=pool,sequences=sequences)

if __name__=='__main__':
 registry=compile_registry();dump(ROOT/'game/assets/room13-dialogue-bindings.json',registry)
 print('Compiled',len(registry['routes']),'call-site scopes; no art activated')
