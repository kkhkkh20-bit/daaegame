# 실제 시작 뒤 보유 자료만 준비하는 읽기 화면 검수 fixture.
testcase reading_review_proof:
    $ preferences.text_cps=0
    $ persistent.room13_pw_controls_seen=False
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Function(r13_grant,["V111:E01","V111:E02","V111:E03","V111:E04"],"qa")
    run Jump("r13_v111_gate_proof")
    pause until screen "r13_proof_workspace" timeout 40
    pause .5
    screenshot "증거_첫안내.png"
    click id "r13_pw_open_E04"
    pause .5
    screenshot "증거상세_PC.png"

testcase reading_review_end:
    pause 1.0
    run Show("reading_review_ending_background")
    run Show("r13_end_card",name="남겨진 이름",stat="지킨 사람 7 · 잃은 사람 2",lost="피코 · 톡")
    pause .6
    screenshot "결말_첫화면.png"
    click id "r13_end_details"
    pause .3
    screenshot "결말_기록펼침.png"

screen reading_review_ending_background():
    zorder 99
    add r13_end_cut_art("END-09")

testcase reading_review_room_targets:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_set,"gate_registered",True)
    run Function(r13_edit,location="room13")
    run Jump("r13_v111_room_empty")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="note_pick" and room13["location"]=="room13") timeout 60
    pause 1.0
    if eval (r13_world_offset()>0):
        click pos (48,276)
        pause .8
    assert eval (r13_world_offset()==0 and room13["v111"]["gate"]=="note_pick")
    screenshot "13호실_조사.png"
    # 기존 사각형 밖 5px, 새 허용 범위 안. 정답·획득 순서는 같은 라벨에서 처리한다.
    click pos (155,407)
    click pos (900,600) until screen "r13_proof_workspace" timeout 60
    assert eval (r13_v111_owned("E06") and r13_v111_owned("E30"))
    assert eval (renpy.get_screen("r13_proof_workspace").scope.get("view")=="pair")
    assert eval (tuple(renpy.get_screen("r13_proof_workspace").scope.get("pair"))==("V111:E01","V111:E06"))
    assert eval (not room13["arguments"].get("v111:두 편지를 나란히 본다"))
    screenshot "13호실_편지두장.png"
