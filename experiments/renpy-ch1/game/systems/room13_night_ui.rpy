# B notebook dialogue (2026-10-24 owner approval). Historical function names
# preserve geometry and save compatibility; controls retain their existing actions.
init 150 python:
    R13_NIGHT_UI="assets/ui-night/"
    R13_NIGHT_TEXT_COLOR="#4b3420"
    R13_NIGHT_CONTROL_Y=694          # centre line of the small text controls
    R13_NIGHT_TEXT_BOTTOM=670        # last dialogue line ends above the controls row

    def r13_night_control_y():
        return 674 if r13_touch_ui() else 684

    def r13_night_say_size():
        # The mockup's line is a step larger than the boxed window's (same size setting).
        # 2026-10-27 타이포 시안: 켜지면 display 단계. 줄 수·위치 계산이 모두 이 함수를 쓰므로 여기서 바꾼다.
        if R13_TYPE_V2:return r13_type("display")
        return 32 if r13_touch_ui() else _r13_say_size()+4

    def r13_night_say_lines(what):
        if not isinstance(what,str):return 1
        size=r13_night_say_size()
        packet=getattr(store,"r13_packet",None)
        face=None if getattr(store,"r13_thought_active",False) or "r13_visitor" in renpy.get_showing_tags() else r13_bdialogue_face(packet[0] if packet else None,r13_fullbody_emotion(getattr(store,"r13_directed_pose","neutral")))
        return max(1,_r13_say_lines(what,size,988 if face else 1090))

    def r13_night_say_top(what=None):
        """Top of the dialogue text: lines stack upward from a fixed bottom, so one line sits
        low like the mockup and two lines never reach the controls row."""
        size=r13_night_say_size()
        return (560 if r13_touch_ui() else 578)-max(0,r13_night_say_lines(what)-2)*(size+4)

    def r13_night_text_color():
        # B dialogue uses paper-role colours on the cream notebook.
        if getattr(store,"r13_thought_active",False):return r13_role_color("thought","paper")
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] is None:return r13_role_color("narration","paper")
        # 2026-10-27 타이포 시안: 말은 ink 토큰(값은 지금과 같다). 생각·서술의 역할색은 그대로 둔다.
        return r13_type_color("ink") if R13_TYPE_V2 else R13_NIGHT_TEXT_COLOR

    def r13_night_shade_alpha():
        # The approved "대사창 진하기" setting still decides how dark the shade gets.
        return {"99":.88,"d4":.985,"f5":1.0}.get(persistent.room13_window_alpha or "d4",1.0)

    def r13_night_shade_top(what=None):
        top=r13_night_say_top(what)-150
        if (persistent.room13_window_alpha or "d4") in ("f0","f5","fa","ff"):top-=60
        return max(240,top)

    def r13_night_ribbon():
        return Frame(r13_asset_path("file:"+(R13_NIGHT_UI+"name_ribbon.png")),44,0,44,0)

style r13_night_link_text is text:
    font r13_ui_font() size 20 color "#4b3420" hover_color "#b03730" insensitive_color "#8f8778"
    outlines []

screen r13_night_link(caption,glyph,icon,command,enabled=True,link_id=None):
    $ on_paper=not r13_black_card
    $ label_width=(208 if r13_touch_ui() else 184) if caption in ("건너뛰기","더보기") else (370 if r13_touch_ui() else 300)
    button:
        id (link_id or ("r13_night_"+caption))
        xsize label_width ysize (88 if r13_touch_ui() else 56) yalign .5 padding (0,0)
        background None hover_background None
        action command sensitive enabled alt caption
        fixed:
            xysize (label_width,88 if r13_touch_ui() else 56)
            if on_paper:
                add Transform(Frame(Crop((16,12,168,32),r13_asset_path("file:assets/ui-b-dialogue/b_ribbon_name.png")),16,6,32,6),xysize=(label_width,52 if r13_touch_ui() else 44),alpha=1.0 if enabled else .55) align (.5,.5)
            text caption align (.5,.5) xoffset -6 font R13_UI_BOLD_FONT size (28 if r13_touch_ui() else 24) color ("#fff6e7" if enabled else "#c0b6a5")

screen r13_night_controls(ready=True):
    $ line_active=renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_topics","r13_entry_karo_topics"))
    $ skip_action=([SetVariable("r13_carriage_skip",True),Function(renpy.end_interaction,True)] if place=="마차 안" else [SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)])
    hbox:
        xanchor 1.0 xpos (R13_CONCEPT_RIGHT-30) yanchor .5 ypos r13_night_control_y() spacing 12
        if _preferences.afm_enable and line_active:
            use r13_night_link("자동 읽기 중 · 정지","■",None,Preference("auto-forward","disable"),enabled=ready,link_id="r13_night_auto_stop")
        if line_active:
            use r13_night_link("건너뛰기","▸▸",None,skip_action,enabled=ready)
        use r13_night_link("더보기",None,"settings",Show("r13_more_tools"),enabled=ready)
