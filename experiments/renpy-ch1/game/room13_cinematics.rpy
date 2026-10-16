# Authored scene illustrations. These never advance time, grant evidence or
# disclose a hidden event. All shots are restricted to the father's knowledge.
default persistent.room13_cinematics_seen = []
default r13_cg_active = False

init 55 python:
    import json as r13_cinema_json
    with renpy.file("assets/room13-cinematics.json") as r13_cinema_file:
        R13_CINEMATICS = {item["id"]: item for item in r13_cinema_json.load(r13_cinema_file)["items"]}

    def r13_cinematic_art(key):
        item = R13_CINEMATICS[key]
        art = Crop(tuple(item["rect"]), item["file"])
        # Lamp flicker and outdoor snow (systems/room13_dot_fx.rpy, 0.18.37).
        art = r13_cinematic_fx(key, art, tuple(item["rect"][2:]))
        return Transform(art, xysize=(1280,720), nearest=True)

# Keep the named transform resolvable for existing saves. New scenes show
# their native pixel composition without a fractional camera zoom.
transform r13_cinematic_drift:
    subpixel False
    nearest True
    align (.5,.5)
    zoom 1.0

screen r13_cinematic_view(key):
    style_prefix "r13"
    modal True
    zorder 150
    default ready = False
    timer .45 action SetScreenVariable("ready",True)
    add r13_cinematic_art(key)
    add Solid("#111a2048") ysize 48
    add Solid("#111a2070") ypos 660 ysize 60
    text R13_CINEMATICS[key]["title"]:
        xpos 34 ypos 12 size 23 color "#fff6df"
    button:
        area (0,48,1280,612)
        background None
        action Return(True)
        sensitive ready
    textbutton "계속  ›":
        xpos 1100 ypos 673
        text_size 23 text_color "#fff6df"
        background None
        action Return(True)
        sensitive ready
    if ready:
        key "dismiss" action Return(True)

label r13_cinematic(key, leave=False):
    $ r13_cg_active = True
    $ renpy.music.stop(channel="typing")
    window hide
    hide r13_visitor
    if key in R13_ENDING_STORIES:
        call r13_ending_story(key)
        if key not in persistent.room13_cinematics_seen:
            $ persistent.room13_cinematics_seen=persistent.room13_cinematics_seen+[key]
        if leave:
            scene expression r13_ending_story_art(key,3)
            $ r13_scene_key=None
        $ r13_cg_active=leave
        return
    if key not in persistent.room13_cinematics_seen:
        $ renpy.config.skipping = None
        call screen r13_cinematic_view(key)
        $ persistent.room13_cinematics_seen = persistent.room13_cinematics_seen + [key]
    elif not (renpy.is_skipping() or r13_fast_read or r13_fast_all):
        call screen r13_cinematic_view(key)
    if leave:
        scene expression r13_cinematic_art(key) with Dissolve(.3)
        $ r13_scene_key = None
    $ r13_cg_active = leave
    return
