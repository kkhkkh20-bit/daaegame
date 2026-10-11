# Shared case interpreter. Original v2 snapshot stays intact; 0.4 has an authored village opening.
default source_mode = False
default source_inventory = []
default source_seen = []
default source_flags = []
default source_location = "bed13"
default source_group = "meet"
default source_phase = 0
default source_statement = 0
default source_step = 0
default source_pressed = False
default source_started_meeting = False
default source_camera = "stage"
default source_scene = "P1"
default source_background = "carriage"
default source_night = None
default source_found = False
default source_permission = False
default source_actor = "granny"
default source_stage_person = None
default source_votes = {}
default source_effect_log = []
default source_line_log = []
default source_shown_text = ""
default source_current_line = None
default source_complete = False
default source_proof_show = []
default source_checks = {}

define source_thought = Character(None,cb_who_id="dad")
define source_character = source_thought
image source clock = Composite((512,512),(0,0),"assets/clock-base.png",(0,0),"assets/clock-hands.png")

init 10 python:
    import re
    import builtins as source_builtins
    SOURCE_PACKAGE = json.load(renpy.file("chapter-source.json"))
    SOURCE_EP = SOURCE_PACKAGE["episode"]
    SOURCE_PATHS = json.load(renpy.file("assets/source-map.json"))
    SOURCE_ALIAS = {"det0":"dad","det1":"daram","innma":"granny","geokkuri":"bami","wanggu":"neoul"}
    SOURCE_CHARS = {k:getattr(store,v) for k,v in SOURCE_ALIAS.items()}
    SOURCE_CHARS["???"] = Character("???")
    SOURCE_CHARS.update({k:getattr(store,k) for k in ("seryeon","nabi","doto","buri","karo")})
    SOURCE_LOC = {x["id"]:x for x in SOURCE_EP["LOCS"]}
    SOURCE_MAP_POINTS = {"plaza":(335,578),"front":(405,303),"kitchen":(590,460),"hall":(738,135),"dotoroom":(982,91),"bed13":(977,316),"dining":(152,380)}
    SOURCE_ICONS = {"C01":"assets/pouch.png","C02":"assets/flour-world.png","C03":"nabi neutral","C04":"assets/somsom.png","C05":"clue fur","C06":"source clock","C07":"bami neutral","C08":"assets/notebook.png","C09":"assets/notebook.png","C10":"assets/record.png","C11":"assets/notebook.png","C12":"seryeon neutral","C13":"bami neutral","C14":"karo neutral"}
    renpy.music.register_channel("scene_fx",mixer="sfx",loop=False)
    renpy.music.register_channel("pulse",mixer="sfx",loop=True)

    def source_name(key):
        return NAMES.get(SOURCE_ALIAS.get(key,key),key)

    def source_text(text):
        text=str(text).replace("[","[[")
        return re.sub(r"\{([^{}]+)\}",r"{color=#ffdc91}\1{/color}",text)

    def source_grant(key):
        if key in SOURCE_EP["EV"] and key not in store.source_inventory:
            store.source_inventory.append(key)
            source_fx("found")
            renpy.notify("수첩에 기록했다: "+SOURCE_EP["EV"][key]["name"])
            village_progress()

    def source_fx(key):
        if key in ("roll","carStop","carDepart","letter","tick2"):
            return # Archived horse audio stays disabled, as requested.
        path=("assets/door.wav" if key=="doorOpen" else
              SOURCE_PATHS["audio/v3/sfx/wood-door-close.wav"] if key=="door" else
              "assets/source-"+key+".wav")
        if renpy.loadable(path) and not renpy.is_skipping():
            store.source_effect_log.append(key)
            renpy.music.play(path,channel="scene_fx",loop=False)

    def source_score(key):
        spec=SOURCE_PACKAGE["music"].get(key)
        path="assets/town-bright.mp3" if key=="village_bright" else SOURCE_PATHS.get(spec["media"]) if spec else None
        if path!=renpy.music.get_playing():
            if path: renpy.music.play(path,fadeout=.15,fadein=.2)
            else: renpy.music.stop(fadeout=.15)

    def source_pulse(enabled):
        store.typing_allowed=not enabled
        renpy.music.stop(channel="typing")
        if enabled:
            store.source_effect_log.append("heartbeat")
            renpy.music.stop(fadeout=0)
            renpy.music.play("assets/source-silence.wav",channel="pulse",loop=False)
            renpy.music.queue("assets/source-heartbeat.wav",channel="pulse",loop=True,clear_queue=True)
        else: renpy.music.stop(channel="pulse",fadeout=0)

    def source_face(who,mood=""):
        person=SOURCE_ALIAS.get(who,who)
        village_observe(person)
        store.dialogue_speaker=person if person in CAST else None
        store.dialogue_expression=("distressed" if mood in ("sad","shock","nervous","worried","cower") else "thinking" if mood=="think" else "expressive" if mood in ("smile","oops") else "neutral")
        if who in ("det0","narr"):
            person=store.source_stage_person
            mood=""
        elif person in CAST:
            store.source_stage_person=person
        if person not in CAST or store.source_camera not in ("stage","courtyard") or store.source_night or store.source_proof_show:
            renpy.hide("visitor")
            return
        face=("distressed" if mood in ("sad","shock","nervous","worried","cower") else
              "thinking" if mood=="think" else "expressive" if mood in ("smile","oops") else "neutral")
        if face not in CAST[person]: face="neutral"
        renpy.show(person+" interview_"+face,tag="visitor",at_list=[store.portrait_close])

    def source_bg(key):
        if key=="plaza":
            return Transform("assets/outdoor-gate-morning.png",size=(1280,720))
        if key.startswith("outdoor-"):
            return Transform("assets/"+key+".png",size=(1280,720))
        if key in SOURCE_EP["BGS"] and SOURCE_EP["BGS"][key].get("src"):
            spec=SOURCE_EP["BGS"][key]
            image=SOURCE_PATHS[spec["src"]]
            view=spec.get("view")
            return Transform(Crop(tuple(view),image) if view else image,size=(1280,720))
        return {"bed13":"bg room","dining":"bg council","kitchen":"bg kitchen"}.get(key,"bg front")

    def source_picture():
        pictures={"carriage":"assets/carriage.png","driver":SOURCE_PATHS["art/ch1/cinematics/carriage-driver-close.png"],"approach":"assets/approach.png","village":SOURCE_PATHS["art/ch1/cinematics/village-arrival-wide.png"],"postoffice":"assets/outdoor-post.png","innentrance":"assets/outdoor-inn.png","courtyard":"assets/outdoor-inn.png","seal":"assets/pouch.png"}
        if store.source_camera in pictures: return Transform(pictures[store.source_camera],size=(1280,720))
        if store.source_night in ("home","return"): return source_bg("room")
        return source_bg(store.source_background)

    def source_directions(value):
        if isinstance(value,source_builtins.dict): return value
        result={}
        for part in str(value).split(";"):
            if ":" in part:
                k,v=part.split(":",1);result[k]=int(v) if v.isdigit() else v
        return result

    def source_questions(person):
        return [q for q in SOURCE_EP["TALK"].get(person,[])
                if (not q.get("need") or q["need"] in store.source_inventory)
                and (not q.get("after") or q["after"] in store.source_seen)
                and village_topic_available(q)]

    def source_card(key):
        ev=SOURCE_EP["EV"][key]
        if key=="C13" and "inn_c13fix" in store.source_flags:
            return ev.get("card2",ev.get("desc2",ev["desc"]))
        return ev.get("card",ev["desc"])

    def source_state():
        opened=lambda s:bool(renpy.get_screen(s))
        return dict(stage=store.stage,location=store.source_location,group=store.source_group,phase=store.source_phase,statement=store.source_statement,step=store.source_step,pressed=store.source_pressed,
          inventory=list(store.source_inventory),seen=list(store.source_seen),found=store.source_found,permission=store.source_permission,complete=store.source_complete,
          line=store.source_current_line,text=store.source_shown_text,scene=store.source_scene,camera=store.source_camera,night=store.source_night,effects=list(store.source_effect_log),lines=list(store.source_line_log),
          music=renpy.music.get_playing(),typing=renpy.music.get_playing(channel="typing"),pulse=renpy.music.get_playing(channel="pulse"),fx=renpy.music.get_playing(channel="scene_fx"),
          village_map=opened("arrival_map"),village_place=opened("arrival_place"),village_questions=opened("arrival_questions"),village_inn=opened("arrival_interior"),cold=store.arrival_cold,village_location=store.arrival_location,background=store.source_background,checks=dict(store.source_checks),met=list(store.arrival_met),village_seen=list(store.arrival_seen),post_closed=store.arrival_post_closed,stone=store.arrival_stone,
          trust_events=list(store.village_trust_events),flags=list(store.source_flags),minutes=store.village_minutes,time_events=list(store.village_time_events),observations=list(store.village_observations),trust=dict(store.village_trust),residents=village_resident_points(store.source_location),available_topics=[q["id"] for q in source_questions(store.source_person)] if hasattr(store,"source_person") else [],support_hearing=store.village_hearing_active,support_person=store.village_hearing_person,
          roam=opened("source_explore"),map=opened("source_map"),questions=opened("source_questions"),evidence=opened("source_evidence"),debate=opened("source_debate"),choice=opened("source_choice"),inspect=opened("source_inspect"),code=opened("chest_lock"),complete_screen=opened("trial_complete"),saving=opened("save"),loading=opened("load"),exception=opened("_exception"))

    def source_pause_effects():
        if store.source_mode:
            blocked=any(renpy.get_screen(s) for s in ("pause_menu","save","load","source_evidence"))
            renpy.music.set_pause(blocked,channel="pulse")
            if blocked:renpy.music.stop(channel="typing")
    config.interact_callbacks.append(source_pause_effects)

    def source_empty_click():
        renpy.end_interaction(("ambient",renpy.get_mouse_pos()))

    def source_ambient(point):
        x,y=point
        if store.source_location=="bed13":
            zone=("side-box" if 110<x<355 and 280<y<560 else
                  "window" if 400<x<570 and 95<y<290 else
                  "door" if x>1040 else "floor")
            return zone,ARRIVAL["observations"][zone]
        return "surroundings",ARRIVAL["observations"][store.source_location]

    def source_mark(action,value):
        anchors={"bag":(900,285),"quilt":(620,365),"chest":(747,474),
          "under":(854,516),"head":(740,190),"fur":(295,530),
          "clock":(430,170),"book":(340,495),"diary":(340,495)}
        key=store.source_location+":"+str(value if action=="spot" else action)
        if key not in store.source_checks and (value in anchors or action in anchors):
            store.source_checks[key]=anchors.get(value,anchors.get(action))

