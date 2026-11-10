# 시작 장면만 준비한다. 이후 화면 조작과 기존 등 고정 라벨을 실행한다.
init python:
    def qa149_prepare(place="store",night=False):
        qa146_prepare(2,2 if night else 0,place,gate="lamp_prep2" if night else "morning_finish2",scene="MS14_D02_S05" if night else "MS14_D02_S03",values={"ui_room_arrival_seen":True,"piko_alive":True},evidence=["E01","E06","E07"])
        r13_v111_arrive(["daram"])
        store.r13_ex149_held=None
        store.preferences.text_cps=0
        store.r13_conv_skip_run=False

    def qa149_diagnostics():
        sc=renpy.get_screen("r13_topics")
        qa146_output("149-topics.json",dict(person=sc.scope.get("person") if sc else None,questions=[(row[0],str(getattr(row[1],"value",None))) for row in r13_v111_questions("karo")],visible=r13_visible_people(),ready=r13_ex149_person_ready("karo"),where=r13_where("karo"),actor_ready=r13_v111_actor_ready("karo"),available=r13_ex149_available(),calm=r13_sidequest_calm(),sidequests=room13.get("v111",{}).get("sidequests"),values=room13["v111"]["values"],flags={k:getattr(store,k,None) for k in QA146_ACTIVE_FIELDS},wallet=room13.get("livelihood"),wallet_types={k:str(type(v)) for k,v in (room13.get("livelihood") or {}).items()},day_type=str(type(room13.get("day"))),day_int=type(room13.get("day")) is int,model_wallet=_r13_ex149_wallet()))

    def qa149_matrix():
        saved=qa146_save_context();rows=[]
        try:
            for day in range(2,8):
                qa149_prepare()
                if day>2:
                    r13_edit(day=day)
                    room13["v111"]["scene"]="MS14_D04_S01" if day<7 else "MS14_D07_S02"
                    room13["v111"]["gate"]="sleep4" if day<7 else "free_day7"
                    if day==7:
                        room13["v111"]["values"].update({"meeting:fire":"win","D07_S02_handover_completed":True,"D07_S02_message_completed":True,"route7":"uncommitted"})
                diagnostics={}
                for person in ("resident_eunho","karo"):
                    place=r13_where(person)
                    if place not in r13_places():
                        diagnostics[person]=dict(place=place,allowed=False);continue
                    r13_edit(location=place);r13_v111_roam_arrive(["daram"])
                    diagnostics[person]=dict(place=place,visible=person in r13_visible_people(),ready=r13_ex149_person_ready(person),topics=r13_ex149_topics(person))
                assert "market" in r13_places(),(day,"장터 접근 불가")
                rows.append(dict(day=day,people=diagnostics))
            qa149_prepare("market")
            assert r13_ex149_person_ready("resident_eunho"),(r13_where("resident_eunho"),r13_visible_people())
            assert r13_ex149_mark("intro_seen")
            assert r13_ex149_receive("cord") and r13_ex149_receive("weight")
            before=r13_wallet(room13)["cash"]
            assert not r13_ex149_receive("cord") and r13_wallet(room13)["cash"]==before
            r13_edit(location="store",period=1);r13_v111_roam_arrive(["daram"])
            assert r13_ex149_scale_place() and r13_ex149_observe("scale_pivot")
            assert r13_ex149_scale_correct() and r13_ex149_owned("weight")
            r13_edit(location="gate");r13_v111_roam_arrive(["daram"])
            assert r13_ex149_person_ready("karo"),(r13_where("karo"),r13_visible_people())
            for key in R13_EX149_DELIVERY_PARTS:assert r13_ex149_observe(key)
            assert r13_ex149_delivery_tie() and r13_ex149_delivery_report()
            r13_edit(location="square",period=2);r13_v111_roam_arrive(["daram"])
            room13["v111"]["gate"]="lamp_prep2";room13["v111"]["scene"]="MS14_D02_S05"
            r13_v111_set("lamp_latch_seen2",True)
            assert r13_ex149_lamp_ready("lamp")
            assert r13_ex149_lamp_supply("lamp") and not r13_ex149_owned("cord")
            assert r13_v111_value("lamp_cord2") and not r13_v111_value("lamp_bound2")
            assert not r13_ex149_lamp_supply("lamp")
            qa146_output("exploration149-runtime.json",dict(scope="실제 SDK의 준비 상태 재실·물품 연계. 자연 완주 아님.",days=rows,state=room13))
        finally:qa146_restore_context(saved)

label qa149_hub(place="store"):
    $ qa146_begin()
    $ qa149_prepare(place)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    while True:
        call r13_v111_wait(room13['v111']['gate'])
        $ renpy.test.qa149_return=_return

