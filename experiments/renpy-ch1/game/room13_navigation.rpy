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
        if location in ("forest","facility","greenhouse","altar"):return "mountain"
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
            if key=="greenhouse":return bool(r13_v111_value("greenhouse_address_known") and r13_v111_value("tosil_safe_handoff_confirmed"))
            if key=="altar":return bool(r13_v111_value("altar_guide_confirmed"))
            if key=="passage":return bool(r13_v111_value("E09_PASSAGE"))
        # Do not expose secret names through stale/legacy current-location saves.
        if key=="ancient":return r13_ancient_open()
        if key=="passage":return bool(store.room13.get("passage_open") and r13_secret_route_available())
        if key=="greenhouse":return bool(store.room13["day"]>=R13_WEEK2_DAY and (r13_has("E19") or r13_has("Y03")))
        if key=="altar":return bool(store.room13.get("finale_started"))
        return True

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
    default selected=r13_map_selection(initial_region or r13_map_region(room13["location"]),room13["location"])
    default map_hover=None
    default map_notice=None
    default ready=False
    $ region = region if region in R13_MAP_NODES else "village"
    $ selected = r13_map_selection(region,selected)
    $ close_action = Function(r13_inn_guide_close) if local_guide else Return(False)
    key "game_menu" action close_action
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#2c211b")
    # 2026-10-24: 「여관 안」·「숲·산길」은 B 지도(수첩 틀 + 장소 스티커, game/room13_map_b.rpy).
    # 마을 탭은 마을 v2 납품 전까지 기존 그림 지도를 그대로 쓴다.
    if region=="village":
        use r13_cartography(region,selected,ready,map_hover)
    else:
        use r13_map_b(region,selected,ready,map_hover,map_notice)
    # B 지도는 구역 이름·현재 위치·안내를 수첩 아래 띠에 쓴다. 마을만 왼쪽 위 이름판과 안내 줄을 쓴다.
    if region=="village":
        add Frame(R13_NIGHT_UI+"panel_small.png",12,12) xpos 24 ypos 20 xysize (250,76)
        fixed:
            area (46,20,206,76)
            vbox:
                yalign .5 spacing 5
                text "마을 지도" size 29 color "#f6ecd8"
                text ("현재 · "+(R13_MAP_LABELS.get(room13["location"],"마을") if r13_map_discovered(room13["location"]) else "마을")) size 17 color "#d9c9ac" xsize 206
        frame:
            area (24,548,1232,48) padding (20,8)
            background Frame(R13_NIGHT_UI+"panel_small.png",12,12)
            text (map_notice or r13_map_input_hint(region)) size (24 if r13_touch_ui() else 20) color "#e3d6bd" yalign .5
    add Frame(R13_NIGHT_UI+"panel_small.png",12,12) xpos 24 ypos 602 xysize (1232,110)
    # Center every map control in the same footer, including 88px touch targets.
    $ map_controls_y=602+(110-r13_map_control_height())//2
    if selected:
        text r13_map_label(selected) xpos 48 ypos 627 size 27 color "#f6ecd8"
        $ meeting_venue=r13_meeting_map_venue(selected)
        text (("● 현재 위치" if selected==room13["location"] else "선택됨")+(" · "+meeting_venue[2] if meeting_venue else " · 이동 버튼으로 확정")+(" · 모임 중" if meeting_venue and r13_meeting_map_pending(selected) else "")) xpos 48 ypos 663 size 17 color "#d9b46c" xsize 302
        $ can_travel=selected!=room13["location"] and (selected in dict(r13_local_connections()) if local_guide else selected in r13_places())
        fixed:
            area (r13_control_x(3)-24,map_controls_y,R13_CONTROL["width"],r13_map_control_height())
            use r13_control("이곳으로 이동","map",[Hide("r13_inn_guide"),Return(("travel",selected))] if local_guide else Return(selected),enabled=ready and can_travel,primary=True,height=r13_map_control_height(),control_id="r13_map_travel")
    else:
        text "아직 확인한 장소가 없습니다." xpos 48 ypos 642 size 22 color "#d9c9ac"
    if not local_guide:
        hbox:
            xpos 366 ypos map_controls_y spacing 8
            for key,title in R13_MAP_REGIONS:
                if r13_map_nodes(key):
                    textbutton title:
                        id ("r13_map_region_"+key)
                        style "r13_action_button" xsize 116 ysize r13_map_control_height() padding (8,8) text_size 19
                        background Frame(R13_NIGHT_UI+("opt_btn_selected.png" if region==key else "opt_btn_idle.png"),16,16)
                        hover_background Frame(R13_NIGHT_UI+"opt_btn_hover.png",16,16)
                        text_color "#e3d6bd" text_hover_color "#fff6e2"
                        text_xalign .5 text_yalign .5
                        action [SetScreenVariable("region",key),SetScreenVariable("selected",r13_map_selection(key,selected)),SetScreenVariable("map_hover",None),SetScreenVariable("map_notice",None)]
                        selected region==key sensitive ready
    fixed:
        area (r13_control_x(4)-24,map_controls_y,R13_CONTROL["width"],r13_map_control_height())
        use r13_control("현장으로","dialogue",close_action,enabled=ready,height=r13_map_control_height(),control_id="r13_map_close")
