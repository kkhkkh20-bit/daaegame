"""Reviewed D06–D10 native Ren'Py control flow, not a runtime interpreter."""
from build_v111_days45 import *
lines.clear();lines.append('# Reviewed D06–D10 source IDs and explicit field/proof callbacks.')
for sid,s in SCENES.items():
 if not 6<=s['source_scene']['day']<=10:continue
 DATA['scene_days'][sid]=s['source_scene']['day'];DATA['audio'][sid]=s['audio']['file']
 for b in s['blocks']:
  for c in b['cues']:
   r=copy.deepcopy(c['source_record']);ops=[]
   for effect in r.get('effects',[]):
    if '=' not in effect:raise ValueError((r['id'],effect))
    k,v=effect.split('=',1);ops.append(dict(op='set',field=k,value=scalar(v)))
   r.update(operations=ops,direction=c['directed_expression']);DATA['records'][r['id']]=r
DATA['initial'].update(KKOMI_ALIVE=True,OWL_ALIVE=True,TOK_ALIVE=True,grandmother_custody='free',tok_workshop_present=True,tok_hearing_present=True,DARAM_DETAINED=False,route7='uncommitted',prevention=None)
# Exact observation descriptions come from authored source, not internal state codes.
OBS={
 'E06_CONTACT':('학교 뒤 공개 물자 수량','MS14_D06_S01_L0043'),
 'E06_FIRE':('등잔·천·발화 지점','MS14_D06_S04_L0036'),
 'E08_CHILD_ACCOUNT':('다람의 진술과 손목 기록','MS14_D08_S01_L0025'),
 'E08_ROOM':('13호 현장과 도토의 관찰','MS14_D08_S02_L0043'),
 'E08_CHILD_POSITION':('도토가 확인한 다람의 두 손','MS14_D08_S02_L0033'),
 'E08_ROOM_REACH':('문틈과 책상 사이 거리','MS14_D08_S02_L0034'),
 'E08_TOOL':('촛대 파손·상처 대조 자료','MS14_D08_S03_L0007'),
 'E08_CONTACT_ASSEMBLY':('접힌 천·닫힌 핀·고리','MS14_D08_S03_L0036'),
 'E08_WOUND_WIRE':('상처 가장자리의 구리 파편','MS14_D08_S03_L0034'),
 'E08_RECENT_LETTER':('6일에 쓴 엄마의 편지','MS14_D08_S04_L0032'),
 'E09_PASSAGE':('직접 왕복한 통로','MS14_D09_S01_L0013'),
 'E09_PIN_OWNER':('핀 수선과 인수 기록','MS14_D09_S02_L0025'),
 'E09_PIN_TIME':('첫 비명 뒤 핀을 다시 채운 때','MS14_D09_S03_L0031'),
 'E09_PIN_HANDOVER_TIME':('양손 확인 뒤 계단참의 핀','MS14_D09_S03_L0032'),
 'E09_SCARF':('목도리 찢어진 끝','MS14_D09_S03_L0050'),
 'E09_MAIL':('발송·필사본·반송의 출처','MS14_D09_S04_L0015'),
 'E10_PUMP':('6일에 마지막 쓴 연락함','MS14_D10_S04_L0012'),
}
OBS_TEXT={
 'E08_CHILD_ACCOUNT':'다람은 붙잡힌 손목을 놓아 달라고 했다가 촛대로 손을 쳤다고 말했다. 서리가 손목의 멍을 기록했다.',
 'E08_TOOL':'서리는 손목과 머리의 상처 모양이 다르며 머리 상처가 부러진 윗조각의 면과 맞는다고 말했다. 손잡이 아래조각과 윗조각은 분리돼 있고, 윗조각의 장식 고리에는 접힌 천과 닫힌 핀이 남아 있다.',
 'E08_ROOM_REACH':'도토가 다람의 손을 잡고 위치를 확인한 문틈에서 책상 옆 발견 자리까지는 그 자세로 손이 닿지 않는다.',
 'E06_CONTACT':'학교 뒤 공개 보급판: 오늘 수건 두 장과 소금 한 꾸러미 인수 표시. 수령인과 거처는 적혀 있지 않다.',
 'E06_FIRE':'등잔은 뒷벽 물통 옆에서 뚜껑이 닫힌 채 기름이 남아 있었다. 문 쪽 탄 자국과 기름 냄새가 나는 천은 따로 확인해 보관했다.',
 'E08_CHILD_POSITION':'도토는 문틈에서 왼손을 잡고 오른손의 아랫조각도 보았다고 말했다. 뒤 충격음이 났을 때부터 문이 열릴 때까지 두 손과 위치를 계속 확인했다.',
 'E09_PASSAGE':'쐐기·안전줄·바깥 문지기를 확인하고 통로를 왕복했다. 주방에서 문을 여닫고 13호 뒤로 연결된다. 안쪽 손잡이는 없다.',
 'E09_PIN_OWNER':'공방 수선장과 인수 등본: 핀 뒤의 구리 수리 끝과 수령인을 확인했다. 현재 증인의 출석과는 별개인 보관 기록이다.',
 'E09_PIN_HANDOVER_TIME':'나비: 도토가 다람의 손을 잡고 있었을 때도 다시 채운 핀이 계단참의 할머니 목도리에 있었다. 주방 이동은 그 뒤였다.',
}
for key,(name,rid) in OBS.items():
 DATA['evidence'][key]=dict(name=name,kind='기록',variants=dict(observed=OBS_TEXT.get(key,DATA['records'][rid]['text'])))