label qa149_lamp(learned=True):
    $ qa146_begin()
    $ qa149_prepare("square",True)
    $ room13["livelihood"]=r13_wallet(room13)
    $ room13["livelihood"]["items"]=["cord"]
    if learned:
        $ r13_ex149_mark("knot_method")
    $ r13_v111_set("lamp_latch_seen2",True)
    call r13_scene(R13_PLACES['square'][1],R13_PLACES['square'][0],'calm')
    call r13_lamp_prep2
    return

testcase exploration149_runtime:
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa146_begin)
    run Function(qa149_matrix)

testcase exploration149_shop_and_bag:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa149_hub','market')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    run Function(qa_early_person_point,'resident_eunho')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_eunho')
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .8
    click '묶음끈과 표준추를 쓸 수 있을까요?'
    click pos (900,600) until screen 'r13_ex149_shop' timeout 25
    pause .8
    screenshot '149-shop-pc.png'
    click id 'ex149_receive_cord'
    pause .5
    click pos (900,600) until screen 'r13_ex149_shop' timeout 25
    pause .5
    click id 'ex149_receive_weight'
    pause .5
    click pos (900,600) until screen 'r13_ex149_shop' timeout 25
    pause .5
    assert eval (r13_ex149_owned('cord') and r13_ex149_owned('weight') and r13_wallet(room13)['cash']==0)
    click id 'ex149_shop_back'
    pause until screen 'r13_topics' timeout 20
    pause .6
    click '돌아가기'
    pause until screen 'r13_hub' timeout 20
    pause .8
    click id 'r13_field_items149'
    pause until screen 'r13_ex149_bag' timeout 20
    pause .8
    screenshot '149-bag-pc.png'
    run Function(qa_field146_journal_mode,True)
    pause .8
    screenshot '149-bag-touch-large.png'
    click id 'ex149_select_weight'
    pause until screen 'r13_hub' timeout 20
    assert eval (r13_ex149_held=='weight')
    pause .8
    click id 'r13_field_items149'
    pause .3
    assert eval (r13_ex149_held is None)
    run Function(qa_field146_restore_mode)

testcase exploration149_lamp_original_outcome:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa149_lamp')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    click id 'r13_field_items149'
    pause until screen 'r13_ex149_bag' timeout 20
    click id 'ex149_select_cord'
    pause until screen 'r13_hub' timeout 20
    pause .8
    if eval (qa_field146_object_point('lamp')[0]>1200):
        click pos (1232,276)
        pause 1.0
    if eval (qa_field146_object_point('lamp')[0]<80):
        click pos (48,276)
        pause 1.0
    click pos qa_field146_object_point('lamp')
    pause until screen 'r13_confirm' timeout 20
    pause .8
    screenshot '149-lamp-item-confirm.png'
    click '더 살펴보기'
    pause until screen 'r13_hub' timeout 20
    assert eval (r13_ex149_owned('cord') and not r13_v111_value('lamp_cord2') and not r13_v111_value('lamp_bound2'))
    pause .8
    click pos qa_field146_object_point('lamp')
    pause until screen 'r13_confirm' timeout 20
    click '걸쇠 고정하기'
    click pos (900,600) until screen 'r13_hub' timeout 30
    assert eval (r13_v111_value('lamp_bound2') and not r13_ex149_owned('cord') and 'cord' in r13_wallet(room13)['used'])

testcase exploration150_lamp_missing_method:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa149_lamp',False)
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    click id 'r13_field_items149'
    pause until screen 'r13_ex149_bag' timeout 20
    click id 'ex149_select_cord'
    pause until screen 'r13_hub' timeout 20
    pause .8
    if eval (qa_field146_object_point('lamp')[0]>1200):
        click pos (1232,276)
        pause 1.0
    if eval (qa_field146_object_point('lamp')[0]<80):
        click pos (48,276)
        pause 1.0
    $ renpy.test.ex150_before=winter_copy.deepcopy(room13)
    click pos qa_field146_object_point('lamp')
    pause until eval (r13_packet and '묶는 방법부터' in r13_packet[1]) timeout 20
    pause .8
    screenshot '150-lamp-method-needed.png'
    click pos (900,600) until screen 'r13_hub' timeout 20
    assert eval (room13==renpy.test.ex150_before and r13_ex149_owned('cord') and r13_ex149_held=='cord')
    assert eval (not r13_v111_value('lamp_bound2') and not r13_v111_value('lamp_cord2'))

