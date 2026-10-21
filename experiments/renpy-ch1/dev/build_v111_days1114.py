"""Reviewed final days in ordinary Ren'Py labels and existing Room13 inputs.
This build-time authoring script is never shipped as an execution controller.
"""
from build_v111_days610 import *
lines.clear();lines.append('# Reviewed D11–D14 source records and native callbacks.')
DIRECTION_EFFECTS={
 '담요 소유 수량 유지; 출발 시 가족 짐으로 복귀','가족 실제 자리 확인 전 대피완료 아님','실제 도착 대상별 학교 도착 기록',
 '네로 학교 잔류; 밤 재출발 없음','실제 작업 완료 뒤 굽이 통과 불가; 미대피자만 상실','토실 전달 반복 금지',
 '먹음/쓴맛/증상/사망 사실 생성 금지','약장 직접 확인 완료에만 접근 차단 기록','학교 자리 확보; 온기 도착 별도',
 '엄마 다람 보호 전담; 환자 부축 중복 금지','다람 location=아빠 동행; 피해 슬롯 아님','다람 location=학교; 나비 보호; 피해 슬롯 아님',
 '가족 거래 수락; 실제 혜택 수령은 D13_A에서 확인','가족 거래 혜택 없음; 엄마·다람 대결 종료까지 현장',
 '실룩 결박/구금 대사 없음','정지 담당=돌목; 실룩 감독 교대 전 하차 대기','굴돌 실제 학교 인수 후 handed_over',
 '모모 실제 학교 인수 후 handed_over','선생님 분리 감독 장소 실제 인수 후 handed_over','실룩 원래 감독 장소 인수 후 handed_over',
 '미인계자 감독·보온 대기; 사망/전원구조 생성 없음','실제 마지막 인수 후 전원 구조','실제 수레 반환',
 '엄마·다람·까로 학교 이동; 까로 귀환 전 현장 운반 금지','엄마·다람·네로 학교 이동; 네로 현장 역할 해제',
 '환자 부축 일시 중지; 실제 저지 결과 별도','환자 부축 일시 중지; 너울 보호; 생긴 부상만 기록','실제 폭행 피해 기록; 새 사망 없음',
 '부상 진료/실패 후회 블록 제외; 실제 구조 결과 유지','실제 구조자 보존; 새 구조 자동 생성 없음','실제 배정 성인만 길 안내',
 '명령 대결 1회 완료; 산에서 반복 없음','까로 학교 운반 전담; 다른 동시 역할 해제','돌목 보호 역할; 다른 감독 역할 교대 필요',
 '고정부 분리 미완료; 기존 구조 유지','공구 내려놓음; 자동 분리 성공 없음','호송 장비 실제 보존·반환; 해당 모든 확인 후에만 current_transport_chain_stopped=true',
 '점등 없음; 다음 날 실제 연결 작업 유지','초롱 출연 없음; 실제 연결분만 점등','가족 과자 유지; 즉각 화해 강요 없음','이름판 강요 없음','보미 결말 유지; 토실 추가 청취 없음',
 '가족 실제 학교 이동 후 night14_lodging=school','거래 미수락 유지',
}
EXACT_EFFECTS={
 '도담 alive=false (늦은 섭취 피해 경로의 실제 의료 확인)':[dict(op='set',field='alive:kid_dodam',value=False)],
 '새미 alive=true (실제 진료 생존 확인; 추가 피해 생성 없음)':[dict(op='set',field='alive:kid_saemi',value=True)],
 'current_sacrifice_operation_closed=false 유지':[dict(op='set',field='current_sacrifice_operation_closed',value=False)],
 'route12=uncommitted 유지':[],
 'teacher custody=Neoul':[dict(op='set',field='teacher_custody',value='neoul')],
 'teacher custody=Dolmok_supervision':[dict(op='set',field='teacher_custody',value='guard')],
 'teacher transfer=listed; 실제 탑승 전 aboard 금지':[dict(op='set',field='teacher_transfer',value='listed')],
 'teacher transfer=not_aboard':[dict(op='set',field='teacher_transfer',value='not_aboard')],
}
UNBOUND=[]
for sid,spec in SCENES.items():
 if spec['source_scene']['day']<11:continue
 DATA['scene_days'][sid]=spec['source_scene']['day'];DATA['audio'][sid]=spec['audio']['file']
 for b in spec['blocks']:
  for c in b['cues']:
   r=copy.deepcopy(c['source_record']);ops=[]
   for effect in r.get('effects',[]):
    if effect in EXACT_EFFECTS:ops+=EXACT_EFFECTS[effect]
    elif effect in DIRECTION_EFFECTS:pass # Bound at the explicit semantic callback below.
    elif re.fullmatch(r'[A-Za-z0-9_.]+=[A-Za-z0-9_]+',effect):
     k,v=effect.split('=',1);ops.append(dict(op='set',field=k,value=scalar(v)))
    elif re.fullmatch(r'[a-z_]+[+-]=1',effect):
     # Quantity transfer is committed in the once-only actual handoff callback.
     pass
    else:UNBOUND.append((r['id'],effect))
   r.update(operations=ops,direction=c['directed_expression']);DATA['records'][r['id']]=r
if UNBOUND:raise ValueError(UNBOUND)
# All 113 individual requires are explicit callbacks, separate from block/scene
# control flow. Never evaluate the authored natural-language conditions at runtime.
ACTORS={'굴돌':'resident_guldol','까로':'karo','초롱':'resident_lamplighter','네로':'resident_nero','돌목':'guard','백 부인':'resident_madam','바둑이':'resident_badook','부리':'buri','아빠':'dad','엄마':'mom'}
allowed={}
for rid,r in DATA['records'].items():
 if not r.get('requires'):continue
 expr=[]
 for req in r['requires']:
  if req=='route12=late_exposure':expr.append(V('route12')+"=='late_exposure'")
  elif req.startswith('나비 실제 학교 인수 담당'):expr.append("r13_v111_actor_ready('nabi') and room13['location']=='school'")
  elif req.startswith('토실 밖에서'):expr.append(V('tosil_listen')+"=='outside' and "+V('adult_interview_done'))
  elif req.startswith('토실 선택='):expr.append(V('tosil_listen')+"=='inside' and r13_v111_actor_ready('resident_tosil')")
  elif req=='실제 군중 폭행 피해 결말 아님':expr.append('not '+V('crowd_injury'))
  elif req.startswith(('다람 현장','다람·엄마','다람 location=광장')):expr.append("r13_v111_actor_ready('daram') and room13['location']=='square'")
  elif req=='엄마 현장 잔류':expr.append("r13_v111_actor_ready('mom') and room13['location']=='square'")
  else:
   name=next((name for name in ACTORS if req.startswith(name+' ')),None)
   if name not in ACTORS:raise ValueError((rid,req))
   expr.append('r13_v111_actor_ready('+q(ACTORS[name])+')')
 allowed[rid]=' and '.join(dict.fromkeys(expr))
# Existing r13_lines keeps normal dialogue/skip behavior. It is called only when
# this record's authored condition is satisfied, including before applying effects.
def late(sid,first,last):
 for n in range(first,last+1):
  rid=sid+'_L%04d'%n
  if rid not in DATA['records']:continue
  before=len(lines)
  audio=SOURCE[rid].get('audio_change',{})
  if audio.get('operation')=='stop_bgm':
   code('room13["v111"]["music_hold"]=room13["v111"]["scene"]');code('renpy.music.stop(fadeout=.15)')
  elif audio.get('operation')=='start_low':
   code('room13["v111"]["music_hold"]=None')
   code('room13["v111"]["music_override"]='+repr(dict(scene=sid,path=audio.get('file'))))
   code('renpy.music.play('+q(audio['file'])+',fadein=1.0,relative_volume=.28)')
  segment(sid,n,n)
  if rid in allowed and len(lines)>before:
   body=lines[before:];del lines[before:];lines.append('    if '+allowed[rid]+':');lines.extend('    '+x for x in body)
def arrive(cast):code('r13_v111_arrive('+q(cast)+')')
def start(sid,loc,key,cast,period=0):begin(sid,loc,key,cast,period);arrive(cast)
def setv(k,v):code('r13_v111_set('+q(k)+','+q(v)+')')
def observation(key,name,text):DATA['evidence'][key]=dict(name=name,kind='기록',variants=dict(observed=text))
def grant(key,event):code('r13_v111_apply('+q(event)+',[dict(op="acquire",key='+q(key)+',variant="observed")])')
def select(rows):
 lines.append('    menu:')
 for title,target,guard in rows:
  lines.append('        '+q(title)+(' if '+guard if guard else '')+':');lines.append('            jump r13_v111_'+target)
