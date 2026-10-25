init python:
    def qa_nw_dump():
        with open(os.path.join(config.basedir,"qa_result.txt"),"w") as f:
            for h in _history_list[-60:]:f.write("%s: %s\n"%(h.who,h.what))
    def qa_nw_day(day,route):
        r13_v111_set("day",day)
        r13_edit(day=day)
        r13_v111_set("route7",route)
        r13_v111_set("OWL_ALIVE",route!="murder")
        r13_v111_set("DARAM_DETAINED",route=="murder" and day<10)
        # Where the next scene starts, so its travel step returns at once.
        r13_edit(location="post" if (route=="murder" and day==10) else "school")

testcase v111_nw_d08_room_stone:
    # Room 13 on day 8: Buri's missing notebook, Granny's whisper, the unmarked stone.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,8,"murder")
    run Function(r13_v111_set,"DARAM_DETAINED",True)
    run Jump("r13_v111_room_checked8")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_owned("NW_STONE") and r13_v111_value("NW_STONE.variant")=="observed")
    assert eval (qa_nw_seen("그 도토 말이에요") and qa_nw_seen("제가 넣은 돌이 아닙니다") and qa_nw_seen("할아버지는 새 수첩을 늘 품에 넣") and qa_nw_seen("바싹 말라 있다"))

testcase v111_nw_d10_room13_half_then_lost:
    # Gate (self-defence): half once, then a wrong answer lists Daram; she still leaves custody.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Function(r13_v111_set,"tries:room13",r13_nw_tries_max("room13")-2)
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("meeting:room13") is None and r13_v111_value("tries:room13")==r13_nw_tries_max("room13")-1)
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    if screen "r13_meeting_retry_choice":
        click id "r13_meeting_retry_accept"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="lose" and r13_v111_value("listed:daram") is True and r13_v111_value("DARAM_DETAINED") is False)
    assert eval qa_nw_seen("몸을 지키려다 지나치게 다치게 한")
    assert eval qa_nw_seen("흰 끈을 맨다")
    assert eval qa_nw_seen("세련이 빈손으로 온다")
    assert eval not qa_nw_seen("편지 일은 따로 확인했어요")
    assert eval (r13_v111_owned("E10_PUMP") and r13_v111_value("grandmother_custody")!="detained")

testcase v111_nw_d10_room13_partial:
    # A later point lost: Daram is freed, the culprit stays 'someone who used the passage'.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:room13",r13_nw_tries_max("room13")-1)
    run Jump("r13_v111_owner_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial" and not r13_v111_value("listed:daram") and r13_v111_value("DARAM_DETAINED") is False)
    assert eval (qa_nw_seen("통로를 쓴 누군가") and qa_nw_seen("편지 일은 따로 물었어요") and r13_v111_value("grandmother_custody")!="detained")

testcase v111_nw_d10_records_lost:
    # Living owl, addressee point lost: Granny keeps the bundle, the old man is listed.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:records",r13_nw_tries_max("records")-1)
    run Jump("r13_v111_authority_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="lose" and r13_v111_value("listed:resident_owlgp") is True and r13_v111_owned("E10_PUMP"))
    assert eval (qa_nw_seen("종이 타는 냄새") and qa_nw_seen("이건 네 엄마가 너희한테 남긴 거") and qa_nw_seen("수레가 오기 전에"))

testcase v111_nw_d10_records_partial:
    # Writing point lost: the family gets the records, the old man stays under watch.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E02"])
    run Function(r13_v111_set,"tries:records",r13_nw_tries_max("records")-1)
    run Jump("r13_v111_writing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="partial" and not r13_v111_value("listed:resident_owlgp"))
    assert eval (qa_nw_seen("기록은 가족이 받으시오") and qa_nw_seen("돌려받은 서류가 탁자 위에 놓여"))

testcase v111_nw_d10_room13_won:
    # Every point held: the notebook line, Sling names Granny, Granny is held.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_contact_answer10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="win" and r13_v111_value("grandmother_custody")=="detained" and not r13_v111_value("listed:daram"))
    assert eval (qa_nw_seen("제가 방을 나설 땐") and qa_nw_seen("본보기를 맡긴 사람") and qa_nw_seen("편지 일은 따로 확인했어요") and not qa_nw_seen("세련이 빈손으로 온다"))

testcase v111_nw_d07_stone_out:
    # Event 07: 2026-10-25 부엉이 예방 1단계로 7일 메뉴 A(남아서 돌을 꺼냄)가 걷혔다. 같은 「돌을 꺼내 눈에 묻는」 일은
    # 이제 7일 낮 자유 시간에 집게를 들고 13호 난로에서 한다(room13_v111_owl_prevent.rpy). 진입을 그 길로 바꿨다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="room13",period=1)
    run Function(r13_v111_set,"tongs7",True)
    run Call("r13_v111_free_day7_pick",7)
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("stove13_7")=="empty") timeout 120
    assert eval (qa_nw_seen("검푸르게 타는 돌을 꺼낸다") and qa_nw_seen("머리가 맑아진다") and r13_v111_owned("NW_STONE"))

testcase v111_nw_d10_five_chances:
    # 회의별 기회(2026-10-24 소유자 결정 5, 쟁점 수 + 2): 13호는 쟁점 다섯이라 7번. 남은 기회가 있으면 증명으로
    # 돌아가고, 마지막 기회를 쓴 오답은 그대로 선다. (시험 이름은 예전 「다섯 번」 그대로 둔다.)
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==1 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==6)
    run Function(r13_v111_set,"tries:room13",5)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==6 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==1)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial" and r13_nw_tries_max("room13")==7)

testcase v111_nw_d10_owner_contact_pin:
    # 0.20.4 proof scope: the exposed copper end on the pin (E08_CONTACT_ASSEMBLY) with the
    # repair record also proves the owner; the next proof shows its new title.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E08_CONTACT_ASSEMBLY"
    pause 0.8
    click "QA V111:E09_PIN_OWNER"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("proof_given:구리선과 수선 출처를 대조한다")==["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"])
    assert eval (R13_CLAIMS["v111:첫 비명 뒤 핀을 다시 채운 때"]["assertion"]=="핀이 언제 떨어졌는가")
    screenshot "v111_nw_d10_time_title.png"
