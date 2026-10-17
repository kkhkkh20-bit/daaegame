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
    # The anonymous cold open remains available for review, not the default route.
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
    scene expression Transform("assets/village-overview.png",size=(1280,720)) with Dissolve(.18)
    call screen arrival_map
    $ village_advance_evening(5 if _return != arrival_location else 0)
    $ arrival_location = _return
    if arrival_location == "post":
        call source_scenes([arrival_scene("post")])
        $ arrival_post_closed = True
        if "post" not in arrival_seen:
            $ arrival_seen.append("post")
        jump arrival_place
    jump arrival_place

label arrival_place:
    if arrival_location not in village_places_seen:
        $ village_places_seen.append(arrival_location)
    $ stage = "village"
    call scene_present(dict(sid="V_PLACE_"+arrival_location,title=ARRIVAL_PLACES[arrival_location][0],sub=village_clock(),camera="innentrance" if arrival_location=="inn" else "stage",bg="outdoor-"+arrival_location,music="village_bright"))
    call screen arrival_place
    $ arrival_action = _return
    if arrival_action == "map":
        jump arrival_roam
    if arrival_action == "nearby":
        call screen village_nearby_residents(arrival_location)
        if _return != "back":
            $ selected_local = _return
            $ selected_room = village_interior_room(selected_local,arrival_location)
            if selected_room:
                $ arrival_inn_room = selected_room
                if "inn:"+arrival_inn_room not in village_interiors_seen:
                    $ village_interiors_seen.append("inn:"+arrival_inn_room)
                call scene_present(village_inn_spec())
                call village_contact(selected_local)
                jump arrival_inn
            call village_contact(selected_local)
        jump arrival_place
    if arrival_action == "look":
        call source_lines(VILLAGE_PLACE_LOOK[arrival_location],"V_LOOK_"+arrival_location)
        jump arrival_place
    if arrival_action == "stay":
        $ arrival_inn_room = "reception"
        jump arrival_inn
    if arrival_action == "stone":
        $ arrival_key = "stone"
        call arrival_topic
        jump arrival_place
    if isinstance(arrival_action,str) and arrival_action.startswith("local:"):
        call village_contact(arrival_action.split(":",1)[1])
        jump arrival_place
    $ arrival_question_person = arrival_location
    call arrival_interview
    jump arrival_place

label arrival_inn:
    if arrival_inn_room not in VILLAGE_INTERIORS["inn"]["rooms"]:
        $ arrival_inn_room = "reception"
    if "inn:"+arrival_inn_room not in village_interiors_seen:
        $ village_interiors_seen.append("inn:"+arrival_inn_room)
    call scene_present(village_inn_spec())
    call screen arrival_interior
    $ inn_action = _return
    if inn_action == "outside":
        jump arrival_place
    if inn_action == "map":
        jump arrival_roam
    if inn_action == "look":
        call source_lines(VILLAGE_INTERIORS["inn"]["rooms"][arrival_inn_room]["look"],"V_INN_LOOK_"+arrival_inn_room)
        jump arrival_inn
    if inn_action.startswith("room:"):
        $ arrival_inn_room = inn_action.split(":",1)[1]
        jump arrival_inn
    if inn_action.startswith("local:"):
        call village_contact(inn_action.split(":",1)[1])
        jump arrival_inn
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
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#0b172733")
    add arrival_actor+" interview_neutral" at portrait_question id "topic_actor"
    vbox:
        xpos 360 ypos 140 spacing 5
        for q in ARRIVAL["questions"][arrival_question_person]:
            use topic_banner(q["q"],Return(q["id"]),q["id"] in arrival_seen,enabled=ready)
        use topic_banner("대화 마치기",Return("back"),enabled=ready)

