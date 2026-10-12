style winter_button is button:
    background Solid("#233a3beF")
    hover_background Solid("#3e5654")
    insensitive_background Solid("#202b2c")
    padding (18,14)
style winter_button_text is button_text:
    size 23
    color "#eee4c9"
    insensitive_color "#87918b"

screen winter_hud():
    zorder 20
    frame:
        xpos 24 ypos 18 padding (16,10) background Solid("#142526ef")
        vbox:
            text place size 23 color "#edcf94"
            text clock_text size 18 color "#bac9c5"
    hbox:
        xpos 982 ypos 18 spacing 8
        textbutton "수첩" action Show("winter_evidence",False) style "winter_button" xsize 92
        textbutton "저장" action ShowMenu("save") style "winter_button" xsize 92
        textbutton "설정" action ShowMenu("pause_menu") style "winter_button" xsize 92

screen winter_hub():
    modal True
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    if winter["location"]=="inn":
        add Transform("granny inn_activity",size=(190,330),fit="contain") xpos 590 ypos 180
        add Crop((380,375,540,160),Transform("assets/front.png",size=(1280,720))) xpos 380 ypos 375
    elif winter_location["person"]:
        add Transform(winter_location["person"]+" world",size=(200,310),fit="contain") xpos 800 ypos 220
    frame:
        xpos 30 ypos 130 xsize 590 ysize 402 background Solid("#142526ed") padding (22,18)
        vbox:
            spacing 12
            text ("오늘 남은 행동  %d / 3"%winter["ap"]) size 27 color "#edcf94"
            text "이동·둘러보기·수첩은 행동을 쓰지 않습니다." size 18 color "#bac9c5"
            viewport:
                xsize 546 ysize 278 mousewheel True draggable True
                vbox:
                    spacing 8
                    for key in winter_options(winter):
                        textbutton (WINTER["actions"][key]["name"]+"  · 1회"):
                            style "winter_button" xsize 540 ysize 60 text_size 20
                            action Return(key) sensitive ready and winter["ap"]>0
                    if not winter_options(winter):
                        text "지금 이곳에서 더 물을 이야기는 없다.\n다른 장소를 살피거나 수첩을 읽자." size 22 xsize 510
    frame:
        xpos 30 ypos 545 xsize 840 ysize 70 background Solid("#142526ed")
        text ("내일: 토리가 광장 난간에서 연습한다고 했다." if winter["day"]==1 else "오늘만: 토리가 광장에 있다. 내일 난간을 막는다고 했다." if winter["day"]==2 else "누비의 집을 경비가 지켜본다. 가족을 옮길 시간이 남았다." if winter["day"]==5 and winter["witness"]=="available" else "누비가 구금됐다. 7일이 지나기 전에 이송 지시를 확인하자." if winter["witness"]=="detained" else "남은 기록을 비교하자. 열흘째 심의는 준비와 관계없이 열린다.") size 20 xsize 790
    hbox:
        xpos 30 ypos 635 spacing 16
        textbutton "주변 살펴보기" style "winter_button" xsize 260 action Return("look") sensitive ready
        textbutton "지도 · 이동하기" style "winter_button" xsize 280 action Return("map") sensitive ready
        textbutton "여관으로 돌아가 밤 보내기" style "winter_button" xsize 430 action Return("rest") sensitive ready

screen winter_map():
    modal True
    add Transform("assets/winter-gate.webp",size=(1280,720))
    add Solid("#102329df")
    text "눈에 막힌 마을" xpos 54 ypos 125 size 36 color "#edcf94"
    text "방문할 장소를 고르세요 · 이동은 무료" xpos 54 ypos 180 size 21
    for key,x,y in (("gate",70,290),("square",420,270),("post",800,270),("inn",100,430),("workshop",450,430),("room",800,430),("passage",800,550)):
        if key!="passage" or winter_has(winter,"map"):
            button:
                xpos x ypos y xsize 300 ysize 88 style "winter_button"
                action Return(key)
                vbox:
                    text WINTER["places"][key]["name"] size 25 color "#edcf94"
                    text ("현재 위치" if key==winter["location"] else "이동하기") size 18
    textbutton "돌아가기" xpos 60 ypos 630 action Return(winter["location"]) style "winter_button"

screen winter_confirm(message):
    modal True
    zorder 60
    default ready=False
    timer .3 action SetScreenVariable("ready",True)
    add Solid("#081718cb")
    frame:
        xpos 200 ypos 240 xsize 880 background Solid("#203638")
        vbox:
            spacing 24
            text message size 29 xsize 820
            hbox:
                spacing 24
                textbutton "진행한다" style "winter_button" xsize 310 action Return(True) sensitive ready
                textbutton "다시 생각한다" style "winter_button" xsize 380 action Return(False) sensitive ready

