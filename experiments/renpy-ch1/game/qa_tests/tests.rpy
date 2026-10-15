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
    click "아이뿐이라는 주장"
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
    click "아이뿐이라는 주장"
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
    click "아이뿐이라는 주장"
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
    click "아이뿐이라는 주장"
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
    click pos (640,600) until screen "choice" timeout 40
    click "문을 살펴본다"
    click pos (640,600) until screen "choice" timeout 40
    click "안으로 들어간다"
    click pos (640,600) until screen "choice" timeout 40
    click "문을 밀어 본다"
    click pos (640,600) until screen "choice" timeout 40
    click "안쪽 선반을 살핀다"
    click pos (640,600) until screen "choice" timeout 40
    click "문을 두드리며 기다린다"
    click pos (640,600) until screen "r13_hub" timeout 60
    assert eval (r13_has("observed:store_door") and "H1" not in room13["evidence"] and room13["day"]==4)
    screenshot "tc1_after.png"
    $ r13_qa_town_dump()

testcase town_c_wedge:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=2,location="inn",life_poc=True),("ev_b_done",),("wedge",))
    click pos (640,600) until screen "choice" timeout 40
    click "받아들인다"
    click pos (640,600) until screen "choice" timeout 40
    click "가진 물건을 문에 써 본다"
    click pos (640,600) until screen "choice" timeout 40
    click "나무 쐐기"
    click pos (640,600) until screen "choice" timeout 40
    click "안으로 들어간다"
    click pos (640,600) until screen "choice" timeout 40
    assert eval ("H1" not in room13["evidence"])
    click "안쪽 선반을 살핀다"
    click pos (640,600) until screen "choice" timeout 40
    click "문틈으로 빗장을 들어 올려 나간다"
    click pos (640,600) until screen "r13_hub" timeout 60
    assert eval ("H1" in room13["evidence"] and r13_has("room_searched") and room13["day"]==3)
    $ r13_qa_town_dump()

testcase town_c_mungchi:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=2,location="inn",life_poc=True),("ev_b_done",))
    click pos (640,600) until screen "choice" timeout 40
    click "받는 척하고 13호에 숨어 기다린다"
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
    click "바둑이에게 처마 순찰을 빼 달라고 한다"
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
    click "음식 짐을 같이 날라 준다"
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
    click "돌의 옛 기록과 지금 출력을 보여 준다"
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
    click "증거도 없이 가둘 겁니까"
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
    click "짐을 받아 오면 돈을 주겠다고 한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "백 부인 빚 때문입니까"
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
    click "건강 확인서를 받아 두고 옮긴다"
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

testcase skip_modes:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="workshop",life_poc=True),("ep1_done","ev_b_done"))
    pause until screen "say" timeout 30
    pause 1.0
    screenshot "skip_footer.png"
    click "숨기기"
    pause 0.5
    assert eval (_windows_hidden)
    screenshot "hidden.png"
    click pos (640,300)
    pause 0.5
    assert eval (not _windows_hidden)
    click "빠르게"
    pause until screen "choice" timeout 20
    pause 1.0
    screenshot "choice_context.png"
    assert eval (not r13_fast_all and not r13_fast_read)
    keysym "K_4"
    pause 1.0
    click "건너뛰기"
    pause 0.5
    click pos (1150,90) until screen "choice" timeout 40
    assert eval (not r13_fast_read)
    assert eval ("W5" in room13["evidence"])
    click "증거도 없이 가둘 겁니까"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    $ open("qa_result.txt","w").write("skip to choice, number key 4 picked sliver question")


