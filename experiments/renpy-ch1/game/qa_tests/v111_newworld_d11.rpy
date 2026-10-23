init python:
    def qa_nw_day11():
        r13_v111_set("day",11)
        r13_edit(day=11,location="school",period=2)
        r13_v111_set("route7","murder")
        r13_v111_set("OWL_ALIVE",False)
        r13_v111_set("DARAM_DETAINED",False)
        r13_v111_set("family_reunited",True)
        r13_v111_set("family_school_place",True)
        r13_grant(["V111:"+k for k in ("E11","E08","NW_PIKO_TREMOR","NW_KEEPER_DATE","NW_INNER_PRICE","NW_MUSOE_DEEP","NW_KKOMI_NOSTONE","NW_STONE")],"qa")

testcase v111_nw_d11_hyp_lost:
    # Gate 0: repeating the village's own word ends the meeting; nobody puts out a fire.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_v111_set,"tries:hypothesis",R13_NW_TRIES-1)
    run Jump("r13_v111_hypothesis11")
    click pos (900,600) until "아르카가 사람을 부른다" timeout 60
    click "아르카가 사람을 부른다"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:hypothesis")=="lose" and r13_v111_owned("NW_SICK_BEDS"))
    assert eval (qa_nw_seen("불려 간 사람은 복을 받은 거고") and qa_nw_seen("모독한 손님") and qa_nw_seen("아랫길 등 끊음") and not qa_nw_seen("아르카등을 끈다"))

testcase v111_nw_d11_hyp_wrong_reason:
    # A wrong reason leaves that house's fire burning and moves on to the next question.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_v111_set,"tries:hypothesis",R13_NW_TRIES-1)
    run Jump("r13_v111_hyp1_q11")
    click pos (640,300) until "초롱은 젊어서 버틴다" timeout 60
    click "초롱은 젊어서 버틴다"
    click pos (640,300) until "백 부인은 그 돌 곁에서 잠을 자지 않는다" timeout 60
    assert eval (r13_v111_value("hyp_issue:1")=="lost" and qa_nw_seen("초소 불은 그대로 두겠소"))

testcase v111_nw_d11_hyp_partial:
    # Gates held, the storehouse question lost: only some fires go out.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_v111_set,"hyp_issue:1","won")
    run Function(r13_v111_set,"hyp_issue:2","lost")
    run Function(r13_v111_set,"hyp_issue:3","won")
    run Function(r13_v111_set,"hyp_issue:4","won")
    run Jump("r13_v111_hyp5_won11")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:hypothesis")=="partial")
    assert eval (qa_nw_seen("창고 문은 잠긴 채다") and qa_nw_seen("일부 집의 돌 회수") and qa_nw_seen("아르카등을 끈다") and not qa_nw_seen("내 측정도 같아"))

testcase v111_nw_d11_hyp_won:
    # Every question answered: most of the village puts out its fires; Mother's note.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Function(r13_v111_set,"hyp_issue:1","won")
    run Function(r13_v111_set,"hyp_issue:2","won")
    run Function(r13_v111_set,"hyp_issue:3","won")
    run Function(r13_v111_set,"hyp_issue:4","won")
    run Jump("r13_v111_hyp5_won11")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:hypothesis")=="win" and r13_v111_value("lower_lights_cut") is True)
    assert eval (qa_nw_seen("집집의 돌 회수") and qa_nw_seen("내 측정도 같아") and qa_nw_seen("사람들이 하나둘 일어선다"))

testcase v111_nw_d11_hyp_stone_proof:
    # Gate 5 played through the real proof screen with the unmarked stone.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Jump("r13_v111_hyp5_proof11")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:NW_STONE"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("meeting:hypothesis")=="partial")
    assert eval (qa_nw_seen("각인 없는 검푸른 돌입니다") and qa_nw_seen("침상 목록을 가슴에 끌어안는다"))

testcase v111_nw_d11_hyp1_two_records:
    # 0.20.4 proof scope: Chorong's log and Piko's tremor are enough for issue 1;
    # the father adds what the lamp record (E08) would have shown.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 접는다" timeout 60
    click "편지를 접는다"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Jump("r13_v111_hyp1_proof11")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E11"
    pause 0.8
    click "QA V111:NW_PIKO_TREMOR"
    pause 0.8
    click "QA 닫기"  # 0.20.7: the proof book stays open between picks
    pause 0.5
    click "선택한 근거 제출"
    click pos (640,300) until "백 부인은 그 돌 곁에서 잠을 자지 않는다" timeout 60
    assert eval (r13_v111_value("hyp_issue:1")=="won" and qa_nw_seen("받침에서 멀어지면 바닥이 차갑습니다"))