screen arrival_interior():
    modal True
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    if arrival_inn_room == "reception":
        imagebutton:
            id "inn_host_activity"
            xpos 590 ypos 180
            idle Transform("granny inn_activity",size=(190,330),fit="contain")
            hover Transform("granny inn_activity",size=(190,330),fit="contain",alpha=.85)
            sensitive ready action Return("talk")
        # Exact foreground slice of the same background hides the legs behind the counter.
        add Crop((380,375,540,160),Transform("assets/front.png",size=(1280,720))) xpos 380 ypos 375 id "inn_counter_foreground"
        frame:
            xpos 532 ypos 548 padding (12,8) background Solid("#172225de")
            text "잔을 닦는 여관 주인 · 말 걸기" size 20 color "#f3e8cd"
        button:
            xpos 943 ypos 185 xsize 224 ysize 325
            background None hover_background Solid("#f4d9a411")
            sensitive ready action Return("room:lounge")
        button:
            xpos 70 ypos 192 xsize 135 ysize 328
            background None hover_background Solid("#f4d9a411")
            sensitive ready action Return("outside")
    else:
        for guest in village_inn_guests():
            imagebutton:
                id ("inn_guest_"+guest["id"])
                xpos guest["x"] ypos guest["y"]
                idle Transform(guest["id"]+" "+guest["pose"],size=(guest["width"],guest["height"]),fit="contain")
                hover Transform(guest["id"]+" "+guest["pose"],size=(guest["width"],guest["height"]),fit="contain",alpha=.85)
                sensitive ready action Return("local:"+guest["id"])
            frame:
                xpos (guest["x"]-30) ypos 545 padding (12,8) background Solid("#172225de")
                text guest["caption"] size 18 color "#f3e8cd"
    use inn_room_navigation(ready)

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

screen arrival_place():
    modal True
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    for local in village_outdoor_people(arrival_location):
        imagebutton:
            xpos local["x"] ypos local["y"]
            idle Transform(local["id"]+(" activity" if local.get("activity_pose") else " world"),size=(local["width"],local["height"]),fit="contain")
            hover Transform(local["id"]+(" activity" if local.get("activity_pose") else " world"),size=(local["width"],local["height"]),fit="contain",alpha=.86)
            sensitive ready action Return("local:"+local["id"])
        frame:
            xpos (local["x"]-12) ypos (local["y"]+local["height"]+3)
            padding (9,5) background Solid("#172225da")
            vbox:
                spacing 3
                text local["public_name"] size 17 color "#f3e7ce"
                text local["activity"] size 14 color "#c6d0c9"
    $ resident = village_arrival_resident(arrival_location)
    if resident:
        $ person = SOURCE_ALIAS.get(resident,resident)
        imagebutton:
            xpos 740 ypos (105 if person=="bami" else 310)
            idle Transform(person+" world",size=(170,225),fit="contain")
            hover Transform(person+" world",size=(170,225),fit="contain",alpha=.85)
            sensitive ready action Return("talk")
    elif not village_outdoor_people(arrival_location):
        text "주민은 자리를 비웠다." xpos 685 ypos 555 size 21 color "#f3e7ce"
    if arrival_location == "fountain":
        button:
            xpos 380 ypos 155 xsize 190 ysize 315
            background None hover_background None padding (0,0)
            sensitive ready action Return("stone")
    add Solid("#172225f2",xsize=1280,ysize=118) ypos 602
    add Solid("#bca579",xsize=1232,ysize=1) xpos 24 ypos 602
    if village_optional_people(arrival_location):
        textbutton ("주변 둘러보기 · %d"%len(village_optional_people(arrival_location))):
            xpos 40 ypos 612 xsize 280 ysize 64
            background None hover_background Solid("#344743") text_size 23
            sensitive ready action Return("nearby")
    textbutton "거리 살펴보기":
        xpos 345 ypos 612 xsize 245 ysize 64
        background None hover_background Solid("#344743") text_size 23
        sensitive ready action Return("look")
    hbox:
        xpos 620 ypos 612 spacing 18
        textbutton "지도 · 이동하기" sensitive ready action Return("map") xsize 250 ysize 64 background Solid("#dfd2af") text_color "#21302e" hover_background Solid("#f0e4c5") text_size 23
        if arrival_location == "inn":
            textbutton "여관에 들어가기" sensitive ready action Return("stay") text_size 23
    text "거리의 주민을 눌러 말 걸기" xpos 58 ypos 685 size 16 color "#aab8b0"

screen arrival_stone_glow():
    zorder 10
    add Solid("#8bdfca18") at arrival_glimmer