testcase evening_board:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=2,location="room13",life_poc=True),("+brief","ep1_patrol_seen","ep2_seen"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "ev_board.png"
    assert eval (all(a["cost"]==0 for a in ROOM13["activities"].values()) and not R13_CONTEXT_WAIT)
    click "초롱과 등불 돌기 · 광장"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "ev_lamp.png"
    click "식은 등을 함께 센다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "순회를 마치고 돌아간다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("W6" in room13["evidence"] and r13_has("know_stone_failing") and room13["period"]==2 and room13["location"]=="square")
    $ r13_qa_town_dump()

testcase evening_visit:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=2,location="gate",life_poc=True,case_state="occurred",daram_state="held"),("badook_ally","ep1_done","ev_b_done","ev_c_done","ep3_bell_seen"),("snack",))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "ev_visit.png"
    click "담요를 넣어 달라고 부탁한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "구운 밤을 넣어 준다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("daram_warm") and r13_has("daram_fed") and "W7" in room13["evidence"] and room13["period"]==2)
    $ r13_qa_town_dump()

testcase evening_eve:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=6,period=2,location="dining",life_poc=True,case_state="occurred",daram_state="held"),("witness:nabi","tok_detained","ep1_done","ev_b_done","ev_c_done","ep3_bell_seen","ep4_seen"))
    click pos (1150,90) until screen "choice" timeout 40
    click "나비 옆에 앉는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "톡을 찾는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "ev_eve.png"
    click "그만 일어선다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("ev_eve_done") and r13_has("eve:nabi") and r13_has("eve:tok"))
    $ r13_qa_town_dump()

testcase b3_ration_chain:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=0,location="square",life_poc=True,case_state="occurred",daram_state="held"),("scale_rigged","know_ration_scale","ep1_done","ev_b_done","ev_c_done","ep4_seen"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "b3_ration.png"
    click "도토에게 배급 장부를 보자고 한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "배급소 저울을 다시 재자고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("bori_cleared") and r13_has("rumor:fair") and r13_has("ration_fixed"))
    run Call("r13_qa_goto",5,0,"inn")
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("heard:rumor:fair"))
    $ r13_flag("rumor:briber")
    assert eval (r13_shop_price(room13,"snack")==2)
    $ r13_qa_town_dump()

testcase b3_scale_half:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="store",life_poc=True),("scale_rigged","rumor:briber","ep1_done","ev_b_done","ep4_seen","ev_a_done"))
    pause 1.0
    assert eval (r13_shop_price(room13,"snack")==3)
    run Call("r13_qa_talk","resident_eunho")
    click pos (1150,90) until "저울이 기울어 있다고 말한다" timeout 30
    click "저울이 기울어 있다고 말한다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "제 물건만 반값에 주시죠"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 40
    assert eval (r13_has("shop_half") and r13_shop_price(room13,"hat")==3 and r13_shop_price(room13,"snack")==1)
    $ r13_qa_town_dump()

testcase b3_firewood:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=2,location="school",life_poc=True,case_state="occurred",daram_state="held"),("ep1_done","ev_b_done","ev_c_done","ep3_bell_seen","ev_visit:5","ev_e_done"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "b3_wood.png"
    click "왜 장작을 가져가는지 묻는다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "대피소 장작을 대신 나르겠다고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("W8" in room13["evidence"] and r13_has("bori_ally") and room13["period"]==2)
    $ r13_qa_town_dump()

testcase b3_pages:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=0,location="post",life_poc=True),("ep1_done","ev_b_done","ev_c_done","ep4_seen"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "b3_pages.png"
    click "장부를 베낄 시간을 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("pages_sold") and not r13_has("know_stone_history"))
    run Call("r13_qa_goto",5,0,"post")
    pause 1.0
    run Call("r13_qa_talk","resident_librarian")
    click pos (1150,90) until "베껴 둔 돌 기록을 보여 달라고 한다" timeout 30
    click "베껴 둔 돌 기록을 보여 달라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 60
    assert eval (r13_has("know_stone_history") and "W3" in room13["evidence"])
    $ r13_qa_town_dump()

testcase carry_good:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=8,period=0,location="inn",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True),("bori_cleared","scale_public","kids_fed","tok_cleared","musoe_recovering","know_stone_failing"))
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (all(r13_has(f) for f in ("transport_terms","supply_terms","shelter_agreed","operators_terms","clinic_observation","w1_links_done")) and not r13_has("measurement_plan"))
    $ r13_qa_town_dump()

