# V1.1.1 continuation uses existing world, map, notebook and scene renderer.
init 310 python:
    R13_V111_ENTRY.update({
        "MS14_D04_S01":([],{"day":4}),
        "MS14_D04_S02":(["E18"],{}),
        "MS14_D04_S03":(["E19"],{"afternoon_visit_declined":True}),
        "MS14_D04_S04":(["E20"],{"bami_status":"temporarily_with_badugi","dolmok.location":"clinic"}),
        "MS14_D05_S01":(["E21","E22"],{}),
        "MS14_D05_S02":([],{"somi_entry_consent":True,"E24.status":"partial"}),
        "MS14_D05_S03":(["E20","E22","E23","E24"],{"musoe.location":"clinic","somi.location":"clinic"}),
        "MS14_D05_S04":([],{"bami_status":"cleared"}),
        "MS14_D05_S05":([],{"mother_warning_received":True,"supply_contact_pending":True}),
    })
    # Existing map component needs positions for the already registered places.
    # 0.20.11: ms14_somi/ms14_somi_inside use the drawn riverside house (alias of "somi", init 313).
    R13_MAP_NODES["village"].update(ms14_guardroom=(155,375))
    R13_MAP_LABELS.update(ms14_somi="솜이네 골목",ms14_somi_inside="솜이네 방",ms14_guardroom="밝은 초소")
    # Use the existing approved Somi room master for this place, without starting
    # the inactive MS14 controller or changing the picture itself.
    _v111_somi=MS14_ART["somi_inside"]["file"]
    R13_WORLD_LAYOUTS["ms14_somi_inside"]=dict(width=1920,initial_x=0,ignore_legacy_positions=True,slots=[(330,660,300,"floor"),(710,680,325,"floor"),(1100,670,315,"floor"),(1510,680,340,"floor"),(1760,680,315,"floor")],files={k:_v111_somi for k in ("morning","afternoon","evening")})
    ROOM13["objects"].setdefault("ms14_somi_inside",{})["v111_coat"]=dict(rect=[1400,350,300,300],need=[],give=[],flags=[],text="허락받고 벗어 놓은 회색 겉옷")
    ROOM13["objects"].setdefault("ms14_somi",{})["v111_bedding"]=dict(rect=[600,470,260,180],need=[],give=[],flags=[],text="처마 아래 젖은 침구와 물통")
    # No generated prop sprites: observations point to the existing gate scenery.
    ROOM13["objects"]["gate"]["v111_fence"]=dict(rect=[850,300,170,240],need=[],give=[],flags=[],text="울타리 못에 회색 천이 걸렸다.")
    ROOM13["objects"]["gate"]["v111_bucket"]=dict(rect=[1050,500,150,140],need=[],give=[],flags=[],text="엎어진 양동이 옆의 발자국은 겹쳐 있다.")
    R13_OBJECT_NAMES.update(v111_coat="벗은 겉옷",v111_bedding="침구와 물통",v111_fence="울타리 천",v111_bucket="양동이")
    MS14_SPEAKERS.update({"사자 선생님":"resident_teacher","선생님":"resident_teacher","꼬미":"kid_kkomi","도담":"kid_dodam","새미":"kid_saemi","보리":"resident_bori","누비":"resident_nubi","도토":"doto","부엉이":"resident_owlgp","서리":"resident_seori","따닥":"resident_ttadak","슬링":"resident_sling","촌장":"resident_ppul","엄마":"mom","은호":"resident_eunho","창고 아이 1":"kid_kkam","창고 아이 2":"kid_mong","창고 아이 3":"kid_bang","누비의 큰아이":"kid_nubi1","누비의 둘째":"kid_nubi2","누비의 막내":"kid_nubi3","아이":"kid_nubi3"})
    # Existing unnamed child slot: retain the original script label, no new art.
    for _key,_name in (("kid_nubi1","누비의 큰아이"),("kid_nubi2","누비의 둘째"),("kid_nubi3","누비의 막내")):
        R13_NAMES.setdefault(_key,_name)
        if _key not in R13_CHARS:R13_CHARS[_key]=Character(R13_NAMES[_key],cb_who_id=_key)
    # Already approved places/backgrounds, not a replacement map or new UI.
    R13_PLACES["laundry"]=("마을 빨래터","ep_laundry")
    R13_PLACES["v111_custody"]=("보호실 면회 자리","ep_holding_morning")
    R13_PLACES["v111_supervised"]=("분리된 감독 자리","ep_holding_morning")
    R13_MAP_LABELS["v111_supervised"]="분리 감독 자리"
    R13_MAP_NODES["village"]["v111_custody"]=(150,330)
    R13_MAP_LABELS["v111_custody"]="보호실"
    # 0.20.11: the laundry has its own drawn place on the widened map (room13-cartography.json).
    R13_MAP_LABELS["laundry"]="빨래터"
    R13_MAP_LABELS["somi"]="솜이네"
    for _key,_title,_bg in (("v111_labor","공동 장작 하역장","ep_woodshed_intact"),("v111_woodshed","학교 뒤 장작 창고","ep_woodshed_intact"),("v111_fire","장작 창고 바깥","ep_woodshed_fire"),("v111_ruin","식은 장작 창고 터","ep_woodshed_ruin")):
        R13_PLACES[_key]=(_title,_bg)
        R13_MAP_NODES["village"][_key]=(102,190)
        R13_MAP_LABELS[_key]=_title
        ROOM13["objects"][_key]={}
    for _loc in ("v111_woodshed","v111_fire","v111_ruin"):
        for _object,_rect,_text in (("v111_wood",[680,410,260,240],"옆문 앞 장작"),("v111_water",[340,420,200,220],"물통과 천"),("v111_lamp",[720,400,240,200],"등잔과 별도 보관할 천")):
            ROOM13["objects"][_loc][_object]=dict(rect=_rect,need=[],give=[],flags=[],text=_text)
    R13_OBJECT_NAMES.update(v111_wood="장작",v111_water="물통과 천",v111_lamp="등잔과 천")

