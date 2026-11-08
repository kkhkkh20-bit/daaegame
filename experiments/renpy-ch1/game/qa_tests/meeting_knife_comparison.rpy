# 실제 대조 선택 뒤에만 실물을 확대하고 다음 쟁점에서는 인물로 돌아온다.
testcase meeting_knife_tip_closeup:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko112_meeting)
    assert eval (not r13_nw_comparison and not r13_v111_owned('E33'))
    run Call("qa_rr_scene","r13_v111_knife_fit")
    click pos (900,600) until eval (r13_nw_comparison=='knife_tip') timeout 60
    pause 1.0
    assert eval (r13_meeting_active and r13_meeting_claim=='NW:lamp')
    screenshot "knife-tip-physical-match.png"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S05_L9101') timeout 60
    assert eval (r13_nw_comparison is None and r13_v111_owned('E33') and r13_v111_owned('E17'))
    pause 1.0
    screenshot "knife-tip-confirmed-record.png"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    assert eval (r13_nw_comparison is None and not r13_v111_value('tries:lamp') and not r13_v111_value('lamp_theft_supported'))
    assert eval (v111_claim=='v111:바깥 걸쇠 주장과 발견 위치를 대조한다')
