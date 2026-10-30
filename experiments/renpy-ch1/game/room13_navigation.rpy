default persistent.room13_map_list = False

# Spatial navigation: selecting a pin never travels or spends time.
init 60 python:
    R13_MAP_REGIONS = (("village", "마을"), ("inn", "여관 안"), ("mountain", "숲·산길"))
    R13_MAP_NODES = {
        "village": {"gate":(132,354), "square":(336,250), "inn":(715,299),
            "post":(466,172), "workshop":(585,425), "clinic":(407,370),
            "school":(95,143), "store":(553,292),
            # 0.18.63 new places; init 61 replaces these with the v5 map points.
            "river":(267, 375), "forest":(82, 406), "market":(561, 319),
            # 0.20.11 widened village map: Somi's riverside house and the laundry have their own places.
            "somi":(0,0), "laundry":(0,0)},
        "inn": {"inn":(435,420), "dining":(434,307), "kitchen":(170,307),
            "hall":(340,120), "room13":(685,120), "passage":(685,40), "guestroom":(245,65), "ancient":(685,0)},
        "mountain": {"forest":(180,300), "facility":(110,135), "greenhouse":(382,108), "altar":(644,100)},
    }
    R13_MAP_LABELS = {"gate":"마을 입구", "square":"광장", "inn":"여관 접수대",
        "post":"우체국", "workshop":"수리점", "clinic":"진료실", "school":"학교",
        "store":"공동 창고", "dining":"식당", "kitchen":"주방", "hall":"2층 복도",
        "room13":"13호실", "guestroom":"임시 객실", "passage":"숨은 통로", "facility":"보호시설",
        "greenhouse":"폐온실", "altar":"산속 제단"}

    R13_INN_LOCATIONS=("inn","dining","kitchen","hall","room13","passage","guestroom","ancient")
    R13_LOCAL_CONNECTIONS={
        "inn":(("dining","식당"),("kitchen","주방"),("hall","2층 복도"),("outside","여관 밖으로")),
        "dining":(("inn","접수대"),("kitchen","주방")),
        "kitchen":(("dining","식당"),("inn","접수대")),
        "hall":(("inn","1층 접수대"),("room13","13호실"),("guestroom","임시 객실")),
        "room13":(("hall","복도로"),("passage","숨은 통로")),
        "guestroom":(("hall","복도로"),),
        "passage":(("room13","13호실로"),),
    }

    def r13_local_connections():
        allowed=set(r13_places())
        return [(key,title) for key,title in R13_LOCAL_CONNECTIONS.get(store.room13["location"],())
            if key=="outside" or key in allowed]

    def r13_local_destination(key):
        # Validate again at dispatch, including after a saved interaction resumes.
        return key if key in dict(r13_local_connections()) else None

    def r13_map_control_height():
        # 740x360 landscape: 88 virtual px equals a 44 CSS-px finger target.
        return max(88,r13_control_height()) if r13_touch_ui() else r13_control_height()

    def r13_map_label(key):
        """Connect the spoken destination with its map name only during that trip."""
        state=store.room13
        story=state.get("v111",{})
        going_to_box=(story.get("gate")=="go_box" or
            (story.get("gate")=="travel" and story.get("scene")=="MS14_D02_S01"
                and story.get("travel_to")=="forest"
                and not story.get("values",{}).get("mother_box_checked_day2")))
        if (key=="forest" and state.get("day")==2
                and globals().get("r13_v111_active",lambda:False)()
                and going_to_box
                and key in r13_places()):
            return R13_MAP_LABELS[key]+" · 교환함"
        return R13_MAP_LABELS[key]

    def r13_map_input_hint(region):
        if region=="village":
            if r13_touch_ui():
                return "지도를 손가락으로 끌어 둘러보세요. 테두리 장소 선택 후 이동으로 확정합니다."
            return "드래그·휠 / Shift+방향키·PgUp·PgDn으로 둘러보기 · 장소 선택 후 이동으로 확정"
        return "테두리가 있는 곳은 이동할 수 있습니다. 장소를 고른 뒤 이동을 누르세요."

    def r13_map_region(location):
        if location in R13_INN_LOCATIONS:return "inn"
        if location in ("forest","facility","greenhouse","altar","hidden_base14"):return "mountain"
        return "village"

    def r13_map_nodes(region):
        allowed=set(r13_places())|{store.room13["location"]}
        rows=[(key,point) for key,point in R13_MAP_NODES[region].items()
            if key in allowed and r13_map_discovered(key)]
        if globals().get("r13_v111_active",lambda:False)():
            destination=store.room13.get("v111",{}).get("travel_to") if store.room13.get("v111",{}).get("gate")=="travel" else None
            if destination and destination in dict(rows):
                aliases=globals().get("R13_V111_MAP_ALIASES",{})
                footprint=aliases.get(destination,destination)
                rows=[(k,p) for k,p in rows if k==destination or aliases.get(k,k)!=footprint]
        return rows

    def r13_map_locked_nodes(region):
        """Public places drawn on the map can explain a closed route without unlocking it.
        Aliased story locations and undiscovered secret sites must not leak through this UI.
        """
        if region not in ("village","mountain"):return []
        aliases=globals().get("R13_V111_MAP_ALIASES",{})
        active={aliases.get(key,key) for key,point in r13_map_nodes(region)}
        return [(key,point) for key,point in R13_MAP_NODES[region].items()
            if key not in aliases and key not in active and key not in ("greenhouse","altar") and r13_map_discovered(key)]

    def r13_map_discovered(key):
        if globals().get("r13_v111_active",lambda:False)():
            if key=="hidden_pandol":return bool(r13_v111_value("hidden_pandol:visit_allowed"))
            if key=="greenhouse":return bool(r13_v111_value("greenhouse_address_known") and r13_v111_value("tosil_safe_handoff_confirmed"))
            if key=="altar":return bool(r13_v111_value("altar_guide_confirmed"))
            if key=="passage":return bool(r13_v111_value("E09_PASSAGE"))
        # Do not expose secret names through stale/legacy current-location saves.
        if key=="ancient":return r13_ancient_open()
        if key=="passage":return bool(store.room13.get("passage_open") and r13_secret_route_available())
        if key=="greenhouse":return bool(store.room13["day"]>=R13_WEEK2_DAY and (r13_has("E19") or r13_has("Y03")))
        if key=="altar":return bool(store.room13.get("finale_started"))
        return True

    def r13_map_initial_pick():
        v=store.room13.get("v111",{}) if globals().get("r13_v111_active",lambda:False)() else {}
        target=v.get("travel_to") if v.get("gate")=="travel" else None
        if target and any(key==target for key,point in r13_map_nodes(r13_map_region(target))):
            return target
        return store.room13["location"]

    def r13_map_selection(region,selected):
        keys=[key for key,point in r13_map_nodes(region)]
        if selected in keys:return selected
        current=store.room13["location"]
        if current in keys:return current
        return next((key for key in keys if key in r13_places()),keys[0] if keys else None)

    def r13_location_path(location=None):
        location=location or store.room13["location"]
        if not r13_map_discovered(location):return "마을"
        title=R13_MAP_LABELS.get(location,R13_PLACES[location][0])
        if location=="ancient":return "마을 › 여관 › 지하 › "+title
        if location in R13_INN_LOCATIONS:
            return "마을 › 여관 › "+("접수대" if location=="inn" else title)
        if location in ("facility","greenhouse","altar"):
            return "마을 › 북쪽 산길 › "+title
        return "마을 › "+title