# Evidence is granted only by a record's actual semantic completion marker.
for r in DATA['records'].values():
 if not re.match('MS14_D(06|07|08|09|10)_',r['id']):continue
 for op in list(r['operations']):
  if op.get('field') in OBS:r['operations'].append(dict(op='acquire',key=op['field'],variant='observed'))
# Distinct observed events are never disguised as the same rescue witness.
DATA['evidence']['E06_EMPTY']=dict(name='빈 창고 진압과 네 아이 인수',kind='관찰기록',variants=dict(observed='네 아이를 학교에 실제로 인계했다. 아이들이 없는 창고에서 보리가 불의 확산을 막으려 한 것을 아빠가 보았다. 아이 구조 목격은 아니다.'))
DATA['evidence']['E06_RESCUE']=dict(name='보리의 세 아이 구조 목격',kind='관찰기록',variants=dict(observed='보리가 아이 하나를 안고 나왔고 두 아이가 뒤따라 나왔다. 아빠가 직접 보았다. 꼬미는 구조하지 못했다.'))
DATA['evidence']['E07_NUBI']=dict(name='누비의 직접 진술',kind='증언',variants=dict(observed='누비는 스스로 불을 놓았다고 말했다. 이 진술만으로 너울의 약속이나 살인 의도까지 입증한 것은 아니다.'))
for rid,key in [('MS14_D06_S04_L0027','E06_RESCUE'),('MS14_D06_S04_L0030','E06_EMPTY'),('MS14_D07_S01_L0045','E07_NUBI')]:
 DATA['records'][rid]['operations'].append(dict(op='acquire',key=key,variant='observed'))

# A repair copy is available from either workshop attendance path; live testimony
# still requires Tok alive and actually present at the hearing (MID-05).
for rid in ('MS14_D09_S02_L0018','MS14_D09_S02_L0026'):
 DATA['records'][rid]['operations'].append(dict(op='set',field='tok_repair_copy_owned',value=True))
# Only actual crossing of the custody-room threshold changes location (MID-08).
DATA['records']['MS14_D10_S03_L0088']['operations'].append(dict(op='set',field='DARAM_location',value='school'))
# Existing numeric IDs may have intentional gaps; never invent records.
def segment(sid,first,last):
 for n in range(first,last+1):
  if sid+'_L%04d'%n in DATA['records']:records(sid,n,n)
def begin(sid,loc,key,cast,period=0):context(sid,loc,key,cast,period)
def finish_day(key,day,target):
 label(key);travel('school',key);goto(key+'_input')
 act(key+'_input','school',['daram'],obj('잠자리를 정리한다','school','blankets'),key+'_done')
 bindings[key+'_input']['daram_if_free']=True
 label(key+'_done');code('r13_v111_set("day",'+str(day)+')');goto(target)
def field(key,loc,cast,object_name,title,target):act(key,loc,cast,obj(title,loc,object_name),target)
def talk(key,loc,cast,person_id,title,target):act(key,loc,cast,person(title,loc,person_id),target)
def proof(key,title,evidence,target,wrong=None,hint=None):
 label(key);lines.append('    call r13_v111_proof('+','.join(map(q,[title,evidence,'r13_v111_'+target,('r13_v111_'+wrong) if wrong else None,('r13_v111_'+hint) if hint else None]))+')');lines.append('    jump expression _return')
