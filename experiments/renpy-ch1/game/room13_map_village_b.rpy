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

    def r13_village_b_label_px():
        # 2026-10-27 소유자 「마을지도 글씨가 너무 큼」: 장소 이름표를 body(24) 에서 small(22) 로 내린다.
        # 휴대폰은 r13_type 이 26 을 주지만 같은 지적이 그대로 보이므로 PC 단계값(22, 크게 26)으로 맞춘다.
        # 다만 20 아래로는 내리지 않는다 — 휴대폰 가로(844x390)에서 20 이 약 10px 이라 그 밑이면 읽히지 않는다(0.20.67).
        ls=1.3 if r13_touch_ui() else 1.0
        px=(r13_type("small") if R13_TYPE_V2 else 20*ls)
        if R13_TYPE_V2 and r13_touch_ui():
            px=r13_read_size(22,26)
        return max(20,px) if R13_TYPE_V2 else px

    def r13_village_b_label_width(label,scaled=True):
        # 이름표 폭은 그 글자 크기로 잰다(글자당 px+1). 꺼짐 동등성: 이름표 버튼은 터치 배율을 곱했고 배지 자리는 안 곱했다.
        px=r13_village_b_label_px()
        if R13_TYPE_V2:
            return max(144,len(label)*(px+1)+24)
        return max(144,len(label)*21+24)*((1.3 if r13_touch_ui() else 1.0) if scaled else 1.0)

    class R13VillageBSurface(renpy.Displayable):
        """지도 하단 조작(선택 표시판·지역 탭·이동·현장으로)이 함께 쓰는 한 가지 판.

        2026-10-27 소유자 「버튼 크기·폰트가 각각이고 글씨가 눌린다」: 공통 R13ButtonStateVisual 은 160x52 원본의
        비율(3.4:1)을 지키려고 버튼 안에 더 작은 종이를 놓고(「마을」 106x44 → 종이 31px) 글자를 그 종이에 맞춰
        Transform(zoom) 으로 줄였다. 그래서 같은 줄에서 종이 높이가 31·42·44 로 갈리고 「마을」만 20px 로 흐릿하게
        눌렸다. 그림을 늘이지도 글자를 줄이지도 않고 칸 크기 그대로 캔버스에 그린다 — 평면 버튼 자산과 같은 모양
        (둥근 네모·남색 2px 테두리·빨강/크림 면). 보조 버튼은 R13_SOFT_FLAT_BUTTONS 가 켜진 동안 같은 연한 판을 쓴다."""
        PRIMARY={"basic":("#d9434c","#c74850"),"pressed":("#b8323e","#a83641"),"selected":("#c12f3f","#b03441"),"disabled":("#d6b9b7","#d3bab8")}
        STANDARD={"basic":"#fff5e3","pressed":"#e8dfcd","selected":"#dce8f0","disabled":"#eae6dc"}
        def __init__(self,primary=False,chosen=False,hovered=False,disabled=False,**kwargs):
            super(R13VillageBSurface,self).__init__(**kwargs)
            self.primary=primary;self.chosen=chosen;self.hovered=hovered;self.disabled=disabled
            self.soft=R13SoftButtonSurface(hovered=hovered,chosen=chosen,disabled=disabled)
        def visit(self):
            return [self.soft]
        def render(self,width,height,st,at):
            w=max(1,int(width));h=max(1,int(height));r=renpy.Render(w,h)
            soft=getattr(store,"R13_SOFT_FLAT_BUTTONS",False)
            if not self.primary and soft:
                r.blit(renpy.render(self.soft,w,h,st,at),(0,0))
                return r
            state="disabled" if self.disabled else "pressed" if self.hovered else "selected" if self.chosen else "basic"
            if self.primary:
                face=self.PRIMARY[state][1 if soft else 0]  # 켜진 동안은 채도 .85 (SaturationMatrix 와 같은 값)
            else:
                face=self.STANDARD[state]
            edge="#a9adb0" if self.disabled else "#293c53"
            c=r.canvas();rad=min(10,h//3)
            for (x,y,ww,hh,col) in ((0,0,w,h,edge),(2,2,w-4,h-4,face)):
                c.rect(col,(x+rad,y,ww-2*rad,hh));c.rect(col,(x,y+rad,ww,hh-2*rad))
                for cx,cy in ((x+rad,y+rad),(x+ww-rad-1,y+rad),(x+rad,y+hh-rad-1),(x+ww-rad-1,y+hh-rad-1)):
                    c.circle(col,(cx,cy),rad)
            return r

    def r13_village_b_control_text():
        # 네 조작의 공통 글자 크기. 2026-10-27 외부 평가: 휴대폰 가로에서 19는 약 10px 로 줄어 읽기 어려웠다.
        return (r13_type("body") if R13_TYPE_V2 else (26 if r13_touch_ui() else 19))

screen r13_village_b_control(label, rect, action, control_id, primary=False, enabled=True, chosen=False):
    # 지도 하단 조작. 칸을 그대로 쓰는 판(R13VillageBSurface) 위에 글자를 줄이지 않고 놓는다. 글자가 안 들어가면
    # 칸을 넓힌다 — 폭은 r13_map_diary_footer 의 표에서 큰 글씨·휴대폰(30px)까지 실측해 둔 값이다.
    # 높이는 PC 44 / 휴대폰 88(740x360 가로에서 44 CSS px 손가락 표적). 줄의 중심선 663 은 그대로.
    $ bx,by,bw,bh=rect
    button:
        id control_id
        area (bx,by-((88 if r13_touch_ui() else 44)-bh)//2,bw,88 if r13_touch_ui() else 44)
        padding (0,0)
        background R13VillageBSurface(primary=primary,chosen=chosen)
        hover_background R13VillageBSurface(primary=primary,chosen=chosen,hovered=True)
        insensitive_background R13VillageBSurface(primary=primary,disabled=True)
        activate_sound ("<volume 0.65>"+r13_asset_path("file:assets/diary-sounds/paper-selection.mp3"))
        action action sensitive enabled selected chosen alt label
        text label font R13_UI_BOLD_FONT size r13_village_b_control_text() color ("#8b8175" if not enabled else "#fff5e5" if primary else ("#4b3420" if getattr(store,"R13_SOFT_FLAT_BUTTONS",False) else "#263953")) align (.5,.5) text_align .5

screen r13_village_b_plate(label, rect):
    # 「선택: …」 표시판. 누르는 것이 아니지만 같은 줄의 버튼과 같은 높이·글자·테두리를 쓴다(2026-10-27 소유자 「통일」).
    $ bx,by,bw,bh=rect
    fixed:
        area (bx,by-((88 if r13_touch_ui() else 44)-bh)//2,bw,88 if r13_touch_ui() else 44)
        add R13VillageBSurface() xysize (bw,88 if r13_touch_ui() else 44)
        text label font R13_UI_BOLD_FONT size r13_village_b_control_text() color (r13_type_color("ink") if R13_TYPE_V2 else "#493324") align (.5,.5) text_align .5

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
                        # 터치 화면에서는 이름표 칸(클릭 영역)을 1.3배로 유지한다. 글자 크기는 r13_village_b_label_px —
                        # 2026-10-27 소유자 「글씨가 너무 큼」으로 body→small, 휴대폰도 PC 값으로.
                        $ ls=1.3 if r13_touch_ui() else 1.0
                        $ lpx=r13_village_b_label_px()
                        $ lw=r13_village_b_label_width(label)
                        $ choose = [SetScreenVariable("selected",key),SetScreenVariable("map_notice",None)] if state!="locked" else SetScreenVariable("map_notice",label+" · 지금은 이곳으로 갈 수 없습니다.")
                        button:
                            id ("map_building_"+key)
                            area (int(hx*zoom),int(hy*zoom),int(hw*zoom),int(hh*zoom)) padding (0,0)
                            background None hover_background None
                            action choose sensitive ready alt label
                        button:
                            id ("map_name_"+key)
                            area (int((cx-lw/2)*zoom),int((cy-19*ls)*zoom),int(lw*zoom),int(38*ls*zoom)) padding (0,0)
                            background None hover_background None
                            action choose sensitive ready alt label
                            fixed:
                                xysize (int(lw*zoom),int(38*ls*zoom))
                                add Transform(Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10),xysize=(int(lw*zoom),int(38*ls*zoom)))
                                text label font R13_UI_BOLD_FONT size max(12,int(lpx*zoom)) color ((r13_type_color("accent") if R13_TYPE_V2 else "#963b2f") if key==selected else (r13_type_color("ink") if R13_TYPE_V2 else "#493324") if state=="open" else (r13_type_color("disabled") if R13_TYPE_V2 else "#88796b")) align (.5,.5)
                # 공개된 행만 상태를 그린다. 미발견 장소에는 잠금 아이콘도 만들지 않는다.
                for key,state in rows:
                    if key in R13_VILLAGE_B_PLACES:
                        $ place=R13_VILLAGE_B_PLACES[key]
                        $ cx,cy=place["label_center"]
                        $ lw=r13_village_b_label_width(r13_map_label(key),scaled=False)
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
            text "다람탐정 · 마을 지도" font R13_UI_BOLD_FONT size (r13_type("subtitle") if R13_TYPE_V2 else 28) color (r13_type_color("ink") if R13_TYPE_V2 else "#493324") yalign .5
    textbutton "×":
        id "r13_village_close_x"
        area ((1180,48,88,88) if r13_touch_ui() else (1176,56,62,62)) padding (0,0)
        # 2026-10-26 소유자: 「X 버튼이 너무 작고 눈에 안 띈다」. 다른 버튼과 같은 판 위에 크게 둔다.
        background R13ControlSurface() hover_background R13ControlSurface(hovered=True) insensitive_background R13ControlSurface(disabled=True)
        text_xalign .5 text_yalign .5
        text_font R13_UI_BOLD_FONT text_size 40 text_color "#493324" text_hover_color "#963b2f" text_align .5
        action close_action sensitive ready
    fixed:
        area (920,72,248,38)
        hbox:
            align (.5,.5) spacing 8
            add Transform(r13_asset_path("file:assets/map-status/current_location.png"),zoom=1.0/3) yalign .5
            text ("현재 · "+(r13_map_label(room13["location"]) if r13_map_discovered(room13["location"]) else "마을")) font R13_UI_BOLD_FONT size (r13_type("small") if R13_TYPE_V2 else 18) color (r13_type_color("muted") if R13_TYPE_V2 else "#765b3e") yalign .5 xmaximum 212
    $ extras=[(key,state) for key,state in rows if key not in R13_VILLAGE_B_PLACES]
    if extras:
        add Solid("#f7e8cd") xpos 100 ypos 62 xysize (218,54)
        textbutton "다른 장소 ▾":
            id "r13_village_other_places"
            area (102,48 if r13_touch_ui() else 72,200,88 if r13_touch_ui() else 36) padding (0,0) background None
            text_yalign .5
            text_font R13_UI_BOLD_FONT text_size (r13_type("body") if R13_TYPE_V2 else 20) text_color (r13_type_color("ink") if R13_TYPE_V2 else "#493324")
            action ToggleScreenVariable("extra_places") sensitive ready
    use r13_map_diary_footer("village",selected,ready,local_guide,close_action)
    $ meeting_venue=r13_meeting_map_venue(selected) if selected else None
    $ visible_notice=map_notice or ((meeting_venue[2]+(" · 모임 중" if r13_meeting_map_pending(selected) else "")) if meeting_venue else None)
    if visible_notice:
        frame:
            area (330,584,620,44) padding (12,6)
            background Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10)
            text visible_notice font R13_UI_BOLD_FONT size (r13_type("body") if R13_TYPE_V2 else 19) color (r13_type_color("accent") if R13_TYPE_V2 else "#963b2f") align (.5,.5)
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
                text "다른 장소" font R13_UI_BOLD_FONT size (r13_type("subtitle") if R13_TYPE_V2 else 26) color (r13_type_color("ink") if R13_TYPE_V2 else "#493324")
                viewport:
                    xysize (472,404) mousewheel True draggable True
                    vbox:
                        spacing 4
                        for key,state in extras:
                            textbutton r13_map_label(key):
                                id ("map_name_"+key)
                                xsize 472 ysize (88 if r13_touch_ui() else 60) padding (12,6)
                                background Solid("#ead8b866") hover_background Solid("#e0c19b99")
                                text_font R13_UI_BOLD_FONT text_size (r13_type("body") if R13_TYPE_V2 else 24) text_color ((r13_type_color("ink") if R13_TYPE_V2 else "#493324") if state=="open" else (r13_type_color("disabled") if R13_TYPE_V2 else "#88796b"))
                                action ([SetScreenVariable("selected",key),SetScreenVariable("map_notice",None),SetScreenVariable("extra_places",False)] if state!="locked" else SetScreenVariable("map_notice",r13_map_label(key)+" · 지금은 이곳으로 갈 수 없습니다."))

# 하단 한 줄(y 643, 높이 PC 44 / 휴대폰 88). 폭은 Pretendard Bold 실측(진행폭)으로 가장 큰 글자(휴대폰 크게 30px)
# 가 좌우 8px 여유를 두고 들어가게 잡았다 — 선택판 「장소를 선택하세요」 214 → 232, 「마을」 52 → 112,
# 「여관 안」 85 → 124, 「숲·산길」 86 → 128, 「이곳으로 이동」 162 → 196, 「현장으로」 104 → 136. 간격 12.
# 글자가 더 길어지면 칸을 넓힌다. 글자를 줄이거나 늘이지 않는다(2026-10-27 소유자).
screen r13_map_diary_footer(region,selected,ready,local_guide,close_action):
    use r13_village_b_plate(("선택: "+r13_map_label(selected) if selected else "장소를 선택하세요"),(102,643,232,40))
    if not local_guide:
        for key,title,rect in (("village","마을",(346,643,112,40)),("inn","여관 안",(470,643,124,40)),("mountain","숲·산길",(606,643,128,40))):
            if r13_map_nodes(key):
                use r13_village_b_control(title,rect,[SetScreenVariable("region",key),SetScreenVariable("selected",r13_map_selection(key,selected)),SetScreenVariable("map_hover",None),SetScreenVariable("map_notice",None)],"r13_map_region_"+key,enabled=ready,chosen=key==region)
    $ can_travel=selected and selected!=room13["location"] and (selected in dict(r13_local_connections()) if local_guide else selected in r13_places())
    use r13_village_b_control("이곳으로 이동",(746,643,196,40),[Hide("r13_inn_guide"),Return(("travel",selected))] if local_guide else Return(selected),"r13_map_travel",primary=True,enabled=ready and can_travel)
    use r13_village_b_control("현장으로",(954,643,136,40),close_action,"r13_map_close",enabled=ready)
    add Transform(r13_asset_path("file:assets/map-village-b/sticker_daram_stubborn.png"),xysize=(67,67),fit="contain") xpos 1137 ypos 631
