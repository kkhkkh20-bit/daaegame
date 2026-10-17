# 0.19.17 장소 화면의 방향·매대 뒤 크기 (소유자 2026-10-17)
#   "다들 너무 오른쪽만 보긴 하네." / "매대 뒤에는 너무 작아서 안 보이려나."
# - 방향: 그림은 대부분 오른쪽을 본다. 장소 오른쪽 절반에 선 사람은 좌우를 뒤집어 가운데(손님 쪽)를 보게 한다.
#   소품에 손을 맞춘 사람(perspective_skip, 작업 손 위치로 가림이 붙은 포즈)과 R13_FACING_KEEP 사람은 그대로.
# - 매대 뒤 크기: 깊이 규칙대로면 장터 안쪽 상인이 너무 작다. 매대·창구 뒤 사람(staff_occlusion)은
#   장소별 R13_STAFF_BOOST만큼 발(매대에 가려진 자리)을 기준으로 키운다. 머리가 매대 위로 더 올라온다.
init 127 python:
    R13_STAFF_BOOST={"market":1.35,"square":1.15,"store":1.1}
    R13_FACING_KEEP=set()
    R13_FACING_CONTACTS={"standing","self-contained","held_ledger","held_notebook","sorting","counter_front","carrying_tray"}

    _r13_facing_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_facing_stage(entry)
        s=store.room13 or {}
        location=s.get("location")
        active=r13_layout(location) or {}
        staff=active.get("staff_occlusion",{})
        skip=set(active.get("perspective_skip",[]))|R13_FACING_KEEP
        boost=R13_STAFF_BOOST.get(location,1.0)
        world_w=r13_world_width(location)
        result=[]
        for actor in actors:
            a=dict(actor)
            if a["person"] in staff and boost!=1.0:
                spec=r13_acting_spec(a["person"],a["pose"]) or {}
                pw,ph=r13_actor_geometry(a["person"],a["pose"])
                foot=spec.get("foot",[pw/2.0,ph])
                scale=float(a["height"])/ph
                fx=a["x"]+foot[0]*scale;fy=a["y"]+foot[1]*scale
                ns=scale*boost;w=int(pw*ns);h=int(ph*ns)
                x=int(fx-foot[0]*ns);y=int(fy-foot[1]*ns)
                a.update(x=x,y=y,width=w,height=h,depth=y+h,
                    rect=[max(0,x),max(0,y),max(1,min(world_w,x+w)-max(0,x)),max(1,min(720,y+h)-max(0,y))])
            centre=a["x"]+a["width"]/2.0
            a["flip"]=bool(a["person"]!="daram" and a["person"] not in skip and (a["person"] in staff or not a.get("occlusion"))
                and (a.get("contact") in R13_FACING_CONTACTS or a["person"] in staff) and centre>world_w/2.0)
            result.append(a)
        return sorted(result,key=lambda x:x["depth"])

    _r13_facing_art=r13_staged_art
    def r13_staged_art(actor,still=False):
        art=_r13_facing_art(actor,still)
        return Transform(art,xzoom=-1.0) if actor.get("flip") else art

    _r13_facing_face=r13_actor_face
    def r13_actor_face(actor,margin=10):
        x,y,w,h=_r13_facing_face(actor,margin)
        if not actor.get("flip"):return (x,y,w,h)
        # Mirror the head box inside the sprite's own rectangle.
        return (actor["x"]+actor["width"]-(x-actor["x"])-w,y,w,h)