init 311 python:
    def r13_v111_tok_attends(venue):
        if venue not in ("workshop","hearing"):raise ValueError(venue)
        return bool(r13_v111_value("TOK_ALIVE") and r13_v111_value("tok_"+venue+"_present"))

    def r13_v111_actor_ready(person):
        v=store.room13.get("v111",{}).get("values",{})
        life={"resident_nero":"nero_alive","resident_owlgp":"OWL_ALIVE","kid_kkomi":"KKOMI_ALIVE","resident_tok":"TOK_ALIVE","resident_piko":"piko_alive","resident_musoe":"musoe_alive"}
        if v.get(life.get(person,"alive:"+person),True) is False:return False
        if person=="dad":return True
        if v.get("busy:"+person) in ("family_walk","medical_call","school_transport") and v.get("location:"+person)!=store.room13["location"]:return False
        location=v.get("location:"+person)
        authored=set(store.room13["v111"].get("people",[])+r13_v111_binding().get("people",[]))
        if person in authored:return location is None or location==store.room13["location"]
        # Unassigned residents keep their existing actual world schedule.
        return not v.get("busy:"+person) and globals().get("r13_where",lambda p:None)(person)==store.room13["location"]
    def r13_v111_arrive(people):
        # Called only at authored actual arrivals, never as a record condition.
        people=list(people)
        scene=store.room13["v111"].get("scene")
        if "mom" in people and r13_v111_value("madam_observer_consent") and r13_v111_person_alive("resident_madam") and (scene=="MS14_D14_S02" or scene=="MS14_D14_S04" and store.room13["location"]=="school"):
            people.append("resident_madam")
        present=list(dict.fromkeys(person for person in people if r13_v111_person_alive(person)))
        for person in present:
            r13_v111_set("location:"+person,store.room13["location"])
        store.room13["v111"]["people"]=present
    def r13_v111_record_allowed(rid):
        check=R13_V111_ALLOWED.get(rid)
        return bool(check and check())

