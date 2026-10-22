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
