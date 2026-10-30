# 지도: 마을(납품 B 지도 그림)과 여관 안. 갈 수 있는 곳은 지금 장소와 이 대기의 이동 선택지 장소뿐.
# 이동 차례면 목적지를 골라 둔 채 연다.

screen v2_map():
    modal True
    zorder 50
    $ places = v2_map_places()
    $ travel = (V2_GATES.get(v2_gate) or {}).get("travel")
    default pick = travel or next((p for p in places if p != v2_loc), v2_loc)
    default tab = ("inside" if (pick in V2_LAYOUT["map"]["inside"] and v2_loc in V2_LAYOUT["map"]["inside"]) else "village")
    add Solid("#00000088")
    add "assets/map-village-b/notebook_frame_1280x720.png"
    if tab == "village":
        add "assets/map-village-b/map_background_1136x570.png" xpos 88 ypos 58
        for key, (x, y) in V2_LAYOUT["map"]["village"].items():
            $ name = V2_PLACES.get(key, {}).get("name", key)
            $ ok = key in places or (key == "inn" and any(p in V2_LAYOUT["map"]["inside"] for p in places))
            $ here = key == v2_loc or (key == "inn" and v2_loc in V2_LAYOUT["map"]["inside"])
            if 130 < y < 620:
                button:
                    xanchor 0.5 yanchor 0.5 xpos x ypos y
                    style "v2_button" padding (12, 2)
                    selected pick == key or (key == "inn" and pick in V2_LAYOUT["map"]["inside"])
                    action (SetScreenVariable("pick", key if key != "inn" else ("inn" if "inn" in places else pick)) if ok else Notify(v2_map_locked_text(key)))
                    alt name
                    hbox:
                        spacing 4
                        if here:
                            add Transform("assets/map-status/current_location.png", zoom=0.3) yalign 0.5
                        elif not ok:
                            add Transform("assets/map-status/locked.png", zoom=0.3) yalign 0.5
                        text name size v2_type("small") yalign 0.5
    else:
        vbox:
            xpos 200 ypos 160 spacing 18
            text "여관 안" size v2_type("subtitle") color V2_COLOR["accent"]
            for key in V2_LAYOUT["map"]["inside"]:
                $ ok = key in places
                textbutton (("● " if key == v2_loc else "") + V2_PLACES[key]["name"]) style "v2_button" xsize 520 ysize 70:
                    selected pick == key
                    action (SetScreenVariable("pick", key) if ok else Notify(v2_map_locked_text(key)))
                    text_size v2_type("emphasis")
    frame:
        xpos 88 ypos 58 xysize (1136, 64)
        background Solid("#f7ecd8")
        text "다람탐정 · 마을 지도" xalign 0.5 yalign 0.5 size v2_type("title")
        text "현재 · " + v2_place_name() xalign 0.97 yalign 0.5 size v2_type("small") color V2_COLOR["muted"]
    frame:
        xpos 88 ypos 628 xysize (1136, 70)
        background Solid("#f7ecd8")
    hbox:
        xpos 100 ypos 633 spacing 14
        frame:
            xysize (260, 60)
            background v2_frame("ui-b-options/b_opt_choice.png", 18)
            text "선택: " + v2_place_name(pick) size v2_type("small") xalign 0.5 yalign 0.5
        textbutton "마을" style "v2_button" xysize (110, 60) action SetScreenVariable("tab", "village") selected tab == "village" text_size v2_type("body")
        textbutton "여관 안" style "v2_button" xysize (130, 60) action SetScreenVariable("tab", "inside") selected tab == "inside" text_size v2_type("body")
        null width 120
        textbutton "이곳으로 이동" style "v2_primary" xysize (210, 60) action [Hide("v2_map"), Return(("map", pick))] sensitive (pick in places and pick != v2_loc) text_size v2_type("body")
        textbutton "현장으로" style "v2_button" xysize (150, 60) action Hide("v2_map") text_size v2_type("body")
