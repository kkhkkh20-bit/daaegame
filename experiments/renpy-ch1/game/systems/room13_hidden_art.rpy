# 판돌 집·옛 시설 정비실 전용 배경과 물건 그림(2026-10-26 납품, 신규그림27).
# 지금까지는 솜이네 방·옛 시설 배경을 빌려 썼다. 납품 안내대로 장면 단계마다 다른 그림이라,
# 같은 장소 안에서 단계에 따라 배경과 조사 자리를 함께 바꾼다. 대사·진행 조건은 그대로다.
#   판돌 집: 7일은 문간(쟁반·문 안쪽 손), 11일 방문부터 실내(안쪽 돌), 돌을 바꾼 뒤 장작불.
#   정비실: 문을 열기 전 닫힌 문, 연 뒤 열린 문, 정비실 단계(hidden_base_room14)는 실내.
# 판돌 누나 그림(HIDDEN-P3)은 이름이 정해진 뒤 연결한다(지금은 지문 속 목소리).
# 물건 그림(숟가락·핀·종이·판·단면판·점검표·수첩)은 대사 줄의 ev: 컷으로 보인다(assets/evidence/HIDDEN_*).
init 325 python:
    R13_HIDDEN_ART={
        "hidden_pandol":{
            "door":("assets/hidden-places/hidden-p1-doorway.webp",dict(
                hp_table=[980,300,360,130],hp_stove=[1450,60,250,490],hp_wood=[1690,340,180,200],hp_tongs=[1300,120,130,160])),
            "inner":("assets/hidden-places/hidden-p2-inner.webp",dict(
                hp_table=[270,330,260,200],hp_stove=[1350,280,250,230],hp_wood=[1035,420,215,110],hp_tongs=[1630,190,70,160])),
            "wood":("assets/hidden-places/hidden-p2-wood.webp",None),
        },
        "hidden_base14":{
            "closed":("assets/hidden-places/hidden-a1-closed.webp",dict(
                hb_door=[1220,80,420,480],hb_section=[40,260,215,275],hb_incident=[1070,300,250,220],hb_notebook=[1870,540,160,95])),
            "open":("assets/hidden-places/hidden-a1-open.webp",None),
            "room":("assets/hidden-places/hidden-a2-interior.webp",dict(
                hb_door=[1900,140,220,330],hb_section=[40,260,215,275],hb_incident=[1070,300,250,220],hb_notebook=[1870,540,160,95])),
        },
    }
    for _ha_loc in R13_HIDDEN_ART:
        _ha_spec=R13_WORLD_LAYOUTS[_ha_loc]
        _ha_spec.pop("state_files",None)
        _ha_spec["crops"]={p:[0,0,2170,724] for p in ("morning","afternoon","evening")}
        _ha_spec["files"]={p:R13_HIDDEN_ART[_ha_loc]["door" if _ha_loc=="hidden_pandol" else "closed"][0] for p in ("morning","afternoon","evening")}
    R13_WORLD_LAYOUTS["hidden_pandol"]["initial_x"]=520
    R13_WORLD_LAYOUTS["hidden_base14"]["initial_x"]=700

    def r13_hidden_art_phase(location):
        if location=="hidden_pandol":
            if store.room13.get("day",1)<11:return "door"
            return "wood" if r13_hp_value("heat_replaced") else "inner"
        if location=="hidden_base14":
            if (store.room13.get("v111") or {}).get("gate")=="hidden_base_room14":return "room"
            return "open" if r13_hidden_base_value("opened") else "closed"
        return None

    def r13_hidden_art_sync(location):
        """단계에 맞는 조사 자리를 그 장소의 물건 표에 옮긴다. 그림이 같은 단계(장작불·열린 문)는 앞 단계 자리를 쓴다."""
        phase=r13_hidden_art_phase(location)
        table=R13_HIDDEN_ART[location]
        rects=table[phase][1] or table["inner" if phase=="wood" else "closed"][1]
        for key,rect in rects.items():
            if key in ROOM13["objects"][location]:ROOM13["objects"][location][key]["rect"]=list(rect)
        return table[phase][0]

    _r13_hidden_art_file=r13_world_file
    def r13_world_file(location,period):
        if location in R13_HIDDEN_ART:return r13_hidden_art_sync(location)
        return _r13_hidden_art_file(location,period)

    # 정비실은 옛 시설과 장면 키를 같이 쓴다. 키로 장소를 찾으면 옛 시설이 먼저 나와
    # 대사 장면에서 옛 배경이 보이므로, 지금 있는 숨은 장소를 먼저 본다.
    _r13_hidden_art_scene=r13_world_scene_location
    def r13_world_scene_location(key):
        location=(store.room13 or {}).get("location")
        if location in R13_HIDDEN_ART and R13_PLACES.get(location,(None,None))[1]==key:return location
        return _r13_hidden_art_scene(key)