FAMILY=['dad','mom','daram']
observation('E14_SUPPLY','학교 물자 인수·사용 기록','아빠와 까로가 실제로 운반한 온기 상자를 선생님이 인수했다. 연결·사용 상태는 따로 확인한다. 새 조각을 만든 기록이 아니다.')
# DAY 11 — locate the family through observed messages, protect Tosil first.
s='MS14_D11_S00';start(s,'school','day11',['daram','karo']);late(s,1,5);travel('forest','pump11');arrive(['daram','karo']);late(s,6,8);goto('pump_open11')
field('pump_open11','forest',['daram','karo'],'v111_box','셋째 말뚝 아래 통을 연다','pump_reply11')
label('pump_reply11');late(s,9,14);setv('root_address_known',True);goto('root11')
s='MS14_D11_S01';start(s,'forest','root11',['daram','resident_tosil']);late(s,1,4);goto('root_note11')
field('root_note11','forest',['daram','resident_tosil'],'forest_roots','눌러 둔 돌 아래 쪽지를 본다','root_read11')
label('root_read11');late(s,5,15);setv('greenhouse_address_known',True)
lines.append('    if '+V('grandmother_custody')+"=='detained':");lines.append('        call r13_v111_tosil_detained11');lines.append('    else:');lines.append('        call r13_v111_tosil_free11');late(s,24,38);travel('school','tosil_school11');arrive(['daram','resident_tosil']);lines.append('    if r13_v111_value("location:nabi") not in (None,"school"):');lines.append('        jump r13_v111_nabi_waiting11');goto('nabi_arrival11')
label('tosil_detained11');late(s,20,23);lines.append('    return')
label('tosil_free11');late(s,16,19);lines.append('    return')
label('nabi_waiting11');late(s,48,50);goto('nabi_wait11')
field('nabi_wait11','school',['daram','resident_tosil'],'desks','나비가 올 때까지 토실과 기다린다','nabi_arrival11')
label('nabi_arrival11');arrive(['daram','resident_tosil','nabi']);late(s,39,47);goto('tosil_handoff11')
talk('tosil_handoff11','school',['daram','resident_tosil','nabi'],'nabi','토실의 보호를 부탁합니다.','tosil_safe11')
label('tosil_safe11');late(s,51,52);goto('reunion11')
s='MS14_D11_S02';start(s,'greenhouse','reunion11',['daram','mom']);late(s,1,16);setv('family_reunited',True);goto('dry11')
s='MS14_D11_S02A';start(s,'greenhouse','dry11',['daram','mom']);late(s,1,20)
select([('두 장을 꺼내 덮는다','blanket_use11',V('carried_dry_blankets')+'==2'),('한 장을 함께 덮는다','blanket_one11',V('carried_dry_blankets')+'==1'),('짐 안에 둔다','blanket_keep11',V('carried_dry_blankets')+'>0'),('외투 안쪽을 함께 덮는다','coat_use11',V('carried_dry_blankets')+'==0')])
# Zero stock has no meaningless menu: native jump before reaching it.
# Rewritten below after generation so only actual two-way inventory decisions show.
label('blanket_use11');late(s,21,27);goto('dry_done11')
label('blanket_one11');late(s,36,38);goto('dry_done11')
label('blanket_keep11');late(s,28,31);late(s,33,35);goto('dry_done11')
label('coat_use11');late(s,28,31);goto('dry_done11')
label('dry_done11');late(s,32,32);goto('button11')
s='MS14_D11_S02B';start(s,'greenhouse','button11',['daram','mom']);late(s,1,21);goto('mother_questions11')
wait('mother_questions11','greenhouse',['daram','mom'],[
 person('어떻게 지냈어?','greenhouse','mom'),person('왜 우리를 부르지 않았어?','greenhouse','mom'),person('왜 돌아오지 못했어?','greenhouse','mom')],['mother_life11','mother_invitation11','mother_return11'])
for key,a,b,flag in [('mother_life11',22,35,'mother_q_life'),('mother_invitation11',36,41,'mother_q_invitation'),('mother_return11',42,48,'mother_q_return')]:
 label(key);late(s,a,b);setv(flag,True);goto('mother_ready11')
