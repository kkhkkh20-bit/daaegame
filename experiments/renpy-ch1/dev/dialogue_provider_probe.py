"""Run with the real Ren'Py store after init; no disk/save/gameplay mutations."""
def probe(s):
 import json,itertools
 results=[];missing={};seen_routes=set()
 old_defer=s.r13_defer_grants;s.r13_defer_grants=True
 base=s.r13_new();old=getattr(s,"room13",None);old_cue=s.r13_fx_cue;s.r13_fx_cue=lambda *args,**kwargs:None;old_fx=s.source_fx;s.source_fx=lambda *args,**kwargs:None
 def check(route,identity,rows,state):
  result=s.r13_bind_dialogue_rows(rows,identity,route,s.R13_DIALOGUE_BINDINGS);seen_routes.add(route)
  results.append((route,len(result['rows'])))
  for u in result['unresolved']:
   missing.setdefault((route,u['person'],u['text'],u['reason']),dict(route=route,identity=identity,state=state,**u))
 try:
  # Real final init registry, including init-added topics and overwritten data.
  for key,spec in s.ROOM13['topics'].items():
   for child in ('with_dad','held','rescued'):
    s.room13=dict(base,day=7,daram_state=child,flags=[],read_topics=[])
    rows=s.r13_conversation_topic_lines(key)
    check('dynamic:035','topic:'+key,rows,dict(key=key,child=child))
    check('dynamic:664','topic:record_full:'+key,rows,dict(key=key,child=child))
    if key.startswith(('item:','return:')) or key=='life:snack':check('dynamic:605','material:accepted:'+key,rows,dict(key=key,child=child))
    if key=='tool:seam':check('dynamic:097','topic:tool:seam',rows,dict(child=child))
    s.room13['read_topics']=[key]
    check('dynamic:665','topic:review:'+key,s.r13_conversation_topic_lines(key),dict(key=key,child=child,read=True))
  for key,spec in s.ROOM13['activities'].items():
   check('dynamic:081','activity:'+key,spec.get('lines',[]),dict(key=key))
   check('dynamic:109','activity:'+key,spec.get('lines',[]),dict(key=key))
  for person,text in s.R13_GREETING.items():check('dynamic:024','greeting:'+person,[(person,text)],dict(person=person))
  # All authored debate data paths, including soft/broken_by/counters/conclusion.
  def walk(value,path=()):
   if isinstance(value,dict):
    if 'who' in value and 'text' in value:yield path,[(value['who'],value['text'].replace('【','').replace('】',''))]
    for k,v in value.items():yield from walk(v,path+(k,))
   elif isinstance(value,(list,tuple)):
    if value and isinstance(value[0],(list,tuple)) and all(len(p)>=2 and (p[0] is None or p[0] in s.R13_CHARS) and isinstance(p[1],str) and any('가'<=c<='힣' for c in p[1]) for p in value):yield path,value
    elif len(value)>=2 and (value[0] is None or isinstance(value[0],str) and value[0] in s.R13_CHARS) and isinstance(value[1],str) and any('가'<=c<='힣' for c in value[1]):yield path,[value]
    else:
     for i,v in enumerate(value):yield from walk(v,path+(i,))
  for path,rows in walk(s.R13_DEBATE):check('dynamic:607','debate:'+':'.join(map(str,path)),rows,dict(path=path))
  for name,route in [('R13_JOB_START_LINES','dynamic:592'),('R13_JOB_ASK_LINES','dynamic:596'),('R13_ALIBI','dynamic:169'),('R13_GRUDGES','dynamic:611'),('R13_CARRY_GOOD','dynamic:202'),('R13_CARRY_REFUSE','dynamic:203')]:
   for path,rows in walk(getattr(s,name,{})):check(route,name+':'+str(path),rows,dict(path=path))
  for key,packets in s.R13_OBSERVATION_CHAT.items():
   for child in ('with_dad','held'):
    s.room13=dict(base,flags=['entry_corrected'],daram_state=child)
    identity='object:'+':'.join(key)
    check('dynamic:096',identity+':dad-thought-v1',s.r13_make_observation_lines([(None,'관찰')],identity),dict(child=child,key=key))
  for route,name in [('dynamic:216','R13_FAKE_TESTIMONY_LINES'),('dynamic:217','R13_C4_UNENFORCED')]:check(route,name,getattr(s,name),{})
  scale=s.ROOM13['topics']['eunho_scale']['lines']
  check('dynamic:172','b3:scale:open',scale[:1]+[('resident_eunho','……그래서, 저한테 무엇을 원하십니까?')],{})
  check('dynamic:173','b3:scale:quiet',scale[1:],{})
  for cross in s.R13_ALIBI_CROSS:check('dynamic:170','alibi:cross:'+cross[2],cross[1],{})
  for session,stance,person in itertools.product(('trial','finale'),range(3),s.R13_GREETING):
   check('dynamic:609','meeting:opinions:C1:choice',s.r13_meeting_reaction_lines(dict(session=session,changed=[dict(person=person,to=stance)])),dict(session=session,stance=stance,person=person))
  for place,day,caught in itertools.product(('store','workshop','post','kitchen'),(1,2,3,7),(False,True)):
   check('dynamic:718','ev:m:report:'+place,s.r13_kongi_report(place,day,['ev_b_caught'] if caught else [])[0],dict(place=place,day=day,caught=caught))
  songflags=['ev_e_done','tools_sold','mom_hideout_found','w2_bell_silent']
  for bits in itertools.product((False,True),repeat=5):
   flags=[f for f,b in zip(songflags,bits) if b]
   s.room13=dict(base,flags=flags,case_state='occurred' if bits[-1] else 'pending')
   check('dynamic:612','hyeoni:song:7:1',[('resident_hyeoni',v) for v in s.r13_hyeoni_verses()],dict(flags=flags,case=s.room13['case_state']))
  # Direct topic aliases and activity slices do not rebuild their transcript.
  for route,key,identity in [('dynamic:086','w2_eunho','negotiation:supplies:opening'),('dynamic:192','librarian_stone','b3:pages:stone'),('dynamic:194','librarian_stone','b3:pages:stone'),('dynamic:199','librarian_stone','b3:buy:stone'),('dynamic:743','life:karo','w1c:karo:work')]:
   check(route,identity,s.ROOM13['topics'][key]['lines'],dict(key=key))
  for key in s.R13_MEDKIT_RESULTS:check('dynamic:739','medkit:'+key,s.ROOM13['topics'][key]['lines'],dict(key=key))
  for route,key,cut in [('dynamic:575','use_knife_burlap',1),('dynamic:576','use_lantern_rear',0),('dynamic:578','use_knife_under',1),('dynamic:579','use_rubbing_stone',1)]:
   check(route,'activity:'+key+(':read' if cut else ''),s.ROOM13['activities'][key]['lines'][cut:],dict(key=key))
  for claim,spec in s.R13_DEBATE.items():
   for st in spec['statements']:
    s.room13=dict(base,flags=[],evidence=[],propositions=[])
    check('dynamic:606','meeting:live:'+claim+':'+st['id'],s.r13_meeting_live_rows(claim,st['id']),dict(claim=claim,sid=st['id']))
    check('dynamic:213','meeting:replay:'+claim+':'+st['id'],[(st['who'],st['text'].replace('【','').replace('】',''))]+st.get('press',[]),dict(claim=claim,sid=st['id']))
    check('dynamic:214','debate:press_missing:'+claim+':'+st['id'],st.get('press_missing',[(st['who'],'그래서, 있습니까?')]),dict(claim=claim,sid=st['id']))
    check('dynamic:215','debate:press:'+claim+':'+st['id'],st.get('press',[(st['who'],'말한 그대로입니다.')]),dict(claim=claim,sid=st['id']))
  # Counter, conclusion, partial, and gap output use the same final-init dictionaries.
  for claim,spec in s.R13_DEBATE.items():
   s.room13=dict(base,flags=[],evidence=[],propositions=[])
   check('dynamic:211','debate:partial:'+claim,s.r13_debate_partial_lines(claim),dict(claim=claim))
   conclusion=spec['conclusion']
   check('dynamic:222','debate:conclusion:'+claim,conclusion['correct'],dict(claim=claim))
   for choice in ('weak','over'):
    check('dynamic:223','debate:conclusion_wrong:'+claim+':'+choice,[conclusion[choice]],dict(claim=claim,choice=choice))
   point=conclusion.get('point')
   if point:
    for choice in list(point.get('wrong_who',{}))+['unknown']:
     check('dynamic:224','debate:point_wrong:'+claim+':'+choice,[point.get('wrong_who',{}).get(choice,conclusion['over'])],dict(claim=claim,choice=choice))
    for key,rows in point.get('decisive',{}).items():check('dynamic:226','debate:conclusion:'+claim,list(rows)+list(conclusion['correct']),dict(claim=claim,key=key))
    check('dynamic:227','debate:point_key_wrong:'+claim+':wrong',[point['wrong_key']],dict(claim=claim))
   for st in spec['statements']:
    check('dynamic:218','debate:unanswerable:'+claim,[(st['who'],st['text'].replace('【','').replace('】',''))]+s.r13_debate_gap_lines(claim,st),dict(claim=claim,sid=st['id']))
    counter=st.get('counter')
    if counter:
     check('dynamic:219','debate:counter:'+claim+':'+st['id'],counter['lines'],dict(claim=claim,sid=st['id']))
     check('dynamic:220','debate:counter_ok:'+claim+':'+st['id'],counter['correct'],dict(claim=claim,sid=st['id']))
     for key,row in counter['wrong'].items():check('dynamic:221','debate:counter_wrong:'+claim+':'+st['id']+':'+key,[row],dict(claim=claim,sid=st['id'],key=key))
  import pathlib,textwrap
  source=pathlib.Path(s.config.basedir+'/game/systems/room13_carryover.rpy').read_text()
  block=source.split('    python:\n',1)[1].split('    if not _carry',1)[0]
  for flags in [[],['bori_hostile'],['bori_punished'],['eunho_blackmailed'],list(s.R13_BAD_RUMORS),list(s.R13_BAD_RUMORS)+['rumor:fair']]:
   s.room13=dict(base,flags=flags,evidence=[]);env=dict(vars(s),_carry=[]);exec(textwrap.dedent(block),env)
   for flag,rows in env['_refuse']:check('dynamic:203','carry:refuse:'+flag,rows,dict(flags=flags))
  s.room13=dict(base,flags=[],evidence=['N08'])
  check('dynamic:369','nt:ppul:board',s.r13_present('resident_ppul','N08'),{})
  # Present uses the actual chain of wrappers. Reset state per response.
  flagsets=[[],['mom_identity','buri_honest','bami_consent'],['buri_refused','bami_identity_leaked','bami_pressured'],['mom_hideout_found','librarian_dead','chorong_dead','kkomi_dead']]
  for flags in flagsets:
   for person in s.R13_GREETING:
    for key in s.ROOM13['evidence']:
     s.room13=dict(base,day=7,period=1,flags=list(flags),evidence=[key],read_topics=[],presented=[])
     for disclose in (False,True):
      rows=s.r13_present(person,key,disclose)
      if rows:
       check('dynamic:029','present:'+person+':'+key+':'+str(disclose),rows,dict(person=person,key=key,flags=flags,disclose=disclose))
       if person=='karo':check('dynamic:013','entry:karo:present:'+key,rows,dict(key=key,flags=flags))
  return dict(cases=len(results),bound_occurrences=sum(n for _,n in results),tested_routes=sorted(seen_routes),unresolved=list(missing.values()),scope='Actual final-init data and presentation wrapper chain; bounded state matrix, not full gameplay QA')
 finally:s.room13=old;s.source_fx=old_fx;s.r13_fx_cue=old_cue;s.r13_defer_grants=old_defer
