style default:
    font "assets/Galmuri11.ttf"
    size 27
    color "#f3e7ce"
style button:
    background Solid("#30261fea")
    hover_background Solid("#785437")
    insensitive_background Solid("#282421")
    padding (20, 14)
style button_text:
    color "#f3e7ce"
    hover_color "#ffdc91"
    insensitive_color "#887f72"
    size 25
style frame:
    background Solid("#201b18ef")
    padding (28, 24)
style say_dialogue:
    size 29
    line_spacing 10
style say_label:
    size 27
    bold True

screen main_menu():
    tag menu
    add "bg approach"
    add Solid("#120e0a88")
    frame:
        xalign 0.08
        yalign 0.48
        xsize 620
        vbox:
            spacing 22
            text "다람탐정" size 62 color "#ffdc91"
            text "열세 번째 침대" size 34
            text "Ren’Py 웹 플레이 테스트" size 23 color "#c6b699"
            textbutton "처음부터" action Start() xsize 480
            textbutton "이어하기" action ShowMenu("load") xsize 480
            text "약 5분 · 조사 / 증거 / 회의\n기존 1장의 일부를 사용한 기술 시제품" size 21 color "#c6b699"

screen say(who, what):
    window:
        id "window"
        xalign 0.5
        yalign 1.0
        xsize 1200
        ysize 175
        background Solid("#211a16f2")
        padding (35, 20)
        vbox:
            spacing 12
            if who:
                text who id "who" color "#ffcc86"
            text what id "what" xsize 1110
    text "▼" xalign 0.94 yalign 0.97 color "#d8b568" size 22

screen choice(items):
    modal True
    frame:
        xalign 0.5
        yalign 0.5
        xsize 900
        vbox:
            spacing 15
            for item in items:
                textbutton item.caption action item.action xfill True

screen hud():
    zorder 20
    frame:
        xpos 28
        ypos 20
        padding (18, 12)
        vbox:
            spacing 4
            text place size 24 color "#f8d994"
            text clock_text size 20 color "#c6b699"
    hbox:
        xpos 994
        ypos 20
        spacing 10
        imagebutton:
            idle Transform("assets/evidence.png", size=(56, 56))
            hover Transform("assets/evidence.png", size=(56, 56), alpha=0.7)
            action Show("evidence_book")
            tooltip "증거"
        imagebutton:
            idle Transform("assets/save.png", size=(56, 56))
            hover Transform("assets/save.png", size=(56, 56), alpha=0.7)
            action ShowMenu("save")
            tooltip "저장"
        imagebutton:
            idle Transform("assets/menu.png", size=(56, 56))
            hover Transform("assets/menu.png", size=(56, 56), alpha=0.7)
            action ShowMenu("pause_menu")
            tooltip "메뉴"
    $ tip = GetTooltip()
    if tip:
        text tip xalign 0.92 ypos 84 size 20

screen investigate():
    # This modal interaction only exists after the last introductory line.
    modal True
    default input_ready = False
    timer 0.35 action SetScreenVariable("input_ready", True)
    add Transform("assets/pouch-world.png", size=(70, 75)) xpos 870 ypos 265
    add Transform("assets/flour-world.png", size=(70, 58)) xpos 580 ypos 332
    button:
        xpos 680 ypos 215 xsize 310 ysize 115
        background None
        hover_background Solid("#e4c58422")
        sensitive input_ready
        action Return("pouch")
        tooltip "베개 살펴보기"
    button:
        xpos 565 ypos 485 xsize 330 ysize 100
        background None
        hover_background Solid("#e4c58422")
        sensitive input_ready
        action Return("fur")
        tooltip "침대 아래 살펴보기"
    button:
        xpos 560 ypos 330 xsize 145 ysize 100
        background None
        hover_background Solid("#e4c58422")
        sensitive input_ready
        action Return("flour")
        tooltip "이불의 손자국"
    frame:
        xpos 28 ypos 592 xsize 690
        vbox:
            spacing 8
            text "방을 살펴보자" color "#ffdc91"
            text "베개 · 이불 · 침대 아래" size 23
    textbutton "회의로":
        xpos 1010 ypos 610 xsize 220
        sensitive input_ready and "pouch" in inventory and "fur" in inventory
        action Return("meeting")
    $ tip = GetTooltip()
    if tip:
        frame:
            xalign 0.5 ypos 520
            text tip size 23

