# Authored opening, kept separate from the captured chapter/source baseline.
default arrival_location = None
default arrival_met = []
default arrival_seen = []
default arrival_greeted = []
default arrival_post_closed = False
default arrival_stone = False
default arrival_cold = False
default arrival_checked_in = False

init 20 python:
    ARRIVAL = json.load(renpy.file("village-story.json"))
    ARRIVAL_PLACES = {
        "gate": ("마을 입구", "outdoor-gate.png", (155,435), "wanggu"),
        "fountain": ("광장", "outdoor-fountain.png", (430,295), "buri"),
        "lane": ("지붕 아래 골목", "outdoor-lane.png", (680,455), "geokkuri"),
        "post": ("우체국", "outdoor-post.png", (740,215), None),
        "inn": ("겨울잠 여관", "outdoor-inn.png", (990,330), "seryeon"),
    }
    ARRIVAL_PEOPLE = {"gate":"wanggu", "fountain":"buri", "lane":"geokkuri", "inn":"seryeon"}

    def arrival_cold_picture(packet):
        zoom=packet.get("z",1)
        width,height=int(1280/zoom),int(720/zoom)
        x=max(0,min(1280-width,int(packet.get("fx",.5)*1280-width/2)))
        y=max(0,min(720-height,int(packet.get("fy",.5)*720-height/2)))
        image=Transform(SOURCE_PATHS[packet["img"]],size=(1280,720))
        return Transform(Crop((x,y,width,height),image),size=(1280,720))

    def arrival_scene(key):
        if key in store.arrival_seen:
            spec = dict(ARRIVAL["visits"].get(key, ARRIVAL["scenes"].get(key)))
            spec["items"] = ARRIVAL["repeat"][key]
            spec["sid"] += "_REPEAT"
        else:
            spec = ARRIVAL["visits"].get(key, ARRIVAL["scenes"].get(key))
        return spec

    def arrival_case():
        # Copy, never mutate the snapshot or the authored data in place.
        import copy
        scenes = copy.deepcopy(ARRIVAL["case"])
        if "seryeon" in store.arrival_met:
            for packet in scenes[0]["items"]:
                if isinstance(packet,source_builtins.list) and packet[1]=="세련입니다. 여기 묵고 있는 손님이에요.":
                    packet[1]="어제 문 앞에서 봤죠? 제 돈이 없어졌습니다."
        if "wanggu" in store.arrival_met:
            for packet in scenes[1]["items"]:
                if isinstance(packet,source_builtins.list) and packet[1]=="자경단장 너울입니다. 주머니 모양은요?":
                    packet[1]="신고받고 왔습니다. 주머니 모양은요?"
        return scenes

    def arrival_question_lines(question):
        opening = ARRIVAL.get("question_openings",{}).get(question["id"])
        if not opening:
            return question["lines"]
        variant = "met" if store.source_person in store.arrival_met else "unmet"
        return opening[variant] + question["lines"][5:]

label arrival_prologue:
    call arrival_cold_open
    $ source_scene, place, clock_text = "V_TITLE", "프롤로그", "고갯길"
    window hide
    hide visitor
    scene black with Dissolve(.15)
    $ source_pulse(False)
    $ source_score("inn_family")
    $ renpy.pause(.3,hard=True)
    show screen arrival_title
    $ renpy.pause(1.2,hard=True)
    hide screen arrival_title
    show screen hud
    call source_scenes([ARRIVAL["scenes"]["carriage"]])
    $ stage,arrival_location = "village","gate"
    jump arrival_place

label arrival_cold_open:
    $ arrival_cold = True
    $ source_camera,source_night,source_stage_person = "cold",None,None
    $ source_scene,place,clock_text = "COLD","어느 방", "그날 자정"
    hide screen hud
    hide visitor
    window hide
    scene black with Dissolve(.15)
    $ source_pulse(False)
    $ source_score(None)
    $ typing_allowed = False
    $ cold_index = 0
    while cold_index < len(SOURCE_EP["COLD"]):
        $ cold_packet = SOURCE_EP["COLD"][cold_index]
        if cold_packet.get("title"):
            window hide
            scene black with Dissolve(.3)
            $ source_pulse(False)
            show screen arrival_cold_title
            $ renpy.pause(1.3,hard=True)
            hide screen arrival_cold_title
        else:
            $ renpy.music.play("assets/cold-heart-"+str(cold_index)+".wav",channel="pulse",loop=True,fadein=.1)
            $ renpy.pause(.2,hard=True)
            scene expression arrival_cold_picture(cold_packet) with Dissolve(.2)
            show screen arrival_cold_shade
            if cold_packet.get("fxs") == "breath":
                $ source_fx("page")
            elif cold_packet.get("fxs") == "step":
                $ source_fx("steps")
            $ cold_who = "narr" if cold_packet["say"].startswith("(") else "???"
            call source_lines([[cold_who,cold_packet["say"]]],"COLD_"+cold_packet["id"])
        $ cold_index += 1
    hide screen arrival_cold_shade
    $ source_pulse(False)
    $ arrival_cold = False
    return