def choice(sid,rid,after):
 r=DATA['records'][sid+'_L%04d'%rid];lines.append('    menu:')
 for i,o in enumerate(r['options']):
  title=SHORT.get(o['id'],o['label']);lines.append('        '+q(title)+':')
  for fx in o['effects']:
   k,v=fx.split('=',1)
   if k=='scene_local.choice':k='choice:'+sid
   lines.append('            $ r13_v111_set('+q(k)+','+q(scalar(v))+')')
  tail=DATA['records'].get(sid+'_L%04d'%(rid+1),{})
  if tail.get('kind')=='system' and tail.get('operations'):lines.append('            $ r13_v111_commit('+q(tail['id'])+')')
  lines.append('            jump r13_v111_'+after[i])
SHORT={
 'MS14_D07_S03_B002_O01':'다람과 남고 까로에게 부탁한다',
 'MS14_D07_S03_B002_O02':'다람과 의료진을 데려온다',
 'MS14_D07_S03_B002_O03':'도토에게 인계하고 의료진을 부른다',
 'MS14_D06_S01_B004_O02':'먼저 먹어. 그릇은 가져다줄게.',
}
C=lambda sid:V('choice:'+sid)
s='MS14_D06_S01';cast=['daram','resident_teacher','resident_lamplighter','kid_kkomi']
begin(s,'school','day6',cast);segment(s,1,12)
lines.append('    call r13_lines([("resident_teacher","낮 동안은 이쪽에 앉아 있어도 됩니다. 먹을 건 따로 챙겨 주세요.",{"no_lead":True})],"v111:school_day_permission")')
lines.append('    if '+V('carried_dry_blankets')+'==2:');lines.append('        call r13_v111_blankets6')
segment(s,17,23);choice(s,24,['bowl_together6','bowl_eat6'])
label('blankets6');segment(s,13,16);lines.append('    return')
for key,a,b in [('bowl_together6',26,29),('bowl_eat6',30,33)]:label(key);segment(s,a,b);goto('nabi_supply6')
label('nabi_supply6');segment(s,34,42);travel('dining','supply6');goto('board6')
field('board6','dining',['daram','nabi'],'table','공개 보급판을 확인한다','board_done6')
label('board_done6');segment(s,43,48);goto('woodshed6')
s='MS14_D06_S02';cast=['daram','kid_kkomi','resident_bori'];begin(s,'v111_woodshed','woodshed6',cast,1);segment(s,1,2);code('r13_nw_acquire("NW_KKOMI_NOSTONE")');segment(s,3,4);goto('woodshed_check6')
field('woodshed_check6','v111_woodshed',cast,'v111_wood','문 앞과 뒤창을 살핀다','woodshed_seen6')
label('woodshed_seen6');segment(s,5,24);choice(s,25,['today6','permission6'])
label('today6');segment(s,27,29);goto('permission_today6')
label('permission6');segment(s,30,33);goto('fire6')
s='MS14_D06_P01';begin(s,'school','permission_today6',['daram','resident_teacher','doto','kid_kkomi'],1);segment(s,1,8);travel('v111_woodshed','children_fetch6');goto('acorn_recover6')
talk('acorn_recover6','v111_woodshed',['daram','kid_kkomi','doto'],'kid_kkomi','깡통의 도토리도 챙겨 줄래?','acorn_recovered6')
label('acorn_recovered6');lines.append('    call r13_lines([(None,"꼬미가 깡통에서 도토리를 꺼내 손에 쥐었다.")],"v111:acorn_recovered")');code('r13_v111_set("acorn_recovered",True)');segment(s,9,18);travel('school','children_handoff6');goto('handoff6')
field('handoff6','school',['daram','resident_teacher','doto','kid_kkomi'],'blankets','네 아이와 물자를 확인한다','handoff_done6')
label('handoff_done6');segment(s,19,24);goto('empty_fire6')
s='MS14_D06_S03P';begin(s,'v111_fire','empty_fire6',['resident_bori','doto'],2);segment(s,1,8);goto('after_fire6')
s='MS14_D06_S03';begin(s,'v111_fire','fire6',['daram','resident_bori'],2);segment(s,1,8);travel('school','children_safe6');segment(s,9,10);travel('v111_fire','rescue6');goto('wet_cloth6')
field('wet_cloth6','v111_fire',['resident_bori'],'v111_water','물에 적신 천을 건넨다','wet_done6')
label('wet_done6');goto('clear_wood6')
field('clear_wood6','v111_fire',['resident_bori'],'v111_wood','옆문 장작을 치운다','rescue_done6')
label('rescue_done6');segment(s,11,22);goto('after_fire6')
s='MS14_D06_S04';begin(s,'school','after_fire6',['daram','nabi','resident_bori','neoul','doto'],2);segment(s,1,10)
lines.append('    if '+V('FIRE_EVACUATED')+':');lines.append('        call r13_v111_bori_unhurt6');lines.append('    else:');lines.append('        call r13_v111_bori_burned6');segment(s,19,24)
lines.append('    if '+V('FIRE_EVACUATED')+':');lines.append('        call r13_v111_empty_testimony6');lines.append('    else:');lines.append('        call r13_v111_rescue_testimony6');segment(s,31,33);travel('v111_ruin','cold_fire6');goto('fire_evidence6')
for key,a,b in [('bori_unhurt6',15,18),('bori_burned6',11,14),('empty_testimony6',28,30),('rescue_testimony6',25,27)]:label(key);segment(s,a,b);lines.append('    return')
field('fire_evidence6','v111_ruin',['doto'],'v111_lamp','등잔과 천을 따로 확인한다','fire_record6')
label('fire_record6');segment(s,34,37);travel('school','return_school6');branch('bowl_result6',V('KKOMI_ALIVE'),'four_bowls6','empty_bowl6')
for key,a,b in [('four_bowls6',44,49),('empty_bowl6',38,43)]:label(key);segment(s,a,b);goto('sleep6')
finish_day('sleep6',7,'day7')
s='MS14_D07_S01';cast=['resident_nubi','resident_bori','nabi'];begin(s,'laundry','day7',cast);segment(s,1,17);choice(s,18,['children_school7','children_here7'])
for key in ('children_school7','children_here7'):
 label(key)
 if key=='children_here7':segment(s,25,29)
 segment(s,20,22);goto('nubi_children_school7')
