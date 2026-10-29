init python:
    def qa_nw_day14(route="murder"):
        r13_v111_set("day",14)
        r13_edit(day=14,location="school",period=1)
        r13_v111_set("route7",route)
        r13_v111_set("OWL_ALIVE",route!="murder")
        r13_v111_set("DARAM_DETAINED",False)
        r13_v111_set("family_reunited",True)
        r13_v111_set("family_school_place",True)
        r13_v111_set("all_cart_handed",True)
        r13_v111_set("altar_guide_confirmed",True)
        r13_v111_set("bomi_death_confirmed",True)
        for k in ("piko_alive","KKOMI_ALIVE","nero_alive"):r13_v111_set(k,True)
        r13_v111_set("route12","premeal_stopped")

testcase v111_nw_d14_left_name:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"departed:daram",True)
    run Function(r13_v111_set,"outcome13","partial_rescue")
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("ending14")=="left_name" and qa_nw_seen("다람 몫이었다") and qa_nw_seen("치우지 마"))

testcase v111_nw_d14_frozen:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_set,"nero_alive",False)
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_end_card" timeout 120
    assert eval (r13_v111_value("ending14")=="frozen" and r13_nw_loss_count()==4 and qa_nw_seen("받아 적지 못했다") and qa_nw_seen("이름을 읽던 나비가"))

testcase v111_nw_d14_partial_departed:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"outcome13","partial_rescue")
    run Function(r13_v111_set,"cart_departed",True)
    run Function(r13_edit,location="square")
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_hub" timeout 150
    assert eval (r13_v111_value("ending14")=="partial" and qa_nw_seen("한 줄도 채우지 못했다") and qa_nw_seen("접지 마. 아직 안 왔잖아") and not qa_nw_seen("한 자리 났어"))

testcase v111_nw_d14_altar_lost:
    # Point 1 lost: the irons stay; the day goes on to Granny.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_edit,location="gate")
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:altar",r13_nw_tries_max("altar")-1)
    run Jump("r13_v111_altar1_wrong14")
    click pos (900,600) until "토실에게 함께 듣겠냐고 묻는다" timeout 120
    assert eval (r13_v111_value("meeting:altar")=="lose" and qa_nw_seen("다음 겨울에 다시 정하겠소") and qa_nw_seen("숫자를 보시오"))

testcase v111_nw_d14_altar_half_then_partial:
    # No ledger: the school's three days are only half; the meeting ends partial at best.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_edit,location="gate")
    run Function(r13_grant,["V111:NW_TABLET_A","V111:NW_TABLET_B"],"qa")  # 0.20.5: the next question needs them in hand
    # 2026-10-29 P03: 처음 한 번은 기회를 쓰지 않고 촌장이 되묻는다. 같은 제출을 다시 내면 반쪽이다.
    run SetVariable("v111_claim","v111:희생의 숫자와 장부를 대조한다")
    run SetVariable("v111_last_presented",["V111:E14_SUPPLY"])
    run Jump("r13_v111_altar1_wrong14")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("altar_half1") is None and not r13_v111_value("tries:altar") and qa_nw_seen("아무도 안 무너진다는 건 어디 있소") and not qa_nw_seen("사람 하나에 마을 하나가"))
    run SetVariable("v111_claim","v111:희생의 숫자와 장부를 대조한다")
    run SetVariable("v111_last_presented",["V111:E14_SUPPLY"])
    run Jump("r13_v111_altar1_wrong14")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    assert eval (r13_v111_value("altar_half1") is True and r13_v111_value("meeting:altar") is None and qa_nw_seen("장작은 어디서 나오오"))
    run Function(r13_v111_set,"altar_issue:2","won")
    run Function(r13_v111_set,"altar_issue:3","won")
    run Function(r13_v111_set,"altar_issue:4","won")
    run Jump("r13_v111_altar_close14")
    pause 2.0
    assert eval (r13_v111_value("meeting:altar")=="partial")

testcase v111_nw_d14_bomi:
    # Bomi's record, the burnt page, the stone and the day-7 ledger line before Granny.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"meeting:room13","win")
    run Function(r13_v111_set,"grandmother_custody","detained")
    run Function(r13_grant,["V111:NW_NEOUL_LEDGER","V111:NW_BURNT_PAGE","V111:NW_STONE"],"qa")
    run Function(r13_edit,location="gate")
    run Jump("r13_v111_granny_interview14")
    click pos (900,600) until "밖에서 기다리고, 확인한 일을 나중에 말해 주겠다고 한다" timeout 120
    click "밖에서 기다리고, 확인한 일을 나중에 말해 주겠다고 한다"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("마지막 날짜 옆에") and qa_nw_seen("여기, 그 애가 적은 날짜가 있네") and qa_nw_seen("우리 집 불이 되잖아") and qa_nw_seen("털어놓았다고 풀려나지는 않는다") and not qa_nw_seen("그 애는 날짜도 몰랐어"))

testcase v111_nw_d14_true_ending:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_v111_set,"ending14","morning")
    run Function(r13_grant,["V111:NW_NEOUL_LEDGER"],"qa")
    run Function(r13_v111_set,"meeting:records","win")
    run Function(r13_v111_set,"meeting:hypothesis","win")
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_v111_set,"meeting:altar","win")
    # 2026-10-24: 진엔딩 조건에 불·수프 대승리가 더해졌다(GRAND_WIN_DESIGN.md 2-5).
    run Function(r13_v111_set,"grand:fire",True)
    run Function(r13_v111_set,"grand:soup",True)
    run Jump("r13_v111_cookie14")
    click pos (900,600) until screen "r13_end_card" timeout 150
    assert eval (r13_v111_value("ending14")=="true" and qa_nw_seen("여기만이 아닐지도 몰라") and qa_nw_seen("닫음"))

testcase v111_nw_d14_altar_without_records:
    # 0.20.5 (Codex T01): no ledger and none of the later records: each question is named as
    # unanswerable, no chance is spent, and the meeting ends partial without a dead-end proof.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_edit,location="gate")
    run Function(r13_v111_set,"altar1_half_asked",True)  # 2026-10-29 P03: 첫 되묻기는 이미 들은 판
    run SetVariable("v111_last_presented",["V111:E14_SUPPLY"])
    run Jump("r13_v111_altar1_wrong14")
    click pos (900,600) until eval (r13_v111_value("meeting:altar") is not None) timeout 120
    assert eval (r13_v111_value("meeting:altar")=="partial" and not r13_v111_value("tries:altar") and qa_nw_seen("지금 내 손에는 다 없다"))
