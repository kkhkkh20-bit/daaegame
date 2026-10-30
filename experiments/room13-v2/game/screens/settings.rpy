# 설정: 읽기·소리·화면. 저장·불러오기는 설정창 아래 줄(소유자 결정).

screen v2_settings():
    modal True
    zorder 80
    default tab = "read"
    add Solid("#00000088")
    add "assets/ui-b-options/b_opt_panel.png" xalign 0.5 yalign 0.5 zoom 0.98
    add Transform("assets/ui-b-options/b_opt_title_tape.png", zoom=0.6) xpos 92 ypos 36
    text "설정" xpos 118 ypos 46 size v2_type("title")
    imagebutton:
        xpos 1110 ypos 42 idle Transform("assets/ui-b-options/b_opt_close.png", zoom=0.6)
        action Hide("v2_settings") alt "닫기"
    vbox:
        xpos 96 ypos 140 spacing 18
        for key, label in (("read", "읽기"), ("sound", "소리"), ("screen", "화면")):
            textbutton label style "v2_button" xysize (170, 64) action SetScreenVariable("tab", key) selected tab == key text_size v2_type("subtitle")
    vbox:
        xpos 310 ypos 120 spacing 20 xsize 860
        text "변경한 설정은 바로 적용됩니다." size v2_type("small") color V2_COLOR["muted"]
        if tab == "read":
            hbox:
                spacing 14
                text "글자 크기" size v2_type("subtitle") xsize 230 yalign 0.5
                for key, label in (("small", "작게"), ("normal", "보통"), ("large", "크게")):
                    textbutton label style "v2_button" xysize (150, 62) action SetField(persistent, "v2_text_size", key) selected persistent.v2_text_size == key text_size v2_type("body")
            hbox:
                spacing 14
                text "대사 표시 속도" size v2_type("subtitle") xsize 230 yalign 0.5
                for cps, label in ((30, "느리게"), (55, "보통"), (90, "빠르게"), (0, "즉시")):
                    textbutton label style "v2_button" xysize (130, 62) action Preference("text speed", cps) selected preferences.text_cps == cps text_size v2_type("body")
            hbox:
                spacing 14
                text "자동 넘김" size v2_type("subtitle") xsize 230 yalign 0.5
                textbutton "수동" style "v2_button" xysize (130, 62) action Preference("auto-forward", "disable") selected not preferences.afm_enable text_size v2_type("body")
                for t, label in ((10, "짧게"), (20, "보통"), (30, "길게")):
                    textbutton label style "v2_button" xysize (130, 62) action [Preference("auto-forward", "enable"), Preference("auto-forward time", t)] selected (preferences.afm_enable and preferences.afm_time == t) text_size v2_type("body")
        elif tab == "sound":
            for label, mixer in (("음악", "music"), ("효과음·환경음", "sfx")):
                hbox:
                    spacing 14
                    text label size v2_type("subtitle") xsize 230 yalign 0.5
                    bar value Preference(mixer + " volume") xsize 420 ysize 30 yalign 0.5
        else:
            hbox:
                spacing 14
                text "화면" size v2_type("subtitle") xsize 230 yalign 0.5
                textbutton "창 모드" style "v2_button" xysize (150, 62) action Preference("display", "window") text_size v2_type("body")
                textbutton "전체 화면" style "v2_button" xysize (170, 62) action Preference("display", "fullscreen") text_size v2_type("body")
    add Solid("#c9b48f") xpos 96 ypos 540 xysize (1080, 2)
    hbox:
        xpos 96 ypos 566 spacing 16
        if not main_menu:
            textbutton "메인화면" style "v2_button" xysize (170, 64) action MainMenu(confirm=False) text_size v2_type("body")
            textbutton "저장 · 불러오기" style "v2_button" xysize (240, 64) action Show("v2_files", mode="save") text_size v2_type("body")
        null width 300
        textbutton "닫기" style "v2_primary" xysize (170, 64) action Hide("v2_settings") text_size v2_type("body")

# 저장·불러오기: 6칸, 쪽 셋. 메인 메뉴에서는 불러오기만.
screen v2_files(mode="save"):
    modal True
    zorder 90
    default page = 1
    default cur = mode
    add Solid("#000000aa")
    frame:
        xalign 0.5 yalign 0.5 xysize (1160, 640)
        background v2_frame("ui-b-options/b_opt_choice.png", 18)
        padding (30, 24)
        vbox:
            spacing 18
            hbox:
                spacing 16
                text ("저장" if cur == "save" else "불러오기") size v2_type("display") color V2_COLOR["muted"]
                for n in (1, 2, 3):
                    textbutton "%d쪽" % n style "v2_button" action SetScreenVariable("page", n) selected page == n text_size v2_type("small") padding (12, 2)
                if not main_menu:
                    textbutton ("불러오기로 ›" if cur == "save" else "저장으로 ›") style "v2_button" action SetScreenVariable("cur", "load" if cur == "save" else "save") text_size v2_type("small") padding (12, 2)
            grid 2 3:
                spacing 18
                for i in range(1, 7):
                    $ slot = "%d-%d" % (page, i)
                    button:
                        style "v2_button" xysize (530, 130)
                        action (FileSave(slot, confirm=False, page=None) if cur == "save" else FileLoad(slot, confirm=False, page=None))
                        alt "%d쪽 %d번" % (page, i)
                        hbox:
                            spacing 16 yalign 0.5
                            add FileScreenshot(slot, empty=Null()) xysize (160, 90)
                            vbox:
                                yalign 0.5
                                text "%d쪽 %d번" % (page, i) size v2_type("body")
                                text (FileTime(slot, format="%m/%d %H:%M", empty="비어 있음")) size v2_type("small") color V2_COLOR["muted"]
            textbutton "돌아가기" style "v2_button" action Hide("v2_files") text_size v2_type("body")
