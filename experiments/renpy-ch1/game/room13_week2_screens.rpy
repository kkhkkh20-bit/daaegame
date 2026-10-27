# The crisis is a field confrontation, not a second formal trial.
screen r13_crisis():
    style_prefix "r13"
    modal True
    zorder 35
    default ready=False
    default preparations_open=False
    timer .15 action SetScreenVariable("ready",True)
    use r13_meeting_stage("F1")
    frame:
        area (24,18,900,66) padding (16,8) background R13PaperFrame()
        add R13AntiqueIcon("meeting_stone",size=30) xpos 0 ypos 8
        vbox:
            xpos 42
            text "제단 앞 회의 · 14일째" size 17 color "#795d40"
            text "연결을 멈춰야 한다" size r13_read_size(23,27) color "#493b30"
    $ preparations=r13_crisis_preparations()
    textbutton ("대피 준비 · %d / %d"%(sum(ok for name,ok in preparations),len(preparations))):
        style "r13_action_button" xpos 942 ypos 18 xsize 314 ysize 64 text_size 21
        action ToggleScreenVariable("preparations_open") sensitive ready
    for index,key in enumerate(("F1","F2","F3","F4")):
        $ proved=key in room13["propositions"]
        $ open_claim=r13_debate_open(key)
        button:
            area (48+(index%2)*598,482+(index//2)*82,586,72) padding (14,9)
            background R13PaperPanel(proved) hover_background R13PaperPanel(True)
            action Return(key) sensitive ready and open_claim
            fixed:
                xsize 554 ysize 54
                text ("{s}"+R13_CLAIMS[key]["assertion"]+"{/s}" if proved else R13_CLAIMS[key]["assertion"]) size r13_read_size(21,25) color ("#82745d" if not open_claim else "#493b30") xsize (432 if not open_claim else 554) yalign .5
                if not open_claim:
                    text ("입증함" if proved else "이번 회의 정리됨" if r13_debate_closed(key) else "반론 자료 부족") xpos 446 xsize 108 size r13_read_size(16,18) color "#795d40" yalign .5
    hbox:
        xpos 48 ypos 650 spacing 16
        textbutton "수첩을 다시 본다" style "r13_action_button" xsize 312 ysize 60 text_size 23 action Show("r13_book") sensitive ready
        textbutton "모은 근거와 해 둔 준비로 움직인다" style "r13_action_button" xsize 620 ysize 60 text_size 23 action Return("finish") sensitive ready
    if preparations_open:
        frame:
            area (838,94,418,370) padding (20,16) background R13PaperFrame()
            vbox:
                spacing 12
                text "함께 움직일 준비" size 24 color "#493b30"
                for name,prepared in preparations:
                    text (name+" · "+("모아 둠" if prepared else "마련하지 못함")) size 20 color ("#3d7058" if prepared else "#795d40")
                if room13["case_state"]=="occurred" and any(r13_debate_open(c) for c in r13_case_available()):
                    textbutton "13호 사건에서 남은 문제" style "r13_action_button" xsize 370 ysize 54 text_size 19 action Return("case") sensitive ready
                if r13_has("E29"):
                    textbutton "가족과 빠져나갈 길" style "r13_action_button" xsize 370 ysize 54 text_size 19 action Return("escape") sensitive ready

screen r13_crisis_proof(claim,heading="제단 앞 · 맞서야 할 주장",can_press=True,need_evidence=False,leave_label="다른 주장부터",chances=None):
    style_prefix "r13"
    modal True
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    $ control_height=88 if r13_touch_ui() else 56
    frame:
        area (50,100,1180,570) padding (48,32,28,24) background R13DiaryPanel()
        fixed:
            hbox:
                xsize 1090
                text heading font R13_UI_TYPE["title"]["font"] size 22 color "#717367"
                if chances:
                    text chances size 22 color "#795d40" xalign 1.0
            text R13_CLAIMS[claim]["assertion"] font R13_UI_TYPE["title"]["font"] ypos 40 size r13_read_size(30,32) color "#765426" xsize 1090
            text ("고른 자료 · %d개"%len(room13["arguments"].get(claim,[]))) ypos 116 size 22
            # 2026-10-27 외부 리뷰: 고르기·확인·제출이 다른 행동임을 첫 제출 성공 전까지만 단계로 보인다.
            if need_evidence and r13_proof_guide_active():
                text r13_proof_guide_steps(len(room13["arguments"].get(claim,[]))) id "r13_proof_steps" xpos 1090 xanchor 1.0 ypos 116 size 22 font R13_UI_BOLD_FONT
            frame:
                area (0,142,1090,190) padding (20,16) background r13_sticker_button()
            viewport:
                xpos 20 ypos 158 xsize 1050 ysize 158 draggable True mousewheel True scrollbars "vertical"
                vscrollbar_unscrollable "hide"
                vbox:
                    spacing 8
                    for key in room13["arguments"].get(claim,[]):
                        hbox:
                            spacing 16
                            text ("· "+ROOM13["evidence"][key]["name"]) size r13_read_size(23,26) xsize 850 yalign .5
                            if need_evidence:
                                use r13_control("빼기",None,Return(("remove",key)),enabled=ready,width=128,height=control_height,label_size=24)
                    if not room13["arguments"].get(claim):
                        vbox:
                            spacing 12
                            text "아직 고른 자료가 없습니다." font R13_UI_BOLD_FONT size 24 color "#493b30"
                            text "아래 ‘자료 고르기’에서 대조할 자료를 골라 주세요." size 22 color "#717367" xmaximum 1000
            text (r13_proof_guide_help(len(room13["arguments"].get(claim,[])),chances) if need_evidence and r13_proof_guide_active() else r13_proof_edit_help(chances)) ypos 350 size (26 if r13_touch_ui() else 22) color "#795d40" xsize 1090
            hbox:
                ypos 414 spacing 16
                use r13_control("자료 고르기",None,Return("present"),enabled=ready,width=258,height=control_height,label_size=24,control_id="r13_proof_pick")
                use r13_control("되묻는다",None,Return("press"),enabled=(ready and can_press),width=258,height=control_height,label_size=24,control_id="r13_proof_hint")
                use r13_control("선택한 근거 제출",None,Return("argue"),enabled=(ready and (bool(room13["arguments"].get(claim)) or not need_evidence)),primary=True,width=258,height=control_height,label_size=24,control_id="r13_proof_submit")
                use r13_control(leave_label,None,Return("leave"),enabled=ready,width=258,height=control_height,label_size=24,control_id="r13_proof_back")

screen r13_rescue_notes():
    style_prefix "r13"
    modal True
    zorder 60
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (165,145,950,475) padding (30,26)
        vbox:
            spacing 20
            text "아이에게 닿을 방법" size 33 color "#765426"
            if room13["scout_revision"]!=room13["convoy_revision"]:
                text "지금 따르고 있는, 끌고 가라는 명령과 지킴 순서를 확인하지 못했다." size 24 xsize 875
            for route in r13_rescue_routes():
                text {"order":"너울과 맞춰 본 명령으로 옮기는 것을 멈출 수 있다.","laundry":"누비와, 물건이 들어오며 지키는 사람이 바뀌는 때에 맞춰 아이를 넘겨받기로 했다.","maintenance":"부리와 점검문을 확인해 두었다."}[route] size 24 xsize 875
            if r13_has("operators_ready") and r13_has("patient_transport"):
                text "장치를 다룰 사람들과 나를 사람들이 있다. 엄마와 함께 사람 쪽 연결을 막을 수 있다." size 24 xsize 875
            elif not r13_rescue_routes():
                text "함께 연결을 막고 아이를 옮길 준비도 갖추지 못했다. 혼자 끌고 가는 걸 막으면 경비를 넘어서기 어렵다." size 24 xsize 875
            textbutton "돌아간다" action Return(False) sensitive ready text_size 25

screen r13_ending_screen(key):
    style_prefix "r13"
    modal True
    zorder 70
    default ready=False
    timer .5 action SetScreenVariable("ready",True)
    add Solid("#111b2266")
    text "이번 여정의 끝" xpos 76 ypos 84 size 23 color "#dfbd7e"
    text R13_ENDINGS[key]["title"] xpos 72 ypos 126 xsize 568 size r13_read_size(47,51) color "#fff0d0" outlines [(2,"#1d262b",0,1)]
    text r13_ending_story_frame(key,3)["caption"] xpos 76 ypos 218 xsize 540 size r13_read_size(24,28) color "#fff0d0" line_spacing 7 outlines [(1,"#1d262b",0,1)]
    textbutton "후일담 다시 보기":
        style "r13_action_button" area (76,584,340,62) text_size 24 action Return("replay") sensitive ready
    textbutton "이름 판":
        style "r13_action_button" area (430,584,200,62) text_size 24 action Return("board") sensitive ready
    frame:
        area (680,54,548,612) padding (26,24) background R13PaperFrame()
        vbox:
            spacing 12
            text "남은 기록" size 28 color "#765426"
            viewport:
                xsize 496 ysize 230 draggable True mousewheel True scrollbars "vertical" vscrollbar_unscrollable "hide"
                vbox:
                    spacing 12
                    for line in r13_ending_notes():
                        text line size r13_read_size(22,26) xsize 464 color "#493b30"
            text "새 여정은 첫날부터 시작해요. 이번 기록과 물건은 이어지지 않아요." size 20 xsize 490 color "#795d40"
            textbutton "새 여정 시작" style "r13_action_button" xsize 490 ysize 54 text_size 24 action Return("restart") sensitive ready
            hbox:
                spacing 12
                textbutton "진행 불러오기" style "r13_action_button" xsize 239 ysize 52 text_size 22 action ShowMenu("load") sensitive ready
                textbutton "메인화면으로" style "r13_action_button" xsize 239 ysize 52 text_size 22 action Confirm("메인화면으로 돌아가시겠습니까?",MainMenu(confirm=False)) sensitive ready

screen r13_nearby():
    style_prefix "r13"
    modal True
    zorder 45
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (220,150,840,515) padding (24,20)
        vbox:
            spacing 15
            text "주변 사람들" size 32 color "#765426"
            viewport:
                xsize 780 ysize 350 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 10
                    for person in r13_people():
                        button:
                            xsize 730 ysize 85 padding (10,8)
                            background R13PaperPanel() hover_background R13PaperPanel()
                            action Return(person) sensitive ready
                            hbox:
                                spacing 20
                                add Transform(r13_art(person,"avatar_neutral"),size=(66,66),fit="contain")
                                text R13_NAMES[person] size 25 yalign .5
            textbutton "돌아가기" action Return(False) sensitive ready
