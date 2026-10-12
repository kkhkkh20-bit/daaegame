# Optional everyday encounters with recurring characters from the next episodes.
# Their private motives and future cases never enter the chapter-one proof data.
default village_people_met = []
default village_people_topics = []
default village_people_revisions = {}
default village_people_trust = {}
default village_places_seen = []
default village_people_memories = {}

init 30 python:
    VILLAGE_PEOPLE = json.load(renpy.file("village-residents.json"))

    def village_contact_name(person):
        spec=VILLAGE_PEOPLE["profiles"][person]
        return spec["name"] if person in store.village_people_met else spec["public_name"]

    def village_people_here(location):
        result=[]
        for route in VILLAGE_PEOPLE["routines"]:
            if route["place"]!=location or not route["start"]<=store.village_minutes<route["end"]:
                continue
            spec=VILLAGE_PEOPLE["profiles"][route["id"]]
            entry=dict(route,public_name=village_contact_name(route["id"]),
                met=route["id"] in store.village_people_met,role=spec["role"])
            if route["id"] in CAST:
                crop=CAST[route["id"]]["world"]["crop"]
                entry["width"]=round(route["height"]*crop[2]/float(crop[3]))
                entry["x"]+=round((route["width"]-entry["width"])/2.0)
            result.append(entry)
        return result

    def village_outdoor_people(location):
        # Additional draft residents use a list, so the background never fills with tiny actors.
        return [entry for entry in village_people_here(location) if not entry.get("list_only")]

    def village_optional_people(location):
        return [entry for entry in village_people_here(location) if entry.get("list_only")]

    def village_contact_record(person, topic, permission):
        info=topic.get("testimony")
        if not info:return
        if not hasattr(store,"village_testimonies"):store.village_testimonies={}
        previous=store.village_testimonies.get(info["id"],{})
        store.village_testimonies[info["id"]]=dict(info,speaker=person,
            heard_place=previous.get("heard_place",store.place),
            heard_minute=previous.get("heard_minute",store.village_minutes),
            permission=permission,verified=False)
        memories=dict(store.village_people_memories.get(person,{}))
        memories["public_statement"]= "permitted" if permission else "kept_private"
        store.village_people_memories[person]=memories

    def village_contact_topics(person):
        return [topic for topic in VILLAGE_PEOPLE["profiles"][person]["topics"]
            if topic.get("requires")!="stone" or store.arrival_stone]

    def village_contact_revision(topic):
        return "post_closed" if store.arrival_post_closed and topic["id"] in (
            "elder_inn","bodum_night","workshop_post") else "base"

    def village_contact_done(topic):
        return (topic["id"] in store.village_people_topics and
            store.village_people_revisions.get(topic["id"],"base")==village_contact_revision(topic))

    def village_contact_lines(person,topic):
        spec=VILLAGE_PEOPLE["profiles"][person]
        return spec["post_known"] if village_contact_revision(topic)=="post_closed" else topic["lines"]

    for person,spec in VILLAGE_PEOPLE["profiles"].items():
        NAMES[person]=spec["name"]
        SOURCE_CHARS[person]=DynamicCharacter("village_contact_name(%r)"%person,cb_who_id=person)
        TIMELINE["residents"][person]=dict(public_purpose=spec["public_purpose"])