testcase carry_refuse:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=8,period=0,location="inn",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True),("bori_punished","eunho_blackmailed","rumor:briber","rumor:strongarm","badook_ally"),(),30)
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("bori_refuses") and r13_has("eunho_refuses") and r13_has("teacher_doubts"))
    $ r13_edit(location="gate")
    run Call("r13_qa_talk","karo")
    click pos (1150,90) until "마차 썰매를 빌린다" timeout 30
    click "마차 썰매를 빌린다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 30
    click "썰매를 열 냥에 빌린다"
    pause 1.0
    click pos (1150,90) until screen "r13_topics" timeout 30
    assert eval (r13_has("transport_terms") and r13_cash_now()==20)
    $ r13_qa_town_dump()

testcase w2e_bell:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=9,period=0,location="square",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True),("w1_links_done","village_alerted"))
    click pos (1150,90) until screen "choice" timeout 60
    screenshot "w2e_bell.png"
    click "설이에게 종을 치라고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("w2_bell_rung") and r13_has("operators_terms") and r13_has("transport_terms") and room13["period"]==0)

testcase w2e_numbers:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=9,period=0,location="workshop",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True,evidence=["W4"]),("w1_links_done",))
    click pos (1150,90) until screen "choice" timeout 60
    click "가짜 숫자에 동의한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("numbers_forged") and not r13_available(ROOM13["activities"]["w2_measure1"]))
    $ r13_edit(location="clinic")
    run Call("r13_qa_talk","resident_seori")
    click pos (1150,90) until "촌장의 숫자를 지난주 기록과 맞춘다" timeout 30
    click "촌장의 숫자를 지난주 기록과 맞춘다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("forgery_exposed") and not r13_has("numbers_forged"))

testcase w2e_tools:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=9,period=0,location="workshop",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True),("w1_links_done","w2e_p_done"))
    click pos (1150,90) until screen "choice" timeout 60
    click "제가 결정할 일은"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("tools_sold") and r13_has("tools_missing") and "부리의 할아버지 도구는 도시로 팔려 갔다." in r13_ending_notes())

testcase w2e_share:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=10,period=0,location="store",life_poc=True,case_state="occurred",week2_started=True,trial_ended=True),("w1_links_done","supplies_ready","kids_fed"))
    click pos (1150,90) until screen "choice" timeout 60
    screenshot "w2e_share.png"
    click "남은 몫을 경매에 붙인다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("share_auction") and r13_has("rumor:profiteer") and r13_cash_now()==10)

testcase trial_fake_testimony:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E36'),("-gates","witness:nabi","witness:tok","fair_hearing","fake_testimony"))
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이뿐이라는 주장"
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
    assert eval (r13_has("fake_testimony_exposed") and r13_has("c4_unenforced"))
    $ r13_flag("qa_marker")
    $ r13_qa_dump()

testcase trial_c1_h7:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'H7', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E36'),("-gates","witness:nabi","witness:tok","ttadak_witness"))
    pause 1.0
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아이뿐이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "되묻기"
    pause 0.5
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA H7"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "다른 길이 있으니"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    assert eval ("C1" in room13["propositions"])

testcase w1c_mother_line:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("+w1c","ep1_patrol_seen","ev_a_done"),(),12)
    click pos (1150,90) until screen "choice" timeout 40
    click "엄마 초상을 그려 달라고 한다 (5냥)"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    run Call("r13_qa_goto",2,0,"post")
    click pos (1150,90) until screen "choice" timeout 40
    click "오늘 품삯은 제가 내겠습니다"
    pause 1.0
    click pos (1150,90) until screen "choice" timeout 40
    click "할머니께 쪽지 하나만"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("mom_portrait") and r13_has("fake_letter_planted") and "H9" in room13["evidence"])
    run Call("r13_qa_goto",4,2,"hall",("ep1_done","ev_b_done","ev_c_done","ep4_seen"))
    click pos (1150,90) until screen "choice" timeout 40
    screenshot "w1c_night.png"
    click "할머니를 따라간다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (room13["case_state"]=="prevented" and r13_has("prevention_witness") and "E17" in room13["evidence"])