label start:
    $ source_mode = True
    $ source_inventory, source_seen, source_flags = [], [], []
    $ source_effect_log, source_line_log = [], []
    $ source_checks = {}
    $ village_minutes,village_time_events,village_observations = 1050,[],[]
    $ village_trust,village_trust_events = {p:-1 for p in TIMELINE["voters"]},[]
    $ village_hearing_active,village_hearing_person = False,None
    $ source_proof_show = []
    hide screen source_proof
    $ source_found = source_permission = source_complete = source_started_meeting = False
    $ arrival_met, arrival_seen, arrival_greeted = [], [], []
    $ arrival_post_closed = arrival_stone = False
    $ arrival_location = None
    $ arrival_checked_in = arrival_cold = False
    $ source_group, source_phase, source_statement, source_step = "meet",0,0,0
    $ stage = "opening"
    show screen hud
    show screen source_world
    call arrival_prologue
    $ source_location, stage = "bed13", "investigation"
    jump source_roam

label source_scenes(scenes, scene_index=0):
    while scene_index < len(scenes):
        $ source_sc = scenes[scene_index]
        $ source_scene, place, clock_text = source_sc.get("sid",""),source_sc["title"],source_sc["sub"]
        $ source_camera = source_sc.get("camera","carriage" if source_scene=="P1" else "village" if source_scene=="P2" else "stage")
        $ source_background = source_sc.get("bg") or source_sc["loc"]
        $ source_night = None
        $ source_stage_person = SOURCE_ALIAS.get(source_sc.get("who"),source_sc.get("who"))
        hide visitor
        window hide
        scene black with Dissolve(.15)
        $ source_pulse(False)
        $ source_score(source_sc.get("music"))
        $ renpy.pause(.3,hard=True)
        scene expression source_picture() with Dissolve(.22)
        call source_lines(source_sc["items"],source_scene)
        $ scene_index += 1
    return

