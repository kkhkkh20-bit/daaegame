# 실제 SDK에 준비 상태를 주입하는 접근·취소 검사다. 자연 플레이 도달성 검사는 아니다.
# 조회 전수와 실제 지도·확인창 클릭을 구분한다. 공개 빌드에는 포함하지 않는다.
init python:
    QA147_ACCESS_PUBLIC=("inn","hall","room13","dining","square","gate","post","workshop","clinic","school","store")
    QA147_ACCESS_CONTEXTS={
        "lamp_rope":(0,"square","MS14_D02_S01"),
        "morning_finish2":(0,"square","MS14_D02_S03"),
        "afternoon2":(1,"dining","MS14_D02_S04"),
        "shelter_enter":(1,"square","MS14_D02_S04"),
    }

    def qa147_access_prepare(gate):
        period,place,scene=QA147_ACCESS_CONTEXTS[gate]
        values=dict(ui_room_arrival_seen=True,piko_sheltered=False)
        if gate=="shelter_enter":
            values.update(D02_afternoon="shelter",piko_sacks2=True,piko_cloth2=True,piko_bench_clean2=True)
        qa146_prepare(2,period,place,gate=gate,scene=scene,values=values,evidence=["E01","E06"])
        # 개방은 방문 기록에 기대지 않는다. 방문을 만든 뒤 통과했다고 세지 않는다.
        store.room13["v111"]["visited_places"]=[]
        store.r13_conv_skip_run=False
        renpy.test.qa147_access_returned=None
        renpy.hide_screen("r13_hub")

    def qa147_access_query_matrix():
        saved=qa146_save_context()
        report=[]
        try:
            for gate in ("lamp_rope","morning_finish2","afternoon2"):
                for place in QA147_ACCESS_PUBLIC:
                    qa147_access_prepare(gate)
                    store.room13["location"]=place
                    store.room13["v111"]["values"]["location:daram"]=place
                    before=winter_copy.deepcopy(store.room13)
                    places=list(r13_places())
                    assert set(QA147_ACCESS_PUBLIC)<=set(places),(gate,place,"미방문 공공장소가 닫힘",places)
                    assert not set(("passage","hidden_pandol","hidden_base14","v111_labor","v111_fire"))&set(places),(gate,place,places)
                    binding=r13_v111_binding()
                    people=list(r13_visible_people())
                    assert len(people)==len(set(people)),(gate,place,"주민 중복",people)
                    for person in people:
                        assert r13_v111_person_alive(person),(gate,place,"사망자 표시",person)
                        assert not r13_v111_value("departed:"+person),(gate,place,"떠난 주민 표시",person)
                        assert r13_v111_actor_ready(person),(gate,place,"보이는 주민과 대화 불가",person)
                        r13_v111_questions(person)
                    texts=[]
                    for key,spec in ROOM13["objects"].get(place,{}).items():
                        visible=r13_object_visible(spec)
                        text=r13_v111_ambient_text(key,spec)
                        if visible and text:texts.append(text)
                    text=" ".join(texts)
                    for forbidden in ("우박의 측정지","백 부인의 매입 장부","등번호 3","판매자 실룩","장치가 낸 힘의 숫자","이름 대신 쓴 번호"):
                        assert forbidden not in text,(gate,place,"미래 자료 내용 누출",forbidden,text)
                    assert not r13_v111_owned("E13") and not r13_v111_owned("E16"),(gate,place,"미래 자료 획득")
                    assert store.room13==before,(gate,place,"조회 중 이야기 상태 변경")
                    report.append(dict(gate=gate,place=place,people=people,observations=texts,open_places=places))
            # 입장 전 첫날에는 같은 공공장소 목록을 추가하지 않는다.
            qa146_prepare(1,0,"gate",gate="gate_request",scene="MS14_D01_S02")
            assert "clinic" not in r13_places() and "school" not in r13_places()
            # 실제 위기 게이트와 7일 S02의 완료 전후를 별도 준비 상태에서 조회한다.
            cases=[
                (3,0,"square","piko_clean","MS14_D03_S01",dict(piko_alive=False),False),
                (6,2,"v111_fire","wet_cloth6","MS14_D06_S03",dict(FIRE_EVACUATED=False),False),
                (7,1,"school","free_day7","MS14_D07_S02",dict(**{"meeting:fire":"win","D07_S02_handover_completed":False,"D07_S02_message_completed":False}),False),
                (7,1,"school","free_day7","MS14_D07_S02",dict(**{"meeting:fire":"win","D07_S02_handover_completed":True,"D07_S02_message_completed":True,"route7":"uncommitted"}),True),
            ]
            for day,period,place,gate,scene,values,opened in cases:
                qa146_prepare(day,period,place,gate=gate,scene=scene,values=values)
                before=winter_copy.deepcopy(store.room13)
                public=list(r13_v111_public_revisit_places())
                assert (set(QA147_ACCESS_PUBLIC)<=set(public))==opened,(day,gate,public,opened)
                assert store.room13==before,(day,gate,"경계 조회 중 상태 변경")
            qa146_output("village147-access-query.json",dict(scope="실제 SDK 준비 상태 조회. 자연 플레이는 아니다.",states=report))
        finally:
            qa146_restore_context(saved)

    def qa147_access_cancel_diagnostic(tag,before):
        after=winter_copy.deepcopy(store.room13)
        changes=[]
        def compare(left,right,path):
            if isinstance(left,dict) and isinstance(right,dict):
                for key in sorted(set(left)|set(right),key=str):
                    if key not in left:changes.append(dict(path=path+str(key),before="키 없음",after=right[key]))
                    elif key not in right:changes.append(dict(path=path+str(key),before=left[key],after="키 없음"))
                    else:compare(left[key],right[key],path+str(key)+".")
            elif left!=right:
                changes.append(dict(path=path.rstrip("."),before=left,after=right))
        compare(before,after,"")
        screens={}
        for name in ("r13_hub","r13_confirm","r13_map","r13_topics","say"):
            screen=renpy.get_screen(name)
            screens[name]=None if not screen else {key:screen.scope.get(key) for key in
                ("ready","world_ready","message","selected","region") if key in screen.scope}
        qa146_output("village147-"+tag+"-cancel-diagnostic.json",dict(
            scope="준비 상태에서 실제 화면 조작 후 취소. 자동 저장 메타 변경과 본편 변경을 구별한다.",
            before=before,after=after,changes=changes,
            returned=getattr(renpy.test,"qa147_access_returned",None),
            gate=after.get("v111",{}).get("gate"),scene=after.get("v111",{}).get("scene"),
            mouse=list(renpy.get_mouse_pos()),screens=screens,morning_save_due=r13_morning_due()))

