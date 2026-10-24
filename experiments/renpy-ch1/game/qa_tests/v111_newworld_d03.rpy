init python:
    def qa_nw_day3_meeting_ready():
        # State the authored day-3 meeting entry requires (owned records and consent).
        r13_v111_set("day",3)
        r13_grant(["V111:"+k for k in ("E11","E12","E13","E14","E15","E16","E32")],"qa")
        r13_v111_set("silluk_knife_comparison_consent",True)
        r13_v111_set("silluk.children.location","workshop_with_buri")
        r13_edit(location="workshop")

testcase v111_nw_d03_lamp_lost:
    # Losing Tok's innocence (gate) ends the meeting: Tok is listed, Silluk walks free.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"tries:lamp",r13_nw_tries_max("lamp")-1)
    run Jump("r13_v111_trial_wrong")
    pause 1.0
    click pos (900,600) until "확인된 3번 돌을 돌려 달라고 한다" timeout 90
    assert eval (r13_v111_value("meeting:lamp")=="lose" and r13_v111_value("listed:resident_tok") is True)
    assert eval (qa_nw_seen("그것으로 됐소") and qa_nw_seen("보호시설 명단에도") and qa_nw_seen("톡에게서 받아 내시오") and not qa_nw_seen("어느 때 생긴 흔적인지부터"))
    click "확인된 3번 돌을 돌려 달라고 한다"
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("silluk_status")=="released" and r13_v111_value("stone_choice_completed") is True)
    run Function(r13_edit,location="square")
    run Jump("r13_v111_restore3")
    pause 1.0
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("초롱이 혼자 받침에 돌을 끼운다"))
    screenshot "v111_nw_d03_lost.png"

testcase v111_nw_d03_lamp_partial:
    # A later issue lost: partial. Tok is cleared, Silluk is only a man who sold a found stone.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"tries:lamp",r13_nw_tries_max("lamp")-1)
    run Jump("r13_v111_trial_wrong_latch")
    pause 1.0
    click pos (900,600) until "오늘은 반환 요구를 보류한다" timeout 90
    assert eval (r13_v111_value("meeting:lamp")=="partial" and not r13_v111_value("listed:resident_tok"))
    # The meeting is set up at its start, so the loss counts at the repair step (audit 2026-10-22).
    assert eval (qa_nw_seen("짐 나른 걸로 사람을 붙잡아 둘 순 없소") and qa_nw_seen("누가 꺼냈는지도 못 밝혔"))
    click "오늘은 반환 요구를 보류한다"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("silluk_status")=="released")

testcase v111_nw_d03_lamp_won:
    # Win keeps the authored custody choice; handing Silluk to Neoul lists him.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"lamp_theft_supported",True)
    run Jump("r13_v111_badugi_arrives")
    pause 1.0
    click pos (900,600) until "확인된 3번 돌을 돌려 달라고 한다" timeout 90
    click "확인된 3번 돌을 돌려 달라고 한다"
    click pos (900,600) until "증거를 넘기고 너울이 실룩을 데려가게 한다" timeout 90
    assert eval (r13_v111_value("meeting:lamp")=="win")
    click "증거를 넘기고 너울이 실룩을 데려가게 한다"
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (r13_v111_value("listed:resident_siluk") is True and r13_v111_value("silluk_status")=="detained_work_waiting_station")
