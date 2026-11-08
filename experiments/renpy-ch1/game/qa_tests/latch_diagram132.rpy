# 준비한 정상 3일차 회의에서 실제 설명 대사·표시·정리를 확인한다.
testcase latch132_diagram_outer_inner_clear:
    run Function(renpy.set_physical_size,(1280,720))
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_piko112_meeting)
    run Function(r13_grant,['V111:E17','V111:E33'],'qa:latch132')
    $ qa_latch132_evidence=tuple(room13['evidence'])
    $ qa_latch132_tries=r13_v111_value('tries:lamp')
    $ qa_latch132_proof=r13_v111_value('proof_given:바깥 걸쇠 주장과 발견 위치를 대조한다')
    run Call("qa_rr_scene","r13_v111_trial_latch_ok")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S05_L0021') timeout 45
    pause .8
    assert eval (r13_ep_cut_current=='latch132_outer' and renpy.get_screen('r13_latch_diagram132') and r13_meeting_active)
    screenshot "latch132-outer-desktop.png"
    # 0.20.131 대사 중 저장의 packet에는 cut가 없었다. 같은 대사/서사에서 복원 경계를 검사한다.
    $ r13_packet=tuple(r13_packet[:2])+(dict((k,v) for k,v in r13_packet[2].items() if k!='cut'),)+tuple(r13_packet[3:])
    $ r13_ep_cut_current=None
    run Hide("r13_latch_diagram132")
    run Function(r13_latch132_after_load)
    pause .4
    assert eval (r13_ep_cut_current=='latch132_outer' and renpy.get_screen('r13_latch_diagram132') and 'cut' not in r13_packet[2])
    screenshot "latch132-legacy-packet-restored.png"
    $ qa_latch132_touch=r13_touch_ui
    $ qa_latch132_large=persistent.room13_large_text
    $ r13_touch_ui=lambda:True
    $ persistent.room13_large_text=True
    run Function(renpy.set_physical_size,(844,390))
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S05_L0023') timeout 45
    pause .8
    assert eval (r13_ep_cut_current=='latch132_inner' and renpy.get_screen('r13_latch_diagram132'))
    screenshot "latch132-inner-phone-large.png"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D03_S05_L0025') timeout 60
    pause .4
    assert eval (not r13_ep_cut_current and not renpy.get_screen('r13_latch_diagram132'))
    run Function(r13_latch132_after_load)
    assert eval (not r13_ep_cut_current and not renpy.get_screen('r13_latch_diagram132'))
    screenshot "latch132-next-issue-clear.png"
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    assert eval (not renpy.get_screen('r13_latch_diagram132') and tuple(room13['evidence'])==qa_latch132_evidence and r13_v111_value('tries:lamp')==qa_latch132_tries and r13_v111_value('proof_given:바깥 걸쇠 주장과 발견 위치를 대조한다')==qa_latch132_proof)
    $ r13_touch_ui=qa_latch132_touch
    $ persistent.room13_large_text=qa_latch132_large
    run Function(renpy.set_physical_size,(1280,720))
