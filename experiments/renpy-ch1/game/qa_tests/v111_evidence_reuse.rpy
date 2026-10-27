# 2026-10-24 자료 재사용(docs/design/EVIDENCE_CLUTTER_PLAN.md 2부, 소유자 "추천안대로").
# 받을 때 쓸모없어 보이던 자료 10건이 나중 회의의 대체 세트·덧붙임, 또는 인물 반응으로 다시 쓰인다.
# 정답 세트·회의 결론은 그대로다. 보고서: docs/reviews/evidence-reuse-20261024/적용보고.md
init python:
    def qa_reuse_start(day,location="school",**values):
        r13_v111_set("day",day)
        r13_edit(day=day,location=location)
        for k,v in values.items():r13_v111_set(k,v)
    def qa_reuse_text(packets):
        return " ".join((p[1] or "").replace("\n"," ") for p in (packets or []))
    def qa_reuse_ok(key,correct,given):
        return r13_v111_proof_accepts(key,correct,["V111:"+k for k in given])
    def qa_reuse_given(key,keys):
        r13_v111_set("proof_given:"+key,sorted("V111:"+k for k in keys))

testcase evidence_reuse_sets:
    # 덧붙임·대체 세트의 받는 범위. 정답 세트는 그대로 통과하고, 관련 없는 자료는 여전히 떨어진다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    # E14 (11일 돌의 출처): 덧붙임만. 운반표만으로는 안쪽 돌 값을 대신하지 못한다.
    assert eval qa_reuse_ok("요즘 돌이 어디서 오는지 대조한다",["NW_INNER_PRICE","NW_MUSOE_DEEP"],["NW_INNER_PRICE","NW_MUSOE_DEEP","E14"])
    assert eval not qa_reuse_ok("요즘 돌이 어디서 오는지 대조한다",["NW_INNER_PRICE","NW_MUSOE_DEEP"],["E14","NW_MUSOE_DEEP"])
    # E28 (11일 초롱의 하루): 덧붙임. 대체 세트(E11+떨림) 위에도 얹힌다.
    assert eval qa_reuse_ok("초롱과 피코의 하루를 대조한다",["E11","E08","NW_PIKO_TREMOR"],["E11","E08","NW_PIKO_TREMOR","E28"])
    assert eval qa_reuse_ok("초롱과 피코의 하루를 대조한다",["E11","E08","NW_PIKO_TREMOR"],["E11","NW_PIKO_TREMOR","E28"])
    assert eval not qa_reuse_ok("초롱과 피코의 하루를 대조한다",["E11","E08","NW_PIKO_TREMOR"],["E28","NW_PIKO_TREMOR"])
    # E27 (10일 기록 회의): 접수 묶음(E07) 자리를 엄마의 경고 편지가 대신한다. 초대장·발송 순서는 꼭 있어야 한다.
    assert eval qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E27","E09_MAIL"])
    assert eval qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E07","E09_MAIL","E27"])
    assert eval not qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E27"])
    assert eval not qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E27","E09_MAIL"])
    # E35·E29·E34·NW_BURNT_PAGE: 덧붙임만. 혼자서는 통과하지 못한다.
    assert eval qa_reuse_ok("아내가 봤다는 담요의 시점을 확인한다",["E13_MENDING"],["E13_MENDING","E35"])
    assert eval not qa_reuse_ok("아내가 봤다는 담요의 시점을 확인한다",["E13_MENDING"],["E35"])
    assert eval qa_reuse_ok("촌장이 어젯밤 있던 곳을 확인한다",["NW_HALL_WINDOW"],["NW_HALL_WINDOW","E29"])
    assert eval not qa_reuse_ok("촌장이 어젯밤 있던 곳을 확인한다",["NW_HALL_WINDOW"],["E29"])
    assert eval qa_reuse_ok("장부의 두 배를 실룩에게 보인다",["E16"],["E16","E34"])
    assert eval not qa_reuse_ok("장부의 두 배를 실룩에게 보인다",["E16"],["E34"])
    assert eval qa_reuse_ok("맨 처음 이름을 짚는다",["NW_NAMES","NW_NEOUL_LEDGER"],["NW_NAMES","NW_NEOUL_LEDGER","NW_BURNT_PAGE"])
    assert eval not qa_reuse_ok("맨 처음 이름을 짚는다",["NW_NAMES","NW_NEOUL_LEDGER"],["NW_NAMES","NW_BURNT_PAGE"])
    # 다른 회의의 자료는 여전히 덧붙일 수 없다.
    assert eval not qa_reuse_ok("아내가 봤다는 담요의 시점을 확인한다",["E13_MENDING"],["E13_MENDING","E29"])