init 312 python:
    MS14_SPEAKERS.update({"굴돌":"resident_guldol","판돌":"npc_pandol","순찰대원":"v111_patrol","실룩의 아이":"v111_siluk_child","아랫길 주민":"v111_lower_resident","아랫길 노인":"v111_lowerroad_elder","주민":"v111_resident","아이":"v111_child"})
    for _key,_name in (("v111_patrol","순찰대원"),("v111_siluk_child","실룩의 아이"),("v111_lower_resident","아랫길 주민"),("v111_lowerroad_elder","아랫길 노인"),("v111_resident","주민"),("v111_child","아이")):
        R13_NAMES[_key]=_name
        R13_CHARS[_key]=Character(_name,cb_who_id=_key)
    R13_REL_DEAD["resident_owlgp"]="v111:owl_dead"
    R13_REL_STAMPED.add("v111:owl_dead")
    R13_V111_LIFE={"resident_nero":"nero_alive","resident_owlgp":"OWL_ALIVE","kid_kkomi":"KKOMI_ALIVE","resident_tok":"TOK_ALIVE","resident_piko":"piko_alive","resident_musoe":"musoe_alive","kid_dodam":"alive:kid_dodam"}
    # Register the already approved place art as world layouts, so the existing
    # hub uses the same background as dialogue and every rect shares its space.
    for _place in ("laundry","v111_labor","v111_woodshed","v111_fire","v111_ruin"):
        _bg=R13_PLACES[_place][1]
        _files={k:("assets/"+v) for k,v in R13_EP_BACKGROUNDS[_bg].items()} if isinstance(R13_EP_BACKGROUNDS[_bg],dict) else {k:r13_ep_background_file(_bg) for k in ("morning","afternoon","evening")}
        R13_WORLD_LAYOUTS[_place]=dict(width=1920,initial_x=0,ignore_legacy_positions=True,slots=[(280,660,310,"floor"),(680,680,325,"floor"),(1070,660,315,"floor"),(1480,680,335,"floor"),(1770,670,310,"floor")],files=_files)

init 313 python:
    # Existing cartography contours are reused for places within those map areas.
    # There are no new generated map plates or replacement navigation controls.
    R13_V111_MAP_ALIASES={"ms14_somi":"somi","ms14_somi_inside":"somi","ms14_guardroom":"gate","v111_custody":"gate","v111_supervised":"gate","v111_labor":"store","v111_woodshed":"school","v111_fire":"school","v111_ruin":"school"}
    for _alias,_base in R13_V111_MAP_ALIASES.items():
        _node=winter_copy.deepcopy(R13_CARTOGRAPHY["regions"]["village"]["nodes"][_base])
        _node["art_key"]=_base
        R13_CARTOGRAPHY["regions"]["village"]["nodes"][_alias]=_node
        R13_MAP_NODES["village"][_alias]=R13_MAP_NODES["village"][_base]

