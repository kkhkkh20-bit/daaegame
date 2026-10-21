"""Reviewed D04–D05 native-label authoring. Never used as a runtime engine.
Source record IDs and reviewed field callbacks; no natural-language conditions.
Does not regenerate or overwrite the owner's D01–D03 revisions.
"""
import copy,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MASTER=json.loads(next((ROOT/'docs/story-v111/source').glob('*.json')).read_text())
DATA=json.loads((ROOT/'game/v111/records.json').read_text())
SOURCE={c['source_record']['id']:c for s in MASTER['scenes'] for b in s['blocks'] for c in b['cues']}
SCENES={s['source_scene']['scene_id']:s for s in MASTER['scenes']}
DATA['ambience']={sid:s['audio'].get('ambience_key') for sid,s in SCENES.items()}
def scalar(x):
 if x=='true':return True
 if x=='false':return False
 if re.fullmatch(r'-?\d+',x):return int(x)
 return x
for sid,s in SCENES.items():
 if s['source_scene']['day'] not in (4,5):continue
 DATA['scene_days'][sid]=s['source_scene']['day'];DATA['audio'][sid]=s['audio']['file']
 for b in s['blocks']:
  for c in b['cues']:
   r=copy.deepcopy(c['source_record']);ops=[]
   for effect in r.get('effects',[]):
    if re.fullmatch(r'acquire\(E\d+\)',effect):ops.append(dict(op='acquire',key=effect[8:-1],variant='observed'))
    elif '='in effect:
     k,v=effect.split('=',1);ops.append(dict(op='set',field=k,value=scalar(v)))
    else:raise ValueError((r['id'],effect))
   r.update(operations=ops,direction=c['directed_expression']);DATA['records'][r['id']]=r
DATA['evidence']['E21']=dict(name='밤이의 그날 밤 목격',kind='증언',variants=dict(observed='밤이: 양동이가 넘어졌을 때 처마에 있었다. 맨발로 울타리 쪽에 가는 사람을 봤지만 얼굴과 키는 모른다.'))
# Missing source-state transitions, tied to completion of actual testimony.
PATCH={
 'MS14_D04_S03_L0020':[dict(op='set',field='dolmok.location',value='clinic')],
 'MS14_D04_S04_L0018':[dict(op='acquire',key='E21',variant='observed')],
 'MS14_D05_S01_L0024':[dict(op='set',field='E24.status',value='partial')],
}
for rid,ops in PATCH.items():DATA['records'][rid]['operations']+=ops
bindings=json.loads((ROOT/'game/v111/field-bindings.json').read_text())
lines=['# Reviewed D04–D05 source IDs in existing Ren’Py labels.','']
q=repr
people={
 'MS14_D04_S01':['daram','resident_nero','resident_somi'],
 'MS14_D04_S02':['daram','resident_kongi','resident_tosil','bami'],
 'MS14_D04_S03':['daram','guard','neoul','resident_badook'],
 'MS14_D04_S04':['daram','resident_badook','bami'],
 'MS14_D05_S01':['daram','resident_nero','resident_somi','resident_musoe'],
 'MS14_D05_S02':['daram','resident_nero','resident_somi','resident_musoe'],
 'MS14_D05_S03':['daram','guard','neoul','resident_nero','resident_badook','resident_kongi'],
 'MS14_D05_S04':['daram','resident_lamplighter'],
 'MS14_D05_S05':['daram','resident_somi','resident_musoe','resident_nero','resident_badook']}
def label(key):lines.extend(['','label r13_v111_'+key+':'])
def goto(key):lines.append('    jump r13_v111_'+key)
def code(x):lines.append('    $ '+x)
def travel(loc,key,companions=None):lines.append('    call r13_v111_travel('+q(loc)+','+q(key)+(','+q(companions) if companions is not None else '')+')')
def context(sid,loc,key,cast=None,period=None):
 label(key)
 code('r13_v111_scene('+q(sid)+')')
 if period is not None:code('r13_edit(period='+str(period)+')')
 code('room13["v111"]["people"]=[]');travel(loc,key,[p for p in (cast or people[sid]) if p in ('daram','mom')]);code('r13_v111_arrive('+q(cast or people[sid])+')');code('r13_v111_score()')
