# Presentation only: read existing case state, never grant facts or move actors.
# The painted lamps/fire and all characters/UI retain their original brightness.
init 163 python:
    R13_SCENE_CONTRAST={
        "inn":dict(tint="#f5faff",saturation=.96,ambience=.65),
        "hall":dict(tint="#f7fbff",saturation=.98,ambience=.75),
        "room13":dict(tint="#f7fbff",saturation=.98,ambience=.70),
    }

    def r13_scene_contrast_key(location,period):
        state=getattr(store,"room13",None) or {}
        return "after" if location in R13_SCENE_CONTRAST and state.get("case_state")=="occurred" else None

    def r13_scene_treatment(location,period,source):
        if not r13_scene_contrast_key(location,period):return source
        profile=R13_SCENE_CONTRAST[location]
        return Transform(source,matrixcolor=TintMatrix(profile["tint"])*SaturationMatrix(profile["saturation"]))

    def r13_scene_ambience_gain(bg,mood):
        location={"front":"inn","hall":"hall","room":"room13"}.get(bg)
        if mood in ("hearing","quiet","travel") or not r13_scene_contrast_key(location,None):return 1.0
        return R13_SCENE_CONTRAST[location]["ambience"]

    _r13_contrast_scene_music=r13_sound_scene_music
    def r13_sound_scene_music(bg,title,mood):
        # Preserve authored music/ambience selection, silence and movement sounds.
        path=_r13_contrast_scene_music(bg,title,mood)
        renpy.music.set_volume(r13_scene_ambience_gain(bg,mood),delay=.6,channel="ambience")
        return path
