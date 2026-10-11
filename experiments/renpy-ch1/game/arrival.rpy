# Authored opening, kept separate from the captured chapter/source baseline.
default arrival_location = None
default arrival_met = []
default arrival_seen = []
default arrival_greeted = []
default arrival_post_closed = False
default arrival_stone = False

init 20 python:
    ARRIVAL = json.load(renpy.file("village-story.json"))
    ARRIVAL_PLACES = {
        "gate": ("마을 입구", "map-signpost.png", (155,435), "wanggu"),
        "fountain": ("광장", "map-plaza-fountain.png", (430,295), "buri"),
        "lane": ("지붕 아래 골목", "map-bench.png", (680,455), "geokkuri"),
        "post": ("우체국", "map-post-office.png", (740,215), None),
        "inn": ("겨울잠 여관", "map-inn.png", (990,330), "seryeon"),
    }
    ARRIVAL_PEOPLE = {"gate":"wanggu", "fountain":"buri", "lane":"geokkuri", "inn":"seryeon"}

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
    call source_scenes([ARRIVAL["scenes"]["carriage"], ARRIVAL["scenes"]["arrival"]])
    $ stage = "village"
    jump arrival_roam

label arrival_roam:
    $ stage = "village"
    $ source_camera, source_night, source_stage_person = "village",None,None
    $ place, clock_text = "작은 동물마을", "첫날 저녁 · 첫눈을 앞두고"
    window hide
    hide visitor
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("inn_friend")
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.18)
    call screen arrival_map
    $ arrival_location = _return
    if arrival_location == "post":
        call source_scenes([arrival_scene("post")])
        $ arrival_post_closed = True
        if "post" not in arrival_seen:
            $ arrival_seen.append("post")
        jump arrival_roam
    if arrival_location == "inn":
        call source_scenes([arrival_scene("inn")])
        if "inn" not in arrival_seen:
            $ arrival_seen.append("inn")
    jump arrival_place

label arrival_place:
    $ place, clock_text = ARRIVAL_PLACES[arrival_location][0], "첫날 저녁"
    $ source_camera,source_night,source_stage_person = "innentrance" if arrival_location=="inn" else "stage",None,None
    $ source_background = "plaza"
    window hide
    hide visitor
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("inn_friend")
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.18)
    call screen arrival_place
    $ arrival_action = _return
    if arrival_action == "map":
        jump arrival_roam
    if arrival_action in ("talk","stone"):
        $ arrival_key = "stone" if arrival_action=="stone" else "seryeon" if arrival_location=="inn" else arrival_location
        call source_scenes([arrival_scene(arrival_key)])
        if arrival_key not in arrival_seen:
            $ arrival_seen.append(arrival_key)
        $ arrival_person = "buri" if arrival_key=="stone" else ARRIVAL_PEOPLE[arrival_location]
        if arrival_person not in arrival_met:
            $ arrival_met.append(arrival_person)
        if arrival_key == "stone":
            $ arrival_stone = True
        jump arrival_place
    if arrival_action == "stay":
        if not arrival_post_closed:
            call source_scenes([ARRIVAL["scenes"]["inn_before_post"]])
            jump arrival_roam
        $ stage = "opening"
        call source_scenes([ARRIVAL["scenes"]["checkin"]])
        call source_scenes([sc for sc in SOURCE_EP["PRO"] if sc["sid"]=="P5"])
        call source_scenes([ARRIVAL["scenes"]["bedroom"]])
        call source_scenes(arrival_case())
        return

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
    add Transform("assets/map.png",size=(1280,720))
    add Solid("#24354444")
    use arrival_snow
    frame:
        xpos 28 ypos 115
        vbox:
            spacing 8
            text "어디로 갈까?" size 30 color "#ffdc91"
            text "만남은 발길 닿는 대로." size 19
    for key, spec in ARRIVAL_PLACES.items():
        button:
            xpos spec[2][0]-90 ypos spec[2][1]-100 xsize 205 ysize 185
            background None hover_background Solid("#ffdc9122")
            padding (0,0) sensitive ready action Return(key)
            fixed:
                add Transform("assets/"+spec[1],size=(170,125),fit="contain") xalign .5
                frame:
                    ypos 127 xalign .5 padding (12,8)
                    vbox:
                        text spec[0] size 22 xalign .5
                        if key=="post" and arrival_post_closed:
                            text "내일 아침 9시" size 16 color "#c6b699" xalign .5
                        elif key in arrival_seen:
                            text "다녀온 곳" size 16 color "#c6b699" xalign .5
    frame:
        xpos 32 ypos 633 padding (16,10)
        text ("우체국은 내일 연다. 오늘은 쉴 곳을 찾자." if arrival_post_closed else "건물을 눌러 이동 · 주민을 눌러 대화") size 21 color "#c6b699"

screen arrival_place():
    modal True
    default ready = False
    timer .35 action SetScreenVariable("ready",True)
    use arrival_snow
    $ person = SOURCE_ALIAS.get(ARRIVAL_PEOPLE[arrival_location],ARRIVAL_PEOPLE[arrival_location])
    imagebutton:
        xpos 720 ypos (105 if person=="bami" else 245)
        idle Transform(person+" world",size=(225,290),fit="contain")
        hover Transform(person+" world",size=(225,290),fit="contain",alpha=.85)
        sensitive ready action Return("talk")
    if arrival_location == "fountain":
        frame:
            xpos 385 ypos 310 padding (14,14)
            vbox:
                text "◆" size 62 color "#a6dad7" at arrival_glimmer
                text "작은 등" size 16 color "#c6b699"
        button:
            xpos 365 ypos 285 xsize 130 ysize 155
            background None hover_background None padding (0,0)
            sensitive ready action Return("stone")
    hbox:
        xpos 620 ypos 612 spacing 18
        imagebutton:
            idle Transform("assets/move.png",size=(64,64))
            sensitive ready action Return("map")
        textbutton "마을 지도" sensitive ready action Return("map")
        if arrival_location == "inn":
            textbutton "방을 묻는다" sensitive ready action Return("stay")

screen arrival_stone_glow():
    zorder 10
    add Solid("#8bdfca22")
    text "◆" xpos 385 ypos 305 size 80 color "#c8fff0" at arrival_glimmer
