# Unified exploration. Legacy mode state is presentation-only; no clock, evidence or schedule changes.
default r13_field_view = "people"
default r13_field_spots = False # legacy save compatibility; no field markers.
default r13_field_pick = None
default r13_field_location = None
default r13_scene_hint_seen = ()

init 85 python:
    def r13_field_hint_state(location,wide,seen,pan_seen):
        # Preserve per-place and persistent first-wide-place discovery independently.
        return (location not in seen, bool(wide and not pan_seen))

    def r13_field_selection():
        picked=getattr(store,"r13_field_pick",None)
        if not picked or picked[0]!=store.room13["location"]:return None
        spec=ROOM13["objects"].get(picked[0],{}).get(picked[1])
        if not spec or not r13_object_visible(spec):return None
        x,y,w,h=spec["rect"]
        offset=r13_world_offset(picked[0])
        return picked[1] if x+w>offset and x<offset+1280 else None

    def r13_field_sync():
        if not getattr(store,"room13",None):return
        # Normalize old saves, including a saved same-location nearby-look view.
        store.r13_field_view="people"
        location=store.room13["location"]
        if getattr(store,"r13_field_location",None)!=location:
            store.r13_field_location=location
            store.r13_field_view="people"
            store.r13_field_pick=None
        elif store.r13_field_pick and not r13_field_selection():
            store.r13_field_pick=None

    config.interact_callbacks.append(r13_field_sync)
    config.after_load_callbacks.append(r13_field_sync)

screen r13_field_view_controls(ready):
    # Keep the legacy screen name for saved screens; no separate mode or toggle.
    $ wide=r13_world_width()>1280
    $ scene_hint,pan_hint=r13_field_hint_state(room13["location"],wide,r13_scene_hint_seen,persistent.r13_pan_hint_seen)
    if scene_hint or pan_hint:
        if scene_hint:
            timer 3.0 action SetVariable("r13_scene_hint_seen",tuple(r13_scene_hint_seen)+(room13["location"],))
        if pan_hint:
            timer 6.0 action SetField(persistent,"r13_pan_hint_seen",True)
        frame:
            area (28,656,720,48) padding (16,8) background R13InkPanel(alpha="e6",slim=True)
            text ("인물·사물을 눌러 조사 · 좌우로 끌어 이동" if wide else "인물이나 사물을 눌러 조사하세요") yalign .5 size r13_read_size(21,24) color "#fff4df" font r13_ui_font()
