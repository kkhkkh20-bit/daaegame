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
    assert eval (qa_nw_seen("펼쳐 놓은 수첩을 자꾸 들여다보더라") and qa_nw_seen("제가 넣은 돌이 아닙니다") and qa_nw_seen("그런데 그게 없어요") and qa_nw_seen("바싹 말라 있다"))

testcase v111_nw_d10_room13_half_then_lost:
    # Gate (self-defence): half once, then a wrong answer lists Daram; she still leaves custody.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Function(r13_v111_set,"tries:room13",1)
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("meeting:room13") is None and r13_v111_value("tries:room13")==2)
    run SetVariable("v111_last_presented",["V111:E08_TOOL"])
    run Jump("r13_v111_hearing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="lose" and r13_v111_value("listed:daram") is True and r13_v111_value("DARAM_DETAINED") is False)
    assert eval qa_nw_seen("과잉방위요")
    assert eval qa_nw_seen("흰 끈을 맨다")
    assert eval qa_nw_seen("세련이 빈손으로 온다")
    assert eval not qa_nw_seen("본떴다고 인정했어요")
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
    run Function(r13_v111_set,"tries:room13",2)
    run Jump("r13_v111_owner_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial" and not r13_v111_value("listed:daram") and r13_v111_value("DARAM_DETAINED") is False)
    assert eval (qa_nw_seen("통로를 쓴 누군가") and qa_nw_seen("여관으로 돌려보냈습니다") and r13_v111_value("grandmother_custody")!="detained")

testcase v111_nw_d10_records_lost:
    # Living owl, addressee point lost: Granny keeps the bundle, the old man is listed.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:records",2)
    run Jump("r13_v111_authority_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="lose" and r13_v111_value("listed:resident_owlgp") is True and r13_v111_owned("E10_PUMP"))
    assert eval (qa_nw_seen("종이 타는 냄새") and qa_nw_seen("저 사람한테는 안 보였어") and qa_nw_seen("수레가 오기 전에"))

testcase v111_nw_d10_records_partial:
    # Writing point lost: the family gets the records, the old man stays under watch.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"prevented")
    run SetVariable("v111_last_presented",["V111:E02"])
    run Function(r13_v111_set,"tries:records",2)
    run Jump("r13_v111_writing_wrong10")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="partial" and not r13_v111_value("listed:resident_owlgp"))
    assert eval (qa_nw_seen("관찰 대상으로 적겠소") and qa_nw_seen("돌려받은 것은 전부인가"))

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
    assert eval (qa_nw_seen("책상에는 서류뿐이었습니다") and qa_nw_seen("본보기를 맡긴 사람") and qa_nw_seen("본떴다고 인정했어요") and not qa_nw_seen("세련이 빈손으로 온다"))

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

testcase v111_nw_d10_three_chances:
    # Three chances: two wrong answers go back to the proof with a notice; the third stands.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==1 and r13_v111_value("meeting:room13") is None and r13_nw_tries_left("room13")==2)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("tries:room13")==2 and r13_v111_value("meeting:room13") is None)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Jump("r13_v111_owner_wrong10")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:room13")=="partial")
