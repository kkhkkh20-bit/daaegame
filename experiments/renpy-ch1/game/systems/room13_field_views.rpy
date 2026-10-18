# Presentation state only: no clock, evidence or schedule changes.
default r13_field_view = "people"
default r13_field_spots = False # legacy save compatibility; markers are automatic now.
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

screen r13_field_spots_overlay(ready):
    for key,spec in ROOM13["objects"].get(room13["location"],{}).items():
        if r13_object_visible(spec):
            $ x,y,w,h=spec["rect"]
            $ selected=r13_field_selection()==key
            button:
                area (int(x+w/2)-36,int(y+h/2)-36,72,72) padding (0,0)
                background None hover_background None
                action SetVariable("r13_field_pick",(room13["location"],key)) sensitive ready
                alt (r13_object_name(key)+" 선택") tooltip r13_object_name(key)
                fixed:
                    xysize (44,44) align (.5,.5)
                    add R13InkPanel(focused=selected,alpha="e6",slim=True)
                    add R13AntiqueIcon("investigate",size=26) align (.5,.5)

screen r13_field_view_controls(ready):
    $ investigating=r13_field_view=="scene"
    use r13_footer_control(0,"사람 보기" if investigating else "주변 살피기","dialogue" if investigating else "investigate",SetVariable("r13_field_view","people" if investigating else "scene"),enabled=ready)
    if investigating:
        $ target=r13_field_selection()
        frame:
            area (28,r13_control_y()-64,944,48) padding (16,8) background R13InkPanel(alpha="e6",slim=True)
            text (r13_object_name(target) if target else "살펴볼 물건을 누르세요 · 좌우로 끌어 둘러볼 수 있어요") yalign .5 size r13_read_size(21,24) color "#fff4df" font r13_ui_font()
        use r13_footer_control(1,"살펴보기","investigate",[Function(r13_click_feedback,target),Return(("object",target))] if target else NullAction(),enabled=ready and bool(target),primary=True)
