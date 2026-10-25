# 2026-10-25 전체 13곳 납품 지도. 원본/좌표: design/resource-intake-20261025/map-apply/apply_handoff/.
# 배경과 라벨은 같은 균일 배율/뷰포트로 이동한다. 별칭은 기존 목록과 공개/이동 판정을 유지한다.
init 65 python:
    R13_VILLAGE_B_ART = "assets/map-village-b/"
    import json as village_b_json
    with renpy.file(R13_VILLAGE_B_ART+"layout.json") as village_b_file:
        R13_VILLAGE_B_LAYOUT = village_b_json.load(village_b_file)
    R13_VILLAGE_B_PLACES = {row["id"]:row for row in R13_VILLAGE_B_LAYOUT["locations"]}

    R13_VILLAGE_B_VIEW = (88,122,1136,506)

    def r13_village_b_focus(selected, zoom):
        base = globals().get("R13_V111_MAP_ALIASES",{}).get(selected,selected)
        row = R13_VILLAGE_B_PLACES.get(base,R13_VILLAGE_B_PLACES["square"])
        cx,cy = row["label_center"]
        return (max(0,min(1,(cx*zoom-568)/max(1,1642*zoom-1136))),
                max(0,min(1,(cy*zoom-253)/max(1,958*zoom-506))))

    def r13_village_b_rows():
        allowed = set(r13_places())
        rows = [(key, "open" if key in allowed else "shown") for key, point in r13_map_nodes("village")]
        seen = set(k for k, state in rows)
        rows.extend((key, "locked") for key, point in r13_map_locked_nodes("village") if key not in seen)
        return rows

    def r13_village_b_plate(primary=False):
        # 납품 trimmed 비율(일반 약 3.2:1/원본 label 3.5:1)을 유지하는 고정 크기 그림.
        return r13_asset_path("file:"+(R13_VILLAGE_B_ART + ("b_button_primary_trimmed.png" if primary else "b_button_trimmed.png")))

