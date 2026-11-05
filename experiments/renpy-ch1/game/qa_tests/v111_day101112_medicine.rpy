# 12일 서리가 첫 발화를 하기 전에 실제 현장에 도착했는지 두 경로에서 검사한다.
# 준비는 기존 상태 함수만 쓰고, 이후 실제 의료진 도착 라벨을 진행한다.
init python:
    def qa_d101112_medical(route):
        r13_v111_set("day",12)
        r13_v111_set("route12",route)
        r13_v111_set("DARAM_DETAINED",False)
        r13_v111_set("location:daram","school")
        r13_v111_set("location:resident_seori","clinic")
        r13_v111_set("location:resident_bori","clinic")
        r13_v111_set("busy:resident_bori","medical_call")
        r13_v111_set("medical_called",True)
        r13_v111_set("soup_fragment_observed",True)
        r13_edit(location="school",period=2)
        r13_v111_scene("MS14_D12_S04")
        r13_v111_arrive(["daram","nabi","resident_teacher"])

testcase v111_d101112_medical_late:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_d101112_medical,"late_exposure")
    run Jump("r13_v111_medical_arrival12")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D12_S04_L0044") timeout 60
    assert eval (room13["location"]=="school" and r13_packet[0]=="resident_seori")
    assert eval (qa_nw_seen("보리가 서리와 함께 들어온다"))
    assert eval (all(r13_v111_value("location:"+p)=="school" and r13_v111_actor_ready(p) for p in ["resident_seori","resident_bori"]))
    assert eval (r13_v111_value("busy:resident_bori") is False)
    assert eval (r13_v111_value("route12")=="late_exposure")
    screenshot "d101112-doctor-late.png"

testcase v111_d101112_medical_premeal:
    pause 1.0
    click "처음부터"
    click pos (900,600) until "편지를 외투 안에" timeout 60
    click pos (900,600) until screen "r13_hub" timeout 90
    run Function(qa_d101112_medical,"premeal_stopped")
    run Jump("r13_v111_medical_arrival12")
    click pos (900,600) until eval (r13_packet and r13_packet[2].get("line_id")=="MS14_D12_S04_L0044") timeout 60
    assert eval (room13["location"]=="school" and r13_packet[0]=="resident_seori")
    assert eval (qa_nw_seen("보리가 서리와 함께 들어온다"))
    assert eval (all(r13_v111_value("location:"+p)=="school" and r13_v111_actor_ready(p) for p in ["resident_seori","resident_bori"]))
    assert eval (r13_v111_value("busy:resident_bori") is False)
    assert eval (qa_nw_seen("먹은 아이는 있어요") and qa_nw_seen("작은 냄비에서는 아직 한 그릇도 안 펐어요"))
    assert eval (r13_v111_value("route12")=="premeal_stopped")
    screenshot "d101112-doctor-premeal.png"