testcase evidence_reuse_lines:
    # 덧붙인 자료를 냈을 때만 상대가 그 자료를 한 줄로 짚는다. 안 냈으면 그 줄은 없다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ qa_reuse_start(11,family_reunited=True)
    $ qa_reuse_given("초롱과 피코의 하루를 대조한다",["E11","E08","NW_PIKO_TREMOR"])
    $ qa_reuse_given("요즘 돌이 어디서 오는지 대조한다",["NW_INNER_PRICE","NW_MUSOE_DEEP"])
    assert eval ("우리 답장까지" not in qa_reuse_text(r13_nw_block("hyp1_won11")) and "운반표도" not in qa_reuse_text(r13_nw_block("hyp3_won11")))
    $ qa_reuse_given("초롱과 피코의 하루를 대조한다",["E11","E08","NW_PIKO_TREMOR","E28"])
    $ qa_reuse_given("요즘 돌이 어디서 오는지 대조한다",["NW_INNER_PRICE","NW_MUSOE_DEEP","E14"])
    assert eval "우리 답장까지 날라 주셨습니다" in qa_reuse_text(r13_nw_block("hyp1_won11"))
    assert eval "등에서 빠진 돌까지 그 창고로" in qa_reuse_text(r13_nw_block("hyp3_won11"))
    $ qa_reuse_start(10,route7="prevented",OWL_ALIVE=True)
    $ qa_reuse_given("반송·필사본·초대 발송을 대조한다",["E01","E27","E09_MAIL"])
    assert eval ("그 편지는 내가 쓴 게 아니야" in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0034"])) and "여관에 말하지 마" in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0034"])))
    $ qa_reuse_given("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"])
    assert eval "아내가 제게 쓴 편지" not in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0034"]))
    $ qa_reuse_start(13,"square")
    $ qa_reuse_given("아내가 봤다는 담요의 시점을 확인한다",["E13_MENDING","E35"])
    $ qa_reuse_given("촌장이 어젯밤 있던 곳을 확인한다",["NW_HALL_WINDOW","E29"])
    $ qa_reuse_given("장부의 두 배를 실룩에게 보인다",["E16","E34"])
    assert eval "마른 담요 두 장뿐입니다" in qa_reuse_text(r13_v111_lines(["MS14_D13_S03_L0019"]))
    assert eval "지킬 수 있는 말만 하시는 분" in qa_reuse_text(r13_nw_block("badook_won13"))
    assert eval "끝나는 날도 안 적힌 작업표" in qa_reuse_text(r13_nw_block("rein_ledger13"))
    $ qa_reuse_given("아내가 봤다는 담요의 시점을 확인한다",["E13_MENDING"])
    $ qa_reuse_given("촌장이 어젯밤 있던 곳을 확인한다",["NW_HALL_WINDOW"])
    $ qa_reuse_given("장부의 두 배를 실룩에게 보인다",["E16"])
    assert eval ("마른 담요 두 장뿐" not in qa_reuse_text(r13_v111_lines(["MS14_D13_S03_L0019"])) and "지킬 수 있는 말만" not in qa_reuse_text(r13_nw_block("badook_won13")) and "작업표네요" not in qa_reuse_text(r13_nw_block("rein_ledger13")))
    $ qa_reuse_start(14,OWL_ALIVE=False)
    $ qa_reuse_given("맨 처음 이름을 짚는다",["NW_NAMES","NW_NEOUL_LEDGER","NW_BURNT_PAGE"])
    assert eval "날짜를 적던 아이였다고요" in qa_reuse_text(r13_nw_block("altar4_won14"))
    $ qa_reuse_given("맨 처음 이름을 짚는다",["NW_NAMES","NW_NEOUL_LEDGER"])
    assert eval "날짜를 적던 아이였다고요" not in qa_reuse_text(r13_nw_block("altar4_won14"))

testcase evidence_reuse_reactions:
    # 회의에 쓸 자리가 없는 자료는 그 일과 닿은 사람에게 보여 줄 때 다른 면이 보인다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ r13_grant(["V111:NW_MADAM_DAY7","V111:E14","V111:E31","V111:E25"],"qa")
    $ qa_reuse_start(14,family_reunited=True)
    $ qa_rx=r13_v111_present_reaction("npc_pandol","V111:NW_MADAM_DAY7")
    assert eval "그런 돌을 땔 방이 거기 몇이나 되오" in qa_reuse_text(qa_rx)
    $ qa_rx=r13_v111_present_reaction("resident_madam","V111:E14")
    assert eval "제 장부가 기억하고요" in qa_reuse_text(qa_rx)
    $ qa_reuse_start(12,family_reunited=True)
    $ qa_rx=r13_v111_present_reaction("mom","V111:E31")
    assert eval "다음 끼니가 언제일지 몰랐어" in qa_reuse_text(qa_rx)
    # 돌목의 반응은 13호 회의가 결정된 뒤에만 열린다(예방 경로에서는 열리지 않는다).
    assert eval not r13_reaction_day_ok([s for s in R13_REACTIONS["present"] if s["person"]=="guard" and s["evidence"]=="E25"][0])
    $ r13_v111_set("meeting:room13","partial")
    $ qa_rx=r13_v111_present_reaction("guard","V111:E25")
    assert eval "손에 무엇을 쥐고 있었느냐" in qa_reuse_text(qa_rx)
    # 날짜 밖에서는 그 사람의 일반 대답으로 돌아간다.
    $ qa_reuse_start(13)
    $ qa_rx=r13_v111_present_reaction("npc_pandol","V111:NW_MADAM_DAY7")
    assert eval "땔 방이" not in qa_reuse_text(qa_rx)

