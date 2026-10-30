# 대화창: B 대사판·이름 리본·표정 얼굴(얼굴은 대화 그림이 표정을 바꾼다). 건너뛰기 확인창 없음.
# 건너뛰기는 다음 고르는 화면까지 간다(엔진이 고르는 화면 앞에서 멈춘다).
# 검은 카드(오프닝 세 줄)와 회의 무대(머리띠)도 이 화면 하나가 그린다.

screen say(who, what):
    if v2_line == "card":
        text what id "what":
            xalign 0.5 yalign 0.45 text_align 0.5
            color "#f3eadb" size v2_type("subtitle")
        hbox:
            xpos 860 ypos 668 spacing 110
            textbutton "건너뛰기" action Skip(fast=True, confirm=False) text_color "#f3eadb" text_size v2_type("body") text_hover_color "#ffffff"
            textbutton "더보기" action [FileTakeScreenshot(), Show("v2_settings")] text_color "#f3eadb" text_size v2_type("body") text_hover_color "#ffffff"
    else:
        if v2_stage:
            frame:
                xpos 30 ypos 20 xsize 900
                background v2_frame("ui-b-field/b_panel_small.png", 18)
                padding (24, 12)
                vbox:
                    spacing 2
                    text v2_stage[0] size v2_type("small") color V2_COLOR["muted"]
                    text v2_stage[1] size v2_type("emphasis")
        window id "window":
            xpos 40 ypos 548 xsize 1200 ysize 166
            background "assets/ui-b-dialogue/b_panel_dialogue.png"
            text what id "what":
                xpos 82 ypos 30 xsize 1010
                size v2_type("display") line_spacing 6
                color (V2_COLOR["ink"] if v2_line != "doc" else V2_COLOR["navy"])
        if who:
            frame:
                xpos 130 ypos 512 xysize (150, 46)
                background v2_ribbon()
                text who xalign 0.4 yalign 0.5 color V2_COLOR["inverse"] size v2_type("title")
        hbox:
            xpos 818 ypos 664 spacing 16
            button:
                xysize (186, 44) background v2_ribbon()
                action Skip(fast=True, confirm=False)
                text "건너뛰기" xalign 0.45 yalign 0.5 color V2_COLOR["inverse"] size v2_type("body")
            button:
                xysize (186, 44) background v2_ribbon()
                action [FileTakeScreenshot(), Show("v2_settings")]
                text "더보기" xalign 0.45 yalign 0.5 color V2_COLOR["inverse"] size v2_type("body")

# 시간·장소 머리(조사 화면과 대화 둘 다 위에 남는다). 마차·검은 화면에서는 숨긴다.
screen v2_hud():
    zorder 5
    if v2_loc not in ("black", "carriage") and not main_menu:
        # 회의 무대 머리띠가 떠 있으면 장소 이름표는 머리띠가 대신한다.
        frame:
            xpos 28 ypos 22 ysize 48
            at v2_hide_if(bool(v2_stage))
            background v2_frame("ui-b-field/b_panel_small.png", 16)
            padding (12, 4, 18, 4)
            hbox:
                spacing 6 yalign 0.5
                add Transform("assets/ui-b-field/b_icon_pin.png", zoom=0.55) yalign 0.5
                text v2_place_name() size v2_type("title") yalign 0.5
        add Transform("assets/ui-b-field/b_tape_red.png", zoom=0.42, rotate=8) xpos 150 ypos 14 at v2_hide_if(bool(v2_stage))
        frame:
            xpos 944 ypos 22 xysize (230, 66)
            background v2_frame("ui-b-field/b_panel_small.png", 16)
            hbox:
                xpos 12 yalign 0.5 spacing 18
                vbox:
                    text "%02d" % v2_day size v2_type("title")
                    text "일째" size v2_type("small") color V2_COLOR["muted"]
                vbox:
                    text V2_DAY["weekday"] size v2_type("body")
                    text V2_PERIODS[min(v2_period, 2)] size v2_type("small") color V2_COLOR["muted"]

# 자료를 얻으면 오른쪽 위에 잠깐 뜨는 쪽지(지금 판 자료 모서리 카드와 같은 자리).
screen notify(message):
    zorder 100
    frame at v2_notify_fade:
        xalign 1.0 xoffset -40 ypos 110
        background v2_frame("ui-b-field/b_panel_small.png", 16)
        padding (18, 12, 24, 12)
        hbox:
            spacing 12
            add Transform("assets/record.png", fit="contain", xysize=(40, 40)) yalign 0.5
            text message size v2_type("body") yalign 0.5
    timer 2.6 action Hide("notify")

transform v2_hide_if(hidden):
    alpha (0.0 if hidden else 1.0)

transform v2_notify_fade:
    on show:
        alpha 0.0
        linear 0.2 alpha 1.0
    on hide:
        linear 0.3 alpha 0.0