testcase w1c_wall_and_seal:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=1,location="inn",life_poc=True),("+w1c","ep1_done","ev_b_done","ev_c_done","ep4_seen","ev_a_done"))
    click pos (1150,90) until screen "choice" timeout 40
    click "비밀을 지켜 주겠다고 한다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("H7" in room13["evidence"] and r13_has("ttadak_witness"))
    run Call("r13_qa_goto",5,0,"hall",("case_occurred_marker",))
    pause 1.0
    $ r13_edit(case_state="occurred",daram_state="held")
    run Call("r13_qa_goto",5,0,"hall")
    click pos (1150,90) until screen "choice" timeout 40
    click "몰래 뒤를 밟는다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("W9" in room13["evidence"] and "H8" in room13["evidence"] and r13_has("family_items_lost"))
    $ r13_cash(20,"qa")
    run Call("r13_qa_goto",6,0,"gate")
    click pos (1150,90) until screen "choice" timeout 40
    click "열 냥에 산다"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("fake_testimony"))

testcase karo_work_offer:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=2,location="room13",life_poc=True),())
    pause 1.0
    $ r13_edit(flags=[f for f in room13["flags"] if f!="livelihood_open"])
    run Call("r13_qa_goto",2,0,"inn")
    click pos (1150,90) until screen "r13_hub" timeout 60
    assert eval (r13_has("livelihood_open") and room13["period"]==0)

testcase linebreak_pages:
    pause 2.0
    click "처음부터"
    pause 3.0
    $ preferences.text_cps=0
    run Call("r13_qa_linebreak")
    pause 1.5
    screenshot "lb_two_sentences.png"
    click pos (1150,90)
    pause 1.5
    screenshot "lb_page1.png"
    click pos (1150,90)
    pause 1.5
    screenshot "lb_page2.png"

testcase present_portrait:
    # 0.18.13: the portrait is a record shown from the notebook; a name-only question stays vague.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("+w1c","ep1_patrol_seen","ev_a_done"),(),12)
    click pos (1150,90) until screen "choice" timeout 40
    click "엄마 초상을 그려 달라고 한다 (5냥)"
    pause 1.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("P01" in room13["evidence"] and not [k for k,s in r13_topics("resident_sling")+r13_topics("resident_lamplighter") if k.startswith("portrait_")])
    assert eval ("ask_mom:sling" in [k for k,s in r13_topics("resident_sling")])
    run Function(r13_qa_present,"resident_sling","P01")
    assert eval ("초롱 아저씨" in r13_qa_last_present and "J08" in room13["evidence"] and "ask_mom:sling" not in [k for k,s in r13_topics("resident_sling")])
    run Function(r13_qa_present,"resident_lamplighter","P01")
    assert eval ("확인할 필요" in r13_qa_last_present and "J07" in room13["evidence"] and r13_has("portrait_lamp_seen"))
    assert eval (r13_goal_is_question())
    # Reply sent on day 8 afternoon: normally day 9 afternoon (abs 33); with the face known, day 9 morning (abs 32).
    run Function(r13_edit,day=8,period=1)
    run Function(r13_w2_action_done,"w2_reply")
    assert eval (room13["reply_due"]==32)

testcase memory_grudge:
    # 0.18.14: a harmed resident stays cold despite good rumors; repair is tied to the incident.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=0,location="room13"),("yeoni_hostile","rumor:fair","heard:rumor:fair"),(),5)
    pause 1.0
    assert eval ("grudge_cold:yeoni" in [k for k,s in r13_topics("resident_yeoni")] and "grudge_fix:yeoni" in [k for k,s in r13_topics("resident_yeoni")])
    assert eval (r13_conversation_topic_lines("grudge_cold:yeoni")[0][1].startswith("광장에서 좋은 말이 돈다는 건 알아요. 그래도"))
    assert eval (r13_qa_price("rumor:briber")==r13_qa_price()+1 and r13_qa_price("rumor:briber","rumor:fair")==r13_qa_price())
    assert eval (r13_qa_price("eunho_hostile","rumor:fair")==r13_qa_price()+1 and r13_qa_price("eunho_hostile","eunho_reconciled")==r13_qa_price())
    assert eval (r13_bad_rumors()==[])
    run Call("r13_qa_grudge","yeoni")
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("yeoni_reconciled") and r13_cash_now()==2 and not [k for k,s in r13_topics("resident_yeoni") if k.startswith("grudge_")])

