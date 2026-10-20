import json,pathlib
R=pathlib.Path(__file__).resolve().parents[1];N=json.loads((R/'docs/story-v111/compiled-reference.json').read_text());D=json.loads((R/'game/v111/records.json').read_text());bindings={}
option_sources={'letter_menu':'MS14_D01_S01_L0014','gate_choice':'MS14_D01_S02_L0022','gate_investigate':'MS14_D01_S03_L0008','registered_menu':'MS14_D01_S04_L0012','post_menu':'MS14_D02_S02_L0015','afternoon':'MS14_D02_S04_L0020','stone_choice':'MS14_D03_S05_L0048','custody_choice':'MS14_D03_S05_L0056'}
for option_node,source_rid in option_sources.items():
 for i,option in enumerate(N[option_node]['options']):
  source_index=i-3 if option_node=='gate_investigate' else i
  if source_index>=0:option['title']=D['records'][source_rid]['options'][source_index]['label']
# Each binding points at an existing field object, speaker, map destination, or
# existing record presentation. Actual story decisions remain native menus.
field={
'gate_request':('gate',['guard','daram'],'ledger'),
'gate_investigate':('gate',['guard','daram'],'mixed'),
'gate_choice':('gate',['guard','daram'],'guard'),
'registered_menu':('gate',['guard','daram','karo'],'mixed'),
'room_observe':('room13',['daram'],'bed'), 'note_pick':('room13',['daram'],'mother_note'), 'bundle_open':('room13',['daram'],'family_bundle'),
'sleep1':('room13',['daram'],'bed'), 'sleep2':('room13',['daram'],'bed'),'sleep3':('room13',['daram'],'bed'),
'lamp_rope':('square',['resident_lamplighter','daram'],'lamp'),
'go_box':('square',['resident_lamplighter','daram'],'move:forest'),
'box_inspect':('forest',['resident_lamplighter','daram'],'v111_box'), 'box_note':('forest',['resident_lamplighter','daram'],'v111_box'),
'envelope_show':('post',['seryeon','daram'],'seryeon'), 'post_menu':('post',['seryeon','daram'],'seryeon'),
'portrait_ask':('square',['resident_piko','daram'],'resident_piko'), 'lamp_observe':('square',['resident_piko','daram'],'lamp'),
'shelter_work':('dining',['nabi','daram'],'table'),'shelter_enter':('square',['resident_piko','daram'],'move:dining'),
'nero_work':('forest',['resident_nero','daram'],'resident_nero'),
'piko_clean':('dining',['resident_piko','nabi','daram'],'table'),
'lamp_inspect3':('square',['resident_tok','neoul','resident_lamplighter','daram'],'lamp'),
'fragment_request':('square',['resident_tok','resident_lamplighter','daram'],'resident_tok'),
'lamp_log_request':('square',['resident_lamplighter','daram'],'resident_lamplighter'),
'loan_read':('workshop',['buri','daram'],'tools'), 'measurement_read':('clinic',['resident_ubak','daram'],'notes'),
'transport_read':('square',['resident_siluk','daram'],'resident_siluk'), 'knife_permission':('square',['resident_siluk','daram'],'resident_siluk'),
'store_visit':('square',['resident_siluk','daram'],'move:store'), 'stone_check':('store',['resident_madam','resident_tok','daram'],'resident_tok'),
'sale_check':('store',['resident_madam','daram'],'ledger'), 'restore_input':('square',['resident_tok','resident_lamplighter','daram'],'lamp'),
'blankets_receive':('square',['resident_nero','daram'],'resident_nero')}
for key,(loc,people,kind) in field.items():
 opts=[]
 for i,o in enumerate(N[key]['options']):
  row=dict(title=o['title'],location=loc,guard=o.get('guard',[]))
  if kind=='mixed':
   if key=='gate_investigate':
    if i<3:row['object']=['gate_documents','rules','ledger'][i]
    else:row['person']='guard'
   else:
    if i==0:row['person']='guard'
    else:row.update(location='inn',move='inn')
  elif kind.startswith('move:'):row.update(location=kind[5:],move=kind[5:])
  elif kind in people:row['person']=kind
  else:row['object']=kind
  if key=='envelope_show':row['present']='V111:E01'
  if key=='gate_choice' and i==0:row['present']='V111:E01'
  opts.append(row)
 bindings[key]=dict(location=loc,people=people,options=opts)
