# Optional everyday encounters with recurring characters from the next episodes.
# Their private motives and future cases never enter the chapter-one proof data.
default village_people_met = []
default village_people_topics = []
default village_people_revisions = {}
default village_people_trust = {}
default village_places_seen = []

init 30 python:
    VILLAGE_PEOPLE = json.load(renpy.file("village-residents.json"))

    def village_contact_name(person):
        spec=VILLAGE_PEOPLE["profiles"][person]
        return spec["name"] if person in store.village_people_met else spec["public_name"]

    def village_outdoor_people(location):
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
        if person not in village_people_met:
            $ village_people_met.append(person)
        if village_contact_first_topic:
            $ village_people_topics.append(village_contact_topic["id"])
            $ village_people_trust[person] = village_people_trust.get(person,0)+1
            $ village_advance_evening(5)
        $ village_people_revisions[village_contact_topic["id"]] = village_contact_read_revision
        if not any(resident["id"]==person for resident in village_outdoor_people(arrival_location)):
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
