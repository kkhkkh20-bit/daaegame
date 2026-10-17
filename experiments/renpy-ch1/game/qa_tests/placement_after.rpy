# 2026-10-17 placement / perspective review (docs/ACTION_REQUEST_20261017.md, docs/placement_mockups).
# For each place, a busy scheduled time (people actually present, fixed spots preferred) is staged with the
# game's own r13_stage_people and drawn with the game's own background, prop layers and actor art
# (furniture masks included) at the full panorama width. Output: $ROOM13_QA_OUT/placement/<place>.png
# and <place>.json (who stands where). dev tool: label them into docs/placement_mockups/after/.
init 999 python:
    R13_QA_PLACEMENT_PLACES=("market","post","square","inn","store","clinic","workshop","school","gate",
        "facility","greenhouse","dining","hall","river","forest","altar")

    def r13_qa_placement_states(base,location):
        variants=[(),("week2_started",)]
        for day in range(1,15):
            for period in range(3):
                for extra in variants:
                    n=winter_copy.deepcopy(base)
                    n.update(day=day,period=period,location=location)
                    if extra:
                        n.update(week2_started=True,case_state="occurred")
                    yield n

    def r13_qa_placement_shots():
        import os,json as qa_json
        out=os.path.join(os.environ.get("ROOM13_QA_OUT","/tmp/room13-qa"),"placement")
        if not os.path.isdir(out):os.makedirs(out)
        base=winter_copy.deepcopy(store.room13)
        summary={}
        for location in R13_QA_PLACEMENT_PLACES:
            best=None
            for n in r13_qa_placement_states(base,location):
                store.room13=n
                if not r13_layout(location):continue
                try:people=list(r13_people())
                except Exception:continue
                # Busy times first, preferring those where the fixed spots (counters, stalls) are used.
                fixed=r13_layout(location).get("positions",{})
                score=len(people)+3*sum(1 for p in people if p in fixed)
                if best is None or score>best[0]:best=(score,winter_copy.deepcopy(n))
            if best is None:continue
            store.room13=best[1]
            actors=r13_stage_people(False)
            width=r13_world_width(location)
            children=[r13_world_background(location)]
            for prop,px,py in r13_world_props(False):
                children.append(Transform(prop,xpos=px,ypos=py))
            for a in actors:
                children.append(Transform(r13_staged_visible_art(a,still=True),xpos=a["x"],ypos=a["y"]))
            renpy.render_to_file(Fixed(*children,xysize=(width,720)),os.path.join(out,location+".png"),width=width,height=720)
            rows=[]
            for a in actors:
                if a.get("occlusion"):
                    # The click shape (focus mask) of a person behind furniture, to check offline
                    # that the hidden legs are not pressable.
                    rx,ry,rw,rh=a["rect"]
                    renpy.render_to_file(r13_actor_hit_mask(a),os.path.join(out,"%s-%s-hit.png"%(location,a["person"])),width=rw,height=rh)
                face=r13_actor_face(a,0)
                rows.append(dict(person=a["person"],name=R13_NAMES.get(a["person"],a["person"]),pose=a["pose"],
                    x=a["x"],y=a["y"],w=a["width"],h=a["height"],rect=list(a["rect"]),feet=r13_ma_feet(a)[1],
                    occlusion=[list(p) for p in a.get("occlusion",[])],face=[round(v,1) for v in face]))
            summary[location]=dict(day=store.room13["day"],period=store.room13["period"],
                week2=bool(store.room13.get("week2_started")),width=width,actors=rows)
            with open(os.path.join(out,location+".json"),"w") as f:
                f.write(qa_json.dumps(summary[location],ensure_ascii=False,indent=1))
        store.room13=base
        r13_qa_note("placement: %r"%({k:(v["day"],v["period"],len(v["actors"])) for k,v in summary.items()},))
        return True

testcase placement_after:
    # render_to_file draws at the window's pixel scale: use a 1:1 window.
    $ renpy.set_physical_size((1280,720))
    pause 2.0
    click "처음부터"
    pause 3.0
    run Call("r13_qa_roam",dict(day=3,period=0,location="square",life_poc=True),("entry_corrected","lodging"))
    pause 3.0
    screenshot "placement_start.png"
    assert eval r13_qa_placement_shots()
