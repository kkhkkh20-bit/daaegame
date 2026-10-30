# 2026-10-25 전체 13곳 납품 지도. 원본/좌표: design/resource-intake-20261025/map-apply/apply_handoff/.
# 배경과 라벨은 같은 균일 배율/뷰포트로 이동한다. 별칭은 기존 목록과 공개/이동 판정을 유지한다.
init 65 python:
    R13_VILLAGE_B_ART = "assets/map-village-b/"
    import json as village_b_json
    with renpy.file(R13_VILLAGE_B_ART+"layout.json") as village_b_file:
        R13_VILLAGE_B_LAYOUT = village_b_json.load(village_b_file)
    R13_VILLAGE_B_PLACES = {row["id"]:row for row in R13_VILLAGE_B_LAYOUT["locations"]}

    R13_VILLAGE_B_VIEW = (88,122,1136,506)

    def r13_village_b_label_boxes(zoom,touch=None):
        """장소 이름표마다 (왼쪽, 위, 오른쪽, 아래) — 지도 그림 좌표(배율 전). 화면 쪽 이름표 칸과 같은 식이다."""
        if touch is None:touch=r13_touch_ui()
        ls=1.3 if touch else 1.0
        out={}
        for key,place in R13_VILLAGE_B_PLACES.items():
            cx,cy=place["label_center"]
            lw=r13_village_b_label_width(r13_map_label(key))
            out[key]=(cx-lw/2.0,cy-19*ls,cx+lw/2.0,cy+19*ls)
        return out

    def r13_village_b_clean_scrolls(zoom,touch=None):
        """이름표가 보기 창 가장자리에 걸리지 않는 스크롤 위치(그림 좌표, 정수)의 목록을 축마다 돌려준다.

        2026-10-27 소유자: 처음 열린 지도에서 오른쪽 위 「수리점」이 수첩 판 가장자리에서 반쯤 잘려 보였다.
        보기 창이 그림보다 좁아 끌어 보는 지도라 어느 위치든 걸치는 이름표가 생길 수 있지만, 적어도 처음 보이는
        화면만은 모든 이름표가 통째로 보이거나 통째로 숨어야 한다. 1.15 배율에서는 가로로 그런 위치가 하나도 없어서
        기본 배율을 1.0 으로 내렸다(이름표 글자도 25→22px 로 같이 작아진다 — 「글씨가 너무 큼」 지적과 같은 방향)."""
        boxes=r13_village_b_label_boxes(zoom,touch)
        vw,vh=R13_VILLAGE_B_VIEW[2]/float(zoom),R13_VILLAGE_B_VIEW[3]/float(zoom)
        def clean(axis,view,total):
            lo,hi=(0,2) if axis==0 else (1,3)
            spans=[(b[lo],b[hi]) for b in boxes.values()]
            limit=int(max(0,total-view))
            return [s for s in range(0,limit+1)
                    if all(not (a<s<b) and not (a<s+view<b) for a,b in spans)]
        return clean(0,vw,1642),clean(1,vh,958)

    def r13_village_b_focus(selected, zoom):
        base = globals().get("R13_V111_MAP_ALIASES",{}).get(selected,selected)
        row = R13_VILLAGE_B_PLACES.get(base,R13_VILLAGE_B_PLACES["square"])
        cx,cy = row["label_center"]
        # 바라는 위치: 고른 장소를 가운데에. 그 다음 이름표가 창 가장자리에 걸리지 않는 가장 가까운 위치로 당긴다.
        # 그런 위치가 없는 축은 바라는 위치 그대로 둔다(잘리는 것보다 엉뚱한 곳이 보이는 쪽이 더 나쁘다).
        vw,vh=R13_VILLAGE_B_VIEW[2]/float(zoom),R13_VILLAGE_B_VIEW[3]/float(zoom)
        want_x=max(0,min(1642-vw,cx-vw/2.0));want_y=max(0,min(958-vh,cy-vh/2.0))
        xs,ys=r13_village_b_clean_scrolls(zoom)
        def near(options,want,lo,hi,view):
            # 고른 장소의 이름표는 반드시 창 안에 들어오는 위치만 고른다.
            fits=[s for s in options if s<=lo and hi<=s+view]
            pool=fits or options
            return min(pool,key=lambda s:abs(s-want)) if pool else want
        box=r13_village_b_label_boxes(zoom).get(base)
        if box:
            want_x=near(xs,want_x,box[0],box[2],vw);want_y=near(ys,want_y,box[1],box[3],vh)
        # 2026-10-30 눈가림 플레이(4일 지도 솜이네 이름표가 안 보임): min(1,1.0) 은 정수 1 을 돌려주는데, 뷰포트의
        # xinitial/yinitial 은 정수를 「1픽셀」로 읽는다. 맨 아래·맨 오른쪽(솜이네·빨래터·큰 강)을 고르면 맨 위·맨 왼쪽이
        # 열렸다. 늘 소수(비율)로 돌려준다.
        return (float(max(0.0,min(1.0,(want_x*zoom)/max(1.0,1642*zoom-1136)))),
                float(max(0.0,min(1.0,(want_y*zoom)/max(1.0,958*zoom-506)))))

    # 2026-10-30 눈가림 플레이(4일 지도에 솜이네 이름표가 없음): 새 이야기의 별칭 장소(ms14_somi 등)는 기존 지도 점을
    # 그대로 쓰도록 등록했지만(R13_V111_MAP_ALIASES), 이 지도는 그림 장소 id 만 그려 별칭은 「다른 장소」 목록에만 있었다.
    # 같은 자리의 원래 장소가 목록에 없으면 별칭을 그 자리에 그린다. 둘 다 있으면 원래대로 원래 장소만 그린다.
    def r13_village_b_base(key):
        return globals().get("R13_V111_MAP_ALIASES",{}).get(key,key)
    def r13_village_b_drawn(key,rows):
        if key in R13_VILLAGE_B_PLACES:return True
        base=r13_village_b_base(key)
        if base==key or base not in R13_VILLAGE_B_PLACES:return False
        keys=[k for k,state in rows]
        if base in keys:return False
        # 같은 원래 장소를 가리키는 별칭이 여럿이면 목록에서 앞의 것 하나만 그린다.
        return next(k for k in keys if r13_village_b_base(k)==base)==key

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
            px=r13_type_pc("body")   # 2026-10-28 휴대폰도 PC 단계(예전 22/26). 휴대폰 열(28)이면 이름표가 잘린다
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
                    if r13_village_b_drawn(key,rows):
                        $ place=R13_VILLAGE_B_PLACES[r13_village_b_base(key)]
                        $ hx,hy,hw,hh=place["provisional_hit_rect"]
                        $ cx,cy=place["label_center"]
                        $ label=r13_map_label(key)
                        # 터치 화면에서는 이름표 칸(클릭 영역)을 1.3배로 유지한다. 글자 크기는 r13_village_b_label_px —
                        # 2026-10-27 소유자 「글씨가 너무 큼」으로 body→small, 휴대폰도 PC 값으로.
                        $ ls=1.3 if r13_touch_ui() else 1.0
                        $ lpx=r13_village_b_label_px()
                        $ lw=r13_village_b_label_width(label)
                        $ choose = [SetScreenVariable("selected",key),SetScreenVariable("map_notice",None)] if state!="locked" else SetScreenVariable("map_notice",r13_map_locked_notice(label))
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
                    if r13_village_b_drawn(key,rows):
                        $ place=R13_VILLAGE_B_PLACES[r13_village_b_base(key)]
                        $ cx,cy=place["label_center"]
                        $ lw=r13_village_b_label_width(r13_map_label(key),scaled=False)
                        use r13_map_status_badges(key,state,selected,(int((cx-lw/2)*zoom),int((cy-19)*zoom),int(lw*zoom),int(38*zoom)))
    add r13_asset("file:assets/map-village-b/notebook_frame_1280x720.png")
    # 수첩 상단의 좁은 봉제선 대신 지도 창 안에 제목 전용 64px 공간을 확보한다.
    add Solid("#f7e8cd") xpos 88 ypos 58 xysize (1136,64)
    add Solid("#b99a6b") xpos 100 ypos 120 xysize (1112,2)
    # 기존 수첩 에셋으로 가볍게 꾸미고, 제목과 현재 위치를 한 줄에 정렬한다.
    # 2026-10-27 소유자: 왼쪽 위에 빨강·청록 조각만 찍혀 보였다(테이프 장식). 장식은 조사 화면 이름표 한 곳만 쓰므로 뺀다.
    fixed:
        area (360,62,540,54)
        hbox:
            align (.5,.5) spacing 12
            add Transform(Crop((16,16,32,32),r13_asset_path("file:assets/ui-b-field/b_icon_acorn.png")),zoom=1.0) yalign .5
            text "다람탐정 · 마을 지도" font R13_UI_BOLD_FONT size (r13_type("subtitle") if R13_TYPE_V2 else 28) color (r13_type_color("ink") if R13_TYPE_V2 else "#493324") yalign .5
    use r13_map_close_x(close_action,ready,"r13_village_close_x")
    fixed:
        area (920,72,248,38)
        hbox:
            align (.5,.5) spacing 8
            add Transform(r13_asset_path("file:assets/map-status/current_location.png"),zoom=1.0/3) yalign .5
            text ("현재 · "+(r13_map_label(room13["location"]) if r13_map_discovered(room13["location"]) else "마을")) font R13_UI_BOLD_FONT size (r13_type("small") if R13_TYPE_V2 else 18) color (r13_type_color("muted") if R13_TYPE_V2 else "#765b3e") yalign .5 xmaximum 212
    $ extras=[(key,state) for key,state in rows if not r13_village_b_drawn(key,rows)]
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
        # 2026-10-29 눈가림 플레이: 잠긴 장소 안내에 「지금 생각: …」이 붙으면서 두 줄이 되어 44px 칸 밖으로 넘쳐 겹쳤다.
        # 아래끝(628, 하단 버튼 줄 위)은 그대로 두고 칸이 위로 자란다. 줄 사이를 두어 두 줄이 붙지 않게 한다.
        frame:
            xpos 330 xsize 620 ypos 628 yanchor 1.0 yminimum 44 padding (16,8)
            background Frame(r13_asset_path("file:assets/map-village-b/b_panel_small_trimmed.png"),12,10)
            text visible_notice font R13_UI_BOLD_FONT size (r13_type("body") if R13_TYPE_V2 else 19) color (r13_type_color("accent") if R13_TYPE_V2 else "#963b2f") xsize 588 text_align .5 xalign .5 yalign .5 line_spacing 4
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
                                action ([SetScreenVariable("selected",key),SetScreenVariable("map_notice",None),SetScreenVariable("extra_places",False)] if state!="locked" else SetScreenVariable("map_notice",r13_map_locked_notice(r13_map_label(key))))

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
    # 2026-10-27 소유자 "애매하게 뒷배경을 초과하면 안 돼": 오른쪽 아래 다람 스티커가 수첩 모서리 밖으로 걸쳐 있어 뺐다.


# 2026-10-28 소유자: 「지도의 X 표시가 삐져나왔으니 자연스럽게, 네모 아이콘을 빼도 되고」 → 시안 A(판 없이 X만).
# 판(62px)이 종이 오른쪽 끝(1224)을 넘어 1238 까지 나갔다. X 는 제목 띠(58~122) 오른쪽 안에 두고, 손가락이 닿는 칸은
# 넓게 잡되 종이 밖으로는 내지 않는다. 마을·여관·숲 지도가 같은 자리를 쓰므로 한 곳에서 그린다.
screen r13_map_close_x(close_action,ready,xid=None):
    textbutton "×":
        id xid
        area ((1140,58,84,64) if r13_touch_ui() else (1162,62,58,56)) padding (0,0) background None
        text_xalign .5 text_yalign .5
        text_font R13_UI_BOLD_FONT text_size r13_type("display") text_color r13_type_color("ink") text_hover_color r13_type_color("accent") text_align .5
        action close_action sensitive ready alt "닫기"
