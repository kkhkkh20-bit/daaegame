testcase existing_carriage_direction:
    pause 1.0
    click "처음부터"
    pause 3.0
    assert screen "say"
    assert eval (ms14 is None and r13_packet[0] is None and r13_carriage_narrow)
    assert eval (r13_packet[1]=="다람이 과자 봉지를 외투 안쪽으로 당긴다.")
    assert eval (renpy.music.get_playing(channel="scene_fx") is not None)
    screenshot "carriage_direction_intro.png"
    click pos (900,600)
    pause 0.8
    assert eval (r13_packet[1]=="아빠는 안 잡아 줘?")
    screenshot "carriage_direction_dialogue.png"
    click "씬 건너뛰기"
    pause 2.0
    assert eval (place=="눈에 막힌 입구")
    assert eval (not renpy.music.get_playing(channel="scene_fx"))
    assert eval (not renpy.game.context().scene_lists.layer_at_list["master"][1])
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (ms14 is None and room13["location"]=="gate" and "E01" in room13["evidence"])

# Verify the reveal through uninterrupted ordinary dialogue, as well as skip above.
testcase existing_carriage_full:
    pause 1.0
    click "처음부터"
    pause 3.0
    click pos (900,600) until eval (r13_packet[1]=="또 읽어?") timeout 60
    assert screen "r13_evidence_card"
    pause 0.6
    screenshot "carriage_direction_letter.png"
    click pos (900,600) until eval (r13_packet[0]=="karo") timeout 60
    assert not screen "r13_evidence_card"
    assert eval (r13_packet[1].startswith("지붕 보입니다."))
    assert eval ("carriage_reveal" in r13_packet[2] and not r13_carriage_narrow)
    screenshot "carriage_direction_reveal.png"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (place=="눈에 막힌 입구" and ms14 is None)
    assert eval (not renpy.game.context().scene_lists.layer_at_list["master"][1])
    assert eval (not renpy.music.get_playing(channel="scene_fx"))

testcase existing_carriage_paged_skip:
    pause 1.0
    click "처음부터"
    pause 3.0
    click pos (900,600) until eval (r13_packet[0]=="karo") timeout 60
    assert eval (len(r13_pages)>1)
    click "씬 건너뛰기"
    pause 2.0
    assert eval (place=="눈에 막힌 입구" and not r13_carriage_narrow)
    assert eval (not renpy.game.context().scene_lists.layer_at_list["master"][1])
