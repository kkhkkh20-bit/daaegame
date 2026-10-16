# Horizontal exploration uses one world coordinate space. UI stays outside it.
default r13_world_cameras = {}

init 58 python:
    R13_WORLD_LAYOUTS=json.load(renpy.file("assets/room13-world-layout.json")) if renpy.loadable("assets/room13-world-layout.json") else {}

    # 0.18.59: a layout with "periods" (wide art delivered for some daylight
    # periods only) is used only then. Other periods keep the 1280 backdrop,
    # its object rects and its staging, exactly as before.
    def r13_layout(location=None,daylight=None):
        location=location or (store.room13 or {}).get("location")
        spec=R13_WORLD_LAYOUTS.get(location)
        if not spec:return {}
        if spec.get("periods") and (daylight or r13_daylight()) not in spec["periods"]:return {}
        return spec

    def r13_world_width(location=None):
        location=location or (store.room13 or {}).get("location")
        return int(r13_layout(location).get("width",1280))

    def r13_world_height(location=None):
        return 720

    def r13_world_offset(location=None):
        location=location or (store.room13 or {}).get("location")
        initial=r13_layout(location).get("initial_x",0)
        value=getattr(store,"r13_world_cameras",{}).get(location,initial)
        return int(max(0,min(r13_world_width(location)-1280,round(value/2.0)*2)))

    def r13_world_revision(location):
        return r13_hashlib.sha256(json.dumps(R13_WORLD_LAYOUTS[location],sort_keys=True).encode("utf-8")).hexdigest()

    def r13_world_scene_location(key):
        return next((location for location in R13_WORLD_LAYOUTS if R13_PLACES.get(location,(None,None))[1]==key and r13_layout(location)),None)

    def r13_world_state(location=None):
        """Scene state for layouts drawn per case state (hall, 13호): the same rule as
        the old backgrounds, after = the case has occurred."""
        spec=R13_WORLD_LAYOUTS.get(location or (store.room13 or {}).get("location"),{})
        if "state_files" not in spec:return None
        return "after" if (store.room13 or {}).get("case_state")=="occurred" else "before"

    def r13_world_file(location,period):
        spec=R13_WORLD_LAYOUTS[location]
        state=r13_world_state(location)
        files=spec["state_files"][state] if state else spec["files"]
        return files[period]

    def r13_world_background(location=None,daylight=None):
        location=location or store.room13["location"]
        spec=R13_WORLD_LAYOUTS[location]
        period=daylight or r13_daylight()
        # 0.18.59: hall/13호 choose before/after first, then the daylight picture.
        path=r13_world_file(location,period)
        crop=spec.get("crops",{}).get(period)
        source=Crop(tuple(crop),path) if crop else path
        # Dot effects (room13_dot_fx.rpy) sit in the picture's own pixels, before scaling.
        source=r13_dot_fx_scene(location,period,source,path,crop)
        return Transform(source,size=(int(spec["width"]),720),nearest=True,subpixel=False)

    def r13_camera_background(st,at,location,daylight):
        # Re-evaluated on a new dialogue interaction, retaining the field view.
        return Crop((r13_world_offset(location),0,1280,720),r13_world_background(location,daylight)),None

    class R13WorldCameraChanged:
        def __init__(self,location):
            self.location=location
        def __call__(self,value):
            value=int(max(0,min(r13_world_width(self.location)-1280,round(value/2.0)*2)))
            cameras=dict(getattr(store,"r13_world_cameras",{}))
            if cameras.get(self.location)!=value:
                cameras[self.location]=value
                store.r13_world_cameras=cameras
                # A pan happens inside call screen, before its next checkpoint.
                # Keep the current viewport when a save resumes this interaction.
                renpy.retain_after_load()

    def r13_world_adjustment(location):
        return ui.adjustment(range=max(0,r13_world_width(location)-1280),value=r13_world_offset(location),
            step=2,force_step=True,changed=R13WorldCameraChanged(location))

    def r13_pan_camera(adjustment,direction):
        adjustment.change(max(0,min(adjustment.range,adjustment.value+direction*480)))

    def r13_world_edge_people(adjustment):
        left=[];right=[]
        value=adjustment.value
        for actor in r13_stage_people():
            fx,fy,fw,fh=r13_actor_face(actor,0)
            center=fx+fw/2.0
            if center<value+30:left.append(actor["person"])
            elif center>value+1250:right.append(actor["person"])
        return (tuple(left),tuple(right))

    def r13_world_edge_label(people):
        names=[R13_NAMES.get(p,p) for p in people]
        return "·".join(names[:2])+(" 외 %d"%(len(names)-2) if len(names)>2 else "")

    def r13_world_edge_refresh(adjustment,shown):
        if r13_world_edge_people(adjustment)!=shown:
            renpy.restart_interaction()

    def r13_world_to_screen(point,location=None):
        return (point[0]-r13_world_offset(location),point[1])

