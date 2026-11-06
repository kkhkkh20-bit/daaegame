init python:
    def qa_nw_day5(presented):
        r13_v111_set("day",5)
        r13_grant(["V111:"+k for k in ("E20","E22","E23","E24")],"qa")
        r13_edit(location="gate")
        store.v111_last_presented=list(presented)

testcase v111_nw_d05_half_then_lost:
    # Part of the right set once: one more try. A wrong answer after that is final.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day5,["V111:E20"])
    run Function(r13_v111_set,"tries:gate_post",r13_nw_tries_max("gate_post")-2)
    run Jump("r13_v111_wrong5")
    pause 1.0
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    assert eval (r13_v111_value("tries:gate_post")==r13_nw_tries_max("gate_post")-1 and r13_v111_value("meeting:gate_post") is None)
    assert eval (qa_nw_seen("무언가 말하려다 입을 다문다") and not qa_nw_seen("명단에 올리시오"))
    run Function(qa_nw_day5,["V111:E20"])
    run Jump("r13_v111_wrong5")
    pause 1.0
    if screen "r13_meeting_retry_choice":
        click id "r13_meeting_retry_accept"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("meeting:gate_post")=="lose" and r13_v111_value("listed:bami") is True and r13_v111_value("bami_status")=="listed")
    assert eval (qa_nw_seen("밤이는 보호시설에 보낼 명단에") and qa_nw_seen("밤이 아니라고 했잖아"))
    screenshot "v111_nw_d05_lost.png"

testcase v111_nw_d05_extra_e21_wins:
    # 0.20.4 proof scope: the four needed records plus Bami's own testimony (E21) win;
    # Neoul sets the child's own word aside in one line. An unrelated extra still fails.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day5,[])
    run Function(r13_grant,["V111:E21"],"qa")
    assert eval (r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E20","V111:E21","V111:E22","V111:E23","V111:E24"]))
    assert eval (not r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E01","V111:E20","V111:E22","V111:E23","V111:E24"]))
    assert eval (not r13_v111_proof_accepts("밤이 혐의의 근거를 확인한다",["E20","E22","E23","E24"],["V111:E20","V111:E21","V111:E22","V111:E23"]))
    run Jump("r13_v111_proof5")
    pause 1.5
    assert screen "r13_proof_workspace"
    if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E20") is None):
        if eval (renpy.get_screen("r13_proof_workspace").scope["page"]>0):
            click id "r13_pw_prev" until eval (renpy.get_screen("r13_proof_workspace").scope["page"]==0) timeout 20
        if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E20") is None):
            click id "r13_pw_next" until eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E20") is not None) timeout 20
    click id "r13_pw_check_E20"
    if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E21") is None):
        if eval (renpy.get_screen("r13_proof_workspace").scope["page"]>0):
            click id "r13_pw_prev" until eval (renpy.get_screen("r13_proof_workspace").scope["page"]==0) timeout 20
        if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E21") is None):
            click id "r13_pw_next" until eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E21") is not None) timeout 20
    click id "r13_pw_check_E21"
    if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E22") is None):
        if eval (renpy.get_screen("r13_proof_workspace").scope["page"]>0):
            click id "r13_pw_prev" until eval (renpy.get_screen("r13_proof_workspace").scope["page"]==0) timeout 20
        if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E22") is None):
            click id "r13_pw_next" until eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E22") is not None) timeout 20
    click id "r13_pw_check_E22"
    if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E23") is None):
        if eval (renpy.get_screen("r13_proof_workspace").scope["page"]>0):
            click id "r13_pw_prev" until eval (renpy.get_screen("r13_proof_workspace").scope["page"]==0) timeout 20
        if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E23") is None):
            click id "r13_pw_next" until eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E23") is not None) timeout 20
    click id "r13_pw_check_E23"
    if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E24") is None):
        if eval (renpy.get_screen("r13_proof_workspace").scope["page"]>0):
            click id "r13_pw_prev" until eval (renpy.get_screen("r13_proof_workspace").scope["page"]==0) timeout 20
        if eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E24") is None):
            click id "r13_pw_next" until eval (renpy.get_widget("r13_proof_workspace","r13_pw_check_E24") is not None) timeout 20
    click id "r13_pw_check_E24"
    click id "r13_pw_submit"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:gate_post")=="win" and r13_v111_value("listed:bami") is not True)
    assert eval (qa_nw_seen("아이 말은 그렇다 치고") and not qa_nw_seen("의심받는 아이 말로"))
    assert eval (qa_nw_seen("종이 접어 줘요. 더 작게.") and qa_nw_seen("밤이는 작아진 종이를 받아"))
