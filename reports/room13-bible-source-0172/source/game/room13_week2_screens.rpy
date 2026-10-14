# The crisis is a field confrontation, not a second formal trial.
screen r13_crisis():
    style_prefix "r13"
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    add Solid("#172a2aa6")
    frame:
        area (40,165,770,435) padding (24,20) background R13PaperPanel()
        vbox:
            spacing 15
            text "연결을 멈춰야 한다" size 33 color "#765426"
            text "지금 사람들이 따르는 말" size 21 color "#717367"
            for key in ("F1","F2","F3","F4"):
                $ proved=key in room13["propositions"]
                $ open_claim=r13_debate_open(key)
                button:
                    xsize 720 yminimum 65 padding (14,12)
                    background R13PaperPanel(proved)
                    hover_background R13PaperPanel()
                    action Return(key) sensitive (ready and open_claim)
                    vbox:
                        text ("{s}"+R13_CLAIMS[key]["assertion"]+"{/s}" if proved else R13_CLAIMS[key]["assertion"]) size 24 xsize 680
                        if not proved and not open_claim:
                            text ("반론을 그만뒀다" if r13_debate_closed(key) else "반론할 자료가 없다") size 19 color "#8c7060"
    frame:
        area (840,165,400,435) padding (23,20) background R13PaperPanel()
        vbox:
            spacing 16
            text "함께 움직일 준비" size 27 color "#765426"
            for name,prepared in r13_crisis_preparations():
                text (name+" · "+("모아 둠" if prepared else "마련하지 못함")) size 21 color ("#3d7058" if prepared else "#8c7060")
            null height 5
            text "수첩에서 확인한 자료만 보여 줄 수 있다." size 21 xsize 342
            if room13["case_state"]=="occurred" and any(r13_debate_open(c) for c in r13_case_available()):
                textbutton "13호 사건에서 남은 문제" action Return("case") sensitive ready text_size 21
            if r13_has("E29"):
                textbutton "가족과 빠져나갈 길" action Return("escape") sensitive ready text_size 21
    frame:
        area (40,620,1200,80) padding (20,10) background R13PaperPanel()
        hbox:
            spacing 40
            textbutton "수첩을 다시 본다" action Show("r13_book") sensitive ready text_size 24
            textbutton "모은 근거와 해 둔 준비로 움직인다" action Return("finish") sensitive ready text_size 24

screen r13_crisis_proof(claim):
    style_prefix "r13"
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    frame:
        area (50,160,1180,450) padding (28,25) background R13PaperPanel()
        vbox:
            spacing 18
            text "제단 앞 · 맞서야 할 주장" size 22 color "#717367"
            text R13_CLAIMS[claim]["assertion"] size 31 color "#765426"
            text "직접 내놓은 자료" size 22
            viewport:
                xsize 1110 ysize 170 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 8
                    for key in room13["arguments"].get(claim,[]):
                        text ("· "+ROOM13["evidence"][key]["name"]) size 23
                    if not room13["arguments"].get(claim):
                        text "아직 내놓은 자료가 없다." size 22 color "#717367"
            hbox:
                spacing 25
                textbutton "근거를 내놓는다" action Return("present") sensitive ready text_size 24
                textbutton "되묻는다" action Return("press") sensitive ready text_size 24
                textbutton "논리를 연결한다" action Return("argue") sensitive ready text_size 24
                textbutton "다른 주장부터" action Return("leave") sensitive ready text_size 24

screen r13_rescue_notes():
    style_prefix "r13"
    modal True
    zorder 60
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
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
    add Solid("#172a2aa6")
    frame:
        area (60,55,1160,610) padding (32,28) background R13PaperPanel()
        vbox:
            spacing 18
            text "이번 여정의 끝" size 23 color "#717367"
            text R13_ENDINGS[key]["title"] size 44 color "#765426"
            viewport:
                xsize 1080 ysize 240 draggable True mousewheel True scrollbars "vertical"
                vbox:
                    spacing 12
                    for line in r13_ending_notes():
                        text line size 24 xsize 1040
                    text ("기억할 일 · "+R13_ENDINGS[key]["knowledge"]) size 24 xsize 1040 color "#496450"
            text "새 여정은 첫날부터 시작한다. 읽은 대사와 발견 기록은 남고, 증거와 관계는 다시 쌓는다." size 22 xsize 1060
            if not (store.room13 or {}).get("secret_route_unlocked"):
                text "이번 여정의 기억이 남았다. 새 여정에서는 13호실의 책장과 여관 도면을 더 깊이 조사할 수 있다." size 22 xsize 1060 color "#765426"
            text ("지금까지 본 결말 · "+" / ".join(R13_ENDINGS[e]["title"] for e in persistent.room13_endings if e in R13_ENDINGS)) size 20 xsize 1060 color "#717367"
            hbox:
                spacing 24
                textbutton "새 여정 시작" action Return("restart") sensitive ready text_size 25
                textbutton "저장 불러오기" action ShowMenu("load") sensitive ready text_size 25
                textbutton "제목으로" action MainMenu(confirm=False) sensitive ready text_size 25

screen r13_nearby():
    style_prefix "r13"
    modal True
    zorder 45
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
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
