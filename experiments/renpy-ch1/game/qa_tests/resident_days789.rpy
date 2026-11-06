# 시작 상태만 준비하고 새 행동·대사, 실제 이동, 기존 획득 시점은 본편 라벨로 확인한다.
init python:
    def qa_resident789(day,route='murder',tok=True):
        r13_v111_set('day',day)
        r13_edit(day=day,location='gate',period=0)
        incident=(day!=7 and route=='murder')
        r13_v111_set('route7','uncommitted' if day==7 else route)
        r13_v111_set('OWL_ALIVE',not incident)
        r13_v111_set('DARAM_DETAINED',incident)
        r13_v111_set('location:daram','v111_custody' if incident else 'school' if day==7 else 'gate')
        r13_v111_set('DARAM_location','custody_room' if incident else 'school' if day==7 else 'with_dad')
        r13_v111_set('TOK_ALIVE',True)
        r13_v111_set('tok_workshop_present',tok)
        r13_v111_set('tok_hearing_present',not tok)


testcase resident7_teacher_and_bori:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,7)
    run Function(r13_grant,['V111:E06_FIRE'],'qa')
    run Function(r13_v111_scene,'MS14_D07_S01')
    run Function(r13_v111_set,'KKOMI_ALIVE',True)
    run Function(r13_v111_set,'FIRE_EVACUATED',True)
    run Jump('r13_v111_nubi_children_school7')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    pause until screen 'r13_hub' timeout 45
    click '선생님'
    click '선생님, 누비 씨 아이 셋을 맡아 주셨습니까?'
    click pos (900,600) until eval (r13_packet and '막내의 작은 대답을 듣고서야' in r13_packet[1].replace('\n',' ')) timeout 60
    assert eval (r13_v111_value('D07_S01_school_completed') is True and r13_v111_value('NUBI_CHILDREN_location')=='school')
    assert eval (not r13_v111_value('NUBI_admitted_setting_fire') and r13_v111_value('meeting:fire') is None)
    screenshot 'resident7_teacher.png'
    # 회의 뒤 아이 교실 상태를 별도로 준비한다. 위 인수만으로 자백·승리를 얻었다고 세지 않는다.
    run Function(r13_v111_set,'NUBI_admitted_setting_fire',True)
    run Function(r13_v111_set,'meeting:fire','win')
    run Function(r13_v111_scene,'MS14_D07_S02')
    run Function(r13_v111_arrive,['nabi','resident_bori','resident_teacher','kid_kkomi'])
    run Jump('r13_v111_school_names_done7')
    click pos (900,600) until eval (r13_packet and '나르는 거랑 안 깨는 건 달라' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('KKOMI_ALIVE') is True and not qa_nw_seen('꼬미가 앉았어야'))
    screenshot 'resident7_bori.png'


testcase resident7_nubi_admission:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,7)
    run Function(r13_grant,['V111:E06_FIRE'],'qa')
    run Function(r13_v111_set,'bori_nubi_door_witness_heard',True)
    run Jump('r13_v111_day7')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until screen 'choice' timeout 90
    run Jump('r13_v111_nubi_admission7')
    click pos (900,600) until eval (r13_packet and '가져간다고 안 했어요' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (not r13_v111_value('D07_S01_admission_completed') and not r13_v111_owned('E07_NUBI'))
    screenshot 'resident7_nubi.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    assert eval (r13_v111_value('NUBI_admitted_setting_fire') is True and r13_v111_value('NUBI_intent_to_kill')=='unproven')
    assert eval (r13_v111_owned('E07_NUBI'))


testcase resident8_custody_care:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,8)
    run Jump('r13_v111_custody8')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '소매를 정리할 자리를' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('DARAM_DETAINED') is True and r13_v111_value('OWL_ALIVE') is False)
    assert eval (not r13_v111_owned('E08_CHILD_ACCOUNT'))
    screenshot 'resident8_care.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E08_CHILD_ACCOUNT') and r13_v111_value('DARAM_DETAINED') is True)


