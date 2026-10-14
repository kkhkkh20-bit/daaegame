# Ren'Py UI tests: dev/run_renpy_tests.sh <name>... (not shipped; build excludes qa_tests/)

testcase newgame:
    pause 2.0
    click "처음부터"
    pause 4.0
    screenshot "n_01.png"
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(ctx=renpy.exports.get_screen("main_menu") is not None, room=(renpy.store.room13 or {}).get("location") if hasattr(renpy.store,"room13") else None)))

testcase trial_missing:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05'),())
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이만 그럴 수 있었다는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "m_board.png"
    click "결론을 말한다"
    pause 1.0
    click "다른 길이 있으니"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result") in ("detained","cleared","culprit_proven") timeout 120
    pause 0.5
    screenshot "m_verdict.png"
    $ r13_qa_dump()

testcase trial_giveup:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E06', 'E07', 'E09'),())
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E01"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E01"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "g_board.png"
    click "반론을 그만둔다"
    pause 1.0
    click "반론을 그만둔다"
    pause 0.5
    click pos (640,600) until eval room13.get("trial_result") in ("detained","cleared","culprit_proven") timeout 120
    pause 0.5
    screenshot "g_verdict.png"
    $ r13_qa_dump()

testcase trial_win:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E06', 'E07', 'E09'),())
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E06"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E07"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "w_ready.png"
    click "결론을 말한다"
    pause 1.0
    click "누군가가 냈다"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result") in ("detained","cleared","culprit_proven") timeout 120
    pause 0.5
    screenshot "w_verdict.png"
    $ r13_qa_dump()

testcase trial_full:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E36'),())
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이만 그럴 수 있었다는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "다른 길이 있으니"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E06"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E07"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "할머니가 어르신을 죽였다"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "f_after_wrong.png"
    click "결론을 말한다"
    pause 1.0
    click "누군가가 냈다"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "그때 식당에 있었다는 말"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    run Return(("select","s2"))
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E12"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "주방에서 그 방까지"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "도우러 들어갔을 뿐이라는 변명"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E13"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E15"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E14"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E36"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "구하다 주운 게 아니라"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result")=="culprit_proven" and room13.get("granny_state")=="detained" timeout 120
    pause 0.5
    screenshot "f_verdict.png"
    $ r13_qa_dump()

testcase trial_gate_unenforced:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E36'),("-gates","witness:nabi","witness:tok"))
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이만 그럴 수 있었다는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "다른 길이 있으니"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E06"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E07"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "할머니가 어르신을 죽였다"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "f_after_wrong.png"
    click "결론을 말한다"
    pause 1.0
    click "누군가가 냈다"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "그때 식당에 있었다는 말"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    run Return(("select","s2"))
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E12"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "주방에서 그 방까지"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "도우러 들어갔을 뿐이라는 변명"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E13"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E15"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E14"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E36"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "구하다 주운 게 아니라"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result") in ("detained","cleared","culprit_proven") timeout 120
    pause 0.5
    screenshot "gu_verdict.png"
    $ r13_flag("qa_marker")
    $ r13_qa_dump()

testcase trial_gate_no_witness:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E36'),("-gates",))
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이만 그럴 수 있었다는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "다른 길이 있으니"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E06"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E07"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "할머니가 어르신을 죽였다"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "f_after_wrong.png"
    click "결론을 말한다"
    pause 1.0
    click "누군가가 냈다"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result") in ("detained","cleared","culprit_proven") timeout 120
    pause 0.5
    screenshot "gn_verdict.png"
    $ r13_qa_dump()

testcase finale_win:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_finale",('E16', 'E18', 'E20', 'E21', 'E23', 'E25', 'E26', 'E31'),('operators_ready', 'patient_transport', 'shelter_ready', 'supplies_ready'))
    pause 1.0
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    click "누구도 돌아오지 못함"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E20"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E31"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "아무도 돌아올 수 없다"
    pause 0.6
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    click "돌릴 방법이 없다"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E23"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E21"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "갈수록 짧아졌다"
    pause 0.6
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    click "오늘 밤 희생 없이"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E25"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E26"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "fi_f3_ready.png"
    click "결론을 말한다"
    pause 1.0
    click "손으로 교대하며"
    pause 0.6
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    click "질서를 깨뜨려"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E18"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E16"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "엄마를 다시 붙잡으려고"
    pause 0.6
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    screenshot "fi_hub.png"
    $ r13_qa_dump()
    click "모은 근거와 해 둔 준비로"
    pause 1.0
    click "사람들과 움직인다"
    pause 1.0
    click pos (640,600) until eval room13.get("ending") is not None timeout 120
    pause 0.5
    screenshot "fi_ending.png"
    $ r13_qa_dump()

testcase finale_missing:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_finale",('E20',),('operators_ready', 'patient_transport', 'shelter_ready', 'supplies_ready'))
    pause 1.0
    click pos (640,600) until screen "r13_crisis" timeout 60
    pause 0.6
    screenshot "fm_hub.png"
    click "모은 근거와 해 둔 준비로"
    pause 1.0
    click "사람들과 움직인다"
    pause 1.0
    click pos (640,600) until eval room13.get("ending") is not None timeout 120
    pause 0.5
    $ r13_qa_dump()

