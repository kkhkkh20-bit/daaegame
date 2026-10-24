label r13_v111_qa_day13_reactions:
    # 13일 아침 반응 묶음만 본다(13일 진입 조건을 다 맞추지 않고 문장과 조건을 확인한다).
    call r13_scene(R13_PLACES["dining"][1],R13_PLACES["dining"][0],"calm")
    call r13_lines(r13_nw_block('kkomi_gone13'),'nw:kkomi_gone13')
    call r13_lines(r13_nw_block('fever13'),'nw:fever13')
    $ r13_v111_set('qa_reactions_done',True)
label r13_v111_qa_hold13:
    pause
    jump r13_v111_qa_hold13

testcase v111_nw_aftermath_reactions:
    # 0.20.20 뒤 반응: 꼬미의 빈자리와 다람의 열이 13일 아침까지 이어진다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"kkomi_soup_dead",True)
    run Function(r13_v111_set,"daram_fever12",True)
    run Jump("r13_v111_qa_day13_reactions")
    pause 1.0
    click pos (900,600) until eval (r13_v111_value("qa_reactions_done") is True) timeout 60
    assert eval (qa_nw_seen("꼬미 자리에 도토리 놔 둘래") and qa_nw_seen("대장은 오늘 누워 있는 거야"))

testcase v111_nw_aftermath_memorial:
    # 0.20.20 결말에서 이름 부르기: 죽은 사람마다 남은 물건 한 줄. 산 사람 줄은 나오지 않는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day14)
    run Function(r13_v111_set,"piko_alive",False)
    run Function(r13_v111_set,"KKOMI_ALIVE",False)
    run Function(r13_v111_set,"nero_alive",False)
    run Function(r13_v111_set,"alive:neoul",False)
    run Function(r13_v111_set,"crowd_intervention","failed")
    run Function(r13_v111_set,"crowd_blocked_by_dad",True)
    run Jump("r13_v111_ending_dispatch14")
    click pos (900,600) until screen "r13_confirm" timeout 120
    assert eval (r13_v111_value("ending14")=="frozen")
    assert eval (qa_nw_seen("피코의 이젤은 그대로") and qa_nw_seen("도토리 한 알이 놓여") and qa_nw_seen("네로의 장갑 한 짝"))
    assert eval (qa_nw_seen("알 하나가 빠져 있었다") and qa_nw_seen("누가 먼저 쳤는지는 아무도 몰라요"))
    assert eval (qa_nw_seen("등 뒤에서 들린 소리") and not qa_nw_seen("작은 그릇 하나를 날마다") and not qa_nw_seen("모모 씨의 이름은"))

testcase v111_fork_fate_points:
    # 0.20.20 갈림길: 판정 시점 칸이 회의 사이에 들어가고, 이번 판 결과만 이름이 보인다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_fork_fixture)
    run Function(r13_fork_set_fate,"fate_piko","lost")
    run Function(r13_fork_set_fate,"fate_kkomi","saved")
    run Show('r13_records')
    pause 0.5
    click '갈림길'
    pause 0.5
    assert screen 'r13_fork_screen'
    assert eval ([c['key'] for c in r13_fork_columns()][:6]==['gate','fate_piko','lamp','gate_post','fate_kkomi','fire'])
    assert eval ([c['key'] for c in r13_fork_columns() if c.get('fate')]==['fate_piko','lamp','gate_post','fate_kkomi','fire'])
    screenshot "fork_fate_points.png"