label('nubi_children_school7');travel('school','nubi_children_school7',[]);code('r13_v111_arrive(["nabi","resident_teacher","kid_nubi1","kid_nubi2","kid_nubi3"])');goto('nubi_children_receipt7')
talk('nubi_children_receipt7','school',['nabi','resident_teacher','kid_nubi1','kid_nubi2','kid_nubi3'],'resident_teacher','누비 씨의 아이 셋 인수를 확인한다','nubi_children_received7')
label('nubi_children_received7');segment(s,24,24);travel('laundry','nubi_children_received7',[]);code('r13_v111_arrive(["resident_nubi","resident_bori"])');goto('bori_witness7')
talk('bori_witness7','laundry',['resident_nubi','resident_bori'],'resident_bori','창고 문 앞에서 무엇을 보셨습니까?','bori_witness_heard7')
label('bori_witness_heard7');lines.append('    call r13_lines([("resident_bori","불이 번지기 전에 누비 씨가 창고 문 앞에 서 있는 건 봤소.",{"no_lead":True})],"v111:bori_fire_door_witness")');code('r13_v111_set("bori_nubi_door_witness_heard",True)');goto('nubi_proof7')
proof('nubi_proof7','불이 시작된 곳과 진술을 대조한다',['E06_FIRE'],'nubi_admission7','nubi_wrong7')
# New world (event 05): one presentation. Losing Nubi's fire (gate) makes Bori the arsonist.
label('nubi_wrong7');lines.extend(['    if r13_nw_retry("fire"):','        call r13_lines(r13_v111_lines(["MS14_D07_S01_L0046","MS14_D07_S01_L0047"]),"v111:nubi_wrong7:retry")','        jump r13_v111_nubi_proof7']);code('r13_nw_meeting_end("fire","lose")');code('r13_nw_list("resident_bori","fire_lose")');segment(s,46,47);goto('responsibility7')
label('nubi_admission7');lines.append('    if not r13_v111_value("bori_nubi_door_witness_heard"):');lines.append('        jump r13_v111_bori_witness7');segment(s,30,45);goto('responsibility7')
s='MS14_D07_S02';begin(s,'school','responsibility7',['nabi','resident_bori','resident_nubi','neoul']);segment(s,1,2)
lines.extend(['    if r13_v111_value("meeting:fire")=="lose":','        jump r13_v111_responsibility_answers7'])
branch('fire_basis_route7',V('FIRE_EVACUATED'),'empty_fire_basis7','rescue_fire_basis7')
proof('empty_fire_basis7','불의 원인과 빈 창고 진압을 구분한다',['E06_FIRE','E06_EMPTY','E07_NUBI'],'responsibility_answers7','responsibility_wrong7')
proof('rescue_fire_basis7','불의 원인과 아이 구조를 구분한다',['E06_FIRE','E06_RESCUE','E07_NUBI'],'responsibility_answers7','responsibility_wrong7')
# Weighing the three faults (non-gate): a half presentation gets one more try; otherwise
# '셋 다 책임' stands, Bori is listed for hiding, and Neoul's promise is not recorded.
label('responsibility_wrong7')
lines.extend(['    if r13_nw_retry("fire",["E06_FIRE","E06_EMPTY","E07_NUBI"] if r13_v111_value("FIRE_EVACUATED") else ["E06_FIRE","E06_RESCUE","E07_NUBI"],"너울이 고개를 젓는다. 불의 원인과 그날 밤 일을 함께 묶어야 한다."):',
 '        jump r13_v111_fire_basis_route7'])