init 314 python:
    R13_V111_SCENE_CHECKS={
        "MS14_D06_S01":lambda:r13_v111_value("mother_warning_received") is True,
        "MS14_D06_S02":lambda:r13_v111_value("school_day_seat")=="confirmed",
        "MS14_D06_S03":lambda:r13_v111_value("FIRE_EVACUATED") is False,
        "MS14_D06_P01":lambda:r13_v111_value("evacuation_requested") is True,
        "MS14_D06_S03P":lambda:r13_v111_value("FIRE_EVACUATED") is True and r13_v111_value("warehouse_children_school_handover")==4,
        "MS14_D06_S04":lambda:bool(r13_v111_value("D06_S03_main_completed") or r13_v111_value("D06_S03P_empty_fire_completed")),
        "MS14_D07_S01":lambda:r13_v111_owned("E06_FIRE"),
        "MS14_D07_S02":lambda:r13_v111_value("NUBI_admitted_setting_fire") is True,
        "MS14_D07_S03":lambda:r13_v111_value("D07_S02_handover_completed") is True,
        "MS14_D07_S04":lambda:r13_v111_value("route7")=="murder" and r13_v111_value("D07_S03_C_completed") is True,
        "MS14_D07_P01":lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="A",
        "MS14_D07_P02":lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("prevention")=="B",
        "MS14_D08_S01":lambda:r13_v111_value("route7")=="murder" and r13_v111_value("DARAM_DETAINED") is True,
        "MS14_D08_S02":lambda:r13_v111_value("route7")=="murder" and r13_v111_value("OWL_ALIVE") is False,
        "MS14_D08_S03":lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E08_ROOM"),
        "MS14_D08_P01":lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True,
        "MS14_D09_S01":lambda:r13_v111_value("route7")=="murder",
        "MS14_D09_S02":lambda:r13_v111_value("route7")=="murder" and r13_v111_owned("E09_PASSAGE"),
        "MS14_D09_S03":lambda:r13_v111_owned("E09_PIN_OWNER"),
        "MS14_D09_P01":lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True,
        "MS14_D10_S01":lambda:r13_v111_value("route7")=="murder" and all(r13_v111_owned(k) for k in ("E08_CHILD_POSITION","E08_ROOM_REACH","E08_CONTACT_ASSEMBLY","E08_WOUND_WIRE","E09_PIN_HANDOVER_TIME","E09_SCARF")),
        "MS14_D10_S02":lambda:r13_v111_value("D10_S01_main_completed") is True,
        "MS14_D10_S03":lambda:r13_v111_value("D10_S02_second_door_completed") is True,
        "MS14_D10_S04":lambda:r13_v111_value("D10_confrontation_release_completed") is True and r13_v111_value("DARAM_DETAINED") is False,
        "MS14_D10_P01":lambda:r13_v111_value("route7")=="prevented" and r13_v111_value("OWL_ALIVE") is True,
        "MS14_D11_S00":lambda:r13_v111_owned("E10_PUMP"),
        "MS14_D11_S01":lambda:r13_v111_value("root_address_known") is True,
        "MS14_D11_S02":lambda:r13_v111_value("tosil_safe_handoff_confirmed") is True and r13_v111_value("greenhouse_address_known") is True,
        "MS14_D11_S02A":lambda:r13_v111_value("family_reunited") is True,
        "MS14_D11_S02B":lambda:r13_v111_value("family_reunited") is True,
        "MS14_D11_S03":lambda:r13_v111_value("family_reunited") is True,
        "MS14_D11_S04":lambda:r13_v111_value("family_school_place") is True,
        "MS14_D12_S01":lambda:r13_v111_value("lower_road_handover")==3 or r13_v111_value("lower_road_lost") is True,
        "MS14_D12_S03":lambda:r13_v111_value("route12")=="late_exposure",
        "MS14_D12_S04":lambda:r13_v111_value("route12") in ("late_exposure","premeal_stopped") and r13_v111_value("soup_fragment_observed") is True,
        "MS14_D12_S05":lambda:r13_v111_value("route12")=="late_exposure" and r13_v111_value("teacher_confessed") is True and r13_v111_value("medical_arrived") is True,
        "MS14_D12_A":lambda:r13_v111_value("route12")=="premeal_stopped",
        "MS14_D12_B":lambda:r13_v111_value("route12")=="early_prevented",
        "MS14_D13_S02":lambda:r13_v111_value("family_reunited") is True and r13_v111_value("DARAM_DETAINED") is not True,
        "MS14_D13_S03":lambda:r13_v111_value("family_deal") is False and r13_v111_owned("E13_MENDING"),
        "MS14_D13_S04":lambda:r13_v111_value("false_message_admitted") is True,
        "MS14_D13_A":lambda:r13_v111_value("family_deal") is True,
        "MS14_D13_B":lambda:r13_v111_value("cart_stopped") is True and not r13_v111_value("all_cart_handed"),
        "MS14_D13_C":lambda:r13_v111_value("false_message_admitted") is True and r13_v111_value("cart_stopped") is True,
        "MS14_D14_S01":lambda:r13_v111_value("all_cart_handed") is True,
        "MS14_D14_S02":lambda:r13_v111_value("all_cart_handed") is True and r13_v111_value("altar_guide_confirmed") is True,
        "MS14_D14_S04":lambda:r13_v111_value("bomi_death_confirmed") is True,
        "MS14_D14_S05":lambda:r13_v111_value("family_reunited") is True and r13_v111_value("night14_lodging") in ("gate","school"),
        "MS14_D14_END_FAMILY":lambda:r13_v111_value("outcome13")=="family_priority",
        "MS14_D14_END_PARTIAL":lambda:r13_v111_value("outcome13")=="partial_rescue",
        "MS14_D14_END_VIOLENCE":lambda:r13_v111_value("crowd_injury") is True,
    }

init 316 python:
    def r13_v111_warning_audio(event,**kwargs):
        packet=getattr(store,"r13_packet",None)
        if event=="slow_done" and r13_v111_active() and packet and len(packet)>2 and isinstance(packet[2],dict) and packet[2].get("v111_silence_after"):
            store.room13["v111"]["music_hold"]=store.room13["v111"].get("scene")
            renpy.music.stop(fadeout=0.0 if renpy.is_skipping() else .15)
    config.all_character_callbacks.append(r13_v111_warning_audio)

