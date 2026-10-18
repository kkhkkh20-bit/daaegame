# Direct scene interaction; activity/time rules remain in room13_rules.rpy.
init 61 python:
    # A separate borrowed room shares the intact room artwork, never its
    # investigation rewards or the crime-scene before/after state.
    ROOM13["objects"]["guestroom"]={
        key:dict(rect=list(ROOM13["objects"]["room13"][key]["rect"]),text=text,need=[],give=[],flags=[])
        for key,text in {
            "bed":"나비가 깨끗한 이불을 펴 두었다. 오늘부터 쓸 임시 객실의 침대다.",
            "window":"닫힌 창 너머로 여관 처마에 쌓인 눈이 보인다.",
            "boxes":"옆방에서 옮겨 온 가족의 짐이다. 가방을 침대 곁에 놓았다.",
            "cup":"따뜻한 물을 담은 컵이 놓여 있다.",
        }.items()
    }
    R13_CONTEXT_ACTIVITIES={
        ("workshop","plans"):("map",),
        # The shelf (booth) now lives inside the gate-document popup; the visit
        # request sits on the guard post's child-handover notice instead.
        ("gate","rules"):("interview",),
        ("room13","floor"):("wax",),
        ("inn","keys"):("protect_bami",),
        ("post","notice"):("custody_draft","w2_spring_proof","w2_plan_proof"),
        ("square","cart"):("recovery",),
        ("square","lamp"):("warning","w2_reply"),
        ("greenhouse","signal"):("w2_secure_contact","w2_meet"),
        ("clinic","bed"):("w2_recovery",),
        ("store","ledger"):("w2_archive",),
        ("school","desks"):("w2_shelter",),
        ("store","sacks"):("w2_supplies",),
        ("workshop","tools"):("w2_operators",),
        ("school","blankets"):("w2_transport","w2_nubi_safety"),
        ("workshop","axle"):("w2_measure1","w2_measure2"),
        ("greenhouse","tools"):("w2_original",),
        ("gate","road"):("w2_route","w2_escape","w2_break_tail"),
        ("facility","notice"):("w2_scout","w2_rescue_order"),
        ("facility","sidegate"):("w2_rescue_laundry","w2_rescue_maintenance"),
        ("school","lessons"):("w2_protect_seori",),
        ("clinic","notes"):("case_compare",),
        ("passage","steps"):("passage_measure",),
    }
    R13_CONTEXT_WAIT={
        ("gate","bundles"):"마차 옆에서 눈을 털며 쉰다",
        ("square","cart"):"손수레 옆에서 바람이 잦아들기를 기다린다",
        ("inn","cups"):"접수대 옆에서 따뜻한 차를 마신다",
        ("dining","table"):"식탁에 앉아 식사를 마친다",
        ("kitchen","stove"):"화덕 곁에서 몸을 녹인다",
        ("post","cup"):"우편 접수대 옆에서 차를 마신다",
        ("workshop","wood"):"난로에 장작을 보태고 몸을 녹인다",
        ("room13","cup"):"방에서 차를 마시며 생각을 정리한다",
        ("clinic","bed"):"침상 곁에서 조용히 시간을 보낸다",
        ("school","stove"):"학교 난로 곁에서 몸을 녹인다",
        ("store","sacks"):"창고에서 운반할 짐을 정리하며 기다린다",
        ("facility","mug"):"접견실에서 다음 교대를 기다린다",
        ("greenhouse","watercan"):"도구를 정리하고 잠시 쉰다",
        ("altar","village_view"):"난간에서 마을을 바라보며 숨을 고른다",
    }
    R13_OBJECT_NAMES={
        "booth":"초소 선반", "rules":"아이를 넘길 때의 규칙", "ledger":"장부", "road":"마차와 고갯길",
        "bundles":"마차의 담요", "shovel":"삽", "crates":"채소 상자", "woodpile":"장작 더미",
        "desk":"접수대", "door":"출입문", "keys":"객실 열쇠", "register":"접수 장부",
        "knitting":"털실 바구니", "coats":"걸린 외투", "cups":"찻잔들", "stone":"광장의 돌",
        "offerings":"남겨 둔 물건", "lamp":"등과 점검함", "stall":"가판대", "cart":"손수레",
        "wood":"장작", "notice":"게시된 공고", "parcels":"우편물", "cup":"찻잔",
        "scarf":"목도리", "twine":"묶음 끈", "plans":"보수 도면", "axle":"작업대의 차축",
        "bolts":"부품 접시", "rag":"작업용 천", "wheel":"바퀴", "tools":"작업 도구",
        "bed":"침대", "window":"창문", "boxes":"여행 가방", "under":"침대 밑", "floor":"바닥 흔적",
        "books":"책장", "letters":"편지", "notebook":"공책", "coat":"코트", "sewing":"반짇고리",
        "socks":"양말", "bedside_books":"머리맡 책", "bread":"빵 그릇", "rail":"복도 난간",
        "towels":"접은 수건", "boots":"신발", "bucket":"청소 도구", "table":"식탁",
        "mittens":"말리는 장갑", "blankets":"담요", "breadboard":"빵 도마", "pot":"국솥",
        "steps":"통로의 계단", "handle":"안쪽 손잡이", "linen":"세탁물", "mop":"걸레",
        "baskets":"천 바구니", "notes":"진료 메모", "basin":"물대야", "bottles":"약병",
        "curtain":"가림막", "desks":"학교 책상", "stove":"난로", "lessons":"학습 공책",
        "firewood":"난방 장작", "sacks":"물자 자루", "scale":"저울", "burlap":"포장천",
        "cloth":"작업실의 천", "signal":"연락 표식", "pots":"화분", "watercan":"물뿌리개",
        "sidegate":"물건 들이는 문", "mug":"접견실의 잔", "valve":"제단 밸브", "supplies":"산 위의 물자",
        "village_view":"마을을 보는 난간", "approach":"산길 계단", "shelf":"찬장", "rear":"주방 뒷문",
        "vegetables":"손질할 채소", "flour":"밀가루", "dishes":"접시", "herbs":"말린 풀", "ladles":"국자",
    }
    def r13_choice_layout(person,pose,side):
        # Save-compatible hook: choices keep the existing central portrait.
        # Show/hide must not move or resize the interlocutor.
        return

    def r13_object_name(key):
        return R13_OBJECT_NAMES.get(key,key)

    def r13_object_actions(key):
        linked=R13_CONTEXT_ACTIVITIES.get((store.room13["location"],key),())
        return [(action,spec) for action,spec in r13_actions() if action in linked]

    def r13_context_wait(key):
        return R13_CONTEXT_WAIT.get((store.room13["location"],key))

    def r13_bed_available(key):
        if key!="bed" or not r13_has("lodging"):return False
        displaced=r13_has("family_room_unusable") or store.room13["case_state"]=="occurred"
        return store.room13["location"]==("guestroom" if displaced else "room13")

    def r13_actor_face_target(actor):
        spec=r13_acting_spec(actor["person"],actor["pose"])
        if not spec or not spec.get("head"):return None
        hx,hy,hw,hh=spec["head"]
        scale=float(actor["width"])/spec["crop"][2]
        x=max(0,int(actor["x"]+hx*scale));y=max(100,int(actor["y"]+hy*scale))
        right=min(r13_world_width(),int(actor["x"]+(hx+hw)*scale))
        bottom=min(720,int(actor["y"]+(hy+hh)*scale))
        if right<=x or bottom<=y:return None
        return (x,y,right-x,bottom-y)

    def r13_actor_nameplate(actor):
        face=r13_actor_face_target(actor) or tuple(actor["rect"])
        # A tail, tool or carried basket can extend the sprite far to one side.
        # Name the actual head, never the left edge of the full sprite crop.
        half_width=(sum(9 if ch==" " else 18 for ch in R13_NAMES[actor["person"]])+24)/2.0
        cx=min(r13_world_width()-8-half_width,max(8+half_width,face[0]+face[2]/2.0))
        return (int(cx),max(101,int(face[1])-36))

    def r13_actor_nameplates(actors):
        faces={actor["person"]:(r13_actor_face_target(actor) or tuple(actor["rect"])) for actor in actors}
        placed=[]
        # Group labels and the inn's fixed navigation must not cover participant names.
        group_ids={a.get("life_group") for a in actors if a.get("life_group")}
        reserved=[tuple(g["label_position"])+(R13_CONTROL["width"],r13_control_height()) for g in getattr(store,"R13_LIFE_GROUPS",[]) if g["id"] in group_ids and not g.get("member_conversation")]
        inn_nav=(r13_world_offset()+276,186,976,64) if group_ids and store.room13["location"]=="inn" else None
        def overlap(a,b):
            return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
        for actor in sorted(actors,key=lambda a:(faces[a["person"]][1],faces[a["person"]][0])):
            person=actor["person"];face=faces[person]
            cx,top=r13_actor_nameplate(actor)
            top=actor.get("nameplate_top",max(101,top-14))
            width=max(88,sum(9 if ch==" " else 18 for ch in R13_NAMES[person])+32)
            preferred=(int(cx-width/2),top,width,48)
            candidates=[]
            for dy in (0,-52,-104,52):
                for dx in (0,-32,32,-64,64):
                    candidates.append((max(8,min(r13_world_width()-8-width,preferred[0]+dx)),max(101,min(676,top+dy)),width,48))
            candidates.append((max(8,min(r13_world_width()-8-width,preferred[0])),min(676,face[1]+face[3]+6),width,48))
            def score(rect):
                blocked=sum(overlap(rect,f) for f in faces.values())
                blocked+=sum(overlap(rect,p["rect"]) for p in placed)
                blocked+=sum(overlap(rect,r) for r in reserved)
                if actor.get("life_group") and inn_nav:blocked+=overlap(rect,inn_nav)
                if r13_world_width()==1280:blocked+=overlap(rect,(1075,642,180,62))
                return blocked*10000+abs(rect[0]-preferred[0])+abs(rect[1]-preferred[1])*1.1
            rect=min(candidates,key=score)
            leader=None
            if rect[:2]!=preferred[:2]:
                above=rect[1]+rect[3]<=face[1]
                below=rect[1]>=face[1]+face[3]
                if above:
                    leader=((rect[0]+rect[2]/2,rect[1]+rect[3]),(face[0]+face[2]/2,face[1]-2))
                elif below:
                    leader=((rect[0]+rect[2]/2,rect[1]),(face[0]+face[2]/2,face[1]+face[3]+2))
                else:
                    left=rect[0]+rect[2]/2<face[0]+face[2]/2
                    leader=((rect[0]+rect[2] if left else rect[0],rect[1]+24),(face[0]-2 if left else face[0]+face[2]+2,face[1]+face[3]/2))
            placed.append(dict(person=person,rect=tuple(int(v) for v in rect),leader=leader))
        return placed

    class R13NameLeader(renpy.Displayable):
        def __init__(self,points,**kwargs):
            super(R13NameLeader,self).__init__(**kwargs)
            self.left=int(min(p[0] for p in points))-2
            self.top=int(min(p[1] for p in points))-2
            self.points=tuple((int(x)-self.left,int(y)-self.top) for x,y in points)
            self.width=max(p[0] for p in self.points)+3
            self.height=max(p[1] for p in self.points)+3
        def render(self,width,height,st,at):
            result=renpy.Render(self.width,self.height)
            result.canvas().line("#b79b68",self.points[0],self.points[1],2)
            return result

    def r13_actor_face_targets(actor):
        # Compatibility for inspection tools; actual buttons use the full
        # visible-alpha mask, never a face rectangle with prop holes removed.
        face=r13_actor_face_target(actor)
        return [face] if face else []

    def r13_overflow_people():
        visible={actor["person"] for actor in r13_stage_people()}
        return [person for person in r13_people() if person not in visible]

    # Every authored timed action keeps a physical interaction path.
    assert {key for keys in R13_CONTEXT_ACTIVITIES.values() for key in keys}==set(ROOM13["activities"])
    assert all(key in ROOM13["objects"].get(location,{}) for location,key in R13_CONTEXT_ACTIVITIES)

