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
    click "아이만 들어갔다"
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

testcase trial_partial:
    # 0.18.35: without the wound comparison (E35) the candlestick point still opens. Two statements
    # break, the broken candlestick alone is answered (not accepted), and closing keeps what was broken.
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
    assert eval (not r13_debate_is_broken("C2","s2"))
    click "다시 휘두를 사람이"
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    assert eval (r13_debate_stuck("C2") and r13_debate_progress("C2")==(2,3))
    screenshot "p_stuck.png"
    click "여기까지 정리한다"
    pause 1.0
    click "여기까지 정리한다"
    pause 0.5
    click pos (640,600) until eval "trial_notes" in room13 timeout 120
    pause 0.5
    assert eval (room13["trial_result"]=="detained" and room13["debate"]["closed"].get("trial:C2")=="partial")
    assert eval ("반박했다" in room13["trial_notes"][1]["fact"] and "한 번 휘둘렸을 뿐" in room13["trial_notes"][1]["question"])
    $ r13_qa_dump()

testcase trial_win:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E06', 'E07', 'E09', 'E35'),())
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
    click "QA E35"
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
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E35', 'E36'),())
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
    click "아이만 들어갔다"
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
    click "QA E35"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "주방 레버로만"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "통로를 아는 할머니가 죽였다"
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
    click "주방에 간 뒤로는"
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
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "식당을 나설 때도"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E35"
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
    click "핀이 내려친 쪽 고리에"
    pause 0.6
    click pos (640,600) until eval room13.get("trial_result")=="culprit_proven" and room13.get("granny_state")=="detained" timeout 120
    pause 0.5
    screenshot "f_verdict.png"
    $ r13_qa_dump()

testcase trial_gate_unenforced:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E35', 'E36'),("-gates","witness:nabi","witness:tok"))
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
    click "아이만 들어갔다"
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
    click "QA E35"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "주방 레버로만"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "통로를 아는 할머니가 죽였다"
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
    click "주방에 간 뒤로는"
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
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "식당을 나설 때도"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E35"
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
    click "핀이 내려친 쪽 고리에"
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
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E35', 'E36'),("-gates",))
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
    click "아이만 들어갔다"
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
    click "QA E35"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "주방 레버로만"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "통로를 아는 할머니가 죽였다"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    screenshot "f_after_wrong.png"
    click "결론을 말한다"
    pause 1.0
    click "누군가가 냈다"
    pause 0.6
    # 0.18.35: without Nabi the alibi point still opens (the passage breaks one statement),
    # but her statement stays unbreakable. Closing it partially leaves C3 unproven.
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "식당에 있었다는 말"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "한참 걸려요"
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E05"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    assert eval (r13_debate_stuck("C3"))
    click "여기까지 정리한다"
    pause 1.0
    click "여기까지 정리한다"
    pause 0.5
    click pos (640,600) until eval "trial_notes" in room13 timeout 120
    pause 0.5
    assert eval ("C3" not in room13["propositions"] and room13["debate"]["closed"].get("trial:C3")=="partial")
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
    click "아무도 못 돌아온다는"
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
    click "반짝 효과는 짧고"
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
    click "학교에 모여 식량을"
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
    click "엄마를 붙잡으려"
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
    # 0.18.42 moved hide/fast into 더보기; 0.18.46 put 건너뛰기 (skip this conversation) on the bar.
    click "더보기"
    pause 0.5
    click "대화창 숨기기"
    pause 0.5
    assert eval (_windows_hidden)
    screenshot "hidden.png"
    click pos (640,300)
    pause 0.5
    assert eval (not _windows_hidden)
    click "더보기"
    pause 0.5
    click "모든 대사 빠르게"
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
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E35', 'E36'),("-gates","witness:nabi","witness:tok","fair_hearing","fake_testimony"))
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
    click "아이만 들어갔다"
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
    click "QA E35"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "주방 레버로만"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "결론을 말한다"
    pause 1.0
    click "통로를 아는 할머니가 죽였다"
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
    click "주방에 간 뒤로는"
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
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "식당을 나설 때도"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E35"
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
    click "핀이 내려친 쪽 고리에"
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
    run Call("r13_qa_trial",('E01', 'H7', 'E06', 'E07', 'E09', 'E12', 'E13', 'E14', 'E15', 'E35', 'E36'),("-gates","witness:nabi","witness:tok","ttadak_witness"))
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
    click "아이만 들어갔다"
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
    pause 1.0
    assert screen "r13_life_closeup"
    click pos (850,487)
    pause .5
    click pos (873,439)
    pause .5
    click "구운 밤"
    click pos (873,439)
    pause .5
    click "질긴 묶음끈"
    click pos (873,439)
    pause 1.0
    screenshot "delivery_tied.png"
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