def records(sid,first,last):
 # Numeric original IDs, not synthetic evidence-display rows or stage directions.
 for n in range(first,last+1):
  rid=sid+'_L%04d'%n;r=DATA['records'][rid]
  if rid=='MS14_D05_S04_L0006':
   first,rest=r['text'].split('.',1)
   lines.append('    call r13_lines([(None,'+q(first+'.')+',dict(no_lead=True,v111_silence_after=True))],'+q('v111:'+rid+':first')+')')
   lines.append('    $ renpy.music.stop(fadeout=0.0 if renpy.is_skipping() else .15)')
   lines.append('    $ room13["v111"]["music_hold"]=room13["v111"]["scene"]')
   lines.append('    call r13_lines([(None,'+q(rest.strip())+',dict(no_lead=True))],'+q('v111:'+rid+':rest')+')')
  elif r['kind'] in ('dialogue','narration','evidence') and r.get('player_visible',True):lines.append('    call r13_lines(r13_v111_lines(['+q(rid)+']),'+q('v111:'+rid)+')')
  if r['operations']:code('r13_v111_commit('+q(rid)+')')
def wait(key,loc,cast,options,targets):
 label(key);bindings[key]=dict(location=loc,people=cast,options=options)
 lines.append('    call r13_v111_wait('+q(key)+')')
 for i,target in enumerate(targets):
  lines.extend(['    if _return=='+str(i)+':','        jump r13_v111_'+target])
 goto(key)
def obj(title,loc,name):return dict(title=title,location=loc,object=name)
def person(title,loc,name,**kw):return dict(title=title,location=loc,person=name,**kw)
def act(key,loc,cast,option,target):wait(key,loc,cast,[option],[target])
def branch(key,expression,yes,no):label(key);lines.extend(['    if '+expression+':','        jump r13_v111_'+yes]);goto(no)
V=lambda k:'r13_v111_value('+q(k)+')'
s='MS14_D04_S01'
branch('day4',V('silluk_status')+"=='detained_work_waiting_station'",'labor4','somi4')
context(s,'v111_labor','labor4',['daram','resident_siluk','neoul']);records(s,1,7);goto('labor_sheet4')
act('labor_sheet4','v111_labor',['daram','resident_siluk','neoul'],person('작업표를 보여 주십시오.','v111_labor','neoul'),'labor_confirm4')
label('labor_confirm4');records(s,8,15);goto('somi4')
context(s,'ms14_somi','somi4');branch('nero_route4',V('nero_met_day2'),'nero_known4','nero_new4')
# context falls through to route label.
label('nero_known4');records(s,17,19);goto('portrait_show4')
label('nero_new4');records(s,20,22);goto('nero_help4')
act('nero_help4','ms14_somi',['daram','resident_nero'],obj('침구와 물통을 돕는다','ms14_somi','v111_bedding'),'nero_help_done4')
label('nero_help_done4');records(s,23,33);goto('portrait_show4')
act('portrait_show4','ms14_somi',people[s],person('이분을 보셨습니까?','ms14_somi','resident_nero',present='V111:E09'),'somi_talk4')
label('somi_talk4');records(s,34,61);goto('eaves4')
s='MS14_D04_S02';context(s,'square','eaves4');records(s,1,15);goto('portrait_place4')
act('portrait_place4','square',people[s],person('여기 두고 물러날게.','square','bami',present='V111:E09'),'bami_mother4')
label('bami_mother4');records(s,16,28);travel('ms14_somi','visit_return4');records(s,29,31);goto('cry4')
s='MS14_D04_S03';context(s,'gate','cry4',period=2);records(s,1,2);goto('look_gate4')
act('look_gate4','gate',people[s],obj('밝은 쪽에서 살핀다','gate','road'),'bite4')
label('bite4');records(s,3,26);goto('testimony4')
s='MS14_D04_S04';context(s,'ms14_guardroom','testimony4');records(s,1,7);goto('bami_ask4')
act('bami_ask4','ms14_guardroom',people[s],person('어디서 봤니?','ms14_guardroom','bami'),'bami_night4')
label('bami_night4');records(s,8,33);travel('gate','fence4');goto('inspect_gate4')
wait('inspect_gate4','gate',['daram'],[obj('울타리 천','gate','v111_fence'),obj('겹친 발자국','gate','road'),obj('엎어진 양동이','gate','v111_bucket')],['fence_seen4','tracks_seen4','bucket_seen4'])
for key,flag in [('fence','d4_fence_seen'),('tracks','d4_tracks_seen'),('bucket','d4_bucket_seen')]:
 label(key+'_seen4');code('r13_v111_set('+q(flag)+',True)');goto('inspection_ready4')
