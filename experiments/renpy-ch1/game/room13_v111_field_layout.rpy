# Field staging keeps investigable objects clear (owner-approved plan 2026-10-22, item 1:
# "조사할 때 인물이 방해하지 않게 — 캐릭터 크기는 유지하고, 증거를 가리지 않는 자리로 배치").
# r13_stage_people (room13_acting.rpy) scores each standing slot; a body covering a "critical"
# rectangle costs a lot. Besides the layout's fixed list, every object the current story step
# lets the player inspect at this place now counts as critical, so residents stand elsewhere.
init 336 python:
    def r13_stage_critical(location,layout):
        base=list(layout.get("critical",R13_STAGE_CRITICAL.get(location,[]))) if layout else list(R13_STAGE_CRITICAL.get(location,[]))
        if not r13_v111_active() or location!=(store.room13 or {}).get("location"):
            return base
        objects=ROOM13["objects"].get(location,{})
        for option in r13_v111_binding().get("options",[]):
            key=option.get("object")
            if not key or option.get("location")!=location:continue
            spec=objects.get(r13_v111_object_key(key)) or objects.get(key)
            rect=spec and spec.get("rect")
            if rect and tuple(rect) not in [tuple(r) for r in base]:base.append(tuple(rect))
        return base

    # A resident chosen into a free slot can end up behind someone staged later at a fixed spot
    # (gate: 실룩 behind 바둑이, owner QA 2026-10-22 mockup note). If a free-slot resident's face is
    # covered by a body in front, stage the fixed-position people first and choose again.
    R13_STAGE_ORDER_OVERRIDE=None
    _r13_order_visible_people=r13_visible_people
    def r13_visible_people():
        people=_r13_order_visible_people()
        order=R13_STAGE_ORDER_OVERRIDE
        if order:
            people=[p for p in order if p in people]+[p for p in people if p not in order]
        return people

    def r13_stage_face_covered(rows):
        for i,a in enumerate(rows):
            if not a.get("slot"):continue
            try:fx,fy,fw,fh=r13_actor_face_target(a)
            except Exception:continue
            cx,cy=fx+fw/2.0,fy+fh/2.0
            for b in rows:
                if b is a:continue
                bx,by,bw,bh=b["rect"]
                if bx<=cx<=bx+bw and by<=cy<=by+bh and by+bh>a["rect"][1]+a["rect"][3]:
                    return True
        return False

    _r13_order_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        global R13_STAGE_ORDER_OVERRIDE
        rows=_r13_order_stage_people(entry)
        if R13_STAGE_ORDER_OVERRIDE is None and r13_v111_active() and r13_stage_face_covered(rows):
            fixed=[a["person"] for a in rows if not a.get("slot")]
            R13_STAGE_ORDER_OVERRIDE=fixed+[a["person"] for a in rows if a.get("slot")]
            try:
                again=_r13_order_stage_people(entry)
            finally:
                R13_STAGE_ORDER_OVERRIDE=None
            if not r13_stage_face_covered(again):rows=again
        return rows

    # Stand spots by role (owner 2026-10-22, mockup D: "서 있을 자리를 먼저 정한다").
    # Gate: the gatekeeper beside the right gate post, the carter whispering at his shoulder,
    # Karo kneeling at his own wheel, Daram beside him with her notebook, Bori carrying wood at
    # the woodpile. The gate passage and the booth papers stay clear; ordinary things (the
    # cart, crates, fence) have people beside them so the empty space is not a pointer.
    R13_STAND_SPOTS={
        "gate":dict(
            positions={"guard":[1234,592,222],"resident_siluk":[1290,545,212],"karo":[630,628,230],
                       "daram":[730,704,205],"resident_bori":[1770,666,238]},
            poses={"guard":"neutral","daram":"thinking","resident_siluk":"event_whisper","karo":"living_axlewrap",
                   "resident_bori":"map27_carry_firewood_v2"},
            pose_positions={"karo:living_axlewrap":[630,628]},
            pinned=["karo","guard","daram","resident_siluk","resident_bori"],
        ),
        # 0.20.9 (play review D23-01): the north exchange box (1150-1370) stays clear. Chorong stands
        # at its left edge with her lamp, Silluk a step behind her.
        "forest":dict(
            positions={"resident_lamplighter":[1060,700,226],"resident_siluk":[880,700,240]},
            poses={},
            pose_positions={},
            pinned=["resident_lamplighter","resident_siluk"],
        ),
    }
    for _spot_place,_spot in R13_STAND_SPOTS.items():
        _spot_layout=R13_WORLD_LAYOUTS.get(_spot_place)
        if not _spot_layout:continue
        # Spots are written against the old 1920x720 picture; a wider picture moves them with it.
        _sdx,_sdy=_spot_layout.get("wide_shift",[0,0])
        _spot=dict(_spot,positions={k:[v[0]+_sdx,v[1]+_sdy]+v[2:] for k,v in _spot["positions"].items()},
            pose_positions={k:[v[0]+_sdx,v[1]+_sdy] for k,v in _spot["pose_positions"].items()})
        _spot_layout["positions"]=dict(_spot_layout.get("positions",{}),**_spot["positions"])
        _spot_layout["poses"]=dict(_spot_layout.get("poses",{}),**_spot["poses"])
        _spot_layout["pose_positions"]=dict(_spot_layout.get("pose_positions",{}),**_spot["pose_positions"])
        _spot_layout["pinned"]=list(dict.fromkeys(list(_spot_layout.get("pinned",[]))+_spot["pinned"]))

    # People with no part in the current gate scene go where their day's work is
    # ("다른 주민은 생활과 이야기상 맞는 장소로 분산"): Nero to the general store, Badook to the
    # square patrol. Anyone the current scene names, or who has an option here, stays.
    R13_RELOCATE={("gate","resident_nero"):"store",("gate","resident_badook"):"square"}
    def r13_v111_needed_at(person,place):
        if not r13_v111_active():return True
        binding=r13_v111_binding()
        if person in binding.get("people",[]):return True
        return any(o.get("person")==person and o.get("location")==place for o in binding.get("options",[]))
    _r13_relocate_where=r13_where
    def r13_where(person):
        place=_r13_relocate_where(person)
        target=R13_RELOCATE.get((place,person))
        if target and not r13_v111_needed_at(person,place):return target
        return place

