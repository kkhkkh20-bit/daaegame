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
        xpos 855 ypos 18 xsize 400 ysize 70 padding (14,9) background Solid("#142526ed")
        vbox:
            spacing 3
            text ("%d일째 · %s요일 · %s"%(winter["day"],winter_weekday(winter),winter_period_name(winter))) size 22 color "#edcf94"
            text place size 20 color "#edf0e8" xsize 370
    hbox:
        xpos 855 ypos 95 spacing 7
        textbutton "달력" action Show("winter_calendar") style "winter_button" xsize 92 ysize 40 text_size 20 padding (10,8)
        textbutton "수첩" action Show("winter_evidence",False) style "winter_button" xsize 92 ysize 40 text_size 20 padding (10,8)
        textbutton "저장" action ShowMenu("save") style "winter_button" xsize 92 ysize 40 text_size 20 padding (10,8)
        textbutton "설정" action ShowMenu("pause_menu") style "winter_button" xsize 92 ysize 40 text_size 20 padding (10,8)

screen winter_hub():
    modal True
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    button:
        xpos 0 ypos 105 xsize 1280 ysize 495 padding (0,0)
        background None hover_background None insensitive_background None
        action Function(winter_empty_result) sensitive ready
    if winter["location"]=="square":
        add Transform("assets/pouch-world.png",size=(62,65),fit="contain") xpos 530 ypos 350
    for object_key,object_spec in WINTER_WORLD["places"][winter["location"]]["objects"].items():
        $ rect=object_spec["rect"]
        button:
            xpos rect[0] ypos rect[1] xsize rect[2] ysize rect[3] padding (0,0)
            background None hover_background None insensitive_background None
            action Return(("object",object_key)) sensitive ready
    for actor,x,y,w,h,pose in winter_people(winter):
        if not (winter["location"]=="post" and actor!="seryeon") and not (winter["location"]=="inn" and actor!="granny"):
            add Transform(actor+" "+pose,size=(w,h),fit="contain") xpos x ypos y
        $ hit_height=(375-y if actor=="granny" and winter["location"]=="inn" else 410-y if actor=="seryeon" and winter["location"]=="post" else h)
        button:
            xpos x ypos y xsize w ysize hit_height padding (0,0)
            background None hover_background None insensitive_background None
            action Return(("person",actor)) sensitive ready
    if winter["location"]=="inn":
        add Crop((380,375,540,160),Transform("assets/front.png",size=(1280,720))) xpos 380 ypos 375
        for actor,x,y,w,h,pose in winter_people(winter):
            if actor!="granny":
                add Transform(actor+" "+pose,size=(w,h),fit="contain") xpos x ypos y
    if winter["location"]=="post":
        add Crop((0,410,1280,182),winter_background("winter_post")) xpos 0 ypos 410
        # Doto is a customer in front of the counter; Seryeon works behind it.
        for actor,x,y,w,h,pose in winter_people(winter):
            if actor!="seryeon":
                add Transform(actor+" "+pose,size=(w,h),fit="contain") xpos x ypos y
    for key,point in winter.get("checks",{}).items():
        if key.startswith(winter["location"]+":"):
            add TopicTick() xpos point[0]-13 ypos point[1]-13
    for actor,x,y,w,h,pose in winter_people(winter):
        if actor!="bami":
            textbutton (WINTER_NAMES[actor]+" · 대화"):
                xpos x+w//2 xanchor .5 ypos (445 if actor=="seryeon" and winter["location"]=="post" else min(y+h,555)) padding (10,5)
                background Solid("#142526df") text_size 18 text_color "#eee4c9"
                action Return(("person",actor)) sensitive ready
    frame:
        xpos 24 ypos 592 xsize 1232 ysize 120 background Solid("#142526f5") padding (16,10)
        text winter_goal(winter) size 20 color "#edcf94" xpos 0 ypos 0
        text ("다람의 수첩 · 궁금한 곳을 살피고, 주민의 말을 들어 보자.") size 16 color "#bac9c5" xpos 0 ypos 27
    hbox:
        xpos 30 ypos 650 spacing 16
        textbutton "주변 살펴보기" style "winter_button" xsize 260 ysize 52 text_size 20 action Return("look") sensitive ready
        textbutton "지도 · 이동하기" style "winter_button" xsize 240 ysize 52 text_size 20 action Return("map") sensitive ready
        textbutton "시간 보내기" style "winter_button" xsize 180 ysize 52 text_size 20 action Return("wait") sensitive ready and winter_period(winter)<3
        textbutton "여관으로 돌아가 밤 보내기" style "winter_button" xsize 430 ysize 52 text_size 20 action Return("rest") sensitive ready

