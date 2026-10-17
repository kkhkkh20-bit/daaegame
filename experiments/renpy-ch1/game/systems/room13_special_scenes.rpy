# Approved 0.19.22 scene-only cuts. Never register these as neutral or world poses.
# The existing cut lifecycle keeps the composition through the whole dialogue block,
# including narration, and clears it at the block end. Saved displayables retain it.
init 162 python:
    R13_SPECIAL_SCENES = json.load(renpy.file("assets/room13-special-scenes.json"))
    _r13_regular_ep_cut_art = r13_ep_cut_art

    def r13_special_scene_art(name):
        spec = R13_SPECIAL_SCENES["scenes"][name]
        left, top, right, bottom = spec["visible_bounds"]
        width, height = right-left, bottom-top
        scale = min(900.0 / width, float(spec["cut_max_height"]) / height)
        w, h = int(round(width * scale)), int(round(height * scale))
        # Opaque copy of the current authored background covers any normal portrait
        # behind the cut; no standing duplicate appears beside the injured/group art.
        background = r13_background(store.r13_scene_bg)
        if store.r13_scene_bg == "r13_school":
            # Use the same school art, with a close camera on the clear floor.
            # The plain background deliberately excludes shelter crowd overlays.
            background = _r13_ep_art_world_background("school")
            camera_x = 650 if name == "bori_silent_single_shoe" else 900
        else:
            camera_x = 240
        background = Transform(Crop((camera_x,270,800,450),background),
            size=(1280,720),nearest=True)
        return Fixed(background,
            Transform(Crop((left,top,width,height),spec["file"]), size=(w,h), xpos=(1280-w)//2,
                ypos=spec["cut_ground_y"]-h, nearest=False), xysize=(1280,720))

    def r13_ep_cut_art(name):
        if name in R13_SPECIAL_SCENES["scenes"]:
            return r13_special_scene_art(name)
        return _r13_regular_ep_cut_art(name)