bindings['shelter_cloth']=dict(location='inn',people=['granny','daram'],options=[dict(title='마른 천을 빌린다',location='inn',person='granny')])
bindings['shelter_invite']=dict(location='square',people=['resident_piko','daram'],options=[dict(title='비운 벤치와 조건을 전한다',location='square',person='resident_piko')])
(R/'game/v111/field-bindings.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
loc={
'start':'gate','letter_read':'gate','gate_arrival':'gate','registered':'gate','inn':'inn','room_empty':'room13','room_note':'room13','bundle':'room13','room_compare':'room13',
'day2':'gate','square2':'square','chorong':'square','box_path':'forest','box_empty':'forest','box_written':'forest','post':'post','post_checked':'post','piko2':'square','portrait_commission':'square','lamp_details':'square','diner_offer':'dining','shelter_choice':'dining','shelter_prepare':'square','shelter_done':'dining','nero_choice':'dining','nero_done':'forest','evening2':'inn','evening2_end':'room13',
'piko_alive3':'dining','piko_receive':'dining','piko_dead3':'square','lamp3':'square','lamp_interior3':'square','lamp_fragment3':'square','lamp_log3':'square','workshop3':'workshop','loan3':'workshop','clinic3':'clinic','measurement3':'clinic','silluk3':'square','transport3':'square','knife_observed':'square','store3':'store','stone3':'store','sale3':'store','trial_open':'workshop','restore3':'square','restore_defer':'square','box_news3':'square','piko_evening':'clinic','piko_memorial':'square','somi_lead':'square','blankets3':'square','stairs3':'room13'}
# Authored in-record location changes, not background-array slideshows.
move={'MS14_D01_S05_L0036':'inn','MS14_D01_S05_L0039':'room13','MS14_D02_S04_L0042':'square','MS14_D02_S04_L0049':'forest','MS14_D02_S04_L0076':'square','MS14_D02_S04_L0079':'inn','MS14_D02_S04_L0083':'room13','MS14_D02_S05_L0006':'room13','MS14_D03_S04_L0026':'workshop','MS14_D03_S04_L0028':'store','MS14_D03_S04_L0034':'workshop'}
q=lambda x:repr(x)
lines=['# Native Room13 story labels. Generated from reviewed source IDs; no runtime route interpreter.','label r13_v111_start:','    $ room13["v111"]=dict(version="1.1.1",values=winter_copy.deepcopy(R13_V111["initial"]),gate="",people=["daram"])','    $ ms14=None; r13_flag("lodging"); r13_carriage_skip=False','    call r13_carriage_departure','    jump r13_v111_start_block']
def dest(k):return 'r13_v111_'+('start_block' if k=='start' else k)
def travel(place,key):
 return ['    call r13_v111_travel('+q(place)+','+q(key)+')']
def optext(ops):return repr(ops)
for key,node in N.items():
 lines+=['', 'label '+dest(key)+':']
 kind=node['kind']
 if kind=='block':
  phase={'room_compare':2,'diner_offer':1,'evening2':2,'evening2_end':2,'piko_alive3':0,'piko_dead3':0,'trial_open':1,'restore3':2,'restore_defer':2,'box_news3':2,'piko_evening':2,'piko_memorial':2,'stairs3':2}.get(key)
  if phase is not None:lines+=['    $ r13_edit(period='+str(phase)+')']
  lines+=['    $ r13_v111_scene('+q(node['scene'])+')']
  if key in loc and key!='start':lines+=travel(loc[key],key)
  lines+=['    $ r13_v111_score()']
  if key=='gate_arrival':lines+=['    $ r13_carriage_finish(); r13_carriage_skip=False', '    call r13_scene("winter","눈에 막힌 입구","calm")']
  # Dialogue groups retain existing skip/auto behavior; effect boundaries stay explicit.
  pending=[]
  def flush():
   if pending:
    lines.append('    call r13_lines([r13_v111_line(x) for x in '+repr(list(pending))+'], '+q('v111:'+key+':'+pending[0])+')');pending.clear()
  for rid in node['records']:
   r=D['records'][rid]
   if rid in move:flush();lines+=travel(move[rid],rid)
   if r['kind'] in ('dialogue','narration','choice','evidence') and r.get('player_visible',True):pending.append(rid)
   if r['operations']:
    flush();lines+=['    $ r13_v111_commit('+q(rid)+')']
  flush()
  lines+=['    jump '+dest(node['next'])]
 elif kind=='branch':
  lines+=['    if r13_v111_value('+q(node['field'])+')=='+repr(node['value'])+':','        jump '+dest(node['yes']),'    jump '+dest(node['no'])]
 elif kind=='mark':
  lines+=['    $ r13_v111_apply('+q(key)+','+optext(node['operations'])+')','    jump '+dest(node['next'])]
 elif kind=='proof':
  lines+=['    call r13_v111_proof('+q(node['title'])+','+q(node['correct'])+','+q(dest(node['to']))+','+q(dest(node['wrong']) if node.get('wrong') else None)+','+q(dest(node['hint']) if node.get('hint') else None)+')','    jump expression _return']
 elif kind=='notebook':lines+=['    call screen r13_book','    jump '+dest(node['next'])]
 elif kind=='read':lines+=['    show screen r13_material_corner('+q('V111:'+node['key'])+')','    call screen r13_confirm("기록을 다시 확인했다.",yes="닫는다")','    hide screen r13_material_corner','    jump '+dest(node['next'])]
 elif kind=='choice':
  if key=='lamp_observe':
   lines+=['    if all(r13_v111_value("lamp_part_%d"%i) for i in range(4)):','        jump '+dest('lamp_details')]
  if key in field:
   # Slot completion is triggered by field/talk/map input, not a one-option menu.
   if key not in ('shelter_enter','registered_menu','go_box','store_visit'):lines+=travel(field[key][0],key)
   lines+=['    call r13_v111_wait('+q(key)+')','    $ v111_answer=_return']
  elif key in ('letter_open','leave_carriage'):
   lines+=['    call screen r13_confirm('+q(node['title'])+',yes='+q(node['title'])+')','    if not _return:','        jump '+dest(key),'    $ v111_answer=0']
  else:
   opts=[]
   for i,o in enumerate(node['options']):
    cond=' and '.join(('r13_v111_owned(%r)'%k if t=='evidence' and val else 'not r13_v111_owned(%r)'%k if t=='evidence' else 'r13_v111_value(%r)==%r'%(k,val)) for t,k,val in o['guard']) or 'True'
    opts.append('('+repr(o['title'])+','+str(i)+') for _ in [0] if '+cond)
   lines+=['    $ v111_menu_owner='+q(key)]
   lines+=['    $ v111_menu='+(' + '.join('['+x+']' for x in opts)),'    $ v111_answer=renpy.display_menu(v111_menu)']
  if key=='shelter_work':
   lines+=['    call r13_v111_travel("inn","shelter_cloth")','    call r13_v111_wait("shelter_cloth")','    call r13_v111_travel("square","shelter_invite")','    call r13_v111_wait("shelter_invite")']
  if key=='nero_work':
   for work in ('젖은 빈 포대를 분리한다','마른 받침으로 침구를 옮긴다','끈을 묶고 운반표에 이름을 적는다'):
    lines+=['    call screen r13_confirm('+q(work)+',yes='+q(work)+')','    if not _return:','        jump '+dest(key)]
  for i,o in enumerate(node['options']):
   lines+=['    if v111_answer=='+str(i)+':']
   source_index=i-3 if key=='gate_investigate' else i
   if key in option_sources and source_index>=0:
    lines+=['        $ r13_v111_option('+q(option_sources[key]+'_O'+str(source_index+1))+')']
   if o.get('operations'):lines+=['        $ r13_v111_apply('+q('option:'+key+':'+str(i))+','+optext(o['operations'])+')']
   lines+=['        jump '+dest(o['to'])]
  lines+=['    jump '+dest(key)]
lines+=['','label r13_v111_day4:','    $ r13_v111_context("checkpoint")','    call screen r13_confirm("이번 공개분은 3일차까지입니다. 현재 진행을 저장해 둘 수 있습니다.",yes="메인 화면으로",no="저장하기")','    if not _return:','        call screen save','        jump r13_v111_day4','    return']
(R/'game/room13_v111_days123.rpy').write_text('\n'.join(lines)+'\n')
