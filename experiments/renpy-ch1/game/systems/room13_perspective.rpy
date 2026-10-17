# Perspective (owner, 0.18.57): "캐릭터 배치시킬 때 원근법 반영해서 크기 조절해."
# Whoever stands deeper in the picture (feet higher on screen) is drawn smaller. Each place has
# one line, standing height = a * feet_y + b, taken from its authored floor spots
# (room13-world-layout.json floors/slots). The post office had none that agreed (people behind
# the counter were drawn larger than people on the front floor), so its line is set by hand and
# people behind its counter count as standing 60px deeper than their hidden feet.
# Furniture-bound poses (hanging, benches, chairs, seats, hands on a workbench) and Daram at home
# keep their authored size; pose shape and stature still come from r13_world_display_height.
#
# 2026-10-17 (owner approved docs/placement_mockups, docs/ACTION_REQUEST_20261017.md §1): one rule
# for every place, standing adult height h(y) = H700*(y-yv)/(700-yv), stored as "perspective" [a,b]
# in room13-world-layout.json. Each person's height is h(y) times their build (R13_STATURE: child
# .76, teen .90, elder .95, a few individual values). People serving behind a counter or stall
# ("staff_occlusion" in the layout) stand at their real, hidden feet and follow the same line.
# "perspective_skip" lists people whose art is matched to a prop layer (따닥 at the door frame).
init 126 python:
    R13_PERSPECTIVE={
        "inn":(0.309,50),"square":(0.381,0),"store":(0.719,-141),"workshop":(0.406,-7),
        "gate":(0.217,94),"hall":(0.608,-117),"school":(0.215,119),"altar":(0.342,29),
        "dining":(0.642,-128),"post":(0.38,0),
    }
    R13_PERSPECTIVE_COUNTER_DEPTH={"post":60}
    R13_STATURE_GROUPS={
        "child":("daram","bami","resident_kongi","resident_somi","resident_tosil","resident_jongjong"),
        "teen":("buri","nabi","doto","resident_tori","resident_kkwak","resident_mungchi","resident_ubak","resident_guseul"),
        "elder":("granny","resident_owlgp","resident_ppul","resident_musoe","resident_guldol"),
    }
    R13_STATURE_BASE={"child":.76,"teen":.90,"elder":.95}
    R13_STATURE_FIX={"resident_bori":1.06,"resident_tok":1.04,"resident_teacher":1.04,"resident_mungchi":.96}

    def r13_stature(person,layout=None):
        # A place's own standing_heights (e.g. the hall's bat) still win for the people it lists.
        layout=layout or {}
        own=layout.get("standing_heights",{})
        if person in own and layout.get("standing_height_reference"):
            return own[person]/float(layout["standing_height_reference"])
        if person in R13_STATURE_FIX:return R13_STATURE_FIX[person]
        for group,people in R13_STATURE_GROUPS.items():
            if person in people:return R13_STATURE_BASE[group]
        return 1.0

    R13_PERSPECTIVE_CONTACTS={"standing","self-contained","held_ledger","held_notebook","sorting",
        "carrying_tray","counter_front","floor_sit","kneeling","portable_stool","portable_crate",
        "portable_bucket","squatting","crouching"}

    def r13_perspective_line(location):
        # 0.18.59: a wide picture (room13-world-layout.json "perspective") has its own floor
        # spots and so its own line; the old 1280 scenes keep the lines above.
        layout=r13_layout(location)
        if layout and layout.get("perspective"):return tuple(layout["perspective"])
        return R13_PERSPECTIVE.get(location)

    def r13_perspective_height(location,feet):
        a,b=r13_perspective_line(location)
        return a*feet+b

    _r13_perspective_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_perspective_stage(entry)
        s=store.room13 or {}
        location=s.get("location")
        if r13_perspective_line(location) is None:return actors
        layout=getattr(store,"R13_WORLD_LAYOUTS",{}).get(location,{})
        # Pose shape only; build comes from r13_stature (not counted twice).
        probe_layout=dict(layout,standing_height_reference=1000,standing_heights={})
        world_w=r13_world_width(location)
        active=r13_layout(location)
        staff=active.get("staff_occlusion",{}) if active else {}
        skip=active.get("perspective_skip",[]) if active else []
        result=[]
        for actor in actors:
            if actor["person"]=="daram" or actor["person"] in skip or (actor.get("contact") not in R13_PERSPECTIVE_CONTACTS and actor["person"] not in staff):
                result.append(actor);continue
            spec=r13_acting_spec(actor["person"],actor["pose"]) or {}
            pw,ph=r13_actor_geometry(actor["person"],actor["pose"])
            foot=spec.get("foot",spec.get("anchor",{}).get("foot",[pw/2.0,ph]))
            scale=float(actor["height"])/ph
            fx=actor["x"]+foot[0]*scale;fy=actor["y"]+foot[1]*scale
            depth_feet=fy
            slot=actor.get("slot")
            behind_counter=bool(slot and len(slot)>3 and slot[3]=="counter")
            if behind_counter:depth_feet-=R13_PERSPECTIVE_COUNTER_DEPTH.get(location,0)
            shape=r13_world_display_height(actor["person"],actor["pose"],1000.0,probe_layout)/1000.0
            target=r13_perspective_height(location,depth_feet)*shape*r13_stature(actor["person"],layout)
            factor=max(.6,min(1.4,target/float(actor["height"])))
            if abs(factor-1)<.04:
                result.append(actor);continue
            new_scale=scale*factor
            w=int(pw*new_scale);h=int(ph*new_scale)
            x=int(fx-foot[0]*new_scale);y=int(fy-foot[1]*new_scale)
            if behind_counter:
                # Feet are hidden by the counter: shrink about the middle of the body so the head
                # does not sink behind the counter or parcels.
                y=int(actor["y"]+actor["height"]/2.0-h/2.0)
            left=max(0,x);top=max(0,y);right=min(world_w,x+w);bottom=min(720,y+h)
            changed=dict(actor)
            changed.update(x=x,y=y,width=w,height=h,rect=[left,top,max(1,right-left),max(1,bottom-top)],depth=y+h)
            result.append(changed)
        return sorted(result,key=lambda a:a["depth"])