screen evidence_book():
    modal True
    zorder 60
    add Solid("#100c09bb")
    frame:
        xpos 120 ypos 120 xsize 1040 ysize 500
        vbox:
            spacing 20
            text "증거 수첩" size 32 color "#ffdc91"
            if not inventory:
                text "아직 모은 증거가 없다." color "#c6b699"
            for key in inventory:
                hbox:
                    spacing 22
                    add EVIDENCE[key][2] at thumbnail
                    vbox:
                        spacing 10
                        text EVIDENCE[key][0] color "#ffdc91"
                        text EVIDENCE[key][1] size 22 xsize 735
            textbutton "닫기" action Hide("evidence_book")

screen testimony():
    modal True
    frame:
        xpos 30 ypos 140 xsize 655
        vbox:
            spacing 14
            text "세련의 발언" size 23 color "#d4b07e"
            text "제 주머니하고는 아무 관계도 없어요." size 30 xsize 590
            if stage == "comparison":
                text "두 흔적을 비교할 다른 증거는?" size 23 color "#ffdc91"
            else:
                text "어떤 증거로 확인할까?" size 23 color "#ffdc91"
            textbutton "되묻기" action Return("press")
    hbox:
        xpos 40 ypos 525 spacing 18
        for key in inventory:
            button:
                xsize 385 ysize 145
                action Return(key)
                vbox:
                    spacing 12
                    add EVIDENCE[key][2] at thumbnail xalign 0.5
                    text EVIDENCE[key][0] size 22 xalign 0.5

screen pause_menu():
    tag menu
    modal True
    zorder 50
    style_prefix "trial"
    add Solid("#110d0aec")
    frame:
        xalign 0.5 yalign 0.5 xsize 650
        vbox:
            spacing 18
            text "잠깐 쉬어가기" size 36 color "#ffdc91"
            textbutton "돌아가기" action Return() xfill True
            textbutton "저장" action ShowMenu("save") xfill True
            textbutton "불러오기" action ShowMenu("load") xfill True
            textbutton "음악 켜기 / 끄기" action Preference("music mute", "toggle") xfill True
            textbutton "처음 화면으로" action MainMenu(confirm=False) xfill True

screen save():
    tag menu
    zorder 50
    use file_slots("저장", True)

screen load():
    tag menu
    zorder 50
    use file_slots("불러오기", False)

screen file_slots(title, saving):
    modal True
    style_prefix "trial"
    add Solid("#110d0aec")
    frame:
        xalign 0.5 yalign 0.5 xsize 930
        background Solid("#201b18f5")
        vbox:
            spacing 18
            text title size 36 color "#ffdc91"
            for slot in (1, 2, 3):
                hbox:
                    spacing 20
                    add FileScreenshot(slot) xsize 192 ysize 108
                    button:
                        xsize 620 ysize 108
                        action (FileSave(slot, confirm=False) if saving else FileLoad(slot, confirm=False))
                        vbox:
                            spacing 8
                            text "슬롯 [slot]" color "#ffdc91"
                            text FileTime(slot, format="%Y-%m-%d %H:%M", empty="비어 있음") size 23
            textbutton "돌아가기" action Return()

screen trial_complete():
    modal True
    zorder 50
    add Solid("#120e0ad9")
    frame:
        xalign 0.5 yalign 0.5 xsize 930
        vbox:
            spacing 22
            text "첫 모순을 찾았다" size 42 color "#ffdc91"
            text "주머니와 솜솜의 접촉은 확인했다.\n누가 옮겼는지, 돈이 어디로 갔는지는 아직 남아 있다." size 28
            text "이번 테스트는 여기까지입니다.\n증거를 제시하는 순서를 바꿔도 같은 추론으로 이어집니다." size 23 color "#c6b699"
            textbutton "다시 플레이" action Start()
            textbutton "처음 화면으로" action MainMenu(confirm=False)

screen notify(message):
    zorder 100
    frame:
        xalign 0.5 ypos 100
        text message size 23
    timer 2.5 action Hide("notify")

screen confirm(message, yes_action, no_action):
    modal True
    zorder 100
    add Solid("#000000bb")
    frame:
        xalign 0.5 yalign 0.5 xsize 900
        vbox:
            spacing 20
            text message
            hbox:
                spacing 30
                textbutton "예" action yes_action
                textbutton "아니요" action no_action

style trial_frame is frame
style trial_button is button
style trial_button_text is button_text