testcase reinspect_and_credit:
    # 0.18.19: candlestick parts from the first run; 은호's hidden ledger is credit, not the murder.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=0,location="clinic",case_state="occurred",victim_state="dead",daram_state="held",evidence=["E07"],read_topics=["tok_repair"]),())
    pause 1.0
    assert eval ("seal_look" in [k for k,s in r13_topics("resident_seori")])
    run Function(r13_flag,"saw_eunho_hide")
    run Function(r13_finish_topic,"eunho_hidden_ledger")
    assert eval ("J16" in room13["evidence"] and "13호 사건" in ROOM13["evidence"]["J16"]["does_not_establish"])
    run Function(r13_edit,day=9)
    run Function(r13_flag,"eunho_refuses")
    assert eval ("w2_eunho_credit" in [k for k,s in r13_topics("resident_eunho")])

testcase use_knowledge:
    # 0.18.19: play dumb, test testimony by a favour, keep the envelope sealed.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="inn",life_poc=True,evidence=["H9"]),("know_granny_reads","warning_location"))
    pause 1.0
    assert eval ("granny_letter_ask" in [k for k,s in r13_topics("granny")] and "granny_letter_confront" in [k for k,s in r13_topics("granny")])
    run Function(r13_finish_topic,"granny_letter_confront")
    assert eval (r13_has("granny_knows_found_out") and "granny_letter_ask" not in [k for k,s in r13_topics("granny")])
    run Function(r13_edit,location="square")
    assert eval ("warning_keep" in [k for k,a in r13_actions()] and "warning" in [k for k,a in r13_actions()])
    run Function(r13_finish_action,"warning_keep")
    assert eval (r13_has("warning_sealed_held") and "warning" not in [k for k,a in r13_actions()])
    run Function(r13_finish_topic,"warning_open_with")
    assert eval ("E18" in room13["evidence"] and "J18" in room13["evidence"])
    run Function(r13_edit,day=5,case_state="occurred")
    run Function(r13_finish_topic,"doto_view_claim")
    run Function(r13_finish_topic,"doto_view_test")
    assert eval ("J17" in room13["evidence"])

testcase event_offer:
    # 0.18.19: an ordinary event shows as a marker; clicking enters, passing by applies its look-away outcome.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="square",life_poc=True),("+w1c","+offers","ev_l_done","ev_i_done","ep1_patrol_seen","ev_a_done"),(),12)
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval ("r13_w1c_portrait" in room13["offers"] and not r13_has("ev_g_done"))
    click "피코가 판자에"
    click pos (1150,90) until screen "choice" timeout 40
    click "모른 척한다"
    click pos (1150,90) until screen "r13_hub" timeout 40
    assert eval (r13_has("ev_g_done") and "r13_w1c_portrait" not in room13.get("offers",{}))
    run Function(r13_edit,location="post",period=0)
    run Function(r13_flag,"ev_g_done")
    run Function(r13_offer,"r13_w1c_letters")
    run Function(r13_edit,period=1)
    run Function(r13_offers_tick)
    assert eval (r13_has("ev_l_done") and r13_has("warning_exposed") and room13["offer_news"])

testcase grant_after_reaction:
    # 0.18.20: a record earned by showing something is granted after the reaction is read, once.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="post",life_poc=True,evidence=["P01"]),())
    pause 1.0
    run Function(r13_qa_present_deferred,"resident_sling","P01")
    assert eval ("J08" not in room13["evidence"] and room13["pending_grants"] and r13_has("portrait_known"))
    run Function(r13_flush_grants)
    assert eval ("J08" in room13["evidence"] and not room13["pending_grants"])
    run Function(r13_qa_present_deferred,"resident_sling","P01")
    run Function(r13_flush_grants)
    assert eval (room13["evidence"].count("J08")==1)