testcase ledger_order:
    # 0.18.15 B-2: showing the ledger to 백 부인 first lets her move the goods at the next time change.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=0,location="store",evidence=["H1"]),("ev_b_done","ev_c_done"))
    pause 1.0
    run Function(r13_qa_present,"resident_madam","H1")
    assert eval ("지난 장부" in r13_qa_last_present and not r13_madam_moved() and r13_object_visible(ROOM13["objects"]["store"]["hoard"]))
    run Function(r13_edit,period=1)
    assert eval (r13_madam_moved() and r13_object_visible(ROOM13["objects"]["store"]["hoard_moved"]) and not r13_object_visible(ROOM13["objects"]["store"]["sacks"]))
    run Function(r13_qa_present,"resident_seori","H1")
    assert eval ("H11" in room13["evidence"] and "H10" not in room13["evidence"] and "H1" in room13["evidence"] and not r13_has("madam_exposed"))
    run Function(r13_qa_present,"resident_eunho","H1")
    assert eval (r13_has("eunho_deal_offered") and "ledger_deal" in [k for k,s in r13_topics("resident_eunho")])

testcase testimony_scope:
    # 0.18.15 C: first statements stay; records narrow them; rumors keep their source.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="room13",life_poc=True),())
    pause 1.0
    assert eval ("rumor_mom:yeoni" in [k for k,s in r13_topics("resident_yeoni")] and "rumor_mom:karo" not in [k for k,s in r13_topics("karo")])
    run Function(r13_finish_topic,"rumor_mom:yeoni")
    assert eval ("J11" in room13["evidence"] and "rumor_mom:karo" in [k for k,s in r13_topics("karo")])
    run Function(r13_finish_topic,"rumor_mom:karo")
    assert eval ("J13" in room13["evidence"] and "엄마는 보지 못했다" in ROOM13["evidence"]["J13"]["establishes"])
    run Function(r13_edit,day=5,case_state="occurred",victim_state="dead",evidence=["E11","E05"])
    run Function(r13_finish_topic,"nabi_alibi")
    assert eval ("J09" in room13["evidence"] and "E15" in room13["evidence"] and "nabi_gap" not in [k for k,s in r13_topics("nabi")])
    run Function(r13_qa_present,"nabi","E11")
    assert eval ("nabi_gap" in [k for k,s in r13_topics("nabi")])
    run Function(r13_finish_topic,"nabi_gap")
    assert eval ("E12" in room13["evidence"] and "J09" in room13["evidence"])
    run Function(r13_qa_present,"doto","E05")
    assert eval ("J10" in room13["evidence"] and "복도 쪽 문" in r13_qa_last_present)

testcase delivery_cord:
    # 0.18.16 D-1: no double-pay choice; reading labels and tying the boxes with a cord leads to the bonus.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="gate"),(),("cord","snack"))
    pause 1.0
    run Call("r13_qa_delivery")
    click pos (640,600) until screen "choice" timeout 40
    click "작은 상자의 짐표를 읽는다"
    click pos (640,600) until screen "choice" timeout 40
    click "짐을 수레에 올려 본다"
    click pos (640,600) until screen "choice" timeout 40
    click "가진 물건을 짐에 써 본다"
    click pos (640,600) until screen "choice" timeout 40
    click "구운 밤"
    click pos (640,600) until screen "choice" timeout 40
    click "가진 물건을 짐에 써 본다"
    click pos (640,600) until screen "choice" timeout 40
    click "질긴 묶음끈"
    click pos (640,600) until screen "choice" timeout 40
    click "짐을 나르러 간다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice=="combine" and "same_lane" in r13_wallet(room13)["relations"])
    assert eval (r13_complete_job(room13,"delivery","combine")[1]["pay"]==14)

