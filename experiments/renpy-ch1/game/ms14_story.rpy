# New story pilot in the existing engine/UI. Original campaign labels remain loadable.
default ms14 = None
default ms14_node = None
default ms14_record = None
default ms14_background_key = "carriage"
default ms14_village_visible = False
default ms14_props = []
default ms14_options = []
default ms14_answer = None
default ms14_menu_page = 0
default ms14_block_skip = False

init 220 python:
    import ms14_runtime as ms14_rt
    MS14_DATA = json.load(renpy.file("ms14/route.json"))
    MS14_ART = json.load(renpy.file("ms14/art.json"))
    ms14_rt.validate(MS14_DATA)
    R13_PLACES["ms14_somi"] = ("솜이네 골목","winter")
    R13_PLACES["ms14_stable"] = ("마구간 앞","ep_stable")
    R13_PLACES["ms14_somi_inside"] = ("솜이네 방","ep_somi_home")
    R13_PLACES["ms14_guardroom"] = ("밝은 초소 안","winter")
    MS14_SPEAKERS = {"아빠":"dad", "다람":"daram", "까로":"karo", "돌목":"guard",
        "너울":"neoul", "할머니":"granny", "초롱":"resident_lamplighter", "세련":"seryeon",
        "모모":"resident_momo", "피코":"resident_piko", "나비":"nabi", "네로":"resident_nero",
        "톡":"resident_tok", "부리":"buri", "우박":"resident_ubak", "실룩":"resident_siluk",
        "백 부인":"resident_madam", "바둑이":"resident_badook", "솜이":"resident_somi",
        "콩이":"resident_kongi","토실":"resident_tosil","밤이":"bami","무쇠":"resident_musoe",
        "진료 담당자":"ms14_clinician","종업원":"ms14_attendant"}
    R13_CHARS["ms14_clinician"] = Character("진료 담당자")
    R13_CHARS["ms14_attendant"] = Character("종업원")
    for _ms_key, _ms_spec in MS14_DATA["evidence"].items():
        _ms_id = "MS14:"+_ms_key
        ROOM13["evidence"][_ms_id] = dict(id=_ms_id, name=_ms_spec["name"], kind=_ms_spec["kind"],
            establishes="", does_not_establish="", current_run_only=True, retained_on_show=True, scenes=[])
        R13_RECORD_SHORT[_ms_id] = _ms_spec["name"]

    def ms14_observed(key):
        if not store.ms14 or not key.startswith("MS14:"):return None
        return ms14_rt.observed(MS14_DATA, store.ms14, key[5:])

    def ms14_present_entries(entries):
        return [key for key in entries if not key.startswith("MS14:") or ms14_rt.presentable(MS14_DATA,store.ms14,key[5:])]

    def ms14_silence():
        if not store.ms14:return
        cue = "MS14_D05_S04_L0006:first_sentence_done"
        if cue in store.ms14.get("presentation",{}).get("cues",[]):return
        store.ms14 = ms14_rt.silence(store.ms14)
        renpy.music.stop(channel="music",fadeout=.12)

    def ms14_character_callback(event, **kwargs):
        packet = getattr(store,"r13_packet",None)
        record = getattr(store,"ms14_record",None)
        if event=="slow_done" and store.ms14 and record and record.get("id")=="MS14_D05_S04_L0006" and packet and len(packet)>2 and isinstance(packet[2],dict) and packet[2].get("ms14_silence_after"):
            ms14_silence()

    def ms14_audio_after_load():
        if store.ms14 and store.ms14.get("presentation",{}).get("music_silent"):
            renpy.music.stop(channel="music")

    config.all_character_callbacks.append(ms14_character_callback)
    config.after_load_callbacks.append(ms14_audio_after_load)

    def ms14_art_key(key):
        if not store.ms14:return None
        if key == "MS14:E30":return "bundle"
        if key == "MS14:E09":
            return {"complete":"portrait_complete", "unfinished":"portrait_unfinished",
                "child_completed":"portrait_child"}.get(store.ms14["values"]["portrait"])
        return None

    def ms14_material_art(key):
        if key == "MS14:E35" and store.ms14:
            count = store.ms14["values"]["carried_dry_blankets"]
            if count == 2:
                return Composite((160,100),(0,0),Transform(MS14_ART["blanket_ochre"]["file"],xysize=(100,100),fit="contain",nearest=True),
                    (60,0),Transform(MS14_ART["blanket_teal"]["file"],xysize=(100,100),fit="contain",nearest=True))
            if count == 1:return Transform(MS14_ART["blanket_ochre"]["file"],xysize=(160,100),fit="contain",nearest=True)
            return None
        art = ms14_art_key(key)
        if not art:return None
        return Transform(MS14_ART[art]["file"], xysize=(160,100), fit="contain", nearest=True)

    def ms14_sync():
        # Never feed MS14 IDs or effects through the old campaign's grant/upgrade hooks.
        # Only the existing notebook/HUD view is projected, with no world event evaluation.
        n = winter_copy.deepcopy(store.room13)
        n["day"] = store.ms14["values"]["day"]
        n["evidence"] = ["MS14:"+k for k in store.ms14["evidence"]]
        for key in n["evidence"]:
            n["records"].setdefault(key, dict(day=n["day"],period=n["period"],source="실제로 조사한 자료"))
        store.room13 = n

    def ms14_stage(node):
        scene = node.get("scene")
        # Branch nodes have no presentation; the selected authored block owns it.
        if not scene:return
        key = scene[5:]
        background = {"D01_S01":"carriage","D01_S02":"gate","D01_S03":"gate","D01_S04":"gate",
            "D01_S05":"room","D02_S01":"square","D02_S02":"post","D02_S03":"square",
            "D02_S04":"dining","D02_S05":"room","D03_S01":"square","D03_S02":"square",
            "D03_S03":"clinic","D03_S04":"store","D03_S05":"square","D03_S06":"square",
            "D04_S01":"somi","D04_S02":"square","D04_S03":"gate","D04_S04":"guardroom",
            "D05_S01":"somi","D05_S02":"somi_inside","D05_S03":"guardroom",
            "D05_S04":"gate","D05_S05":"room"}[key]
        overrides = {"day2":"stable","inn":"inn","square2":"square", "go_box":"square",
            "box_path":"forest","box_inspect":"forest","box_empty":"forest","box_note":"forest","box_written":"forest",
            "shelter_choice":"dining","shelter_work":"dining","shelter_prepare":"square","shelter_enter":"dining",
            "nero_choice":"square","nero_work":"forest","nero_done":"forest","evening2":"inn",
            "piko_alive3":"dining","piko_clean":"dining","piko_receive":"dining",
            "workshop3":"workshop","loan_read":"workshop","loan3":"workshop",
            "silluk3":"square","transport_read":"square","transport3":"square","knife_permission":"square","knife_observed":"square",
            "piko_evening":"clinic","piko_memorial":"square","stairs3":"room", "labor4":"square",
            "d4_visit_declined":"somi","d4_field":"gate","d4_field_talk":"gate","d4_collect":"gate",
            "d4_collect_input":"gate","d4_diner":"dining","d4_box_news":"square",
            "d5_inside":"somi_inside","d5_wait":"somi_inside","d5_clinic_handover":"clinic","d5_gate_visit":"clinic",
            "d5_night_visit":"somi_inside","d5_diner_guard":"dining","d5_inn_lobby":"inn",
            "d5_hall":"hall"}
        background = overrides.get(store.ms14["node"],background)
        store.ms14_background_key = background
        store.place = MS14_DATA["scenes"][scene]["location"]
        store.r13_scene_bg = {"gate":"winter","room":"room","dining":"council","square":"winter_square",
            "post":"winter_post","workshop":"winter_workshop","clinic":"clinic","forest":"forest",
            "stable":"ep_stable","inn":"front","store":"market","somi":"winter","carriage":"carriage",
            "somi_inside":"ep_somi_home","guardroom":"winter","hall":"hall"}[background]
        store.ms14_props = []
        store.r13_last_partner = None
        n = winter_copy.deepcopy(store.room13)
        n["location"] = {"carriage":"gate","room":"room13","gate":"gate","somi":"ms14_somi","stable":"ms14_stable",
            "somi_inside":"ms14_somi_inside","guardroom":"ms14_guardroom"}.get(background,background)
        n["period"] = {"D04_S02":1,"D04_S03":2,"D04_S04":2,"D05_S03":1,"D05_S04":1,"D05_S05":2}.get(key,0)
        if store.ms14["node"] in ("evening2","evening2_alive","evening2_outside","evening2_end","sleep1","sleep2","stairs3","sleep3","sleep4"):
            n["period"] = 2
        store.room13 = n

    def ms14_background():
        # BG_SOMI_LANE has no dedicated art. Use the delivery's explicit exterior
        # reframe candidate, never the existing house INTERIOR as an outside lane.
        spec = MS14_ART["gate" if store.ms14_background_key=="somi" else store.ms14_background_key]
        if store.ms14_background_key == "guardroom":
            # Only the desk side of the provided reframe candidate; the adjacent
            # holding-cell door is not the room where Bami agreed to sit.
            w,h=spec["size"]
            return Transform(Crop((w//2,0,w-w//2,h),spec["file"]),xysize=(1280,720),fit="cover",nearest=True)
        if store.ms14_background_key == "carriage" and not store.ms14_village_visible:
            return Composite((1280,720),(0,0),Solid("#161516"),(300,0),
                Transform(Crop((650,0,736,780),spec["file"]),xysize=(680,720),nearest=True))
        width,height = spec["size"]
        scale = max(1280.0/width,720.0/height)
        scaled_w,scaled_h = int(round(width*scale)),int(round(height*scale))
        return Crop(((scaled_w-1280)//2,(scaled_h-720)//2,1280,720),
            Transform(spec["file"],xysize=(scaled_w,scaled_h),nearest=True))

    def ms14_cue_before(record):
        rid = record["id"]
        background = {"MS14_D01_S05_L0036":"inn","MS14_D01_S05_L0039":"room",
            "MS14_D02_S04_L0049":"forest","MS14_D02_S04_L0076":"square",
            "MS14_D02_S04_L0079":"inn","MS14_D02_S04_L0083":"room",
            "MS14_D02_S05_L0006":"room","MS14_D03_S04_L0026":"workshop",
            "MS14_D03_S04_L0028":"store","MS14_D03_S04_L0034":"workshop"}.get(rid)
        if background:
            store.ms14_background_key = background
            renpy.scene()
            renpy.show("expression",what=ms14_background(),tag="ms14_stage")
        # Detail art is shown only after the corresponding explicit observation input.
        if rid == "MS14_D01_S05_L0022":store.ms14_props = ["bundle","family"]
        if rid == "MS14_D02_S01_L0033":store.ms14_props = ["box"]
        if rid == "MS14_D02_S01_L0039":store.ms14_props = []
        if rid == "MS14_D03_S06_L0017":store.ms14_props = ["portrait_child"]
        if rid == "MS14_D04_S02_L0016":store.ms14_props = [ms14_art_key("MS14:E09")]
        if rid == "MS14_D05_S04_L0006":store.ms14_props = ["warning_private"]
        # The hidden action is staged as source narration only where it is literal visible
        # movement, not instructions, author truth or effects. No synthetic hand poses.
        return

    def ms14_line(record):
        speaker = MS14_SPEAKERS.get(record.get("speaker"))
        if record.get("speaker") and speaker is None:raise Exception("Unmapped speaker: "+record["speaker"])
        # Stable source record identity isolates read tracking from the old campaign.
        if record["id"] == "MS14_D05_S04_L0006":
            first, rest = ms14_rt.warning_parts(record["text"])
            return [(speaker,first,{"no_lead":True,"expression":"neutral","ms14_silence_after":True}),
                (speaker,rest,{"no_lead":True,"expression":"neutral"})]
        return [(speaker, record["text"], {"no_lead":True,"expression":"neutral"})]

    def ms14_menu_options(node):
        return [(o["title"],i) for i,o in enumerate(node["options"]) if ms14_rt.allowed(store.ms14,o["guard"])]

screen ms14_prop_layer():
    zorder 1
    for ms_i, ms_prop in enumerate(ms14_props):
        add Transform(MS14_ART[ms_prop]["file"],xysize=(420,290),fit="contain",nearest=True):
            xpos (650 if ms_i==0 else 860) ypos (105 if ms_i==0 else 160)

label ms14_start:
    $ room13_mode = True
    $ winter_mode = True
    $ source_mode = False
    $ winter = winter_new()
    $ room13 = r13_new()
    $ ms14 = ms14_rt.new_state(MS14_DATA)
    $ ms14_village_visible = False
    $ r13_scene_key = None
    $ r13_world_cameras = {}
    $ r13_inspection_location = None
    $ r13_prepare_history()
    $ room13["learning_archive"] = []
    $ typing_allowed = True
    hide screen winter_hud
    hide screen hud
    hide screen source_world
    hide screen source_proof
    show screen r13_hud
    show screen ms14_prop_layer
    stop music fadeout .3
    jump ms14_run

label ms14_run:
    $ ms14 = ms14_rt.upgrade(ms14,MS14_DATA)
    $ ms14_node = MS14_DATA["nodes"][ms14["node"]]
    $ ms14_sync()
    $ ms14_stage(ms14_node)
    if ms14_node["kind"] == "branch":
        $ ms14 = ms14_rt.enter(ms14,ms14_rt.branch_target(ms14,ms14_node))
        jump ms14_run
    scene expression ms14_background()
    if ms14_node["kind"] == "block":
        $ ms14_block_skip = False
        while ms14["cursor"] < len(ms14_node["records"]):
            $ ms14_record = MS14_DATA["records"][ms14_node["records"][ms14["cursor"]]]
            $ ms14_cue_before(ms14_record)
            if not ms14_block_skip and ms14_record["player_visible"] and ms14_record["kind"] in ("dialogue","narration","evidence"):
                call r13_lines(ms14_line(ms14_record),ms14_record["id"])
            if ms14_record["id"] == "MS14_D05_S04_L0006":
                $ ms14_silence()
            $ ms14 = ms14_rt.finish_record(ms14,ms14_record)
            $ ms14_sync()
            if ms14_record["id"] in ("MS14_D03_S01_L0021","MS14_D03_S01_L0039"):
                $ ms14_props = [ms14_art_key("MS14:E09")]
            if ms14_record["id"] == "MS14_D01_S01_L0022":
                $ ms14_village_visible = True
                scene expression ms14_background()
        $ ms14 = ms14_rt.enter(ms14,ms14_node["next"])
    elif ms14_node["kind"] == "choice":
        $ ms14_menu_page = 0
        call ms14_choice
    elif ms14_node["kind"] == "proof":
        call ms14_proof
    elif ms14_node["kind"] == "mark":
        $ ms14 = ms14_rt.apply(ms14,ms14["node"],ms14_node["operations"])
        $ ms14 = ms14_rt.enter(ms14,ms14_node["next"])
    elif ms14_node["kind"] == "read":
        $ ms14_record = ms14_rt.observed(MS14_DATA,ms14,ms14_node["key"])
        call r13_lines([(None,ms14_record["establishes"])],ms14["node"])
        $ ms14 = ms14_rt.enter(ms14,ms14_node["next"])
    elif ms14_node["kind"] == "notebook":
        call screen r13_records(close_action=Return())
        $ ms14 = ms14_rt.enter(ms14,ms14_node["next"])
    elif ms14_node["kind"] == "end":
        jump ms14_review_end
    jump ms14_run

label ms14_choice:
    $ renpy.choice_for_skipping()
    $ ms14_options = ms14_menu_options(ms14_node)
    if len(ms14_options)>5:
        $ ms14_options = ms14_options[ms14_menu_page*4:ms14_menu_page*4+4]+[("다른 항목을 본다",-1)]
    $ ms14_answer = renpy.display_menu([(ms14_node["title"],None)]+ms14_options,screen="choice")
    if ms14_answer == -1:
        $ ms14_menu_page = (ms14_menu_page+1) % ((len(ms14_menu_options(ms14_node))+3)//4)
        jump ms14_choice
    $ ms14 = ms14_rt.choose(ms14,ms14_node,ms14_answer)
    return

label ms14_proof:
    $ renpy.choice_for_skipping()
    $ ms14_options = [("자료를 고른다","pick"),("선택한 자료를 제시한다","submit")]
    if ms14_node.get("hint"):
        $ ms14_options.append(("힌트를 생각한다","hint"))
    $ ms14_options.append(("자료를 다시 읽는다","read"))
    $ ms14_answer = renpy.display_menu([(ms14_node["title"]+" · 선택 %d개"%len(ms14["selected"]),None)]+ms14_options,screen="choice")
    if ms14_answer == "pick":
        call screen r13_book(target=None,present=True)
        if _return and _return.startswith("MS14:"):
            $ ms14 = ms14_rt.select(ms14,_return[5:])
            $ renpy.notify("고른 자료: "+" · ".join(MS14_DATA["evidence"][k]["name"] for k in ms14["selected"]))
        jump ms14_proof
    elif ms14_answer == "submit":
        if ms14["selected"]:
            $ ms14 = ms14_rt.submit(ms14,ms14_node)
        else:
            $ renpy.notify("제시할 자료를 직접 골라 주세요.")
    elif ms14_answer == "hint":
        $ ms14 = ms14_rt.enter(ms14,ms14_node["hint"])
    else:
        call screen r13_records(close_action=Return())
        jump ms14_proof
    return

label ms14_review_end:
    $ ms14 = ms14_rt.upgrade(ms14,MS14_DATA)
    if ms14["values"]["day"] == 4 and "E18" in ms14["evidence"]:
        $ ms14 = ms14_rt.enter(ms14,"d4_depart")
        show screen ms14_prop_layer
        jump ms14_run
    hide r13_visitor
    hide screen ms14_prop_layer
    $ ms14_props = []
    $ renpy.notify("새 스토리 검토 구간: 5일 밤까지")
    menu:
        "기록을 살펴본다":
            call screen r13_records(close_action=Return())
            jump ms14_review_end
        "메인 화면으로":
            hide screen r13_hud
            $ room13_mode = False
            $ winter_mode = False
            return
