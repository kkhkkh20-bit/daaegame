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
    timer .35 action SetScreenVariable("ready",True)
    if source_location == "bed13":
        add Transform("assets/pouch-world.png",size=(60,64)) xpos 880 ypos 270
        add Transform("assets/flour-world.png",size=(64,53)) xpos 590 ypos 337
        add Transform(Crop((880,550,365,150),"assets/chest.png"),size=(150,62)) xpos 659 ypos 443
        if not source_found:
            add Transform(Crop((802,490,110,80),"assets/somsom.png"),size=(27,19),alpha=.23) xpos 828 ypos 480
        for rect,action in [((680,215,310,115),("spot","bag")),((563,331,150,97),("spot","quilt")),((550,500,345,87),("under",None)),((620,170,325,62),("head",None)),((655,406,158,93),("chest",None))]:
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
        for i,person in enumerate(SOURCE_EP["PPL"].get(source_location,[])):
            $ actor = SOURCE_ALIAS.get(person[0],person[0])
            imagebutton:
                xpos (690+i*220) ypos (80 if actor=="bami" else 245)
                idle Transform(actor+" world",size=(190,290),fit="contain")
                hover Transform(actor+" world",size=(190,290),fit="contain",alpha=.85)
                action Return(("talk",person[0])) sensitive ready
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
    hbox:
        xpos 810 ypos 604 spacing 15
        imagebutton:
            idle Transform("assets/move.png",size=(64,64))
            action Return(("map",None)) sensitive ready
        textbutton ("회의로" if not source_started_meeting else "회의 재개"):
            action Return(("meeting",None)) sensitive ready

screen source_map():
    modal True
    add Transform("assets/map.png",size=(1280,720))
    add Solid("#140f0a88")
    frame:
        xpos 25 ypos 110
        vbox:
            text "마을과 여관" size 32 color "#ffdc91"
            text "장소를 고르세요" size 21
    for key,pos in SOURCE_MAP_POINTS.items():
        button:
            xpos pos[0] ypos pos[1] xsize 224 ysize 91 padding (10,12)
            action Return(key)
            hbox:
                spacing 8
                add Transform("assets/move.png",size=(36,36))
                vbox:
                    text SOURCE_LOC[key].get("short",SOURCE_LOC[key]["name"]) size 21
                    text ("현재 위치" if key==source_location else "") size 17 color "#c6b699"
    textbutton "돌아가기" xpos 45 ypos 625 action Return(source_location)

screen source_questions(person):
    modal True
    add Transform(source_actor+" neutral",size=(340,390),fit="contain") xpos 825 ypos 155
    frame:
        xpos 55 ypos 120 xsize 690 ysize 490
        vbox:
            spacing 10
            text source_name(person) size 32 color "#ffdc91"
            for q in source_questions(person):
                textbutton (q["q"]+(" · 기록함" if q["id"] in source_seen else "")):
                    action Return(q) xsize 620 ysize 53
            textbutton "돌아가기" action Return("back")

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

screen source_inspect(key):
    modal True
    $ evidence_key = key[:3]
    $ picture = ("assets/contract.png" if key=="C01b" else SOURCE_ICONS.get(evidence_key,"assets/notebook.png"))
    add Solid("#130f0be8")
    frame:
        xpos 160 ypos 100 xsize 960 ysize 520
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
    $ claim = round["stms"][source_statement]
    $ actor = SOURCE_ALIAS.get(claim["w"],claim["w"])
    add Transform(actor+" neutral",size=(325,365),fit="contain") xpos 825 ypos 165
    frame:
        xpos 25 ypos 110 xsize 725 ysize 415
        fixed:
            text round.get("topic","원탁 회의") size 27 color "#ffdc91"
            for i,statement in enumerate(round["stms"]):
                button:
                    xpos 0 ypos 50+i*87 xsize 674 ysize 80 padding (12,9)
                    background Solid("#65503d" if i==source_statement else "#30261fed")
                    action Return(("select",i))
                    text source_name(statement["w"])+"  "+source_text(statement["t"]) size 22 xmaximum 650
            hbox:
                ypos 327 spacing 24
                textbutton "되묻기" action Return(("press",None))
                textbutton "증거" action Return(("evidence",None))
                text ("비교 "+str(source_step)+" / "+str(len(claim.get("steps",[])))) size 19 yalign .5
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
                    add Transform(SOURCE_ICONS[key],size=(450,310),fit="contain")
                    text SOURCE_EP["EV"][key]["name"] size 22 color "#ffdc91"
