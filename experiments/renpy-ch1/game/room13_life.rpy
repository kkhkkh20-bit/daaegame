# Shared rules for routines, discovery records and authored negotiation.
init 57 python:
    class R13QuestionBar(renpy.Displayable):
        def __init__(self,focused=False,**kwargs):
            super(R13QuestionBar,self).__init__(**kwargs)
            self.focused=focused
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height))
            out=renpy.Render(w,h)
            canvas=out.canvas()
            canvas.rect("#fff3d5" if self.focused else "#f0e9db",(0,0,w,h))
            canvas.rect("#dfb854" if self.focused else "#918671",(1,1,max(1,w-2),max(1,h-2)),3 if self.focused else 1)
            return out

    class R13InvestigationRing(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(56,56)
            out.canvas().circle("#f3ce81",(28,28),24,3)
            return out

    class R13ActionGlyph(renpy.Displayable):
        def __init__(self,kind,**kwargs):
            super(R13ActionGlyph,self).__init__(**kwargs)
            self.kind=kind
        def render(self,width,height,st,at):
            out=renpy.Render(58,58);c=out.canvas()
            if self.kind=="talk":
                c.circle("#687f99",(28,23),17)
                c.polygon("#687f99",[(14,32),(13,45),(29,34)])
                for x in (20,28,36):c.circle("#f8f1de",(x,23),2)
            elif self.kind=="inspect":
                c.circle("#b86550",(24,23),17,5)
                c.line("#b86550",(36,36),(49,49),7)
            elif self.kind=="present":
                c.rect("#bea057",(9,10,30,35),3)
                c.rect("#d4b665",(19,18,30,35))
                c.circle("#f7f0d8",(34,33),8)
                c.line("#f7f0d8",(27,46),(41,46),3)
            else:
                c.lines("#628966",False,[(10,41),(27,41),(27,19),(43,19)],5)
                c.lines("#628966",False,[(35,10),(45,19),(35,28)],5)
            return out

    R13_CORE_PEOPLE=set(R13_GREETING)
    R13_RESIDENTS=ROOM13["residents"]
    R13_DIRECTION={
        "entry:arrival":{"daram":"thinking","dad":"thinking"},
        "night1:knocking":{"daram":"thinking","nabi":"distressed"},
        "case:discovery:v3":{"daram":"distressed","dad":"distressed"},
        "case:sealing:v3":{"daram":"distressed","dad":"distressed"},
        "case:interview:opening:v3":{"daram":"distressed","dad":"thinking"},
        "trial:C2:done":{"daram":"distressed","dad":"thinking"},
        "trial:C4:done":{"dad":"thinking","granny":"distressed"},
        "reunion:held:question":{"mom":"distressed","dad":"distressed"},
        "reunion:free":{"mom":"distressed","daram":"distressed"},
        "rescue:child":{"daram":"distressed","dad":"thinking"},
        "finale:child_on_convoy":{"daram":"distressed","mom":"distressed"},
        "ending:E5:meal":{"daram":"expressive","mom":"neutral"},
        "ending:family":{"daram":"expressive"},
    }
    for person,spec in R13_RESIDENTS.items():
        R13_NAMES.setdefault(person,spec["name"])
        R13_GREETING.setdefault(person,"지금 하던 일을 마저 해야 해서요. 무슨 일입니까?")
        R13_CHARS.setdefault(person,Character(R13_NAMES[person],cb_who_id=person if person in CAST else None))

    def r13_daylight():
        # Period 3 is late evening, using the same authored evening art.
        return ("morning","afternoon","evening")[min(2,int((store.room13 or {}).get("period",0)))]

    def r13_scene_identity(bg,title,mood):
        state=store.room13 or {}
        return (bg,title,mood,r13_daylight(),state.get("case_state"))

    def r13_art_path(group,daylight=None):
        return "assets/room13-pixel-%s-%s.webp"%(group,daylight or r13_daylight())

    R13_PIXEL_LAYOUTS=json.load(renpy.file("assets/room13-pixel-layouts.json"))
    R13_CARRIAGE_IMAGE=json.load(renpy.file("assets/room13-cinematics.json")).get("carriage_file","assets/room13-pixel-carriage-morning.webp")

    def r13_atlas(path,index,columns=3,rows=2):
        spec=R13_PIXEL_LAYOUTS.get(path.rsplit("/",1)[-1])
        if spec:
            return Transform(Crop(tuple(spec["rects"][index]),path),size=(1280,720),nearest=True)
        raise ValueError("Missing pixel atlas metadata: " + path)

    def r13_background(key):
        world_location=r13_world_scene_location(key)
        if world_location:
            return DynamicDisplayable(r13_camera_background,world_location,r13_daylight())
        if key=="winter":
            return Transform(r13_art_path("gate"),size=(1280,720),nearest=True)
        if key=="winter_carriage":
            # Empty interior: Dad is the viewpoint and is never drawn.
            return Transform("assets/room13-pixel-carriage-empty-winter.webp",size=(1280,720),nearest=True)
        if key=="village_overview":
            return Transform(r13_art_path("overview"),size=(1280,720),nearest=True)
        if key=="r13_altar":
            return Transform(r13_art_path("altar"),size=(1280,720),nearest=True)
        if key=="hall":
            after=store.room13 and store.room13["case_state"]=="occurred"
            return Transform(r13_art_path("hall-after" if after else "hall-before"),size=(1280,720),nearest=True)
        if key in ("front","kitchen","winter_passage","council"):
            index={"front":0,"kitchen":1,"winter_passage":2,"council":3}[key]
            return r13_atlas(r13_art_path("inn"),index,2,2)
        if key in ("winter_square","winter_post","winter_workshop"):
            index=("winter_square","winter_post","winter_workshop").index(key)
            return r13_atlas(r13_art_path("village"),index,2,2)
        if key=="guestroom":
            return Transform(r13_art_path("room-before"),size=(1280,720),nearest=True)
        if key=="room":
            after=store.room13 and store.room13["case_state"]=="occurred"
            return Transform(r13_art_path("room-after" if after else "room-before"),size=(1280,720),nearest=True)
        if key.startswith("r13_"):
            index=("clinic","school","store","greenhouse","facility","altar").index(key[4:])
            return r13_atlas(r13_art_path("locations"),index)
        raise ValueError("Missing Room13 pixel background: " + key)

    def r13_evidence_art(key):
        # Authored rectangles refer to the actual adopted artwork, never an old sheet.
        # Evidence illustrations stay fixed when the clock changes.
        # 0.18.59: a wide scene names its own crop (picture + native rect), so the
        # close-up matches the room the player actually searched.
        for location,layout in getattr(store,"R13_WORLD_LAYOUTS",{}).items():
            crop=layout.get("evidence",{}).get(key)
            if crop:
                return Crop(tuple(crop["rect"]),crop["file"])
        for name,spec in R13_PIXEL_LAYOUTS.items():
            rect=spec.get("evidence",{}).get(key)
            if rect:
                return Crop(tuple(rect),"assets/"+name)
        return None

    # Optional neighbours follow named errands and home/work time, rather than
    # gathering in the square every day. Story-critical locations and emergency
    # overrides below remain authoritative. "home" is an existing private-home
    # rest period, not an invisible resident still counted in the field.
    R13_WEEKLY_ROUTINES = {
        "resident_tori": [
            ("square","inn","home"),("square","inn","home"),("home","inn","home"),
            ("workshop","inn","home"),("square","home","home"),("square","inn","home"),("home","square","inn")],
        "resident_yeoni": [
            ("home","workshop","home"),("square","inn","home"),("home","inn","home"),
            ("workshop","store","home"),("home","workshop","home"),("store","inn","home"),("home","school","home")],
        "resident_kongi": [
            ("store","post","home"),("store","post","home"),("square","post","home"),
            ("store","post","home"),("store","post","home"),("square","post","home"),("store","post","home")],
        "resident_seol": [
            ("tower","home","home"),("tower","tower","home"),("tower","home","home"),
            ("tower","home","home"),("tower","tower","home"),("tower","home","home"),("tower","home","home")],
        "resident_ppul": [
            ("post","post","home"),("square","post","home"),("post","post","home"),
            ("post","post","home"),("square","post","home"),("post","post","home"),("square","post","home")],
        "resident_sling": [
            ("post","post","post"),("post","square","post"),("post","post","post"),
            ("post","square","post"),("post","post","post"),("post","square","post"),("post","post","post")],
        "resident_piko": [
            ("home","square","home"),("home","square","home"),("home","square","home"),
            ("home","square","home"),("home","square","home"),("square","square","home"),("home","square","home")],
        "resident_somi": [
            ("home","home","home"),("home","square","home"),("home","home","home"),
            ("home","square","home"),("home","home","home"),("home","square","home"),("home","square","home")],
    }

    def r13_resident_where(person):
        if person not in R13_RESIDENTS:return None
        s=store.room13
        if person=="resident_piko" and s["day"]>=R13_WEEK2_DAY:return "clinic"
        if person=="resident_badook" and s["day"]>=R13_WEEK2_DAY and r13_has("patient_transport"):return "school"
        if s["day"]>=r13_tl(11) and r13_has("shelter_ready") and person in ("resident_tori","resident_yeoni","resident_kongi","resident_somi","resident_musoe"):
            return "school"
        where=R13_WEEKLY_ROUTINES.get(person,R13_RESIDENTS[person]["weekly_locations"])[(s["day"]-1)%7][min(s["period"],2)]
        return "square" if person=="resident_piko" and s.get("location")=="square" and s.get("offers",{}).get("r13_w1c_portrait")==dict(day=s["day"],period=s["period"],location="square") else {"home":None,"library":"post","lowroad":"gate","tower":"square"}.get(where,where)

    def r13_activity_text(person):
        if person in R13_CALENDAR:return r13_calendar_activity(person)
        if person in R13_RESIDENTS:return R13_RESIDENTS[person]["activity"]
        return ""

    def r13_note_encounter(person):
        n=winter_copy.deepcopy(store.room13)
        entry=dict(person=person,day=n["day"],period=n["period"],place=n["location"])
        if entry not in n["encounters"]:n["encounters"].append(entry)
        store.room13=n

    def r13_note_topics(person):
        return [ROOM13["topics"][k]["title"] for k in store.room13["read_topics"] if k in ROOM13["topics"] and ROOM13["topics"][k]["npc"]==person]

    def r13_object_visible(spec):
        s=store.room13
        return (all(r13_has(k) for k in spec.get("need",[])) and
            (not spec.get("case") or spec["case"]==s["case_state"]))

label r13_topic_choice(key):
    if key=="w2_erased":
        call r13_lines([("resident_seori","회복 기록의 그 줄은 제가 지웠습니다. 환자가 다시 나빠졌으니 회복이라고 쓰면 안 된다고 할머니가 그러셨죠."),("dad","잠깐이라도 나아진 사실까지 없어진 건 아니잖습니까."),("resident_seori","압니다. 하지만 원본을 내놓으면 사람들이 제가 한 검사도 전부 다시 따지려 들 겁니다.")],"negotiation:erased:start")
        $ r13_speaker("resident_seori","neutral")
        menu:
            "기록을 고치는 일에 어디까지 책임을 지겠습니까?"
            "서명은 두고, 사실과 지시를 나눠 주세요":
                call r13_lines([("resident_seori","결국 제 책임을 없애 주겠다는 말은 아니군요."),("dad","책임까지 없던 일로 만들어 버리면 이 기록도 믿을 수 없게 됩니다."),("resident_seori","……가족에게는 제가 먼저 말하겠습니다. 고치기 전에 베껴 둔 기록에는 할머니가 확인한 흔적도 남아 있습니다.")],"negotiation:erased:accepted")
                $ r13_flag("seori_responsibility_accepted")
                return True
            "서명 부분만 잘라 내면 서로 편할 겁니다":
                call r13_lines([("resident_seori","누가 적었는지도 모르는 베낀 종이를 내밀자는 겁니까?"),("dad","검사원님을 보호하려는 뜻입니다."),("resident_seori","서명을 잘라 내는 건 기록을 또 한 번 지우는 일입니다. 다른 방법을 찾아 주십시오.")],"negotiation:erased:cut")
                return False
            "지금 서명하지 않으면 한패로 알리겠습니다":
                call r13_lines([("resident_seori","제 잘못은 기록에 남기겠습니다. 하지만 협박에 못 이겨 한 말로 만들어 놓고, 그 말을 믿어 달라고 하실 겁니까?"),(None,"검사원이 말없이 서류를 접었다. 언성을 높인다고 받아 낼 수 있는 서명이 아니었다.")],"negotiation:erased:threat")
                $ r13_flag("seori_threatened")
                return False
            "원본을 더 확인한 뒤 이야기하겠습니다":
                return False
    if key=="w2_eunho":
        call r13_lines(ROOM13["topics"][key]["lines"],"negotiation:supplies:opening", binding_route="dynamic:086")
        $ r13_speaker("resident_eunho","neutral")
        menu:
            "창고를 열 조건을 어떻게 정할까?"
            "모두 같은 기준으로 수량과 받는 집을 적는다":
                call r13_lines([("resident_eunho","우리 창고 물건을 다른 집보다 더 빼놓으라는 뜻은 아니구려."),("dad","적어도 사장님 댁만 굶기자는 약속은 아닙니다. 갚을 몫도 공동 기록에 남기겠습니다."),("resident_eunho","서리가 창고 수량을 확인하면 물건을 내놓겠습니다. 빈 자루도 함께 세어야 합니다.")],"negotiation:supplies:agreement")
                return True
            "위기 뒤 매입가로 전부 갚겠다고 약속한다":
                call r13_lines([("resident_eunho","어느 돈으로 말입니까? 봄이 오면 이 마을을 떠나실 분 아닙니까."),("dad","갚을 몫은 기록으로 남기겠습니다."),("resident_eunho","빚진 사람 이름만 적힌 종이는 이미 많습니다. 오늘 누구 몫이 남는지부터 따져 봅시다.")],"negotiation:supplies:unfunded")
                return False
            "먼저 내놓으면 주민들이 편이 될 겁니다":
                call r13_lines([("resident_eunho","오늘은 내 편을 들어도, 내일 물건이 떨어지면 또 내 집 문을 두드릴 거요. 나한테 필요한 건 박수가 아니라 어디까지 약속하느냐입니다.")],"negotiation:supplies:popularity")
                return False
            "창고의 실제 수량부터 살펴보고 다시 온다":
                return False
    return False
