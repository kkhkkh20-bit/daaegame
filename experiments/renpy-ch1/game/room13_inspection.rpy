# Optional, save-local usable-item puzzle. No forensic evidence, time, or
# relationship rewards: the family's travelling writing case moves with them.
init 66 python:
    R13_INSPECTION_ITEMS = {
        # Owner asked what these are for (0.18.5): each line names its use.
        # 0.18.20: what each tool is and does in general; no target, order or reward.
        "pencil": ("짧은 연필", "종이 위에 눕혀 문지르면 아래에 눌린 무늬가 옮겨진다."),
        "paper": ("얇은 종이", "얇아서 아래의 무늬가 비친다. 무늬 위에 깔고 문지를 수 있다."),
        "ruler": ("납작한 자", "끝이 얇고 단단하다. 좁은 틈이나 홈을 누를 수 있다."),
        "magnifier": ("접이식 돋보기", "책상 물건을 확대한다. 현장의 이불 바느질·수리점 도면도 조사 메뉴에서 살필 수 있다."),
    }
    # Coordinates are in the game's 1280x720 canvas, independent of source size.
    # Art-specific positions can be replaced by inspection-layout.json at build.
    R13_INSPECTION_LAYOUT = {
        "desk": {"file":"assets/room13-pixel-inspect-desk.webp", "targets":{
            "notebook":[100,125,210,155], "letters":[345,125,230,140],
            "cup":[1020,110,150,120], "candle":[690,105,110,150],
            "pencil":[570,345,180,75], "paper":[330,325,205,155],
            "ruler":[115,385,185,90], "drawer":[825,290,335,220]}},
        "drawer": {"file":"assets/room13-pixel-inspect-drawer.webp", "targets":{
            "tag":[340,145,235,145], "buttons":[145,360,130,110],
            "thread":[545,355,135,125], "eraser":[730,365,120,100],
            "divider":[910,140,75,365], "compartment":[985,165,180,325]}},
        "icons": {},
    }
    if renpy.loadable("room13-inspection-layout.json"):
        R13_INSPECTION_LAYOUT.update(json.load(renpy.file("room13-inspection-layout.json")))
    R13_INSPECTION_NAMES = dict(notebook="우리 수첩",letters="가져온 편지",cup="찻잔",candle="촛불",
        drawer="여행 필기함의 서랍",tag="눌린 운반표",buttons="여분 단추",thread="실패",eraser="지우개",
        divider="오른쪽 칸막이",compartment="작은 도구칸")
    R13_INSPECTION_NAMES.update({k:v[0] for k,v in R13_INSPECTION_ITEMS.items()})

    def r13_inspection_available():
        if not store.room13 or not r13_has("lodging"): return False
        displaced=r13_has("family_room_unusable") or store.room13.get("case_state")=="occurred"
        return store.room13.get("location")==("guestroom" if displaced else "room13")

    def r13_inspection_state():
        result=dict(version=1,inventory=[],taken=[],seen=[],paper_placed=False,rubbing=False,compartment_open=False,groove_held=False)
        if store.room13: result.update(winter_copy.deepcopy(store.room13.get("inspection_items",{})))
        return result

    def r13_inspection_has_items():
        return bool(r13_inspection_state()["inventory"])

    def r13_inspection_transition(state,view,target,selected=None):
        """Pure reducer: all durable writes return through r13_edit, supporting rollback."""
        s=winter_copy.deepcopy(state)
        # The groove stays pressed only until the next click (press, then push the panel).
        held=bool(s.get("groove_held"));s["groove_held"]=False
        out=dict(view=view,selected=selected,lens=None,message="")
        def say(message):
            out["message"]=message
            return s,out
        def take(key):
            if key in s["taken"]: return say("이미 챙긴 물건이다.")
            s["taken"].append(key)
            if key not in s["inventory"]: s["inventory"].append(key)
            out["selected"]=None
            if key=="magnifier":
                return say("아이템 획득: 접이식 돋보기. 책상 물건을 크게 보거나, 현장 조사 메뉴에서 쓸 수 있다.")
            if all(k in s["taken"] for k in ("pencil","paper","ruler")):
                return say("아이템 획득: %s. 세 도구를 모두 챙겼다."%R13_INSPECTION_ITEMS[key][0])
            return say("아이템 획득: %s. %s"%R13_INSPECTION_ITEMS[key])
        if view not in ("desk","drawer") or target not in R13_INSPECTION_LAYOUT[view]["targets"]:
            return say("손이 닿는 물건부터 살펴보자.")
        seen=view+":"+target
        if seen not in s["seen"]: s["seen"].append(seen)
        if selected and selected not in s["inventory"]:
            out["selected"]=None
            return say("그 물건은 지금 아이템에 없다.")
        if view=="drawer" and target=="compartment" and held and not s["compartment_open"]:
            s["compartment_open"]=True;out["selected"]=None
            return say("홈을 누른 채 판을 오른쪽으로 밀었다. 판이 옆으로 밀리며 도구칸이 열렸다. 안에 접이식 돋보기가 있다.")
        if selected=="magnifier":
            out["lens"]=(view,target)
            return say("돋보기를 가까이 댔다. 작은 무늬를 크게 살펴본다.")
        if selected:
            if view=="drawer" and target=="tag" and selected=="paper":
                if s["paper_placed"]: return say("종이는 이미 운반표 위에 놓여 있다.")
                s["inventory"].remove("paper");s["paper_placed"]=True;out["selected"]=None
                return say("얇은 종이를 운반표 위에 펼쳤다. 눌린 무늬를 옮겨 낼 도구가 필요하다.")
            if view=="drawer" and target=="tag" and selected=="pencil":
                if not s["paper_placed"]: return say("운반표에 바로 칠하면 글씨를 덮어 버린다. 얇은 종이를 먼저 대자.")
                if s["rubbing"]: return say("탁본은 이미 완성됐다.")
                s["rubbing"]=True;out["selected"]=None
                return say("연필을 눕혀 문질렀다. 칸막이 아래쪽 홈을 누른 채 오른쪽으로 미는 그림이 나타났다.")
            # 0.18.20: opening depends on the motion, not on having made the rubbing.
            # Press the bottom groove with the ruler, then push the panel to the right.
            if view=="drawer" and target=="divider" and selected=="ruler":
                if s["compartment_open"]: return say("이미 열려 있다.")
                s["groove_held"]=True
                return say("자 끝으로 아래쪽 홈을 눌렀다. 안쪽에서 걸림쇠가 조금 내려갔다.")
            if view=="drawer" and target=="compartment" and selected=="ruler" and not held:
                if s["compartment_open"]: return say("이미 열려 있다.")
                return say("판 틈에 자를 넣어 봤다. 판은 걸린 채 움직이지 않는다.")
            return say("여기에는 이 도구를 쓸 일이 없겠다. 물건은 그대로 두었다.")
        if view=="desk" and target in ("pencil","paper","ruler"): return take(target)
        if view=="desk" and target=="drawer":
            out["view"]="drawer"
            return say("우리 여행 필기함의 서랍을 열었다. 안쪽에는 문구와 바느질 도구가 나뉘어 있다.")
        if view=="desk" and target=="notebook":
            return say("직접 본 것과 전해 들은 말을 나누어 적어 둔 우리 수첩이다.")
        if view=="drawer" and target=="compartment":
            if s["compartment_open"]: return take("magnifier")
            return say("오른쪽 작은 도구칸이 닫혀 있다. 손잡이 대신 아래쪽에 얕은 홈이 있다.")
        if view=="drawer" and target=="tag":
            if s["rubbing"]: return say("탁본에 나타난 그림: 아래쪽 홈을 누르고, 누른 채 오른쪽으로 민다.")
            if s["paper_placed"]: return say("운반표 위에 얇은 종이가 놓여 있다.")
            return say("색이 지워진 낡은 운반표다. 손끝에 얕게 눌린 무늬가 걸린다.")
        texts={
            "letters":"집에서 챙겨 온, 아내 이름으로 온 편지다. 방에 온 뒤 새로 도착한 편지는 없다.",
            "cup":"물을 마신 자국이 남았다. 종이에 쏟지 않도록 손잡이를 돌려 두었다.",
            "candle":"필기할 때 쓰는 촛불이다. 종이와는 거리를 두자.",
            "buttons":"우리 외투에 달 여분 단추다. 서로 크기가 조금씩 다르다.",
            "thread":"여행 전에 챙긴 실과 바늘이다. 다른 방에서 발견한 바느질 흔적과는 별개다.",
            "eraser":"오래 써서 한쪽 모서리가 둥글어진 지우개다.",
            "divider":"칸막이 아래쪽에 작은 누름 홈이 있다. 세게 잡아당기는 구조는 아닌 듯하다.",
        }
        return say(texts.get(target,"물건이 놓였던 자리를 다시 확인했다."))

    def r13_inspection_click(view,target,selected):
        state,result=r13_inspection_transition(r13_inspection_state(),view,target,selected)
        r13_edit(inspection_items=state)
        for name in ("view","selected","lens","message"):
            renpy.set_screen_variable(name,result[name],screen="r13_desk_inspection")
        renpy.restart_interaction()

    def r13_inspection_icon(key,width=96,height=76):
        art=r13_material_art("tool:"+key)
        if art is not None:return Transform(art,xysize=(width,height),fit="contain",nearest=True)
        spec=R13_INSPECTION_LAYOUT.get("icons",{}).get(key)
        if spec and renpy.loadable(spec["file"]):
            return Transform(Transform(spec["file"],crop=tuple(spec["crop"])),xysize=(width,height),fit="contain",nearest=True)
        # Development fallback only; asset contract and release tests require icons.
        return Text(R13_INSPECTION_ITEMS[key][0],size=20,color="#fff2cf",text_align=.5)

    def r13_memo_taken():
        """13호 desk after Mom's memo is picked up (0.18.48): the envelope is gone from the desk."""
        s=store.room13 or {}
        return bool(s.get("life_poc")) and s.get("location")=="room13" and r13_has("M01")

    def r13_inspection_art(view):
        spec=R13_INSPECTION_LAYOUT[view]
        art=spec["file"]
        if view=="desk" and r13_memo_taken() and renpy.loadable("assets/room13-pixel-inspect-desk-nomemo.webp"):
            art="assets/room13-pixel-inspect-desk-nomemo.webp"  # dev/make_desk_without_memo.py
        layers=[(0,0),Transform(art,xysize=(1280,720),nearest=True) if renpy.loadable(art) else Solid("#59402b",xsize=1280,ysize=720)]
        state=r13_inspection_state()
        if view=="desk":
            for key in ("pencil","paper","ruler"):
                if key not in state["taken"]:
                    x,y,w,h=spec["targets"][key]
                    layers.extend([(x,y),r13_inspection_icon(key,w,h)])
        else:
            bg=layers[1]
            # 0.18.63: drawn state art (ART_REQUEST_01822 section 1, dev/import_drawer_puzzle.py).
            # The code-drawn layers below stay only as a fallback when a file is missing.
            if state["compartment_open"]:
                x,y,w,h=spec["targets"]["compartment"]
                strip=int(w*.22)
                opened=r13_drawer_state_art("open")
                if opened:
                    # Panel pushed into the right wall: the open-drawer picture replaces the closed one.
                    layers[1]=opened[1]
                else:
                    layers.extend([(x,y),R13DrawerCavity(w-strip,h),
                        (x+w-strip,y),Transform(bg,crop=(x,y,strip,h))])
                if "magnifier" not in state["taken"]:
                    # The existing magnifier icon, a separate layer over the empty compartment.
                    layers.extend([(x+18,y+int(h*.28)),r13_inspection_icon("magnifier",w-strip-36,int(h*.42))])
            elif state.get("groove_held"):
                # The ruler's tip sits in the notch; the panel edge glows where it should be pushed.
                x,y,w,h=spec["targets"]["compartment"]
                gx,gy,gw,gh=spec["targets"]["divider"]
                layers.extend([(x,y),R13HoverCorners(w,h,"#ffe08acc",6)])
                held=r13_drawer_state_art("held")
                layers.extend(list(held) if held else [(gx+gw//2-40,gy-58),r13_inspection_icon("ruler",80,80)])
            if state["paper_placed"]:
                # Blank and rubbed paper share one canvas and one rect: the paper never jumps.
                sheet=r13_drawer_state_art("rubbing" if state["rubbing"] else "paper")
                if sheet:
                    layers.extend(list(sheet))
                else:
                    x,y,w,h=spec["targets"]["tag"]
                    layers.extend([(x+10,y+8),R13RubbingSheet(w-20,h-16,state["rubbing"])])
        return Composite((1280,720),*layers)

    def r13_drawer_state_art(key):
        """((x,y), displayable) for a drawn drawer state, or None when the file is missing.
        Rects are in the 1280x720 canvas; the ruler's fractional top-left rounds to a pixel."""
        spec=R13_INSPECTION_LAYOUT.get("drawer_states",{}).get(key)
        if not spec or not renpy.loadable(spec["file"]):return None
        x,y,w,h=spec["rect"]
        # Overlays are stored at 2x display size: smooth 2:1 reduction (nearest would drop pixels).
        art=Transform(spec["file"],xysize=(int(w),int(h)),nearest=(key=="open"))
        return (int(round(x)),int(round(y))),art

    def r13_drawer_layers(state=None):
        """QA: which drawn drawer states the drawer view uses for a puzzle state."""
        state=state or r13_inspection_state()
        out=[]
        if state["compartment_open"] and r13_drawer_state_art("open"):out.append("open")
        elif state.get("groove_held") and r13_drawer_state_art("held"):out.append("held")
        if state["paper_placed"]:
            key="rubbing" if state["rubbing"] else "paper"
            if r13_drawer_state_art(key):out.append(key)
        return out

    class R13RubbingSheet(renpy.Displayable):
        """Thin paper over the tag. Rubbed: graphite hatch with the pressed picture left pale —
        the right panel with its bottom notch, ① press down at the notch, ② push right."""
        def __init__(self,width,height,rubbed=False,**kwargs):
            super(R13RubbingSheet,self).__init__(**kwargs)
            self.w=int(width);self.h=int(height);self.rubbed=rubbed
        def render(self,width,height,st,at):
            w,h=self.w,self.h;r=renpy.Render(w,h);c=r.canvas()
            c.rect("#00000040",(6,6,w-6,h-6))
            c.rect("#f3ead2dd",(0,0,w-6,h-6))
            c.rect("#cbbd9a",(0,0,w-6,h-6),2)
            if not self.rubbed:return r
            pw,ph=w-6,h-6
            # Graphite: dense diagonal strokes on the paper only.
            # Graphite strokes: short uneven bands, like a pencil laid flat.
            c.rect("#8a857a",(0,0,pw,ph))
            for row,y in enumerate(range(0,ph,3)):
                off=(row*37)%23
                for x in range(-off,pw,46):
                    c.rect("#5d5951",(max(0,x),y,min(pw,x+34)-max(0,x),2))
            c.rect("#cbbd9a",(0,0,pw,ph),2)
            # Pale (unrubbed) lines: what was pressed into the tag.
            pale="#f3ead2"
            bx,by,bw,bh=int(pw*.56),int(ph*.12),int(pw*.26),int(ph*.76)
            c.rect("#4a4640",(bx-3,by-3,bw+6,bh+6))
            c.rect(pale,(bx,by,bw,bh),3)
            nx=bx+bw//2;ny=by+bh
            c.circle(pale,(nx,ny),9,3)
            # ① down arrow onto the notch
            ax=bx-int(pw*.16)
            c.line(pale,(ax,by+10),(ax,ny-6),4)
            c.polygon(pale,[(ax-9,ny-14),(ax+9,ny-14),(ax,ny-2)])
            c.line(pale,(ax,ny-4),(nx-12,ny-4),3)
            # ② right arrow beside the panel
            ry=by+bh//2;rx=bx+bw+8
            c.line(pale,(rx,ry),(min(pw-14,rx+int(pw*.12)),ry),4)
            tip=min(pw-4,rx+int(pw*.12)+10)
            c.polygon(pale,[(tip-12,ry-9),(tip-12,ry+9),(tip,ry)])
            for text,(tx,ty) in (("1",(ax-28,by+4)),("2",(rx+4,ry-34))):
                t=renpy.render(Text(text,size=22,color=pale,outlines=[(2,"#4a4640",0,0)]),w,h,st,at)
                r.blit(t,(tx,ty))
            return r

    class R13DrawerCavity(renpy.Displayable):
        def __init__(self,width,height,**kwargs):
            super(R13DrawerCavity,self).__init__(**kwargs)
            self.w=int(width);self.h=int(height)
        def render(self,width,height,st,at):
            w,h=self.w,self.h;r=renpy.Render(w,h);c=r.canvas()
            c.rect("#2a1d14",(0,0,w,h))
            c.rect("#1a120c",(0,0,w,14));c.rect("#1a120c",(0,0,12,h))
            c.rect("#6b4a30",(0,0,w,h),3)
            return r

    class R13HoverCorners(renpy.Displayable):
        """Pixel corner brackets: marks what can be touched without boxing the art."""
        def __init__(self,width=None,height=None,color="#f6d18acc",thick=4,**kwargs):
            super(R13HoverCorners,self).__init__(**kwargs)
            self.fw=width;self.fh=height;self.color=color;self.t=thick
        def render(self,width,height,st,at):
            w=int(self.fw or width);h=int(self.fh or height);t=self.t;L=max(12,min(w,h)//5)
            r=renpy.Render(w,h);c=r.canvas()
            for x,y,dx,dy in ((0,0,1,1),(w,0,-1,1),(0,h,1,-1),(w,h,-1,-1)):
                c.rect(self.color,(min(x,x+dx*L),min(y,y+dy*t),L,t))
                c.rect(self.color,(min(x,x+dx*t),min(y,y+dy*L),t,L))
            return r

    def r13_inspection_lens(view,target):
        x,y,w,h=R13_INSPECTION_LAYOUT[view]["targets"][target]
        return Transform(Transform(r13_inspection_art(view),crop=(x,y,w,h)),xysize=(640,400),fit="contain",nearest=True)

    # Register a broad desk behind existing small targets. Specific targets
    # retain later draw order, and the portable kit is never placed at a crime scene.
    for _r13_desk_place in ("room13","guestroom"):
        _r13_existing=ROOM13["objects"].get(_r13_desk_place,{})
        # 0.18.56 (owner): the desk target is its front edge, below the cup, bread, notebook and papers.
        _r13_desk_spec=dict(rect=[0,448,430,72],text="우리 여행 필기함을 펼칠 책상이다.",
            need=["lodging"],give=[],flags=[],live_family_desk=True)
        ROOM13["objects"][_r13_desk_place]=dict([("desk",_r13_desk_spec)]+[(k,v) for k,v in _r13_existing.items() if k!="desk"])
    _r13_before_inspection_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec.get("live_family_desk") and not r13_inspection_available():return False
        return _r13_before_inspection_visible(spec)
    _r13_before_inspection_name=r13_object_name
    def r13_object_name(key):
        if key=="desk" and store.room13 and store.room13["location"] in ("room13","guestroom"):
            return "책상 · 여행 필기함"
        return _r13_before_inspection_name(key)

screen r13_desk_inspection():
    modal True
    zorder 90
    default view="desk"
    default selected=None
    default lens=None
    default message=("우리 여행 필기함이다. 서랍 속 작은 도구칸이 잠겨 있다." if not r13_inspection_state()["compartment_open"] else "우리 여행 필기함이다. 돋보기를 고르고 물건을 누르면 크게 볼 수 있다.")
    add r13_inspection_art(view)
    for target,rect in R13_INSPECTION_LAYOUT[view]["targets"].items():
        if not (view=="desk" and target in ("pencil","paper","ruler") and target in r13_inspection_state()["taken"]) and not (view=="desk" and target=="letters" and r13_memo_taken()):
            button:
                area tuple(rect) padding (0,0) background None hover_background R13HoverCorners()
                action (Return("mother_note") if view=="desk" and target=="letters" and room13.get("life_poc") and room13["location"]=="room13" else Function(r13_inspection_click,view,target,selected))
                sensitive (lens is None)
                tooltip ("접힌 메모와 편지" if target=="letters" and room13.get("life_poc") and room13["location"]=="room13" else R13_INSPECTION_NAMES[target])
                alt ("접힌 메모와 편지" if target=="letters" and room13.get("life_poc") and room13["location"]=="room13" else R13_INSPECTION_NAMES[target])
    frame:
        area (16,14,1248,68) padding (18,10) background R13ActionPanel()
        hbox:
            spacing 20
            text ("책상 · 여행 필기함" if view=="desk" else "열린 서랍") size 27 color "#fff2cf" yalign .5 xsize 330
            text ("사용 중: "+R13_INSPECTION_ITEMS[selected][0] if selected else "물건을 눌러 살펴보기") size 21 color "#d9bc80" yalign .5 xsize 400
            if selected:
                textbutton "선택 해제" style "r13_action_button" text_size 19 xsize 155 ysize 46 action SetScreenVariable("selected",None) sensitive (lens is None)
            textbutton ("책상으로" if view=="drawer" else "방으로"):
                style "r13_action_button" text_size 20 xsize 160 ysize 46
                action ([SetScreenVariable("view","desk"),SetScreenVariable("selected",None),SetScreenVariable("message","필기함에서 손을 떼고 책상을 다시 보았다.")] if view=="drawer" else Return("exit"))
                sensitive (lens is None)
    $ hint=GetTooltip()
    if hint and not lens:
        frame:
            xpos 24 ypos 518 padding (12,7) background R13ActionPanel()
            text hint size 20 color "#fff2cf"
    frame:
        area (16,564,1248,80) padding (18,12) background R13ActionPanel()
        text message size 22 color "#fff2cf" xsize 1200
    frame:
        area (16,652,1248,60) padding (14,4) background R13ActionPanel()
        hbox:
            spacing 12
            text "아이템" size 21 color "#d9bc80" yalign .5 xsize 100
            for key in r13_inspection_state()["inventory"]:
                button:
                    style "r13_action_button" xsize 222 ysize 52 padding (8,2)
                    background (Solid("#675635") if selected==key else R13ActionPanel())
                    action [SetScreenVariable("selected",None if selected==key else key),SetScreenVariable("message",("선택을 해제했다." if selected==key else R13_INSPECTION_ITEMS[key][1]+" 사용할 대상을 누르자."))]
                    sensitive (lens is None)
                    hbox:
                        spacing 8 yalign .5
                        add r13_inspection_icon(key,44,44) yalign .5
                        text R13_INSPECTION_ITEMS[key][0] size 21 color "#fff2cf" yalign .5
            if not r13_inspection_state()["inventory"]:
                text "챙긴 물건이 여기에 놓입니다." size 21 color "#c1c9c2" yalign .5
    if lens:
        button:
            area (0,0,1280,720) padding (0,0) background Solid("#081820e8")
            action NullAction()
        frame:
            area (270,90,740,550) padding (20,16) background R13ActionPanel()
            vbox:
                spacing 12
                text ("돋보기 · "+R13_INSPECTION_NAMES[lens[1]]) size 25 color "#f6d18a"
                add r13_inspection_lens(lens[0],lens[1]) xalign .5
                textbutton "돋보기 내려놓기" style "r13_action_button" text_size 22 xsize 690 ysize 54 action SetScreenVariable("lens",None)
        key "game_menu" action SetScreenVariable("lens",None)
    elif selected:
        key "game_menu" action SetScreenVariable("selected",None)
    elif view=="drawer":
        key "game_menu" action [SetScreenVariable("view","desk"),SetScreenVariable("message","책상으로 돌아왔다.")]
    else:
        key "game_menu" action Return("exit")

screen r13_item_bag():
    modal True
    zorder 95
    use r13_records(initial_tab="all",close_action=Hide("r13_item_bag"))

screen r13_item_bag_content():
    # 2026-10-27 수첩 공통 틀 좌표. (r13_item_bag 은 initial_tab="all" 로 열어 실제로는 자료 탭이 보인다.)
    text "아이템" xpos (R13_NB_LEFT+4) ypos R13_NB_TOP size (r13_type("subtitle") if R13_TYPE_V2 else 26) color (r13_type_color("ink") if R13_TYPE_V2 else "#765426") font R13_UI_BOLD_FONT
    viewport:
        area (R13_NB_LEFT,R13_NB_TOP+48,R13_NB_WIDTH,r13_nb_body_bottom()-(R13_NB_TOP+48)) mousewheel True draggable True scrollbars "vertical"
        vbox:
            spacing 16
            for key in r13_inspection_state()["inventory"]:
                frame:
                    xsize (R13_NB_WIDTH-34) padding (18,16) background R13PaperPanel()
                    hbox:
                        spacing 18
                        add r13_inspection_icon(key,62,56)
                        vbox:
                            spacing 8
                            text R13_INSPECTION_ITEMS[key][0] size (r13_type("emphasis") if R13_TYPE_V2 else r13_read_size(23,27)) color (r13_type_color("accent") if R13_TYPE_V2 else "#765426") xsize (R13_NB_WIDTH-150)
                            text R13_INSPECTION_ITEMS[key][1] size (r13_type("body") if R13_TYPE_V2 else r13_read_size(20,24)) color (r13_type_color("ink") if R13_TYPE_V2 else "#493b30") xsize (R13_NB_WIDTH-150)
            if not r13_inspection_state()["inventory"]:
                text "아직 챙긴 도구가 없다." size (r13_type("body") if R13_TYPE_V2 else 22) color (r13_type_color("muted") if R13_TYPE_V2 else "#796044")
    if r13_tool_notes():
        use r13_nb_footer_button(1,"돋보기 관찰 메모",Show("r13_tool_notebook"),width=R13_CONTROL["width"],control_id="r13_nb_tool_notes")

label r13_inspect_desk:
    if not r13_inspection_available():
        return
    window hide
    hide r13_visitor
    while True:
        call screen r13_desk_inspection
        if _return!="mother_note":
            return
        # 0.18.50 (owner): read the memo over the desk close-up, not back in the room.
        $ renpy.show("r13_desk_bg",what=r13_inspection_art("desk"))
        call r13_mother_note
        $ renpy.hide("r13_desk_bg")
