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
            call r13_lines(ROOM13["activities"]["use_knife_burlap"]["lines"][1:],"activity:use_knife_burlap:read")
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
                call r13_lines(ROOM13["activities"]["use_lantern_rear"]["lines"],"activity:use_lantern_rear")
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
                call r13_lines([(None,"같은 모양의 표준 추를 왼쪽 접시에 올렸을 때 가게 추 쪽으로 기울었다. 가운데 조정 나사 둘레에는 새로 긁힌 자국이 있었다."),
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