branch('inspection_ready4','all(r13_v111_value(k) for k in '+q(['d4_fence_seen','d4_tracks_seen','d4_bucket_seen'])+')','tracks_talk4','inspect_gate4')
label('tracks_talk4');records(s,34,40);goto('collect4')
act('collect4','gate',['daram','resident_badook','bami'],person('같이 천을 수거해 주십시오.','gate','resident_badook'),'cloth4')
label('cloth4');records(s,41,50);travel('dining','night_diner4');records(s,51,59);travel('square','night_lamp4');records(s,60,64);travel('room13','bed4');records(s,65,65);goto('sleep4')
act('sleep4','room13',['daram'],obj('관찰과 추측을 나눠 적고 잔다','room13','bed'),'morning5')
s='MS14_D05_S01';label('morning5');code('r13_v111_set("day",5)');goto('somi5')
context(s,'ms14_somi','somi5');records(s,1,7);travel('ms14_somi_inside','inside5');records(s,8,24);code('r13_nw_acquire("NW_MUSOE_DEEP")');goto('wait_cloth5')
s='MS14_D05_S02';context(s,'ms14_somi_inside','wait_cloth5');records(s,1,15);goto('compare_cloth5')
act('compare_cloth5','ms14_somi_inside',people[s],obj('허락받은 옷과 천을 대조한다','ms14_somi_inside','v111_coat'),'cloth_match5')
label('cloth_match5');records(s,16,28);travel('clinic','clinic_handoff5');records(s,29,31);goto('hearing5')
s='MS14_D05_S03';context(s,'gate','hearing5');records(s,1,9);goto('proof5')
label('proof5');lines.append('    call r13_v111_proof("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],"r13_v111_bami_clear5","r13_v111_wrong5","r13_v111_hint5")');lines.append('    jump expression _return')
# New world (event 04): one presentation. A half presentation (part of the right set)
# gets one more try; any other wrong answer is final and Bami goes on the list.
label('wrong5')
lines.extend(['    if r13_nw_half(["E20","E22","E23","E24"]) and not r13_v111_value("gate_post_hardened"):',
 '        $ r13_v111_set("gate_post_hardened",True)',
 '        call r13_lines(r13_v111_lines(["MS14_D05_S03_L0038","MS14_D05_S03_L0039"]),"v111:MS14_D05_S03_L0038")',
 '        jump r13_v111_proof5'])
code('r13_nw_meeting_end("gate_post","lose")');code('r13_nw_list("bami","gate_post_lose")');code('r13_v111_set("bami_status","listed")')
records(s,38,39);goto('warning5')
label('hint5');records(s,40,40);goto('proof5')
label('bami_clear5');code('r13_nw_meeting_end("gate_post","win")');records(s,12,37);goto('warning5')
s='MS14_D05_S04';context(s,'gate','warning5');records(s,1,4);goto('envelope5')
act('envelope5','gate',people[s],person('봉투를 받겠습니다.','gate','resident_lamplighter'),'warning_read5')
label('warning_read5');records(s,5,13);goto('warning_compare5')
label('warning_compare5');lines.append('    call r13_v111_proof("두 편지의 초대를 대조한다",["E01","E27"],"r13_v111_warning_compared5")');lines.append('    jump expression _return')
label('warning_compared5');records(s,14,15)
lines.extend(['    menu:','        "첫날 기록을 다시 본다":','            call r13_v111_review5','        "답장을 쓴다":','            pass']);records(s,18,30);goto('reply_handoff5')
act('reply_handoff5','gate',people[s],person('답장을 맡기겠습니다.','gate','resident_lamplighter',present='V111:E28'),'reply_done5')
label('reply_done5');records(s,9501,9503);goto('night5')
label('review5');records(s,17,17);lines.append('    return')
s='MS14_D05_S05';context(s,'ms14_somi_inside','night5',period=2);records(s,1,16);travel('dining','diner5');records(s,17,26);records(s,9501,9502);travel('inn','lobby5');records(s,27,32);travel('hall','hall5');records(s,33,37);travel('room13','lock5');goto('lock_check5')
act('lock_check5','room13',['daram'],obj('문과 창문 잠금을 확인한다','room13','window'),'safety5')
label('safety5');records(s,38,43);branch('blankets5',V('carried_dry_blankets')+'==2','packed5','empty_bag5')
label('packed5');records(s,45,48);goto('last5')
label('empty_bag5');records(s,49,52);goto('last5')
label('last5');records(s,53,64);goto('sleep5')
act('sleep5','room13',['daram'],obj('아침 일정을 정하고 잔다','room13','bed'),'morning6')
label('morning6');code('r13_v111_set("day",6)');goto('day6')
(ROOT/'game/room13_v111_days45.rpy').write_text('\n'.join(lines)+'\n')
(ROOT/'game/v111/records.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
(ROOT/'game/v111/field-bindings.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
