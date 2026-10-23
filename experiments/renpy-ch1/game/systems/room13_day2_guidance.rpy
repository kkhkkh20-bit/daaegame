# 0.20.15 추가 QA A01/A02: 이미 제시된 일을 찾는 안내. 이동·획득·판정은 실행하지 않는다.
init 353 python:
    R13_DAY2_GUIDANCE={
        "lamp_rope":"아내가 남긴 메모를 초롱에게 확인하자. 먼저 등불의 덮개 지지 끈을 잡아 점검을 돕자.",
        "go_box":"초롱과 깊은 숲의 교환함으로 가 보자. 아내 소식이 남아 있는지 직접 확인하자.",
        "box_inspect":"교환함과 주변을 직접 살펴 아내 소식이 남아 있는지 확인하자.",
        "box_note":"우리가 왔다는 쪽지를 교환함에 직접 넣자.",
        "envelope_show":"우체국에서 서련에게 초대 편지의 봉투를 보여 발신인을 확인하자.",
        "post_menu":"봉투를 돌려받기 전에 서련에게 남은 질문을 확인하자.",
    }
    R13_DAY2_TRAVEL_GUIDANCE={
        ("MS14_D02_S01","gate"):"아내 소식을 찾기 전에 돌아갈 마차가 있는지 입구에서 확인하자.",
        ("MS14_D02_S01","square"):"아내가 남긴 메모를 초롱에게 확인하자. 광장으로 가 보자.",
        ("MS14_D02_S01","forest"):R13_DAY2_GUIDANCE["go_box"],
        ("MS14_D02_S02","post"):"우체국에서 초대 편지의 발신인을 확인하자.",
    }

    def r13_day2_guidance():
        state=getattr(store,"room13",None) or {}
        v=state.get("v111") or {}
        if state.get("day")!=2 or not v:return None
        if v.get("gate")=="travel":
            return R13_DAY2_TRAVEL_GUIDANCE.get((v.get("scene"),v.get("travel_to")))
        return R13_DAY2_GUIDANCE.get(v.get("gate"))

    def r13_day2_idle_guidance(person):
        state=getattr(store,"room13",None) or {}
        v=state.get("v111") or {}
        gate=v.get("gate")
        place="square" if gate in ("lamp_rope","go_box") else "forest"
        if (state.get("day")!=2 or person!="resident_lamplighter" or state.get("location")!=place
                or gate not in ("lamp_rope","go_box","box_inspect","box_note")):
            return None
        if gate=="lamp_rope":
            return [r13_nw_added_line(dict(speaker="초롱",kind="dialogue",expression="flustered",
                text="등불 옆 덮개 지지 끈을 먼저 잡아 주세요. 점검을 마치고 이야기해요."))]
        return [r13_nw_added_line(dict(speaker="아빠",kind="thought",text=R13_DAY2_GUIDANCE[gate]))]

    _r13_day2_object_name=r13_object_name
    def r13_object_name(key):
        state=getattr(store,"room13",None) or {}
        if (key=="lamp" and state.get("day")==2 and state.get("location")=="square"
                and (state.get("v111") or {}).get("gate")=="lamp_rope"):
            return "등불 · 덮개 지지 끈"
        return _r13_day2_object_name(key)
