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

    def r13_field_paper():
        return Frame(Crop((8,8,224,44),r13_asset_path("file:assets/ui-b-field/b_panel_small.png")),24,12,24,12)

    def r13_field_button_art(primary=False):
        return Frame(Crop((16,10,128,32),r13_asset_path("file:assets/ui-b-field/b_button_primary.png") if primary else r13_asset_path("file:assets/ui-b-field/b_button.png")),24,10,24,10)

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
            add R13ButtonStateVisual("","square_standard",width,height or r13_control_height(),chosen or primary,enabled,state_icon,22) id ((control_id or "r13_field_icon_control")+"_visual")
    else:
        use r13_state_button(caption,command,width,height or r13_control_height(),family="primary" if chosen or primary else "wide_choice",chosen=chosen,enabled=enabled,icon=state_icon,text_size=r13_read_size(22,25),control_id=control_id or ("r13_field_control_"+caption))

screen r13_field_notebook_surface():
    $ book_top=r13_field_notebook_top()
    add Transform(Frame(Crop((16,16,1168,128),r13_asset_path("file:assets/ui-b-field/b_panel_dialogue.png")),64,30,64,30),xysize=(1232,712-book_top)) xpos 24 ypos book_top
    # A permanent notebook mascot, never a substitute for the current speaker.
    add Transform(r13_asset_path("file:assets/ui-b-field/sticker_daram_delighted.png"),xysize=(72,72)) xpos 76 ypos (book_top+10)

screen r13_field_view_controls(ready):
    # Keep the legacy screen name for saved screens; no separate mode or toggle.
    $ wide=r13_world_width()>1280
    $ scene_hint,pan_hint=r13_field_hint_state(room13["location"],wide,r13_scene_hint_seen,persistent.r13_pan_hint_seen)
    $ book_top=r13_field_notebook_top()
    hbox:
        xpos 178 ypos (book_top+8) spacing 4
        add Transform(Crop((16,16,32,32),r13_asset_path("file:assets/ui-b-field/b_icon_acorn.png")),xysize=(30,30)) yalign .5
        text "조사" size r13_read_size(24,27) color "#4b3021" font R13_UI_BOLD_FONT yalign .5
    if scene_hint or pan_hint:
        if scene_hint:
            timer (6.0 if room13["location"]=="gate" else 3.0) action SetVariable("r13_scene_hint_seen",tuple(r13_scene_hint_seen)+(room13["location"],))
        if pan_hint:
            timer 6.0 action SetField(persistent,"r13_pan_hint_seen",True)
        frame:
            area (190,book_top+42,536,44) padding (0,0) background None
            text ("인물과 놓인 물건·붙은 글을 눌러 살펴보세요." if room13["location"]=="gate" and scene_hint else ("인물·사물을 눌러 조사 · 좌우 끝 화살표로 이동" if wide else "인물이나 사물을 눌러 조사하세요")) size r13_read_size(20,23) color "#6a4d37" font r13_ui_font() xsize 536
