# Morning-only staff-side placement. Existing art, identities, events and schedules are authoritative.
# Runs after contacts179, balance180 and groups181; never creates or replaces a resident.
init 182 python:
    R13_POST_STAFF_CONTACT = dict(
        background="assets/room13-pixel-wide-post-morning.webp", crop=(0,0,2160,720),
        source="assets/room13-pixel-acting-seryeon.webp", source_crop=(596,514,385,461),
        # The clipboard is HELD, not planted on the counter. Crop-relative hand(321,181)
        # lands at(1566,432); same approved pose, adjusted for reviewed counter depth.
        hand=(1566,432), height=234, depth=560,
        # Local rear edge of the actual morning counter, not a scaled1280 mask.
        # Only x1368..1606 intersects this actor; bound the mask to this reviewed span.
        foreground=((1368,511),(1410,503),(1450,496),(1500,488),(1550,480),(1606,471),
                    (1606,720),(1368,720)),
    )

    def r13_post_staff_contact(actors):
        state=store.room13 or {}
        if state.get("location")!="post" or state.get("period")!=0:return actors
        contact=R13_POST_STAFF_CONTACT;layout=r13_layout("post")
        if (r13_world_width()!=2160 or layout.get("files",{}).get("morning")!=contact["background"]
                or tuple(layout.get("crops",{}).get("morning",()))!=contact["crop"]):return actors
        # Preserve an authored event composition as a unit, not just its offer owner.
        if any(r13_offer_for_person(a["person"]) for a in actors):return actors
        result=[]
        for actor in actors:
            if actor["person"]=="seryeon" and actor["pose"]=="action_1":
                spec=r13_acting_spec("seryeon","action_1") or {}
                # A new source needs its own furniture review; do not fallback to another crop.
                if (spec.get("file")==contact["source"] and tuple(spec.get("crop",()))==contact["source_crop"]
                        and tuple(spec.get("hand",()))==(321,181)):
                    actor=r13_contact_geometry(actor,"action_1","hand",contact["hand"],contact["height"],contact["depth"])
                    actor["map27_occlusion"]=[list(contact["foreground"])]
                    actor["map27_keepouts"]=[]
                    actor["activity"]="우편 창구 안쪽에서 접수 내용을 기록한다."
            result.append(actor)
        return sorted(result,key=lambda a:a["depth"])

    _r13_post_staff_stage=r13_stage_people
    def r13_stage_people(entry=False):
        return r13_post_staff_contact(_r13_post_staff_stage(entry))