screen r13_village_b_control(label, rect, action, control_id, primary=False, enabled=True, chosen=False):
    $ bx,by,bw,bh=rect
    fixed:
        area (bx,by-((88 if r13_touch_ui() else 44)-bh)//2,bw,88 if r13_touch_ui() else 44)
        use r13_state_button(label,action,bw,88 if r13_touch_ui() else 44,family="map_flat_primary" if primary else "map_flat_standard",chosen=chosen,enabled=enabled,text_size=19,control_id=control_id)

screen r13_map_village_b(selected,ready,map_hover,map_notice,local_guide,close_action,extra_places,village_zoom):
    add Solid("#d9d7c6")
    $ rows=r13_village_b_rows()
    # 최소 배율도 창을 채우게 제한하여 좌우 빈틈을 만들지 않는다.
    $ zoom=max(village_zoom,1136.0/1642,506.0/958)
    $ fx,fy=r13_village_b_focus(selected,zoom)
    key "shift_K_LEFT" action Scroll("r13_map_view","horizontal decrease",160)
    key "shift_K_RIGHT" action Scroll("r13_map_view","horizontal increase",160)
    key "shift_K_UP" action Scroll("r13_map_view","vertical decrease",160)
    key "shift_K_DOWN" action Scroll("r13_map_view","vertical increase",160)
    viewport id "r13_map_view":
        area R13_VILLAGE_B_VIEW
        draggable True mousewheel True pagekeys True
        xinitial fx yinitial fy
        fixed:
            xysize (max(1136,int(1642*zoom)),max(506,int(958*zoom)))
            add Solid("#eae6d8")
            fixed:
                xysize (int(1642*zoom),int(958*zoom))
                xalign .5 yalign .5
                add Transform(r13_asset_path("file:assets/map-village-b/village_clean.png"),zoom=zoom)
                for key,state in rows:
                    if key in R13_VILLAGE_B_PLACES:
                        $ place=R13_VILLAGE_B_PLACES[key]
                        $ hx,hy,hw,hh=place["provisional_hit_rect"]
                        $ cx,cy=place["label_center"]
                        $ label=r13_map_label(key)
                        $ lw=max(144,len(label)*21+24)
                        $ choose = [SetScreenVariable("selected",key),SetScreenVariable("map_notice",None)] if state!="locked" else SetScreenVariable("map_notice",label+" · 지금은 이곳으로 갈 수 없습니다.")
                        button:
                            id ("map_building_"+key)
                            area (int(hx*zoom),int(hy*zoom),int(hw*zoom),int(hh*zoom)) padding (0,0)
                            background None hover_background None
                            action choose sensitive ready alt label
                        button:
                            id ("map_name_"+key)
                            area (int((cx-lw/2)*zoom),int((cy-19)*zoom),int(lw*zoom),int(38*zoom)) padding (0,0)
                            background None hover_background None
                            action choose sensitive ready alt label
                            fixed:
                                xysize (int(lw*zoom),int(38*zoom))
                                add Transform(Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10),xysize=(int(lw*zoom),int(38*zoom)))
                                text label font R13_UI_BOLD_FONT size max(12,int(20*zoom)) color ("#963b2f" if key==selected else "#493324" if state=="open" else "#88796b") align (.5,.5)
                # 공개된 행만 상태를 그린다. 미발견 장소에는 잠금 아이콘도 만들지 않는다.
                for key,state in rows:
                    if key in R13_VILLAGE_B_PLACES:
                        $ place=R13_VILLAGE_B_PLACES[key]
                        $ cx,cy=place["label_center"]
                        $ lw=max(144,len(r13_map_label(key))*21+24)
                        use r13_map_status_badges(key,state,selected,(int((cx-lw/2)*zoom),int((cy-19)*zoom),int(lw*zoom),int(38*zoom)))
    add r13_asset("file:assets/map-village-b/notebook_frame_1280x720.png")
    # 수첩 상단의 좁은 봉제선 대신 지도 창 안에 제목 전용 64px 공간을 확보한다.
    add Solid("#f7e8cd") xpos 88 ypos 58 xysize (1136,64)
    add Solid("#b99a6b") xpos 100 ypos 120 xysize (1112,2)
    # 기존 수첩 에셋으로 가볍게 꾸미고, 제목과 현재 위치를 한 줄에 정렬한다.
    add Transform(r13_asset_path("file:assets/map-village-b/b_tape_red.png"),zoom=.8,rotate=-8) xpos 112 ypos 67
    add Transform(r13_asset_path("file:assets/map-village-b/b_tape_teal.png"),zoom=.65,rotate=9) xpos 156 ypos 88
    fixed:
        area (360,62,540,54)
        hbox:
            align (.5,.5) spacing 12
            add Transform(Crop((16,16,32,32),r13_asset_path("file:assets/ui-b-field/b_icon_acorn.png")),zoom=1.0) yalign .5
            text "다람탐정 · 마을 지도" font R13_UI_BOLD_FONT size 28 color "#493324" yalign .5
    textbutton "×":
        id "r13_village_close_x"
        area ((1180,48,88,88) if r13_touch_ui() else (1190,64,48,48)) padding (0,0) background None
        text_xalign .5 text_yalign .5
        text_font R13_UI_BOLD_FONT text_size 28 text_color "#493324" text_align .5
        action close_action sensitive ready
    fixed:
        area (920,72,248,38)
        hbox:
            align (.5,.5) spacing 8
            add Transform(r13_asset_path("file:assets/map-status/current_location.png"),zoom=1.0/3) yalign .5
            text ("현재 · "+(r13_map_label(room13["location"]) if r13_map_discovered(room13["location"]) else "마을")) font R13_UI_BOLD_FONT size 18 color "#765b3e" yalign .5 xmaximum 212
    $ extras=[(key,state) for key,state in rows if key not in R13_VILLAGE_B_PLACES]
    if extras:
        add Solid("#f7e8cd") xpos 100 ypos 62 xysize (218,54)
        textbutton "다른 장소 ▾":
            id "r13_village_other_places"
            area (102,48 if r13_touch_ui() else 72,200,88 if r13_touch_ui() else 36) padding (0,0) background None
            text_yalign .5
            text_font R13_UI_BOLD_FONT text_size 20 text_color "#493324"
            action ToggleScreenVariable("extra_places") sensitive ready
    use r13_map_diary_footer("village",selected,ready,local_guide,close_action)
    $ meeting_venue=r13_meeting_map_venue(selected) if selected else None
    $ visible_notice=map_notice or ((meeting_venue[2]+(" · 모임 중" if r13_meeting_map_pending(selected) else "")) if meeting_venue else None)
    if visible_notice:
        frame:
            area (330,584,620,44) padding (12,6)
            background Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10)
            text visible_notice font R13_UI_BOLD_FONT size 19 color "#963b2f" align (.5,.5)
    if extra_places:
        # 뒤 버튼의 우발 선택을 막되 클릭 한 번으로 닫을 수 있는 공개 목적지 목록.
        button:
            area (0,58,1280,570) background Solid("#18243570")
            action SetScreenVariable("extra_places",False)
        frame:
            area (380,100,520,480) padding (24,20)
            background Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),16,16)
            vbox:
                spacing 8
                text "다른 장소" font R13_UI_BOLD_FONT size 26 color "#493324"
                viewport:
                    xysize (472,404) mousewheel True draggable True
                    vbox:
                        spacing 4
                        for key,state in extras:
                            textbutton r13_map_label(key):
                                id ("map_name_"+key)
                                xsize 472 ysize (88 if r13_touch_ui() else 60) padding (12,6)
                                background Solid("#ead8b866") hover_background Solid("#e0c19b99")
                                text_font R13_UI_BOLD_FONT text_size 24 text_color ("#493324" if state=="open" else "#88796b")
                                action ([SetScreenVariable("selected",key),SetScreenVariable("map_notice",None),SetScreenVariable("extra_places",False)] if state!="locked" else SetScreenVariable("map_notice",r13_map_label(key)+" · 지금은 이곳으로 갈 수 없습니다."))