testcase resident8_recovered_and_delivery:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,8,'prevented')
    run Function(r13_v111_set,'prevention','promise')
    run Jump('r13_v111_prevent_clinic8')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    if eval (renpy.get_screen('r13_map').scope['selected']!='room13'):
        click id 'r13_map_region_inn'
        click id 'map_room_room13'
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '그럼 제가 이쪽으로 갈게요' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('OWL_ALIVE') is True and r13_v111_value('DARAM_DETAINED') is False)
    screenshot 'resident8_owl.png'
    # 다음 오후 장면을 준비한 뒤 학교 인계·광장 이동·공개 길 부탁은 실제 화면을 누른다.
    run Jump('r13_v111_mother_letter8')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_region_village'
    keysym 'shift_K_UP'
    keysym 'shift_K_UP'
    keysym 'shift_K_UP'
    pause .5
    click id 'map_name_school'
    click id 'r13_map_travel'
    click pos (900,600) until screen 'r13_hub' timeout 60
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until screen 'r13_hub' timeout 90
    screenshot 'resident8_before_escort.png'
    click '오른쪽 구역' until '바둑이' timeout 20
    click '바둑이'
    click '공개 길 동행을 부탁합니다.'
    click pos (900,600) until eval (r13_packet and '봉투를 넣은 안주머니를 손바닥으로' in r13_packet[1].replace('\n',' ')) timeout 45
    assert eval (r13_v111_value('public_road_escort_completed') is True and not r13_v111_value('mother_warning_read8'))
    assert eval ('daram' not in room13['v111']['people'] and not r13_v111_actor_ready('daram'))
    screenshot 'resident8_delivery.png'
    click pos (900,600) until screen 'r13_hub' timeout 45
    assert eval (r13_v111_value('mother_warning_read8') is True and r13_v111_value('mother_secret_shared') is False)


testcase resident9_tok_and_postal:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,9)
    run Function(r13_grant,['V111:E09_PASSAGE'],'qa')
    run Jump('r13_v111_workshop9')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '물건부터 보겠습니다' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval ('resident_tok' in room13['v111']['people'] and not r13_v111_owned('E09_PIN_OWNER'))
    screenshot 'resident9_tok.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E09_PIN_OWNER') and r13_v111_value('DARAM_DETAINED') is True)
    run Jump('r13_v111_postal9')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until eval (r13_packet and '묶음을 맡긴 사람. 거기까지요' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('DARAM_DETAINED') is True and not r13_v111_value('mother_warning_shared9'))
    assert eval ('daram' not in room13['v111']['people'])
    screenshot 'resident9_postal.png'


testcase resident9_copy_route:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,9,'murder',False)
    run Function(r13_grant,['V111:E09_PASSAGE'],'qa')
    run Jump('r13_v111_workshop9')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    click id 'r13_map_travel'
    click pos (900,600) until eval (renpy.get_screen('r13_hub') and r13_v111_owned('E09_PIN_OWNER')) timeout 90
    assert eval (not qa_nw_seen('물건 보자면서 자꾸 저를 보시니까요') and r13_v111_value('tok_repair_copy_owned') is True)
    assert eval (r13_v111_value('tok_hearing_present') is True and r13_v111_value('DARAM_DETAINED') is True)
    screenshot 'resident9_copy.png'


testcase resident9_buri_passage:
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_resident789,9)
    run Jump('r13_v111_passage9')
    pause 1.0
    click '지도' until screen 'r13_map' timeout 30
    pause until eval renpy.get_screen('r13_map').scope['ready'] timeout 30
    if eval (renpy.get_screen('r13_map').scope['selected']!='kitchen'):
        click id 'r13_map_region_inn'
        click id 'map_room_kitchen'
    click id 'r13_map_travel'
    pause until screen 'r13_hub' timeout 45
    # 측정 시작 상태를 준비한 뒤 실제 본편의 질문·응답과 자료 생성 시점을 확인한다.
    run Jump('r13_v111_passage_walk9')
    click pos (900,600) until eval (r13_packet and '네가 물은 그대로 남겨 둘게' in r13_packet[1].replace('\n',' ')) timeout 90
    assert eval (r13_v111_value('DARAM_DETAINED') is True and r13_v111_value('OWL_ALIVE') is False)
    assert eval (not r13_v111_owned('E09_PASSAGE') and 'buri' in room13['v111']['people'] and 'daram' not in room13['v111']['people'])
    screenshot 'resident9_buri.png'
    click pos (900,600) until screen 'r13_hub' timeout 60
    assert eval (r13_v111_owned('E09_PASSAGE') and r13_v111_value('TTADAK_ALIVE') is True)
