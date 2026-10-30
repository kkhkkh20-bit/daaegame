# 고르기: 오른쪽에 번호 붙은 종이 카드. 선택지가 하나면 엔진이 이 화면을 띄우지 않는다.

screen v2_choice():
    modal True
    $ items = v2_menu_items(v2_current()[1])
    vbox:
        xpos 600 yalign 0.42 spacing 14
        for i, (label, target) in enumerate(items):
            button:
                xsize 620 ysize 64
                background v2_frame("ui-b-options/b_opt_choice.png", 18)
                hover_background v2_frame("ui-b-options/b_opt_choice_hover.png", 18)
                action Return(i)
                alt label
                hbox:
                    yalign 0.5 xpos 16 spacing 22
                    frame:
                        xysize (40, 40) yalign 0.5
                        background Solid("#5b3a26")
                        text "%d" % (i + 1) xalign 0.5 yalign 0.5 color V2_COLOR["inverse"] size v2_type("body")
                    text label size v2_type("emphasis") yalign 0.5
