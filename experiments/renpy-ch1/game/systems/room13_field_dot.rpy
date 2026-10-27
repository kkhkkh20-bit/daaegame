# 현장(조사 화면) 인물의 도트 칸 통일(2026-10-27, 소유자 "캐릭터 조사하기에 나오는 사람들 크기랑 이미지 도트 사이즈가 다 다름").
#
# 원인: 현장 인물은 자리표의 키(205~340px)에 맞춰 원본(대부분 도트풍으로 그린 부드러운 고해상 그림, 인물마다
# 해상도가 다름)을 연속 배율로 줄여 그렸다. 0.20.62 에서 2px 격자(Flatten)를 씌웠지만 격자 안의 내용 해상도가
# 인물마다 달라 칸이 제각각으로 보였고, 원근(0.75~1.25 연속)과 생활 동작 비율이 또 비정수 배율을 만들었다.
#
# 규칙:
# - 모든 현장 그림을 대화 도트판과 같은 도트 수로 다시 찍었다(assets/field-dot-v2, 표 room13-field-dot-v2.json).
#   서 있는 그림은 대화 도트판(어른 210·덩치 230·노인 195·부리 185·아이 165·도담 132 도트)을 1배로 되돌린 것,
#   몸동작 그림은 같은 칸 크기로 칸 평균 축소한 것이다. 키 비율(어른 210 : 아이 165 : 도담 132)은 승인값 그대로다.
# - 장면마다 "화면 1px = 도트 k 칸"의 k 를 정수로 하나 정한다(R13_FIELD_DOT_SCREEN_PX, 기본 1). 축소된 현장(입구 0.75)은
#   월드 좌표에서 k/0.75 배로 그려 화면에서는 똑같이 정수 px 가 되게 한다. 최근접(nearest)으로만 그린다.
# - 원근은 정수 단계로만 둔다: 원근층이 낸 배율(0.75~1.25)을 k 에 곱해 반올림한다. k=1 인 장면에서는 1 아래 정수가 없으므로
#   모두 같은 크기다(한 장면 안에서 칸 크기가 같은 것이 목표). k=2 로 둔 장면에서만 뒷줄이 1배로 떨어질 수 있다.
# - 자리는 그대로다: 발(걸린 인물은 고리, 앉은 인물은 좌석, 작업대에 손을 댄 인물은 손)의 월드 좌표를 지키고 그림 크기만 바꾼다.
#   축소 현장에서는 화면 px 가 정수가 되게 월드 좌표를 1/배율 단위로 맞춘다(입구: 4px 단위 = 화면 3px).
# - 클릭 영역·이름표는 표의 머리 상자(도트 좌표)로 잡는다(r13_actor_face / r13_actor_face_target 이 actor["dot"] 를 본다).
# - 표에 없는 자세(실행 중에 생긴 것)는 예전 경로로 그리고 로그에 남긴다 — 조용히 틀어지지 않게.
init 340 python:
    R13_FIELD_DOT=json.load(renpy.file("assets/room13-field-dot-v2.json"))["people"] if renpy.loadable("assets/room13-field-dot-v2.json") else {}
    # 장면별 "화면 1px 당 도트 칸 수"의 역수, 즉 도트 한 칸이 화면에서 몇 px 인가. 기본 1. 2 로 두면 앞줄 2배·뒷줄 1배가 된다.
    R13_FIELD_DOT_SCREEN_PX={}
    R13_FIELD_DOT_DEFAULT_PX=1
    R13_FIELD_DOT_MISSING=set()

    def r13_field_dot_px(location=None):
        location=location or (store.room13 or {}).get("location")
        return int(R13_FIELD_DOT_SCREEN_PX.get(location,R13_FIELD_DOT_DEFAULT_PX))

    def r13_field_dot_entry(person,pose):
        return R13_FIELD_DOT.get(person,{}).get("poses",{}).get(pose)

    def r13_field_dot_anchor_kind(actor,spec,layout):
        # r13_stage_people 이 자리를 잡을 때 쓴 기준점과 같은 것을 고른다.
        contact=actor.get("contact") or spec.get("contact","standing")
        if contact=="hanging":return "hook"
        if contact in ("background_bench","background_chair") and spec.get("seat"):return "seat"
        location=(store.room13 or {}).get("location")
        work=layout.get("work",{}).get(actor["person"]) if layout else {
            ("granny","inn"):1,("buri","workshop"):1,("seryeon","post"):1,("mom","greenhouse"):1,("neoul","facility"):1}.get((actor["person"],location))
        if work and spec.get("hand") and contact not in ("self_seated","portable_stool","portable_crate","portable_bucket","floor_sit","ground","kneeling","squatting","crouching","background_chair"):
            return "hand"
        return "foot"

    def r13_field_dot_source_point(kind,spec,width,height):
        if kind=="hook":return spec.get("hook",spec.get("foot",[width/2.0,0]))
        if kind=="seat":return spec["seat"]
        if kind=="hand":return spec["hand"]
        return spec.get("foot",spec.get("anchor",{}).get("foot",[width/2.0,height]))

    def r13_field_dot_point(kind,entry):
        if kind=="hook":return entry.get("hook",entry.get("foot",[entry["size"][0]/2.0,0]))
        if kind in ("seat","hand"):return entry[kind]
        return entry.get("foot",[entry["size"][0]/2.0,float(entry["size"][1])])

    _r13_field_dot_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_field_dot_stage(entry)
        s=store.room13 or {}
        location=s.get("location")
        if not location:return actors
        if not R13_FIELD_DOT:return r13_clear_objects_last(actors,location)
        zoom=r13_field_zoom(location)
        layout=r13_layout(location)
        world_w=r13_world_width(location);world_h=r13_world_height(location)
        px=r13_field_dot_px(location)
        # 월드 좌표 단위: 화면 px 가 정수가 되는 가장 작은 월드 px(입구 0.75 → 4).
        unit=1
        for cand in (1,2,3,4,5,6,7,8):
            if abs(cand*zoom-round(cand*zoom))<1e-6:unit=cand;break
        result=[]
        for actor in actors:
            dot=r13_field_dot_entry(actor["person"],actor["pose"])
            if not dot:
                key=(actor["person"],actor["pose"])
                if key not in R13_FIELD_DOT_MISSING:
                    R13_FIELD_DOT_MISSING.add(key)
                    renpy.log("현장 도트 표에 없는 자세: %s %s (예전 경로로 그림)"%key)
                result.append(actor);continue
            spec=r13_acting_spec(actor["person"],actor["pose"]) or {}
            pw,ph=r13_actor_geometry(actor["person"],actor["pose"])
            old_scale=float(actor["height"])/ph
            kind=r13_field_dot_anchor_kind(actor,spec,layout)
            try:
                sp=r13_field_dot_source_point(kind,spec,pw,ph);dp=r13_field_dot_point(kind,dot)
            except KeyError:
                kind="foot";sp=r13_field_dot_source_point(kind,spec,pw,ph);dp=r13_field_dot_point(kind,dot)
            ax=actor["x"]+sp[0]*old_scale;ay=actor["y"]+sp[1]*old_scale
            # 원근층이 낸 배율은 정수 단계로만 받는다(k=1 이면 항상 1).
            step=max(1,int(round(px*actor.get("perspective_factor",1.0))))
            scale=step/float(zoom)
            dw,dh=dot["size"]
            w=int(round(dw*scale));h=int(round(dh*scale))
            x=ax-dp[0]*scale;y=ay-dp[1]*scale
            x=int(round(x/unit))*unit;y=int(round(y/unit))*unit
            x=max(0,min(world_w-w,x)) if w<=world_w else 0
            left=max(0,x);top=max(0,y);right=min(world_w,x+w);bottom=min(world_h,y+h)
            changed=dict(actor)
            changed.update(x=x,y=y,width=w,height=h,rect=[left,top,max(1,right-left),max(1,bottom-top)],depth=y+h,
                dot=dict(file=dot["file"],scale=scale,size=[dw,dh],head=dot.get("head"),anchor_kind=kind))
            result.append(changed)
        return r13_clear_objects_last(result,location)

    def r13_clear_objects_last(actors,location):
        # 조사 물건 회피는 배치 사슬의 맨 끝, 도트 환산이 끝난 사각형으로 한 번만 한다.
        # 바닥 소품(keepouts)은 이야기 모드와 무관하게 늘 비킨다(통 안에 선 사람은 어느 모드에서도 틀리다).
        width=r13_world_width(location)
        keepouts=r13_stage_keepouts(location,r13_layout(location) or None)
        rects=[tuple(r) for r in r13_stage_critical(location,r13_layout(location))] if r13_v111_active() else []
        if rects or keepouts:actors=r13_clear_objects(actors,rects,width,keepouts)
        actors=r13_clamp_to_world(actors,width)
        return sorted(actors,key=lambda a:a.get("depth",0))