label source_direction(direction):
    $ source_dir = source_directions(direction)
    if source_dir.get("night") in ("home","out","return"):
        $ source_pulse(False)
    if "music" in source_dir:
        $ source_score(source_dir["music"])
    if "camera" in source_dir or "night" in source_dir:
        window hide
        hide visitor
        scene black with Dissolve(.12)
        $ source_camera = source_dir.get("camera","stage")
        $ source_night = source_dir.get("night")
        $ renpy.pause(.3,hard=True)
        scene expression source_picture() with Dissolve(.18)
    if source_dir.get("who") == "none":
        $ source_stage_person = None
        hide visitor
    elif source_dir.get("who"):
        $ source_stage_person = SOURCE_ALIAS.get(source_dir["who"],source_dir["who"])
    if source_dir.get("sfx"):
        $ source_fx(source_dir["sfx"])
    if source_dir.get("stone"):
        show screen arrival_stone_glow
        $ renpy.pause(.8,hard=True)
        hide screen arrival_stone_glow
    if source_dir.get("chime"):
        $ source_fx("found")
    if source_dir.get("ms"):
        $ renpy.pause(min(source_dir["ms"]/1000.0,8.0))
    return

label source_lines(items, origin="", index=0):
    while index < len(items):
        $ source_packet = items[index]
        if isinstance(source_packet,source_builtins.list):
            $ source_w, source_t = source_packet[0], source_packet[1]
            $ source_m = (source_packet[6] if len(source_packet)>6 and source_packet[6] else source_packet[2] if len(source_packet)>2 else "")
            $ source_meta = {}
        else:
            $ source_w, source_t, source_m = source_packet.get("w"),source_packet.get("t"),source_packet.get("m","")
            $ source_meta = source_packet
        if source_meta.get("dir"):
            call source_direction(source_meta["dir"])
        elif source_meta.get("loc"):
            $ source_background = SOURCE_EP["LOC_BG"].get(source_meta["loc"],source_meta["loc"])
            $ place = SOURCE_LOC[source_meta["loc"]]["name"]
            $ source_camera,source_night = "stage",None
            window hide
            hide visitor
            scene black with Dissolve(.12)
            $ source_score("inn_meet")
            $ renpy.pause(.3,hard=True)
            scene expression source_picture() with Dissolve(.18)
        elif source_meta.get("hint"):
            $ renpy.notify(source_meta["hint"])
        elif source_meta.get("fade"):
            window hide
            scene black with Dissolve(.2)
        elif source_w == "@dir":
            call source_direction(source_t)
        elif source_w == "@grant":
            $ source_grant(source_t)
        elif source_w == "@inspect":
            call screen source_inspect(source_t)
        elif source_meta.get("sfx"):
            $ source_fx(source_meta["sfx"])
        elif source_t:
            $ source_mapping = SOURCE_EP["DIR"].get(str(source_t).strip("()"),{}) if source_w=="narr" else {}
            if source_mapping.get("c") == "stage":
                if source_mapping.get("cmd"):
                    call source_direction(source_mapping["cmd"])
            else:
                $ source_current_line = origin+":"+str(index)
                $ source_shown_text = village_vote_line(source_w,source_mapping.get("t",source_t),source_meta)
                if stage=="opening" and source_scene=="P13" and source_t.startswith("베개 밑") and source_camera=="stage":
                    $ source_camera = "seal"
                    hide visitor
                    scene expression source_picture() with Dissolve(.2)
                elif stage=="opening" and source_scene=="P13" and source_t.startswith("봉인띠를 자르겠습니다"):
                    $ source_camera = "stage"
                    scene expression source_picture() with Dissolve(.2)
                $ source_line_log.append(dict(id=source_current_line,w=source_w,t=source_shown_text))
                if source_meta.get("grant"):
                    $ source_grant(source_meta["grant"])
                if source_meta.get("votes"):
                    $ village_apply_votes(source_meta["votes"])
                if source_meta.get("beat"):
                    $ source_flags.append(source_meta["beat"])
                if source_meta.get("show"):
                    $ source_proof_show = source_meta["show"]
                    show screen source_proof
                if source_meta.get("fx"):
                    $ source_fx(source_meta["fx"])
                if source_meta.get("audio") in ("silence","pulse"):
                    $ source_pulse(source_meta["audio"]=="pulse")
                    $ source_score(None)
                    $ typing_allowed = False
                elif source_meta.get("audio") == "calm":
                    $ source_pulse(False)
                    $ source_score("inn_meet")
                elif source_meta.get("audio") in ("press","impact"):
                    $ source_pulse(False)
                    $ source_score("inn_meet_press" if source_group=="meet" else "inn_climax_press")
                    if source_meta["audio"] == "impact":
                        $ source_fx("cut9")
                if str(source_t).startswith(("…상자 뒤에 뭐가 있어","아빠… 위에 눈이…")):
                    $ source_pulse(True)
                if source_w=="narr" and "두 손으로 작은 몸" in source_t:
                    window hide
                    hide visitor
                    scene black with Dissolve(.12)
                    $ source_camera = "held"
                    scene cg somsom with Dissolve(.2)
                    $ renpy.pause(.2,hard=True)
                if str(source_t).startswith(("바구니랑 수건","모르겠어. 그러니까")):
                    $ source_pulse(False)
                    $ source_score("inn_serious")
                if source_w=="narr" and "바구니에 옮기고" in source_t:
                    $ source_camera = "stage"
                    scene expression source_picture() with Dissolve(.22)
                if source_t=="…움직였어.":
                    $ source_fx("pop9")
                $ source_face(source_w,source_m)
                $ source_character = SOURCE_CHARS.get(source_w,source_thought)
                $ source_rendered = source_text(source_shown_text)
                source_character "[source_rendered]"
                if source_meta.get("ask"):
                    $ source_ask = source_meta["ask"]
                    call screen source_choice(source_ask["title"],source_ask["items"])
                    while not _return.get("ok"):
                        call source_lines(_return.get("wr",[]),origin+"/wrong")
                        call screen source_choice(source_ask["title"],source_ask["items"])
        $ index += 1
    return