label village_contact(person):
    $ village_contact_person = person
    $ source_camera,source_night,source_stage_person = "stage",None,person
    $ village_contact_memories = getattr(store,"council_relationship_memories",{}).get(person,[])
    if "private_statement_exposed" in village_contact_memories and "apologized_for_private_statement" not in village_contact_memories:
        call source_lines([[person,"다른 분께 제 말을 전하셨다면서요. 우리끼리만 알기로 하지 않았나요?"],["det0","먼저 여쭤야 했습니다."]],"V_PRIVATE_AFTER_"+person)
        call screen source_choice("대화를 이어갈까?",[
            dict(label="미안합니다. 다음에는 먼저 묻겠습니다",key="apologize"),
            dict(label="지금은 대화를 마친다",key="back")])
        if _return["key"]=="back":
            return
        $ council_relationship_memories[person].append("apologized_for_private_statement")
        $ village_people_memories.setdefault(person,{})["privacy_repair"]="apologized"
        call source_lines([[person,"알겠습니다. 다음에는 꼭 물어봐 주세요."]],"V_PRIVATE_REPAIR_"+person)
    while True:
        $ arrival_actor = person
        $ source_camera,source_night,source_stage_person = "stage",None,person
        window hide
        hide visitor
        call screen village_contact_questions(person)
        if _return == "back":
            return
        $ source_fx("select")
        $ village_contact_topic = _return
        $ village_contact_read_revision = village_contact_revision(village_contact_topic)
        $ village_contact_first_topic = village_contact_topic["id"] not in village_people_topics
        call source_lines(village_contact_lines(person,village_contact_topic),"V_PERSON_"+person+"_"+village_contact_topic["id"])
        if village_contact_topic.get("testimony"):
            call screen source_choice("이 말을 수첩에 남길까?",[
                dict(label="다른 사람에게 말해도 되는지 묻는다",key="ask"),
                dict(label="지금은 둘만 알고 있는다",key="private")])
            $ village_contact_permission = _return["key"]=="ask"
            if village_contact_permission:
                call source_lines([["det0","이 말씀을 다른 분께 전해도 괜찮겠습니까?"],[person,"네. 제가 한 말 그대로 전해 주세요."]],"V_PERMISSION_"+person)
            else:
                call source_lines([["det0","지금은 저희만 알고 있겠습니다."],[person,"고맙습니다."]],"V_PRIVATE_"+person)
            $ village_contact_record(person,village_contact_topic,village_contact_permission)
        if person not in village_people_met:
            $ village_people_met.append(person)
        if village_contact_first_topic:
            $ village_people_topics.append(village_contact_topic["id"])
            $ village_people_trust[person] = village_people_trust.get(person,0)+1
            $ village_advance_evening(5)
        $ village_people_revisions[village_contact_topic["id"]] = village_contact_read_revision
        if not any(resident["id"]==person for resident in village_people_here(arrival_location)):
            call source_lines(VILLAGE_PEOPLE["profiles"][person]["departure"],"V_PERSON_"+person+"_DEPARTURE")
            return

screen village_contact_questions(person):
    modal True
    default ready = False
    timer .25 action SetScreenVariable("ready",True)
    add person+" interview_neutral" at portrait_question id "topic_actor"
    vbox:
        xpos 360 ypos 116 spacing 5
        text village_contact_name(person) size 29 color "#ffdc91"
        for topic in village_contact_topics(person):
            $ changed = topic["id"] in village_people_topics and not village_contact_done(topic)
            use topic_banner(topic["title"]+(" · 새 이야기" if changed else ""),Return(topic),done=village_contact_done(topic),enabled=ready)
        use topic_banner("돌아가기",Return("back"),enabled=ready)


screen village_nearby_residents(location):
    modal True
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    add Solid("#100c09dd")
    frame:
        xpos 140 ypos 110 xsize 1000 ysize 550 padding (24,20)
        background Solid("#261e19ef")
        fixed:
            text (ARRIVAL_PLACES[location][0]+" · 근처 사람들") size 30 color "#ffdc91"
            text (village_clock()+" · 지금 이곳에서 만날 수 있다") ypos 43 size 18 color "#c6b699"
            viewport:
                xpos 0 ypos 82 xsize 950 ysize 360
                mousewheel True draggable True scrollbars "vertical" style_prefix "resident"
                vbox:
                    spacing 8
                    for entry in village_optional_people(location):
                        $ person=entry["id"]
                        button:
                            xsize 910 ysize 72 padding (12,8)
                            background Solid("#49362ccf") hover_background Solid("#6b5040ef")
                            sensitive ready action Return(person)
                            hbox:
                                spacing 18
                                add Transform(person+" avatar_neutral",size=(54,54),fit="contain")
                                vbox:
                                    spacing 5
                                    text entry["public_name"] size 23 color "#f3e7ce"
                                    text (entry["role"] if entry["met"] else "말 걸어 보기") size 16 color "#c6b699"
            textbutton "닫기" xpos 740 ypos 452 sensitive ready action Return("back") xsize 180 ysize 55