branch('mother_ready11','all(r13_v111_value(k) for k in '+q(['mother_q_life','mother_q_invitation','mother_q_return'])+')','mother_last11','mother_questions11')
label('mother_last11');late(s,49,54)
lines.append('    if '+V('forgery_confirmed')+':');lines.append('        call r13_v111_forgery_question11')
lines.append('    if '+V('OWL_ALIVE')+' and '+V('owl_invitation_testimony')+':');lines.append('        call r13_v111_owl_question11');goto('facility11')
label('forgery_question11');late(s,55,57);lines.append('    return')
label('owl_question11');late(s,58,59);lines.append('    return')
s='MS14_D11_S03';start(s,'facility','facility11',['daram','mom','resident_guldol','resident_lamplighter','guard','karo'],1);late(s,1,1);lines.append('    if r13_v111_actor_ready("resident_guldol"):');lines.append('        call r13_v111_guldol_heat11');lines.append('    else:');lines.append('        call r13_v111_mother_heat11');goto('heat_check11')
label('guldol_heat11');late(s,2,9);lines.append('    return')
label('mother_heat11');late(s,43,45);lines.append('    return')
field('heat_check11','facility',['daram','mom','resident_guldol','resident_lamplighter','guard','karo'],'blankets','조각과 잔열을 확인한다','heat_seen11')
label('heat_seen11');late(s,10,19);setv('heat_inventory_observed',True)
lines.append('    if '+V('carried_dry_blankets')+'>0:');lines.append('        call r13_v111_family_blankets11');lines.append('    else:');lines.append('        call r13_v111_no_blankets11')
select([('가족 자리부터 본다','family_place11',None),('아랫길 대피 준비를 확인한다','rescue_prepare11',None),('준비된 물자를 학교로 옮긴다','supply_school11',None)])
label('family_blankets11');late(s,20,21);lines.append('    return')
label('no_blankets11');late(s,22,23);lines.append('    return')
label('family_place11');late(s,48,49);travel('school','family_place11');arrive(['mom','daram','nabi','resident_teacher']);goto('family_place_check11')
field('family_place_check11','school',['mom','daram','nabi','resident_teacher'],'blankets','가족 세 사람이 쓸 자리를 확인한다','family_place_done11')
label('family_place_done11');setv('family_school_place',True);goto('school_visit11')
label('rescue_prepare11');travel('square','rescue_prepare11');arrive(['mom','daram','karo','resident_nero','resident_lamplighter']);goto('rescue_cart11')
talk('rescue_cart11','square',['mom','daram','karo','resident_nero','resident_lamplighter'],'karo','빈 수레와 덮개를 부탁합니다.','rescue_ready11')
label('rescue_ready11');setv('rescue_cart_ready',True);setv('rescue_cover_ready',True);setv('rescue_driver_ready',True);setv('rescue_lights_ready',True);goto('day_rescue11')
label('day_rescue11');late(s,50,53);travel('forest','day_rescue11',[]);arrive(['karo','resident_nero']);goto('day_rescue_door11')
field('day_rescue_door11','forest',['karo','resident_nero'],'v111_box','아랫길 사람들의 문을 연다','day_rescue_school11')
label('day_rescue_school11');travel('school','day_rescue_school11');arrive(['mom','daram','nabi','resident_teacher','resident_nero','karo']);setv('lower_road_handover',3);goto('school_visit11')
label('supply_school11');travel('school','supply_school11');arrive(['mom','daram','karo','resident_teacher','nabi']);late(s,24,27);setv('school_supply_handed',True);setv('school_heat_connected',False);grant('E14_SUPPLY','actual_school_supply11');goto('school_visit11')
label('school_visit11');arrive(['mom','daram','nabi','resident_teacher','resident_tosil']);late(s,28,36);lines.append('    if not r13_v111_value("family_school_place"):');lines.append('        jump r13_v111_family_space_after_supply11');goto('family_space_ready11')
field('family_space_after_supply11','school',['mom','daram','nabi','resident_teacher'],'blankets','가족 세 사람의 실제 자리를 확인한다','family_space_checked11')
label('family_space_checked11');setv('family_school_place',True);goto('family_space_ready11')
label('family_space_ready11')
lines.append('    if '+V('carried_dry_blankets')+'>0 and not '+V('tosil_blanket_given')+':');lines.append('        jump r13_v111_blanket_choice11');goto('night11')
label('blanket_choice11');select([('가족 짐에 보관한다','blanket_store11',None),('토실에게 한 장을 건넨다','tosil_blanket11',None)])
label('blanket_store11');late(s,54,55);goto('night11')
label('tosil_blanket11');late(s,37,40);lines.append('    if r13_v111_value("carried_dry_blankets")>1:');lines.append('        call r13_v111_tosil_blanket_remaining11');lines.append('    else:');lines.append('        call r13_v111_tosil_blanket_last11');code('r13_v111_apply("tosil_actual_blanket",[dict(op="set",field="carried_dry_blankets",value=r13_v111_value("carried_dry_blankets")-1),dict(op="set",field="tosil_bedding_received",value=1),dict(op="set",field="tosil_blanket_given",value=True)])');goto('night11')
label('tosil_blanket_remaining11');late(s,41,41);lines.append('    return')
label('tosil_blanket_last11');late(s,57,57);lines.append('    return')
s='MS14_D11_S04';start(s,'school','night11',['mom','daram','resident_teacher','karo','resident_nero'],2);late(s,1,1)
lines.append('    if '+V('carried_dry_blankets')+'>0:');lines.append('        call r13_v111_rest_blanket11')
branch('night_rescue_route11',V('lower_road_handover')+'==3','lower_safe11','request_rescue11')
label('rest_blanket11');late(s,2,7);lines.append('    return')
label('lower_safe11');late(s,30,32);setv('nero_alive',True);goto('sleep11')
label('request_rescue11');late(s,8,14);goto('night_rescue_prepare11')
field('night_rescue_prepare11','school',['mom','daram','resident_teacher','karo','resident_nero'],'blankets','운반 인력·길등·덮개를 확인한다','night_rescue_choices11')
label('night_rescue_choices11')
code('r13_v111_set("rescue_cart_ready",r13_v111_actor_ready("karo"))')
code('r13_v111_set("rescue_driver_ready",r13_v111_actor_ready("karo"))')
code('r13_v111_set("rescue_lights_ready",bool(r13_v111_value("heat_inventory_observed")))')
setv('rescue_cover_ready',True)
lines.append('    if r13_v111_value("rescue_cart_ready") and r13_v111_value("rescue_driver_ready") and r13_v111_value("rescue_lights_ready") and r13_v111_value("school_supply_handed"):');lines.append('        jump r13_v111_night_rescue11')
select([('준비된 수레로 지금 출발한다','night_rescue11',V('rescue_cart_ready')+' and '+V('rescue_cover_ready')+' and '+V('rescue_driver_ready')+' and '+V('rescue_lights_ready')),('학교 물자 인계를 먼저 끝낸다','late_supply11','not '+V('school_supply_handed')),('없는 운반수단을 지금 구한다','late_cart11','not '+V('rescue_cart_ready'))])
label('night_rescue11');travel('forest','night_rescue11',[]);arrive(['karo','resident_nero']);late(s,15,16);goto('snow_door11')
field('snow_door11','forest',['karo','resident_nero'],'v111_box','눈에 막힌 문을 연다','night_rescue_done11')
label('night_rescue_done11');late(s,17,19);travel('school','night_rescue_done11');arrive(['mom','daram','resident_teacher','karo','resident_nero']);late(s,20,25);setv('lower_road_handover',3);setv('nero_alive',True);goto('sleep11')
label('late_supply11');late(s,35,36);goto('late_supply_handoff11')
field('late_supply_handoff11','school',['mom','daram','resident_teacher','karo'],'blankets','온기 상자 인수를 확인한다','late_supply_done11')
label('late_supply_done11');setv('school_supply_handed',True);setv('school_heat_connected',False);grant('E14_SUPPLY','actual_late_school_supply11');goto('late_road11')
label('late_cart11');late(s,37,38);goto('late_road11')
label('late_road11');travel('forest','late_road11',[]);arrive(['karo']);late(s,26,29);setv('lower_road_lost',True);setv('location:resident_nero','forest');setv('nero_alive',False);goto('sleep11')
finish_day('sleep11',12,'day12')
# DAY 12 definitions appended below.
s='MS14_D12_S01';start(s,'school','day12',['mom','daram','karo','guard','resident_teacher','resident_nero']);branch('loss_route12',V('lower_road_lost'),'loss_names12','living_names12')
label('loss_names12');travel('forest','loss_names12',[]);arrive(['karo']);late(s,1,3);travel('square','names_square12');arrive(['daram','karo']);late(s,4,9);goto('morning_notice12')
label('living_names12');late(s,10,15);goto('morning_notice12')
label('morning_notice12');travel('school','notice12');arrive(['mom','daram','guard','resident_teacher']);late(s,16,23);goto('morning_prep12_entry')
label('morning_prep12_entry');code('r13_v111_scene("MS14_D12_S01")');goto('morning_prep12')
wait('morning_prep12','school',['mom','daram','guard','resident_teacher'],[
 person('약장 관리를 확인합니다.','clinic','resident_seori'),person('온기 자리를 부탁드립니다.','school','resident_teacher'),person('학교 운반을 부탁한다.','square','karo'),obj('배식 준비를 살핀다','school','desks'),person('학교 물자를 함께 확인하시겠습니까?','store','resident_madam')],['medicine12','warm_place12','carrier12','meal12','madam_invite12'])
