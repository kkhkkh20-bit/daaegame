# 납품 상태 스티커: 기존 공개된 지도 행에만 표시한다. 이동·발견·저장 데이터는 변경하지 않는다.
init 66 python:
    def r13_map_status_kinds(key, state, selected):
        current = key == store.room13.get("location")
        if current:
            return ("current_location",)
        if state != "open":
            return ("locked",)
        return ("map_selected",) if key == selected else ()

screen r13_map_status_badges(key, state, selected, label_rect):
    $ bx,by,bw,bh=label_rect
    $ badges=r13_map_status_kinds(key,state,selected)
    for badge in badges:
        # 48px로 통일해 축소 지도에서도 읽히도록 하며, 원본 비율을 유지한다.
        add Transform("assets/map-status/"+badge+".png",zoom=.5) xpos (int(bx)-24) ypos (int(by+bh/2)-28)