testcase gate_documents:
    # 0.18.22: no document popup. The shelf scene gives the original; the guard hands over his list.
    pause 2.0
    click "처음부터"
    pause 3.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "gate_hub.png"
    assert eval ("G1" not in room13["evidence"] and "G3" not in room13["evidence"])
    run Jump("r13_qa_gate_shelf")
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval ("G1" in room13["evidence"] and "G3" not in room13["evidence"])
    run Jump("r13_entry_guard_menu")
    pause 1.0
    assert screen "r13_entry_topics"
    screenshot "gate_topics.png"
    click "이름 목록이 다른 이유"
    click pos (640,600) until screen "r13_entry_topics" timeout 40
    assert eval ("G3" in room13["evidence"])

testcase bed_hint_day1:
    # 0.18.22: on day 1 the bed says why sleep waits instead of saying nothing.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="room13",life_poc=True,evidence=["E03"]),("lodging",))
    pause 2.0
    screenshot "room13_daram_afternoon.png"
    assert eval (not r13_bed_available("bed") and "책상" in r13_bed_blocked_reason("bed"))
    run Call("r13_object_options","bed")
    pause 1.0
    assert screen "r13_object_context"
    screenshot "bed_hint_day1.png"
    $ room13["evidence"].append("M01")
    assert eval (r13_bed_available("bed") and r13_bed_blocked_reason("bed") is None)

testcase goal_fold:
    # 0.18.22: the field question folds open; a picked question opens its 조사 메모 card.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=1,location="room13",life_poc=True,evidence=["E01","E03","E04","M01","J04"]),("lodging","livelihood_open","observed:room13:books","ep1_eaves_seen","ep1_done"))
    pause 2.0
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    screenshot "goal_fold_closed.png"
    run SetVariable("r13_goal_open",True)
    pause 1.0
    screenshot "goal_fold_open.png"
    run [SetVariable("r13_goal_open",False),Show("r13_learning_notes",focus=0)]
    pause 1.0
    assert screen "r13_learning_notes"
    screenshot "goal_fold_notes.png"
    run Hide("r13_learning_notes")

testcase drawer_visual:
    # 0.18.22: rubbing picture, pressed groove and opened panel are drawn, not ASCII.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=1,location="room13",life_poc=True,evidence=["M01","E03"]),("lodging",))
    pause 2.0
    run Call("r13_inspect_desk")
    pause 1.0
    click pos (962,368)
    pause 1.0
    $ room13["inspection_items"]=dict(version=1,inventory=["pencil","ruler"],taken=["pencil","paper","ruler"],seen=[],paper_placed=True,rubbing=True,compartment_open=False,groove_held=True)
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "drawer_rubbing_held.png"
    $ room13["inspection_items"]=dict(version=1,inventory=["pencil","ruler"],taken=["pencil","paper","ruler"],seen=[],paper_placed=True,rubbing=True,compartment_open=True,groove_held=False)
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "drawer_open.png"

testcase inn_workers:
    # 0.18.22 (owner): 토리 actually sews and 따닥 actually repairs at the inn.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="inn",life_poc=True),("lodging","entry_corrected"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ print("QA_INN", [(a["person"],a["pose"],a["x"],a["y"]) for a in r13_stage_people(False)])
    screenshot "inn_workers.png"

testcase life_door:
    # 0.18.22 map assets B: leave for the inn's cloth, cloth under the front door, stays fixed.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("lodging","entry_corrected","livelihood_open"))
    pause 1.0
    assert eval (r13_life_door_available())
    run Jump("r13_qa_life_door")
    pause 1.0
    screenshot "life_door_before.png"
    click pos (1075,562)
    click pos (640,600) until screen "r13_life_closeup" timeout 40
    click "여관의 낡은 천"
    click pos (550,457)
    click pos (640,600) until screen "r13_life_closeup" timeout 40
    pause 1.0
    screenshot "life_door_after.png"
    assert eval (r13_has("inn_draft_sealed"))