label('madam_invite12');arrive(['resident_madam']);lines.append('    call r13_lines([("resident_madam","내놓은 돌이 어디 쓰이는지는 보겠어요.",{"no_lead":True})],"v111:madam_observer_consent12")');setv('madam_observer_consent',True);travel('school','madam_school12',[]);arrive(['mom','daram','resident_teacher','resident_madam']);goto('morning_prep12_entry')
label('medicine12');arrive(['resident_seori']);late(s,24,25);setv('medicine_locked',True);goto('morning_prep12_entry')
label('warm_place12');travel('school','warm_place12');arrive(['mom','daram','resident_teacher']);late(s,26,27);setv('warm_seat_ready',True);goto('morning_prep12_entry')
label('carrier12');arrive(['karo']);late(s,28,30);travel('school','carrier_arrived12');arrive(['karo','mom','daram','resident_teacher']);setv('carrier_arrived',True);setv('busy:karo','school_transport');goto('carrier_receipt12')
talk('carrier_receipt12','school',['karo','mom','daram','resident_teacher'],'resident_teacher','도착한 온기 상자의 인수를 확인한다','carrier_received12')
label('carrier_received12');setv('warm_support_arrived',True);setv('school_supply_handed',True);grant('E14_SUPPLY','actual_school_supply12');setv('busy:karo',False);goto('morning_prep12_entry')
s='MS14_D12_S02';start(s,'school','meal12',['daram','nabi','resident_teacher','resident_bori','kid_dodam','kid_saemi'],1);setv('route12','uncommitted');setv('location:mom','facility');late(s,1,24);setv('bottle_original_seal_seen',True);goto('meal_choice12')
label('meal_choice12');select([('배식 전에 더 살핀다','stay_meal12',None),('다람과 온기 조각을 받으러 간다','take_daram12',None),('다람은 나비 곁에 두고 다녀온다','leave_daram12',None),('예방 준비를 확인한다','prevent_check12',None)])
label('prevent_check12');lines.append('    if all(r13_v111_value(k) for k in ("medicine_locked","warm_seat_ready","carrier_arrived","warm_support_arrived")):');lines.append('        jump r13_v111_prevent_ready12');lines.append('    if not r13_v111_value("medicine_locked"):');lines.append('        jump r13_v111_medicine_missing12');lines.append('    if not r13_v111_value("warm_seat_ready"):');lines.append('        jump r13_v111_seat_missing12');goto('carrier_missing12')
label('medicine_missing12');late(s,34,35);goto('morning_prep12_entry')
label('seat_missing12');late(s,36,37);goto('morning_prep12_entry')
label('carrier_missing12');late(s,38,39);goto('morning_prep12_entry')
label('prevent_ready12');late(s,41,42);goto('early12')
label('stay_meal12');late(s,26,27);goto('premeal12')
label('take_daram12');setv('route12','late_exposure');late(s,28,30);setv('DARAM_location','with_father');goto('pickup12')
label('leave_daram12');setv('route12','late_exposure');late(s,31,33);setv('DARAM_location','school');setv('busy:nabi','daram_guard');goto('pickup12')
label('pickup12');travel('facility','pickup12');arrive(['mom']);lines.append('    if r13_v111_value("DARAM_location")=="with_father":');lines.append('        $ r13_v111_arrive(["mom","daram"])');goto('pickup_box12')
field('pickup_box12','facility',['mom'],'blankets','준비된 온기 상자를 인수한다','pickup_done12')
label('pickup_done12');setv('heat_box_received',True);goto('late_meal12')
s='MS14_D12_S03';start(s,'school','late_meal12',['daram','nabi','resident_bori','resident_teacher','kid_saemi'],2);setv('busy:nabi',False);late(s,1,11);setv('medical_called',True);setv('busy:resident_bori','medical_call');goto('soup_fragment12')
field('soup_fragment12','school',['nabi','resident_teacher'],'stove','작은 냄비의 남은 수프를 보존한다','fragment_seen12')
label('fragment_seen12');late(s,12,20);setv('soup_fragment_observed',True);goto('soup_hearing12')
s='MS14_D12_A';start(s,'school','premeal12',['daram','nabi','resident_teacher','resident_bori','kid_dodam','kid_saemi'],1);setv('route12','premeal_stopped');late(s,1,10);setv('medical_called',True);setv('busy:resident_bori','medical_call');setv('soup_fragment_observed',True);goto('soup_hearing12')
observation('E12_FRAGMENT','냄비 파편과 병 입구','작은 냄비에 남은 파편과 병 입구의 비대칭 경계 두 곳, 제조 이음선을 대조했다. 내용물의 성분을 입증하지 않는다.')
observation('E12_SEAL','준비 때 온전했던 개봉 봉인','배식 준비 때 선생님이 받은 병의 마개와 목을 잇는 개봉 봉인은 끊어지지 않았다.')
observation('E12_HANDLING','작은 냄비의 인계·관찰 구간','나비가 큰 냄비에서 나누어 작은 냄비를 직접 건넸다. 교사의 얼굴과 상체는 보였지만 손은 가림판 뒤라 투입 장면은 보지 못했다. 확인한 구간에 세척대 왕복은 없었다.')
s='MS14_D12_S04';start(s,'school','soup_hearing12',['daram','nabi','resident_teacher','resident_madam'],2);late(s,1,1)
lines.append('    if '+V('route12')+"=='late_exposure':");lines.append('        call r13_v111_meal_observations12');goto('bottle_match12')
label('meal_observations12');late(s,2,13);lines.append('    return')
field('bottle_match12','school',['nabi','resident_teacher'],'desks','병과 파편의 경계를 대조한다','bottle_matched12')
label('bottle_matched12');late(s,14,21);grant('E12_FRAGMENT','fragment_comparison12');grant('E12_SEAL','original_seal_recalled12');goto('seal_proof12')
proof('seal_proof12','재사용 설명과 개봉 봉인을 대조한다',['E12_FRAGMENT','E12_SEAL'],'seal_answer12','medicine_wrong12','soup_hint12')
branch('seal_answer12',V('route12')+"=='late_exposure'",'seal_late12','seal_pre12')
label('seal_late12');late(s,22,27);goto('handling12')
label('seal_pre12');late(s,62,67);goto('handling12')
label('handling12');late(s,28,28);branch('handling_route12',V('route12')+"=='late_exposure'",'handling_late12','handling_pre12')
label('handling_late12');late(s,29,40);goto('medical_arrival12')
label('handling_pre12');late(s,68,79);late(s,94,95);goto('medical_arrival12')
label('medical_arrival12');late(s,41,46);arrive(['daram','nabi','resident_teacher','resident_seori','resident_bori','guard','neoul']);setv('busy:resident_bori',False);setv('medical_arrived',True);grant('E12_HANDLING','handling_observed12');goto('soup_final12')
proof('soup_final12','파편·봉인·취급 구간을 함께 제시한다',['E12_FRAGMENT','E12_SEAL','E12_HANDLING'],'soup_conclusion12','fragment_wrong12','soup_hint_final12')
label('soup_conclusion12');late(s,47,47);branch('soup_conclusion_route12',V('route12')+"=='late_exposure'",'conclusion_late12','conclusion_pre12')
label('conclusion_late12');late(s,48,56);goto('confessed12')
label('conclusion_pre12');late(s,80,88);goto('confessed12')
label('confessed12');late(s,57,61);setv('teacher_confessed',True);branch('soup_after_route12',V('route12')+"=='late_exposure'",'aftermath_late12','aftermath_pre12')
for key,a,b,target in [('medicine_wrong12',89,90,'seal_proof12'),('fragment_wrong12',91,92,'soup_final12'),('soup_hint12',93,93,'seal_proof12'),('soup_hint_final12',93,93,'soup_final12')]:label(key);late(s,a,b);goto(target)
label('aftermath_pre12');late(s,96,102);select([('돌목에게 감독을 맡긴다','teacher_guard_pre12',None),('너울에게 신병을 넘긴다','teacher_neoul_pre12',None)])
label('teacher_guard_pre12');late(s,103,104);goto('soup_pre_close12')
label('teacher_neoul_pre12');late(s,105,108);goto('soup_pre_close12')
label('soup_pre_close12');s='MS14_D12_A';lines.append('    if r13_v111_value("school_heat_connected"):');lines.append('        call r13_v111_pre_lights12');lines.append('    else:');lines.append('        call r13_v111_pre_no_lights12');goto('sleep12')
label('pre_lights12');late(s,23,23);lines.append('    return')
label('pre_no_lights12');arrive(['mom','daram','nabi','resident_teacher','guard','neoul']);late('MS14_D12_S05',27,28);lines.append('    return')
s='MS14_D12_S05';start(s,'school','aftermath_late12',['daram','nabi','resident_teacher','resident_seori','resident_bori','guard','neoul'],2);late(s,1,12)
lines.append('    if '+V('school_heat_connected')+':');lines.append('        call r13_v111_lights12');lines.append('    else:');lines.append('        call r13_v111_no_lights12')
late(s,43,43);late(s,17,20)
lines.append('    if '+V('school_heat_connected')+':');lines.append('        call r13_v111_child_light12');lines.append('    else:');lines.append('        call r13_v111_child_dark12');late(s,30,31)
select([('돌목에게 감독을 맡긴다','teacher_guard_late12',None),('너울에게 신병을 넘긴다','teacher_neoul_late12',None)])
label('teacher_guard_late12');late(s,32,33);goto('sleep12')
label('teacher_neoul_late12');late(s,34,37);goto('sleep12')
for key,a,b in [('lights12',13,16),('no_lights12',27,28),('child_light12',21,26),('child_dark12',39,42)]:
 label(key)
 if key in ('lights12','no_lights12'):arrive(['daram','mom','nabi','resident_teacher','resident_seori','resident_bori','guard','neoul'])
 late(s,a,b);lines.append('    return')
