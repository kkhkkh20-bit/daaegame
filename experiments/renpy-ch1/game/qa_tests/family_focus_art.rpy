# 실제 대사·기존 물건 그림을 쓰는 첫 발견 화면 시험. 진행은 13호실 상태로 준비한다.
testcase family_focus_art:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Call("r13_qa_v111_place","room13",0)
    pause until screen "r13_hub" timeout 45
    $ qa_focus_evidence_before=tuple(room13['evidence'])
    run Call("r13_qa_v111_lines",r13_v111_lines(['MS14_D01_S05_L9101','MS14_D01_S05_L0020','MS14_D01_S05_L0021']),"qa:family-note")
    pause until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D01_S05_L9101') timeout 30
    assert eval (r13_ep_cut_current=='focus:E06' and renpy.showing('r13_ep_cut'))
    pause .8
    screenshot "family-focus-note.png"
    click pos (900,600) until screen "r13_hub" timeout 40
    assert eval (not r13_ep_cut_current and not renpy.showing('r13_ep_cut'))
    run Call("r13_qa_v111_lines",r13_v111_lines(['MS14_D01_S05_L0023','MS14_D01_S05_L0024','MS14_D01_S05_L0025','MS14_D01_S05_L0026']),"qa:family-drawing")
    pause until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D01_S05_L0023') timeout 30
    assert eval (r13_ep_cut_current=='focus:D01_FAMILY_DRAWING')
    pause .8
    screenshot "family-focus-drawing.png"
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D01_S05_L0026') timeout 35
    assert eval (not r13_ep_cut_current and not renpy.showing('r13_ep_cut'))
    click pos (900,600) until screen "r13_hub" timeout 30
    $ qa_focus_touch_before=r13_touch_ui
    $ qa_focus_large_before=persistent.room13_large_text
    $ r13_touch_ui=lambda: True
    $ persistent.room13_large_text=True
    run Call("r13_qa_v111_lines",r13_v111_lines(['MS14_D01_S05_L0045','MS14_D01_S05_L0046','MS14_D01_S05_L0047','MS14_D01_S05_L0048','MS14_D01_S05_L0049']),"qa:family-snack")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get('line_id')=='MS14_D01_S05_L0046') timeout 30
    assert eval (r13_ep_cut_current=='focus:D01_SNACK_BAG')
    pause .8
    screenshot "family-focus-snack-large-touch.png"
    click pos (900,600) until screen "r13_hub" timeout 40
    assert eval (not r13_ep_cut_current and not renpy.showing('r13_ep_cut') and tuple(room13['evidence'])==qa_focus_evidence_before)
    $ r13_touch_ui=qa_focus_touch_before
    $ persistent.room13_large_text=qa_focus_large_before