testcase life_meal:
    # 0.18.22 map assets C: the set kept aside is served once, then the existing finish/ask.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="dining",life_poc=True),("lodging","entry_corrected","livelihood_open"))
    pause 1.0
    run Jump("r13_qa_life_meal")
    pause 1.0
    screenshot "life_meal_before.png"
    click pos (1018,392)
    pause 1.0
    screenshot "life_meal_after.png"
    click "맡은 일만 마친다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice=="finish" and r13_has("life_meal_served"))

testcase fullbody_dialogue:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_fullbody")
    click pos (1276,300) until eval r13_qa_fb_done timeout 1500
    pause 1.0

testcase fullbody_tuned:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_fullbody",("normal","large"),["bami","doto"],["neutral","surprise"])
    click pos (1276,300) until eval r13_qa_fb_done timeout 300
    pause 1.0

testcase fullbody_line_emotions:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_line_emotions")
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_0.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_1.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_2.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_3.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_4.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_5.png"
    click pos (640,600)
    pause 1.2
    $ r13_qa_le_record()
    screenshot "le_6.png"
    click pos (640,600)
    pause 1.5

testcase inn_v4_travel:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_inn_v4")
    click pos (640,600) until screen "r13_hub" timeout 60
    pause 1.0
    $ r13_qa_inn_note("lobby")
    screenshot "inn_lobby.png"
    click "‹ 식당"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("after-dining-chip")
    click "접수대 ›"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    click "주방 ›"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("after-kitchen-chip")
    click "접수대 ›"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    click "안내도"
    pause 1.0
    $ r13_qa_inn_note("guide-open-lobby")
    screenshot "inn_guide_lobby.png"
    keysym "K_ESCAPE"
    pause 1.0
    $ r13_qa_inn_note("guide-escape")
    click "2층으로 ↑"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("hall")
    screenshot "inn_hall.png"
    click "안내도"
    pause 1.0
    $ r13_qa_inn_note("guide-open-hall")
    screenshot "inn_guide_hall.png"
    click "닫기"
    pause 1.0
    $ r13_qa_inn_note("guide-closed")
    click "13호실"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("room13")
    click "복도로 ›"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    click "↓ 1층 로비"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("back-lobby")
    click "바깥으로"
    pause 1.5
    $ r13_qa_inn_note("outside-map")
    screenshot "inn_outside_map.png"
    click "현장으로 돌아가기"
    pause 1.0
    click "안내도"
    pause 1.0
    click "식당"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("guide-travel-dining")
    $ r13_qa_inn_dump()

testcase inn_v4_guestroom:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_inn_v4","occurred")
    click pos (640,600) until screen "r13_hub" timeout 60
    pause 1.0
    click "2층으로 ↑"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("hall-occurred")
    screenshot "inn_hall_occurred.png"
    click "안내도"
    pause 1.0
    $ r13_qa_inn_note("guide-occurred")
    screenshot "inn_guide_occurred.png"
    click "닫기"
    pause 1.0
    click "임시 객실 ›"
    pause 1.5
    click pos (640,600) until screen "r13_hub" timeout 30
    $ r13_qa_inn_note("guestroom")
    $ r13_qa_inn_dump()

testcase gm_package:
    # 0.18.22 visual gimmicks: feel → knife on the seam → lift the board → read the contents.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=0,location="store",life_poc=True),("lodging","entry_corrected"),("knife",))
    pause 1.0
    run Jump("r13_qa_gm_package")
    pause 1.0
    click pos (685,540)
    pause .5
    assert eval (r13_gm_state("package").get("felt") and r13_gm_state("package").get("stage","closed")=="closed")
    click "부리의 작업칼"
    click pos (685,540)
    pause .5
    click pos (698,508)
    pause 1.0
    screenshot "gm_package_revealed.png"
    click pos (678,497)
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice is True)