s='MS14_D12_B';start(s,'school','early12',['daram','mom','nabi','resident_teacher','karo','kid_dodam','kid_saemi'],2);late(s,1,14);setv('route12','early_prevented');setv('school_heat_connected',True);setv('busy:karo',False);goto('sleep12')
finish_day('sleep12',13,'day13')
# DAY 13 — fixed blanket identity, actual passengers, sequential handovers.
s='MS14_D13_S01';start(s,'school','day13',['mom','daram','npc_pandol','karo']);setv('busy:karo',False);late(s,1,9);goto('blanket_mend13')
field('blanket_mend13','school',['mom','daram','npc_pandol','karo'],'blankets','회색 담요를 실제로 수선한다','blanket_mended13')
label('blanket_mended13');late(s,10,23);setv('pandol_blanket_mended',True)
observation('E13_ORDER','중지된 이송 명령 사본','돌목이 가족 한 사람만 제외하는 대신 현재 이송 명령 전체의 중지를 적었다. 입구 인수도 중지하며 기존 감독 기록은 보존한다.')
observation('E13_MENDING','오늘 아침 회색 담요 수선','학교 문 옆 정리대에서 아빠가 벌어진 회색 담요에 새 무늬 천을 꿰맸다. 다람이 천을 잡았고 까로가 판돌에게 둘러 주었다. 가족 침구와 다른 담요다.')
grant('E13_MENDING','actual_blanket_mending13');lines.append('    if r13_v111_value("teacher_custody")=="guard":');lines.append('        jump r13_v111_teacher_relief13');goto('gate_bench13')
label('teacher_relief13');arrive(['mom','daram','guard','resident_teacher','v111_patrol']);goto('teacher_relief_check13')
talk('teacher_relief_check13','school',['mom','daram','guard','resident_teacher','v111_patrol'],'guard','초소로 가기 전 교사 감독 교대를 확인한다','teacher_relief_done13')
label('teacher_relief_done13');setv('busy:v111_patrol','teacher_supervision');setv('teacher_supervisor','v111_patrol');setv('busy:guard',False);goto('gate_bench13')
s='MS14_D13_S02';start(s,'gate','gate_bench13',['mom','daram','guard']);late(s,1,11);travel('square','cart_arrival13');arrive(['mom','daram','npc_pandol','resident_ppul','neoul','karo','guard']);late(s,12,28);goto('offer13')
label('offer13');select([('조건을 더 묻는다','offer_question13',None),('가족 셋이 수락하고 물러난다','offer_accept13',V('family_offer_terms_seen')),('거절하고 현장에 남는다','offer_refuse13',V('family_school_place'))])
label('offer_question13');late(s,29,32);setv('family_offer_terms_seen',True);goto('offer13')
label('offer_accept13');late(s,38,39);setv('family_deal',True);goto('family_exit13')
label('offer_refuse13');late(s,33,35);setv('family_deal',False);goto('blanket_lie13')
s='MS14_D13_S03';start(s,'square','blanket_lie13',['mom','daram','npc_pandol','resident_ppul','guard','karo']);late(s,1,17);goto('mending_proof13')
proof('mending_proof13','아내가 봤다는 담요의 시점을 확인한다',['E13_MENDING'],'mending_answer13','mending_wrong13','mending_hint13')
label('mending_answer13');late(s,18,40);setv('false_message_admitted',True);goto('cart_inspect13')
label('mending_wrong13');late(s,43,44);goto('mending_proof13')
label('mending_hint13');late(s,45,45);goto('mending_proof13')
field('cart_inspect13','square',['mom','daram','karo','guard'],'cart','실제 탑승자와 하차 준비를 확인한다','cart_observed13')
label('cart_observed13');setv('cart_roster',['npc_pandol','resident_momo','resident_guldol'])
lines.append('    if r13_v111_value("silluk_status")=="supervised_compulsory_labor" and r13_v111_person_alive("resident_siluk"):');lines.append('        call r13_v111_silluk_board_observation13')
lines.append('    if r13_v111_value("teacher_transfer")=="listed" and r13_v111_person_alive("resident_teacher"):');lines.append('        call r13_v111_teacher_board_observation13');goto('stop_cart13')
# Reuse the existing approved cart observations (room13_ep6_cart.rpy:254–255),
# not an inference that a listed person is already aboard on day12.
label('teacher_board_observation13');setv('location:resident_teacher','square');lines.append('    call r13_lines([(None,"사자 선생님이 출석부를 품에 안고 앉아 있었다.",{"show":"resident_teacher","pose":"collapse_attendance"})],"v111:teacher_actual_cart_observation")');code('r13_v111_set("teacher_transfer","aboard")');code('r13_v111_set("cart_roster",r13_v111_value("cart_roster")+["resident_teacher"])');lines.append('    return')
label('silluk_board_observation13');setv('location:resident_siluk','square');lines.append('    call r13_lines([(None,"짐칸 끝에 실룩. 고개를 숙이고 있었다.")],"v111:silluk_actual_cart_observation")');code('r13_v111_set("silluk_transfer","aboard")');code('r13_v111_set("cart_roster",r13_v111_value("cart_roster")+["resident_siluk"])');lines.append('    return')
s='MS14_D13_S04';start(s,'square','stop_cart13',['mom','daram','karo','guard','resident_badook','npc_pandol','resident_momo','resident_guldol','resident_ppul','neoul'],2);late(s,1,6);setv('cart_stopped',True);setv('stop_actor','resident_badook');setv('busy:resident_badook','stop_cart');code('r13_v111_set("cart_roster",r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"])');late(s,10,14);goto('family_position13')
label('family_position13');select([('곁에 남는다','family_stay13',None),('까로와 학교로 간다','family_karo13','not '+V('busy:karo')),('네로와 학교로 간다','family_nero13',V('nero_alive')+' and not '+V('busy:resident_nero')+' and r13_v111_actor_ready("resident_nero")')])
label('family_stay13');late(s,63,64);setv('family_location','square');setv('busy:mom','daram_guard');goto('handover_plan13')
label('family_karo13');late(s,56,59);setv('family_location','moving_to_school');setv('location:mom','on_way_school');setv('location:daram','on_way_school');setv('location:karo','on_way_school');setv('busy:karo','family_walk');goto('family_walk_karo13')
label('family_nero13');arrive(['mom','daram','resident_nero','karo','guard','resident_badook']);late(s,60,62);lines.append('    hide r13_visitor');code('renpy.pause(.35)');setv('family_location','school');setv('location:mom','school');setv('location:daram','school');setv('location:resident_nero','school');setv('busy:mom','daram_guard');setv('busy:resident_nero','daram_guard');arrive(['karo','guard','resident_badook']);goto('handover_plan13')
label('family_walk_karo13');lines.append('    hide r13_visitor');code('renpy.pause(.35)');setv('location:mom','school');setv('location:daram','school');setv('busy:mom','daram_guard');setv('family_location','school');setv('busy:karo',False);arrive(['karo','guard','resident_badook']);lines.append('    call r13_lines([(None,"잠시 뒤, 까로가 혼자 광장으로 돌아왔다.",{"show":"karo","no_lead":True})],"v111:family_escort_return13")');goto('handover_plan13')
label('handover_plan13');lines.append('    if room13["v111"].get("scene")!="MS14_D13_S04":');lines.append('        $ r13_v111_scene("MS14_D13_S04")');lines.append('        $ room13["v111"]["music_hold"]="MS14_D13_S04"');lines.append('        $ renpy.music.stop(fadeout=.15)');lines.append('        $ r13_v111_score()');select([('학교 침상과 인수를 먼저 확인한다','school_handover_prep13',None),('하차한 사람부터 부축한다','pandol_down13',V('handover_prepared13')),('보온·감독 아래 인계를 기다린다','partial13',None),('검증한 기록을 공개한다','crowd13',V('false_message_admitted')+' and not '+V('crowd_resolution_done'))])
label('school_handover_prep13');travel('school','handover_prep13');arrive(['nabi','karo']);goto('nabi_beds13')
talk('nabi_beds13','school',['nabi','karo'],'nabi','침상과 인수를 부탁합니다.','beds_ready13')
label('beds_ready13');setv('handover_prepared13',True);setv('busy:karo',False);travel('square','beds_ready13');arrive(['guard','karo','resident_badook']);goto('handover_plan13')
label('pandol_down13');arrive(['guard','karo','resident_badook','npc_pandol']);lines.append('    if r13_v111_value("family_location")=="square":');lines.append('        $ r13_v111_arrive(["guard","karo","resident_badook","npc_pandol","mom","daram"])');late(s,15,19);travel('school','pandol_school13');arrive(['nabi','karo','npc_pandol']);late(s,20,23);setv('handed:npc_pandol',True)
observation('E13_HANDOVER','판돌의 학교 인수 기록','실제 발판으로 내려 부축한 판돌을 학교 침상에서 나비가 인수했다. 수레 정지만으로 인수 완료를 기록하지 않았다.')
grant('E13_HANDOVER','pandol_actual_school_handover');goto('momo_transport13')
label('momo_transport13');travel('square','momo_transport13');arrive(['karo','guard','resident_badook','resident_momo']);goto('momo_down13')
field('momo_down13','square',['karo','guard','resident_badook','resident_momo'],'cart','모모를 발판으로 부축한다','momo_school13')
label('momo_school13');late(s,65,67);travel('school','momo_school13');arrive(['nabi','karo','resident_momo']);late(s,68,68);setv('handed:resident_momo',True);goto('guldol_transport13')
label('guldol_transport13');travel('square','guldol_transport13');arrive(['karo','guard','resident_badook','resident_guldol']);goto('guldol_down13')
field('guldol_down13','square',['karo','guard','resident_badook','resident_guldol'],'cart','굴돌을 발판으로 부축한다','guldol_school13')
label('guldol_school13');late(s,69,70);travel('school','guldol_school13');arrive(['nabi','karo','resident_guldol']);late(s,71,71);setv('handed:resident_guldol',True);goto('last_cart13')
label('last_cart13');travel('square','last_cart13',[]);arrive(['karo','resident_badook','resident_ppul']);lines.append('    if "resident_teacher" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_teacher"):');lines.append('        jump r13_v111_teacher_transport13');lines.append('    if "resident_siluk" in r13_v111_value("cart_roster") and not r13_v111_value("handed:resident_siluk"):');lines.append('        jump r13_v111_silluk_transport13');lines.append('    if r13_v111_value("family_location")=="square":');lines.append('        call r13_v111_family_still_here13');lines.append('    else:');lines.append('        call r13_v111_family_already_school13');lines.append('    if not all(r13_v111_value("handed:"+p) for p in r13_v111_value("cart_roster")):');lines.append('        jump r13_v111_partial13');late(s,39,42);setv('all_cart_handed',True);setv('busy:resident_badook',False);setv('outcome13','all_rescued');goto('transport_cleanup13')
label('family_still_here13');arrive(['karo','resident_badook','resident_ppul','mom','daram']);late(s,33,35);lines.append('    return')
label('family_already_school13');late(s,37,37);late(s,88,88);late(s,38,38);lines.append('    return')
# The original supervisory destinations are retained for any real extra
# passengers. Merely being listed never adds a person to the actual roster.
label('teacher_transport13');arrive(['karo','guard','resident_badook','resident_teacher','neoul']);goto('teacher_down13')
field('teacher_down13','square',['karo','guard','resident_badook','resident_teacher','neoul'],'cart','교사를 분리된 감독 자리로 옮긴다','teacher_supervised13')
label('teacher_supervised13');late(s,72,74);travel('v111_supervised','teacher_supervised13',[]);arrive(['karo','resident_teacher','neoul']);goto('teacher_receipt13')
talk('teacher_receipt13','v111_supervised',['karo','resident_teacher','neoul'],'neoul','분리된 감독 자리의 인수를 확인한다','teacher_received13')
label('teacher_received13');setv('handed:resident_teacher',True);setv('teacher_transfer','handed_over');setv('busy:neoul','teacher_supervision');goto('last_cart13')
label('silluk_transport13');arrive(['karo','guard','resident_badook','resident_siluk']);goto('silluk_supervision13')
talk('silluk_supervision13','square',['karo','guard','resident_badook','resident_siluk'],'guard','하차 전 감독 교대를 확인합니다.','silluk_down13')
label('silluk_down13');late(s,8,9);late(s,25,26);lines.append('    if r13_v111_value("family_location")=="square":');lines.append('        call r13_v111_silluk_family13');late(s,30,32);late(s,75,77);travel('v111_labor','silluk_down13',[]);arrive(['karo','guard','resident_siluk']);goto('silluk_receipt13')
label('silluk_family13');arrive(['karo','guard','resident_badook','resident_siluk','mom','daram']);late(s,28,29);lines.append('    return')
talk('silluk_receipt13','v111_labor',['karo','guard','resident_siluk'],'guard','원래 감독 장소의 인수를 확인한다','silluk_received13')
label('silluk_received13');setv('handed:resident_siluk',True);setv('silluk_transfer','handed_over');setv('busy:guard','silluk_supervision');goto('last_cart13')
wait('transport_cleanup13','square',['karo','guard','resident_badook'],[
 person('앞으로의 호송을 확인한다','square','resident_badook'),person('명령 전체를 중지해 주십시오.','square','guard'),person('강제 운반을 맡지 않을 거지?','square','karo'),person('빈 수레 반환을 요청한다.','square','karo'),person('중지 명령을 직접 전달한다.','square','guard'),dict(title='학교로 돌아간다',location='school',move='school'),person('내일 고정부 작업과 공구를 부탁합니다.','workshop','buri')],['escort_refuse13','order_stop13','driver_refuse13','cart_return13','relay_stop13','night_finish13','buri_tools13'])