testcase exploration149_delivery_choices:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa149_hub','gate')
    $ room13['livelihood']=r13_wallet(room13)
    $ room13['livelihood']['items']=['cord']
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    run Function(qa_early_person_point,'karo')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'karo')
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .8
    run Function(qa149_diagnostics)
    screenshot '149-karo-topics.png'
    click '수레 옆의 두 짐을 살펴봐도 될까요?'
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    pause .6
    click id 'ex149_look_large_tag'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    pause .6
    click id 'ex149_look_small_tag'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    pause .6
    click id 'ex149_look_box'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    pause .6
    screenshot '149-delivery-observed.png'
    click id 'ex149_tie'
    pause until screen 'choice' timeout 20
    pause .6
    screenshot '149-delivery-method-choice.png'
    click '작은 상자를 큰 상자 위에 그냥 얹는다'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    assert eval (not r13_ex149_state().get('delivery_tied') and r13_ex149_owned('cord'))
    pause .6
    click id 'ex149_tie'
    pause until screen 'choice' timeout 20
    click '두 상자를 겹쳐 끈으로 묶는다'
    pause until screen 'r13_confirm' timeout 20
    click '더 살펴보기'
    pause until screen 'r13_ex149_closeup' timeout 20
    assert eval (not r13_ex149_state().get('delivery_tied'))
    pause .6
    click id 'ex149_tie'
    pause until screen 'choice' timeout 20
    click '두 상자를 겹쳐 끈으로 묶는다'
    pause until screen 'r13_confirm' timeout 20
    click '두 짐 묶기'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    assert eval (r13_ex149_state().get('delivery_tied') and not r13_ex149_state().get('knot_method') and r13_ex149_owned('cord'))
    pause .6
    screenshot '149-delivery-tied.png'
    click id 'ex149_report_delivery'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    assert eval (r13_ex149_state().get('knot_method'))
    pause .6
    click id 'ex149_closeup_back'
    pause until screen 'r13_topics' timeout 20

testcase exploration149_scale_reuse_and_seller:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa149_hub','store')
    $ r13_edit(period=1)
    $ room13['livelihood']=r13_wallet(room13)
    $ room13['livelihood']['items']=['weight']
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    click id 'r13_field_items149'
    pause until screen 'r13_ex149_bag' timeout 20
    click id 'ex149_select_weight'
    pause until screen 'r13_hub' timeout 20
    pause .8
    if eval (qa_field146_object_point('scale')[0]<80):
        click pos (48,276)
        pause 1.0
    click pos qa_field146_object_point('scale')
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    pause .6
    screenshot '149-scale-with-weight.png'
    click id 'ex149_look_pivot'
    pause .5
    click pos (900,600) until screen 'r13_ex149_closeup' timeout 25
    assert eval (r13_ex149_state().get('scale_pivot') and r13_ex149_owned('weight') and not r13_ex149_state().get('scale_corrected'))
    pause .6
    click id 'ex149_closeup_back'
    pause .5
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (not r13_ex149_scale_on_pan and r13_ex149_owned('weight'))
    pause 1.0
    run Function(qa_early_person_point,'resident_eunho')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_eunho')
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .8
    click '표준추를 올려 봤는데, 함께 다시 재 주시겠어요?'
    pause .5
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_ex149_state().get('scale_corrected') and r13_ex149_owned('weight') and not r13_has('scale_rigged') and not r13_has('shop_discount'))

testcase exploration149_main_family_and_grief_order:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until eval (r13_packet and len(r13_packet)>2 and r13_packet[2].get('line_id')=='MS14_D01_S01_L0020') timeout 90
    pause .7
    screenshot '149-main01-family.png'
    assert eval ('셋이 같이 자자' in r13_packet[1])
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa_piko_scene_start)
    run Jump('r13_v111_day3')
    click pos (900,600) until eval (r13_packet and len(r13_packet)>2 and r13_packet[2].get('line_id')=='MS14_D03_S01_L0012') timeout 90
    pause .7
    screenshot '149-main03-child-question.png'
    assert eval (not qa_nw_seen('등 쪽으로 돌아누워서요'))
    click pos (900,600) until eval (r13_packet and len(r13_packet)>2 and r13_packet[2].get('line_id')=='MS14_D03_S01_L0018') timeout 45
    pause .7
    screenshot '149-main03-father-answer.png'
    assert eval ('아빠 여기 있을게' in r13_packet[1] and not qa_nw_seen('등 쪽으로 돌아누워서요'))
    click pos (900,600) until screen 'r13_piko_scene' timeout 90
    assert eval (qa_nw_seen('등 쪽으로 돌아누워서요') and r13_v111_owned('E09'))
    pause .7
    screenshot '149-main03-investigation.png'
