# Approved map actions only. Dialogue, profiles, schedules and authored event poses stay separate.
init 176 python:
    R13_MAP_WORK_NINE=json.load(renpy.file("assets/room13-map-work-nine.json"))
    for _mw in R13_MAP_WORK_NINE["people"]:
        _mp,_mk,_ms=_mw["person"],_mw["pose"],_mw["spec"]
        R13_ACTING.setdefault(_mp,{})[_mk]=_ms
        CAST[_mp][_mk]=_ms
        renpy.image(_mp+" "+_mk,Transform(Crop(tuple(_ms["crop"]),_ms["file"]),nearest=True))

    def r13_map_work_nine_allowed(row,actor,state,has_offer=False):
        if has_offer or state.get("location")!=row["location"] or min(state.get("period",0),2) not in row["periods"]:return False
        if row["person"]=="resident_piko":
            return state.get("day",1)>=11 and actor["pose"] in ("neutral","distressed","activity")
        return actor["pose"] in ("neutral","activity","inn_activity","world")

    _r13_map9_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_map9_stage(entry)
        state=store.room13 or {}
        rows={r["person"]:r for r in R13_MAP_WORK_NINE["people"]}
        result=[]
        for actor in actors:
            row=rows.get(actor["person"])
            if not row or not r13_map_work_nine_allowed(row,actor,state,not entry and bool(r13_offer_for_person(actor["person"]))):
                result.append(actor);continue
            person,pose=row["person"],row["pose"]
            if person=="resident_piko":
                # Source coordinates -> world with one uniform scale; blanket masks drawing AND picking.
                c=row["contacts"];scale=c["source_to_world_uniform_scale"]
                cx,cy,cw,ch=row["spec"]["crop"];tx,ty=c["source_top_left_world_px"]
                x,y=int(round(tx+cx*scale)),int(round(ty+cy*scale));w,h=int(round(cw*scale)),int(round(ch*scale))
                actor=dict(actor);actor.update(pose=pose,x=x,y=y,width=w,height=h,rect=[x,y,w,h],depth=y+h,
                    contact="lying",slot=None,occlusion=c["foreground_polygon_world_px"])
            else:
                fx,fy=r13_ma_feet(actor)
                height=actor["height"]*r13_ma_shape(person,pose)/max(.01,r13_ma_shape(person,actor["pose"]))
                actor=r13_ma_place(actor,pose,fx,fy,height)
                if person=="resident_guldol":
                    # Stone held at the workshop bench surface, feet behind the bench mask.
                    spec=row["spec"];c=row["contacts"];point=c["contacts_normalized_full_canvas"]["stone_external_workbench"]
                    width,height0=row["source_size"];cx,cy,cw,ch=spec["crop"];scale=float(actor["height"])/ch
                    x=int(round(800-(point[0]*width-cx)*scale));y=int(round(454-(point[1]*height0-cy)*scale))
                    actor=dict(actor);actor.update(x=x,y=y,rect=[x,y,actor["width"],actor["height"]],depth=y+actor["height"],slot=None,
                        occlusion=R13_WORLD_LAYOUTS["workshop"].get("occlusion",[]))
            result.append(actor)
        return sorted(result,key=lambda a:a["depth"])
