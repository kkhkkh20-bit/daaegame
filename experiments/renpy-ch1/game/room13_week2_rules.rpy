# Campaign continuation. All consequential state is saved in room13, not persistent.
default persistent.room13_endings = []
default persistent.room13_ending_notes = {}
default r13_ending_id = None

init 56 python:
    R13_PLACES.update({
        "clinic":("임시 진료실","r13_clinic"),
        "school":("마을 학교","r13_school"),
        "store":("공동 물품 창고","r13_store"),
        "greenhouse":("폐온실의 지하 작업실","r13_greenhouse"),
        "facility":("북쪽 보호시설 접견실","r13_facility"),
        "altar":("북쪽 산길 · 숲속 제단","r13_altar"),
    })
    R13_NAMES.update(mom="엄마",resident_teacher="곰 선생님",resident_eunho="은호 사장",
        resident_bori="보리",resident_nubi="누비 아주머니")
    R13_CHARS.update({k:Character(v,cb_who_id=k if k in CAST else None) for k,v in R13_NAMES.items()})
    R13_GREETING.update({
        "resident_seori":"본 일과 전해 들은 일을 나눠 말씀해 주세요. 제 기록도 틀릴 수 있습니다.",
        "resident_teacher":"아이들이 잘 방부터 비우고 있어요. 다들 여기로 오고 싶다고만 하네요.",
        "resident_eunho":"풀어 달라고만 하지 말고, 어디까지 쓸 건지 말해요.",
        "resident_bori":"이 수레 한 번 움직이면 다른 짐은 못 옮겨. 먼저 어디로 가야 하는지 정해 줘.",
        "resident_nubi":"안쪽 시설 세탁물이 아직 안 나왔어요. 일거리가 줄어도 좋은 일은 아니네요.",
        "mom":"어디부터 확인했어? 네가 본 것부터 같이 보자.",
    })
    R13_PRESS.update({
        "F1":"한 사람이 잠깐 자기 이름을 말했다고 모두 돌아올 수 있습니까? 다음 날 다시 나빠진 사람도 있습니다.",
        "F2":"힘을 뽑아내자 불이 돌아온 건 다들 봤습니다. 남은 힘을 모아도 결국 바닥나기는 마찬가지 아닙니까? 오늘 밤 버틸 양까지 확인했습니까?",
        "F3":"방만 있으면 됩니까? 먹을 것, 장작, 밤에 남아 돌릴 사람까지 있어야 합니다.",
        "F4":"아이를 지키려고 한 일입니다. 살인을 따지는 것과 가족에게 편지를 보낸 이유는 다른 문제잖아요.",
    })
    R13_ENDINGS={e["id"]:e for e in ROOM13["endings"]}

    def r13_upgrade():
        n=winter_copy.deepcopy(store.room13)
        # A contradictory scene already seen cannot be silently rewritten by a save migration.
        if n.get("story_revision")!=ROOM13["story_revision"]:
            n["revision_restart_required"]=True
        for k,v in dict(mom_state="hidden",ending=None,events=[],convoy_revision=0,
            scout_revision=-1,observations={},week2_started=False,finale_started=False,
            kitchen_switch=False,passage_open=False).items():
            n.setdefault(k,v)
        # Old saves keep a route only if it was found in that same run; nothing
        # carries over from earlier runs (each run starts from zero).
        if "secret_route_unlocked" not in n:
            n["secret_route_unlocked"]=bool(n.get("passage_open")
                or "map" in n.get("done",[]) or {"E04","E05","E37"}&set(n.get("evidence",[])))
        previous_visual_revision=n.get("visual_revision")
        previous_interaction_revision=n.get("interaction_revision")
        previous_world_art=n.get("world_art_revisions",{})
        world_layouts=getattr(store,"R13_WORLD_LAYOUTS",{})
        world_art={location:r13_world_revision(location) for location in world_layouts}
        if world_art:
            n["world_art_revisions"]=world_art
            for key in list(n.get("checks",{})):
                location,_,object_key=key.partition(":")
                if location in world_art and previous_world_art.get(location)!=world_art[location]:
                    spec=ROOM13["objects"].get(location,{}).get(object_key)
                    if spec:
                        x,y,w,h=spec["rect"]
                        n["checks"][key]=[x+w//2,y+h//2]
        previous_carriage_art=n.get("carriage_art_file")
        carriage_art=getattr(store,"R13_CARRIAGE_IMAGE",None)
        if carriage_art:n["carriage_art_file"]=carriage_art
        n["interaction_revision"]=2
        target_visual_revision="pixel-b-front-v3" if len(getattr(store,"R13_PORTRAITS",{}))==43 else "pixel-b-acting-v2"
        if previous_visual_revision!=target_visual_revision or previous_interaction_revision!=2:
            # Keep discoveries; move their visible checkmarks with the redrawn props.
            points={}
            for key,point in n.get("checks",{}).items():
                location,_,object_key=key.partition(":")
                spec=ROOM13["objects"].get(location,{}).get(object_key)
                if spec:
                    x,y,w,h=spec["rect"]
                    points[key]=[x+w//2,y+h//2]
            n["checks"]=points
            n["last_inspection"]=None
            n["visual_revision"]=target_visual_revision
        store.room13=n
        if previous_visual_revision and previous_visual_revision!=target_visual_revision:
            # Saves serialize displayables too. Replace the old painted scene
            # before the first resumed interaction, without changing the route.
            old_scene=store.r13_scene_key
            background=old_scene[0] if old_scene else R13_PLACES[n["location"]][1]
            who=store.dialogue_speaker
            expression=store.dialogue_expression
            pose=store.r13_current_pose if previous_visual_revision.startswith(("pixel-b-acting","pixel-b-front")) else expression
            choice_screen=renpy.get_screen("choice")
            choice_actor=choice_screen.scope.get("choice_actor") if choice_screen else None
            if choice_actor in CAST:
                pose=choice_screen.scope.get("choice_pose",pose)
            renpy.scene()
            renpy.show("r13_restored_background",what=r13_background(background))
            if who in CAST:r13_speaker(who,expression,pose)
            elif choice_actor in CAST:r13_speaker(choice_actor,expression,pose)
            # A resumed say screen has no fresh Character begin callback.
            store.dialogue_speaker=who
            store.r13_scene_key=None
            choice_screen=renpy.get_screen("choice")
            if choice_screen:
                r13_choice_layout(choice_screen.scope.get("choice_actor"),choice_screen.scope.get("choice_pose","neutral"),True)

        elif previous_interaction_revision!=2 and "r13_visitor" in renpy.get_showing_tags():
            # A saved master-layer actor still contains the old static art.
            # Refresh only that actor; keep cinematic/background layers intact.
            saved_speaker=store.dialogue_speaker
            expression=store.dialogue_expression
            pose=store.r13_current_pose
            choice_screen=renpy.get_screen("choice")
            actor=choice_screen.scope.get("choice_actor") if choice_screen else store.r13_motion_person
            if choice_screen:pose=choice_screen.scope.get("choice_pose",pose)
            if actor in CAST:
                renpy.hide("r13_visitor")
                r13_speaker(actor,expression,pose)
                store.dialogue_speaker=saved_speaker
                if choice_screen:r13_choice_layout(actor,pose,True)

        scene_key=getattr(store,"r13_scene_key",None)
        world_location=r13_world_scene_location(scene_key[0]) if world_layouts and scene_key else None
        if world_location and store.r13_camera=="stage" and previous_world_art.get(world_location)!=world_art[world_location]:
            # Refresh a saved narrow backdrop without replacing its current
            # speaker, pose, entrance timer, dialogue line, or choice layout.
            for tag in renpy.get_showing_tags():
                if tag!="r13_visitor":renpy.hide(tag)
            renpy.show("r13_restored_background",what=r13_background(scene_key[0]),zorder=-1)

        if carriage_art and previous_carriage_art!=carriage_art and store.r13_scene_key and store.r13_scene_key[0]=="winter_carriage":
            # A saved opening serializes its old CG. Replace only this static
            # carriage scene; the current line, read history and HUD stay put.
            renpy.scene()
            renpy.show("r13_restored_background",what=r13_background("winter_carriage"))


    def r13_event(key):
        n=winter_copy.deepcopy(store.room13)
        if key not in n.setdefault("events",[]):n["events"].append(key)
        store.room13=n

    def r13_abs_time():
        return (store.room13["day"]-1)*4+store.room13["period"]

    def r13_w2_where(person):
        s=store.room13;p=min(s["period"],2)
        if person=="mom":return "greenhouse" if r13_has("mom_reunited") else None
        if person=="granny":return None if s["granny_state"]=="detained" else "inn"
        if person=="resident_owlgp":return "school" if s["victim_state"]!="dead" else None
        if person=="nabi":
            if s["granny_state"]=="detained" and p==0:return "inn"
            return "school" if r13_has("shelter_ready") else "dining"
        if person=="buri":return "workshop"
        if person=="resident_tok":return "workshop" if p<2 else "school"
        if person=="resident_seori":return ("clinic","store","school")[p]
        if person=="resident_lamplighter":return ("square","workshop","gate")[p]
        if person=="resident_eunho":return "store"
        if person=="resident_teacher":return "school"
        if person=="resident_bori":return ("school","store","gate")[p]
        if person=="resident_nubi":return "school" if r13_has("nubi_protected") else ("facility","inn","school")[p]
        if person=="neoul":return "facility"
        if person=="karo":return "gate"
        if person=="seryeon":return "post" if p<2 else None
        if person=="doto":return "hall"
        if person=="bami":return "inn" if r13_has("bami_protected") else "hall" if p>0 else None
        return r13_resident_where(person)

    def r13_w2_actions_allowed(key):
        s=store.room13
        if key=="w2_measure1":return s["period"] in (0,1)
        if key=="w2_measure2":
            first=s.get("observations",{}).get("first")
            return bool(first and first["time"]<r13_abs_time() and s["period"]==2)
        if key.startswith("w2_rescue_"):
            return s.get("scout_revision")==s.get("convoy_revision")
        return True

    def r13_w2_action_done(key,started_at=None):
        n=winter_copy.deepcopy(store.room13)
        if key=="w2_reply":
            n["reply_due"]=r13_abs_time()+4
            n["mom_state"]="contact_pending"
        if key=="w2_scout":
            n["scout_revision"]=n["convoy_revision"]
            for ev in ("E27","E28"):
                n["records"][ev].update(day=n["day"],period=n["period"],revision=n["convoy_revision"])
        if key in ("w2_measure1","w2_measure2"):
            n["observations"]["first" if key=="w2_measure1" else "second"]={
                "time":r13_abs_time() if started_at is None else started_at,
                "load":"day_low" if key=="w2_measure1" else "evening_high",
                "operator":"buri","recorder":"resident_seori"}
        if key=="w2_secure_contact":n["mom_state"]="contacted"
        store.room13=n

    def r13_w2_present(person,key,repeated):
        s=store.room13
        if key in ("E19","E30","E27") and person in ("granny","seryeon","neoul"):
            if repeated:return [(person,"이미 확인한 자료입니다. 공개된 내용을 없던 일로 할 수는 없어요.")]
            if key=="E19":
                if r13_has("mom_reunited"):
                    r13_flag("pursuit_active")
                    return [(person,"이곳에서 만나셨군요. 그다음에 어디로 갔는지도 확인해야겠습니다."),
                        (None,"이미 만난 가족이 사라지는 것은 아니다. 하지만 돌아갈 길을 뒤따르는 시선이 생겼다.")]
                n=winter_copy.deepcopy(s)
                n["mom_state"]="relocated"
                n["flags"]=[f for f in n["flags"] if f!="contact_safe"]
                n["done"]=[k for k in n["done"] if k!="w2_secure_contact"]
                store.room13=n
                r13_flag("pursuit_active","contact_compromised")
                return [(person,"이곳에서 연락을 받았군요. 방문 사실은 확인하겠습니다."),
                    (None,"건넨 것은 현재 연락 장소가 적힌 자료였다. 그곳에 나만 갈 수 있는 것은 아니다.")]
            if key=="E30":
                r13_flag("research_disclosed")
                return [(person,"본인이 작성한 연구군요. 다른 사람이 다시 확인한 결과도 있습니까?")]
            if person=="granny" and key=="E27":
                n=winter_copy.deepcopy(s);n["convoy_revision"]+=1
                n["done"]=[k for k in n["done"] if k!="w2_scout"]
                store.room13=n
                r13_flag("convoy_changed")
                return [(person,"그 시간에 데려간다고 했군요. 불편한 점이 없는지 내가 물어볼게요."),
                    (None,"할머니는 끌고 가는 시간을 다시 확인했다. 지금 지키는 순서가 그대로인지 살펴야 한다.")]
        for spec in ROOM13.get("presentations",[]):
            if person!=spec["npc"] or key not in spec["items"]:continue
            known={v.split(":")[0] for v in s["resident_knowledge"].get(person,[])}
            if spec.get("all_shown") and not set(spec["items"]).issubset(known):
                return [(person,"이것만으로는 확인이 어렵습니다. 서로 맞춰 볼 원본도 보여 주세요.")]
            if person=="resident_lamplighter" and not all(r13_has(k) for k in ("E01","E03")):
                return [(person,"편지를 가졌다는 것만으로 가족인지 알 수는 없습니다. 직접 알아볼 흔적도 필요해요.")]
            r13_flag("topic:"+spec["topic"])
            return [(person,spec["reply"]),(None,"새 대화 주제가 열렸다.")]
        return None

    def r13_survival_ready():
        return all(r13_has(k) for k in ("shelter_ready","supplies_ready","operators_ready","patient_transport"))

    def r13_rescue_routes():
        current=store.room13.get("scout_revision")==store.room13.get("convoy_revision")
        if not current:return []
        result=[]
        if r13_has("injunction_support") and r13_has("E27"):result.append("order")
        if all(r13_has(k) for k in ("laundry_support","shelter_ready","E28")):result.append("laundry")
        if all(r13_has(k) for k in ("maintenance_support","operators_ready","E28")):result.append("maintenance")
        return result

    def r13_true_ending_ready():
        s=store.room13
        first=s.get("observations",{}).get("first",{})
        second=s.get("observations",{}).get("second",{})
        return ("F4" in s["propositions"] and r13_has("mother_original_safe")
            and (r13_has("bami_protected") or r13_has("witness_protected"))
            and bool(first and second and first["time"]<second["time"] and first["load"]!=second["load"])
            and ("C4" in s["propositions"] or r13_has("premeditation_prevented_proven")))

    def r13_resolve_ending():
        s=store.room13
        if s["daram_state"]=="lost":return "E1"
        if "F2" not in s["propositions"]:return "E3"
        if not (r13_survival_ready() and "F1" in s["propositions"] and "F3" in s["propositions"]):return "E4"
        return "E6" if r13_true_ending_ready() else "E5"

    def r13_finish_ending(key):
        r13_edit(ending=key)
        if key not in persistent.room13_endings:persistent.room13_endings=persistent.room13_endings+[key]
        notes=dict(persistent.room13_ending_notes)
        notes[key]=R13_ENDINGS[key]["knowledge"]
        persistent.room13_ending_notes=notes
        renpy.save_persistent()

    def r13_crisis_preparations():
        return [("쉴 곳",r13_has("shelter_ready")),("식량과 장작",r13_has("supplies_ready")),
            ("밤에 번갈아 지킬 사람들",r13_has("operators_ready")),("환자 운반",r13_has("patient_transport"))]

    def r13_ending_notes():
        """Only facts experienced in this run, never a hidden ending checklist."""
        s=store.room13
        result=["다람이는 가족과 함께 있다." if s["daram_state"] in ("with_dad","rescued") else "다람이를 데려오지 못했다."]
        if s["victim_state"]=="dead":result.append("13호 사건으로 잃은 사람은 돌아오지 않았다.")
        elif s["case_state"]=="prevented":result.append("그날 함께 방에 들어가 죽음을 막았다.")
        if "F2" in s["propositions"]:result.append("주민들은 억지로 힘을 뽑아내는 일을 멈췄다.")
        if "F4" in s["propositions"]:result.append("가족을 꾀어낸 계획을 모두가 볼 수 있는 기록으로 남겼다.")
        if s["day"]>=14:
            missing=[name for name,ready in r13_crisis_preparations() if not ready]
            if missing:result.append("끝까지 마련하지 못한 것: "+", ".join(missing))
        return result
