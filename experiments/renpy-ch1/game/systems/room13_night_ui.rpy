# B notebook dialogue (2026-10-24 owner approval). Historical function names
# preserve geometry and save compatibility; controls retain their existing actions.
init 150 python:
    R13_NIGHT_UI="assets/ui-night/"
    R13_NIGHT_TEXT_COLOR="#4b3420"
    R13_NIGHT_CONTROL_Y=694          # centre line of the small text controls
    R13_NIGHT_TEXT_BOTTOM=670        # last dialogue line ends above the controls row

    def r13_night_control_y():
        return 660 if r13_touch_ui() else R13_NIGHT_CONTROL_Y

    def r13_night_say_size():
        # The mockup's line is a step larger than the boxed window's (same size setting).
        return _r13_say_size()+3

    def r13_night_say_lines(what):
        if not isinstance(what,str):return 1
        size=r13_night_say_size()
        packet=getattr(store,"r13_packet",None)
        face=None if getattr(store,"r13_thought_active",False) else r13_bdialogue_face(packet[0] if packet else None,r13_fullbody_emotion(getattr(store,"r13_directed_pose","neutral")))
        return max(1,_r13_say_lines(what,size,988 if face else 1090))

    def r13_night_say_top(what=None):
        """Top of the dialogue text: lines stack upward from a fixed bottom, so one line sits
        low like the mockup and two lines never reach the controls row."""
        size=r13_night_say_size()
        bottom=(R13_NIGHT_TEXT_BOTTOM+30 if getattr(store,"r13_field_reading",False) else (608 if r13_touch_ui() else R13_NIGHT_TEXT_BOTTOM))
        return bottom-max(2,r13_night_say_lines(what))*(size+10)  # 0.20.4 owner: one and two lines share one top

    def r13_night_text_color():
        # B dialogue uses paper-role colours on the cream notebook.
        if getattr(store,"r13_thought_active",False):return r13_role_color("thought","paper")
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] is None:return r13_role_color("narration","paper")
        return R13_NIGHT_TEXT_COLOR

    def r13_night_shade_alpha():
        # The approved "대사창 진하기" setting still decides how dark the shade gets.
        return {"99":.72,"d4":.92,"f5":1.0}.get(persistent.room13_window_alpha or "d4",1.0)

    def r13_night_shade_top(what=None):
        top=r13_night_say_top(what)-150
        if (persistent.room13_window_alpha or "d4") in ("f0","f5","fa","ff"):top-=60
        return max(240,top)

    def r13_night_ribbon():
        return Frame(R13_NIGHT_UI+"name_ribbon.png",44,0,44,0)

style r13_night_link_text is text:
    font r13_ui_font() size 20 color "#4b3420" hover_color "#b03730" insensitive_color "#8f8778"
    outlines []

screen r13_night_link(caption,glyph,icon,command,enabled=True,link_id=None):
    $ b_link_color = "#eadfc8" if r13_black_card else "#4b3420"
    # Visible as small text; the pressable area stays at the shared touch height.
    button:
        id (link_id or ("r13_night_"+caption))
        ysize (88 if r13_touch_ui() else 56) yalign .5 padding (10,0)
        background None hover_background None
        action command sensitive enabled alt caption
        hbox:
            align (.5,.5) spacing 8
            # Keep the text and more icon readable when the game canvas scales down.
            # The shared touch target and control centre stay unchanged.
            if glyph:
                text glyph style "r13_night_link_text" color b_link_color size (28 if r13_touch_ui() else 24) yalign .5
            if icon=="settings" and not r13_black_card:
                add Transform(Crop((16,20,32,24),"assets/ui-b-dialogue/b_icon_more.png"),xysize=((32,24) if r13_touch_ui() else (28,21))) yalign .5
            elif icon:
                add R13AntiqueIcon(icon,size=(26 if r13_touch_ui() else 18)) yalign .5 alpha (1.0 if enabled else .5)
            text caption style "r13_night_link_text" color b_link_color size (30 if r13_touch_ui() else 24) yalign .5

screen r13_night_controls(ready=True):
    $ line_active=renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_topics","r13_entry_karo_topics"))
    $ skip_action=([SetVariable("r13_carriage_skip",True),Function(renpy.end_interaction,True)] if place=="마차 안" else [SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)])
    hbox:
        xanchor 1.0 xpos (R13_CONCEPT_RIGHT-30) yanchor .5 ypos r13_night_control_y() spacing 0
        if _preferences.afm_enable and line_active:
            use r13_night_link("자동 읽기 중 · 정지","■",None,Preference("auto-forward","disable"),enabled=ready,link_id="r13_night_auto_stop")
            text "|" style "r13_night_link_text" color "#8f866f" yalign .5
        if line_active:
            use r13_night_link("건너뛰기","▸▸",None,skip_action,enabled=ready)
            text "|" style "r13_night_link_text" color "#8f866f" yalign .5
        use r13_night_link("더보기",None,"settings",Show("r13_more_tools"),enabled=ready)