code('r13_nw_meeting_end("fire","partial")');code('r13_nw_list("resident_bori","fire_partial")');goto('responsibility_answers7')
label('responsibility_answers7');code('r13_nw_meeting_end("fire","win")');lines.extend(['    if r13_v111_value("meeting:fire")=="win":','        $ r13_v111_set("fire_neoul_promise_recorded",True)']);segment(s,4,14);goto('school_names7')
field('school_names7','school',['nabi','resident_teacher'],'desks','명부와 실제 침구를 확인한다','school_names_done7')
label('school_names_done7');segment(s,15,29)
lines.append('    if '+V('KKOMI_ALIVE')+':');lines.append('        call r13_v111_living_child7');lines.append('    else:');lines.append('        call r13_v111_lost_child7');segment(s,38,46);goto('room_visit7')
label('living_child7');segment(s,34,37);segment(s,49,52);lines.append('    return')
label('lost_child7');segment(s,30,33);lines.append('    return')
s='MS14_D07_S03';begin(s,'room13','room_visit7',['daram','granny','resident_owlgp','doto','karo'],2);segment(s,1,14);choice(s,15,['stay7','take7','handover7'])
for key,a,b,target in [('stay7',17,19,'prevent_a7'),('take7',20,22,'prevent_b7'),('handover7',23,31,'incident7')]:label(key);segment(s,a,b);goto(target)
s='MS14_D07_P01';begin(s,'room13','prevent_a7',['daram','doto','resident_owlgp','karo'],2);segment(s,1,14);goto('sleep7')
s='MS14_D07_P02';begin(s,'clinic','prevent_b7',['daram','karo','resident_seori'],2);segment(s,1,21);goto('sleep7')
s='MS14_D07_S04';begin(s,'gate','incident7',['karo','resident_seori'],2);segment(s,1,12);travel('room13','incident_room7');segment(s,13,36);goto('sleep7')
label('sleep7');lines.append('    if r13_v111_value("DARAM_DETAINED"):');lines.append('        jump r13_v111_detained_sleep7');goto('free_sleep7')
finish_day('free_sleep7',8,'day8')
label('detained_sleep7');travel('room13','detained_sleep7');goto('detained_bed7')
field('detained_bed7','room13',[],'bed','다음 날 면회를 준비한다','detained_morning8')
label('detained_morning8');code('r13_v111_set("day",8)');goto('day8')
branch('day8',V('route7')+"=='murder'",'custody8','prevent_clinic8')
s='MS14_D08_S01';begin(s,'v111_custody','custody8',['daram','resident_seori','neoul']);segment(s,1,25);goto('room_evidence8')
s='MS14_D08_S02';begin(s,'room13','room_evidence8',['doto','buri']);goto('room_check8')
field('room_check8','room13',['doto','buri'],'floor','문틈과 발견 자리를 살핀다','room_checked8')
label('room_checked8');segment(s,1,37);code('r13_nw_acquire("NW_STONE")');goto('wounds8')
s='MS14_D08_S03';begin(s,'clinic','wounds8',['resident_seori','buri']);segment(s,1,6);goto('tool_faces8')
field('tool_faces8','clinic',['resident_seori','buri'],'notes','손잡이·파단면·고리를 확인한다','tool_faces_seen8')
label('tool_faces_seen8');segment(s,7,19);goto('wire_curve8')
field('wire_curve8','clinic',['resident_seori','buri'],'notes','구리 조각과 핀 끝을 대조한다','wire_curve_seen8')
label('wire_curve_seen8');segment(s,20,28);goto('mother_letter8')
s='MS14_D08_P01';begin(s,'clinic','prevent_clinic8',['daram','resident_owlgp','resident_seori']);branch('prevention_story8',V('prevention')+"=='A'",'fear8','care8')
label('fear8');segment(s,1,10);goto('missing_pages8')
label('care8');segment(s,11,17);goto('missing_pages8')
label('missing_pages8');segment(s,18,26);code('r13_nw_acquire("NW_STONE","removed" if r13_v111_value("prevention")=="A" else "clinic")');goto('mother_letter8')
s='MS14_D08_S04';begin(s,'square','mother_letter8',['resident_lamplighter','doto','resident_badook'],1);segment(s,1,5);branch('letter_route8',V('route7')+"=='murder'",'letter_murder8','letter_prevent8')
label('letter_murder8');segment(s,6,13);segment(s,22,26);goto('escort8')
label('letter_prevent8');segment(s,14,21);segment(s,27,30);goto('escort8')
talk('escort8','square',['resident_lamplighter','doto','resident_badook'],'resident_badook','공개 길 동행을 부탁합니다.','escort_done8')
label('escort_done8');code('r13_v111_set("public_road_escort_completed",True)');segment(s,31,33);goto('sleep8')
finish_day('sleep8',9,'day9')
branch('day9',V('route7')+"=='murder'",'passage9','prevent_passage9')
s='MS14_D09_S01';begin(s,'kitchen','passage9',['doto','resident_ttadak','granny']);goto('safe_passage9')
wait('safe_passage9','kitchen',['doto','resident_ttadak'],[obj('쐐기·안전줄·문지기를 확인한다','kitchen','rear'),person('들어가기 전에 확인할 것은요?','kitchen','resident_ttadak')],['passage_walk9','passage_safety_hint9'])
label('passage_safety_hint9');segment(s,15,16);goto('safe_passage9')
label('passage_walk9');segment(s,1,14);goto('passage_after9')
wait('passage_after9','kitchen',['doto','resident_ttadak'],[dict(title='작업장으로 간다',location='workshop',move='workshop'),person('실측한 길을 다시 확인합니다.','kitchen','resident_ttadak')],['workshop9','passage_measured_hint9'])
label('passage_measured_hint9');segment(s,17,18);goto('passage_after9')
s='MS14_D09_S02';begin(s,'workshop','workshop9',['buri']);branch('tok_route9','r13_v111_tok_attends("workshop")','tok9','repair_copy9')
label('tok9');code('r13_v111_arrive(["buri","resident_tok"])');segment(s,1,18);goto('scarf9')
label('repair_copy9');segment(s,19,26);goto('scarf9')
s='MS14_D09_S03';begin(s,'dining','scarf9',['nabi']);lines.append('    if '+V('NABI_relationship')+"=='strained':");lines.append('        call r13_v111_repair_trust9');goto('pin_question9')
label('repair_trust9');segment(s,1,5);lines.append('    return')
talk('pin_question9','dining',['nabi'],'nabi','핀을 다시 채운 때를 묻겠습니다.','pin_time9')
label('pin_time9');segment(s,6,34);goto('scarf_compare9')
field('scarf_compare9','dining',['nabi'],'mittens','목도리 끝과 핀을 대조한다','scarf_done9')
label('scarf_done9');segment(s,42,49);goto('postal9')
s='MS14_D09_P01';begin(s,'kitchen','prevent_passage9',['doto','resident_ttadak','granny','nabi']);goto('safe_prevent9')
field('safe_prevent9','kitchen',['doto','resident_ttadak'],'rear','쐐기·안전줄·문지기를 확인한다','prevent_walk9')
label('prevent_walk9');segment(s,1,12);travel('room13','returned_papers9');goto('papers_check9')
field('papers_check9','room13',['resident_owlgp','granny'],'books','반환 장수와 빈 자리를 확인한다','papers_done9')
label('papers_done9');segment(s,13,27);goto('postal9')
s='MS14_D09_S04';begin(s,'post','postal9',['seryeon','resident_sling'],1);segment(s,1,24);branch('night_route9',V('route7')+"=='murder'",'custody_night9','school_night9')
label('custody_night9');travel('v111_custody','custody_night9');segment(s,25,30);goto('sleep9')
label('school_night9');travel('school','school_night9');segment(s,31,36);goto('sleep9')
finish_day('sleep9',10,'day10')
branch('day10',V('route7')+"=='murder'",'waiting10','prevent_hearing10')
s='MS14_D10_S01';begin(s,'school','waiting10',['daram','resident_seori','buri']);segment(s,1,19);goto('hearing10')
s='MS14_D10_S02';begin(s,'school','hearing10',['daram','doto','nabi','granny','neoul','resident_ppul','resident_seori']);segment(s,1,10);goto('wound_proof10')
proof('wound_proof10','두 상처와 촛대 파손을 대조한다',['E08_CHILD_ACCOUNT','E08_TOOL'],'wound_answer10','hearing_wrong10','hearing_hint10')
label('wound_answer10');segment(s,11,33);goto('passage_proof10')
proof('passage_proof10','두 번째 길을 실제 기록으로 보인다',['E09_PASSAGE','E08_ROOM'],'passage_answer10','passage_wrong10','hearing_hint10')
label('passage_answer10');segment(s,34,46);goto('owner10')
# New world (event 06): the day-10 meeting is decided once. A half presentation (part of the
# right set, nothing wrong) gets one more try. Losing a gate (self-defence, the second door)
# lists Daram for the cart; losing a later point frees Daram but leaves Granny free.
def nw_half_retry(key,correct,a,b,proof_key,note):
 label(key)
 lines.append('    if r13_nw_retry("room13",%r,%r):'%(correct,note))
 lines.append('        call r13_lines(r13_v111_lines(%r),%r)'%(['MS14_D10_S0%d_L%04d'%(3 if key in R13_S03_WRONG else 2,n) for n in range(a,b+1) if 'MS14_D10_S0%d_L%04d'%(3 if key in R13_S03_WRONG else 2,n) in DATA['records'] and DATA['records']['MS14_D10_S0%d_L%04d'%(3 if key in R13_S03_WRONG else 2,n)]['kind'] in ('dialogue','narration')],'v111:'+key+':half'))
 lines.extend(['        jump r13_v111_'+proof_key])
