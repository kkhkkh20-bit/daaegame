# Horizontal exploration uses one world coordinate space. UI stays outside it.
default r13_world_cameras = {}

init 58 python:
    R13_WORLD_LAYOUTS=json.load(renpy.file("assets/room13-world-layout.json")) if renpy.loadable("assets/room13-world-layout.json") else {}

    def r13_world_width(location=None):
        location=location or (store.room13 or {}).get("location")
        return int(R13_WORLD_LAYOUTS.get(location,{}).get("width",1280))

    def r13_world_height(location=None):
        return 720

    def r13_world_offset(location=None):
        location=location or (store.room13 or {}).get("location")
        initial=R13_WORLD_LAYOUTS.get(location,{}).get("initial_x",0)
        value=getattr(store,"r13_world_cameras",{}).get(location,initial)
        return int(max(0,min(r13_world_width(location)-1280,round(value/2.0)*2)))

    def r13_world_revision(location):
        return r13_hashlib.sha256(json.dumps(R13_WORLD_LAYOUTS[location],sort_keys=True).encode("utf-8")).hexdigest()

    def r13_world_scene_location(key):
        return next((location for location in R13_WORLD_LAYOUTS if R13_PLACES.get(location,(None,None))[1]==key),None)

    def r13_world_background(location=None,daylight=None):
        location=location or store.room13["location"]
        spec=R13_WORLD_LAYOUTS[location]
        period=daylight or r13_daylight()
        path=spec["files"][period]
        crop=spec.get("crops",{}).get(period)
        source=Crop(tuple(crop),path) if crop else path
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

    def r13_world_to_screen(point,location=None):
        return (point[0]-r13_world_offset(location),point[1])

init 62 python:
    # Rectangles move with the authored wider scene; object facts do not change.
    for r13_world_location,r13_world_layout in R13_WORLD_LAYOUTS.items():
        for r13_world_key,r13_world_rect in r13_world_layout.get("objects",{}).items():
            if r13_world_key not in ROOM13["objects"].get(r13_world_location,{}):
                raise ValueError("Unknown panorama object: "+r13_world_location+":"+r13_world_key)
            ROOM13["objects"][r13_world_location][r13_world_key]["rect"]=list(r13_world_rect)

screen r13_world_camera_controls(adjustment):
    # Keep the screen API for existing callers/saves. Exploration is moved by
    # the shared world viewport's mouse drag or touch swipe, with no HUD controls.
    pass
