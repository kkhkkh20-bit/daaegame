# 현장 생활 동작 배치(2026-10-27, 소유자 "사람들 일상생활을 살아가야 하는데 나를 쳐다보면 안 돼 … 뭔가를 하고 있어야 해").
#
# 배치표 docs/design/FIELD_LIFE_STAGING_20261027.md 를 데이터(assets/room13-field-life.json)로 옮겨
# 장소·시간대·날짜별로 생활 자세와 발 자리를 정한다. 두 가지 일을 한다.
#
# 1) 연기 표 등록. 생활 동작 34장은 원화 시트가 없고 1px 도트 그림(assets/field-dot-v2, origin "life")만 있다.
#    r13_stage_people 사슬은 r13_acting_spec 의 crop·foot·contact 로 기하를 잡으므로, 도트 그림 자체를
#    crop [0,0,w,h] 인 spec 으로 R13_ACTING·CAST 에 넣는다. 맨 끝 도트 층(340)은 같은 그림·같은 발점을 보므로
#    환산이 항등이 되어 자리가 어긋나지 않는다.
# 2) 배치. 표의 행마다 (인물, 장소, 시간대, 날짜, 바꿀 자세)가 맞으면 그 자세로 바꾸고 발을 표의 자리에 둔다.
#    「기존」으로 적힌 자세는 replace_poses 에 없으므로 건드리지 않는다. 사건 표시(offer)가 걸린 사람과
#    생활 묶음(181)이 이미 세운 사람은 그대로 둔다.
#
# 층 순서: map27(178)·생활 묶음(181)·이야기 자세(182) 뒤, 주민 A안(186) 앞 = 183. 그래야 여관 수선 묶음 같은
# 둘 이상의 짝 장면이 이 표보다 앞서고, 조사 물건 회피(337)와 도트 환산(340)은 이 결과를 받아 돈다.
# 좌우 반전은 현장에 없다(회의 화면만 xzoom=-1 을 쓴다). 원화 방향과 표의 「향함」이 다른 자리는 보고에 적는다.
init 183 python:
    R13_FIELD_LIFE=json.load(renpy.file("assets/room13-field-life.json")) if renpy.loadable("assets/room13-field-life.json") else {"contacts":{},"rows":[]}

    def r13_field_life_register():
        # 도트 표(340 에서 또 읽는다)에서 origin "life" 항목만 연기 표로 올린다.
        if not renpy.loadable("assets/room13-field-dot-v2.json"):return 0
        people=json.load(renpy.file("assets/room13-field-dot-v2.json"))["people"]
        contacts=R13_FIELD_LIFE.get("contacts",{})
        count=0
        for person,data in people.items():
            for pose,entry in data.get("poses",{}).items():
                if entry.get("origin")!="life" or not renpy.loadable(entry["file"]):continue
                w,h=entry["size"]
                spec=dict(file=entry["file"],crop=[0,0,w,h],nearest=True,
                    contact=contacts.get(person+":"+pose,"standing"),
                    foot=list(entry.get("foot",[w/2.0,h])),head=list(entry["head"]) if entry.get("head") else None,
                    stature_ratio=round(h/float(data.get("target_dots",210)),3),
                    source_kind="field_life_dot")
                if spec["head"] is None:del spec["head"]
                R13_ACTING.setdefault(person,{})[pose]=spec
                if person in CAST:CAST[person][pose]=spec
                renpy.image(person+" "+pose,Transform(Crop((0,0,w,h),entry["file"]),nearest=True))
                count+=1
        return count

    R13_FIELD_LIFE_REGISTERED=r13_field_life_register()

    def r13_field_life_row(actor,rows,day,period,flags,width,present=()):
        for row in rows:
            if row["person"]!=actor["person"] or period not in row["periods"]:continue
            # 2026-10-27: 같이 선 사람이 있으면 쓰지 않는 행(not_with). 1일 아침 실룩이 돌목 어깨 뒤에서 속삭이는
            # 승인 구도에서 돌목이 쪼그려 명부를 읽으면 실룩의 몸을 반 가린다.
            if set(row.get("not_with",[]))&set(present):continue
            # 같은 장소라도 시간대에 따라 옛 1280 배경으로 돌아가는 곳(우체국 낮·저녁)이 있다. 좌표는 그림에 묶이므로 폭이 다르면 쓰지 않는다.
            if row.get("world_width") and row["world_width"]!=width:continue
            if "days" in row and day not in row["days"]:continue
            if not row.get("min_day",1)<=day<=row.get("max_day",14):continue
            if actor["pose"] not in row["replace_poses"]:continue
            if not set(row.get("need_flags",[]))<=flags or flags.intersection(row.get("not_flags",[])):continue
            spec=r13_acting_spec(actor["person"],row["pose"])
            if not spec or not renpy.loadable(spec["file"]):continue
            return row
        return None

    _r13_field_life_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_field_life_stage(entry)
        s=store.room13 or {}
        location=s.get("location")
        rows=[r for r in R13_FIELD_LIFE.get("rows",[]) if r.get("location")==location]
        if not rows:return actors
        layout=r13_layout(location) or {}
        dx,dy=layout.get("wide_shift",[0,0])
        zoom=r13_field_zoom(location);width=r13_world_width(location)
        day=s.get("day",1);period=min(s.get("period",0),2);flags=set(s.get("flags",[]))
        out=[];present=[a["person"] for a in actors]
        for actor in actors:
            placed=actor
            if not actor.get("life_group") and not r13_offer_for_person(actor["person"]):
                row=r13_field_life_row(actor,rows,day,period,flags,width,present)
                if row:
                    spec=r13_acting_spec(actor["person"],row["pose"])
                    # 도트 그림은 1칸=화면 1px 이므로 월드 키는 도트 높이 / 장면 배율(입구 0.75).
                    height=spec["crop"][3]/float(zoom)
                    tx,ty=row["target"]
                    placed=r13_ma_place(actor,row["pose"],tx+dx,ty+dy,height)
                    placed["slot"]=None
                    # 매대 안/앞(소유자 2026-10-27 "확실하게 매대 앞에서 하는 것인지 매대 안인지 구분"):
                    # 안은 "layout"(넓은 그림의 카운터 폴리곤, 옛 1280 배경은 layout 이 비므로 그 장면의 R13_STAGE_COUNTERS)
                    # 또는 행에 직접 적은 폴리곤으로 다리를 상판에 가린다. 앞은 가림 없음 = 전신.
                    occ=row.get("occlusion")
                    if occ=="layout":
                        mask=list(layout.get("occlusion",[])) if layout else list(R13_STAGE_COUNTERS.get(location,[]))
                    elif isinstance(occ,list):mask=[tuple(p) for p in occ]
                    else:mask=[]
                    placed["occlusion"]=mask
                    # map27 층이 준 매대 마스크는 그 자리에서만 뜻이 있다. 자리를 옮기면 전신이 보여야 하므로 지운다.
                    placed["map27_occlusion"]=[];placed["map27_keepouts"]=[]
                    placed["activity"]=row.get("activity",actor.get("activity",""))
                    placed["field_life"]=row.get("id")
                    # 2026-10-27: 그 물건에서 일하는 행("at_object": 장작더미의 보리)은 그 물건만은 덮어도 된다 — 사슬 끝의
                    # 물건 회피가 보리를 장작더미에서 1,700px 떨어진 화면 밖(327)으로 보냈다. 다른 물건은 그대로 피한다.
                    work=row.get("at_object")
                    work_rect=(layout.get("objects",{}).get(work) if layout else None) or (ROOM13["objects"].get(location,{}).get(work,{}).get("rect") if work else None)
                    placed["work_rect"]=tuple(work_rect) if work_rect else None
            out.append(placed)
        return sorted(out,key=lambda a:a.get("depth",0))