testcase gm_lamp:
    # 0.18.22 visual gimmicks: dark until the lamp is raised; the threshold read unlocks the note.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="kitchen",life_poc=True),("lodging","entry_corrected"),("lantern",))
    pause 1.0
    run Jump("r13_qa_gm_lamp")
    pause 1.0
    click pos (435,472)
    pause .5
    assert eval (not r13_gm_state("lamp").get("seen"))
    click "초롱의 손등불"
    click pos (435,472)
    pause 1.0
    screenshot "gm_lamp_lit.png"
    click "본 것을 적는다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice is True)

testcase gm_scale:
    # 0.18.22 visual gimmicks: the tilt alone does not finish; the screw must be looked at too.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="store",life_poc=True),("lodging","entry_corrected"),("weight",))
    pause 1.0
    run Jump("r13_qa_gm_scale")
    pause 1.0
    click "표준 저울추"
    click pos (410,432)
    pause 1.0
    screenshot "gm_scale_loaded.png"
    assert eval (r13_gm_state("scale").get("tilt_seen") and not r13_gm_state("scale").get("screw_seen"))
    click pos (640,209)
    pause .5
    click pos (653,353)
    pause 1.0
    screenshot "gm_scale_pivot.png"
    click "본 것을 적는다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice is True)

testcase gm_floor:
    # 0.18.22 visual gimmicks 02: hand → knife lifts the board (no M02) → unfolding reads M02.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="room13",life_poc=True),("lodging","entry_corrected"),("knife",))
    pause 1.0
    run Jump("r13_qa_gm_floor")
    pause 1.0
    click pos (640,420)
    click "부리의 작업칼"
    click pos (640,420)
    pause 1.0
    assert eval (r13_gm_state("floor").get("stage")=="open" and "M02" not in room13["evidence"])
    screenshot "gm_floor_open.png"
    click pos (646,432)
    pause 1.0
    screenshot "gm_floor_note.png"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice is True)

testcase gm_stone:
    # 0.18.22 visual gimmicks 02: paper on the stone, rub three rows (drag or sweep), then read.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="square",life_poc=True),("lodging","entry_corrected"),("rubbing",))
    pause 1.0
    run Jump("r13_qa_gm_stone")
    pause 1.0
    click "탁본 종이와 숯"
    click pos (640,330)
    pause 1.0
    assert eval (r13_gm_state("stone").get("paper") and not r13_rub_enough())
    click "한 줄 문지르기"
    pause .5
    click "한 줄 문지르기"
    pause 1.0
    screenshot "gm_stone_half.png"
    click "한 줄 문지르기"
    pause 1.0
    assert eval (r13_rub_enough())
    click "드러난 자국을 살펴본다"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (r13_qa_dv_choice is True)

testcase redesign_world:
    # 2026-10-15: four NPC redesigns stand in their real scheduled places.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(zip(("day","period","location"),r13_qa_redesign_slot("resident_yeoni")),life_poc=True),("lodging","entry_corrected"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_yeoni")
    screenshot "redesign_world_yeoni.png"
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_momo"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_momo")
    screenshot "redesign_world_momo.png"
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_librarian"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_librarian")
    screenshot "redesign_world_librarian.png"
    # The inn panorama is wider than the screen; look at its left end.
    $ r13_world_cameras={"inn":0}
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_nubi"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_nubi")
    screenshot "redesign_world_nubi.png"
    $ r13_world_cameras={}
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_seol"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_seol")
    screenshot "redesign_world_seol.png"
    # 실룩 stands at the right end of the gate panorama (clamped to the edge).
    $ r13_world_cameras={"gate":9999}
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_siluk"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_siluk")
    screenshot "redesign_world_siluk.png"
    $ r13_world_cameras={}
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_nero"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_nero")
    screenshot "redesign_world_nero.png"
    $ r13_world_cameras={}
    run Call("r13_qa_goto",*r13_qa_redesign_slot("resident_bori"))
    click pos (640,600) until screen "r13_hub" timeout 40
    pause 1.0
    $ r13_qa_redesign_record("resident_bori")
    screenshot "redesign_world_bori.png"

