default r13_present_origin = "topics"
default r13_inspection_location = None
# Separate save state: old winter saves resume their original labels unchanged.
default room13_mode = False
default room13 = None
default r13_target = None
default r13_choice = None
default r13_item = None
default r13_topic = None
default r13_action = None
default r13_claim = None
default r13_packet = None
default r13_index = 0
default r13_camera = "stage"
default r13_fast_read = False
default r13_scene_key = None
default persistent.room13_read = []
default persistent.room13_knowledge = []
default persistent.room13_knowledge_revision = None
default persistent.room13_previous_knowledge = {}
default persistent.room13_opening_seen = False

init 55 python:
    import hashlib as r13_hashlib
    ROOM13 = json.load(renpy.file("room13-content.json"))
    R13_PLACES = {
        "gate":("눈에 막힌 입구", "winter"),
        "square":("돌이 있는 광장", "winter_square"),
        "post":("우체국 입구", "winter_post"),
        "inn":("여관 접수대", "front"),
        "dining":("여관 식당", "council"),
        "hall":("여관 2층 복도", "hall"),
        "room13":("여관 2층 · 13호실", "room"),
        "guestroom":("여관 2층 · 임시 객실", "guestroom"),
        "kitchen":("여관 1층 · 주방", "kitchen"),
        "workshop":("수리점", "winter_workshop"),
        "passage":("13호 뒤 서비스 통로", "winter_passage"),
    }
    # Reuse actual art/face mappings; do not give a narrator the father's face.
    R13_NAMES = dict(WINTER_NAMES)
    R13_NAMES.update(resident_owlgp="부엉이 할아버지", resident_lamplighter="초롱",
        resident_tok="톡", resident_piko="피코", resident_seori="서리 검사원",
        resident_ppul="뿔이 촌장")
    R13_CHARS = {k:Character(v, cb_who_id=k if k in CAST else None) for k,v in R13_NAMES.items()}
    R13_CLAIMS = {c["id"]:c for c in ROOM13["claims"]}
    R13_PRESS = {
        "C1": "복도에서는 다른 출입을 보지 못했습니다. 옛 도면에 길이 있다는 것과 지금 사람이 통과할 수 있다는 것은 다릅니다.",
        "C2": "서로 다른 상처라고 해서 서로 다른 범인입니까? 촛대가 갈라진 때와 그 뒤 아이의 위치까지 확인해야 합니다.",
        "C3": "잠깐 안 보였다고 그 시간에 위층까지 다녀왔다고 할 수 있습니까? 길과 걸리는 시간도 확인해야 합니다.",
        "C4": "그 방에 간 적이 있다는 것과 죽였다는 것은 다릅니다. 도와주다 접촉했거나, 발견 뒤 묻은 흔적일 가능성은 없습니까?",
    }
    R13_GREETING = {
        "granny":"젖은 신발은 난로 옆에 두세요. 안쪽 장부는 내가 정리할게요.",
        "nabi":"할 말 있으면 여기서 해. 솥을 비울 수는 없어서.",
        "buri":"고칠 물건이면 내려놔요. 아니면 손 좀 비우고.",
        "karo":"축을 다시 묶고 있었어요. 고갯길은 아직 그대로예요.",
        "resident_owlgp":"발밑 조심하시오. 난간이 흔들려서 붙들어 놓는 중이오.",
        "resident_tok":"작은 부품 잃어버리면 다시 만들어야 해요. 발 옆을 봐 주세요.",
        "resident_lamplighter":"등 바로 아래에는 서 있지 마세요. 점검 중입니다.",
        "bami":"여기는 내 자리야. 밑에서 말하면 들려.",
        "doto":"지금은 장부 옮기는 중이에요. 짧게 말씀해 주세요.",
        "seryeon":"접수할 우편이 있으십니까?",
        "neoul":"어디서 확인한 일인지부터 말씀하십시오.",
    }

    def r13_new():
        return dict(campaign_id="room13_v1",version=3,story_revision=ROOM13["story_revision"],day=1,period=0,location="gate",
            kitchen_switch=False,passage_open=False,
            case_state="pending",victim_state="alive",daram_state="with_dad",
            granny_state="trusted",trial_result="pending",evidence=[],records={},
            flags=[],read_topics=[],done=[],checks={},encounters=[],resident_knowledge={},
            propositions=[],arguments={},log=[],trial_ended=False)

    def r13_prepare_history():
        revision=ROOM13["story_revision"]
        if persistent.room13_knowledge_revision!=revision:
            old=persistent.room13_knowledge_revision or "archived-v1-v2"
            archive=dict(persistent.room13_previous_knowledge)
            archive[old]=list(persistent.room13_knowledge)
            persistent.room13_previous_knowledge=archive
            persistent.room13_knowledge=[]
            persistent.room13_knowledge_revision=revision

    def r13_edit(**values):
        if "location" in values and values["location"]!=store.room13["location"]:
            store.r13_inspection_location=None
        n=winter_copy.deepcopy(store.room13)
        n.update(values)
        store.room13=n

    def r13_flag(*keys):
        n=winter_copy.deepcopy(store.room13)
        for key in keys:
            if key not in n["flags"]:n["flags"].append(key)
        store.room13=n

    def r13_has(key):
        return key in store.room13["flags"] or key in store.room13["evidence"]

    def r13_grant(keys,source):
        n=winter_copy.deepcopy(store.room13)
        added=[]
        for key in keys:
            if key not in n["evidence"]:
                n["evidence"].append(key)
                n["records"][key]=dict(day=n["day"],period=n["period"],source=source,place=n["location"])
                added.append(ROOM13["evidence"][key]["name"])
                if key not in persistent.room13_knowledge:
                    persistent.room13_knowledge=persistent.room13_knowledge+[key]
        store.room13=n
        if added:
            source_fx("found")
            renpy.notify("수첩에 기록: "+" · ".join(added))

    def r13_period():
        return ("오전","오후","저녁","늦은 저녁")[store.room13["period"]]

    def r13_clock():
        return "%d일째 · %s요일 · %s"%(store.room13["day"],("월","화","수","목","금","토","일")[(store.room13["day"]-1)%7],r13_period())

    def r13_time_target():
        return ("오후까지","저녁까지","늦은 저녁까지","내일")[store.room13["period"]]

    def r13_time_consequences(n):
        # Sleeping advances the world just as waiting or an activity does.
        if "bami_identity_leaked" in n["flags"] and "bami_protected" not in n["flags"]:
            if "bami_pressured" not in n["flags"]:n["flags"].append("bami_pressured")
        n["log"].append(dict(day=n["day"],period=n["period"],event="time_boundary"))

    def r13_tick():
        n=winter_copy.deepcopy(store.room13)
        n["period"]=min(3,n["period"]+1)
        r13_time_consequences(n)
        store.room13=n

    def r13_next_day():
        n=winter_copy.deepcopy(store.room13)
        n.update(day=n["day"]+1,period=0,location="inn")
        r13_time_consequences(n)
        store.room13=n

    def r13_available(spec):
        s=store.room13
        if not spec.get("day",[1,7])[0]<=s["day"]<=spec.get("day",[1,7])[1]:return False
        if spec.get("case") and spec["case"]!=s["case_state"]:return False
        if spec.get("period") and s["period"] not in spec["period"]:return False
        if any(r13_has(k) for k in spec.get("not_flags",[])):return False
        if any(s.get(k) not in values for k,values in spec.get("state",{}).items()):return False
        if any(s.get(k) in values for k,values in spec.get("not_state",{}).items()):return False
        return all(r13_has(k) for k in spec.get("need",[]))

    def r13_topics(person):
        return [(k,t) for k,t in ROOM13["topics"].items() if t["npc"]==person and r13_available(t)
            and (store.room13["daram_state"] in ("with_dad","rescued") or not any(who=="daram" for who,line in t["lines"]))
            and not (person=="buri" and r13_has("buri_refused") and k=="buri_records")]

    def r13_actions():
        return [(k,a) for k,a in ROOM13["activities"].items() if a["place"]==store.room13["location"]
            and k not in store.room13["done"] and r13_available(a) and r13_w2_actions_allowed(k)]

    def r13_finish_topic(key):
        t=ROOM13["topics"][key]
        r13_grant(t["give"],R13_NAMES.get(t["npc"],t["npc"])+"와 대화")
        r13_flag(*t["flags"])
        n=winter_copy.deepcopy(store.room13)
        if key not in n["read_topics"]:n["read_topics"].append(key)
        store.room13=n

    def r13_finish_action(key):
        if key in store.room13["done"]:return
        a=ROOM13["activities"][key]
        started_at=r13_abs_time()
        r13_grant(a["give"],a["title"])
        r13_flag(*a["flags"])
        n=winter_copy.deepcopy(store.room13)
        n["done"].append(key)
        store.room13=n
        if a.get("cost",1):r13_tick()
        r13_w2_action_done(key,started_at=started_at)

    def r13_mark(key,x,y):
        n=winter_copy.deepcopy(store.room13)
        n["checks"][n["location"]+":"+key]=(int(x),int(y))
        n["last_inspection"]=dict(place=n["location"],key=key,x=int(x),y=int(y))
        store.room13=n

    def r13_empty_click():
        x,y=renpy.get_mouse_pos()
        renpy.end_interaction(("empty",(int(x),int(y))))

    def r13_places():
        result=["gate","square","post","inn","workshop"]
        if r13_has("lodging"):result += ["dining","kitchen","hall","room13","clinic","school","store"]
        if r13_has("lodging") and (r13_has("family_room_unusable") or store.room13["case_state"]=="occurred"):result.append("guestroom")
        if store.room13.get("passage_open"):result.append("passage")
        if store.room13["day"]>=8:
            result += ["facility"]
            if r13_has("E19"):result.append("greenhouse")
        return result

    def r13_where(person):
        s=store.room13; p=min(s["period"],2)
        if s["day"]>=8:return r13_w2_where(person)
        if person=="resident_owlgp":
            if s["victim_state"]=="dead":return None
            return ("square","inn","dining")[p]
        if person=="granny":return None if s["granny_state"]=="detained" else "inn"
        if person=="nabi":return "dining"
        if person=="buri":return "workshop"
        if person=="karo":return "gate"
        if person=="seryeon":return "post" if s["day"]>=2 and p<2 else None
        if person=="resident_tok":return "workshop" if p<2 else "dining"
        if person=="resident_lamplighter":return ("workshop","square","gate")[p]
        if person=="doto":return "hall" if s["day"]>=5 else "square"
        if person=="bami":
            if s["case_state"]!="occurred":return None
            return "inn" if r13_has("bami_protected") else "hall" if p>0 else None
        if person=="neoul":return "gate" if s["case_state"]=="occurred" else None
        if person=="resident_seori":return "clinic"
        return r13_resident_where(person)

    def r13_people():
        return [p for p in R13_GREETING if r13_where(p)==store.room13["location"]]

    def r13_art(person,pose="world",speaking=False,entrance=False):
        if person not in CAST:raise ValueError("Missing pixel character: " + person)
        state=pose if pose in CAST[person] else "neutral"
        image_name=person+" "+state
        # Portrait icons remain still, including testimony/evidence thumbnails.
        if pose.startswith("avatar_"):return image_name
        return r13_motion_art(image_name,person,pose,speaking,entrance)

    def r13_close_art(person,pose="interview_neutral",height=840,speaking=False,entrance=False):
        spec=r13_close_spec(person,pose)
        art=Crop(tuple(spec["crop"]),spec["file"]) if spec else r13_art(person,pose,speaking,entrance)
        width,native_height=r13_close_geometry(person,pose)
        if not spec and person=="daram" and not r13_acting_spec(person,pose):
            art=Crop((0,20,width,native_height-20),art)
            native_height-=20
        scale=r13_close_scale(person,pose,height)
        return r13_pixel_scale(art,width*scale,native_height*scale,R13_CLOSE_PIXEL_GRID)

    def r13_close_y(person,height=840,top=110,pose="interview_neutral"):
        head=r13_close_head(person,pose)
        if head:
            scale=r13_close_scale(person,pose,height)
            y=int(top+20-head[1]*scale)
            if r13_close_spec(person,pose) and height<800:
                y=max(y,720-int(r13_close_geometry(person,pose)[1]*scale))
            return y
        return top-int(height*.40) if person=="bami" else top

    def r13_icon(key):
        who=ROOM13["evidence_sources"].get(key)
        if who:return r13_art(who,"avatar_neutral")
        detail=r13_evidence_art(key)
        if detail is not None:return detail
        return "assets/record.png" if ROOM13["evidence"][key]["kind"] in ("기록","관찰기록") else "assets/evidence.png"

    def r13_speaker(who,expression="neutral",pose=None):
        store.dialogue_speaker=None
        store.dialogue_expression=expression if who in CAST and "avatar_"+expression in CAST[who] else "neutral"
        store.r13_current_pose=r13_conversation_pose(who,pose or store.dialogue_expression)
        visible=who in CAST and who!="dad" and store.place!="마차 안" and store.r13_camera=="stage"
        if visible:
            arriving=store.r13_motion_person!=who or "r13_visitor" not in renpy.get_showing_tags()
            actor_pose=store.r13_current_pose if r13_acting_spec(who,store.r13_current_pose) else "interview_"+store.dialogue_expression
            renpy.show("r13_actor",what=r13_close_art(who,actor_pose,840,True,arriving),tag="r13_visitor",at_list=[r13_portrait_close(r13_close_y(who,pose=actor_pose))])
            store.r13_motion_person=who
        else:
            renpy.hide("r13_visitor")
            store.r13_motion_person=None

    def r13_read_key(identity,index,text):
        return identity+":"+str(index)+":"+r13_hashlib.sha256(text.encode("utf-8")).hexdigest()[:14]

    def r13_before_line(identity,index,text):
        key=r13_read_key(identity,index,text)
        if key not in persistent.room13_read:
            renpy.config.skipping=None
        elif store.r13_fast_read:
            renpy.config.skipping="slow"
        return key

    def r13_remember_line(key):
        if key not in persistent.room13_read:persistent.room13_read=persistent.room13_read+[key]

    def r13_dialogue_granny_reply(key, repeated, identity):
        # Dialogue only: no state, inventory, consent or timing writes.
        if repeated:
            return [("granny", "그 이야기는 들었어요. 같은 걸 다시 보인다고 내가 다른 기억을 갖게 되지는 않지요.")]
        replies = {
            "E05": [(None, "할머니는 도면보다 내 손을 먼저 보았다."), ("granny", "그 안까지 다녀오셨어요? 오래된 출입 자국일 수도 있잖아요. 아이도 데리고 들어간 건 아니지요?")],
            "E09": [(None, "할머니의 손끝이 종이의 가장자리에서 멈췄다."), ("granny", "구하러 들어간 사람도 많았지요. 누군가 도우러 간 자국까지 같은 뜻으로 보시면 곤란해요.")],
            "E10": [("granny", "목격한 분이 그 좁은 틈에서 어디까지 보았는지부터 확인해야죠. 아이를 돕고 싶은 마음과 실제로 본 것은 다르니까요.")],
            "E13": [("granny", "물건은 고쳐 쓰는 거예요. 수리 쪽지를 가졌다고 그 뒤의 일을 모두 아는 건 아니잖아요.")],
            "E14": [(None, "할머니는 몸을 조금 숙였다가 다시 의자에 기대었다."), ("granny", "작은 핀이네요. 물건 사이에 끼었다는 것과 누가 그랬다는 건 다른 이야기지요.")],
            "E35": [("granny", "상처를 꼼꼼히 보셨군요. 그래도 그 모양만으로 누가 들었는지까지 말할 수는 없잖아요.")],
            "E36": [(None, "할머니는 종이를 돌려주면서도 손을 바로 떼지 않았다."), ("granny", "걱정돼서 사람을 부르는 일이 잘못인가요? 병든 분을 챙겼다는 이유로 나를 의심하시면 서운하지요.")],
        }
        # Even when identity is disclosed, do not grant a new confession or fact.
        return replies[key]

    def r13_present(person,key,identity=False):
        # Only called after explicit confirmation. Inventory and the original remain.
        if key not in store.room13["evidence"]:
            return [(None,"이번 여정에서 직접 확보한 자료부터 확인해야 한다.")]
        n=winter_copy.deepcopy(store.room13)
        disclosure=key+(":named" if identity else ":anonymous")
        legacy_disclosure=disclosure
        if key=="E27":
            # An updated convoy record is new information; showing the same
            # revision twice must not change the convoy twice.
            disclosure+=":revision"+str(n["records"].get(key,{}).get("revision",0))
        known=n["resident_knowledge"].setdefault(person,[])
        repeated=disclosure in known or (key=="E27" and
            n["records"].get(key,{}).get("revision",0)==0 and legacy_disclosure in known)
        if not repeated:known.append(disclosure)
        store.room13=n
        if store.room13["day"]>=8 or person not in R13_CORE_PEOPLE:
            response=r13_w2_present(person,key,repeated)
            if response is not None:return response
        if person=="granny" and key in ("E05","E09","E10","E13","E14","E35","E36"):
            r13_flag("granny_prepared:"+key)
            if key=="E10" and identity:r13_flag("bami_identity_leaked")
            return r13_dialogue_granny_reply(key, repeated, identity)
        unlocked=None
        lines=[]
        if person=="buri" and key in ("E06","E08"):
            if r13_has("buri_refused"):
                return [(person,"할아버지를 범인 취급하면서 부탁할 생각은 마요. 밖에 한 말부터 바로잡아요.")]
            if not r13_has("medical_consent"):
                return [(person,"할아버지 상태부터 따지러 왔어요? 밖에서 무슨 말을 하는지부터 듣고 와요.")]
            knownkeys=[v.split(":")[0] for v in store.room13["resident_knowledge"].get(person,[])]
            if all(e in knownkeys for e in ("E06","E08")):
                unlocked="buri_records";lines=[(person,"……팔을 잡은 일은 지우지 않았네요. 그래도 머리의 상처까지 같은 일이라고 쓰진 않았고. 그럼 할아버지가 하려던 일도 들어 주세요.")]
            else:return [(person,"아이 말과 실제 상처가 같은 이야기인지도 봐야죠. 한쪽만 듣고는 못 넘겨요.")]
        elif person=="nabi" and key=="E11":
            unlocked="nabi_gap";lines=[(person,"도토가 문을 부수던 때? 난 그 앞에 있었어. ……할머니도 그때까지 같이 봤냐고?")]
        elif person=="resident_tok" and key=="E14":
            unlocked="tok_pin";lines=[(person,"이 이음은 알아요. 남아 있는 부품부터 대조합시다.")]
        elif person=="bami" and key=="E06":
            unlocked="bami_saw";lines=[(person,"다람이도 그 아래에 있었다고 했어? 그러면 내가 본 거랑 같아.")]
        elif person=="resident_lamplighter" and key=="E03" and r13_has("E01"):
            unlocked="lamplighter_warning";lines=[(person,"그 매듭 안쪽까지 아는군요. 편지를 받을 분이 맞는지 확인하고 싶었어요.")]
        elif person=="granny" and key=="E18":
            r13_flag("warning_exposed")
            return [(person,"그분이 아직 연락을 하고 있었군요. 어디서 받았어요?"),("dad","장소까지 말씀드리지는 않겠습니다.")]
        if unlocked:
            r13_flag("topic:"+unlocked)
            return lines+[(None,"대화 목록에 새 주제가 열렸다. 더 들을지는 직접 결정할 수 있다.")]
        if person in R13_RESIDENTS and not repeated:
            return [(person,R13_RESIDENTS[person]["unrelated"])]
        return [(person,"전에 보여 준 내용은 기억합니다. 다른 사실이 확인되면 다시 이야기하죠." if repeated else {
            "buri":"이걸로 제가 뭘 확인해 드릴 수 있죠? 제 일인지부터 모르겠는데요.",
            "nabi":"봤어. 그런데 내가 아는 일은 아니야.",
            "bami":"나는 거기 없었어. 아는 척은 못 해.",
            "seryeon":"내용은 확인했습니다. 지금 제 기록을 고칠 근거는 아니군요.",
            "karo":"제가 본 일과는 다른 것 같아요. 모르면서 답할 순 없죠.",
        }.get(person,"그 내용은 제가 확인해 드릴 수 없습니다."))]

    def r13_submit(claim,key):
        if key not in store.room13["evidence"]:return
        n=winter_copy.deepcopy(store.room13)
        pool=n["arguments"].setdefault(claim,[])
        if key not in pool:pool.append(key)
        store.room13=n

    def r13_argument_ready(claim):
        pool=set(store.room13["arguments"].get(claim,[]))
        if claim in ("C2","C4") and not r13_has("bami_consent"):pool.discard("E10")
        if claim=="F3" and not r13_survival_ready():return False
        if claim=="F4" and "C4" in store.room13["propositions"]:
            return {"E01","E18"}.issubset(pool)
        return any(set(path).issubset(pool) for path in R13_CLAIMS[claim]["support_sets"])

    def r13_prove(claim):
        n=winter_copy.deepcopy(store.room13)
        if claim not in n["propositions"]:n["propositions"].append(claim)
        store.room13=n

    def r13_evidence_feedback(claim,key):
        if key=="E10" and not r13_has("bami_consent"):
            return "관찰 내용은 검토하겠습니다. 다만 익명 기록만으로는 위치를 독립적으로 확인하기 어렵습니다. 다른 물증이 필요합니다."
        if key not in {e for path in R13_CLAIMS[claim]["support_sets"] for e in path}:
            return "이 자료는 보관하겠습니다. 하지만 지금 다투는 주장과 어떻게 이어지는지는 아직 설명되지 않았습니다."
        return ROOM13["evidence"][key]["establishes"]+". 다만 "+ROOM13["evidence"][key]["does_not_establish"]+"."

    def r13_stop_typing():
        if store.room13_mode and renpy.get_screen("choice"):
            renpy.config.skipping=None
        if store.room13_mode and any(renpy.get_screen(s) for s in ("r13_hub","r13_interaction","r13_topics","r13_book","r13_confirm","r13_map","r13_calendar","r13_debate","r13_activities","r13_handoff","r13_crisis","r13_crisis_proof","r13_rescue_notes","r13_ending_screen","r13_nearby","r13_resident_notes")):
            renpy.music.stop(channel="typing")
            renpy.config.skipping=None
    config.interact_callbacks.append(r13_stop_typing)
