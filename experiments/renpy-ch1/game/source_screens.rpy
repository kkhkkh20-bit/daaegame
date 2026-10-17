screen source_world():
    if source_night:
        add Transform("daram world",size=(180,250),fit="contain") xpos 925 ypos 290
        if source_night in ("touch","eyes","bami"):
            add Solid("#090b1077")
        if source_night == "out":
            add Solid("#eac78544",xsize=90,ysize=16) xpos 585 ypos 437
        if source_night in ("eyes","bami"):
            if source_night == "bami":
                add Transform("bami world",size=(230,290),fit="contain") xpos 740 ypos 55
            else:
                text "●   ●" xpos 805 ypos 120 color "#ddd9b0" size 18

screen source_explore():
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    # Background reaction lies below every evidence and resident hit target.
    button:
        xpos 0 ypos 95 xsize 1280 ysize 505
        background None hover_background None insensitive_background None
        sensitive ready action Function(source_empty_click)
    if source_location == "bed13":
        add Transform("assets/pouch-world.png",size=(60,64)) xpos 880 ypos 270
        add Transform("assets/flour-world.png",size=(64,53)) xpos 590 ypos 337
        if "C11" in source_inventory:
            add Transform(Crop((835,573,389,150),"assets/chest-open.png"),size=(190,90),fit="contain") xpos 655 yanchor 1.0 ypos 521
        else:
            add Transform(Crop((97,351,1082,722),"assets/chest-complete.png"),size=(190,90),fit="contain") xpos 655 yanchor 1.0 ypos 521
        text "첫…   11…2" xpos 701 ypos 185 size 14 color "#a58f7055"
        if not source_found:
            add Transform(Crop((271,356,766,615),"assets/hidden-somsom.png"),size=(43,28),fit="contain",alpha=.23) xpos 822 ypos 480
        for rect,action in [((850,245,95,90),("spot","bag")),((570,330,145,85),("spot","quilt")),((790,460,150,93),("under",None)),((620,170,325,62),("head",None)),((655,431,160,90),("chest",None))]:
            button:
                xpos rect[0] ypos rect[1] xsize rect[2] ysize rect[3]
                background None hover_background None insensitive_background None
                sensitive ready action Return(action)
        if source_found:
            imagebutton:
                xpos 244 ypos 490
                idle Transform("assets/basket-world.png",size=(120,80),fit="contain")
                action Return(("spot","fur")) sensitive ready
    else:
        if source_location == "hall":
            imagebutton:
                xpos 380 ypos 125
                idle Transform("source clock",size=(110,110))
                action Return(("spot","clock")) sensitive ready
        elif source_location in ("dotoroom","front"):
            imagebutton:
                xpos 290 ypos 450
                idle Transform("assets/notebook.png",size=(120,90),fit="contain")
                action Return(("spot","diary" if source_location=="dotoroom" else "book")) sensitive ready
    for person in village_resident_points(source_location):
        $ actor = SOURCE_ALIAS.get(person["id"],person["id"])
        button:
            xpos person["x"] ypos person["y"] xsize 190 ysize 290 padding (0,0)
            background None hover_background None
            action Return(("talk",person["id"])) sensitive ready
            add Transform(actor+" world",size=(190,290),fit="contain")
    for key,point in source_checks.items():
        if key.startswith(source_location+":"):
            add TopicTick() xpos point[0] ypos point[1]
    hbox:
        xpos 740 ypos 604 spacing 15
        textbutton "이동하기":
            xsize 190 ysize 64
            action Return(("map",None)) sensitive ready
        textbutton ("회의로" if not source_started_meeting else "회의 재개"):
            xsize 180 ysize 64
            action Return(("meeting",None)) sensitive ready

screen source_map():
    modal True
    add Transform("assets/inn-map.png",size=(1280,720))
    frame:
        xpos 25 ypos 110
        vbox:
            text "겨울잠 여관" size 32 color "#ffdc91"
            text "돌아볼 곳을 골라요" size 21
    for key,pos in SOURCE_MAP_POINTS.items():
        button:
            xpos pos[0] ypos pos[1] xsize 224 ysize 91 padding (6,7)
            background Solid("#eee2c8f2") hover_background Solid("#ffecc1")
            action Return(key)
            hbox:
                spacing 8
                add Transform(source_bg(SOURCE_EP["LOC_BG"].get(key,key)),size=(62,62),fit="contain")
                vbox:
                    text SOURCE_LOC[key].get("short",SOURCE_LOC[key]["name"]) size 21 color "#443025"
                    text ("현재 위치" if key==source_location else "") size 17 color "#7a5941"
    textbutton "돌아가기" xpos 45 ypos 625 action Return(source_location)