screen winter_evidence(present=False):
    modal True
    zorder 65
    default page_index=0
    default selection=[]
    default opened=None
    add Solid("#0b191af8")
    text ("비교할 자료 두 개" if present else "조사 수첩") xpos 54 ypos 35 size 35 color "#edcf94"
    text "현재 회차에서 직접 얻은 기록만 사용할 수 있습니다." xpos 54 ypos 86 size 19 color "#bac9c5"
    for index,key in enumerate(winter["evidence"][page_index*8:page_index*8+8]):
        button:
            xpos 44+(index%2)*360 ypos 135+(index//2)*106 xsize 345 ysize 96
            style "winter_button"
            background Solid("#55756a" if key in selection else "#243b3d")
            action ([SetScreenVariable("opened",key),SetScreenVariable("selection",[e for e in selection if e!=key] if key in selection else (selection+[key] if len(selection)<2 else selection))] if present else SetScreenVariable("opened",key))
            vbox:
                text (("✓ " if key in selection else "")+WINTER["evidence"][key]["name"]) size 22 xsize 305
                text (str(winter["records"][key]["day"])+"일째 · "+WINTER["places"][winter["records"][key]["place"]]["name"]) size 16 color "#bac9c5"
    frame:
        xpos 800 ypos 140 xsize 420 ysize 410 background Solid("#243b3d")
        vbox:
            spacing 22
            if opened:
                text WINTER["evidence"][opened]["name"] size 26 color "#edcf94" xsize 370
                text WINTER["evidence"][opened]["text"] size 24 xsize 370
            else:
                text "기록을 눌러 내용을 확인하세요." size 24 xsize 360
                if present:
                    text "서로 뒷받침하는 자료 두 개를 고른 뒤 제시하세요. 선택 순서는 상관없습니다." size 22 xsize 360
    hbox:
        xpos 45 ypos 606 spacing 20
        textbutton "이전" action SetScreenVariable("page_index",page_index-1) sensitive page_index>0 style "winter_button"
        text "[page_index+1]" yalign .5
        textbutton "다음" action SetScreenVariable("page_index",page_index+1) sensitive (page_index+1)*8<len(winter["evidence"]) style "winter_button"
        if present:
            textbutton "두 자료를 제시" action [SetVariable("winter_selected",selection),Return(True)] sensitive len(selection)==2 style "winter_button"
            textbutton "취소" action Return(False) style "winter_button"
        else:
            textbutton "닫기" action Hide("winter_evidence") style "winter_button"

screen winter_board(claim):
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    frame:
        xpos 35 ypos 120 xsize 645 ysize 380 background Solid("#172c2dee")
        vbox:
            spacing 22
            text WINTER_NAMES[claim["who"]] size 27 color "#edcf94"
            text claim["text"] size 29 xsize 592
            text ("입증한 주장 %d개 · 남은 발언 기회 %d"%(len(winter_hearing_wins),3-winter_pressure)) size 20 color "#bac9c5"
    hbox:
        xpos 35 ypos 586 spacing 20
        textbutton "되묻기" style "winter_button" xsize 220 action Return("press") sensitive ready
        textbutton "증거 비교 · 제시" style "winter_button" xsize 300 action Return("present") sensitive ready
        textbutton "이 주장은 보류한다" style "winter_button" xsize 360 action Return("pass") sensitive ready
    text "되묻기와 수첩 검토는 기회를 쓰지 않습니다. 틀린 제시·보류는 1회를 씁니다." xpos 40 ypos 674 size 19

screen winter_end():
    modal True
    zorder 60
    add Solid("#102527f5")
    $ titles={"truth":"함께 겨울을 넘는 사람들","family":"세 사람의 발자국","exposure":"멈춰 선 이송","flight":"비어 있는 자리","separated":"닫힌 문"}
    text titles[winter["ending"]] xpos 70 ypos 65 size 45 color "#edcf94"
    text "겨울의 열흘 · 시나리오 개발판" xpos 70 ypos 126 size 22
    viewport:
        xpos 70 ypos 185 xsize 1120 ysize 360 mousewheel True draggable True
        vbox:
            spacing 15
            text "이번 회차에서 남은 과제" size 28
            for item in winter_missing(winter):
                text ("· "+item) size 23
            if not winter_missing(winter):
                text "가족과 증인을 지키고, 네 주장을 입증하고, 희생 없이 버틸 시간을 마련했다." size 24 xsize 1030
            text "다음 회차에도 기록은 직접 확보해야 합니다. 읽은 대사는 건너뛸 수 있습니다." size 22 xsize 1030
            text "현재판: 10일과 결말까지 플레이 가능. 장소별 겨울 배경·엄마 전용 인물 그림·음성은 후속 제작 대상입니다." size 19 color "#bac9c5" xsize 1030
    hbox:
        xpos 70 ypos 600 spacing 30
        textbutton "다른 열흘 시작하기" action Start("winter_start") style "winter_button"
        textbutton "처음 화면으로" action MainMenu(confirm=False) style "winter_button"