R13_S03_WRONG=('owner_wrong10','time_wrong10','contact_wrong10')
def room13_end(key,a,b,result,kind=None):
 code('r13_nw_meeting_end("room13",%r)'%result)
 if result=='lose':code('r13_nw_list("daram","room13_lose")')
 if kind:code('r13_v111_set("room13_partial_kind",%r)'%kind)
 segment('MS14_D10_S03' if key in R13_S03_WRONG else 'MS14_D10_S02',a,b)
 # Not won: Daram still leaves the protection room for school (the next scene needs it),
 # but nothing here records Granny's admission or a proven release basis (review 2026-10-22).
 code("r13_v111_apply('MS14_D10_S03_L0088',[o for o in R13_V111['records']['MS14_D10_S03_L0088']['operations'] if o['field'] in ('DARAM_DETAINED','DARAM_location','D10_confrontation_release_completed')])");goto('bench10')
nw_half_retry('hearing_wrong10',['E08_CHILD_ACCOUNT','E08_TOOL'],47,48,'wound_proof10','너울이 고개를 젓는다. 아이의 말과 촛대 조각을 함께 놓아야 한다.');room13_end('hearing_wrong10',47,48,'lose')
nw_half_retry('passage_wrong10',['E09_PASSAGE','E08_ROOM'],50,50,'passage_proof10','따닥이 고개를 젓는다. 직접 걸어 본 길과 현장 배치를 함께 놓아야 한다.');room13_end('passage_wrong10',50,50,'lose')
label('hearing_hint10');segment(s,51,52);goto('wound_proof10')
s='MS14_D10_S03';begin(s,'school','owner10',['daram','granny','resident_ppul','neoul','nabi','resident_seori']);segment(s,1,4);goto('owner_proof10')
proof('owner_proof10','구리선과 수선 출처를 대조한다',['E08_WOUND_WIRE','E09_PIN_OWNER'],'owner_answer10','owner_wrong10')
branch('owner_answer10','r13_v111_tok_attends("hearing")','owner_tok10','owner_copy10')
label('owner_tok10');code('r13_v111_arrive(["daram","granny","resident_ppul","neoul","nabi","resident_seori","resident_tok"])');segment(s,5,13);goto('time10')
label('owner_copy10');segment(s,14,17);goto('time10')
label('time10');segment(s,18,22);goto('time_proof10')
proof('time_proof10','첫 비명 뒤 핀을 다시 채운 때',['E09_PIN_TIME','E09_PIN_HANDOVER_TIME'],'time_answer10','time_wrong10')
label('time_answer10');segment(s,23,44);goto('contact_proof10')
proof('contact_proof10','접촉면과 아이의 위치를 대조한다',['E08_CONTACT_ASSEMBLY','E08_WOUND_WIRE','E08_CHILD_POSITION','E08_ROOM_REACH','E09_SCARF'],'contact_answer10','contact_wrong10')
label('contact_answer10');code('r13_nw_meeting_end("room13","win")');segment(s,45,88);code('r13_v111_set("grandmother_custody","detained")');code('r13_v111_set("forgery_confirmed",True)');goto('bench10')
nw_half_retry('owner_wrong10',['E08_WOUND_WIRE','E09_PIN_OWNER'],89,89,'owner_proof10','할머니가 웃는다. 구리선과 수선 기록을 함께 놓아야 한다.');room13_end('owner_wrong10',89,89,'partial','unknown')
nw_half_retry('time_wrong10',['E09_PIN_TIME','E09_PIN_HANDOVER_TIME'],90,90,'time_proof10','나비가 고개를 젓는다. 핀을 다시 채운 때와 계단참의 핀을 함께 놓아야 한다.');room13_end('time_wrong10',90,90,'partial','unknown')
nw_half_retry('contact_wrong10',['E08_CONTACT_ASSEMBLY','E08_WOUND_WIRE','E08_CHILD_POSITION','E08_ROOM_REACH','E09_SCARF'],91,92,'contact_proof10','할머니가 목도리를 여민다. 천과 핀, 상처, 아이의 자리를 함께 놓아야 한다.');room13_end('contact_wrong10',91,92,'partial','accident')
s='MS14_D10_S04';begin(s,'post','bench10',['daram','seryeon','buri','nabi'],1);segment(s,1,27);goto('sleep10')
s='MS14_D10_P01';begin(s,'school','prevent_hearing10',['daram','resident_owlgp','granny','resident_ppul','neoul']);segment(s,1,18);goto('authority_proof10')
proof('authority_proof10','수신인과 가족 전달 권한을 구분한다',['E06_CONTACT','E09_MAIL'],'authority_answer10','authority_wrong10')
label('authority_answer10');segment(s,19,30);goto('writing_proof10')
proof('writing_proof10','반송·필사본·초대 발송을 대조한다',['E01','E07','E09_MAIL'],'writing_answer10','writing_wrong10')
label('writing_answer10');code('r13_nw_meeting_end("records","win")');segment(s,31,48);goto('pocket10')
talk('pocket10','school',['resident_owlgp'],'resident_owlgp','어제는 전부라고 하셨습니다.','pocket_answer10')
label('pocket_answer10');segment(s,49,55);lines.extend(['    menu:','        "가족에게만 날짜와 수량을 본다":','            jump r13_v111_family_paper10','        "공개 수치만 대조하고 인계한다":','            jump r13_v111_public_paper10'])
label('family_paper10');segment(s,56,69);goto('private_handoff10')
wait('private_handoff10','school',['daram','resident_owlgp','granny'],[
 person('아내가 직접 편지를 건넸습니까?','school','resident_owlgp'),
 person('공개 수치만 대조하고 인계해 주십시오.','school','resident_owlgp')],['owl_invitation10','public_paper10'])