screen r13_map_diary_footer(region,selected,ready,local_guide,close_action):
    fixed:
        area (102,643,180,40)
        add Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10) xysize (180,40)
        text ("선택: "+r13_map_label(selected) if selected else "장소를 선택하세요") font R13_UI_BOLD_FONT size 19 color "#493324" xmaximum 168 align (.5,.5) text_align .5
    if not local_guide:
        for key,title,rect in (("village","마을",(300,643,106,40)),("inn","여관 안",(416,643,120,40)),("mountain","숲·산길",(546,643,132,40))):
            if r13_map_nodes(key):
                use r13_village_b_control(title,rect,[SetScreenVariable("region",key),SetScreenVariable("selected",r13_map_selection(key,selected)),SetScreenVariable("map_hover",None),SetScreenVariable("map_notice",None)],"r13_map_region_"+key,enabled=ready,chosen=key==region)
    $ can_travel=selected and selected!=room13["location"] and (selected in dict(r13_local_connections()) if local_guide else selected in r13_places())
    use r13_village_b_control("이곳으로 이동",(704,643,184,40),[Hide("r13_inn_guide"),Return(("travel",selected))] if local_guide else Return(selected),"r13_map_travel",primary=True,enabled=ready and can_travel)
    use r13_village_b_control("현장으로",(902,643,142,40),close_action,"r13_map_close",enabled=ready)
    add Transform(r13_asset_path("file:assets/map-village-b/sticker_daram_stubborn.png"),xysize=(67,67),fit="contain") xpos 1137 ypos 631
