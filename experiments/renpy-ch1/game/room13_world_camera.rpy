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
        location=location or (store.room13 or {}).get("location")
        return int(r13_layout(location).get("height",720))

    # Field zoom (owner 2026-10-22, mockup D: "맵 전체가 쪼그라드는 거지 ... 같은 비율에서 넓게").
    # A wide place listed here is drawn smaller: the viewport shows 1280/zoom world pixels and
    # is scaled by zoom; the strip below holds the field controls or the dialogue. World
    # coordinates (objects, stand spots, saves) do not change. Other places stay at 1.0.
    # 0.20.3: the gate uses its taller 2560x960 art at 0.75, filling the screen (owner 2026-10-22:
    # "맵을 새로 넓게 그려서"); without that art it stays at 1.0.
    R13_FIELD_ZOOM={}
    def r13_field_zoom_init():
        if R13_WORLD_LAYOUTS.get("gate",{}).get("height")==960:R13_FIELD_ZOOM["gate"]=0.75
    def r13_field_zoom(location=None):
        location=location or (store.room13 or {}).get("location")
        if r13_world_width(location)<=1280:return 1.0
        return R13_FIELD_ZOOM.get(location,1.0)
    def r13_view_width(location=None):
        return int(round(1280.0/r13_field_zoom(location)))
    def r13_camera_range(location=None):
        return max(0,r13_world_width(location)-r13_view_width(location))

    def r13_world_offset(location=None):
        location=location or (store.room13 or {}).get("location")
        initial=r13_layout(location).get("initial_x",0)
        value=getattr(store,"r13_world_cameras",{}).get(location,initial)
        return int(max(0,min(r13_camera_range(location),round(value))))

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
        source=r13_scene_treatment(location,period,source)
        # Dot effects (room13_dot_fx.rpy) sit in the picture's own pixels, before scaling.
        source=r13_dot_fx_scene(location,period,source,path,crop)
        return Transform(source,size=(int(spec["width"]),int(spec.get("height",720))),nearest=True,subpixel=False)

    def r13_camera_background(st,at,location,daylight):
        # A period can change during a native dialogue, without calling scene.
        # Follow the current place's live clock rather than the constructor's
        # old morning value; do not change the clock or the saved camera.
        period=r13_daylight() if location==store.room13.get("location") else daylight
        z=r13_field_zoom(location)
        if z<1.0:
            # 0.20.3: dialogue over a zoomed place keeps the same framing; the say window sits in the strip.
            h=r13_world_height(location)
            view=Transform(Crop((r13_world_offset(location),0,r13_view_width(location),h),r13_world_background(location,period)),zoom=z)
            if h*z>=719:return Fixed(view,xysize=(1280,720)),None
            return Fixed(Solid("#1d1611"),view,Transform(Solid("#c9a86a88"),xsize=1280,ysize=1,ypos=int(h*z)),xysize=(1280,720)),None
        return Crop((r13_world_offset(location),0,1280,720),r13_world_background(location,period)),None

    class R13WorldCameraChanged:
        def __init__(self,location):
            self.location=location
            self.destination=None
        def __call__(self,value):
            if getattr(self,"destination",None) is not None:
                value=self.destination
            value=int(max(0,min(r13_camera_range(self.location),round(value))))
            cameras=dict(getattr(store,"r13_world_cameras",{}))
            if cameras.get(self.location)!=value:
                cameras[self.location]=value
                store.r13_world_cameras=cameras
                if getattr(store,"r13_field_pick",None):
                    store.r13_field_pick=None
                # A pan happens inside call screen, before its next checkpoint.
                # Keep the current viewport when a save resumes this interaction.
                renpy.retain_after_load()

    def r13_world_zone_offset(location):
        end=r13_camera_range(location)
        return end if r13_world_offset(location)>end/2.0 else 0

    def r13_world_adjustment(location):
        # Legacy free-pan saves settle at the nearest authored endpoint.
        value=r13_world_zone_offset(location)
        R13WorldCameraChanged(location)(value)
        return ui.adjustment(range=r13_camera_range(location),value=value,
            step=1,force_step=False,changed=R13WorldCameraChanged(location))

    def r13_pan_ease(t):
        return t*t*(3.0-2.0*t)

    def r13_pan_camera(adjustment,direction):
        hub=renpy.get_screen("r13_hub")
        if not hub or hub.scope.get("world_moving",False) or adjustment.animation_target is not None:
            return
        target=adjustment.range if direction>0 else 0
        if target==adjustment.value:return
        # Persist the destination, never a half-travelled view. This is camera
        # presentation only: no time, evidence, flags or resident schedules.
        adjustment.changed.destination=target
        adjustment.changed(target)
        if not persistent.room13_motion or renpy.is_skipping():
            adjustment.change(target)
            adjustment.changed.destination=None
        else:
            renpy.set_screen_variable("world_moving",True,screen="r13_hub")
            adjustment.animate(target-adjustment.value,.65,r13_pan_ease)
            renpy.display.interface.maximum_framerate(.75)
        renpy.restart_interaction()

    def r13_world_pan_finish(adjustment):
        if adjustment.animation_target is not None:return
        # Finish on the exact endpoint before restoring focus/click rectangles.
        target=adjustment.changed.destination
        if target is not None:adjustment.change(target)
        adjustment.changed.destination=None
        renpy.set_screen_variable("world_moving",False,screen="r13_hub")
        renpy.restart_interaction()

    def r13_world_restore_zone():
        # An adjustment's animation clock is not meaningful across save/load.
        hub=renpy.get_screen("r13_hub")
        if hub and getattr(store,"room13",None):
            location=store.room13["location"]
            value=r13_world_zone_offset(location)
            adjustment=hub.scope.get("world_adjustment")
            if adjustment is not None:
                # The viewport can retain this object across a screen rebuild.
                # Cancel it in place before releasing input; replacing scope
                # alone leaves the old viewport animation running for a frame.
                adjustment.animation_target=None
                adjustment.changed=R13WorldCameraChanged(location)
                adjustment.change(value)
            else:
                hub.scope["world_adjustment"]=r13_world_adjustment(location)
            hub.scope["world_moving"]=False
            # Old saved hub render scopes must redraw with current geometry.
            R13_STAGE_CACHE.clear()
            renpy.restart_interaction()

    def r13_world_edge_people(adjustment):
        left=[];right=[]
        value=adjustment.value
        view=r13_view_width()
        for actor in r13_stage_people():
            fx,fy,fw,fh=r13_actor_face(actor,0)
            center=fx+fw/2.0
            if center<value+30:left.append(actor["person"])
            elif center>value+view-30:right.append(actor["person"])
        return (tuple(left),tuple(right))

    def r13_world_edge_label(people):
        names=[R13_NAMES.get(p,p) for p in people]
        return "·".join(names[:2])+(" 외 %d"%(len(names)-2) if len(names)>2 else "")

    def r13_world_edge_refresh(adjustment,shown,bounds=None):
        # Polling must not rebuild the whole field every .3 seconds. Refresh
        # changed labels/limits after the pan, not in its middle.
        if adjustment.animation_target is not None:return
        limits=(adjustment.value<=4,adjustment.value>=adjustment.range-4)
        if r13_world_edge_people(adjustment)!=shown or (bounds is not None and limits!=bounds):
            renpy.restart_interaction()

    def r13_world_to_screen(point,location=None):
        z=r13_field_zoom(location)
        return (int((point[0]-r13_world_offset(location))*z),int(point[1]*z))

    def r13_screen_to_world(point,location=None):
        z=r13_field_zoom(location)
        return (point[0]/z+r13_world_offset(location),point[1]/z)

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
    config.after_load_callbacks.append(r13_world_restore_zone)

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
    # Fixed screen-edge controls; world art, actors and targets share one viewport.
    if adjustment.value>4:
        fixed:
            xpos 8 ypos 236 xysize (80,80)
            imagebutton:
                xpos 4 ypos 4
                idle r13_field_arrow("left") hover r13_field_arrow("left",True)
                action Function(r13_pan_camera,adjustment,-1)
                alt "왼쪽 구역"
    if adjustment.value<adjustment.range-4:
        fixed:
            xpos 1192 ypos 236 xysize (80,80)
            imagebutton:
                xpos 4 ypos 4
                idle r13_field_arrow("right") hover r13_field_arrow("right",True)
                action Function(r13_pan_camera,adjustment,1)
                alt "오른쪽 구역"

# Retained for existing saves.
default persistent.r13_pan_hint_seen = False