screen r13_object_context(key):
    modal True
    zorder 35
    style_prefix "r13"
    default ready=False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#0c202780")
    # The panel is as tall as its choices (0.18.22, owner: no empty box under one button).
    $ option_count=int(bool(r13_tool_available(key)))+len(r13_object_actions(key))+int(bool(r13_context_wait(key) and room13["period"]<3))+int(bool(r13_bed_available(key) or r13_bed_blocked_reason(key)))
    frame:
        xpos 650 ypos 248 xsize 560 padding (18,16) background R13ActionPanel()
        vbox:
            spacing 14
            text r13_object_name(key) size 29 color "#f6d18a"
            if option_count>3:
                viewport:
                    xsize 524 ysize 270 mousewheel True draggable True scrollbars "vertical"
                    use r13_object_context_options(key,ready)
            else:
                use r13_object_context_options(key,ready)
            textbutton "그만 살펴본다" style "r13_action_button" action Return(False) sensitive ready xsize 498 ysize 44

screen r13_object_context_options(key,ready):
    vbox:
        spacing 12
        if r13_tool_available(key):
            textbutton "돋보기로 자세히 살펴보기":
                style "r13_action_button" xsize 498 yminimum 58 text_size 22
                action Return(("tool",key)) sensitive ready
        for action,spec in r13_object_actions(key):
            textbutton (spec["title"]+"\n"+r13_learning_time_text(spec.get("cost",1),ending=action=="w2_escape")):
                style "r13_action_button" xsize 498 yminimum 58 text_size 22
                action Return(("activity",action)) sensitive ready and (room13["period"]<3 or not spec.get("cost",1))
        if r13_context_wait(key) and room13["period"]<3:
            textbutton (r13_context_wait(key)+"\n"+r13_learning_time_text(1)):
                style "r13_action_button" xsize 498 yminimum 58 text_size 22
                action Return(("wait",key)) sensitive ready
        if r13_bed_available(key):
            textbutton "침대에서 잠자기\n오늘 일정을 마치고 다음 날 아침으로":
                style "r13_action_button" xsize 498 yminimum 58 text_size 22
                action Return(("sleep",key)) sensitive ready
        elif r13_bed_blocked_reason(key):
            textbutton ("침대에서 잠자기\n"+r13_bed_blocked_reason(key)):
                style "r13_action_button" xsize 498 yminimum 58 text_size 22
                action NullAction() sensitive False

