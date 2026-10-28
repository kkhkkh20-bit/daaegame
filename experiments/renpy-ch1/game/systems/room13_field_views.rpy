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

    def r13_field_notebook_top():
        # Keep the paper inside the existing lower control band. Only an already
        # empty, zoomed strip may use the taller notebook from the reference.
        bottom=int(r13_world_height()*r13_field_zoom())
        return 552 if r13_world_width()>1280 and bottom<=552 else r13_control_y()-24

    def r13_field_paper(label=False,hover=False,tape=False):
        # Fixed corners and tape; only blank paper stretches.
        kind="label" if label else ("place" if tape else "paper")
        state="hover" if hover else "basic"
        return Frame(r13_asset_path("file:assets/ui-field-stickers/%s_%s.png"%(kind,state)),12,14,42 if not label else 12,12)

    def r13_field_arrow(direction,hover=False):
        return r13_asset_path("file:assets/ui-field-stickers/arrow_%s_%s.png"%(direction,"hover" if hover else "basic"))

    def r13_field_button_art(primary=False):
        return r13_sticker_button(primary=primary)

    def r13_field_icon(name):
        return r13_asset_path("file:"+("assets/ui-b-field/b_icon_%s.png"%({"record":"book","settings":"more","dialogue":"acorn"}.get(name,name))))

    def r13_field_selection():
        picked=getattr(store,"r13_field_pick",None)
        if not picked or picked[0]!=store.room13["location"]:return None
        spec=ROOM13["objects"].get(picked[0],{}).get(picked[1])
        if not spec or not r13_object_visible(spec):return None
        x,y,w,h=spec["rect"]
        offset=r13_world_offset(picked[0])
        return picked[1] if x+w>offset and x<offset+r13_view_width(picked[0]) else None

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

screen r13_field_button(caption,icon,command,enabled=True,width=232,height=None,chosen=False,control_id=None,primary=False):
    $ state_icon=Transform(Crop((16,16,32,32),r13_field_icon(icon)),zoom=30.0/32,alpha=1.0 if enabled else .5) if icon else None
    if not caption:
        # Exact square original, same existing input target and accessibility name.
        button:
            id (control_id or "r13_field_icon_control")
            xysize (width,height or r13_control_height()) padding (0,0)
            background None hover_background None insensitive_background None
            action command sensitive enabled selected chosen alt "메뉴"
            add Transform(r13_field_paper(label=True),xysize=(width,height or r13_control_height()))
            add state_icon xalign .5 yalign .5
    else:
        use r13_state_button(caption,command,width,height or r13_control_height(),family="primary" if chosen or primary else "wide_choice",chosen=chosen,enabled=enabled,icon=state_icon,text_size=r13_type("body"),control_id=control_id or ("r13_field_control_"+caption))

screen r13_field_view_controls(ready):
    # Keep the legacy screen name for saved screens; no separate mode or toggle.
    $ wide=r13_world_width()>1280
    $ scene_hint,pan_hint=r13_field_hint_state(room13["location"],wide,r13_scene_hint_seen,persistent.r13_pan_hint_seen)
    $ book_top=r13_field_notebook_top()
    if scene_hint or pan_hint:
        if scene_hint:
            timer (6.0 if room13["location"]=="gate" else 3.0) action SetVariable("r13_scene_hint_seen",tuple(r13_scene_hint_seen)+(room13["location"],))
        if pan_hint:
            timer 6.0 action SetField(persistent,"r13_pan_hint_seen",True)
        # 안내 문구는 장면을 가리지 않도록 조사 화면에서 상시 표시하지 않는다.

screen r13_field_top_button(caption,icon,command,ready=True,width=144,chosen=False):
    default over=False
    $ top_icon=Transform(Crop((16,16,32,32),r13_field_icon(icon)),zoom=24.0/32)
    button:
        xysize (width,88 if r13_touch_ui() else 64) padding (0,0)
        background None hover_background None action command sensitive ready selected chosen
        hovered SetScreenVariable("over",True) unhovered SetScreenVariable("over",False)
        fixed:
            xysize (width,64) yalign .5
            add Transform(r13_field_paper(hover=chosen or over),xysize=(width,64))
            hbox:
                xalign .5 yalign .5 spacing 7
                add top_icon yalign .5
                text caption font R13_UI_BOLD_FONT size r13_type("small") color "#29364b" yalign .5
