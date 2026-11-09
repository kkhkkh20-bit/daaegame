init python:
    def qa_rest144_prepare():
        r13_v111_set('day',1)
        for key,value in R13_V111_ENTRY.get('MS14_D02_S01',([] ,{}))[1].items():r13_v111_set(key,value)
        r13_grant(['V111:'+key for key in R13_V111_ENTRY.get('MS14_D02_S01',([] ,{}))[0]],'검수 진입')
        r13_v111_set('ui_room_arrival_seen',True)
        r13_edit(day=1,location='room13',period=2)
        renpy.hide_screen('r13_evidence_found')

    def qa_rest144_remember():
        renpy.test.rest144_before=winter_copy.deepcopy(room13)

label qa_rest144_start:
    $ qa_rest144_prepare()
    call r13_scene(R13_PLACES['room13'][1],R13_PLACES['room13'][0],'calm')
    jump r13_v111_sleep1

testcase rest144_cancel_then_sleep:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_rest144_start')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (r13_v111_rest_option() and room13['day']==1)
    run Function(qa_rest144_remember)
    screenshot '144-visible-sleep.png'
    click id 'r13_rest_sleep'
    pause until screen 'r13_confirm' timeout 10
    pause .4
    screenshot '144-sleep-confirm.png'
    click id 'r13_confirm_no'
    pause until screen 'r13_hub' timeout 10
    assert eval (room13==renpy.test.rest144_before)
    # 침대를 직접 눌러도 같은 확인이 열리고, 확인하기 전 날짜는 바뀌지 않는다.
    run Show('qa_hidden_base_return',value=('object','bed'))
    pause .3
    click 'QA 행동'
    pause until screen 'r13_confirm' timeout 10
    assert eval (room13==renpy.test.rest144_before)
    pause .4
    click id 'r13_confirm_yes'
    click pos (900,600) until eval (room13['day']==2) timeout 30
    assert eval (r13_has('v111:applied:option:sleep1:0'))

init python:
    def qa_pan144_coords():
        return sorted((a['person'],a['x'],a['y'],tuple(a['rect'])) for a in r13_stage_people())
    def qa_pan144_remember():
        renpy.test.pan144_before=qa_pan144_coords()

label qa_pan144_start:
    $ r13_v111_set('day',2)
    $ r13_edit(day=2,location='square',period=0)
    $ room13['v111']['scene']='MS14_D02_S01'
    $ r13_v111_arrive(['daram','resident_lamplighter','resident_piko'])
    call r13_scene(R13_PLACES['square'][1],R13_PLACES['square'][0],'calm')
    call r13_v111_wait('chorong_documents2')
    return

testcase panorama144_stable_people:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_pan144_start')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause 1.0
    run Function(qa_pan144_remember)
    screenshot '144-square-left.png'
    click '오른쪽 구역'
    pause 1.0
    assert eval (qa_pan144_coords()==renpy.test.pan144_before)
    screenshot '144-square-right.png'
    click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause 1.0
    assert eval (qa_pan144_coords()==renpy.test.pan144_before)
    assert eval (len({a['person'] for a in r13_stage_people()})==len(r13_stage_people()))

label qa_roam144_start:
    $ qa_rest144_prepare()
    call r13_scene(R13_PLACES['room13'][1],R13_PLACES['room13'][0],'calm')
    call r13_v111_wait('sleep1')
    return

testcase inn144_detour_and_return:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_roam144_start')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (set(('inn','hall','room13'))<=set(r13_places()))
    click '지도'
    pause until screen 'r13_map' timeout 10
    pause .6
    screenshot '144-inn-map-revisit.png'
    click '현장으로'
    pause until screen 'r13_hub' timeout 10
    run Show('qa_hidden_base_return',value=('travel','hall'))
    pause .3
    click 'QA 행동'
    pause until eval (room13['location']=='hall' and renpy.get_screen('r13_hub')) timeout 10
    run Show('qa_hidden_base_return',value=('travel','inn'))
    pause .3
    click 'QA 행동'
    pause until eval (room13['location']=='inn' and renpy.get_screen('r13_hub')) timeout 10
    screenshot '144-revisited-reception.png'
    run Show('qa_hidden_base_return',value=('travel','hall'))
    pause .3
    click 'QA 행동'
    pause until eval (room13['location']=='hall' and renpy.get_screen('r13_hub')) timeout 10
    run Show('qa_hidden_base_return',value=('travel','room13'))
    pause .3
    click 'QA 행동'
    pause until eval (room13['location']=='room13' and renpy.get_screen('r13_hub')) timeout 10
    assert eval (room13['day']==1 and room13['v111']['gate']=='sleep1' and r13_v111_rest_option())
    assert eval (not set(('kitchen','guestroom','passage'))&set(r13_places()))

