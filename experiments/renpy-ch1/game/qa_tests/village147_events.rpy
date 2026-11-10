# 시작·저녁은 직접 준비한다. 이후 주민·질문·선택·재회는 실제 GUI를 누른다.
init python:
    def qa147_events_projection():
        state=qa146_quest_projection();story=store.room13["v111"]
        state.update(scene=story.get("scene"),gate=story.get("gate"),location=store.room13["location"],
                     elapsed=story.get("values",{}).get("elapsed_minutes"),
                     sidequests=winter_copy.deepcopy(story.get("sidequests",{})))
        return state

    def qa147_events_prepare(key):
        qa146_begin()
        place=R13_VISITS147[key]["source_place"]
        qa146_prepare(2,0,place,gate="lamp_rope",scene="MS14_D02_S01",
                      values={"ui_room_arrival_seen":True,"location:seryeon":"post"},evidence=["E01","E06"])
        r13_v111_arrive(["daram"])
        store.r13_conv_skip_run=False
        renpy.test.qa147_event_key=key
        renpy.test.qa147_event_returned=None
        renpy.test.qa147_event_before=qa147_events_projection()
        qa147_events_diagnostics("source-prepared")
        assert r13_visit147_source_allowed(key),(key,"준비된 실제 배우/기회 불일치",r13_visible_people())

    def qa147_events_evening(key):
        # 시간 경과의 자연 플레이 증거가 아니다. 실제 얻은 방문 기억만 유지해 저녁 재회를 준비한다.
        n=winter_copy.deepcopy(store.room13)
        n.update(day=2,period=2,location="dining")
        n["v111"].update(gate="lamp_prep2",scene="MS14_D02_S05",people=["daram"])
        n["v111"]["values"]["location:daram"]="dining"
        store.room13=n
        renpy.test.qa147_event_key=key
        store.r13_v111_talk_person=None
        r13_v111_arrive(["daram"])
        renpy.test.qa147_event_before=qa147_events_projection()
        qa147_events_diagnostics("evening-prepared")
        assert r13_visit147_memory_allowed(key),(key,"저녁 실제 재회 불가",r13_visible_people())

    def qa147_events_diagnostics(tag):
        key=renpy.test.qa147_event_key
        qa146_output("village147-events-"+key+"-"+tag+".json",dict(
            scope="직접 준비한 2일 장면/저녁 뒤 실제 GUI 검수. 자연 플레이 도달성 검사는 아니다.",
            key=key,tag=tag,projection=qa147_events_projection(),state=r13_visit147_state(key),
            all_visit_states={event:r13_visit147_state(event) for event in R13_VISITS147},
            visible=list(r13_visible_people()),
            people={person:dict(ready=r13_v111_actor_ready(person),where=r13_where(person),
                               physical=r13_v111_value("location:"+person),busy=r13_v111_value("busy:"+person))
                    for person in R13_VISITS147[key]["members"]},
            actions=r13_visit147_person_actions(R13_VISITS147[key]["owner"]),
            original_return=getattr(renpy.test,"qa147_event_returned",None)))

label qa147_events_hub(key):
    $ qa147_events_prepare(key)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    while True:
        call r13_v111_wait(room13['v111']['gate'])
        $ renpy.test.qa147_event_returned=_return

label qa147_events_evening_hub(key):
    $ qa147_events_evening(key)
    call r13_scene(R13_PLACES[room13['location']][1],R13_PLACES[room13['location']][0],'calm')
    while True:
        call r13_v111_wait(room13['v111']['gate'])
        $ renpy.test.qa147_event_returned=_return