screen r13_map(initial_region=None, local_guide=False):
    style_prefix "r13"
    modal True
    zorder 45
    default region=initial_region or r13_map_region(room13["location"])
    # 2026-10-30 눈가림 플레이: 이동할 차례에 지도가 지금 자리(솜이네)를 비추며 열려, 열려 있는 목적지(입구)가
    # 화면 밖에 있었고 끌어 옮길 수 있다는 표시도 없어 4일 저녁에 진행이 막혔다. 이동 차례면 목적지를 골라 둔 채 연다.
    default selected=r13_map_selection(initial_region or r13_map_region(room13["location"]),r13_map_initial_pick())
    default map_hover=None
    default map_notice=None
    default extra_places=False
    # 2026-10-27: 1.15 에서는 처음 열린 화면의 가장자리에 이름표가 걸리지 않는 가로 위치가 없다(r13_village_b_clean_scrolls). 1.0 으로.
    default village_zoom=1.0
    default ready=False
    $ region = region if region in R13_MAP_NODES else "village"
    $ selected = r13_map_selection(region,selected)
    $ close_action = Function(r13_inn_guide_close) if local_guide else Return(False)
    key "game_menu" action close_action
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#243349")
    # 납품 B 마을 지도는 자체 수첩·조작 줄을 쓴다. 기존 이동 판정/반환은 공유한다.
    if region=="village":
        use r13_map_village_b(selected,ready,map_hover,map_notice,local_guide,close_action,extra_places,village_zoom)
    else:
        add r13_asset("file:assets/map-village-b/notebook_frame_1280x720.png")
        add Solid("#fff0d4") xpos 88 ypos 58 xysize (1136,570)
        fixed:
            ypos 70
            use r13_map_b(region,selected,ready,map_hover,map_notice)
        text ("다람탐정 · "+("여관 지도" if region=="inn" else "숲·산길 지도")) xpos 640 ypos 78 xanchor .5 size r13_type("subtitle") font R13_UI_BOLD_FONT color "#29364b"
        use r13_map_close_x(close_action,ready)
        use r13_map_diary_footer(region,selected,ready,local_guide,close_action)
        if map_notice:
            frame:
                area (330,584,620,44) padding (12,6) background r13_sticker_button()
                text map_notice font R13_UI_BOLD_FONT size r13_type("small") color "#963b2f" align (.5,.5)