testcase redesign_dialogue:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_fullbody",("normal","large","topic"),list(R13_QA_REDESIGNED),["neutral","surprise"])
    click pos (1276,300) until eval r13_qa_fb_done timeout 300
    pause 1.0

testcase day1_note_spot:
    # 0.18.22 (owner): on day 1 the folded paper on the desk is pressed directly; then sleep opens.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="room13",life_poc=True,evidence=["E03"]),("lodging","entry_corrected"))
    pause 2.0
    assert eval (r13_object_visible(ROOM13["objects"]["room13"]["mother_note"]) and "책상 위" in r13_intro_goal())
    screenshot "day1_note_spot.png"
    click pos (195,398)
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval ("M01" in room13["evidence"] and r13_bed_available("bed") and not r13_object_visible(ROOM13["objects"]["room13"]["mother_note"]))
    pause 1.0
    screenshot "day1_after_note.png"

testcase admin_tool:
    # 0.18.22 owner's test tool: next-step list, hit areas, presets.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="room13",life_poc=True),("lodging","entry_corrected"))
    pause 2.0
    $ persistent.room13_admin=True
    $ r13_admin_hitboxes=True
    run Function(renpy.restart_interaction)
    pause 1.0
    screenshot "admin_hitboxes.png"
    click "관리자"
    pause 1.0
    assert screen "r13_admin"
    assert eval (any("M01" in l and l.startswith("필요 ·") for l in r13_admin_next()))
    screenshot "admin_next.png"
    click "이동·시점"
    click "2일 아침 · 여관"
    click pos (640,600) until screen "r13_hub" timeout 40
    assert eval (room13["day"]==2 and room13["location"]=="inn" and "M01" in room13["evidence"])
    $ persistent.room13_admin=False
    $ r13_admin_hitboxes=False

testcase scenario_dump:
    # Audit helper (not in the default list): writes scenario_dump.json next to the game.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Function(r13_qa_scenario_dump)

testcase compare_j09:
    # 0.18.22 audit: J09 (나비의 처음 말) is now read against E12 in the record comparison.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=5,period=0,location="inn",life_poc=True,case_state="occurred",evidence=["J09","E12"]),("lodging","entry_corrected"))
    pause 1.0
    assert eval ("좁혔다" in r13_compare_result(("J09","E12")))

testcase typography_roles:
    # 0.18.24: narration grey, thought blue with one pair of parentheses, item span in entity colour.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True,evidence=["E01","G1"]),("lodging","entry_corrected"))
    click pos (640,600) until screen "r13_hub" timeout 40
    run Jump("r13_qa_type_lines")
    pause 2.0
    screenshot "type_narration.png"
    click pos (640,600)
    pause 2.0
    screenshot "type_thought.png"
    click pos (640,600)
    pause 2.0
    screenshot "type_speech.png"
    click pos (640,600) until screen "r13_hub" timeout 40
    run Show("r13_records")
    pause 1.5
    screenshot "type_records.png"
    run Show("r13_backlog")
    pause 1.0
    screenshot "type_backlog.png"

testcase dot_fx:
    # 0.18.29 dot effects: fire, glow, snow, lamp and Daram's blink, plus motion-off stills.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_dot_fx")
    click pos (1276,300) until eval r13_qa_fx_done timeout 300
    pause 1.0


testcase karo_center:
    # 0.18.39 (owner): two-line dialogue window, Karo centred, same place in dialogue and questions.
    pause 2.0
    $ persistent.room13_large_text=True
    click "처음부터"
    pause 3.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    pause 1.0
    run Jump("r13_entry_karo_menu")
    pause 1.5
    screenshot "karo_topics.png"
    click "마차가 괜찮은지"
    pause 1.5
    screenshot "karo_line.png"
    $ persistent.room13_large_text=False

testcase opening_cut:
    # 0.18.41 opening cutscene (letter, map route, title, carriage): runs on a new game outside tests; forced here.
    pause 2.0
    $ r13_opening_force = True
    click "처음부터"
    pause 1.0
    screenshot "op_0_letter.png"
    pause 2.6
    screenshot "op_1_lines.png"
    pause 2.2
    screenshot "op_2_route.png"
    pause 2.6
    screenshot "op_3_pin.png"
    pause 3.0
    screenshot "op_4_title.png"
    pause 3.4
    screenshot "op_5_carriage.png"
    pause 3.0
    screenshot "op_6_after.png"
    assert eval (place == "마차 안" and persistent.room13_opening_cut_seen)
    $ r13_opening_force = False