label source_roam:
    $ village_progress()
    $ source_proof_show = []
    hide screen source_proof
    $ stage = "investigation"
    $ place,clock_text = SOURCE_LOC[source_location]["name"],"조사 중"
    $ source_background = SOURCE_EP["LOC_BG"].get(source_location,"bed13")
    $ source_camera,source_night = "stage",None
    $ clock_text = village_clock()+" · 조사"
    hide visitor
    window hide
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("inn_search")
    $ renpy.pause(.3,hard=True)
    scene expression source_picture() with Dissolve(.18)
    call screen source_explore
    $ source_action,source_value = _return
    $ source_mark(source_action,source_value)
    if source_action == "map":
        call screen source_map
        $ source_location = _return
    elif source_action == "talk":
        $ source_person = source_value
        jump source_talk
    elif source_action == "ambient":
        $ source_ambient_key,source_ambient_lines = source_ambient(source_value)
        $ source_check_key = source_location+":"+source_ambient_key
        if source_check_key not in source_checks:
            $ source_checks[source_check_key] = source_value
        call source_lines(source_ambient_lines,"LOOK_"+source_ambient_key)
    elif source_action == "meeting":
        if all(k in source_inventory for k in SOURCE_EP["MEET"]["need"]):
            if not source_started_meeting:
                call source_lines(SOURCE_EP["I9"],"I9")
                $ source_started_meeting = True
            jump source_rounds
        $ renpy.notify("주머니·손자국·나비의 말·작은 손님을 먼저 확인하자.")
    elif source_action == "under":
        if not source_found and all(k in source_inventory for k in ("C01","C02","C03","C09","C12")):
            call source_lines(next(o["say"] for o in SOURCE_LOC["bed13"]["obs"] if o["id"]=="o_under"),"under")
            call source_lines(next(s["say"] for s in SOURCE_LOC["bed13"]["spots"] if s["id"]=="basket"),"basket")
            $ source_found = True
            $ source_grant("C04")
        elif not source_found:
            $ renpy.notify("주머니·이불·숙박부와 나비·세련의 말을 확인하자.")
        else:
            call source_lines(next(s["say"] for s in SOURCE_LOC["bed13"]["spots"] if s["id"]=="basket"),"basket")
    elif source_action == "head":
        call source_lines(next(o["say"] for o in SOURCE_LOC["bed13"]["obs"] if o["id"]=="o_inn_head2"),"head")
        if "head" not in source_seen:
            $ source_seen.append("head")
    elif source_action == "chest":
        if not source_found:
            call source_lines(next(o["say"] for o in SOURCE_LOC["bed13"]["obs"] if o["id"]=="o_inn_box"),"locked-box")
            jump source_roam
        if not source_permission:
            call source_lines(SOURCE_EP["LOCK"]["permission"],"permission")
            $ source_permission = True
        call screen chest_lock
        if _return == "opened":
            call source_lines(SOURCE_EP["LOCK"]["open"],"lock")
            call source_lines(next(s["say"] for s in SOURCE_LOC["bed13"]["spots"] if s["id"]=="ledger"),"ledger")
            $ source_grant("C11")
    elif source_action == "spot":
        $ source_spot = next(s for s in SOURCE_LOC[source_location]["spots"] if s["id"]==source_value)
        call source_lines(source_spot.get("say",[]),source_value)
        $ source_grant(source_spot["ev"])
    jump source_roam

