# 각 장면은 직접 준비한다. 자연 7일 완주로 보고하지 않는다.
init python:
    def qa148_projection():
        n=winter_copy.deepcopy(store.room13)
        n["v111"].pop("world148",None)
        return n

    def qa148_prepare(key,result="safe"):
        values={"ui_room_arrival_seen":True,"piko_alive":True}
        day=2;period=0;gate="morning_finish2";scene="MS14_D02_S03"
        if key in ("seat","tools"):
            day=4;period=1;gate="sleep4";scene="MS14_D04_S01"
            values.update({"meeting:lamp":"win","listed:resident_tok":False})
        if key=="aftermath":
            day=7;period=1;gate="free_day7";scene="MS14_D07_S02"
            values.update({"meeting:fire":"win","D07_S02_handover_completed":True,
                "D07_S02_message_completed":True,"route7":"uncommitted",
                "D06_S03P_empty_fire_completed":True,"warehouse_children_school_handover":4,
                "KKOMI_ALIVE":True,"BORI_hands":"not_rescue_burned"})
        if result=="dead":values.update(piko_alive=False,**{"piko_news3:nabi":True,"piko_news3:buri":True})
        if result=="lost":values.update(D06_S03P_empty_fire_completed=False,D06_S03_main_completed=True,
            warehouse_children_rescued=3,KKOMI_ALIVE=False,BORI_hands="burned")
        place=R13_WORLD148[key]["sources"][0]["location"]
        qa146_prepare(day,period,place,gate=gate,scene=scene,values=values,evidence=["E01","E06","E07","E09","E10","E12"])
        store.r13_conv_skip_run=False
        r13_v111_arrive(["daram"])

    def qa148_runtime_matrix():
        saved=qa146_save_context();report=[]
        try:
            for key,spec in R13_WORLD148.items():
                for context in (("safe","dead") if key in ("seat","tools") else (("safe","lost") if key=="aftermath" else ("safe",))):
                    for result in ("help","listen"):
                        qa148_prepare(key,context);before=qa148_projection()
                        source=spec["sources"][0]
                        assert r13_world148_source_allowed(key,source["object"]),(key,"현장 관찰 불가")
                        assert r13_world148_record(key,"observe"),(key,"관찰 저장 불가")
                        # 지난 본편 location을 고쳐 NPC를 소환하지 않고 실제 일과의 장소로 간다.
                        owner=spec["owner"];place=r13_where(owner)
                        assert place in r13_places(),(key,owner,place,"주민 일과 장소 접근 불가")
                        r13_edit(location=place);r13_v111_roam_arrive(["daram"])
                        assert r13_world148_ready(key),(key,owner,place,r13_visible_people(),"일과 대화 불가")
                        assert r13_world148_record(key,"choose",result),(key,"선택 저장 불가")
                        if result=="help":
                            task=spec["task"];r13_edit(location=task["location"]);r13_v111_roam_arrive(["daram"])
                            assert r13_world148_record(key,"work"),(key,"현장 행동 불가")
                        assert not r13_world148_record(key,"choose","listen"),(key,"선택 덮어쓰기")
                        assert (store.room13["day"],store.room13["period"],store.room13["evidence"],store.room13["v111"]["gate"],store.room13["v111"]["scene"])==(before["day"],before["period"],before["evidence"],before["v111"]["gate"],before["v111"]["scene"])
                        report.append(dict(thread=key,context=context,result=result,owner_place=place,state=r13_world148_state(key),variants=r13_world148_variants(key)))
            qa146_output("world148-runtime-matrix.json",dict(scope="실제 SDK의 준비 상태·일과·행동 조회. 자연 완주는 아니다.",rows=report))
        finally:qa146_restore_context(saved)

label qa148_hub(key):
    $ qa146_begin()
    $ qa148_prepare(key)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    while True:
        call r13_v111_wait(room13['v111']['gate'])
        $ renpy.test.qa148_main_return=_return

testcase world148_runtime_matrix:
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Function(qa146_begin)
    run Function(qa148_runtime_matrix)

testcase world148_postal_object_question_work_and_journal:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa148_hub','postal')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause 1.0
    if eval (qa_field146_object_point('parcels')[0]>1200):
        click pos (1232,276)
        pause 1.0
    screenshot '148-postal-source-before.png'
    click pos qa_field146_object_point('parcels')
    pause .8
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (r13_world148_state('postal').get('observed'))
    pause .8
    pause .8
    run Function(qa_early_person_point,'seryeon')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'seryeon')
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .8
    click '한 묶음으로 오면 보낸 사람도 같습니까?'
    click pos (900,600) until screen 'choice' timeout 25
    pause .7
    screenshot '148-postal-choice.png'
    click '겉표시를 함께 살펴봐도 될까요?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_world148_state('postal').get('result')=='help' and not r13_world148_state('postal').get('worked'))
    pause .7
    click '돌아가기'
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 20
    pause .8
    click pos qa_field146_object_point('parcels')
    pause until screen 'r13_confirm' timeout 20
    pause .7
    screenshot '148-postal-work-confirm.png'
    click '나중에 하기'
    pause until screen 'r13_hub' timeout 20
    assert eval (not r13_world148_state('postal').get('worked'))
    pause .8
    click pos qa_field146_object_point('parcels')
    pause until screen 'r13_confirm' timeout 20
    pause .7
    click '우편 묶음의 겉표시 살피기'
    click pos (900,600) until screen 'r13_hub' timeout 25
    assert eval (r13_world148_state('postal').get('worked'))
    pause .8
    click '마을일'
    pause until screen 'r13_sidequest_journal146' timeout 20
    pause .7
    screenshot '148-world-journal-pc.png'
    assert eval (renpy.get_screen('r13_sidequest_journal146').scope['section']=='world')
    run Function(qa_field146_journal_mode,True)
    pause .7
    screenshot '148-world-journal-touch-large.png'
    assert eval (renpy.get_screen('r13_sidequest_journal146').scope['per_page']==1)
    click '현장으로'
    run Function(qa_field146_restore_mode)
