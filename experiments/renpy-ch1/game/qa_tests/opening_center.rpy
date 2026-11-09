# 승인된 표정 원본과 새 중앙 배경을 실제 시작 경로에서 확인한다.
testcase opening_center_and_quiet_arrival:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until eval (place=="마차 안" and r13_packet and r13_packet[0]=="daram" and "일곱 개" in r13_packet[1]) timeout 60
    $ opening_bounds=renpy.get_image_bounds("r13_visitor")
    assert eval (280<opening_bounds[0]<360 and opening_bounds[0]+opening_bounds[2]<840)
    assert eval (r13_current_pose=="seat_quiz" and r13_carriage_seat_shown=="quiz")
    screenshot "opening_center_quiz.png"
    click pos (900,600) until eval (r13_packet and r13_packet[0]=="daram" and r13_current_pose=="seat_angry") timeout 40
    assert eval (renpy.get_image_bounds("r13_visitor")==opening_bounds)
    screenshot "opening_center_angry.png"
    click pos (900,600) until eval (r13_packet and len(r13_packet)>2 and r13_packet[2].get("line_id")=="MS14_D01_S02_L0002") timeout 60
    assert eval (place=="눈에 막힌 입구" and not r13_packet[2].get("fx"))
    assert eval (all(renpy.music.get_playing(channel=c) is None for c in ["carriage_ride","carriage_hooves","scene_fx","sound"]))
    screenshot "opening_quiet_arrival.png"

testcase opening_center_skip:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until eval (place=="마차 안" and r13_packet and r13_packet[0]=="daram") timeout 60
    click "건너뛰기"
    click pos (900,600) until eval (place=="눈에 막힌 입구") timeout 40
    assert eval (all(renpy.music.get_playing(channel=c) is None for c in ["carriage_ride","carriage_hooves","scene_fx","sound"]))

testcase opening_center_motion_off:
    $ preferences.text_cps=0
    $ persistent.room13_motion=False
    pause 1.0
    click "처음부터"
    click pos (900,600) until eval (place=="마차 안" and r13_packet and r13_packet[0]=="daram") timeout 60
    $ opening_bounds=renpy.get_image_bounds("r13_visitor")
    assert eval (280<opening_bounds[0]<360 and opening_bounds[0]+opening_bounds[2]<840)
    click "건너뛰기"
    click pos (900,600) until eval (place=="눈에 막힌 입구") timeout 40
    assert eval (all(renpy.music.get_playing(channel=c) is None for c in ["carriage_ride","carriage_hooves","scene_fx","sound"]))

testcase opening_neoul_map_departure:
    $ preferences.text_cps=0
    pause 1.0
    click "처음부터"
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(r13_v111_commit,"MS14_D01_S02_L0019")
    run Function(r13_v111_commit,"MS14_D01_S03_L0002")
    run Function(r13_v111_commit,"MS14_D01_S03_L0007")
    run Jump("r13_v111_gate_proven")
    click pos (900,600) until eval (renpy.get_screen("r13_hub") and room13["v111"].get("gate")=="registered_menu") timeout 60
    # 지도에서 먼저 여관으로 이동한 직후의 상태를 준비한다. 소개·장소 복원·대화는 실제 출발 라벨을 탄다.
    run Function(r13_edit,location="inn")
    run Function(r13_v111_set,"location:daram","inn")
    run Jump("r13_v111_registered_depart")
    click pos (900,600) until eval (r13_packet and "마을 장부를 맡은 너울입니다" in r13_packet[1].replace("\n"," ")) timeout 60
    assert eval (room13["location"]=="gate" and all(r13_v111_value("location:"+p)=="gate" and r13_v111_actor_ready(p) for p in ["guard","daram","karo","neoul"]))
    assert eval (qa_nw_seen("초소 안쪽에서 다가온다") and qa_nw_seen("너울 씨, 이 두 분도"))
    screenshot "opening_neoul_introduction.png"
    click pos (900,600) until screen "r13_hub" timeout 60
    assert eval (r13_v111_value("heard_inn_order1") is True and room13["location"]=="inn")
