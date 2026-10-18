# Furniture surfaces and elevated ground are separate coordinates. Existing residents only.
# Final placement after approved map31; original art, schedules and event offers stay authoritative.
init 179 python:
    # Same-child head heights: bed 104/110px; nearer rug 115/120px.
    # These are final pose heights, never multiplied by child/seat stature again.
    R13_HOME_CONTACTS = {
        "room13": {
            "action_1": ("seat",1120,382,175,510),
            "action_2": ("foot",1190,620,253,620),
            "inspect_floor": ("foot",1140,622,189,622),
            "rest": ("foot",1240,620,193,620),
        },
        "guestroom": {
            "action_1": ("seat",880,370,184,500),
            "action_2": ("foot",880,620,264,620),
            "inspect_floor": ("foot",865,622,197,622),
            "rest": ("foot",875,620,201,620),
        },
    }
    R13_SQUARE_LEVELS = {
        "resident_sling": dict(poses=("activity","neutral"),foot=(1370,434),ground=520,elevation=86,standing=198),
        "resident_seol": dict(poses=("living_bellrope","neutral"),foot=(365,415),ground=460,elevation=45,standing=175),
    }

    def r13_contact_geometry(actor,pose,anchor,target,height,depth):
        spec=r13_acting_spec(actor["person"],pose) or {}
        w0,h0=r13_actor_geometry(actor["person"],pose)
        point=spec.get(anchor,spec.get("foot",[w0/2.0,h0]))
        scale=float(height)/h0
        x=int(round(target[0]-point[0]*scale));y=int(round(target[1]-point[1]*scale))
        w=int(round(w0*scale));h=int(round(h0*scale))
        changed=dict(actor)
        changed.update(pose=pose,x=x,y=y,width=w,height=h,rect=[x,y,w,h],depth=depth,
            slot=None,occlusion=[],contact=spec.get("contact","standing"))
        return changed

    _r13_contact_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_contact_stage(entry)
        state=store.room13 or {};location=state.get("location")
        result=[]
        for actor in actors:
            person=actor["person"]
            if not r13_offer_for_person(person):
                if person=="daram" and location in R13_HOME_CONTACTS and r13_home_with_daram():
                    pose=actor["pose"]
                    # The unresolved-case resting pose uses the approved seated source, not a standing figure on a bed.
                    resting=pose=="neutral" and state.get("case_state")=="occurred" and state.get("trial_result")=="pending"
                    key="rest" if resting else pose
                    if key in R13_HOME_CONTACTS[location]:
                        anchor,x,y,height,depth=R13_HOME_CONTACTS[location][key]
                        actor=r13_contact_geometry(actor,"action_1" if resting else pose,anchor,(x,y),height,depth)
                        if resting:actor["activity"]="깔개에 앉아 쉬는 중"
                elif location=="clinic" and person=="resident_seori" and actor["pose"]=="living_notes" and min(state.get("period",0),2) in (0,2):
                    old=r13_acting_spec(person,actor["pose"]);w0,h0=r13_actor_geometry(person,actor["pose"])
                    foot=old.get("foot",old.get("anchor",{}).get("foot",[w0/2.0,h0]))
                    scale=actor["height"]/float(h0);target=(actor["x"]+foot[0]*scale,actor["y"]+foot[1]*scale)
                    review=R13_SEORI_MAP_REVIEW;spec=review["spec"]
                    if renpy.loadable(spec["file"]):
                        # Equal head size at this floor depth; canvas height differs between approved poses.
                        height=old["head"][3]*scale*spec["crop"][3]/spec["head"][3]
                        actor=r13_contact_geometry(actor,review["pose"],"foot",target,height,actor["depth"])
                        actor["activity"]="환자 쪽으로 서서 확인할 서류를 살펴본다."
                elif location=="inn" and r13_world_width()==1920 and person=="granny" and actor["pose"]=="living_keyledger":
                    # Keep the approved carried ledger/key art and its established height.
                    # Crop-relative lower book edge (220,355) sits above the drawn register.
                    spec=r13_acting_spec(person,actor["pose"]);w0,h0=r13_actor_geometry(person,actor["pose"])
                    scale=float(actor["height"])/h0;foot=spec["foot"]
                    target=(1600+(foot[0]-220)*scale,340+(foot[1]-355)*scale)
                    actor=r13_contact_geometry(actor,actor["pose"],"foot",target,actor["height"],target[1])
                    layout=r13_layout("inn");rx,ry,rw,rh=layout["objects"]["register"]
                    actor["map27_occlusion"]=[layout["occlusion"],[(rx,ry),(rx+rw,ry),(rx+rw,ry+rh),(rx,ry+rh)]]
                    actor["map27_keepouts"]=[]
                elif location=="square" and r13_world_width()==1920 and person in R13_SQUARE_LEVELS:
                    level=R13_SQUARE_LEVELS[person]
                    if actor["pose"] in level["poses"]:
                        height=level["standing"]*r13_ma_shape(person,actor["pose"])
                        actor=r13_contact_geometry(actor,actor["pose"],"foot",level["foot"],height,level["ground"])
                        actor["ground_depth"]=level["ground"];actor["elevation"]=level["elevation"]
            result.append(actor)
        return sorted(result,key=lambda a:a["depth"])