screen winter_topics(kind,target):
    modal True
    default ready=False
    timer .4 action SetScreenVariable("ready",True)
    frame:
        xpos 830 ypos 195 xsize 425 ysize 505 background Solid("#142526ed") padding (16,14)
        vbox:
            spacing 10
            text (WINTER_NAMES[target] if kind=="person" else WINTER_WORLD["places"][winter["location"]]["objects"][target]["name"]) size 28 color "#edcf94"
            hbox:
                spacing 8
                textbutton "물어보기" style "winter_button" xsize 188 ysize 43 text_size 20 padding (8,5) selected winter_topic_tab=="talk" action SetVariable("winter_topic_tab","talk")
                textbutton "함께할 일" style "winter_button" xsize 188 ysize 43 text_size 20 padding (8,5) selected winter_topic_tab=="activity" action SetVariable("winter_topic_tab","activity")
            viewport:
                id "winter_topic_scroll"
                xsize 393 ysize 322 mousewheel True draggable True
                vbox:
                    spacing 9
                    if kind=="person" and winter_topic_tab=="talk":
                        use winter_small_topic("안부를 묻는다",Return("hello"),winter_greeting_key(winter,target) in winter.get("seen",[]),ready)
                    for key in winter_display_topics(winter,kind,target,winter_topic_tab):
                        use winter_topic_row(key,ready)
                    if kind=="person" and target in WINTER_SCHEDULES and winter_topic_tab=="talk":
                        use winter_small_topic("평소 어디 계세요?",Return("routine"),"routine:"+target in winter.get("seen",[]),ready)
                    if not winter_display_topics(winter,kind,target,winter_topic_tab):
                        text ("지금은 함께할 일이 없다." if winter_topic_tab=="activity" else "더 알아본 뒤 다시 이야기하자.") size 20 xsize 370
            textbutton ("돌아가기" if kind=="object" else "대화 마치기") style "winter_button" xsize 390 ysize 48 text_size 21 action Return("back") sensitive ready

screen winter_small_topic(caption,act,completed,ready):
    button:
        xsize 387 ysize 60 padding (12,6)
        background Solid("#283e42" if completed else "#2d5868") hover_background Solid("#406c78")
        action act sensitive ready
        text ("{s}"+caption+"{/s}" if completed else caption) size 20 color ("#b9c4c4" if completed else "#f4eddb") xsize 355 yalign .5

screen winter_topic_row(key,ready):
    $ completed=key in winter["done"]
    $ caption=WINTER["actions"][key]["name"]
    use winter_small_topic(caption,Return(key),completed,ready and (completed or winter_can_act(winter,key)))

