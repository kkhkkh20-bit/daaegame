# Investigation-scene actions (0.18.63, owner 2026-10-15 15:34 PDT).
# The poses come from dev/apply_map_actions.py (art/map-actions-20261015/registry.json); this
# layer only places them. Dialogue art, story, schedules, events and unlocks are unchanged.
#
# World layout keys (game/assets/room13-world-layout.json), all in world pixels:
#   slot_actions   {person: pose | {daylight: pose}}  a person shown idle (neutral) shows this activity
#   old_scene_slot_actions {person: pose} the same for periods drawn with the old 1280 scene
#   pose_positions {"person:pose": [x,y]} feet of a pinned person for that pose
#   seats          {"person:pose": [x,y,standing_height]}  seat point on drawn furniture; the
#                  figure is the standing height there times the pose's stature_ratio
#   props          [{file, rect:[x,y,w,h], when:{person|offer}}]  separate prop layers drawn
#                  behind the residents, only while the condition holds
# Sizes never stretch a seated, kneeling or crouching pose to the standing height: they use the
# pose's stature_ratio through r13_world_display_height (room13_acting.rpy).
init 125 python:
    def r13_ma_place(actor,pose,fx,fy,height):
        spec=r13_acting_spec(actor["person"],pose) or {}
        w0,h0=r13_actor_geometry(actor["person"],pose)
        foot=spec.get("foot",[w0/2.0,h0])
        scale=float(height)/h0
        x=int(fx-foot[0]*scale);y=int(fy-foot[1]*scale);w=int(w0*scale);h=int(h0*scale)
        changed=dict(actor)
        changed.update(pose=pose,x=x,y=y,width=w,height=h,rect=[max(0,x),max(0,y),w,h],depth=y+h,
            contact=spec.get("contact","standing"))
        return changed

    def r13_ma_feet(actor):
        spec=r13_acting_spec(actor["person"],actor["pose"]) or {}
        w0,h0=r13_actor_geometry(actor["person"],actor["pose"])
        foot=spec.get("foot",[w0/2.0,h0])
        scale=float(actor["height"])/h0
        return actor["x"]+foot[0]*scale,actor["y"]+foot[1]*scale

    def r13_ma_shape(person,pose):
        return r13_world_display_height(person,pose,1000.0,{"standing_height_reference":1000})/1000.0

    _r13_ma_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_ma_stage(entry)
        s=store.room13 or {}
        layout=r13_layout(s.get("location")) if s.get("location") else {}
        if not actors:return actors
        if not layout:
            # 0.18.67: periods without the wide picture keep the old 1280 scene; its own
            # "old_scene_slot_actions" swap poses in place (feet, size and counter mask kept).
            old=R13_WORLD_LAYOUTS.get(s.get("location"),{}).get("old_scene_slot_actions",{})
            if not old:return actors
            layout={"slot_actions":old}
        slot_actions=layout.get("slot_actions",{});spots=layout.get("pose_positions",{});seats=layout.get("seats",{})
        if not (slot_actions or spots or seats):return actors
        result=[]
        for actor in actors:
            person=actor["person"]
            want=slot_actions.get(person)
            # 0.18.75: a value may differ by daylight ({"morning":…, "evening":…}); pinned people
            # (no slot) can be listed too. Only the forced idle pose is replaced, so authored
            # poses (chairs, counters with their own art) stay as they are.
            if hasattr(want,"get"):want=want.get(r13_daylight())  # store dict is RevertableDict
            if (want and actor["pose"]=="neutral" and r13_acting_spec(person,want)
                    and not (not entry and r13_offer_for_person(person))):
                fx,fy=r13_ma_feet(actor)
                height=actor["height"]*r13_ma_shape(person,want)/max(.01,r13_ma_shape(person,actor["pose"]))
                actor=r13_ma_place(actor,want,fx,fy,height)
            key=person+":"+actor["pose"]
            if key in spots:
                actor=r13_ma_place(actor,actor["pose"],spots[key][0],spots[key][1],actor["height"])
            if key in seats:
                sx,sy,standing=seats[key]
                spec=r13_acting_spec(person,actor["pose"]) or {}
                w0,h0=r13_actor_geometry(person,actor["pose"])
                height=standing*r13_ma_shape(person,actor["pose"])
                scale=float(height)/h0
                seat=spec.get("seat",spec.get("foot",[w0/2.0,h0]))
                x=int(sx-seat[0]*scale);y=int(sy-seat[1]*scale)
                actor=dict(actor);actor.update(x=x,y=y,width=int(w0*scale),height=int(h0*scale),
                    rect=[max(0,x),max(0,y),int(w0*scale),int(h0*scale)],depth=y+int(h0*scale),slot=None)
            result.append(actor)
        return sorted(result,key=lambda a:a["depth"])

    def r13_world_props(entry=False):
        """[(displayable, x, y)] prop layers for the current place, in world pixels."""
        s=store.room13 or {}
        layout=r13_layout(s.get("location")) if s.get("location") else {}
        props=layout.get("props",[]) if layout else []
        if not props:return []
        present={a["person"] for a in r13_stage_people(entry)}
        offers={k for k,_ in r13_offers_here()} if not entry else set()
        result=[]
        for prop in props:
            when=prop.get("when",{})
            if "person" in when and when["person"] not in present:continue
            if "offer" in when and when["offer"] not in offers:continue
            if not renpy.loadable(prop["file"]):continue
            x,y,w,h=prop["rect"]
            result.append((Transform(prop["file"],xysize=(w,h),nearest=True),x,y))
        return result