label('owl_invitation10');lines.append('    call r13_lines([("resident_owlgp","부인이 직접 준 게 아니네. 편지는 할머니가 전했지.",{"no_lead":True})],"v111:owl_invitation_testimony")');code('r13_v111_set("owl_invitation_testimony",True)');goto('private_handoff10')
label('public_paper10');code('r13_v111_arrive(["daram","resident_owlgp","granny","seryeon"])');segment(s,70,83);goto('prevent_return10')
# New world (event 07): the records meeting is decided once. Losing the addressee (gate) gives
# the bundle to Granny and lists the old man; losing the writing point keeps him under watch.
def records_half(key,correct,a,b,proof_key,note):
 label(key)
 rids=['MS14_D10_P01_L%04d'%n for n in range(a,b+1) if 'MS14_D10_P01_L%04d'%n in DATA['records']]
 lines.extend(['    if r13_nw_retry("records",%r,%r):'%(correct,note),
  '        call r13_lines(r13_v111_lines(%r),%r)'%(rids,'v111:'+key+':half'),
  '        jump r13_v111_'+proof_key])
records_half('authority_wrong10',['E06_CONTACT','E09_MAIL'],84,85,'authority_proof10','부엉이가 손을 거둔다. 받는 사람과 그 기록을 함께 놓아야 한다.')
code('r13_nw_meeting_end("records","lose")');code('r13_nw_list("resident_owlgp","records_lose")');segment(s,84,85);code("r13_v111_commit('MS14_D10_P01_L0083')");goto('prevent_return10')
records_half('writing_wrong10',['E01','E07','E09_MAIL'],86,86,'writing_proof10','슬링이 고개를 젓는다. 편지와 봉투, 필사본을 함께 놓아야 한다.')
code('r13_nw_meeting_end("records","partial")');segment(s,86,86);goto('writing_partial10')
label('writing_partial10');segment(s,43,48);goto('pocket10')
s='MS14_D10_S04P';begin(s,'school','prevent_return10',['daram'],1);segment(s,1,5);goto('sleep10')
finish_day('sleep10',11,'day11')
(ROOT/'game/room13_v111_days610.rpy').write_text('\n'.join(lines)+'\n')
(ROOT/'game/v111/records.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
(ROOT/'game/v111/field-bindings.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
