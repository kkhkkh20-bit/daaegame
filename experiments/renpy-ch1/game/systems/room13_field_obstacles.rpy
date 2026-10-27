# 2026-10-27 외부 리뷰(0.20.71) R01: 입구 규칙 게시판 클릭이 까로 이름표와 울타리 천 hitbox 에 가로막혔다.
# 두 원인을 여기서 푼다. 호출하는 쪽(room13_interaction.rpy, room13_v111_later_bindings.rpy)은 대화 연결표가
# 줄 번호를 들고 있어 줄 수를 늘릴 수 없으므로 도우미만 이 파일에 둔다.
init 60 python:
    def r13_gate_wide_rect(rect):
        """1920x720 입구 그림에서 잰 사각형을 넓은 입구(systems/room13_wide_gate.rpy)의 좌표로 옮긴다.
        넓은 입구는 배치표의 objects 만 옮기므로, 코드에서 더한 물건(울타리 천·양동이)은 따로 옮겨야 한다.
        넓은 그림이 없으면 wide_shift 가 없어 그대로다."""
        dx,dy=R13_WORLD_LAYOUTS.get("gate",{}).get("wide_shift",[0,0])
        return [rect[0]+dx,rect[1]+dy]+list(rect[2:])

    def r13_nameplate_obstacles():
        """이름표는 물건 버튼 위에 얹히므로, 지금 장소의 보이는 물건 사각형과 배치표의 critical 사각형을
        이름표 자리 점수(r13_actor_nameplates)의 벌점 대상으로 돌려준다. 얼굴보다 가벼운 벌점이다."""
        location=(store.room13 or {}).get("location")
        rects=[tuple(spec["rect"]) for spec in ROOM13["objects"].get(location,{}).values() if r13_object_visible(spec)]
        for rect in r13_layout(location).get("critical",[]):
            if tuple(rect) not in rects:rects.append(tuple(rect))
        return rects
