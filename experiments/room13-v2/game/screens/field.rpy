# 조사 화면: 지도·기록·생각은 위에, 장면 아래는 비운다. 인물이 기본이고 배경 물건은 직접 누른다(돋보기 표식 없음).
# 넓은 장소는 좌우 화살표로 본다. 인물 도트는 1칸=1px(그림 그대로 크기).

screen v2_field():
    default goal_open = False
    $ data = v2_field_data()
    $ wait = v2_input_wait()

    # 배경 물건: 보이지 않는 단추. 손을 올리면 살짝 밝아진다.
    for key, x, y, w, h, name in data["objects"]:
        button:
            xpos x ypos y xysize (w, h)
            background None
            hover_background Solid("#fff6e633")
            action Return(("object", key))
            alt name

    for who, x, y in data["people"]:
        imagebutton:
            idle "assets/field-dot-v2/%s/neutral.webp" % who
            hover Transform("assets/field-dot-v2/%s/neutral.webp" % who, matrixcolor=BrightnessMatrix(0.08))
            xanchor 0.5 yanchor 1.0 xpos x ypos y
            action Return(("person", who))
            alt V2_PEOPLE[who]["name"]
        frame:
            xanchor 0.5 xpos x yanchor 1.0 ypos y - 222
            background v2_frame("ui-b-field/b_panel_small.png", 10)
            padding (10, 2)
            text V2_PEOPLE[who]["name"] size v2_type("small")

    # 좌우 카메라
    if data["cam"] > 0:
        button:
            xpos 18 yalign 0.42 xysize (54, 50)
            background Solid(V2_COLOR["red"])
            hover_background Solid(V2_COLOR["accent"])
            action Function(v2_pan, -640)
            alt "왼쪽 보기"
            text "←" xalign 0.5 yalign 0.5 color V2_COLOR["inverse"] size v2_type("display")
    if data["cam"] < data["width"] - 1280:
        button:
            xpos 1208 yalign 0.42 xysize (54, 50)
            background Solid(V2_COLOR["red"])
            hover_background Solid(V2_COLOR["accent"])
            action Function(v2_pan, 640)
            alt "오른쪽 보기"
            text "→" xalign 0.5 yalign 0.5 color V2_COLOR["inverse"] size v2_type("display")

    # 위 단추 셋: 지도·기록·생각
    hbox:
        xpos 28 ypos 88 spacing 18
        button:
            style "v2_button" xysize (134, 54)
            action Show("v2_map")
            hbox:
                spacing 6 xalign 0.5 yalign 0.5
                add Transform("assets/ui-b-field/b_icon_map.png", zoom=0.6)
                text "지도" size v2_type("body") yalign 0.5
        button:
            style "v2_button" xysize (134, 54)
            action Show("v2_records")
            hbox:
                spacing 6 xalign 0.5 yalign 0.5
                add Transform("assets/ui-b-field/b_icon_book.png", zoom=0.6)
                text "기록" size v2_type("body") yalign 0.5
        button:
            style "v2_button" xysize (150, 54)
            action [ToggleScreenVariable("goal_open"), SetVariable("v2_goal_seen", data["goal"])]
            hbox:
                spacing 6 xalign 0.5 yalign 0.5
                add Transform("assets/ui-b-field/b_icon_acorn.png", zoom=0.6)
                text ("새 생각" if data["goal"] != v2_goal_seen else "생각") size v2_type("body") yalign 0.5
    button:
        style "v2_button" xpos 1188 ypos 22 xysize (64, 66)
        action [FileTakeScreenshot(), Show("v2_settings")]
        alt "설정"
        add Transform("assets/ui-b-field/b_icon_more.png", zoom=0.6) xalign 0.5 yalign 0.5

    if goal_open:
        frame:
            xpos 28 ypos 156 xsize 520
            background v2_frame("ui-b-field/b_panel_small.png", 16)
            padding (22, 14)
            vbox:
                spacing 6
                hbox:
                    xfill True
                    text "아빠의 생각" size v2_type("small") color V2_COLOR["accent"]
                    textbutton "접기" style "v2_button" xalign 1.0 action SetScreenVariable("goal_open", False) text_size v2_type("small") padding (12, 2)
                text data["goal"] size v2_type("body")

    # 대사를 넘긴 직후 0.6초는 이 화면이 누름을 받지 않는다(같은 손의 연타가 다른 대화를 열지 않게).
    if wait > 0:
        button:
            xysize (1280, 720) background None action NullAction()
        timer wait action Function(renpy.restart_interaction)