label source_talk:
    $ source_actor = SOURCE_ALIAS.get(source_person,source_person)
    $ source_stage_person = source_actor
    $ source_score("inn_t_bami" if source_person=="geokkuri" else "inn_t_neoul" if source_person=="wanggu" else "inn_t_"+source_person)
    hide visitor
    window hide
    call screen source_questions(source_person)
    if _return == "back":
        jump source_roam
    $ source_question = _return
    if source_person in arrival_met and source_person not in arrival_greeted and source_person in ARRIVAL["recognition"]:
        call source_lines(ARRIVAL["recognition"][source_person],"V_RECOGNITION_"+source_person)
        $ arrival_greeted.append(source_person)
    call source_lines(village_question_lines(source_question),source_question["id"])
    $ village_relationship("interview_"+source_person,[SOURCE_ALIAS.get(source_person,source_person)],1)
    if source_question.get("ev"):
        $ source_grant(source_question["id"])
    if source_question.get("sets"):
        $ source_flags.append(source_question["sets"])
    if source_question["id"] not in source_seen:
        $ source_seen.append(source_question["id"])
    if source_question["id"] == "T_se4":
        call source_lines(TIMELINE["departures"]["seryeon"],"V_SERYEON_DEPARTURE")
        jump source_roam
    jump source_talk