label arrival_roam:
    $ stage = "village"
    $ source_camera, source_night, source_stage_person = "village",None,None
    $ place, clock_text = "작은 동물마을", village_clock()+" · 첫눈을 앞두고"
    window hide
    hide visitor
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("village_bright")
    $ renpy.pause(.3,hard=True)
    scene expression Transform("assets/village-map.png",size=(1280,720)) with Dissolve(.18)
    call screen arrival_map
    $ village_minutes += 5 if _return != arrival_location else 0
    $ arrival_location = _return
    if arrival_location == "post":
        call source_scenes([arrival_scene("post")])
        $ arrival_post_closed = True
        if "post" not in arrival_seen:
            $ arrival_seen.append("post")
        jump arrival_roam
    jump arrival_place

label arrival_place:
    $ place, clock_text = ARRIVAL_PLACES[arrival_location][0], village_clock()
    $ source_camera,source_night,source_stage_person = "innentrance" if arrival_location=="inn" else "stage",None,None
    $ source_background = "outdoor-"+arrival_location
    $ stage = "village"
    window hide
    hide visitor
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("village_bright")
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.18)
    call screen arrival_place
    $ arrival_action = _return
    if arrival_action == "map":
        jump arrival_roam
    if arrival_action == "stay":
        jump arrival_inn
    if arrival_action == "stone":
        $ arrival_key = "stone"
        call arrival_topic
        jump arrival_place
    $ arrival_question_person = arrival_location
    call arrival_interview
    jump arrival_place

label arrival_inn:
    $ place,clock_text = "겨울잠 여관 · 접수대",village_clock()
    $ source_camera,source_background,source_night,source_stage_person = "stage","front",None,None
    window hide
    hide visitor
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("village_bright")
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.18)
    call screen arrival_interior
    if _return == "outside":
        jump arrival_place
    if _return == "map":
        jump arrival_roam
    $ arrival_question_person = "granny"
    call arrival_interview
    if arrival_checked_in:
        $ stage = "opening"
        call source_scenes([sc for sc in SOURCE_EP["PRO"] if sc["sid"]=="P5"])
        call source_scenes([ARRIVAL["scenes"]["bedroom"]])
        $ village_event("case_begin")
        call source_scenes(arrival_case())
        return
    jump arrival_inn

label arrival_interview:
    $ arrival_actor = "granny" if arrival_question_person=="granny" else SOURCE_ALIAS.get(ARRIVAL_PEOPLE[arrival_question_person],ARRIVAL_PEOPLE[arrival_question_person])
    window hide
    hide visitor
    call screen arrival_questions
    if _return == "back":
        return
    $ arrival_key = _return
    $ village_event("arrival_"+arrival_key)
    $ village_relationship("arrival_room",["granny"],1) if arrival_key=="room" else None
    if arrival_key == "room":
        if not arrival_post_closed:
            call source_scenes([ARRIVAL["scenes"]["inn_before_post"]])
            if "room" not in arrival_seen:
                $ arrival_seen.append("room")
        else:
            call source_scenes([ARRIVAL["scenes"]["checkin"]])
            $ arrival_checked_in = True
            return
    else:
        call arrival_topic
    jump arrival_interview

label arrival_topic:
    $ village_event("arrival_"+arrival_key)
    call source_scenes([arrival_scene(arrival_key)])
    if arrival_key not in arrival_seen:
        $ arrival_seen.append(arrival_key)
    $ arrival_person = "innma" if arrival_key=="inn_town" else "buri" if arrival_key=="stone" else ARRIVAL_PEOPLE[arrival_location]
    $ village_relationship("arrival_"+arrival_key,[SOURCE_ALIAS.get(arrival_person,arrival_person)],1)
    if arrival_person not in arrival_met:
        $ arrival_met.append(arrival_person)
    if arrival_key == "stone":
        $ arrival_stone = True
    return

screen arrival_cold_title():
    text "1장" xalign .5 yalign .40 size 25 color "#bca487"
    text "열세 번째 침대" xalign .5 yalign .53 size 43 color "#ffdc91"