init 62 python:
    # Rectangles move with the authored wider scene; object facts do not change.
    # Period-limited layouts keep both sets and swap them in place before each
    # interaction (r13_sync_world_rects): copies made from an object (kitchen
    # rear_after) share its rect list and follow it.
    R13_PERIOD_RECTS={}
    for r13_world_location,r13_world_layout in R13_WORLD_LAYOUTS.items():
        for r13_world_key,r13_world_rect in r13_world_layout.get("objects",{}).items():
            if r13_world_key not in ROOM13["objects"].get(r13_world_location,{}):
                raise ValueError("Unknown panorama object: "+r13_world_location+":"+r13_world_key)
            if r13_world_layout.get("periods"):
                base=ROOM13["objects"][r13_world_location][r13_world_key]["rect"]
                R13_PERIOD_RECTS.setdefault(r13_world_location,{})[r13_world_key]=(list(base),list(r13_world_rect))
                continue
            ROOM13["objects"][r13_world_location][r13_world_key]["rect"]=list(r13_world_rect)

    def r13_sync_world_rects():
        if not getattr(store,"room13",None):return
        for location,rects in R13_PERIOD_RECTS.items():
            wide=bool(r13_layout(location))
            objects=ROOM13["objects"].get(location,{})
            for key,(base,authored) in rects.items():
                rect=objects[key]["rect"]
                target=authored if wide else base
                if rect!=target:rect[:]=target

    def r13_check_point(key,point):
        """Inspection tick position. On a period-limited layout the stored point may
        come from the other period's picture: use the object's current rect."""
        location,_,object_key=key.partition(":")
        if location in R13_PERIOD_RECTS and object_key in ROOM13["objects"].get(location,{}):
            x,y,w,h=ROOM13["objects"][location][object_key]["rect"]
            return (int(x+w/2),int(y+h/2))
        return point

    config.interact_callbacks.append(r13_sync_world_rects)
    config.after_load_callbacks.append(r13_sync_world_rects)

init 130 python:
    # Objects registered after init 62 (13호 desk at init 66, the mother's note at
    # init 129) take their wide-scene rect here. guestroom copied its rects at
    # init 61 and keeps the old picture.
    for r13_world_location,r13_world_layout in R13_WORLD_LAYOUTS.items():
        for r13_world_key,r13_world_rect in r13_world_layout.get("late_objects",{}).items():
            if r13_world_key not in ROOM13["objects"].get(r13_world_location,{}):
                raise ValueError("Unknown late panorama object: "+r13_world_location+":"+r13_world_key)
            if r13_world_layout.get("periods"):
                base=ROOM13["objects"][r13_world_location][r13_world_key]["rect"]
                R13_PERIOD_RECTS.setdefault(r13_world_location,{})[r13_world_key]=(list(base),list(r13_world_rect))
                continue
            ROOM13["objects"][r13_world_location][r13_world_key]["rect"]=list(r13_world_rect)

screen r13_world_camera_controls(adjustment):
    # Exploration is moved by the shared world viewport's mouse drag or touch
    # swipe. People standing outside the view are named at the screen edge;
    # the tag also pans toward them.
    $ edge=r13_world_edge_people(adjustment)
    timer .3 repeat True action Function(r13_world_edge_refresh,adjustment,edge)
    if edge[0]:
        textbutton ("‹ "+r13_world_edge_label(edge[0])):
            style "r13_action_button" xpos 8 ypos 236 padding (12,8) text_size 18
            action Function(r13_pan_camera,adjustment,-1)
    elif adjustment.value>4:
        # 0.18.70 (design review 2026-10-16, #4): a wide place with nobody off to the side
        # still shows that there is more to see; a plain arrow, no name.
        textbutton "‹":
            style "r13_action_button" xpos 8 ypos 236 padding (12,8) text_size 22
            action Function(r13_pan_camera,adjustment,-1) tooltip "옆으로 둘러보기"
    if edge[1]:
        textbutton (r13_world_edge_label(edge[1])+" ›"):
            style "r13_action_button" xpos 1272 xanchor 1.0 ypos 236 padding (12,8) text_size 18
            action Function(r13_pan_camera,adjustment,1)
    elif adjustment.value<adjustment.range-4:
        textbutton "›":
            style "r13_action_button" xpos 1272 xanchor 1.0 ypos 236 padding (12,8) text_size 22
            action Function(r13_pan_camera,adjustment,1) tooltip "옆으로 둘러보기"
    # First wide place ever: one quiet line on how to look around, for six seconds.
    if not persistent.r13_pan_hint_seen:
        timer 6.0 action SetField(persistent,"r13_pan_hint_seen",True)
        frame:
            xalign .5 ypos 640 padding (16,8) background "#000000aa"
            text "화면을 좌우로 끌면 옆을 둘러볼 수 있다" size r13_read_size(18,22) color "#f3e6c8"

# 0.18.70: the one-time "drag to look around" line on the first wide place.
default persistent.r13_pan_hint_seen = False