label source_rounds:
    $ stage,place = "meeting","여관 원탁"
    $ source_camera,source_night = "stage",None
    hide visitor
    hide screen round_table
    window hide
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("inn_meet" if source_group=="meet" else "inn_climax")
    $ renpy.pause(.3,hard=True)
    scene bg council with Dissolve(.2)
    show screen round_table
    while source_phase < len(SOURCE_EP["MEET" if source_group=="meet" else "FINAL"]["phases"]):
        $ source_round = SOURCE_EP["MEET" if source_group=="meet" else "FINAL"]["phases"][source_phase]
        $ clock_text = village_round_time()
        if source_round.get("intro"):
            call source_lines(source_round["intro"],source_group+str(source_phase)+"/intro")
        if source_round["type"] == "talk":
            call source_lines(source_round["lines"],source_group+str(source_phase))
        elif source_round["type"] == "adjourn":
            if not all(k in source_inventory for k in source_round["need"]):
                call source_lines(source_round.get("lines",[]),"adjourn")
                $ renpy.notify(source_round["task"])
                hide screen round_table
                jump source_roam
            call source_lines(source_round.get("resume",[]),"resume")
        elif source_round["type"] == "vote":
            call screen source_choice(source_round["q"],[dict(label=source_name(k),key=k) for k in SOURCE_EP["MEET"]["seats"]])
            while _return["key"] != "seryeon":
                $ renpy.notify("지금까지 확인한 이동과 발견 위치를 다시 생각하자.")
                call screen source_choice(source_round["q"],[dict(label=source_name(k),key=k) for k in SOURCE_EP["MEET"]["seats"]])
            call village_support_hearing
            $ village_update_votes()
            call source_lines(TIMELINE["vote_resolution"],"V_SUPPORT_VOTE")
        elif source_round["type"] == "debate":
            $ source_statement,source_step,source_pressed = 0,0,False
            call source_debate_loop
        $ source_phase += 1
    if source_group == "meet":
        $ source_group,source_phase = "final",0
        $ source_fx("impact")
        jump source_rounds
    hide screen round_table
    $ source_pulse(False)
    $ village_event("resolved")
    $ stage = "ending"
    call source_scenes(SOURCE_EP["END"])
    $ source_complete,test_complete = True,True
    stop music fadeout .4
    call screen trial_complete
    return

