# Presentation state only: no clock, evidence or schedule changes.
default r13_field_view = "people"
default r13_field_spots = False # legacy save compatibility; no field markers.
default r13_field_pick = None
default r13_field_location = None

init 85 python:
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
    $ investigating=r13_field_view=="scene"
    use r13_footer_control(0,"사람 보기" if investigating else "주변 살피기","dialogue" if investigating else "investigate",SetVariable("r13_field_view","people" if investigating else "scene"),enabled=ready)
    if investigating:
        frame:
            area (28,r13_control_y()-64,944,48) padding (16,8) background R13InkPanel(alpha="e6",slim=True)
            text "궁금한 물건을 직접 누르세요 · 좌우로 끌어 둘러볼 수 있어요" yalign .5 size r13_read_size(21,24) color "#fff4df" font r13_ui_font()
