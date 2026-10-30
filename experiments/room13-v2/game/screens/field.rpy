# 조사 화면: 지도·기록·생각은 위에, 장면 아래는 비운다. 인물이 기본이고 배경 물건은 직접 누른다(돋보기 표식 없음).
# 넓은 장소는 좌우 화살표로 본다. 인물 도트는 1칸=1px(그림 그대로 크기, 장소를 줄여 그려도 인물은 줄이지 않는다).

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

    # 현장 인물: 도트 한 칸 = 화면 1px. 이름표는 지금 판처럼 머리 위 종이 꼬리표(누르면 그 사람과 이야기).
    for pp in data["people"]:
        imagebutton:
            idle pp["img"]
            hover Transform(pp["img"], matrixcolor=BrightnessMatrix(0.08))
            focus_mask True
            xpos pp["x"] ypos pp["y"]
            action Return(("person", pp["who"]))
            alt V2_PEOPLE[pp["who"]]["name"]
    for pp in data["people"]:
        textbutton V2_PEOPLE[pp["who"]]["name"]:
            area pp["tag"]
            padding (7, 2)
            background Frame("assets/ui-field-stickers/label_basic.png", 12, 12)
            hover_background Frame("assets/ui-field-stickers/label_hover.png", 12, 12)
            text_size v2_type("tag") text_color "#4b3021" text_hover_color "#9c3c2b"
            text_xalign 0.5 text_yalign 0.5
            action Return(("person", pp["who"]))

    # 좌우 카메라: 지금 판과 같은 종이 화살표(한 번에 그 쪽 끝까지).
    if data["cam"] > 0:
        imagebutton:
            xpos 12 ypos 240
            idle "assets/ui-field-stickers/arrow_left_basic.png"
            hover "assets/ui-field-stickers/arrow_left_hover.png"
            action Function(v2_pan, -1)
            alt "왼쪽 보기"
    if data["cam"] < data["cam_range"]:
        imagebutton:
            xpos 1196 ypos 240
            idle "assets/ui-field-stickers/arrow_right_basic.png"
            hover "assets/ui-field-stickers/arrow_right_hover.png"
            action Function(v2_pan, 1)
            alt "오른쪽 보기"

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