screen arrival_cold_shade():
    zorder -1
    add Solid("#02040b88")

screen arrival_questions():
    modal True
    add arrival_actor+" interview_neutral" at portrait_close
    add Solid("#0b172733")
    vbox:
        xpos 360 ypos 140 spacing 5
        for q in ARRIVAL["questions"][arrival_question_person]:
            use topic_banner(q["q"],Return(q["id"]),q["id"] in arrival_seen)
        use topic_banner("대화 마치기",Return("back"))

screen arrival_interior():
    modal True
    default ready = False
    timer .35 action SetScreenVariable("ready",True)
    imagebutton:
        xpos 560 ypos 200
        idle Transform("granny world",size=(240,320),fit="contain")
        hover Transform("granny world",size=(240,320),fit="contain",alpha=.85)
        sensitive ready action Return("talk")
    text "할머니를 눌러 대화" xpos 525 ypos 555 size 21 color "#f3e7ce"
    hbox:
        xpos 730 ypos 612 spacing 18
        textbutton "밖으로" action Return("outside") sensitive ready
        textbutton "이동하기" action Return("map") sensitive ready

transform arrival_snow(delay=0.0, start_x=100):
    xpos start_x ypos -10 alpha .0
    pause delay
    alpha .45
    linear 9.0 xpos (start_x+60) ypos 730
    repeat

transform arrival_glimmer:
    alpha .25
    ease .8 alpha .9
    ease 1.0 alpha .3
    repeat

screen arrival_title():
    text "프롤로그" xalign .5 yalign .42 size 28 color "#c6b699"
    text "고갯길의 두 사람" xalign .5 yalign .54 size 43 color "#ffdc91"

screen arrival_snow():
    for i in range(15):
        text "·" size (14+i%3*4) color "#dce7ed" at arrival_snow(i*.53, i*90-40)

screen arrival_map():
    modal True
    default ready = False
    timer .35 action SetScreenVariable("ready",True)
    add Transform("assets/village-map.png",size=(1280,720))
    add VillagePaths()
    frame:
        xpos 28 ypos 95 background Solid("#eee2c8f2")
        vbox:
            spacing 8
            text "작은 동물마을" size 30 color "#443025"
            text "어디로 갈까?" size 19 color "#7a5941"
    for key, spec in ARRIVAL_PLACES.items():
        button:
            xpos spec[2][0]-90 ypos spec[2][1]-100 xsize 205 ysize 185
            background Solid("#eee2c8f2") hover_background Solid("#ffecc1")
            padding (0,0) sensitive ready action Return(key)
            fixed:
                frame:
                    xalign .5 xsize 192 ysize 114 padding (4,4)
                    background Solid("#e5cc97")
                    add Transform("assets/"+spec[1],size=(184,106))
                frame:
                    ypos 116 xalign .5 padding (8,6) background None
                    vbox:
                        text spec[0] size 22 xalign .5 color "#443025"
                        if key=="post" and arrival_post_closed:
                            text "내일 아침 9시" size 16 color "#7a5941" xalign .5
                        elif key==arrival_location:
                            text "현재 위치" size 16 color "#7a5941" xalign .5
    frame:
        xpos 32 ypos 633 padding (16,10) background Solid("#eee2c8f2")
        text ("우체국은 내일 연다. 오늘은 쉴 곳을 찾자." if arrival_post_closed else "장소를 눌러 이동 · 주민을 눌러 대화") size 21 color "#7a5941"

screen arrival_place():
    modal True
    default ready = False
    timer .35 action SetScreenVariable("ready",True)
    $ resident = village_arrival_resident(arrival_location)
    if resident:
        $ person = SOURCE_ALIAS.get(resident,resident)
        imagebutton:
            xpos 720 ypos (105 if person=="bami" else 245)
            idle Transform(person+" world",size=(225,290),fit="contain")
            hover Transform(person+" world",size=(225,290),fit="contain",alpha=.85)
            sensitive ready action Return("talk")
    else:
        text "주민은 자리를 비웠다." xpos 685 ypos 555 size 21 color "#f3e7ce"
    if arrival_location == "fountain":
        button:
            xpos 380 ypos 155 xsize 190 ysize 315
            background None hover_background None padding (0,0)
            sensitive ready action Return("stone")
    hbox:
        xpos 620 ypos 612 spacing 18
        textbutton "이동하기" sensitive ready action Return("map") xsize 220 ysize 64
        if arrival_location == "inn":
            textbutton "여관에 들어가기" sensitive ready action Return("stay")

screen arrival_stone_glow():
    zorder 10
    add Solid("#8bdfca18") at arrival_glimmer