init 337 python:
    # 0.20.9 (play review D23-01): fixed daily-work spots (map27, e.g. Kalbaram in the forest) are
    # placed after the slot scoring and can still stand on the object the current story step needs.
    # Such a figure steps sideways off it: same pose and height, only the feet move along the floor.
    def r13_clear_critical_x(actor,rects,others,width):
        ax,ay,aw,ah=actor["rect"]
        for ox,oy,ow,oh in rects:
            cover=min(ax+aw,ox+ow)-max(ax,ox)
            if cover<=aw*0.3 or ay+ah<=oy:continue
            foot_y=actor["y"]+actor["height"]
            sides=[ox-aw/2.0-24-k*80 for k in range(8)]+[ox+ow+aw/2.0+24+k*80 for k in range(8)]
            sides=[f for f in sides if aw/2.0<=f<=width-aw/2.0]
            def crowd(f):
                return sum(1 for b in others if b is not actor and abs((b["rect"][0]+b["rect"][2]/2.0)-f)<(aw+b["rect"][2])/2.0)
            if not sides:continue
            cx=ax+aw/2.0
            best=min(sides,key=lambda f:(crowd(f),abs(f-cx)))
            return r13_ma_place(actor,actor["pose"],int(best),foot_y,actor["height"])
        return actor

    _r13_clear_stage_people=r13_stage_people
    def r13_stage_people(entry=False):
        rows=_r13_clear_stage_people(entry)
        if not r13_v111_active():return rows
        location=(store.room13 or {}).get("location")
        rects=[tuple(r) for r in r13_stage_critical(location,R13_WORLD_LAYOUTS.get(location))]
        if not rects:return rows
        width=r13_world_width()
        out=[]
        for actor in rows:
            out.append(r13_clear_critical_x(actor,rects,rows,width) if actor.get("rect") else actor)
        return sorted(out,key=lambda a:a.get("depth",0))
