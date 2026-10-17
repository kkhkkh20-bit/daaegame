# Authored acting and physical staging. These are presentation choices only;
# they never change the clock, evidence, relationships, or resident schedules.
default r13_current_pose = "neutral"

init 59 python:
    R13_ACTING = json.load(renpy.file("assets/room13-pixel-acting.json")) if renpy.loadable("assets/room13-pixel-acting.json") else {}
    R13_LINE_DIRECTION = json.load(renpy.file("assets/room13-line-direction.json")) if renpy.loadable("assets/room13-line-direction.json") else {}
    R13_PORTRAITS = json.load(renpy.file("assets/room13-portraits.json")) if renpy.loadable("assets/room13-portraits.json") else {}

    def r13_portrait_pose(person,pose):
        key=pose[10:] if pose.startswith("interview_") else pose
        poses=R13_PORTRAITS.get(person,{})
        if key in poses:return key
        if key in ("joy","surprise"):return "expressive"
        if key in ("flustered","angry","anxious"):return "distressed"
        if key in ("panic","breakdown"):return "distressed"
        if "read" in key or key=="thinking":return "thinking"
        return key if key in ("neutral","distressed","expressive") else "neutral"

    def r13_close_spec(person,pose):
        return R13_PORTRAITS.get(person,{}).get(r13_portrait_pose(person,pose))

    def r13_close_geometry(person,pose):
        spec=r13_close_spec(person,pose)
        return tuple(spec["crop"][2:]) if spec else r13_actor_geometry(person,pose)

    def r13_close_head(person,pose):
        spec=r13_close_spec(person,pose)
        return spec["head"] if spec else r13_acting_head(person,pose)

    R13_WORLD_PIXEL_GRID = 2
    R13_CLOSE_PIXEL_GRID = 3

    def r13_pixel_scale(art,width,height,grid):
        width=max(1,int(round(width)));height=max(1,int(round(height)))
        if grid>1:
            # Flatten creates an actual low-resolution render texture. Merely
            # composing two scales can otherwise preserve the full-res source.
            # 0.18.93 (2x2 pixel check): the low texture is drawn back at exactly grid x its size.
            # width//grid scaled up to width made e.g. 133 cells fill 400 px, so every ~130th
            # column/row became grid+1 px wide; the box now ends on a whole cell (at most
            # grid-1 px narrower/shorter, top-left unchanged).
            lw,lh=max(1,width//grid),max(1,height//grid)
            low=Transform(art,size=(lw,lh),nearest=True,subpixel=False)
            art=Flatten(low)
            # Keep the bottom edge (feet) where it was: the trimmed rows come off the top.
            return Transform(art,size=(lw*grid,lh*grid),yoffset=height-lh*grid,nearest=True,subpixel=False,rotate_pad=False)
        return Transform(art,size=(width,height),nearest=True,subpixel=False,rotate_pad=False)

    def r13_acting_spec(person,pose):
        poses=R13_ACTING.get(person,{})
        key=pose[10:] if pose.startswith("interview_") else pose
        return poses.get(key) or (poses.get("neutral") if key in ("world","inn_activity","activity") else None)

    def r13_actor_geometry(person,pose):
        spec=r13_acting_spec(person,pose)
        if spec:return tuple(spec["crop"][2:])
        if person=="daram":return tuple(R13_PIXEL_MOTION["canvas"])
        states=CAST[person]
        return tuple(states.get(pose,states["neutral"])["crop"][2:])

    def r13_acting_head(person,pose):
        spec=r13_acting_spec(person,pose)
        if not spec:return None
        if spec.get("head"):return spec["head"]
        emotion=pose[10:] if pose.startswith("interview_") else pose
        avatar=R13_ACTING.get(person,{}).get("avatar_"+emotion)
        if avatar and avatar["file"]==spec["file"]:
            ax,ay,aw,ah=avatar["crop"];x,y,w,h=spec["crop"]
            if x<=ax and y<=ay and ax+aw<=x+w and ay+ah<=y+h:
                return [ax-x,ay-y,aw,ah]
        return None

    def r13_close_scale(person,pose,height):
        width,native_height=r13_close_geometry(person,pose)
        head=r13_close_head(person,pose)
        if (r13_close_spec(person,pose) or {}).get("full_body"):
            return (height*.38)/max(1,head[3])
        if head:
            # Different body poses retain a readable face. In particular a
            # crouched child or hanging bat must not disappear behind the UI.
            scale=(height*.30)/head[3]
            if r13_close_spec(person,pose):
                # A bust must continue under the dialogue panel or beyond the
                # viewport in topic mode; never leave its cut edge floating.
                extent=445.0 if height>=800 else 574.0
                scale=max(scale,extent/max(1,native_height-head[1]))
                scale=min(scale,(375.0 if height>=800 else 390.0)/head[3])
            return min(scale,(880.0 if height>=800 else 590.0)/width)
        if person=="daram" and not r13_acting_spec(person,pose):native_height-=20
        return float(height)/native_height

    def r13_line_performance(identity,index,packet):
        person,text=packet[:2]
        expression=R13_DIRECTION.get(identity,{}).get(person,"neutral")
        pose=expression
        cue=R13_LINE_DIRECTION.get(identity,{}).get(str(index))
        if cue and cue.get("person")==person and cue.get("text")==text:
            pose=cue["pose"]
            expression=cue.get("expression",pose if pose in ("neutral","thinking","distressed","expressive") else expression)
        if len(packet)>2:
            if isinstance(packet[2],dict):
                expression=packet[2].get("expression",expression)
                pose=packet[2].get("pose",expression)
            else:
                expression=packet[2]
                pose=expression
        if len(packet)>3:pose=packet[3]
        # A missing authored pose is an explicit neutral fallback, never an
        # activity label attached to an unrelated standing sprite.
        if person in R13_ACTING and pose not in R13_ACTING[person]:pose=expression if expression in R13_ACTING[person] else "neutral"
        # Full-body dialogue expression (room13_fullbody_dialogue.rpy): the
        # pose carries the new key; expression keeps an older key for avatars.
        emotion=r13_fullbody_line_emotion(identity,index,person,text,expression,pose)
        if emotion:
            pose=emotion
            expression=R13_FULLBODY_TO_LEGACY.get(expression,expression) if expression in R13_FULLBODY_NEW else expression
        return expression,pose

    class R13FurnitureMask(renpy.Displayable):
        size=(1280,720) # Older saves contain only the original full-screen points.
        def __init__(self,points,size=(1280,720),origin=(0,0),**kwargs):
            super(R13FurnitureMask,self).__init__(**kwargs)
            self.size=tuple(size)
            self.points=tuple((point[0]-origin[0],point[1]-origin[1]) for point in points)
        def render(self,width,height,st,at):
            result=renpy.Render(*self.size)
            result.canvas().polygon("#ffffff",self.points)
            return result

    def r13_furniture_foreground(points):
        background=R13_PLACES[store.room13["location"]][1]
        return AlphaMask(r13_background(background),R13FurnitureMask(points))

    # All anchors below were read from the adopted 1280x720 room images.
    # Floor areas avoid chairs; hand slots attach to actual writing/work tops.
    R13_STAGE_FLOORS={
        "gate":[(675,610,248),(400,597,224),(850,614,240)],
        "square":[(805,622,258),(1110,634,260),(325,622,236)],
        "inn":[(335,641,285),(135,621,270),(450,619,244)],
        "dining":[(332,511,202),(662,530,214),(886,520,202)],
        "kitchen":[(128,646,275),(796,548,244),(475,550,235)],
        "hall":[(843,586,276),(657,553,243),(1000,645,290)],
        "workshop":[(215,629,275),(473,606,255),(1058,622,270)],
        "post":[(368,645,265),(700,512,222),(1050,548,236)],
        "clinic":[(860,654,277),(1125,654,266),(415,507,235)],
        "school":[(913,642,272),(570,672,284),(604,390,190)],
        "store":[(724,601,246),(558,560,210),(899,653,278)],
        "greenhouse":[(1112,649,260),(1048,524,229),(335,434,186)],
        "facility":[(383,625,267),(770,602,238),(1111,644,250)],
        "room13":[(637,630,276),(947,620,264),(347,623,260)],
        "guestroom":[(637,630,276),(947,620,264),(347,623,260)],
        "altar":[(495,634,263),(735,603,240),(932,632,253)],
        "passage":[(525,634,260),(790,636,260),(980,637,260)],
    }
    # Dining polygon follows the foreground chair, mug handles and teapot.
    # Its residents occupy the aisle behind these objects, not the tabletop.
    R13_STAGE_COUNTERS={
        "inn":[(465,462),(1279,577),(1279,720),(465,720)],
        "workshop":[(349,497),(690,497),(820,462),(1279,479),(1279,720),(349,720)],
        "post":[(366,552),(1030,466),(1030,392),(1279,392),(1279,720),(366,720)],
        "facility":[(434,419),(1101,438),(1101,648),(434,581)],
        "kitchen":[(216,587),(767,644),(1177,575),(1177,720),(216,720)],
        "dining":[(0,456),(281,449),(316,472),(324,497),(454,480),(548,480),(548,469),(566,469),(566,450),(639,450),(639,469),(658,469),(658,483),(676,483),(676,445),(699,428),(710,407),(752,399),(783,400),(793,411),(833,415),(849,434),(855,472),(916,453),(973,454),(983,421),(997,421),(997,400),(1040,391),(1080,403),(1083,425),(1097,425),(1097,470),(1160,486),(1280,504),(1280,720),(0,720)],
        "greenhouse":[(104,520),(896,579),(995,444),(995,720),(104,720)],
    }

    # Additional occupied-room positions are explicit floor/depth slots.
    # Counter slots use standing poses behind the actual furniture mask.
    R13_STAGE_CACHE={}
    R13_CROWD_SLOTS={
        "gate":[(610,624,215,"floor"),(819,632,228,"floor"),(375,655,231,"floor"),(570,686,248,"floor"),(812,696,250,"floor"),(1040,679,240,"floor"),(126,681,221,"floor"),(440,606,196,"floor")],
        "square":[(195,540,187,"floor"),(435,525,180,"floor"),(680,523,183,"floor"),(910,542,191,"floor"),(120,651,230,"floor"),(385,674,250,"floor"),(662,661,246,"floor"),(1150,678,244,"floor"),(895,675,245,"floor")],
        # Reception visitors stay on the public left floor. Six distinct
        # slots accommodate the maximum six visitors plus the working host.
        "inn":[(78,575,212,"waiting"),(235,582,217,"waiting"),(391,590,222,"waiting"),(78,708,245,"waiting"),(248,711,248,"waiting"),(413,714,251,"waiting")],
        "workshop":[(113,645,249,"floor"),(290,650,224,"floor"),(407,648,316,"counter"),(535,647,342,"counter"),(855,657,325,"counter"),(1020,658,348,"counter"),(1171,658,309,"counter"),(203,542,185,"floor")],
        "post":[(415,660,342,"counter"),(580,646,318,"counter"),(757,632,332,"counter"),(913,628,337,"counter"),(1110,635,381,"counter"),(342,630,208,"floor"),(126,649,250,"floor")],
        "store":[(549,578,213,"floor"),(755,575,216,"floor"),(1114,646,260,"floor"),(573,679,259,"floor"),(761,691,277,"floor"),(986,660,242,"floor"),(418,642,231,"floor"),(160,702,206,"floor")],
        "school":[(368,461,211,"school_back"),(537,464,216,"school_back"),(727,472,217,"school_back"),(918,473,223,"school_back"),(145,477,220,"school_back"),(121,697,264,"school_left"),(340,691,243,"floor"),(826,685,269,"floor"),(1067,677,247,"school_right"),(1210,661,219,"school_right"),(456,568,202,"school_front"),(643,565,205,"school_front"),(836,572,203,"school_front")],
        "dining":[(332,511,202,"floor"),(662,530,214,"floor"),(886,520,202,"floor")],
        "clinic":[(865,654,274,"floor"),(1120,657,265,"floor"),(637,444,177,"floor"),(656,691,224,"floor"),(126,661,249,"floor")],
        "kitchen":[(123,654,273,"floor"),(484,580,274,"counter"),(719,586,309,"counter"),(923,575,279,"counter"),(1142,670,241,"floor")],
        "hall":[(488,526,199,"floor"),(674,569,230,"floor"),(876,617,261,"floor"),(1086,663,281,"floor"),(324,611,257,"floor")],
        "facility":[(269,618,243,"floor"),(645,658,316,"counter"),(906,671,339,"counter"),(1160,662,254,"floor")],
        "greenhouse":[(1114,652,256,"floor"),(225,601,241,"counter"),(952,552,240,"counter")],
    }
    R13_STAGE_CRITICAL={
        "gate":[(1098,357,57,50),(1048,408,133,33),(350,273,83,133)],
        "clinic":[(325,512,326,77)],"store":[(96,458,347,88)],
        "inn":[(850,431,195,57)],"workshop":[(551,491,196,44)],
    }

    R13_STAGE_POSITIONS={
        # Resident-specific work areas; each tuple is a floor contact and
        # authored display height, not an evenly spaced cast lineup.
        ("karo","gate"):(245,610,280),
        ("neoul","gate"):(788,614,280),
        ("resident_bori","gate"):(405,600,230),
        ("resident_badook","gate"):(900,617,257),
        ("resident_siluk","gate"):(634,646,255),
        ("resident_kkwak","gate"):(431,610,235),
        ("resident_lamplighter","gate"):(955,630,251),
        ("doto","square"):(1030,624,245),
        ("resident_ppul","square"):(1090,614,237),
        ("resident_seol","square"):(842,581,218),
        ("resident_piko","square"):(339,607,247),
        ("resident_bori","square"):(214,633,253),
        ("resident_somi","square"):(550,638,245),
        ("resident_kongi","square"):(795,618,230),
        ("resident_tori","inn"):(307,644,259),
        ("resident_yeoni","inn"):(152,643,275),
        ("resident_nubi","inn"):(341,642,255),
        ("resident_madam","inn"):(282,648,250),
        ("resident_owlgp","inn"):(168,634,246),
        ("nabi","dining"):(662,530,214),
        ("resident_owlgp","dining"):(332,511,202),
        ("resident_tok","dining"):(886,520,202),
        ("resident_musoe","workshop"):(202,634,283),
        ("resident_ttadak","workshop"):(473,622,250),
        ("resident_tok","workshop"):(657,572,246),
        ("resident_tori","workshop"):(212,635,278),
        ("resident_yeoni","workshop"):(479,616,257),
        ("resident_ubak","workshop"):(453,620,244),
        ("resident_lamplighter","workshop"):(213,634,266),
        ("resident_librarian","post"):(265,626,248),
        ("resident_momo","post"):(654,534,235),
        ("resident_sling","post"):(694,525,239),
        ("resident_seori","clinic"):(846,640,287),
        ("resident_ubak","clinic"):(1085,660,248),
        ("resident_piko","clinic"):(879,638,254),
        ("resident_teacher","school"):(590,700,330),
        ("resident_badook","school"):(931,622,270),
        ("resident_eunho","store"):(930,655,269),
        ("resident_mungchi","store"):(650,610,245),
        ("resident_madam","store"):(930,655,271),
        ("resident_siluk","store"):(694,639,260),
        ("resident_guseul","store"):(875,642,243),
        ("resident_nubi","store"):(916,640,277),
        ("resident_nero","store"):(674,592,230),
        ("resident_kkwak","store"):(840,625,235),
        ("mom","greenhouse"):(650,700,340),
    }
    R13_LIVING_ALLOWED={
        "resident_musoe":("workshop",),
        "resident_piko":("square",),
        "resident_siluk":("gate","store"),
        "resident_eunho":("store","inn"),
        "resident_mungchi":("store","school","clinic"),
        "resident_ubak":("clinic","workshop"),
        "resident_badook":("gate","square"),
        # 0.18.63 map actions: each drawn activity only where the script puts it.
        "resident_yeoni":("square",),
        "resident_seol":("square",),
        "resident_momo":("post",),
        # 0.18.67: 사서 선생님 standing book-paper action (owner 17:31), post only.
        "resident_librarian":("post",),
        # 0.18.79 (owner 19:16): storybook revisions chosen for these two, investigation scenes only.
        # 보리 ties firewood where the floor shows him (the school back row keeps the idle pose);
        # 네로 folds the luggage tag at the gate and the store.
        # 0.18.93 (owner 19:16/19:34): 네로 is the grey cloaked design again; his own sheet's activity
        # pose (kneeling at a bundle, taking old name tags off luggage) is reused on the lower-road
        # mornings at the river too, instead of drawing a new one.
        "resident_bori":("gate","store","square","workshop"),
        "resident_nero":("gate","store","river"),
        "resident_owlgp":("square",),
        "granny":("inn",),
    }

    def r13_living_pose(person,location,period):
        poses=R13_ACTING.get(person,{})
        if person in R13_LIVING_ALLOWED and location not in R13_LIVING_ALLOWED[person]:
            return "distressed" if store.room13["day"]>=R13_WEEK2_DAY and person=="resident_piko" else "neutral"
        # Main acting sheets explicitly contain action_1/action_2. These
        # choices follow the activity actually drawn in each reviewed cell.
        desired={
            ("granny","inn"):"world_counter_wipe",
            ("resident_tori","square"):"world_bench_left",
            ("guard","gate"):"action_1",
            ("buri","workshop"):"action_2" if period==2 else "action_1",
            ("seryeon","post"):"chair_read" if period==1 else "action_1",
            # 0.18.63: by day Karo wraps the cracked axle (room13-content activity); evening tea stays.
            ("karo","gate"):"action_2" if period==2 else ("living_axlewrap" if "living_axlewrap" in poses else "action_1"),
            ("doto","square"):"world_bulletin_back",
            ("doto","hall"):"action_2" if period==2 else "action_1",
            ("mom","greenhouse"):"action_2" if period==2 else "action_1",
            ("nabi","dining"):"action_1" if period==0 else "action_2",
            ("nabi","inn"):"action_1",
            ("nabi","school"):"action_2",
            ("neoul","gate"):"action_1",
            ("neoul","facility"):"action_2" if period==2 else "action_1",
            ("bami","hall"):"action_2" if period==2 else "action_1",
            ("bami","inn"):"action_2" if period==2 else "action_1",
        }.get((person,location))
        if desired in poses:return desired
        for key in ("living","activity"):
            if key in poses:return key
        authored_living=[key for key in poses if key.startswith("living_")]
        if authored_living:return authored_living[0]
        return "neutral"

    def r13_visible_people():
        # Schedule and custody rules remain authoritative. Everyone present is
        # physically drawn; priority only reserves the host's furniture spot.
        people=list(r13_people())
        host={"gate":"karo","inn":"granny","dining":"nabi","workshop":"buri",
            "post":"seryeon","clinic":"resident_seori","store":"resident_eunho",
            "school":"resident_teacher","greenhouse":"mom","facility":"neoul",
            "hall":"doto","square":"doto"}.get(store.room13["location"])
        return ([host]+[p for p in people if p!=host]) if host in people else people

    def r13_world_display_height(person,pose,height,layout):
        # Per-location perspective is independent of dialogue framing. Preserve
        # the established relative standing heights and the authored pose's
        # head/body ratio, instead of stretching a crouch to standing height.
        # 0.18.63: map-action art (dev/apply_map_actions.py) is drawn in its own proportions.
        # Its height is a share of the person's standing height (stature_ratio), never the
        # standing height itself for a seated or kneeling pose, and never taken from the head.
        ratio=(r13_acting_spec(person,pose) or {}).get("stature_ratio")
        if ratio is not None and not layout.get("standing_height_reference"):
            return height*ratio
        if not layout.get("standing_height_reference"):
            return height
        reference=layout["standing_height_reference"]
        stature=layout.get("standing_heights",{}).get(person,reference)/float(reference)
        pw,ph=r13_actor_geometry(person,pose)
        nw,nh=r13_actor_geometry(person,"neutral")
        head=r13_acting_head(person,pose)
        neutral_head=r13_acting_head(person,"neutral")
        pose_ratio=(ph/float(head[3]))/(nh/float(neutral_head[3])) if head and neutral_head else ph/float(nh)
        if ratio is not None:pose_ratio=ratio
        return height*stature*pose_ratio

    def r13_stage_people(entry=False):
        location=store.room13["location"]
        period=min(store.room13["period"],2)
        layout=r13_layout(location)
        world_width=int(layout.get("width",1280))
        world_height=int(layout.get("height",720))
        # Permission changes the available conversation, not who is standing
        # at this place at the same time. Entry uses the ordinary schedule too.
        people=r13_visible_people()
        # 2026-10-17: people with a fixed spot (counters, stalls) are placed first, so the free
        # floor slots chosen afterwards keep their faces clear.
        if layout.get("pinned"):
            fixed=layout["pinned"]
            people=[p for p in people if p in fixed]+[p for p in people if p not in fixed]
        state=store.room13
        cache_key=(entry,state["day"],period,location,world_width,layout.get("revision",0),tuple(people),
            tuple(sorted(state.get("flags",[]))),state.get("case_state"),
            state.get("victim_state"),state.get("granny_state"),state.get("daram_state"))
        if cache_key in R13_STAGE_CACHE:return R13_STAGE_CACHE[cache_key]
        floors=layout.get("floors") or R13_STAGE_FLOORS.get(location,R13_STAGE_FLOORS["square"])
        staged=[]
        for index,person in enumerate(people):
            pose=r13_living_pose(person,location,period)
            # The post has no free floor beyond its reserved chair. Visitors
            # listen standing behind the counter; their floor activities are
            # shown at other scheduled locations, never on this tabletop.
            # 2026-10-17: on the wide post picture 슬링 works behind the counter like 세련
            # ("staff_occlusion"); the layout names the pose drawn there.
            if location=="post" and person!="seryeon" and person not in layout.get("staff_occlusion",{}):pose="neutral"
            # This narrow aisle has no room for the portable stools authored
            # into the visitors' activity sheets. Use their standing poses;
            # Nabi carries her own tray without snapping it to painted mugs.
            if location=="dining":pose="action_2" if person=="nabi" else "neutral"
            override=layout.get("poses",{}).get(person,{})
            pose=override.get(str(period),pose) if isinstance(override,dict) else override or pose
            spec=r13_acting_spec(person,pose) or {}
            width,height=r13_actor_geometry(person,pose)
            cx,feet,display_height=floors[index%len(floors)]
            if not layout.get("ignore_legacy_positions",False):
                cx,feet,display_height=R13_STAGE_POSITIONS.get((person,location),(cx,feet,display_height))
            if not layout and location=="inn" and person!="granny" and spec.get("contact")!="hanging":cx,feet,display_height=235,640,260
            if not layout and location=="workshop" and person!="buri":cx,feet,display_height=200,637,265
            # Old 1280 backdrop positions; a wide layout supplies its own floors.
            if not layout and location=="post" and person!="seryeon":cx,feet,display_height=830,675,375
            if not layout and person=="seryeon" and location=="post" and pose=="action_2":cx,feet,display_height=670,515,247
            if person=="guard" and location=="gate":cx,feet,display_height=905,602,255
            cx,feet,display_height=layout.get("positions",{}).get(person,(cx,feet,display_height))
            contact=spec.get("contact","standing")
            # Furniture contact is used only for an actually authored hand
            # position. Self-contained stools always remain on the floor.
            work={
                ("granny","inn"):(935,463,300),
                ("buri","workshop"):(680,488,280),
                ("seryeon","post"):(927,522,330),
                ("mom","greenhouse"):(485,476,350),
                ("neoul","facility"):(792,409,330),
            }.get((person,location))
            if person=="granny" and location=="inn" and pose=="action_2":work=(1080,506,300)
            if layout:work=layout.get("work",{}).get(person)
            occlusion=[]
            scale=r13_world_display_height(person,pose,display_height,layout)/height
            foot=spec.get("foot",spec.get("anchor",{}).get("foot",[width/2.0,height]))
            x=int(cx-foot[0]*scale);y=int(feet-foot[1]*scale)
            if contact=="hanging" or (person=="bami" and not spec):
                # Feet grip an actual ceiling beam, not an invisible point
                # above the floor. Hanging artwork is never rotated upright.
                hook=spec.get("hook",spec.get("foot",[width/2.0,0]))
                tx,ty=layout.get("hooks",{}).get(person,(635,75) if location=="hall" else (514,48))
                x=int(tx-hook[0]*scale);y=int(ty-hook[1]*scale)
            if work and spec.get("hand") and contact not in ("self_seated","portable_stool","portable_crate","portable_bucket","floor_sit","ground","kneeling","squatting","crouching","background_chair"):
                tx,ty,display_height=work
                scale=float(display_height)/height
                hand=spec["hand"]
                x=int(tx-hand[0]*scale);y=int(ty-hand[1]*scale)
                if layout:occlusion=layout.get("occlusion",[])
                elif location in R13_STAGE_COUNTERS:occlusion=R13_STAGE_COUNTERS[location]
                elif location=="gate":occlusion=[(949,451),(1230,451),(1230,720),(949,720)]
            if not layout and location=="post" and person!="seryeon":occlusion=R13_STAGE_COUNTERS["post"]
            # 2026-10-17 (docs/ACTION_REQUEST_20261017.md §4): a person serving behind a counter,
            # stall or desk at their fixed spot has their own furniture outline over the legs.
            if layout and not work and person in layout.get("staff_occlusion",{}) and person in layout.get("positions",{}):
                occlusion=[tuple(point) for point in layout["staff_occlusion"][person]]
            if not layout and location=="dining":occlusion=R13_STAGE_COUNTERS["dining"]
            if person=="resident_tori" and location=="square" and contact=="background_bench":
                seat=spec["seat"]
                scale=260.0/height
                x=int(1840-seat[0]*scale);y=int(568-seat[1]*scale)
                occlusion=[]
            if not layout and person=="seryeon" and location=="post" and contact=="background_chair":
                seat=spec["seat"]
                scale=108.0/(foot[1]-seat[1])
                x=int(175-seat[0]*scale);y=int(562-seat[1]*scale)
                occlusion=[(188,408),(317,416),(324,583),(184,577)]
            rendered_width=int(width*scale);rendered_height=int(height*scale)
            left=max(0,x);top=max(0,y);right=min(world_width,x+rendered_width)
            bottom=min(world_height,y+rendered_height)
            rect=[left,top,max(1,right-left),max(1,bottom-top)]
            # Reserve furniture users and hanging actors first. Everyone else
            # can move through depth slots instead of disappearing on overlap.
            pinned=(person in layout.get("pinned",[]) or bool(work) or contact in ("hanging","background_bench","counter_front") or (person=="bami" and location!="inn") or person=="guard" or (person=="karo" and location=="gate") or location=="dining")
            original_pose=pose
            selected_slot=None
            def make_candidate(slot):
                sx,sy,sh,zone=slot
                zone_spec=layout.get("zones",{}).get(zone,{})
                cp=zone_spec.get("pose", "neutral" if zone!="floor" else original_pose)
                if location=="inn" and person=="bami":
                    cp=original_pose
                    if cp=="action_2":sh=int(sh*.80)
                cs=r13_acting_spec(person,cp) or {}
                cw,ch=r13_actor_geometry(person,cp)
                sc=r13_world_display_height(person,cp,sh,layout)/ch
                cf=cs.get("foot",cs.get("anchor",{}).get("foot",[cw/2.0,ch]))
                xx=int(sx-cf[0]*sc);yy=int(sy-cf[1]*sc)
                ww=int(cw*sc);hh=int(ch*sc)
                xx=max(5,min(world_width-5-ww,xx))
                mask=R13_STAGE_COUNTERS.get(location,[]) if zone=="counter" else []
                if not layout and zone=="school_back":mask=[(0,424),(1030,424),(1030,720),(0,720)]
                if not layout and zone=="school_front":mask=[(0,508),(918,508),(918,720),(0,720)]
                if not layout and zone=="school_left":mask=[(0,620),(220,630),(245,720),(0,720)]
                if not layout and zone=="school_right":mask=[(1020,605),(1120,548),(1280,548),(1280,720),(1020,720)]
                if layout:mask=zone_spec.get("occlusion",layout.get("occlusion",[]) if zone=="counter" else [])
                return dict(pose=cp,spec=cs,x=xx,y=yy,width=ww,height=hh,occlusion=mask,contact=cs.get("contact","standing"),slot=tuple(slot))
            def face_box(c):
                cs=c.get("spec") or r13_acting_spec(c.get("person",person),c["pose"]) or {}
                cw,ch=r13_actor_geometry(person if "person" not in c else c["person"],c["pose"])
                head=cs.get("head",[cw*.25,0,cw*.5,ch*.35])
                sc=float(c["height"])/ch
                return [c["x"]+head[0]*sc,c["y"]+head[1]*sc,head[2]*sc,head[3]*sc]
            def overlap(a,b):
                return max(0,min(a[0]+a[2],b[0]+b[2])-max(a[0],b[0]))*max(0,min(a[1]+a[3],b[1]+b[3])-max(a[1],b[1]))
            def masked(point,poly):
                if not poly:return False
                px,py=point;inside=False;j=len(poly)-1
                for i in range(len(poly)):
                    ax,ay=poly[i];bx,by=poly[j]
                    if (ay>py)!=(by>py) and px<(bx-ax)*(py-ay)/float(by-ay)+ax:inside=not inside
                    j=i
                return inside
            def samples(box):
                return [(box[0]+box[2]*fx,box[1]+box[3]*fy) for fx in (.3,.5,.7) for fy in (.3,.5,.7)]
            def visible_body_over_face(body,mask,face):
                return sum(1 for px,py in samples(face) if body[0]<=px<=body[0]+body[2] and body[1]<=py<=body[1]+body[3] and not masked((px,py),mask))
            def penalty(c):
                body=[c["x"],c["y"],c["width"],c["height"]];face=face_box(c)
                score=0.0
                if body[0]<5 or body[0]+body[2]>world_width-5:score+=50000
                if face[1]<104 or face[1]+face[3]>618:score+=50000
                score+=sum(masked(point,c["occlusion"]) for point in samples(face))*5000
                for old in staged:
                    ob=[old["x"],old["y"],old["width"],old["height"]];of=face_box(old)
                    score+=overlap(face,of)*24
                    score+=overlap(body,ob)*.08
                    # A foreground body must not swallow a background face.
                    if body[1]+body[3]>ob[1]+ob[3]:score+=visible_body_over_face(body,c["occlusion"],of)*4500
                    else:score+=visible_body_over_face(ob,old["occlusion"],face)*4500
                for target in layout.get("critical",R13_STAGE_CRITICAL.get(location,[])):
                    # Bodies behind a counter do not cover objects in front.
                    score+=visible_body_over_face(body,c["occlusion"],target)*1200
                return score
            primary=dict(pose=pose,spec=spec,x=x,y=y,width=rendered_width,height=rendered_height,occlusion=occlusion,contact=contact)
            if not pinned:
                candidates=[primary] if not layout and len(people)<=3 and location!="inn" else []
                slots=layout.get("slots") or R13_CROWD_SLOTS.get(location,[(a,b,c,"floor") for a,b,c in floors])
                # 0.18.56 (owner): when 세련 sits in the left background chair, nobody stands on
                # the left floor in front of her.
                if location=="post" and any(a["person"]=="seryeon" and a["contact"]=="background_chair" for a in staged):
                    slots=[slot for slot in slots if not (slot[3]=="floor" and slot[0]<400)]
                occupied={a.get("slot") for a in staged if a.get("slot")} if layout or location in ("store","inn") else set()
                candidates += [make_candidate(slot) for slot in slots if tuple(slot) not in occupied]
                # Dense shelter days have more occupants than ordinary days.
                # Extra depth variants keep all actual residents visible.
                if not layout and len(people)>len(slots) and location!="inn":
                    candidates += [make_candidate((a,b-35,int(c*.86),zone)) for a,b,c,zone in slots]
                elif layout.get("ignore_legacy_positions",False) and len(people)>len(slots):
                    # New panoramas retain all scheduled residents on busy days.
                    # Extra depth rows use the same reviewed floor/counter zones.
                    for depth in range(1,(len(people)+len(slots)-1)//len(slots)):
                        extras=[(a,b-35*depth,int(c*(.86**depth)),zone) for a,b,c,zone in slots]
                        candidates += [make_candidate(slot) for slot in extras if tuple(slot) not in occupied]
                chosen=min(enumerate(candidates),key=lambda item:(penalty(item[1]),item[0]))[1]
                selected_slot=chosen.get("slot")
                pose=chosen["pose"];spec=chosen["spec"];x=chosen["x"];y=chosen["y"]
                rendered_width=chosen["width"];rendered_height=chosen["height"]
                occlusion=chosen["occlusion"];contact=chosen["contact"]
                left=max(0,x);top=max(0,y);right=min(world_width,x+rendered_width);bottom=min(world_height,y+rendered_height)
                rect=[left,top,max(1,right-left),max(1,bottom-top)]
            staged.append(dict(person=person,pose=pose,x=x,y=y,width=rendered_width,height=rendered_height,
                rect=rect,depth=y+rendered_height,occlusion=occlusion,contact=contact,slot=selected_slot,
                activity=r13_calendar_activity(person) if person in R13_CALENDAR else spec.get("activity_label",spec.get("action_ko",spec.get("action",r13_activity_text(person))))))
        result=sorted(staged,key=lambda actor:actor["depth"])
        if len(R13_STAGE_CACHE)>=16:R13_STAGE_CACHE.clear()
        R13_STAGE_CACHE[cache_key]=result
        return result

    def r13_staged_art(actor,still=False):
        art=r13_art(actor["person"],actor["pose"])
        spec=r13_acting_spec(actor["person"],actor["pose"]) or {}
        if spec.get("native_detail"):
            art=Transform(art,size=(max(1,int(round(actor["width"]))),max(1,int(round(actor["height"])))),nearest=True,subpixel=False)
        else:
            art=r13_pixel_scale(art,actor["width"],actor["height"],R13_WORLD_PIXEL_GRID)
        return r13_idle_art(art,actor["person"],actor["pose"],r13_acting_spec(actor["person"],actor["pose"]),actor["width"],actor["height"],contact=actor["contact"],still=still)

    def r13_staged_visible_art(actor,still=False):
        art=r13_staged_art(actor,still)
        if actor["occlusion"]:
            mask=R13FurnitureMask(actor["occlusion"],size=(actor["width"],actor["height"]),origin=(actor["x"],actor["y"]))
            art=AlphaMask(art,mask,invert=True)
        return art

    def r13_actor_hit_mask(actor):
        # Drawing and picking share the same sprite transform, alpha and
        # furniture mask. No broad rectangular target covers transparent gaps.
        x,y,w,h=actor["rect"]
        return Crop((x-actor["x"],y-actor["y"],w,h),r13_staged_visible_art(actor,still=True))

    def r13_actor_face(actor,margin=10):
        cs=r13_acting_spec(actor["person"],actor["pose"]) or {}
        cw,ch=r13_actor_geometry(actor["person"],actor["pose"])
        head=cs.get("head",[cw*.25,0,cw*.5,ch*.35])
        sc=float(actor["height"])/ch
        return (actor["x"]+head[0]*sc-margin,actor["y"]+head[1]*sc-margin,head[2]*sc+2*margin,head[3]*sc+2*margin)

    def r13_object_mask(rect,faces):
        # Focus mask for an object button re-added above residents: opaque on
        # the object's own rectangle, transparent on every nearby face.
        ox,oy,ow,oh=rect
        holes=[(max(0,int(fx-ox)),max(0,int(fy-oy)),min(ow,int(fx+fw-ox)),min(oh,int(fy+fh-oy))) for fx,fy,fw,fh in faces]
        holes=[h for h in holes if h[0]<h[2] and h[1]<h[3]]
        xs=sorted({0,ow}|{h[0] for h in holes}|{h[2] for h in holes})
        ys=sorted({0,oh}|{h[1] for h in holes}|{h[3] for h in holes})
        cells=[]
        for x0,x1 in zip(xs,xs[1:]):
            for y0,y1 in zip(ys,ys[1:]):
                if not any(h[0]<=x0 and x1<=h[2] and h[1]<=y0 and y1<=h[3] for h in holes):
                    cells.append(Solid("#fff",xpos=x0,ypos=y0,xsize=x1-x0,ysize=y1-y0))
        return Fixed(*cells,xysize=(ow,oh))

    def r13_point_on_face(point,entry=False):
        px,py=point[0],point[1]
        return any(fx<=px<=fx+fw and fy<=py<=fy+fh for fx,fy,fw,fh in (r13_actor_face(a,0) for a in r13_stage_people(entry)))

    def r13_objects_over_actors(entry=False):
        # Bodies are drawn over furniture. Where a resident stands in front of
        # a clickable object, the object stays clickable outside their face;
        # the person is still reached by the face or the name tag.
        actors=r13_stage_people(entry)
        result=[]
        visible=[(key,spec) for key,spec in ROOM13["objects"].get(store.room13["location"],{}).items() if r13_object_visible(spec)]
        for index,(key,spec) in enumerate(visible):
            ox,oy,ow,oh=spec["rect"]
            covered=[a for a in actors if a["rect"][0]<ox+ow and ox<a["rect"][0]+a["rect"][2] and a["rect"][1]<oy+oh and oy<a["rect"][1]+a["rect"][3]]
            # 0.18.59: a large object raised above a resident must not cover a smaller
            # object drawn after it (hall rail over the towels); keep their own holes too.
            later=[tuple(other["rect"]) for _,other in visible[index+1:]]
            if covered:result.append((key,tuple(spec["rect"]),r13_object_mask(spec["rect"],[r13_actor_face(a) for a in actors]+later)))
        return result

    def r13_conversation_pose(person,pose="neutral"):
        if person=="seryeon" and store.room13["location"]=="post" and min(store.room13["period"],2)==1:
            key="chair_listen" if pose=="neutral" else "chair_read" if pose=="thinking" else pose
            if key in R13_ACTING.get(person,{}):return key
        return pose
