init python:
    def qa_altar4_prior_wins():
        for i in (1,2,3): r13_v111_set("altar_issue:%d"%i,"won")
    def qa_altar4_ending_requirements():
        r13_v111_set("ending14","morning")
        for who,k in R13_NW_LIVES: r13_v111_set(k,True)
        for m in ("records","hypothesis","blanket"): r13_v111_set("meeting:"+m,"win")
        for m in ("fire","soup"): r13_v111_set("grand:"+m,True)

testcase v111_altar4_basic_rations:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Jump("r13_v111_morning_safe14")
    click pos (900,600) until eval r13_v111_owned("NW_OLD_RATIONS") timeout 150
    assert eval (not r13_v111_owned("NW_NEOUL_LEDGER") and qa_nw_seen("4년 전 집별 돌 배급표"))
    run Function(r13_grant,["V111:NW_NAMES"],"qa")
    run Function(qa_altar4_prior_wins)
    run Jump("r13_v111_altar4_proof14")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_NAMES"
    pause 0.8
    click "QA V111:NW_OLD_RATIONS"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (r13_v111_value("meeting:altar")=="win") timeout 90
    assert eval (r13_v111_value("dallae_first_victim_known") and qa_nw_seen("학교에서 확인한 4년 전") and not qa_nw_seen("너울 씨 장부 상자의 4년 전"))
    run Function(qa_altar4_ending_requirements)
    assert eval (r13_nw_loss_count()==0 and not r13_nw_true_ending_ready() and not r13_v111_owned("NW_NEOUL_LEDGER"))
    run Function(r13_grant,["V111:NW_NEOUL_LEDGER"],"qa")
    assert eval r13_nw_true_ending_ready()

testcase v111_altar4_original_ledger:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14,"prevented")
    run Function(r13_grant,["V111:NW_NAMES","V111:NW_NEOUL_LEDGER"],"qa")
    run Function(qa_altar4_prior_wins)
    run Jump("r13_v111_altar4_proof14")
    pause 1.5
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_NAMES"
    pause 0.8
    click "QA V111:NW_NEOUL_LEDGER"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until eval (r13_v111_value("meeting:altar")=="win") timeout 90
    assert eval (qa_nw_seen("너울 씨 장부 상자의 4년 전") and not qa_nw_seen("학교에서 확인한 4년 전"))
