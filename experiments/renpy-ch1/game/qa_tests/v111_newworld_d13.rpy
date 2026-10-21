init python:
    def qa_nw_day13():
        r13_v111_set("day",13)
        r13_edit(day=13,location="square",period=2)
        r13_v111_set("route7","murder")
        r13_v111_set("OWL_ALIVE",False)
        r13_v111_set("DARAM_DETAINED",False)
        r13_v111_set("family_reunited",True)
        r13_v111_set("family_school_place",True)
        r13_v111_set("family_deal",False)
        r13_v111_set("false_message_admitted",True)

testcase v111_nw_d13_cart_left_with_daram:
    # Blanket point lost: the cart leaves with everyone on it, Daram too.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"false_message_admitted",False)
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_v111_set,"tries:blanket",2)
    run Jump("r13_v111_mending_wrong13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:blanket")=="lose" and r13_v111_value("departed:daram") is True and r13_v111_value("departed:resident_tok") is True and r13_v111_value("departed:npc_pandol") is True)
    assert eval (r13_v111_value("outcome13")=="partial_rescue" and r13_v111_value("cart_departed") is True)
    assert eval (qa_nw_seen("아무도 내리지 못한다") and qa_nw_seen("바퀴가 더 빠르다"))

testcase v111_nw_d13_badook_partial:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:blanket",2)
    run Jump("r13_v111_badook_wrong13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:blanket")=="partial" and qa_nw_seen("어르신 곁에 있었습니다") and qa_nw_seen("내리겠소"))

testcase v111_nw_d13_cart_names:
    # The cart carries the names the meetings listed; a living Piko says what was under the portrait.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_nw_list,"resident_piko","street")
    run Function(r13_v111_set,"meeting:blanket","win")
    run Jump("r13_v111_cart_observed13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 120
    assert eval (qa_nw_seen("톡이 공구 자루") and qa_nw_seen("모과 씨예요") and r13_v111_owned("NW_PIKO_PAINTING") and r13_v111_value("NW_PIKO_PAINTING.variant")=="told")

testcase v111_nw_d13_rein_won:
    # The ledger's double price, then the painting: Neoul is held, his ledger is taken.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_v111_set,"meeting:hypothesis","win")
    run Function(r13_grant,["V111:E16","V111:NW_PIKO_PAINTING"],"qa")
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "근거를 내놓는다"
    pause 0.5
    click "QA V111:E16"
    pause 0.8
    click "논리를 연결한다"
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "근거를 내놓는다"
    pause 0.5
    click "QA V111:NW_PIKO_PAINTING"
    pause 0.8
    click "논리를 연결한다"
    click pos (900,600) until "곁에 남는다" timeout 60
    assert eval (r13_v111_value("meeting:piko")=="win" and r13_v111_value("neoul_held") is True and r13_v111_owned("NW_NEOUL_LEDGER") and r13_v111_value("NW_NEOUL_LEDGER.variant")=="full")
    assert eval (qa_nw_seen("너울 씨가 시켰어요") and qa_nw_seen("그럼 다 죽소"))

testcase v111_nw_d13_rein_painting_first:
    # Painting first: "죽은 화가의 낙서요" and the re-investigation is lost.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_grant,["V111:E16","V111:NW_PIKO_PAINTING"],"qa")
    run Function(r13_v111_set,"tries:piko",2)
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "근거를 내놓는다"
    pause 0.5
    click "QA V111:NW_PIKO_PAINTING"
    pause 0.8
    click "논리를 연결한다"
    click pos (900,600) until "곁에 남는다" timeout 60
    assert eval (r13_v111_value("meeting:piko")=="lose" and not r13_v111_value("neoul_held") and not r13_v111_owned("NW_NEOUL_LEDGER") and qa_nw_seen("화가의 낙서요"))

testcase v111_nw_d13_partial_listed:
    # Badook partial: listed passengers stay aboard with the others; Daram comes down at once.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_v111_set,"cart_roster",["npc_pandol","resident_momo","resident_guldol"])
    run Function(r13_v111_set,"meeting:blanket","partial")
    run Function(r13_v111_set,"cart_stopped",True)
    run Jump("r13_v111_after_rein13")
    click pos (640,300) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("handed:daram") is True and "resident_tok" in r13_v111_value("cart_roster") and "daram" not in r13_v111_value("cart_roster"))
    assert eval (qa_nw_seen("까로가 다람의 손목 끈을 푼다"))