label qa147_access_hub(gate):
    $ qa146_begin()
    $ qa147_access_prepare(gate)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    while True:
        call r13_v111_wait(gate)
        # 취소로 반환됐을 때 본편으로 진행하지 않고 검사 값에 남긴다.
        $ renpy.test.qa147_access_returned=_return

testcase village147_prepared_public_query:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa146_begin)
    run Function(qa147_access_query_matrix)

testcase village147_lunch_cancel_keeps_morning:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_access_hub','morning_finish2')
    pause until eval (renpy.get_screen('r13_hub') and room13['v111'].get('gate')=='morning_finish2' and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    # 첫 허브의 .4초 아침 저장 타이머가 새 morning_ids를 적은 뒤 기준을 잡는다.
    pause 1.0
    $ qa147_access_before=winter_copy.deepcopy(room13)
    screenshot 'village147-lunch-ready.png'
    click id 'r13_lunch147'
    pause until screen 'r13_confirm' timeout 20
    assert eval ('오후 일정' in renpy.get_screen('r13_confirm').scope['message'])
    screenshot 'village147-lunch-confirm.png'
    pause .7
    click id 'r13_confirm_no'
    pause until eval (not renpy.get_screen('r13_confirm') and renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 20
    pause .3
    run Function(qa147_access_cancel_diagnostic,'lunch',qa147_access_before)
    screenshot 'village147-lunch-cancel.png'
    assert eval (room13==qa147_access_before and renpy.test.qa147_access_returned is None and room13['period']==0)

testcase village147_forest_map_cancel_keeps_afternoon:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_access_hub','afternoon2')
    pause until eval (renpy.get_screen('r13_hub') and room13['v111'].get('gate')=='afternoon2' and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    $ qa147_access_before=winter_copy.deepcopy(room13)
    click '지도'
    pause until screen 'r13_map' timeout 20
    pause .7
    click id 'r13_map_region_mountain'
    pause .7
    click id 'map_building_forest'
    pause .4
    click id 'r13_map_travel'
    pause until screen 'r13_confirm' timeout 20
    assert eval ('해가 집니다' in renpy.get_screen('r13_confirm').scope['message'])
    screenshot 'village147-forest-confirm.png'
    pause .7
    click id 'r13_confirm_no'
    pause until eval (not renpy.get_screen('r13_confirm') and renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 20
    pause .3
    run Function(qa147_access_cancel_diagnostic,'forest',qa147_access_before)
    screenshot 'village147-forest-cancel.png'
    assert eval (room13==qa147_access_before and renpy.test.qa147_access_returned is None)
    assert eval (room13['period']==1 and not r13_v111_value('piko_sheltered') and r13_v111_value('D02_afternoon') in (None,'uncommitted'))

testcase village147_shelter_map_cancel_keeps_unfinished_handover:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_access_hub','shelter_enter')
    pause until eval (renpy.get_screen('r13_hub') and room13['v111'].get('gate')=='shelter_enter' and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    $ qa147_access_before=winter_copy.deepcopy(room13)
    click '지도'
    pause until screen 'r13_map' timeout 20
    pause .7
    click id 'r13_map_region_inn'
    pause .7
    click id 'map_room_dining'
    pause .4
    click id 'r13_map_travel'
    pause until screen 'r13_confirm' timeout 20
    assert eval ('저녁으로 넘어갑니다' in renpy.get_screen('r13_confirm').scope['message'])
    screenshot 'village147-shelter-confirm.png'
    pause .7
    click id 'r13_confirm_no'
    pause until eval (not renpy.get_screen('r13_confirm') and renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 20
    pause .3
    run Function(qa147_access_cancel_diagnostic,'shelter',qa147_access_before)
    screenshot 'village147-shelter-cancel.png'
    assert eval (room13==qa147_access_before and renpy.test.qa147_access_returned is None)
    assert eval (room13['period']==1 and room13['location']=='square' and not r13_v111_value('piko_sheltered'))
