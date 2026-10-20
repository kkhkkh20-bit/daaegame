# Approved map-only actions; source receipts and contact review accompany each row.
# Runs after perspective126, map9 176 and Solbang177; never creates residents.
init 178 python:
    R13_MAP_ACTION27 = json.load(renpy.file("assets/room13-map-action27.json"))

    for _m27 in R13_MAP_ACTION27["rows"]:
        if _m27.get("status")!="approved":continue
        _m27_spec=_m27["spec"]
        if not renpy.loadable(_m27_spec["file"]):continue
        R13_ACTING.setdefault(_m27["person"],{})[_m27["pose"]]=_m27_spec
        CAST[_m27["person"]][_m27["pose"]]=_m27_spec
        renpy.image(_m27["person"]+" "+_m27["pose"],Transform(Crop(tuple(_m27_spec["crop"]),_m27_spec["file"]),nearest=True))

    def r13_map27_variant(row,actor,state,daylight,width,has_offer):
        if row.get("status")!="approved" or has_offer:return None
        if actor["person"]!=row.get("person") or state.get("location")!=row.get("location"):return None
        if min(state.get("period",0),2) not in row.get("periods",[]):return None
        if not row.get("min_day",1)<=state.get("day",1)<=row.get("max_day",14):return None
        if "days" in row and state.get("day",1) not in row["days"]:return None
        flags=set(state.get("flags",[]))
        if not set(row.get("need_flags",[]))<=flags or flags.intersection(row.get("not_flags",[])):return None
        # Explicit allowlist: authored events and prior map9 actions are not generic idle.
        if actor["pose"] not in row.get("replace_poses",[]):return None
        variant=row.get("variants",{}).get(daylight)
        if not variant or variant.get("world_width")!=width:return None
        return variant

    def r13_map27_geometry(actor,spec,variant,width):
        # Source anchors are crop-relative pixels. One uniform scale, applied once.
        # Desired height already includes perspective and pose stature; never resize by feet again.
        cw,ch=spec["crop"][2:]
        scale=float(variant["render_height"])/ch
        ax,ay=spec["anchors"][variant["anchor"]]
        tx,ty=variant["target"]
        x=int(round(tx-ax*scale));y=int(round(ty-ay*scale))
        w=int(round(cw*scale));h=int(round(ch*scale))
        for name,target in variant.get("secondary_targets",{}).items():
            sx,sy=spec["anchors"][name]
            if max(abs(x+sx*scale-target[0]),abs(y+sy*scale-target[1]))>variant.get("contact_tolerance",6):
                raise ValueError("map27 secondary contact mismatch: "+name)
        left=max(0,x);top=max(0,y);right=min(width,x+w);bottom=min(720,y+h)
        if right<=left or bottom<=top:raise ValueError("map27 actor outside scene")
        changed=dict(actor)
        changed.update(x=x,y=y,width=w,height=h,rect=[left,top,right-left,bottom-top],
            depth=variant.get("depth",y+h),slot=None,contact=spec.get("contact","standing"),
            occlusion=[],map27_occlusion=variant.get("occlusion",[]),
            map27_keepouts=[[(x+px*scale,y+py*scale) for px,py in poly] for poly in spec.get("foreground_parts",[])])
        return changed

    _r13_map27_stage=r13_stage_people
    def r13_stage_people(entry=False):
        actors=_r13_map27_stage(entry)
        if not R13_MAP_ACTION27["rows"]:return actors
        state=store.room13 or {};width=r13_world_width();daylight=r13_daylight()
        result=[];clearance=[]
        for actor in actors:
            for row in R13_MAP_ACTION27["rows"]:
                # Entry screens also preserve pending events, not only ordinary investigation.
                variant=r13_map27_variant(row,actor,state,daylight,width,bool(r13_offer_for_person(actor["person"])))
                if not variant:continue
                spec=R13_ACTING.get(actor["person"],{}).get(row["pose"])
                if not spec or not renpy.loadable(spec["file"]):continue
                actor=r13_map27_geometry(actor,spec,variant,width)
                actor["pose"]=row["pose"]
                actor["activity"]=row.get("activity",actor.get("activity",""))
                clearance.extend(row.get("clearance",[]))
                break
            result.append(actor)
        # Reserve reviewed working space without changing presence, offers or pose/scale.
        for move in clearance:
            for index,actor in enumerate(result):
                if actor["person"]==move["person"] and actor["pose"] in move["poses"] and not r13_offer_for_person(actor["person"]):
                    result[index]=r13_ma_place(actor,actor["pose"],move["foot"][0],move["foot"][1],actor["height"])
        return sorted(result,key=lambda actor:actor["depth"])

    class R13Map27FurnitureAlphaMask(AlphaMask):
        # Furniture is authored on virtual pixels. Drawable-resolution RTTs
        # resample its edges at small windows, exposing concealed click pixels.
        # Keep the same exact composition for visible art and its focus mask.
        def render(self,width,height,st,at):
            result=super(R13Map27FurnitureAlphaMask,self).render(width,height,st,at)
            result.add_property("drawable_resolution",False)
            result.add_property("texture_scaling","nearest")
            return result

    _r13_map27_visible=r13_staged_visible_art
    def r13_staged_visible_art(actor,still=False):
        # r13_actor_hit_mask calls this same function: no second rectangle-only picker.
        art=_r13_map27_visible(actor,still)
        size=(actor["width"],actor["height"]);origin=(actor["x"],actor["y"])
        for polygon in actor.get("map27_occlusion",[]):
            mask=R13FurnitureMask(polygon,size=size,origin=origin)
            # Authored hand/prop silhouettes may rest ON a counter, in front of its mask.
            for keepout in actor.get("map27_keepouts",[]):
                mask=R13Map27FurnitureAlphaMask(mask,R13FurnitureMask(keepout,size=size,origin=origin),invert=True)
            art=R13Map27FurnitureAlphaMask(art,mask,invert=True)
        return art