init 317 python:
    R13_V111_QUESTIONS={
        "MS14_D01_S01":"편지에 적힌 여관까지 무사히 갈 수 있을까?",
        "MS14_D01_S02":"마을에 들어가려면 무엇을 확인받아야 할까?",
        "MS14_D01_S03":"우리가 낸 신청서와 문지기의 원본은 같은 내용일까?",
        "MS14_D01_S04":"우리 두 사람 모두 제대로 등록됐을까?",
        "MS14_D01_S05":"편지를 보낸 여관에서 아내를 만날 수 있을까?",
        "MS14_D02_S01":"오늘 마을을 떠날 길이 있을까?",
        "MS14_D02_S02":"편지를 부친 사람은 정말 아내일까?",
        "MS14_D02_S03":"아내의 얼굴을 그려 줄 사람을 찾을 수 있을까?",
        "MS14_D02_S04":"남은 낮 시간으로 누구를 먼저 도울 수 있을까?",
        "MS14_D02_S05":"아내를 마지막으로 본 날 이후는 누가 알까?",
        "MS14_D03_S01":"그림 속 얼굴이 아내와 닮았을까?",
        "MS14_D03_S02":"광장 등의 돌은 언제 사라졌을까?",
        "MS14_D03_S03":"톡의 집게는 지금 어디에 있을까?",
        "MS14_D03_S04":"집게를 돌려주기 전에 무엇을 더 확인해야 할까?",
        "MS14_D03_S05":"등을 연 사람과 돌을 가져간 사람은 같을까?",
        "MS14_D03_S06":"돌을 되돌린 뒤 아내를 찾는 길은 어디로 이어질까?",
        "MS14_D04_S01":"아내의 초상으로 만날 수 있는 사람은 누구일까?",
        "MS14_D04_S02":"밤이가 직접 본 것은 어디까지일까?",
        "MS14_D04_S03":"초소 뒤에서 누가 다친 걸까?",
        "MS14_D04_S04":"불빛 안에 남은 흔적이 그날 밤의 말과 맞을까?",
        "MS14_D05_S01":"그날 밤 돌아온 모습을 직접 본 사람은 누구일까?",
        "MS14_D05_S02":"허락받은 옷의 찢어진 끝과 울타리 천이 이어질까?",
        "MS14_D05_S03":"밤이를 붙잡아 둘 근거가 실제로 남아 있을까?",
        "MS14_D05_S04":"아내의 답은 처음 편지와 같은 말을 하고 있을까?",
        "MS14_D05_S05":"우리가 이 문을 스스로 열고 닫을 수 있을까?",
        "MS14_D06_S01":"다람의 자리만 마련하면 다른 아이들은 어디에 있을까?",
        "MS14_D06_S02":"아이들이 안에서 스스로 나올 수 있는 곳일까?",
        "MS14_D06_P01":"허락과 함께 네 아이의 실제 자리도 확보됐을까?",
        "MS14_D06_S03":"아이들이 지나갈 수 있는 길이 남아 있을까?",
        "MS14_D06_S04":"불이 시작된 자리와 따로 보관할 흔적은 무엇일까?",
        "MS14_D07_S01":"기름 천과 등유 통만으로 그날 일을 알 수 있을까?",
        "MS14_D07_S02":"아이들의 오늘 밤 자리와 보호자는 정해졌을까?",
        "MS14_D07_S03":"아픈 어르신과 다람 곁에 지금 누가 남을 수 있을까?",
        "MS14_D08_S02":"도토는 문틈에서 무엇을 계속 확인했을까?",
        "MS14_D08_S03":"두 조각과 상처는 어떤 접촉을 남겼을까?",
        "MS14_D08_S04":"답장을 안전하게 받으려면 무엇이 필요할까?",
        "MS14_D09_S01":"문이 닫혀도 밖으로 돌아올 수 있을까?",
        "MS14_D09_S02":"수선된 핀의 모양과 인수인은 누구일까?",
        # 2026-10-24 행동 검수 9-4: 핀을 다시 채웠다는 말은 이 장면에서 나비에게 처음 듣는다. 아빠가 아는 데까지만.
        "MS14_D09_S03":"비명이 났을 때 할머니는 어디 있었을까?",
        "MS14_D09_S04":"맡긴 사람과 쓴 사람을 같은 사람이라 할 수 있을까?",
        "MS14_D09_P01":"돌려받은 종이의 번호와 빈 자리는 맞을까?",
        "MS14_D10_S02":"그 문 말고 들어갈 길이 실제로 있었을까?",
        "MS14_D10_S03":"상처에 남은 조각과 계단참의 핀은 어떻게 이어질까?",
        "MS14_D10_P01":"가족이라는 말만으로 이 종이를 받을 권리가 있을까?",
        "MS14_D11_S00":"마지막으로 사용한 연락함에 지금 답이 남아 있을까?",
        "MS14_D11_S01":"토실이 안전하게 기다릴 곳은 정해졌을까?",
        "MS14_D11_S02B":"아내가 돌아오지 못한 이유는 무엇일까?",
        "MS14_D11_S03":"지금 가진 열과 운반 인력으로 누구의 자리를 먼저 마련할 수 있을까?",
        "MS14_D11_S04":"아랫길 사람들은 스스로 올라올 수 있을까?",
        "MS14_D12_S01":"몸을 녹일 자리와 물자는 같은 곳에 있을까?",
        "MS14_D12_S02":"배식 준비와 아이들 자리는 안전하게 확인됐을까?",
        "MS14_D12_S03":"남은 수프에서 무엇이 발견됐을까?",
        "MS14_D12_S04":"온전했던 봉인과 확인한 동선은 어떻게 이어질까?",
        "MS14_D13_S01":"판돌에게 둘러 줄 담요의 터진 곳은 어디일까?",
        "MS14_D13_S02":"가족의 자리와 다른 사람의 이송을 함께 약속할 수 있을까?",
        "MS14_D13_S03":"촌장이 전한 시점과 우리가 직접 한 일은 맞을까?",
        "MS14_D13_S04":"수레가 멎은 뒤 실제로 인수된 사람은 누구일까?",
        "MS14_D14_S02":"사람을 묶는 장치와 남은 열의 쓰임은 같은 것일까?",
        "MS14_D14_S04":"실제로 남은 물자는 누구에게 인수됐을까?",
    }
    def r13_v111_goal():
        v=store.room13.get("v111",{})
        # 2026-10-24 행동 검수 4: 이동 대기 중에는 직전 장면의 문구를 유지한다(r13_v111_scene 이 적어 둔 것).
        scene=v.get("thought_scene") if v.get("gate")=="travel" and v.get("thought_pending") else v.get("scene")
        return R13_V111_QUESTIONS.get(scene,"")