testcase shop_flow:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_shop")
    pause 2.0
    screenshot "s_eunho_topics.png"
    click "물건을 산다"
    pause 1.5
    screenshot "s_shop.png"
    click "등잔 기름"
    pause 0.8
    screenshot "s_shop_pick.png"
    click "4냥에 사기"
    pause 0.8
    click "›"
    pause 0.8
    screenshot "s_shop_p2.png"
    click "정밀 줄칼"
    pause 0.5
    click "7냥에 사기"
    pause 0.5
    click "두꺼운 담요"
    pause 0.5
    click "5냥에 사기"
    pause 0.8
    screenshot "s_shop_bought.png"
    $ t1=[k for k,s in r13_topics("resident_tok")]
    $ r13_finish_topic("item:file")
    $ b1=[k for k,s in r13_topics("bami")]
    $ r13_finish_topic("item:blanket")
    $ b2=[k for k,s in r13_topics("bami")]
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(tok_before=t1,E13="E13" in room13["evidence"],bami_before=b1,bami_after=b2,help=room13.get("resident_help"),wallet=r13_wallet(room13)["items"])))

testcase items_chain:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ renpy.store.r13_qa_items_chain()

testcase fresh_run:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(endings=list(persistent.room13_endings),route=room13.get("secret_route_unlocked"),archive=r13_learning_archive_keys(),avail=r13_secret_route_available())))

testcase carriage_skip:
    pause 2.0
    click "처음부터"
    pause 3.0
    screenshot "c0_carriage.png"
    click "건너뛰기"
    pause 1.0
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "c1_after.png"
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(loc=room13["location"],day=room13["day"],period=room13["period"])))

testcase carriage_view:
    pause 2.0
    click "처음부터"
    pause 3.0
    screenshot "v0_narration.png"
    click pos (640,600)
    pause 0.12
    screenshot "v1_pop_mid.png"
    pause 1.5
    screenshot "v2_daram.png"
    click pos (640,600)
    pause 1.2
    click pos (640,600)
    pause 1.2
    screenshot "v3_dad_line.png"
    $ open(renpy.config.basedir+"/qa_result.txt","w").write(repr(dict(place=place,motion=r13_motion_person,showing=list(renpy.get_showing_tags()))))

testcase override_chain:
    pause 1.0
    $ r13_qa_override_chains(R13_QA_CHAIN_NAMES)

# ---- Town events bundle 1 (systems/room13_town_events.rpy) ----

testcase town_b_first_run:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=1,location="store",life_poc=True))
    click pos (640,600) until screen "choice" timeout 40
    screenshot "tb1_choice.png"
    click "지붕을 따라 쫓아간다"
    click pos (640,600) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase town_b_ambush_musoe:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=1,location="workshop",life_poc=True),("somi_route_seen","ep4_seen","ep1_done"))
    click pos (640,600) until screen "choice" timeout 40
    click "골목 입구에서 기다린다"
    click pos (640,600) until screen "choice" timeout 40
    screenshot "tb2_caught.png"
    click "무쇠 할아버지에게 직접 가져다준다"
    click pos (640,600) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase town_b_alley_sell:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=1,location="store",life_poc=True))
    click pos (640,600) until screen "choice" timeout 40
    click "수리점 쪽 골목으로 돌아가 앞질러 간다"
    click pos (640,600) until screen "choice" timeout 40
    click "꾸러미를 빼앗아 은호 사장에게 판다"
    click pos (640,600) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase town_c_locked:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=2,location="inn",life_poc=True,evidence=["E18"]),("ev_b_done",))
    click pos (640,600) until screen "choice" timeout 40
    screenshot "tc1_offer.png"
    click "받아들인다"
    click pos (640,600) until screen "r13_hub" timeout 60
    screenshot "tc1_after.png"
    $ r13_qa_town_dump()

testcase town_c_wedge:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=2,location="inn",life_poc=True),("ev_b_done",),("wedge",))
    click pos (640,600) until screen "choice" timeout 40
    click "쐐기를 챙겨 들고 받아들인다"
    click pos (640,600) until screen "r13_hub" timeout 60
    $ r13_qa_town_dump()

testcase town_c_mungchi:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=2,location="inn",life_poc=True),("ev_b_done",))
    click pos (640,600) until screen "choice" timeout 40
    click "받아들이는 척하고 13호로 돌아와 숨어 기다린다"
    click pos (640,600) until screen "r13_hub" timeout 60
    $ r13_qa_town_dump()

testcase town_n_yeoni:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=1,location="square",life_poc=True),("ev_b_done","ev_c_done","room_searched"),(),5)
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_yeoni")
    click pos (1150,90) until "교환대의 낯익은 물건을 묻는다" timeout 30
    click "교환대의 낯익은 물건을 묻는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "3냥에 되산다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    click "돌아가기"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_mungchi")
    click pos (1150,90) until "13호에서 가져간 물건을 따진다" timeout 30
    click "13호에서 가져간 물건을 따진다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    pause 0.5
    $ r13_qa_town_dump()

