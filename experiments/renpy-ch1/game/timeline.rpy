# Public daily routines and observed conversations, separate from the case snapshot.
default village_minutes = 1050
default village_time_events = []
default village_observations = []
default village_trust = {}
default village_trust_events = []
default village_hearing_active = False
default village_hearing_person = None

init 25 python:
    TIMELINE = json.load(renpy.file("village-state.json"))

    def village_relationship(key,people,amount):
        if key in store.village_trust_events:return
        store.village_trust_events.append(key)
        for person in people:
            if person in TIMELINE["voters"]:
                store.village_trust[person]=store.village_trust.get(person,-1)+amount

    def village_proof_support():
        allies={1:["nabi","buri"],3:["nabi","buri"],7:["bami","doto"],8:["neoul","karo"]}
        if store.source_group=="meet":
            village_relationship("proof_"+str(store.source_phase),allies.get(store.source_phase,[]),1)
            if store.source_phase==7:village_relationship("clock_witness",["bami"],1)

    def village_apply_votes(votes):
        for person,vote in votes.items():
            canonical=SOURCE_ALIAS.get(person,person)
            store.source_votes[person]=("기권" if store.source_group=="meet" and vote=="seryeon" and store.village_trust.get(canonical,-1)<2 else vote)

    def village_vote_line(person,text,meta):
        canonical=SOURCE_ALIAS.get(person,person)
        if store.source_group=="meet" and meta.get("votes",{}).get(person)=="seryeon" and store.village_trust.get(canonical,-1)<2:
            return TIMELINE["hesitant_votes"].get(canonical,text)
        return text

    def village_supporters():
        return [p for p in TIMELINE["voters"] if store.village_trust.get(p,-1)>=2 or p in getattr(store,"council_confirmed_support",[])]

    def village_update_votes():
        store.source_votes={("geokkuri" if p=="bami" else "wanggu" if p=="neoul" else p):("seryeon" if p in village_supporters() else "기권") for p in TIMELINE["voters"]}

    def village_clock():
        day,minute=divmod(store.village_minutes,1440)
        return ("첫날" if day==0 else "다음 날")+" %02d:%02d"%(minute//60,minute%60)

    def village_advance_evening(minutes):
        # Optional evening exploration does not silently skip the night's lodging.
        store.village_minutes=min(TIMELINE["evening_limit"],
            store.village_minutes+max(0,minutes))

    def village_event(key):
        if key in store.village_time_events:return
        store.village_time_events.append(key)
        event=TIMELINE["events"].get(key,{})
        if "at" in event:store.village_minutes=max(store.village_minutes,event["at"])
        elif store.village_minutes<1440:village_advance_evening(event.get("duration",5))

    def village_round_time():
        values=TIMELINE["round_times"][store.source_group]
        village_event("round_"+store.source_group+str(store.source_phase))
        store.village_minutes=max(store.village_minutes,values[min(store.source_phase,len(values)-1)])
        return village_clock()+" · 정오 마차까지 %d분"%max(0,2160-store.village_minutes)

    def village_progress():
        if all(k in store.source_inventory for k in ("C01","C02","C03","C09","C12")):
            village_event("first_hypothesis")
        if store.source_found:village_event("somsom_found")
        if store.source_found and all(k in store.source_inventory for k in ("C06","C07","C08","C13")):
            village_event("clock_reconstruction")

    def village_observe(person):
        person=SOURCE_ALIAS.get(person,person)
        if person not in CAST:return
        entry=dict(person=person,minute=store.village_minutes,place=store.place)
        if not store.village_observations or store.village_observations[-1]!=entry:
            store.village_observations.append(entry)

    def village_last_seen(person):
        return next((x for x in reversed(store.village_observations) if x["person"]==person),None)

    def village_arrival_resident(location):
        person=ARRIVAL_PEOPLE.get(location)
        if not person:return None
        closing=TIMELINE["residents"][SOURCE_ALIAS.get(person,person)].get("evening_until",1440)
        return person if store.village_minutes<closing else None

    def village_residents(location):
        people={key:[p[0] for p in value] for key,value in SOURCE_EP["PPL"].items()}
        if store.source_found:
            people["dining"]=["seryeon","nabi","buri"]
            people["kitchen"]=[]
            people["bed13"]=["innma"]
        if store.source_found and "C08" in store.source_inventory:
            people["dotoroom"]=[]
            people["hall"]=["geokkuri","doto"]
        if "T_se4" in store.source_seen:
            people["dining"]=[p for p in people["dining"] if p!="seryeon"]
            people["front"]=["wanggu","seryeon"]
        return people.get(location,[])

    def village_resident_points(location):
        people=village_residents(location)
        positions=[1030] if location=="bed13" else [690] if len(people)==1 else [690,910] if len(people)==2 else [470,690,910]
        return [dict(id=p,x=positions[i],y=80 if p=="geokkuri" else 245) for i,p in enumerate(people)]

    def village_topic_available(question):
        rules=TIMELINE["topic_rules"].get(question["id"],{})
        return (all(k in store.source_inventory for k in rules.get("evidence",[]))
            and all(k in store.source_seen for k in rules.get("seen",[]))
            and all(k in store.source_flags for k in rules.get("flags",[]))
            and (not rules.get("found") or store.source_found))

    def village_question_variant(question):
        for index,variant in enumerate(TIMELINE["dialogue_variants"]):
            if variant["question"]!=question["id"]:continue
            if not all(k in store.source_inventory for k in variant.get("evidence",[])):continue
            if not all(k in store.source_seen for k in variant.get("seen",[])):continue
            if not all(k in store.source_flags for k in variant.get("flags",[])):continue
            if variant.get("found") and not store.source_found:continue
            return index,variant
        return None

    def village_question_revision(question):
        match=village_question_variant(question)
        return "variant:%d"%match[0] if match else "base"

    def village_question_done(question):
        return (question["id"] in store.source_seen and
            store.source_question_revisions.get(question["id"],"base")==village_question_revision(question))

    def village_question_new(question):
        return question["id"] in store.source_seen and not village_question_done(question)

    def village_question_lines(question):
        match=village_question_variant(question)
        if match:
            variant=match[1]
            return variant["lines"]+arrival_question_lines(question)[variant.get("tail_from",0):]
        return arrival_question_lines(question)

screen village_timetable():
    modal True
    zorder 80
    add Solid("#100c09eb")
    frame:
        xpos 65 ypos 95 xsize 1150 ysize 550
        fixed:
            text "주민 수첩 · "+village_clock() size 29 color "#ffdc91"
            text "직접 만난 시각과 장소를 기록한다. 숨겨진 행적은 아직 알 수 없다." ypos 43 size 18 color "#c6b699"
            viewport:
                id "resident_rows"
                xpos 0 ypos 78 xsize 1102 ysize 365
                mousewheel True draggable True
                scrollbars "vertical" style_prefix "resident"
                vbox:
                    spacing 9 xfill True
                    for person,spec in TIMELINE["residents"].items():
                        $ observation=village_last_seen(person)
                        frame:
                            xfill True padding (8,10)
                            background Solid("#30261f77")
                            hbox:
                                spacing 16
                                if observation:
                                    add Transform(person+" avatar_neutral",size=(34,34),fit="contain")
                                    text NAMES[person] size 21 xsize 100
                                    vbox:
                                        spacing 5 xsize 380
                                        text (("첫날" if observation["minute"]<1440 else "다음 날")+" %02d:%02d"%((observation["minute"]%1440)//60,observation["minute"]%60)) size 18 color "#f8d994"
                                        text observation["place"] size 18 xsize 380
                                    text spec["public_purpose"] size 17 color "#c6b699" xsize 460
                                else:
                                    text "?" size 23 xsize 34
                                    text "아직 만나지 못했다" size 18 color "#91877a"
            textbutton "닫기" xpos 920 ypos 463 action Hide("village_timetable")

style resident_vscrollbar is vscrollbar:
    xsize 14
    base_bar Solid("#4f4034")
    thumb Solid("#b39060",xsize=14,ysize=42)
    thumb_shadow None

label village_support_hearing:
    $ village_hearing_active = True
    $ village_update_votes()
    while len(village_supporters()) < 4:
        $ village_support_choices = [dict(label=source_name(p),key=p) for p in TIMELINE["voters"] if p not in village_supporters()]+[dict(label="다른 사람의 말을 듣는다",key="listen"),dict(label="다시 조사한다",key="return")]
        call screen source_choice("아직 확신하지 못한 주민 · 누구의 걱정부터 들을까?",village_support_choices)
        $ village_hearing_person = _return["key"]
        if village_hearing_person == "return":
            $ village_hearing_active,village_hearing_person = False,None
            return "investigate"
        elif village_hearing_person == "listen":
            $ council_support_listens += 1
            if council_support_listens >= 2:
                call source_lines([["wanggu","지목에 동의한 사람이 부족합니다. 지금은 결정을 미루겠습니다."],["seryeon","저도 떠나야 합니다. 아직 결정 못 하신 거죠?"],["det1","아빠, 누가 왜 망설이는지부터 다시 듣자."]],"V_SUPPORT_ADVERSE")
                $ village_hearing_active,village_hearing_person = False,None
                $ council_support_listens = 0
                if "support_adverse" not in council_history:
                    $ council_history.append("support_adverse")
                return "investigate"
            call source_lines([["wanggu","다른 의견은 없습니까? 단정하고 싶지 않은 분들도 말해 주십시오."]],"V_SUPPORT_LISTEN")
        else:
            $ village_objection = TIMELINE["support"][village_hearing_person]
            call source_lines([[village_hearing_person,village_objection["ask"]]],"V_SUPPORT_ASK")
            call screen source_evidence(present=True)
            if _return == "cancel":
                pass
            elif council_confirm_support(village_hearing_person,_return):
                call source_lines([[village_hearing_person,village_objection["ok"]]],"V_SUPPORT_OK")
                $ village_update_votes()
            else:
                call source_lines([[village_hearing_person,village_objection["wrong"]]],"V_SUPPORT_RETRY")
    $ village_hearing_active,village_hearing_person = False,None
    return "supported"