testcase trial_counter:
    # 0.18.41: after C1 proves the passage, the chief turns it on Daram. A wrong answer keeps
    # the statement standing (no other penalty); presenting again and answering right breaks it.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_trial",('E01', 'E05', 'E06', 'E07', 'E09', 'E35'),())
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
    click "아이만 들어갔다"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "죽음의 원인이라는 주장"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    click "다시 휘두를 사람이"
    pause 0.6
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    screenshot "counter_menu.png"
    click "겁 많은 아이는"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    assert eval (not r13_debate_is_broken("C2","s3"))
    click "자료로 반박"
    pause 0.8
    click "QA E09"
    pause 0.6
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "주방 레버로만"
    pause 0.6
    click pos (640,600) until screen "r13_debate_board" timeout 40
    pause 0.6
    assert eval (r13_debate_is_broken("C2","s3"))
    $ r13_qa_dump()

testcase crossed_accounts:
    # 0.18.41: Kongi's word changes Nabi's answer; Seol's word opens a question for the lamplighter.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn"),())
    pause 1.0
    assert eval ("cross:nabi_door" in [k for k,t in r13_topics("nabi")] and "cross:nabi_light" not in [k for k,t in r13_topics("nabi")])
    $ r13_finish_topic("smalltalk:kongi_basket")
    assert eval ("cross:nabi_light" in [k for k,t in r13_topics("nabi")] and "cross:nabi_door" not in [k for k,t in r13_topics("nabi")])
    assert eval ("cross:lamp_dawn" not in [k for k,t in r13_topics("resident_lamplighter")])
    $ r13_finish_topic("smalltalk:seol_rope")
    assert eval ("cross:lamp_dawn" in [k for k,t in r13_topics("resident_lamplighter")])
    $ r13_finish_topic("smalltalk:tori_stitches")
    assert eval ("cross:tok_pin_job" in [k for k,t in r13_topics("resident_tok")])

testcase granny_later_keeps_topic:
    # 0.18.41: "다음에 하겠습니다" leaves the topic open; the same talk can still give H16.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",case_state="pending"),("know_granny_reads",))
    pause 1.0
    run Jump("r13_qa_granny_ask")
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "다음에 하겠습니다"
    pause 0.6
    click pos (640,600) until eval ("granny_letter_ask" in [k for k,t in r13_topics("granny")]) timeout 40
    assert eval (not r13_has("granny_dumb_done") and "H16" not in room13["evidence"])
    run Jump("r13_qa_granny_ask")
    click pos (640,600) until screen "choice" timeout 40
    pause 0.6
    click "아직 기다리고 있습니다"
    click pos (640,600) until eval ("H16" in room13["evidence"]) timeout 40
    assert eval (r13_has("granny_dumb_done"))

testcase title_fx:
    # 0.18.45 title: first-launch logo and menu fade in, dot snow and lamp flicker.
    pause 0.3
    screenshot "t0.png"
    pause 0.7
    screenshot "t1.png"
    pause 0.8
    screenshot "t2.png"
    pause 0.9
    screenshot "t3.png"
    pause 0.8
    screenshot "t4.png"
    assert eval (R13_TITLE_STATE["intro_done"])

testcase motion_reel:
    # 0.18.43 review reel: record the screen while this runs (not in the default set).
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_reel")
    click pos (1276,300) until eval r13_qa_reel_done timeout 120