label source_debate_loop:
    $ source_proof_show = []
    hide screen source_proof
    window hide
    hide visitor
    call screen source_debate(source_round)
    $ source_action,source_value = _return
    $ source_claim = source_round["stms"][source_statement]
    if source_action == "select":
        if source_statement != source_value:
            $ source_statement,source_step,source_pressed = source_value,0,False
        jump source_debate_loop
    elif source_action == "press":
        call source_lines(source_claim.get("press",[]),"press")
        $ source_pressed = True
        $ source_fx("tap")
        jump source_debate_loop
    call screen source_evidence(present=True)
    $ source_evidence = _return
    if source_evidence == "cancel":
        jump source_debate_loop
    if source_claim.get("needPress") and not source_pressed:
        $ renpy.notify("먼저 어떻게 확인했는지 되물어 보자.")
        jump source_debate_loop
    $ source_steps = source_claim.get("steps",[])
    if source_step < len(source_steps) and source_evidence in source_steps[source_step]["ids"]:
        call source_lines(source_steps[source_step].get("lines",[]),"comparison")
        $ source_step += 1
        $ source_fx("select")
    elif source_step == len(source_steps) and source_evidence in source_claim.get("a",[]):
        $ source_fx("impact")
        $ source_score("inn_meet_press" if source_group=="meet" else "inn_climax_press")
        $ village_proof_support()
        call source_lines(source_claim.get("ok",[]),source_group+str(source_phase)+"/ok")
        return
    elif source_evidence in source_claim.get("soft",{}):
        $ source_soft = source_claim["soft"][source_evidence]
        call source_lines(source_soft.get("lines",[]),"related")
        if "to" in source_soft:
            $ source_statement,source_step,source_pressed = source_soft["to"],0,source_soft.get("pressed",False)
    elif source_evidence in source_claim.get("wr",{}):
        call source_lines(source_claim["wr"][source_evidence],"wrong")
    else:
        $ renpy.notify("이 발언의 되묻기와 다른 기록을 함께 살펴보자.")
    jump source_debate_loop