label r13_object_options(key):
    if not (r13_tool_available(key) or r13_object_actions(key) or (r13_context_wait(key) and room13["period"]<3) or r13_bed_available(key) or r13_bed_blocked_reason(key)):
        return None
    call screen r13_object_context(key)
    $ r13_context_choice=_return
    if not r13_context_choice:
        return None
    if r13_context_choice[0]=="tool":
        call r13_tool_inspect(key)
        return None
    if r13_context_choice[0]=="activity":
        $ r13_action=r13_context_choice[1]
        if r13_action not in [item[0] for item in r13_object_actions(key)]:
            return None
        if ROOM13["activities"][r13_action].get("cost",1) and room13["period"]>=3:
            return None
        if r13_action=="map":
            call r13_compare_first_plan
            if _return:
                $ r13_finish_action("map")
            return None
        call screen r13_confirm(ROOM13["activities"][r13_action]["title"]+"\n"+r13_learning_time_text(ROOM13["activities"][r13_action].get("cost",1),ending=r13_action=="w2_escape"))
        if _return:
            if ROOM13["activities"][r13_action].get("special"):
                call r13_special_activity(r13_action)
                if _return:
                    $ r13_finish_action(r13_action)
            else:
                call r13_lines(ROOM13["activities"][r13_action]["lines"],"activity:"+r13_action, binding_route="dynamic:081")
                $ r13_finish_action(r13_action)
    elif r13_context_choice[0]=="wait" and room13["period"]<3:
        call screen r13_confirm(r13_context_wait(key)+"\n"+r13_learning_time_text(1))
        if _return:
            $ r13_tick()
    elif r13_context_choice[0]=="sleep" and r13_bed_available(key):
        call r13_sleep_in_room
        return _return
    return None

label r13_sleep_in_room:
    if not r13_bed_available("bed"):
        return None
    call screen r13_confirm(r13_learning_sleep_text(),"자기","아직 할 일이 있다")
    if _return:
        if room13["day"]==R13_CASE_DAY and room13["case_state"]=="pending":
            $ r13_edit(period=2)
            return "case"
        if room13["day"]==1 and not r13_has("night1_seen"):
            call r13_first_night
        if room13["day"] in (2,3):
            call r13_poc_night_review from r13_poc_night_review_return
        $ r13_next_day()
        return "slept"
    return None

# Right-click no longer opens the menu; Esc and the explicit 옵션 button remain.
init 99 python:
    config.keymap["game_menu"] = [key for key in config.keymap["game_menu"] if key != "mouseup_3"]