testcase night_talk:
    # 0.18.16 E: 다람이 reacts only to what happened; the topic opens with Dad's telling.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=2,location="room13"),("store_locked_night",))
    pause 1.0
    assert eval (r13_home_with_daram() and "night:locked" in [k for k,s in r13_topics("daram")] and "night:ledger_madam" not in [k for k,s in r13_topics("daram")])
    run Function(r13_town_set,madam_alerted_at=0)
    assert eval ("night:ledger_madam" in [k for k,s in r13_topics("daram")])
    run Function(r13_edit,location="square")
    assert eval ("night:locked" not in [k for k,s in r13_topics("daram")])

testcase owl_and_buri:
    # 0.18.17: living-elder scenes, 부리's stages, 백 부인 ledger approach, 톡 follow-up.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=1,location="hall",life_poc=True),("+w1c","ev_g_done","ev_l_done","ev_i_done","ev_owl_omen_done"))
    click pos (640,600) until screen "choice" timeout 40
    click "수리가 끝나면 다시 오겠습니다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_has("owl_threshold_respected"))
    run Function(r13_edit,day=3)
    assert eval ("owl_old_case" in [k for k,s in r13_topics("resident_owlgp")])
    run Function(r13_edit,day=6,case_state="occurred",victim_state="dead",evidence=["E35","H1"])
    assert eval ("buri_assert" in [k for k,s in r13_topics("buri")])
    run Function(r13_qa_present,"buri","E35")
    assert eval (r13_has("buri_revised") and "아직 무슨 말을" in r13_qa_last_present and "buri_assert" not in [k for k,s in r13_topics("buri")])
    run Function(r13_qa_present,"resident_madam","H1")
    assert eval ("지난 장부" in r13_qa_last_present and "ledger_madam:approach" in [k for k,s in r13_topics("resident_madam")])
    run Function(r13_flag,"tok_hostile","tok_cleared")
    assert eval ("tok_after_doubt" in [k for k,s in r13_topics("resident_tok")])

testcase inn_change:
    # 0.18.18 A: a raised lever before the case makes Granny call off the plan; wax trace after the case.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="kitchen",kitchen_switch=True),("passage_known","ep1_done","ev_b_done","ev_c_done","ep4_seen"))
    pause 1.0
    assert eval (r13_plan_noticed() and r13_object_visible(ROOM13["objects"]["kitchen"]["rear"]) and not r13_object_visible(ROOM13["objects"]["kitchen"]["rear_after"]))
    run Function(r13_flag,"observed:kitchen:rear")
    run Function(r13_edit,case_state="occurred")
    assert eval (r13_object_visible(ROOM13["objects"]["kitchen"]["rear_after_known"]) and not r13_object_visible(ROOM13["objects"]["kitchen"]["rear"]) and not r13_object_visible(ROOM13["objects"]["kitchen"]["rear_after"]))
    run Function(r13_edit,case_state="pending",day=4,period=2,location="hall")
    run Call("r13_case_choice")
    click pos (640,600) until screen "choice" timeout 40
    click "까로와 되돌아온 짐을 확인하러 간다"
    click pos (640,600) until screen "r13_hub" timeout 60
    assert eval (room13["case_state"]=="prevented" and room13["victim_state"]=="protected" and "H13" in room13["evidence"] and "E34" in room13["evidence"] and r13_has("plan_noticed"))

testcase trial_notes:
    # 0.18.19: three lines per claim after the trial; no record names.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=8,period=0,location="inn",case_state="occurred",propositions=["C1","C2"]),())
    pause 1.0
    run Function(r13_record_trial_notes)
    assert eval (len(room13["trial_notes"])==4 and room13["trial_notes"][2]["result"]=="할머니의 이동에 관한 주장은 남았다." and not any(k in n["fact"]+n["question"]+n["result"] for n in room13["trial_notes"] for k in ROOM13["evidence"]))
    assert eval (any(n.get("result")=="잠긴 방에 아이만 있었다는 주장은 무너졌다." for n in r13_first_mystery_notes()))