screen winter_map():
    modal True
    add winter_background("winter")
    add Solid("#102329df")
    text "눈에 막힌 마을" xpos 54 ypos 125 size 36 color "#edcf94"
    text (winter_clock(winter)+"\n알아둔 주민의 현재 일정") xpos 54 ypos 180 size 21
    for key,x,y in (("gate",70,290),("square",420,270),("post",800,270),("inn",100,430),("workshop",450,430),("room",800,430),("passage",800,550)):
        if key!="passage" or winter_has(winter,"map") or winter_has(winter,"passage_known"):
            button:
                xpos x ypos y xsize 300 ysize 88 style "winter_button"
                action Return(key)
                vbox:
                    text WINTER["places"][key]["name"] size 25 color "#edcf94"
                    text (("여기 · " if key==winter["location"] else "")+winter_known_at(winter,key)) size 15 xsize 270
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
    text ("기록을 대조한다" if present else "다람의 수첩") xpos 54 ypos 35 size 35 color "#edcf94"
    text "현재 회차에서 직접 얻은 기록만 사용할 수 있습니다." xpos 54 ypos 86 size 19 color "#bac9c5"
    for index,key in enumerate(winter["evidence"][page_index*8:page_index*8+8]):
        button:
            xpos 44+(index%2)*360 ypos 135+(index//2)*106 xsize 345 ysize 96
            style "winter_button"
            background Solid("#55756a" if key in selection else "#243b3d")
            action ([SetScreenVariable("opened",key),SetScreenVariable("selection",[e for e in selection if e!=key] if key in selection else (selection+[key] if len(selection)<2 else selection))] if present else SetScreenVariable("opened",key))
            vbox:
                text (("선택 · " if key in selection else "")+WINTER["evidence"][key]["name"]) size 22 xsize 305
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
            textbutton "달력 펼치기" action [Hide("winter_evidence"),Show("winter_calendar")] style "winter_button"
            textbutton "닫기" action Hide("winter_evidence") style "winter_button"

screen winter_board(claim):
    modal True
    default ready=False
    timer .35 action SetScreenVariable("ready",True)
    frame:
        xpos 35 ypos 395 xsize 1210 ysize 176 background Solid("#172c2dee")
        vbox:
            spacing 10
            text WINTER_NAMES[claim["who"]] size 27 color "#edcf94"
            text claim["text"] size 27 xsize 1140
            text ("입증한 주장 %d개 · 남은 발언 기회 %d"%(len(winter_hearing_wins),winter_hearing_limit(winter)-winter_pressure)) size 20 color "#bac9c5"
    hbox:
        xpos 35 ypos 586 spacing 20
        textbutton "되묻기" style "winter_button" xsize 220 action Return("press") sensitive ready
        textbutton "증거 비교 · 제시" style "winter_button" xsize 300 action Return("present") sensitive ready
        textbutton "이 주장은 보류한다" style "winter_button" xsize 360 action Return("pass") sensitive ready
    text "상대의 설명을 더 듣거나 수첩을 펼쳐 확인할 수 있습니다." xpos 40 ypos 674 size 19

screen winter_end():
    modal True
    zorder 60
    add Solid("#102527f5")
    $ titles={"truth":"함께 겨울을 넘는 사람들","family":"세 사람의 발자국","exposure":"멈춰 선 이송","flight":"비어 있는 자리","separated":"닫힌 문"}
    text titles[winter["ending"]] xpos 70 ypos 65 size 45 color "#edcf94"
    text "겨울의 두 주 · 첫 번째 이야기" xpos 70 ypos 126 size 22
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
            text "누구의 말을 믿었는지, 누구 곁에 남았는지에 따라 마을의 마지막 밤이 달라집니다." size 19 color "#bac9c5" xsize 1030
    hbox:
        xpos 70 ypos 600 spacing 30
        textbutton "다른 두 주 시작하기" action Start("winter_start") style "winter_button"
        textbutton "처음 화면으로" action MainMenu(confirm=False) style "winter_button"


screen winter_calendar():
    modal True
    zorder 70
    default selected_day=winter["day"]
    add Solid("#0b191af7")
    text "다람의 수첩 · 겨울의 두 주" xpos 45 ypos 28 size 34 color "#edcf94"
    text "들은 약속만 적어 뒀어. 날짜를 누르면 다시 볼 수 있어." xpos 45 ypos 77 size 21 color "#bdccc7"
    for col,weekday in enumerate(("월","화","수","목","금","토","일")):
        text weekday xpos 69+col*111 ypos 132 size 23
    for day in range(1,15):
        $ notes=winter_calendar_notes(winter,day)
        button:
            xpos 40+((day-1)%7)*111 ypos 172+((day-1)//7)*135 xsize 103 ysize 124
            padding (10,10) background Solid("#4e6e69" if day==selected_day else "#243c40") hover_background Solid("#496774")
            action SetScreenVariable("selected_day",day)
            vbox:
                spacing 8
                text (str(day)+"일") size 20 color "#ffe0a1"
                if day==winter["day"]:
                    text "오늘" size 15 color "#ffe0a1"
                if day<winter["day"]:
                    text "지나간 날" size 15 color "#aab8b6"
                if notes:
                    text ("기록 %d개"%len(notes)) size 16 xsize 84
    frame:
        xpos 840 ypos 135 xsize 390 ysize 450 padding (20,20) background Solid("#20383d")
        vbox:
            spacing 20
            text (str(selected_day)+"일 · "+winter_weekday(dict(winter,day=selected_day))+"요일") size 29 color "#edcf94"
            viewport:
                xsize 350 ysize 348 mousewheel True draggable True
                vbox:
                    spacing 17
                    for heading,detail in winter_calendar_notes(winter,selected_day):
                        text heading size 22 color "#ffe0a1" xsize 340
                        text detail size 20 xsize 340
                    if not winter_calendar_notes(winter,selected_day):
                        text "아직 적어 둔 약속이 없다." size 22 xsize 340
    text "주민에게 일정을 물으면 달력에도 남습니다." xpos 45 ypos 468 size 21 color "#bac9c5"
    textbutton "수첩 기록" xpos 45 ypos 625 action [Hide("winter_calendar"),Show("winter_evidence",False)] style "winter_button"
    textbutton "덮기" xpos 1050 ypos 625 action Hide("winter_calendar") style "winter_button" xsize 180