testcase topic_record:
    # 0.18.50: a read question directly replays the kept conversation, without an extra menu.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="gate"),())
    pause 1.0
    $ r13_qa_rows=[("dad","당시 질문"),("karo","당시 대답 하나입니다."),("karo","당시 대답 둘, 조금 더 깁니다.")]
    $ r13_topic_shown=r13_qa_rows
    run Function(r13_finish_topic,"karo_road")
    assert eval (r13_topic_record("karo_road")==[["dad","당시 질문",False],["karo","당시 대답 하나입니다.",False],["karo","당시 대답 둘, 조금 더 깁니다.",False]])
    run Function(r13_edit,daram_state="held")
    assert eval ([t for w,t in r13_topic_key_lines("karo_road")]==["당시 대답 하나입니다.","당시 대답 둘, 조금 더 깁니다."])
    assert eval (r13_topic_when("karo_road")=="2일째 오전")
    run Jump("r13_qa_topic_review")
    click pos (640,640) until screen "r13_hub" timeout 40
    assert eval (r13_topic_record("karo_road")==[["dad","당시 질문",False],["karo","당시 대답 하나입니다.",False],["karo","당시 대답 둘, 조금 더 깁니다.",False]])
    pause 0.5
    screenshot "record_direct_return.png"

testcase conversation_skip:
    # 0.18.46: 건너뛰기 ends the current conversation; what follows it still runs.
    pause 2.0
    click "처음부터"
    pause 3.0
    click pos (1150,90) until screen "r13_hub" timeout 40
    pause 1.0
    run Jump("r13_entry_karo_menu")
    pause 1.5
    click "함께 왔다고"
    pause 1.5
    screenshot "skip_bar.png"
    click "건너뛰기"
    pause 1.5
    assert screen "r13_entry_karo_topics"

testcase memo_from_desk:
    # 0.18.48: reading Mom's memo from the desk close-up shows its card over the close-up, and the
    # envelope is gone from the desk afterwards.
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=1,period=1,location="room13",life_poc=True,evidence=["E03"]),("lodging","entry_corrected"))
    pause 1.0
    run Jump("r13_qa_inspect_desk")
    pause 1.0
    assert eval (not r13_memo_taken())
    click pos (450,170)
    click pos (640,600) until screen "r13_desk_inspection" timeout 40
    pause 0.4
    assert eval ("M01" in room13["evidence"] and r13_memo_taken() and renpy.get_screen("r13_evidence_found") is not None)
    screenshot "memo_card_over_desk.png"
    pause 2.6
    screenshot "desk_without_memo.png"

testcase tok_lamp_late:
    # 0.18.50: after any first choice at Tok's accusation, the lamp can still be checked on the square,
    # which opens Ubak's confession (and so Tok's release and testimony).
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=4,period=0,location="square"),("ep4_seen","ep4_open","entry_corrected","lodging"))
    pause 1.0
    assert eval ("ep4_lamp_look" in [k for k,a in r13_actions()])
    run Function(r13_finish_action,"ep4_lamp_look")
    assert eval (r13_has("clue_lamp_marks") and "ubak_lamp" in [k for k,t in r13_topics("resident_ubak")] or r13_has("clue_lamp_marks") and r13_where("resident_ubak") is None)

testcase admin_pin:
    # 0.18.50: settings → 관리자 도구 → PIN 4861 turns the tool on; a wrong PIN does not.
    pause 2.0
    $ persistent.room13_admin=False
    run Show("r13_admin_pin")
    pause 0.5
    click "1"
    click "2"
    click "3"
    click "4"
    click "확인"
    pause 0.3
    assert eval (not persistent.room13_admin)
    click "4"
    click "8"
    click "6"
    click "1"
    screenshot "pin_typed.png"
    click "확인"
    pause 0.3
    assert eval (persistent.room13_admin and not renpy.get_screen("r13_admin_pin"))
    $ persistent.room13_admin=False

testcase daram_bed:
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="room13",daram_state="with_dad",life_poc=True),("entry_corrected","lodging"))
    pause 1.5
    screenshot "daram_on_bed.png"

testcase long_topic_list:
    # 0.18.50: many topics grow the list upward instead of scrolling.
    pause 2.0
    $ persistent.room13_large_text=True
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=2,period=0,location="inn",life_poc=True),("entry_corrected","lodging"))
    pause 1.0
    $ r13_qa_person="granny"
    run Jump("r13_qa_talk_menu")
    pause 1.5
    screenshot "granny_topics.png"
    $ persistent.room13_large_text=False