label('escort_refuse13');late(s,43,45);setv('actual_stop_actor_refuses_transport',True);goto('transport_cleanup13')
label('order_stop13');late(s,47,47);late(s,80,81);setv('current_order_execution_stopped',True);grant('E13_ORDER','actual_stopped_order13');goto('transport_cleanup13')
label('driver_refuse13');late(s,48,48);late(s,82,83);setv('Kkaro_forced_transport_refused',True);goto('transport_cleanup13')
label('cart_return13');arrive(['karo','guard','resident_badook','resident_eunho']);late(s,49,49);late(s,84,86);setv('cart_returned',True);setv('escort_gear_returned',True);goto('transport_cleanup13')
label('relay_stop13');lines.append('    if r13_v111_value("busy:neoul")=="teacher_supervision":');lines.append('        jump r13_v111_relay_supervised13');arrive(['neoul','guard']);goto('relay_present13')
label('relay_supervised13');travel('v111_supervised','relay_supervised13',[]);arrive(['neoul','resident_teacher']);goto('relay_present13')
label('relay_present13');lines.append('    call screen r13_book("neoul",present=True)');lines.append('    if _return=="V111:E13_ORDER" and r13_v111_owned("E13_ORDER"):');lines.append('        jump r13_v111_relay_confirmed13');lines.append('    if _return:');lines.append('        $ renpy.notify("중지 명령 사본을 직접 보여 줘야 한다.")');goto('transport_cleanup13')
label('relay_confirmed13');late(s,50,50);setv('relay_stopped',True);goto('transport_cleanup13')
label('buri_tools13');arrive(['buri']);lines.append('    call r13_lines([(None,"부리가 공구와 받침을 챙겼다. 내일 현장에 함께 가겠다고 했다.")],"v111:buri_tools_consent13")');setv('buri_device_consent',True);goto('transport_cleanup13')
label('night_finish13');code('r13_v111_set("current_transport_chain_stopped",all(r13_v111_value(k) for k in ["actual_stop_actor_refuses_transport","current_order_execution_stopped","Kkaro_forced_transport_refused","cart_returned","escort_gear_returned","relay_stopped"]))');goto('sleep13')
s='MS14_D13_A';start(s,'square','family_exit13',['mom','daram','guard','karo'],2);late(s,1,8);travel('gate','family_gate13');arrive(['mom','daram','guard','karo']);late(s,9,18);setv('family_benefits_received',True);setv('night14_lodging','gate');setv('outcome13','family_priority');setv('departed_unrescued',True);goto('sleep13')
s='MS14_D13_B';start(s,'square','partial13',['karo','guard','resident_badook'],2);late(s,1,10);setv('outcome13','partial_rescue');setv('cart_stopped',True);setv('pending_handover_supervised',True);goto('sleep13')
s='MS14_D13_C';start(s,'square','crowd13',['guard','karo','resident_badook','neoul'],2);late(s,1,4)
lines.append('    if '+V('family_location')+"=='square':");lines.append('        call r13_v111_daram_crowd13')
select([('너울 앞을 막는다','crowd_block13',None),('현장 감독자에게 보호를 맡긴다','crowd_guard13','not '+V('busy:guard')),('막지 않는다','crowd_watch13',None)])
label('daram_crowd13');arrive(['mom','daram','guard','karo','neoul','resident_badook']);late(s,5,7);lines.append('    return')
label('crowd_block13');late(s,8,16);setv('crowd_resolution_done',True);setv('crowd_injury',False);setv('crowd_intervention','success');setv('outcome13','all_rescued');goto('handover_plan13')
label('crowd_guard13');late(s,17,18);setv('crowd_resolution_done',True);setv('crowd_injury',False);setv('outcome13','all_rescued');goto('handover_plan13')
label('crowd_watch13');late(s,19,20);setv('crowd_resolution_done',True);setv('crowd_injury',True);setv('crowd_intervention','none');setv('outcome13','crowd_violence');goto('sleep13')
# Explicit failed intervention retained for genuine failed input results only.
label('crowd_failed13');late(s,21,23);setv('crowd_resolution_done',True);setv('crowd_injury',True);setv('crowd_intervention','failed');setv('outcome13','crowd_violence');goto('sleep13')
label('sleep13');lines.append('    if r13_v111_value("outcome13")=="family_priority":');lines.append('        jump r13_v111_sleep13_gate');lines.append('    if r13_v111_value("family_location")=="square":');lines.append('        call r13_v111_collect_family13');travel('school','sleep13',['mom','daram']);setv('family_location','school');setv('busy:mom',False);arrive(['mom','daram','nabi']);goto('sleep13_input')
label('collect_family13');travel('square','collect_family13',[]);arrive(['mom','daram']);lines.append('    return')
label('sleep13_gate');travel('gate','sleep13_gate',['mom','daram']);arrive(['mom','daram','guard']);goto('sleep13_gate_input')
talk('sleep13_gate_input','gate',['mom','daram','guard'],'guard','가족 세 사람의 오늘 밤 자리를 확인한다','morning14')
field('sleep13_input','school',['mom','daram','nabi'],'blankets','오늘 밤 자리를 확인한다','morning14')
label('morning14');setv('day',14);goto('day14')
# DAY 14 — preserve the previous day's actual outcome; no resurrection/transport.
label('day14')
select([('가족이 머무는 자리를 확인한다','ending_dispatch14',None)])
label('ending_dispatch14')
lines.extend(['    if '+V('outcome13')+"=='family_priority':",'        jump r13_v111_family_ending14','    if '+V('outcome13')+"=='partial_rescue':",'        jump r13_v111_partial_ending14','    if '+V('crowd_injury')+':','        jump r13_v111_violence_ending14']);goto('morning_safe14')
s='MS14_D14_S01';start(s,'school','morning_safe14',['mom','daram','npc_pandol','nabi']);late(s,1,18);goto('altar_guide14')
talk('altar_guide14','school',['mom','daram','resident_badook'],'resident_badook','제단 접근로를 확인해 주십시오.','altar_ready14')
label('altar_ready14');setv('altar_guide_confirmed',True);setv('busy:resident_badook',False);goto('altar14')
s='MS14_D14_S02';start(s,'altar','altar14',['mom','daram','resident_badook','karo'],1);late(s,1,10);setv('altar_heat_structure_observed',True);goto('mayor_interview14')
label('mayor_interview14');travel('gate','mayor_interview14');arrive(['mom','resident_ppul','resident_badook','karo']);late(s,11,23);setv('mayor_false_invitation_admitted',True)
lines.append('    if '+V('dallae_first_victim_known')+':');lines.append('        call r13_v111_dallae14');goto('device14')
label('dallae14');late(s,24,28);lines.append('    return')
label('device14');lines.append('    if r13_v111_value("buri_device_consent") and not r13_v111_value("mayor_site_decided") :');lines.append('        jump r13_v111_mayor_site_request14');travel('altar','device14');arrive(['mom','daram','karo','resident_badook']);late(s,29,30);lines.append('    if r13_v111_value("mayor_site_joined") and r13_v111_person_alive("buri"):');lines.append('        call r13_v111_buri_work_start14');goto('device_record14')
wait('mayor_site_request14','gate',['mom','daram','resident_ppul','resident_badook','karo'],[person('감독 아래 현장 확인에 동행해 주십시오.','gate','resident_ppul'),person('이 자리에서만 확인하겠습니다.','gate','resident_ppul')],['mayor_site_yes14','mayor_site_no14'])
label('mayor_site_yes14');setv('mayor_site_decided',True);setv('mayor_site_joined',True);goto('device14')
label('mayor_site_no14');setv('mayor_site_decided',True);setv('mayor_site_joined',False);goto('device14')
label('buri_work_start14');arrive(['mom','daram','buri','resident_ppul','resident_badook','karo']);late(s,31,34);lines.append('    if r13_v111_value("madam_observer_consent"):');lines.append('        call r13_v111_madam_device_question14');late(s,42,43);setv('buri_device_present',True);lines.append('    return')
label('madam_device_question14');late(s,35,41);lines.append('    return')
label('madam_device_close14');late(s,60,61);lines.append('    return')
# Existing notebook presentation, either actual record suffices; no fabricated
# supply receipt if the player never delivered/connected the school equipment.
label('device_record14');lines.append('    call screen r13_book("dad",present=True)');lines.extend(['    if _return=="V111:E13_HANDOVER" and r13_v111_owned("E13_HANDOVER"):', '        jump r13_v111_device_rescue14','    if _return=="V111:E14_SUPPLY" and r13_v111_owned("E14_SUPPLY") and r13_v111_value("school_heat_connected"):', '        jump r13_v111_device_supply14']);lines.append('    if _return:');lines.append('        $ renpy.notify("실제 인수한 구조 기록이나 연결·사용을 확인한 물자 기록이 필요하다.")');goto('device_pause14')
field('device_pause14','altar',['mom','daram','karo','resident_badook'],'valve','장치를 살피며 기록을 다시 확인한다','device_record14')
label('device_rescue14');setv('device_record_kind','rescue');late(s,81,83);setv('device_record_shown',True);goto('device_worker14')
label('device_supply14');setv('device_record_kind','supply');late(s,78,80);setv('device_record_shown',True);goto('device_worker14')
label('device_worker14');lines.append('    if r13_v111_value("buri_device_present"):');lines.append('        jump r13_v111_buri_record_answer14');arrive(['mom','daram','karo','resident_badook']);late(s,51,54);setv('busy:karo','device_support');setv('device_support_ready',True);goto('device_order14')
label('device_order14');travel('gate','device_order14');arrive(['mom','resident_ppul','resident_badook','karo']);setv('busy:karo',False);late(s,74,77);lines.append('    if r13_v111_value("madam_observer_consent"):');lines.append('        call r13_v111_madam_device_close14');setv('command_confrontation_done',True);travel('altar','device_work14');arrive(['mom','daram','karo','resident_badook']);setv('busy:karo','device_support');goto('device_detach14')
field('device_detach14','altar',['mom','daram','karo','resident_badook'],'valve','기록한 고정부를 안전하게 분리한다','device_detached14')
label('device_detached14');late(s,62,65);setv('device_detached',True);setv('busy:karo',False);setv('busy:buri',False);lines.append('    if r13_v111_value("busy:guard")=="silluk_supervision":');lines.append('        jump r13_v111_guard_relief14');goto('device_school14')
label('guard_relief14');travel('v111_labor','guard_relief14',[]);code('r13_v111_set("guard_relief_person","neoul" if r13_v111_value("busy:v111_patrol")=="teacher_supervision" else "v111_patrol")');code('r13_v111_arrive(["guard","resident_siluk",r13_v111_value("guard_relief_person")])');goto('guard_relief_check14')
talk('guard_relief_check14','v111_labor',['guard','resident_siluk','v111_patrol'],'guard','학교 인수 동안의 감독 교대를 확인합니다.','guard_relieved14')
label('guard_relieved14');code('r13_v111_set("busy:"+r13_v111_value("guard_relief_person"),"silluk_supervision")');setv('busy:guard',False);goto('device_school14')
label('device_school14');travel('school','device_school14');arrive(['mom','daram','karo','nabi','guard']);late(s,66,68);goto('device_lock14')
field('device_lock14','school',['mom','daram','karo','nabi','guard'],'blankets','부품·기록판·열쇠 인수를 확인한다','device_locked14')
label('device_locked14');late(s,69,69);setv('device_joint_control',True);goto('granny_interview14')
# Optional approved Buri worker path remains conditional on consent and presence;
# no gratitude line is borrowed when the family chose the alternative worker.
label('buri_record_answer14');arrive(['mom','daram','buri','resident_ppul','resident_badook','karo']);lines.append('    if r13_v111_value("device_record_kind")=="supply" and r13_v111_value("buri_supply_participated"):');lines.append('        call r13_v111_buri_supply_answer14');lines.append('    else:');lines.append('        call r13_v111_buri_no_transport_answer14');late(s,55,59);lines.append('    if r13_v111_value("madam_observer_consent"):');lines.append('        call r13_v111_madam_device_close14');setv('command_confrontation_done',True);setv('busy:buri','device_work');setv('device_support_ready',True);goto('device_detach14')
label('buri_supply_answer14');late(s,45,50);lines.append('    return')
label('buri_no_transport_answer14');late(s,84,85);lines.append('    return')
s='MS14_D14_S03';start(s,'gate','granny_interview14',['mom','daram','granny','guard','resident_tosil'],1);late(s,1,11);goto('tosil_listen14')
label('tosil_listen14');select([('안에서 직접 듣는다','tosil_inside14',None),('보호자와 밖에서 기다린다','tosil_outside14',None)])
label('tosil_inside14');setv('tosil_listen','inside');late(s,12,35);setv('bomi_death_confirmed',True);setv('adult_interview_done',True);late(s,36,36);goto('name_board14')
label('tosil_outside14');setv('tosil_listen','outside');setv('location:resident_tosil','outside_guard');late(s,18,24);late(s,30,32);setv('bomi_death_confirmed',True);setv('adult_interview_done',True);late(s,36,39);goto('name_board14')
s='MS14_D14_S04';start(s,'square','name_board14',['mom','daram','resident_tosil','npc_pandol'],2);late(s,1,2)
select([('토실이 이름을 쓰겠다면 기다린다','tosil_name14',None),('지금 쓰지 않아도 된다고 말한다','tosil_no_name14',None)])
label('tosil_name14');late(s,3,7);goto('pandol_news14')
label('tosil_no_name14');s='MS14_D14_S03';late(s,40,41);goto('pandol_news14')
s='MS14_D14_S04';label('pandol_news14');late(s,8,15);travel('school','supply_display14');arrive(['mom','daram','nabi','guard']);goto('supply_inventory14')
field('supply_inventory14','school',['mom','daram','nabi','guard'],'stove','실물·사용처·남은 양을 함께 확인한다','supply_inventory_done14')
label('supply_inventory_done14');late(s,16,21);lines.append('    if r13_v111_actor_ready("resident_madam"):');lines.append('        call r13_v111_madam_inventory14');late(s,24,28);setv('school_inventory_checked',True);setv('school_supply_handed',True);setv('school_heat_connected',True);code('r13_v111_set("current_sacrifice_operation_closed",bool(r13_v111_value("current_transport_chain_stopped") and r13_v111_value("device_joint_control")))');goto('lamp_assignment14')
label('madam_inventory14');late(s,22,23);lines.append('    return')
label('lamp_assignment14');arrive(['mom','daram','nabi','guard','resident_lamplighter']);lines.append('    if r13_v111_actor_ready("resident_lamplighter"):');lines.append('        call r13_v111_chorong_lamps14');lines.append('    else:');lines.append('        call r13_v111_mother_lamps14');lines.append('    if '+V('OWL_ALIVE')+':');lines.append('        call r13_v111_owl_alive14')
lines.append('    if not (r13_v111_value("current_transport_chain_stopped") and r13_v111_value("device_joint_control")):');lines.append('        call r13_v111_unfinished_operation14');goto('cookie14')
label('chorong_lamps14');late(s,29,31);setv('lamp_manager','resident_lamplighter');lines.append('    return')
label('mother_lamps14');late(s,32,32);setv('lamp_manager','mom');lines.append('    return')
label('owl_alive14');arrive(['mom','daram','nabi','guard','resident_owlgp']);late(s,33,34);lines.append('    return')
label('unfinished_operation14');late(s,35,36);lines.append('    return')
s='MS14_D14_END_FAMILY';start(s,'gate','family_ending14',['mom','daram','guard']);late(s,1,11);goto('family_lodging14')
s='MS14_D14_END_PARTIAL';start(s,'square','partial_ending14',['karo','guard','resident_badook']);late(s,1,8);goto('partial_handoff14')
field('partial_handoff14','square',['karo','guard','resident_badook'],'cart','남은 인계에 직접 참여한다','partial_work14')
label('partial_work14');code('v111_pending_patient=next((p for p in (r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"]) if not r13_v111_value("handed:"+p)),None)');goto('partial_patient14')
label('partial_patient14');travel('school','partial_patient14',[]);code('r13_v111_arrive(["mom","daram","nabi","karo","guard"]+([v111_pending_patient] if v111_pending_patient else []))');goto('partial_receipt14')
talk('partial_receipt14','school',['mom','daram','nabi','karo','guard'],'nabi','새로 난 침상의 인수를 확인한다','partial_received14')
label('partial_received14');lines.append('    if v111_pending_patient:');lines.append('        $ r13_v111_set("handed:"+v111_pending_patient,True)');code('v111_pending_rest=[p for p in (r13_v111_value("cart_roster") or ["npc_pandol","resident_momo","resident_guldol"]) if not r13_v111_value("handed:"+p)]')
lines.append('    if v111_pending_rest:');lines.append('        jump r13_v111_partial_wait14');late(s,9,11);setv('pending_handover_completed',True);goto('cookie14')
label('partial_wait14');travel('square','partial_wait14',[]);arrive(['karo','guard','resident_badook']);late(s,12,13);setv('pending_handover_completed',False);setv('pending_handover_supervised',True);goto('cookie14')
s='MS14_D14_END_VIOLENCE';start(s,'clinic','violence_ending14',['mom','daram','guard','resident_seori']);late(s,1,5)
lines.append('    if '+V('family_location')+"=='square':");lines.append('        call r13_v111_crowd_child_saw14');lines.append('    else:');lines.append('        call r13_v111_crowd_child_away14')
lines.append('    if '+V('crowd_intervention')+"=='failed':");lines.append('        call r13_v111_crowd_failed14');lines.append('    else:');lines.append('        call r13_v111_crowd_no_action14');late(s,19,19);goto('cookie14')
for key,a,b in [('crowd_child_saw14',6,7),('crowd_child_away14',8,12),('crowd_failed14',16,18),('crowd_no_action14',13,15)]:label(key);late(s,a,b);lines.append('    return')
s='MS14_D14_S05';label('family_lodging14');travel('gate','family_lodging14');arrive(['mom','daram','guard']);late(s,24,25);goto('cookie_gate14')
label('cookie14');travel('school','cookie14');arrive(['mom','daram']);setv('night14_lodging','school');goto('cookie_scene14')
label('cookie_gate14');arrive(['mom','daram']);setv('night14_lodging','gate');goto('cookie_scene14')
label('cookie_scene14');code('r13_edit(period=2)');code('r13_v111_scene('+q(s)+')');lines.append('    call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],"calm")');code('r13_v111_score()');late(s,1,14)
lines.append('    if '+V('crowd_injury')+':');lines.append('        call r13_v111_cookie_distance14')
late(s,15,23);setv('story14_completed',True);lines.append('    call screen r13_confirm("이야기를 마쳤습니다. 현재 진행을 저장할 수 있습니다.",yes="메인 화면으로",no="저장하기")');lines.append('    if not _return:');lines.append('        call screen save');lines.append('    return')
label('cookie_distance14');late(s,30,32);lines.append('    return')
bindings['morning_prep12']['people_by_location']={
 'school':['mom','daram','guard','resident_teacher'],
 'clinic':['resident_seori'],
 'square':['karo'],
 'store':['resident_madam'],
}
# Condition lambdas are generated from a closed, reviewed allowlist above.
lines+=['','init 315 python:','    R13_V111_ALLOWED={']
for rid,expression in allowed.items():lines.append('        '+q(rid)+':lambda: '+expression+',')
lines.append('    }')
# Replace single-item progression menus with normal native flow. The inventory
# decision remains only when the player really owns at least one blanket.
text='\n'.join(lines)+'\n'
text=text.replace("label r13_v111_day14:\n    menu:\n        '가족이 머무는 자리를 확인한다':\n            jump r13_v111_ending_dispatch14", "label r13_v111_day14:\n    jump r13_v111_ending_dispatch14")
text=text.replace("    menu:\n        '두 장을 꺼내 덮는다'", "    if r13_v111_value('carried_dry_blankets')==0:\n        jump r13_v111_coat_use11\n    menu:\n        '두 장을 꺼내 덮는다'",1)
(ROOT/'game/room13_v111_days1114.rpy').write_text(text)
(ROOT/'game/v111/records.json').write_text(json.dumps(DATA,ensure_ascii=False,indent=2)+'\n')
(ROOT/'game/v111/field-bindings.json').write_text(json.dumps(bindings,ensure_ascii=False,indent=2)+'\n')
