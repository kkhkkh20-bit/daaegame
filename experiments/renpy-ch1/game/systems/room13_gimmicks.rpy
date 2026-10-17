# Checking with the hands (owner's visual-gimmicks package, 0.18.22).
#   The three existing item activities keep their place, item, day, cost and reward. What changes:
#   the reveal happens in a close-up, one step at a time, and the activity only finishes (time,
#   flags, evidence) at the step where Dad reads what he found. Leaving early costs nothing; the
#   close-up state stays for this run (room13["gimmicks"]).
#   package  use_knife_burlap: feel the hard bottom → knife on the seam → lift the board → read.
#   lamp     use_lantern_rear: dark until the lamp is raised; light follows the pointer.
#   scale    use_weight_scale: the standard weight on the empty pan, then the pivot screw.
#            The tilt alone proves nothing (the shop weight's mass is unverified); the activity
#            finishes only after both the tilt and the scratched screw were looked at.
# Assets: assets/r13-gimmick-*.webp (1672x941 lossless). Regions are the package's normalized ones.
init 127 python:
    def _r13_gm_scene(title,image,regions):
        return dict(title=title,before=image,after=image,targets=regions)
    R13_LIFE_SCENES.update({
        "package_closed":_r13_gm_scene("잡화점 · 포장천 자루","assets/r13-gimmick-package-closed.webp",dict(
            mouth=([0.37,0.1,0.29,0.25],"자루 입구"),seam=([0.32,0.65,0.43,0.2],"자루 아래쪽 실밥"))),
        "package_seam":_r13_gm_scene("잡화점 · 포장천 자루","assets/r13-gimmick-package-seam.webp",dict(
            mouth=([0.37,0.1,0.29,0.25],"자루 입구"),insert=([0.36,0.64,0.37,0.13],"천 아래 나무 덮개"))),
        "package_revealed":_r13_gm_scene("잡화점 · 포장천 자루","assets/r13-gimmick-package-revealed.webp",dict(
            food=([0.34,0.58,0.38,0.22],"덮개 아래 물건"))),
        "lamp_floor":_r13_gm_scene("주방 · 뒷문 아래","assets/r13-gimmick-lamp-floor.webp",dict(
            threshold=([0.27,0.6,0.14,0.11],"문턱"),wall=([0.45,0.55,0.28,0.1],"벽 밑"),step=([0.75,0.39,0.1,0.17],"계단 밑"))),
        "scale_base":_r13_gm_scene("잡화점 · 양팔저울","assets/r13-gimmick-scale-base.webp",dict(
            test=([0.105,0.68,0.1,0.2],"탁자 위 표준 추"),pan=([0.22,0.49,0.2,0.22],"왼쪽 접시"),
            reference=([0.625,0.55,0.2,0.2],"가게 추"),pivot=([0.43,0.17,0.14,0.24],"가운데 조정부"))),
        "scale_loaded":_r13_gm_scene("잡화점 · 양팔저울","assets/r13-gimmick-scale-loaded.webp",dict(
            pan=([0.22,0.49,0.2,0.22],"표준 추를 올린 접시"),reference=([0.625,0.55,0.2,0.2],"가게 추"),
            pivot=([0.43,0.17,0.14,0.24],"가운데 조정부"))),
        "scale_pivot":_r13_gm_scene("잡화점 · 저울 조정부","assets/r13-gimmick-scale-pivot.webp",dict(
            screw=([0.43,0.37,0.16,0.24],"조정 나사"))),
    })
    for _k in ("use_knife_burlap","use_lantern_rear","use_weight_scale"):
        ROOM13["activities"][_k]["special"]=True
    R13_GIMMICK_LABELS={"use_knife_burlap":"r13_gm_package","use_lantern_rear":"r13_gm_lamp","use_weight_scale":"r13_gm_scale"}

    def r13_gm_state(key):
        return dict((store.room13 or {}).get("gimmicks",{}).get(key,{}))

    def r13_gm_save(key,**values):
        g=dict(store.room13.get("gimmicks",{}));st=dict(g.get(key,{}));st.update(values);g[key]=st
        r13_edit(gimmicks=g)

    _r13_gm_tool_name=r13_life_tool_name
    def r13_life_tool_name(key):
        if key in globals().get("R13_BORROW",{}):return R13_BORROW[key]["title"]
        return _r13_gm_tool_name(key)

    class R13LampDark(renpy.Displayable):
        """Darkness over the close-up. Raised: a stepped round pool of light follows the pointer."""
        def __init__(self,lit=False,radius=150,**kwargs):
            super(R13LampDark,self).__init__(**kwargs)
            self.lit=lit;self.radius=radius;self.mx=640;self.my=380
        def event(self,ev,x,y,st):
            if self.lit and (x,y)!=(self.mx,self.my):
                self.mx,self.my=x,y;renpy.redraw(self,0)
        def render(self,width,height,st,at):
            r=renpy.Render(1280,720);c=r.canvas()
            dark="#05080cf2" if not self.lit else "#05080ce0"
            if not self.lit:
                c.rect(dark,(0,0,1280,720));return r
            R=self.radius;step=8
            for y in range(0,720,step):
                dy=abs(y+step//2-self.my)
                if dy>=R:
                    c.rect(dark,(0,y,1280,step));continue
                half=int((R*R-dy*dy)**.5)
                left=max(0,int(self.mx)-half);right=min(1280,int(self.mx)+half)
                if left>0:c.rect(dark,(0,y,left,step))
                if right<1280:c.rect(dark,(right,y,1280-right,step))
                # A soft rim: one dimmer band just inside the edge.
                rim=max(0,half-18)
                c.rect("#05080c70",(left,y,max(0,half-rim),step));c.rect("#05080c70",(int(self.mx)+rim,y,max(0,half-rim),step))
            return r

# ---- package ----
label r13_gm_package:
    $ _st=r13_gm_state("package")
    $ _msg="잡화점 구석의 포장천 자루다. 장부에는 ‘바닥남’이라고 적힌 물건들이 이 근처에 쌓여 있었다."
    while True:
        $ _stage=_st.get("stage","closed")
        call screen r13_life_closeup("package_"+_stage,tools=(("knife",) if _stage=="closed" and r13_has("own:knife") else ()),actions=[("back","돌아간다")],message=_msg)
        if _return[0]=="action":
            return False
        $ _t=_return[-1];_tool=_return[1] if _return[0]=="use" else None
        if _stage=="closed":
            if _t=="mouth":
                $ _msg="입구 쪽은 헐렁하다. 손을 넣어 보니 겉겨 섞인 곡식이 조금 들어 있다."
            elif _tool=="knife":
                $ r13_gm_save("package",stage="seam");_st=r13_gm_state("package")
                $ _msg="칼끝으로 아래쪽 실밥만 끊었다. 천 아래에 나무 덮개가 보인다. 칼은 그대로다."
            else:
                $ r13_gm_save("package",felt=True);_st=r13_gm_state("package")
                $ _msg="아래쪽을 눌러 보았다. 곡식이 아니라 단단한 판에 손이 닿는다. 겉천 실밥은 다른 곳보다 새것이다."
        elif _stage=="seam":
            if _t=="insert":
                $ r13_gm_save("package",stage="revealed");_st=r13_gm_state("package")
                $ _msg="나무 덮개를 손으로 들어 올렸다. 아래에 무언가가 차곡차곡 들어 있다."
            else:
                $ _msg="입구 쪽은 헐렁하다. 위에서 보면 평범한 곡식 자루다."
        else:
            # Reading what is inside is the step that finishes the activity (existing lines, flag).
            call r13_lines(ROOM13["activities"]["use_knife_burlap"]["lines"][1:],"activity:use_knife_burlap:read", binding_route="dynamic:575")
            return True
    return False

# ---- lamp ----
label r13_gm_lamp:
    $ _st=r13_gm_state("lamp")
    $ _msg="뒷문 아래는 어둡다. 손등불을 고르면 빛을 비출 수 있다."
    $ _lit=False
    $ _lp_loop=True
    while _lp_loop:
        $ _seen=set(_st.get("seen",[]))
        call screen r13_life_closeup("lamp_floor",tools=(() if _lit else ("lantern",)),actions=([("lower","등불을 내린다")] if _lit else [])+([("note","본 것을 적는다")] if "threshold" in _seen else [])+[("back","돌아간다")],message=_msg,overlay=R13LampDark(_lit))
        if _return[0]=="action":
            if _return[1]=="lower":
                $ _lit=False;_msg="등불을 내렸다. 다시 어두워졌다."
            elif _return[1]=="note":
                call r13_lines(ROOM13["activities"]["use_lantern_rear"]["lines"],"activity:use_lantern_rear", binding_route="dynamic:576")
                return True
            else:
                return False
        elif not _lit and not (_return[0]=="use" and _return[1]=="lantern"):
            $ _msg="너무 어두워 잘 보이지 않는다. 아래쪽에서 손등불을 고르자."
        else:
            # Raising the lamp on a spot lights it and reads it in the same click.
            $ _lit=True
            $ _t=_return[-1]
            if _t=="threshold":
                $ _msg="문턱 아래 바닥에 검은 줄이 있다. 그을음이다. 같은 자리를 여러 번 오간 것처럼 겹쳐 있다."
            elif _t=="wall":
                $ _msg="그을음은 뒷문 밖으로 나가지 않는다. 벽 밑을 따라 안쪽으로 이어진다."
            else:
                $ _msg="계단 밑 벽에서 그을음이 끊긴다. 벽 너머 위층은 13호실 쪽이다."
            $ r13_gm_save("lamp",seen=sorted(_seen|{_t}));_st=r13_gm_state("lamp")
    return False

# ---- scale ----
label r13_gm_scale:
    $ _st=r13_gm_state("scale")
    $ _msg="가게의 양팔저울이다. 오른쪽 접시에 가게 추가 올라가 있고, 왼쪽 접시는 비어 있다."
    while True:
        $ _view=_st.get("view","base")
        $ _loaded=_st.get("loaded",False)
        $ _scene="scale_pivot" if _view=="pivot" else ("scale_loaded" if _loaded else "scale_base")
        $ _ready=_st.get("tilt_seen") and _st.get("screw_seen")
        call screen r13_life_closeup(_scene,tools=(("weight",) if not _loaded and _view!="pivot" else ()),
            actions=([("up","저울 전체로 돌아간다")] if _view=="pivot" else [])+([("note","본 것을 적는다")] if _ready else [])+[("back","돌아간다")],message=_msg)
        if _return[0]=="action":
            if _return[1]=="up":
                $ r13_gm_save("scale",view="base");_st=r13_gm_state("scale")
                $ _msg="조정부에서 눈을 떼었다. 접시는 아까 그대로다."
            elif _return[1]=="note":
                call r13_lines([(None,"같은 모양의 표준 추를 왼쪽 접시에 올렸다. 저울은 가게 추 쪽으로 기울었다. 가운데 조정 나사 둘레에는 새로 긁힌 자국이 있었다."),
                    ("dad","(가게 추가 정말 무거운지, 누가 나사를 돌렸는지는 아직 모른다. 다만 이 저울로 잰 무게는 그대로 믿기 어렵다.)",{"thought":True})],"activity:use_weight_scale:v2")
                return True
            else:
                return False
        else:
            $ _t=_return[-1];_tool=_return[1] if _return[0]=="use" else None
        if _return[0]=="action":
            pass
        elif _view=="pivot":
            $ r13_gm_save("scale",screw_seen=True);_st=r13_gm_state("scale")
            $ _msg="나사 머리 둘레가 반짝이게 긁혀 있다. 오래된 때 위에 난 자국이다. 누가 언제 돌렸는지는 여기 적혀 있지 않다."
        elif _t=="pivot":
            $ r13_gm_save("scale",view="pivot");_st=r13_gm_state("scale")
            $ _msg="가운데 조정부를 가까이 보았다."
        elif _tool=="weight" and _t=="pan":
            $ r13_gm_save("scale",loaded=True,tilt_seen=True);_st=r13_gm_state("scale")
            $ _msg="표준 추를 왼쪽 접시에 올렸다. 같은 모양의 추인데 두 접시 높이가 맞지 않는다."
        elif _t=="pan" and _loaded:
            $ r13_gm_save("scale",loaded=False);_st=r13_gm_state("scale")
            $ _msg="표준 추를 다시 내려 탁자에 두었다."
        elif _t=="test":
            $ _msg="가져온 표준 추다. 아래쪽 쓸 물건에서 골라 접시에 올릴 수 있다." if r13_has("own:weight") else "표준 추가 없다."
        elif _t=="reference":
            $ _msg="가게 추다. 겉모양은 표준 추와 같다. 실제 무게가 같은지는 이것만 봐서는 모른다."
        else:
            $ _msg="빈 접시다."
    return False

# ---- package 02 (0.18.22): under the bed (use_knife_under) and the square stone (use_rubbing_stone) ----
#   floor: hand on the board shows the loose end → knife lifts it (no evidence) → unfolding the
#          note is the step that reads M02. The knife is not used up.
#   stone: the rubbing paper goes on the scraped face → rub by dragging (or one row per button)
#          → once marks span three rows, Dad can read them (R01). The paper is used up only then,
#          by the existing activity rule. The pale marks are abstract, not a script to decipher.
init 128 python:
    R13_LIFE_SCENES.update({
        "floor_closed":_r13_gm_scene("13호 · 침대 밑","assets/r13-gimmick-floor-closed.webp",dict(board=([0.29,0.45,0.43,0.29],"들뜬 판자"))),
        "floor_open":_r13_gm_scene("13호 · 침대 밑","assets/r13-gimmick-floor-open.webp",dict(note=([0.44,0.53,0.13,0.14],"접힌 종이"),board=([0.29,0.45,0.15,0.29],"들어 올린 판자"))),
        "floor_note":_r13_gm_scene("13호 · 접힌 종이","assets/r13-gimmick-note-open.webp",{}),
        "stone_base":_r13_gm_scene("광장 · 돌 표면","assets/r13-gimmick-stone-base.webp",dict(face=([0.3,0.18,0.4,0.56],"긁힌 돌 표면"))),
        "stone_paper":_r13_gm_scene("광장 · 돌 표면","assets/r13-gimmick-stone-paper.webp",{}),
    })
    for _k in ("use_knife_under","use_rubbing_stone"):
        ROOM13["activities"][_k]["special"]=True
    R13_GIMMICK_LABELS.update({"use_knife_under":"r13_gm_floor","use_rubbing_stone":"r13_gm_stone"})
    R13_RUB_AREA=r13_life_rect([0.3,0.18,0.4,0.56]);R13_RUB_COLS=6;R13_RUB_ROWS=4

    def r13_rub_cell_rect(cell):
        x,y,w,h=R13_RUB_AREA;c,r=cell;cw=w//R13_RUB_COLS;rh=h//R13_RUB_ROWS
        return (x+c*cw,y+r*rh,cw if c<R13_RUB_COLS-1 else w-c*cw,rh if r<R13_RUB_ROWS-1 else h-r*rh)

    def r13_rub_cells():
        return [tuple(c) for c in r13_gm_state("stone").get("cells",[])]

    def r13_rub_add(cells):
        known=r13_rub_cells();new=[c for c in cells if c not in known]
        if new:r13_gm_save("stone",cells=[list(c) for c in known+new])
        return bool(new)

    def r13_rub_enough():
        cells=r13_rub_cells()
        return len(cells)>=10 and len({r for c,r in cells})>=3

    def r13_rub_layer():
        full=Transform("assets/r13-gimmick-stone-rubbed.webp",xysize=(1280,720),nearest=True)
        layers=[]
        for cell in r13_rub_cells():
            x,y,w,h=r13_rub_cell_rect(cell)
            layers+=[(x,y),Transform(full,crop=(x,y,w,h))]
        return Composite((1280,720),*layers) if layers else Null(1280,720)

    class R13RubPad(renpy.Displayable):
        """Drag over the paper: every grid cell the pointer crosses while pressed gets rubbed."""
        def __init__(self,**kwargs):
            super(R13RubPad,self).__init__(**kwargs);self.down=False
        def cell_at(self,x,y):
            ax,ay,aw,ah=R13_RUB_AREA
            if not (ax<=x<ax+aw and ay<=y<ay+ah):return None
            return (min(R13_RUB_COLS-1,int((x-ax)*R13_RUB_COLS/aw)),min(R13_RUB_ROWS-1,int((y-ay)*R13_RUB_ROWS/ah)))
        def event(self,ev,x,y,st):
            import pygame_sdl2 as pygame
            if ev.type==pygame.MOUSEBUTTONDOWN and ev.button==1 and self.cell_at(x,y):self.down=True
            elif ev.type==pygame.MOUSEBUTTONUP:self.down=False
            if self.down and ev.type in (pygame.MOUSEBUTTONDOWN,pygame.MOUSEMOTION):
                cell=self.cell_at(x,y)
                if cell and r13_rub_add([cell]):renpy.restart_interaction()
        def render(self,width,height,st,at):
            return renpy.Render(1280,720)

label r13_gm_floor:
    $ _st=r13_gm_state("floor")
    $ _msg="침대 밑을 들여다보았다. 판자 하나가 다른 판자보다 조금 들떠 있다."
    while True:
        $ _stage=_st.get("stage","closed")
        call screen r13_life_closeup("floor_"+_stage,tools=(("knife",) if _stage=="closed" and r13_has("own:knife") else ()),actions=[("back","돌아간다")],message=_msg)
        if _return[0]=="action":
            return False
        $ _t=_return[-1];_tool=_return[1] if _return[0]=="use" else None
        if _stage=="closed" and _tool=="knife":
            $ r13_gm_save("floor",stage="open");_st=r13_gm_state("floor")
            $ _msg="칼끝을 틈에 밀어 넣자 판자가 쉽게 들렸다. 아래에 접힌 종이가 있다."
        elif _stage=="closed":
            $ _msg="판자 한쪽 끝이 들떠 있다. 손톱이 겨우 들어갈 만한 틈이 있다. 손으로는 들리지 않는다."
        elif _t=="note":
            $ r13_gm_save("floor",stage="note");_st=r13_gm_state("floor")
            $ _lines=list(ROOM13["activities"]["use_knife_under"]["lines"][1:])
            if r13_home_with_daram():
                $ _lines.insert(1,("daram","이 도토리, 엄마가 그려 주던 거야."))
            # The unfolded note stays behind the dialogue while it is read.
            $ renpy.show("r13_gm_note",what=Transform("assets/r13-gimmick-note-open.webp",xysize=(1280,720),nearest=True))
            call r13_lines(_lines,"activity:use_knife_under:read", binding_route="dynamic:578")
            $ renpy.hide("r13_gm_note")
            return True
        else:
            $ _msg="들어 올린 판자다. 아래 공간은 손바닥만 하다."
    return False

label r13_gm_stone:
    $ _st=r13_gm_state("stone")
    $ _msg="광장 돌 표면은 매끈해 보인다. 가까이 보면 날카로운 것으로 긁은 홈이 여러 줄 지나간다."
    while True:
        $ _paper=_st.get("paper",False)
        if _paper:
            call screen r13_life_closeup("stone_paper",actions=[("sweep","한 줄 문지르기")]+([("read","드러난 자국을 살펴본다")] if r13_rub_enough() else [])+[("back","돌아간다")],
                message=_msg,overlay=Fixed(r13_rub_layer(),R13RubPad(),xysize=(1280,720)))
        else:
            call screen r13_life_closeup("stone_base",tools=(("rubbing",) if r13_has("own:rubbing") else ()),actions=[("back","돌아간다")],message=_msg)
        if _return[0]=="action":
            if _return[1]=="sweep":
                $ _row=min([r for r in range(R13_RUB_ROWS) if len([c for c in r13_rub_cells() if c[1]==r])<R13_RUB_COLS] or [0])
                $ r13_rub_add([(c,_row) for c in range(R13_RUB_COLS)])
                $ _msg="숯을 눕혀 한 줄을 넓게 문질렀다."
            elif _return[1]=="read":
                call r13_lines(ROOM13["activities"]["use_rubbing_stone"]["lines"][1:],"activity:use_rubbing_stone:read", binding_route="dynamic:579")
                return True
            else:
                return False
        elif _paper:
            $ _msg="종이 위를 숯으로 문지르자 긁힌 자리만 하얗게 남는다." if not r13_rub_enough() else "세 줄 넘게 흔적이 드러났다. 이제 살펴볼 수 있다."
        elif _return[0]=="use" and _return[1]=="rubbing":
            $ r13_gm_save("stone",paper=True);_st=r13_gm_state("stone")
            $ _msg="탁본 종이를 돌 표면에 대고 모서리를 눌러 붙였다. 숯을 든 채 종이 위를 끌면 문질러진다."
        else:
            $ _msg="긁힌 홈이 가로로 여러 줄 있다. 손끝으로는 모양을 알아보기 어렵다."
    return False