screen source_questions(person):
    modal True
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#0b172733")
    add source_actor+" interview_neutral" at portrait_question id "topic_actor"
    vbox:
        xpos 360 ypos 140 spacing 5
        for q in source_questions(person):
            use topic_banner(q["q"]+(" · 새 이야기" if village_question_new(q) else ""),Return(q),village_question_done(q),enabled=ready)
        use topic_banner("대화 마치기",Return("back"),enabled=ready)

screen source_evidence(present=False):
    modal True
    zorder 60
    default detail = (source_inventory[0] if source_inventory else None)
    default page_index = 0
    add Solid("#100c09d9")
    frame:
        xpos 65 ypos 105 xsize 1150 ysize 535
        fixed:
            text ("증거 제시" if present else "증거 수첩") size 32 color "#ffdc91"
            if not present:
                textbutton "주민 수첩" xpos 840 ypos 0 action Show("village_timetable")
            for i,key in enumerate(source_inventory[page_index*6:page_index*6+6]):
                button:
                    xpos (i%2)*230 ypos 65+(i//2)*110
                    xsize 220 ysize 100 padding (8,5)
                    action (Return(key) if present else SetScreenVariable("detail",key))
                    vbox:
                        add Transform(SOURCE_ICONS[key],size=(74,47),fit="contain") xalign .5
                        text SOURCE_EP["EV"][key]["name"] size 17 xalign .5 text_align .5 xmaximum 198
            if detail:
                add Transform(SOURCE_ICONS[detail],size=(430,180),fit="contain") xpos 520 ypos 45
                text SOURCE_EP["EV"][detail]["name"] xpos 520 ypos 235 size 28 color "#ffdc91"
                text source_text(source_card(detail)) xpos 520 ypos 290 size 21 xsize 535
            hbox:
                ypos 425 spacing 20
                textbutton "◀" action [SetScreenVariable("page_index",page_index-1),Function(source_fx,"page")] sensitive page_index>0
                text str(page_index+1)+" / "+str(max(1,(len(source_inventory)+5)//6)) size 22 yalign .5
                textbutton "▶" action [SetScreenVariable("page_index",page_index+1),Function(source_fx,"page")] sensitive (page_index+1)*6<len(source_inventory)
                textbutton ("취소" if present else "닫기") action (Return("cancel") if present else Hide("source_evidence"))

init python:
    class MotherHandwriting(renpy.Displayable):
        """UI trace of the existing v2 '다' comparison, not a new illustration."""
        def __init__(self, ink, **kwargs):
            super(MotherHandwriting,self).__init__(**kwargs)
            self.ink = ink

        def render(self,width,height,st,at):
            rendered = renpy.Render(220,145)
            canvas = rendered.canvas()
            for y in (32,65,98,131):
                canvas.line("#b5a17b55",(0,y),(220,y),1)
            def quadratic(start,control,end):
                return [(round((1-t)**2*start[0]+2*(1-t)*t*control[0]+t*t*end[0]),
                         round((1-t)**2*start[1]+2*(1-t)*t*control[1]+t*t*end[1]))
                        for t in [i/20.0 for i in range(21)]]
            # The same source SVG paths appear on both papers in play_v2.html.
            strokes = [[(38,39),(55,38),(73,39),(85,38)],
                       [(39,40),(38,91)]+quadratic((38,91),(38,99),(47,98))+[(86,97)],
                       [(110,31),(109,93)]+quadratic((109,93),(108,116),(130,119))+
                       quadratic((130,119),(156,124),(180,105)),
                       [(110,60),(146,60)]]
            for stroke in strokes:
                canvas.lines(self.ink,False,stroke,4)
            return rendered

screen source_inspect(key):
    modal True
    $ evidence_key = key[:3]
    $ picture = ("assets/contract.png" if key=="C01b" else SOURCE_ICONS.get(evidence_key,"assets/notebook.png"))
    add Solid("#130f0be8")
    frame:
        xpos 160 ypos 100 xsize 960 ysize 520
        if key == "motherlead":
            fixed:
                text "남겨진 한 줄 · 두 글씨" size 30 color "#ffdc91"
                hbox:
                    ypos 55 spacing 28
                    for caption,ink,paper,kind in (("서점 책 이름표","#593923","#f7edce","book"),("장부의 한 줄","#987746","#e9d6ac","ledger")):
                        frame:
                            xsize 420 ysize 285 padding (18,16)
                            background Solid(paper)
                            vbox:
                                spacing 13
                                text caption size 23 color ink
                                add MotherHandwriting(ink) xalign .5 id ("mother_"+kind)
                                text "‘다’의 마지막 세로획이\n길게 이어져 꼬리를 만든다." size 19 color ink
                text "책 이름표와 나란히 놓아 본다." ypos 355 size 21 color "#c6b699"
                textbutton "계속" ypos 390 action [Function(source_fx,"page"),Return()]
        else:
            vbox:
                spacing 15
                text SOURCE_EP["EV"].get(evidence_key,{}).get("name","흔적 살펴보기") size 30 color "#ffdc91"
                add Transform(picture,size=(890,330),fit="contain")
                textbutton "계속" action [Function(source_fx,"page"),Return()]

screen source_choice(title,options):
    modal True
    zorder 40
    frame:
        xpos 165 ypos 100 xsize 950
        vbox:
            spacing 12
            text source_text(title) size 27 color "#ffdc91"
            for option in options:
                textbutton option["label"] action Return(option) xfill True ysize 49

screen source_debate(round):
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    $ claim = round["stms"][source_statement]
    $ actor = SOURCE_ALIAS.get(claim["w"],claim["w"])
    add Transform(actor+" interview_neutral",size=(325,400),fit="contain") xpos 825 ypos 130 id "debate_actor"
    frame:
        xpos 25 ypos 110 xsize 725 ysize 415
        fixed:
            text round.get("topic","원탁 회의") size 27 color "#ffdc91"
            for i,statement in enumerate(round["stms"]):
                button:
                    xpos 0 ypos 50+i*87 xsize 674 ysize 80 padding (12,9)
                    background Solid("#65503d" if i==source_statement else "#30261fed")
                    action Return(("select",i)) sensitive ready
                    text source_name(statement["w"])+"  "+source_text(statement["t"]) size 22 xmaximum 650
            hbox:
                ypos 327 spacing 24
                textbutton "되묻기" action Return(("press",None)) sensitive ready
                textbutton "증거" action Return(("evidence",None)) sensitive ready
                if source_step and claim.get("steps"):
                    $ compared = claim["steps"][min(source_step,len(claim["steps"]))-1]["ids"][0]
                    text ("비교 중 · "+SOURCE_EP["EV"][compared]["name"]) size 19 yalign .5
    hbox:
        xpos 25 ypos 551 spacing 9
        for key in SOURCE_EP["MEET"]["seats"]:
            $ alias = SOURCE_ALIAS.get(key,key)
            frame:
                xsize 144 ysize 120 padding (4,4)
                vbox:
                    add Transform(alias+" neutral",size=(110,75),fit="contain") xalign .5
                    text source_name(key) size 18 xalign .5
                    text source_name(source_votes.get(key,"기권")) size 15 color "#c6b699" xalign .5

screen source_proof():
    frame:
        xpos 120 ypos 105 xsize 1040 ysize 420
        hbox:
            spacing 30
            for key in source_proof_show[:2]:
                vbox:
                    spacing 14 xsize 470
                    if key == "C06" and "C07" in source_proof_show:
                        fixed:
                            xsize 450 ysize 310
                            add Transform(SOURCE_ICONS[key],size=(210,210),fit="contain") xpos 10 ypos 15 id "proof_clock_ours"
                            add Transform(SOURCE_ICONS[key],size=(210,210),fit="contain",rotate=180) xpos 230 ypos 15 id "proof_clock_bami"
                            text "우리의 시선" xpos 10 ypos 250 xsize 210 text_align .5 size 19 color "#c6b699"
                            text "밤이의 시선" xpos 230 ypos 250 xsize 210 text_align .5 size 19 color "#ffdc91"
                    else:
                        add Transform(SOURCE_ICONS[key],size=(450,310),fit="contain")
                    text SOURCE_EP["EV"][key]["name"] size 22 color "#ffdc91"