init 318 python:
    # 0.20.12 (4~14일 리뷰 남은 그림, 소유자 "도트 퀄리티 비슷하게", "화면 길게"): 6일 창고 안 장면은
    # 바깥 장작더미 대신 길게 이어지는 창고 안 그림을, 새 이야기의 보호시설은 오른쪽으로 벽 한 칸을
    # 늘여 벽화·깨진 돌판·새긴 이름이 있는 그림을 쓴다. 그림 원본: art/bg-woodshed-mural-20261023/round2/.
    # (init 310~312가 이 장소들을 등록한 뒤라야 덮어쓴다.)
    R13_EP_BACKGROUNDS["ep_woodshed_inside"]={"morning":"room13-pixel-wide-woodshed-inside-afternoon.webp",
        "afternoon":"room13-pixel-wide-woodshed-inside-afternoon.webp","evening":"room13-pixel-wide-woodshed-inside-evening.webp"}
    R13_PLACES["v111_woodshed"]=(R13_PLACES["v111_woodshed"][0],"ep_woodshed_inside")
    R13_WORLD_LAYOUTS["v111_woodshed"]=dict(width=2400,initial_x=420,ignore_legacy_positions=True,
        slots=[(330,680,320,"floor"),(760,690,330,"floor"),(1150,680,325,"floor"),(1560,690,335,"floor"),(1980,680,320,"floor")],
        files={k:"assets/"+v for k,v in R13_EP_BACKGROUNDS["ep_woodshed_inside"].items()})
    for _object,_rect in (("v111_wood",[656,309,563,290]),("v111_water",[490,470,180,160]),("v111_lamp",[1880,370,120,130])):
        ROOM13["objects"]["v111_woodshed"][_object]=dict(ROOM13["objects"]["v111_woodshed"][_object],rect=_rect)
    # 보호시설: 왼쪽 2048px은 원래 그림 그대로, 오른쪽에 벽 한 칸(벽화)을 이은 2560px 그림. 축척이 같아
    # 예전 조사 지점·자리 좌표는 그대로 맞고, 새 벽 칸에 자리 두 곳과 벽화 조사 지점을 더한다.
    _fac=R13_WORLD_LAYOUTS["facility"]
    _fac.update(width=2400,files={k:"assets/room13-pixel-wide-facility-%s.webp"%k for k in ("morning","afternoon","evening")})
    _fac["slots"]=list(_fac.get("slots",[]))+[[1960,684,252,"floor"],[2230,692,256,"floor"]]
    ROOM13["objects"]["facility"]["v111_mural"]=dict(ROOM13["objects"]["facility"]["v111_mural"],rect=[1940,80,380,560])
