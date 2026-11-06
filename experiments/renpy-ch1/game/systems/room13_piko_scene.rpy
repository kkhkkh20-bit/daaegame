# 기존 수첩·버튼·현장 그림을 쓰는 피코 곁의 선택 화면.
# 2026-11-06 실제 시안 승인. 자료·시간·정답은 이 화면에서 바꾸지 않는다.
default r13_piko_scene_near = True

init 320 python:
    R13_PIKO_SCENE_CHOICES = (
        dict(key="posture",caption="초롱 씨에게 발견 당시 모습을 묻는다"),
        dict(key="portrait",caption="받은 초상을 다시 본다"),
        dict(key="daram",caption="다람에게 말을 건넨다"),
    )
    def r13_piko_scene_available():
        return (store.room13.get("day")==3 and store.room13.get("location")=="square"
                and r13_v111_value("piko_alive") is False and r13_v111_owned("E09")
                and not r13_v111_value("lamp_bound2"))

    def r13_piko_scene_lines(rows,portrait=False):
        rows=list(rows)
        if rows:
            packet=rows[0]
            # 그림을 접은 선택은 질문 중에도 유지한다. 컷은 대사 묶음이 끝나면 기존 방식으로 내려간다.
            options=dict(packet[2],cut="piko-death3" if store.r13_piko_scene_near and not portrait else None)
            rows[0]=(packet[0],packet[1],options)
        return rows

screen r13_piko_scene():
    modal True
    zorder 65
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    $ touch=r13_touch_ui()
    use r13_notebook_shell("피코 곁에서",stamp="3일 아침 · 광장")
    if r13_piko_scene_near:
        add Transform(r13_ep_cut_art("piko-death3"),xysize=(620,349)) xpos 132 ypos (154 if touch else 174)
        text "발견했을 때의 모습" xpos 144 ypos (506 if touch else 538) size r13_type("small") color r13_type_color("muted") font R13_UI_BOLD_FONT
    else:
        vbox:
            xpos 154 ypos 240 xsize 580 spacing 22
            text "초롱 씨의 설명을 듣는다." size r13_type("subtitle") color r13_type_color("ink") font R13_UI_BOLD_FONT
            text "나는 다람의 손을 잡고 선다." size r13_type("body") color r13_type_color("muted") font R13_UI_BOLD_FONT
    vbox:
        xpos 776 ypos 170 spacing 16
        for entry in R13_PIKO_SCENE_CHOICES:
            $ key,caption=entry["key"],entry["caption"]
            button:
                id ("r13_piko_"+key)
                xysize (430,104) padding (24,10)
                background r13_notebook_button_surface()
                hover_background r13_notebook_button_surface(False,True)
                action Return(key) sensitive ready
                text caption xsize 382 yalign .5 size r13_type("emphasis") color r13_type_color("muted" if r13_v111_value("piko_scene_read:"+key) else "ink") font R13_UI_BOLD_FONT
        button:
            id "r13_piko_leave"
            xysize (430,88) padding (24,10)
            background r13_notebook_button_surface(True)
            hover_background r13_notebook_button_surface(True,True)
            action Return("leave") sensitive ready
            text "등 쪽으로 간다" yalign .5 size r13_type("emphasis") color r13_type_color("inverse") font R13_UI_BOLD_FONT
    button:
        id "r13_piko_distance"
        pos (144,548 if touch else 578) xysize (596,88 if touch else 58) padding (18,8)
        background r13_notebook_button_surface()
        hover_background r13_notebook_button_surface(False,True)
        action Return("distance") sensitive ready
        text ("그림을 접고 설명으로 듣는다" if r13_piko_scene_near else "피코가 있는 쪽을 다시 본다") yalign .5 size r13_type("body") color r13_type_color("ink") font R13_UI_BOLD_FONT
    if ready:
        key "game_menu" action Return("leave")

