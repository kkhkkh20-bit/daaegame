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
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"false_message_admitted",False)
    run Function(r13_nw_list,"daram","room13_lose")
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_v111_set,"tries:blanket",r13_nw_tries_max("blanket")-1)
    run Jump("r13_v111_mending_wrong13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:blanket")=="lose" and r13_v111_value("departed:daram") is True and r13_v111_value("departed:resident_tok") is True and r13_v111_value("departed:npc_pandol") is True)
    assert eval (r13_v111_value("outcome13")=="partial_rescue" and r13_v111_value("cart_departed") is True)
    assert eval (qa_nw_seen("아무도 내리지 못한다") and qa_nw_seen("바퀴가 더 빠르다"))

testcase v111_nw_d13_badook_partial:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run SetVariable("v111_last_presented",["V111:E01"])
    run Function(r13_v111_set,"tries:blanket",r13_nw_tries_max("blanket")-1)
    run Jump("r13_v111_badook_wrong13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:blanket")=="partial" and qa_nw_seen("어르신 곁에 있었습니다") and qa_nw_seen("내리겠소"))

testcase v111_nw_d13_cart_names:
    # The cart carries the names the meetings listed; a living Piko says what was under the portrait.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
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
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_v111_set,"meeting:hypothesis","win")
    run Function(r13_grant,["V111:E16","V111:NW_PIKO_PAINTING"],"qa")
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "자료 고르기"
    pause 0.5
    click "QA V111:E16"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_PIKO_PAINTING"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until "엄마와 다람이 곁에 남게 한다" timeout 60
    assert eval (r13_v111_value("meeting:piko")=="win" and r13_v111_value("neoul_held") is True and r13_v111_owned("NW_NEOUL_LEDGER") and r13_v111_value("NW_NEOUL_LEDGER.variant")=="full")
    assert eval (qa_nw_seen("너울 씨가 시켰어요") and qa_nw_seen("그러면 다 죽소"))

testcase v111_nw_d13_rein_painting_first:
    # Painting first: "죽은 화가의 낙서요" and the re-investigation is lost.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Function(r13_grant,["V111:E16","V111:NW_PIKO_PAINTING"],"qa")
    run Function(r13_v111_set,"tries:piko",r13_nw_tries_max("piko")-1)
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 60
    pause 1.0
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_PIKO_PAINTING"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until "엄마와 다람이 곁에 남게 한다" timeout 60
    assert eval (r13_v111_value("meeting:piko")=="lose" and not r13_v111_value("neoul_held") and not r13_v111_owned("NW_NEOUL_LEDGER") and qa_nw_seen("화가의 낙서요"))

testcase v111_nw_d13_partial_listed:
    # Badook partial: listed passengers stay aboard with the others; Daram comes down at once.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
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

testcase v111_nw_d13_cleanup_bundled:
    # 0.20.12 (후반 기획서 C안): 구조 뒤 다섯 확인을 바둑이·돌목·까로 세 대화로 묶는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_edit,location="square")
    run Function(r13_v111_set,"all_cart_handed",True)
    run Jump("r13_v111_driver_refuse13")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("Kkaro_forced_transport_refused") is True and r13_v111_value("cart_returned") is True and qa_nw_seen("은호 씨한테 돌려드리죠"))
    assert eval ([o["index"] for o in r13_v111_binding()["options"] if o.get("person") in ("karo","guard","resident_badook")]==[0,1])
    run Jump("r13_v111_order_stop13")
    click pos (900,600) until screen "r13_book" timeout 120
    assert eval (r13_v111_value("current_order_execution_stopped") is True and qa_nw_seen("막을 사람이 있어야 해"))
    # 2026-10-29 외부 검토 「행동이 질문 목록 안에 있다」: 처음 책을 그냥 닫으면, 다시 보이는 일은 돌목의 질문이 아니라
    # 너울에게 하는 「자료 제시」다. 너울을 눌러 사본을 내면 받아들인 장면으로 간다.
    run Show("r13_qa_inject_return",value=None)
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval ("neoul" in r13_visible_people() and r13_v111_questions("neoul")==[] and not [q for q in r13_v111_questions("guard") if "너울" in q[0]])
    assert eval (r13_v111_present_index(r13_v111_binding(),"neoul","V111:E13_ORDER")==4)
    run Show("r13_qa_inject_return",value=("person","neoul"))
    pause until screen "r13_topics" timeout 30
    run Show("r13_qa_inject_return",value="present")
    pause until screen "r13_book" timeout 30
    run Show("r13_qa_inject_return",value="V111:E13_ORDER")
    click pos (900,600) until eval (r13_v111_value("relay_stopped") is True and renpy.get_screen("r13_hub") is not None) timeout 120
    assert eval (r13_v111_value("relay_stopped") is True)
    assert eval ([o["index"] for o in r13_v111_binding()["options"] if o.get("person") in ("karo","guard","resident_badook")]==[0])
