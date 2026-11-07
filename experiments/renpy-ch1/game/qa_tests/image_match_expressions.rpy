# 실제 대사층·전용 표정층을 모두 통과한 얼굴을 확인한다. 장면 상태만 준비한다.
testcase image_match_expressions118:
    $ preferences.text_cps=0
    pause 1.0
    click '처음부터'
    click pos (900,600) until '편지를 외투 안에' timeout 60
    click pos (900,600) until screen 'r13_hub' timeout 90
    run Call('r13_qa_v111_place','gate',0)
    pause until screen 'r13_hub' timeout 30
    run Call('r13_qa_v111_lines',r13_v111_lines(['MS14_D01_S03_L0005']),'v111:gate_read_original:MS14_D01_S03_L0003')
    pause until screen 'say' timeout 30
    assert eval (r13_packet[2]['expression']=='angry' and not (r13_dialogue_beat or {}).get('context_key'))
    pause .7
    screenshot 'image-match-daram-name.png'
    click pos (900,600) until screen 'r13_hub' timeout 30
    run Function(qa_fire_deduction7)
    run Call('qa_rr_scene','r13_v111_bori_witness_heard7')
    pause until eval (r13_packet and '불이 번지기 전에' in r13_packet[1]) timeout 30
    assert eval (r13_packet[2]['expression']=='anxious')
    pause .7
    screenshot 'image-match-bori-witness.png'
    click pos (900,600) until screen 'r13_fire_links' timeout 60