label qa_resident144_start:
    $ r13_v111_set('day',6)
    $ r13_edit(day=6,location='dining',period=2)
    $ room13['v111']['scene']='MS14_D06_S04'
    $ r13_grant(['V111:E06_CONTACT','V111:E06_FIRE'],'검수 진입')
    $ r13_v111_arrive(['daram','nabi'])
    call r13_scene(R13_PLACES['dining'][1],R13_PLACES['dining'][0],'calm')
    $ renpy.hide_screen('r13_evidence_found')
    call r13_v111_wait('sleep6_input')
    return

label qa_group144_start:
    $ r13_v111_set('day',2)
    $ r13_edit(day=2,location='inn',period=1)
    $ room13['v111']['scene']='MS14_D02_S04'
    $ r13_v111_arrive(['daram'])
    call r13_scene(R13_PLACES['inn'][1],R13_PLACES['inn'][0],'calm')
    call r13_v111_wait('afternoon2')
    return

testcase resident144_followup_reopen:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_resident144_start')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    screenshot '144-nabi-before.png'
    click '나비'
    pause until screen 'r13_topics' timeout 15
    pause .7
    click '가져간 사람도 적어 두나요?'
    click pos (900,600) until screen 'r13_topics' timeout 20
    pause .7
    click '등잔은 어디에 두셨습니까?'
    click pos (900,600) until screen 'r13_topics' timeout 20
    pause .7
    assert eval (all(q[2] for q in r13_v111_questions('nabi')) and len(r13_v111_questions('nabi'))==2)
    screenshot '144-two-read-questions.png'
    click '돌아가기'
    pause until screen 'r13_hub' timeout 10
    pause .7
    click '나비'
    pause until screen 'r13_topics' timeout 10
    assert eval (not r13_v111_idle_ok('nabi'))
    pause .7
    click '등잔은 어디에 두셨습니까?'
    click pos (900,600) until screen 'r13_topics' timeout 20
    assert eval (room13['day']==6)

testcase resident144_life_group:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_group144_start')
    pause until screen 'r13_hub' timeout 20
    pause 1.0
    assert eval (any(g['id']=='inn_mending' for g in r13_life_groups_here()))
    if eval (r13_world_offset()>0):
        click '왼쪽 구역' until eval (r13_world_offset()==0) timeout 20
    pause .7
    run Function(qa_rest144_remember)
    screenshot '144-inn-mending.png'
    click id 'life_group_inn_mending'
    pause until screen 'r13_life_group_conversation' timeout 10
    pause .5
    screenshot '144-listen-to-residents.png'
    click '계속 듣기'
    pause .4
    click '계속 듣기'
    pause .4
    click '돌아가기'
    pause until screen 'r13_hub' timeout 10
    assert eval (room13==renpy.test.rest144_before)

testcase public144_map_detour_and_resume:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Jump('qa_pan144_start')
    pause until screen 'r13_hub' timeout 20
    pause .8
    run Function(r13_v111_set,'ui_room_arrival_seen',True)
    assert eval ('inn' in r13_places() and 'post' not in r13_places())
    click '지도'
    pause until screen 'r13_map' timeout 10
    pause .7
    click id 'map_name_inn'
    pause .3
    click id 'r13_map_travel'
    pause until eval (room13['location']=='inn' and renpy.get_screen('r13_hub')) timeout 15
    assert eval (room13['day']==2 and room13['v111']['gate']=='chorong_documents2' and r13_v111_value('location:daram')=='inn')
    screenshot '144-optional-inn-visit.png'
    click '지도'
    pause until screen 'r13_map' timeout 10
    pause .7
    click id 'r13_map_region_village'
    pause .4
    click id 'map_name_square'
    pause .3
    click id 'r13_map_travel'
    pause until eval (room13['location']=='square' and renpy.get_screen('r13_hub')) timeout 15
    assert eval (room13['v111']['gate']=='chorong_documents2' and r13_v111_value('location:daram')=='square')
    assert eval ('resident_lamplighter' in r13_visible_people() and 'post' not in r13_places())
    screenshot '144-returned-to-main-question.png'