testcase town_m_kongi:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),(),(),4)
    click pos (640,600) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_kongi")
    click pos (1150,90) until "하루 동안 한 곳을 지켜봐 달라고 한다" timeout 30
    click "하루 동안 한 곳을 지켜봐 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "수리점 뒤 골목"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    click "돌아가기"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ room13["day"]=3
    $ r13_town_daily()
    run Call("r13_qa_talk","resident_kongi")
    click pos (1150,90) until "어제 지켜본 것을 듣는다" timeout 30
    click "어제 지켜본 것을 듣는다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    pause 0.5
    $ r13_qa_town_dump()


# ---- Episodes (systems/room13_episodes.rpy) ----

testcase ep1_bami_safe:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=2,location="inn",life_poc=True))
    click pos (1150,90) until screen "choice" timeout 40
    click "검사가 무엇인지 묻는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "못 봤다고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",3,1,"hall")
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "e1_eaves.png"
    click "바둑이를 설득해 순찰에서 처마를 빼 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",4,0,"inn")
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase ep1_bami_taken:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=2,location="inn",life_poc=True))
    click pos (1150,90) until screen "choice" timeout 40
    click "못 봤다고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",3,1,"hall")
    click pos (1150,90) until screen "choice" timeout 40
    click "지금은 할 수 있는 게 없다고 말한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",4,0,"inn")
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase ep2_nabi:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=2,location="kitchen",life_poc=True))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "e2_kitchen.png"
    click "짐을 같이 날라 준다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_edit(day=3,period=1,location="dining")
    run Call("r13_qa_talk","nabi")
    click pos (1150,90) until "아이들 끼니를 다른 데서 구하자고 한다" timeout 30
    click "아이들 끼니를 다른 데서 구하자고 한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "학교 곰 선생님에게 부탁해 보자고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    click "돌아가기"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_teacher")
    click pos (1150,90) until "표 없는 아이들을 학교 급식에 넣어 달라고 한다" timeout 30
    click "표 없는 아이들을 학교 급식에 넣어 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    click "돌아가기"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_edit(day=4,period=0,location="dining")
    run Call("r13_qa_talk","nabi")
    click pos (1150,90) until "이제 본 대로 말해 줄 수 있는지 묻는다" timeout 30
    click "이제 본 대로 말해 줄 수 있는지 묻는다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    $ r13_qa_town_dump()

testcase ep3_stone:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=2,location="square",life_poc=True,case_state="occurred"),("know_stone_history","ep1_done","ev_b_done","ev_c_done"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "e3_bell.png"
    click "우박에게 지금 돌의 출력을 재 보라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_edit(day=6,period=1,location="post")
    run Call("r13_qa_talk","resident_ppul")
    click pos (1150,90) until "재판을 증거대로 열어 달라고 요구한다" timeout 30
    click "재판을 증거대로 열어 달라고 요구한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "돌의 옛 기록과 지금의 출력을 함께 보여 준다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    $ r13_qa_town_dump()

testcase ep4_tok:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="workshop",life_poc=True),("ep1_done","ev_b_done"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "e4_accused.png"
    click "광장 등을 직접 살펴본다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "톡의 편을 든다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_ubak")
    click pos (1150,90) until "광장 등 뚜껑의 나사 자국을 묻는다" timeout 30
    click "광장 등 뚜껑의 나사 자국을 묻는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "서리 검사원에게 가서 함께 해명하게 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    click "돌아가기"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_edit(day=4)
    run Call("r13_qa_talk","resident_tok")
    click pos (1150,90) until "재판에서 핀 이야기를 직접 해 달라고 한다" timeout 30
    click "재판에서 핀 이야기를 직접 해 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    $ r13_qa_town_dump()

# ---- Town events bundle 2 (systems/room13_town_events2.rpy) ----

testcase town_a_extort:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="square",life_poc=True),("ep1_done",),(),2)
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "ta_offer.png"
    click "물건을 받아 오면 그때 주겠다고 한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "백 부인 빚 때문이냐고 정면으로 묻는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "입막음 값으로 여덟 냥을 받는다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ r13_qa_town_dump()

testcase town_q_certificate:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=1,location="inn",life_poc=True))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "tq_offer.png"
    click "서리 검사원의 건강 확인서를 받아 두고 옮긴다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",3,1,"post",("ep1_done",))
    click pos (1150,90) until screen "r13_hub" timeout 60
    $ r13_qa_town_dump()

testcase town_q_quarantine:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=1,location="inn",life_poc=True))
    click pos (1150,90) until screen "choice" timeout 40
    click "그 방으로 옮긴다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    $ r13_qa_town_dump()

testcase medkit_musoe:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=0,location="workshop",life_poc=True),("ep1_done","ev_b_done","ep4_seen","tok_cleared"),("medkit",))
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_talk","resident_musoe")
    click pos (1150,90) until "도시제 약상자를 건넨다" timeout 30
    click "도시제 약상자를 건넨다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    $ r13_qa_town_dump()

testcase sound_places:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_sound")
    pause 120.0
