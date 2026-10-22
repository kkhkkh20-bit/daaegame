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
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
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
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Function(r13_v111_set,"tries:room13",R13_NW_TRIES-2)
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("meeting:room13") is None and r13_v111_value("tries:room13")==R13_NW_TRIES-1)
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
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
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:room13",R13_NW_TRIES-1)
    run Jump("r13_v111_owner_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial" and not r13_v111_value("listed:daram") and r13_v111_value("DARAM_DETAINED") is False)
    assert eval (qa_nw_seen("통로를 쓴 누군가") and qa_nw_seen("편지 일은 따로 물었어요") and r13_v111_value("grandmother_custody")!="detained")

testcase v111_nw_d10_records_lost:
    # Living owl, addressee point lost: Granny keeps the bundle, the old man is listed.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:records",R13_NW_TRIES-1)
    run Jump("r13_v111_authority_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="lose" and r13_v111_value("listed:resident_owlgp") is True and r13_v111_owned("E10_PUMP"))
    assert eval (qa_nw_seen("종이 타는 냄새") and qa_nw_seen("이건 네 엄마가 너희한테 남긴 거") and qa_nw_seen("수레가 오기 전에"))

testcase v111_nw_d10_records_partial:
    # Writing point lost: the family gets the records, the old man stays under watch.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E02"])
    run Function(r13_v111_set,"tries:records",R13_NW_TRIES-1)
    run Jump("r13_v111_writing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="partial" and not r13_v111_value("listed:resident_owlgp"))
    assert eval (qa_nw_seen("기록은 가족이 받으시오") and qa_nw_seen("돌려받은 서류가 탁자 위에 놓여"))

testcase v111_nw_d10_room13_won:
    # Every point held: the notebook line, Sling names Granny, Granny is held.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Jump("r13_v111_contact_answer10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="win" and r13_v111_value("grandmother_custody")=="detained" and not r13_v111_value("listed:daram"))
    assert eval (qa_nw_seen("제가 방을 나설 땐") and qa_nw_seen("본보기를 맡긴 사람") and qa_nw_seen("편지 일은 따로 확인했어요") and not qa_nw_seen("세련이 빈손으로 온다"))

testcase v111_nw_d07_stone_out:
    # Event 07 path A: Dad takes the stone out and the old man calls Buri's name.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",7)
    run Function(r13_edit,day=7,location="room13")
    run Function(r13_v111_set,"route7","prevented")
    run Function(r13_v111_set,"prevention","A")
    run Jump("r13_v111_prevent_a7")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("검푸르게 타는 돌이다") and qa_nw_seen("부리는 어디 있나"))

testcase v111_nw_d10_five_chances:
    # Five chances per meeting (owner, 2026-10-22): four wrong answers go back to the proof with a notice; the fifth stands.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==1 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==4)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==2 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==3)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==3 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==2)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==4 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==1)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial" and R13_NW_TRIES==5)

testcase v111_nw_d10_owner_contact_pin:
    # 0.20.4 proof scope: the exposed copper end on the pin (E08_CONTACT_ASSEMBLY) with the
    # repair record also proves the owner; the next proof shows its new title.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "근거를 내놓는다"
    pause 0.5
    click "QA V111:E08_CONTACT_ASSEMBLY"
    pause 0.8
    click "QA V111:E09_PIN_OWNER"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "논리를 연결한다"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("proof_given:구리선과 수선 출처를 대조한다")==["V111:E08_CONTACT_ASSEMBLY","V111:E09_PIN_OWNER"])
    assert eval (R13_CLAIMS["v111:첫 비명 뒤 핀을 다시 채운 때"]["assertion"]=="핀이 언제 떨어졌는가")
    screenshot "v111_nw_d10_time_title.png"
