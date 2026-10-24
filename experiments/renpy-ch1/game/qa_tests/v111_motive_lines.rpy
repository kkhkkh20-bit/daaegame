# 2026-10-24 동기 줄 4차(docs/reviews/motive-lines-20261024/문구시안.md): 넣은 줄이 그 경로에서 실제로 나오는지 본다.

testcase v111_motive_d02_karo:
    # 2일 입구: 까로의 쇠 축과 수리점 톡.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",2)
    run Function(r13_flag,"v111:applied:option:sleep1:0")
    run Function(r13_edit,location="gate")
    run Jump("r13_v111_day2")
    click pos (900,600) until "직접 알려 드릴게요" timeout 90
    assert eval (qa_nw_seen("이건 쇠 축이에요") and qa_nw_seen("수리점 톡이요") and qa_nw_seen("내일 아침에 축 떼어서"))

testcase v111_motive_d03_square:
    # 3일 아침 광장(피코가 산 판): 까로가 축을 멘 채 서 있고, 아빠가 너울에게 마차 이야기를 한다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",3)
    run Function(r13_v111_set,"piko_alive",True)
    run Function(r13_grant,["V111:E09"],"qa")
    run Function(r13_edit,location="square")
    run Jump("r13_v111_lamp3")
    click pos (900,600) until screen "r13_hub" timeout 120
    assert eval (qa_nw_seen("수리점 쪽이 아니라 광장 쪽을") and not qa_nw_seen("꺼진 3번 등 쪽을 한참 보다가"))
    assert eval (qa_nw_seen("봄까지 내 마차는 못 굴러가요") and qa_nw_seen("장부엔 사정을 안 적소"))

testcase v111_motive_d03_tok_freed:
    # 3일 회의에서 톡이 풀려난 판: 회의가 끝난 공방에서 축 이야기.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"meeting:lamp","partial")
    run Function(r13_edit,location="square")
    run Jump("r13_v111_restore_route")
    click pos (900,600) until "품삯은 안 받을게요" timeout 90
    assert eval (qa_nw_seen("아까 맡기고 가셨어요") and not qa_nw_seen("명단에 올랐대요"))

testcase v111_motive_d03_tok_listed:
    # 3일 회의를 진 판: 톡은 명단에 오르고 작업 대기소로 끌려가면서도 축을 맡는다.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day3_meeting_ready)
    run Function(r13_v111_set,"meeting:lamp","lose")
    run Function(r13_nw_list,"resident_tok","lamp_lose")
    run Function(r13_edit,location="square")
    run Jump("r13_v111_restore_route")
    click pos (900,600) until "고친 게 하나라도" timeout 90
    assert eval (qa_nw_seen("명단에 올랐대요") and qa_nw_seen("축은 그 전에 끝낼게요") and not qa_nw_seen("아까 맡기고 가셨어요"))

testcase v111_motive_d07_morning:
    # 6일 밤은 학교에서 잤다: 7일 빨래터로 가기 전 학교에서 나비와 장작 이야기.
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"day",6)
    run Function(r13_grant,["V111:E06_FIRE"],"qa")
    run Function(r13_edit,location="school")
    run Jump("r13_v111_sleep6_done")
    click pos (900,600) until screen "r13_hub" timeout 90
    assert eval (r13_v111_value("day")==7 and qa_nw_seen("아껴 때면 이틀이요") and qa_nw_seen("그땐 그때 봐야죠"))

testcase v111_motive_d13_cart:
    # 13일 수레 앞: 다람이 이송 명단의 빈 칸을 묻는다(다람이 명단에 없던 판).
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_nw_day13)
    run Function(r13_v111_set,"meeting:blanket","win")
    run Jump("r13_v111_rein13")
    click pos (900,600) until screen "r13_crisis_proof" timeout 90
    assert eval (qa_nw_seen("저 빈 칸은 뭐야") and qa_nw_seen("다음에 탈 사람 자리") and qa_nw_seen("값이 두 배였습니다"))