testcase village147_postcard_help_and_evening_memory:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_events_hub','postcard')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause .7
    click '부엉이 할아버지'
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '엽서를 쓰시는 중이세요?'
    click pos (900,600) until screen 'choice' timeout 25
    pause .7
    screenshot '147-postcard-choice.png'
    click '안부부터 물어보시면 어떨까요?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_state('postcard').get('result')=='help')
    assert eval (qa147_events_projection()==renpy.test.qa147_event_before and renpy.test.qa147_event_returned is None)
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 20
    run Function(qa147_events_diagnostics,'help-completed')
    run Call('qa147_events_evening_hub','postcard')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause .7
    run Function(qa_early_person_point,'resident_owlgp')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_owlgp')
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '엽서는 보내셨어요?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_state('postcard').get('memory_seen') is True)
    assert eval (r13_visit147_state('postcard').get('result')=='help' and r13_visit147_memory_phase('postcard')=='memory_help')
    assert eval (qa147_events_projection()==renpy.test.qa147_event_before and renpy.test.qa147_event_returned is None)
    screenshot '147-postcard-evening-memory.png'
    run Function(qa147_events_diagnostics,'evening-memory')

testcase village147_sleeve_watch_then_sewing_offer:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_events_hub','sleeve')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause .7
    click '토리'
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '소매가 걸렸니?'
    click pos (900,600) until screen 'choice' timeout 25
    pause .7
    screenshot '147-sleeve-choice.png'
    click '잠깐 옆에서 볼게요.'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_state('sleeve').get('result')=='watch' and r13_sidequest_status('seam')=='unseen')
    assert eval (qa147_events_projection()==renpy.test.qa147_event_before and renpy.test.qa147_event_returned is None)
    pause .7
    click '돌아가기'
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready'] and r13_sidequest_person_actions('resident_yeoni')) timeout 60
    run Function(qa147_events_diagnostics,'before-existing-sewing-owner-click')
    screenshot '147-sleeve-field-before-owner.png'
    run Function(qa_early_person_point,'resident_yeoni')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_yeoni')
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '바느질을 조금 도와드릴까요?'
    click pos (900,600) until screen 'choice' timeout 25
    pause .7
    screenshot '147-sleeve-existing-sewing-offer.png'
    click '지금은 돕기 어렵겠습니다.'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_sidequest_status('seam')=='declined' and r13_visit147_state('sleeve').get('result')=='watch')
    assert eval (room13['v111']['gate']=='lamp_rope' and room13['period']==0 and renpy.test.qa147_event_returned is None)
    run Function(qa147_events_diagnostics,'watch-and-existing-quest-decline')

testcase village147_declined_sleeve_and_unvisited_postcard:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('qa147_events_hub','sleeve')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause .7
    click '토리'
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '소매가 걸렸니?'
    click pos (900,600) until screen 'choice' timeout 25
    pause .7
    click '지금은 도와드리기 어렵겠어요.'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_state('sleeve').get('result')=='decline')
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 20
    run Call('qa147_events_evening_hub','sleeve')
    pause until eval (renpy.get_screen('r13_hub') and renpy.get_screen('r13_hub').scope['world_ready']) timeout 30
    pause .7
    run Function(qa_early_person_point,'resident_tori')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_tori')
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '소매는 이제 편하니?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_memory_phase('sleeve')=='memory_decline' and r13_visit147_state('sleeve').get('memory_seen') is True)
    assert eval (r13_visit147_state('postcard')=={} and r13_sidequest_status('seam')=='unseen')
    pause .7
    click '돌아가기'
    pause until screen 'r13_hub' timeout 20
    pause .7
    run Function(qa_early_person_point,'resident_owlgp')
    if eval (not qa_early_person_visible):
        click pos (qa_early_pan_x,276)
        pause 1.0
        run Function(qa_early_person_point,'resident_owlgp')
    assert eval (qa_early_person_visible)
    click pos (qa_early_person_x,qa_early_person_y)
    click pos (900,600) until screen 'r13_topics' timeout 25
    pause .7
    click '지금은 쉬시는 중이세요?'
    click pos (900,600) until screen 'r13_topics' timeout 25
    assert eval (r13_visit147_state('postcard').get('status')=='passed' and 'result' not in r13_visit147_state('postcard'))
    assert eval (qa147_events_projection()==renpy.test.qa147_event_before and renpy.test.qa147_event_returned is None)
    run Function(qa147_events_diagnostics,'declined-sleeve-and-unvisited-postcard')
