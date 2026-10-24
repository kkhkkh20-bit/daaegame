# 2026-10-24 틀렸을 때 아빠 속말(MEETING_RULES_V2.md 6장 1번): 같은 쟁점에서 1·2·3번째 틀림마다 다른 줄이 나온다.
# 서로 다른 회의 넷 — 3일 칼(선택지), 10일 13호 구리선(증명), 11일 가설 창고(선택지), 12일 수프 명단(증명).
# 문구는 room13_v111_newworld_rules.rpy R13_NW_WRONG_THOUGHTS. 보고서 docs/reviews/wrong-thoughts-20261024/적용보고.md
init python:
    def qa_wt(issue,n):
        return R13_NW_WRONG_THOUGHTS[issue][n]
    def qa_wt_upto(issue,n):
        """n번째까지의 줄은 보였고, 그다음 줄은 아직 안 보였다. 세 줄은 서로 다르다."""
        # 긴 줄은 대사창이 문장 끝(……)에서 두 장으로 나누므로 앞부분으로 찾는다.
        rows=[qa_wt(issue,i)[:14] for i in (1,2,3)]
        if len(set(rows))!=3:return False
        if not all(qa_nw_seen(rows[i-1]) for i in range(1,n+1)):return False
        return all(not qa_nw_seen(rows[i-1]) for i in range(n+1,4))

testcase v111_wrong_thoughts_knife:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Jump("r13_v111_trial_knife")
    pause 1.5
    click "칼 모양만으로 지목한다"
    pause 1.0
    click pos (640,300) until "칼 모양만으로 지목한다" timeout 90
    assert eval (r13_v111_value("tries:lamp")==1 and qa_wt_upto("menu:trial_knife",1))
    click "칼 모양만으로 지목한다"
    pause 1.0
    click pos (640,300) until "칼 모양만으로 지목한다" timeout 90
    assert eval (r13_v111_value("tries:lamp")==2 and qa_wt_upto("menu:trial_knife",2))
    click "칼 모양만으로 지목한다"
    pause 1.0
    click pos (640,300) until "칼 모양만으로 지목한다" timeout 90
    assert eval (r13_v111_value("tries:lamp")==3 and qa_wt_upto("menu:trial_knife",3) and r13_v111_value("meeting:lamp") is None)

testcase v111_wrong_thoughts_room13:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day,10,"murder")
    run Function(r13_edit,location="school")
    run Function(r13_grant,["V111:E08_WOUND_WIRE","V111:E09_PIN_OWNER","V111:E01"],"qa")
    run Jump("r13_v111_owner_proof10")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:room13")==1 and qa_wt_upto("구리선과 수선 출처를 대조한다",1))
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:room13")==2 and qa_wt_upto("구리선과 수선 출처를 대조한다",2))
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:room13")==3 and qa_wt_upto("구리선과 수선 출처를 대조한다",3) and r13_v111_value("meeting:room13") is None)

testcase v111_wrong_thoughts_hyp_store:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day11)
    run Jump("r13_v111_hyp2_q11")
    click pos (640,300) until "켜지 않고 쌓아 둔 돌은 아무 해가 없다" timeout 60
    click "켜지 않고 쌓아 둔 돌은 아무 해가 없다"
    pause 1.0
    click pos (640,300) until "켜지 않고 쌓아 둔 돌은 아무 해가 없다" timeout 90
    assert eval (r13_v111_value("tries:hypothesis")==1 and qa_wt_upto("menu:hyp2",1))
    click "백 부인은 돌을 팔기만 한다"
    pause 1.0
    click pos (640,300) until "켜지 않고 쌓아 둔 돌은 아무 해가 없다" timeout 90
    assert eval (r13_v111_value("tries:hypothesis")==2 and qa_wt_upto("menu:hyp2",2))
    click "켜지 않고 쌓아 둔 돌은 아무 해가 없다"
    pause 1.0
    click pos (640,300) until "켜지 않고 쌓아 둔 돌은 아무 해가 없다" timeout 90
    assert eval (r13_v111_value("tries:hypothesis")==3 and qa_wt_upto("menu:hyp2",3) and r13_v111_value("hyp_issue:2") is None)

testcase v111_wrong_thoughts_soup_list:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day12)
    run Function(r13_v111_set,"teacher_confessed",True)
    run Function(r13_grant,["V111:NW_TRANSFER_LIST","V111:NW_WHITE_BOWLS","V111:E01"],"qa")
    run Jump("r13_v111_list_proof12")
    pause 1.5
    assert screen "r13_crisis_proof"
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:soup")==1 and qa_wt_upto("명단과 흰 그릇을 대조한다",1))
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:soup")==2 and qa_wt_upto("명단과 흰 그릇을 대조한다",2))
    click "자료 고르기"
    pause 0.5
    click "QA V111:E01"
    pause 0.8
    click "QA 닫기"
    pause 0.5
    click "선택한 근거 제출"
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (r13_v111_value("tries:soup")==3 and qa_wt_upto("명단과 흰 그릇을 대조한다",3) and r13_v111_value("meeting:soup") is None)