testcase evidence_reuse_records_alt:
    # 10일 기록 회의를 실제 증명 화면에서 초대장·경고 편지·발송 순서로 이긴다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ qa_reuse_start(10,route7="prevented",OWL_ALIVE=True,DARAM_DETAINED=False)
    $ r13_grant(["V111:E01","V111:E27","V111:E09_MAIL"],"qa")
    run Jump("r13_v111_writing_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA V111:E27"
    pause 0.8
    click "QA V111:E09_MAIL"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="win")
    assert eval (qa_nw_seen("아내가 제게 쓴 편지예요") and qa_nw_seen("할머니의 눈이 편지의 한 줄에서 멎는다") and qa_nw_seen("본보기를 만들었고"))

testcase evidence_reuse_hyp3_extra:
    # 11일 돌의 출처 문항을 실제 증명 화면에서 정답 두 장 + 실룩의 운반표로 낸다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ qa_reuse_start(11,route7="murder",OWL_ALIVE=False,DARAM_DETAINED=False,family_reunited=True,family_school_place=True)
    $ r13_grant(["V111:NW_INNER_PRICE","V111:NW_MUSOE_DEEP","V111:E14"],"qa")
    run Jump("r13_v111_hyp3_proof11")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_INNER_PRICE"
    pause 0.8
    click "QA V111:NW_MUSOE_DEEP"
    pause 0.8
    click "QA V111:E14"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (640,300) until "아이들이 밤을 어디서 보내는지 본다" timeout 60
    assert eval (r13_v111_value("hyp_issue:3")=="won" and qa_nw_seen("등에서 빠진 돌까지 그 창고로 갔어요") and qa_nw_seen("안쪽 돌은 오늘 끄겠소"))

# 2026-10-24 새 사실 1번(docs/reviews/evidence-reuse-20261024/새사실_시안.md, 소유자 "추천안대로"):
# 초상 속 엄마는 바늘을 쥐고 있다(2일 다람의 주문). 10일 기록 회의에서 「손이 아프다」에 덧붙임으로만 쓴다.
# 보고서: docs/reviews/evidence-reuse-20261024/새사실_적용보고.md
testcase evidence_reuse_portrait_needle:
    # 받는 범위와 줄. 초상은 정답 세트·대체 세트 위에 얹히기만 하고, 혼자서는 무엇도 대신하지 못한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E07","E09_MAIL","E09"])
    assert eval qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E27","E09_MAIL","E09"])
    assert eval not qa_reuse_ok("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"],["E01","E09","E09_MAIL"])
    assert eval not qa_reuse_ok("수신인과 가족 전달 권한을 구분한다",["E06_CONTACT","E09_MAIL"],["E06_CONTACT","E09_MAIL","E09"])
    # 2일 주문, 3일 두 판의 그림 속 바늘, 자료 문구.
    assert eval "엄마 손엔 바늘 그려 주세요" in qa_reuse_text(r13_v111_lines(["MS14_D02_S03_L0018"]))
    assert eval "바늘은 따님 주문이에요" in qa_reuse_text(r13_v111_lines(["MS14_D03_S01_L0036"]))
    assert eval "손까지는 다 그려져 있다" in qa_reuse_text(r13_v111_lines(["MS14_D03_S01_L9101"]))
    assert eval all("바늘" in t for t in R13_V111["evidence"]["E09"]["variants"].values())
    # 10일: 초상을 덧붙였을 때만 아빠가 짚고 할머니가 받아친다.
    $ qa_reuse_start(10,route7="prevented",OWL_ALIVE=True)
    $ qa_reuse_given("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL"])
    assert eval "이 초상만으로 아내가 글씨를 부탁했는지까지" not in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0032"]))
    $ qa_reuse_given("반송·필사본·초대 발송을 대조한다",["E01","E07","E09_MAIL","E09"])
    assert eval ("이 초상만으로 아내가 글씨를 부탁했는지까지" in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0032"])) and "그림이야 좋게 그리죠" in qa_reuse_text(r13_v111_lines(["MS14_D10_P01_L0032"])))

testcase evidence_reuse_portrait_proof:
    # 10일 기록 회의를 실제 증명 화면에서 정답 세 장 + 초상으로 이기고, 초상을 짚는 줄이 나온다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    $ qa_reuse_start(10,route7="prevented",OWL_ALIVE=True,DARAM_DETAINED=False)
    $ r13_grant(["V111:E01","V111:E07","V111:E09_MAIL","V111:E09"],"qa")
    run Jump("r13_v111_writing_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA V111:E07"
    pause 0.8
    click "QA V111:E09_MAIL"
    pause 0.8
    click "QA V111:E09"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:records")=="win")
    assert eval (qa_nw_seen("이 초상만으로 아내가 글씨를 부탁했는지까지") and qa_nw_seen("그림이야 좋게 그리죠") and qa_nw_seen("본보기를 만들었고"))
