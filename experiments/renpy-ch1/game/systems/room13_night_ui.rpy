# Night-ink dialogue and settings (owner 2026-10-22, Notion "UI 개선안" top mockup and the
# settings mockup: "맨위 스크린샷 예시 고대로 대화창 옵션창 만들어줘", "이것도 적용해봐 이렇게").
# Dialogue: no box. A shallow navy shade rises from the bottom edge, the speaker's name sits on a
# burgundy brush ribbon with a thin gold rule, the line is large warm-white text, and the line
# tools are small text controls at the bottom right ("▸▸ 건너뛰기 | ⚙ 더보기"). The records
# button moved into 더보기 for plain lines; question screens keep the approved dock.
# Assets: dev/make_night_ui_assets.py -> game/assets/ui-night/.
init 150 python:
    R13_NIGHT_UI="assets/ui-night/"
    R13_NIGHT_TEXT_COLOR="#f6ecd8"
    R13_NIGHT_CONTROL_Y=694          # centre line of the small text controls
    R13_NIGHT_TEXT_BOTTOM=670        # last dialogue line ends above the controls row

    def r13_night_say_size():
        # The mockup's line is a step larger than the boxed window's (same size setting).
        return _r13_say_size()+3

    def r13_night_say_lines(what):
        if not isinstance(what,str):return 1
        size=r13_night_say_size()
        return max(1,_r13_say_lines(what,size,1090))

    def r13_night_say_top(what=None):
        """Top of the dialogue text: lines stack upward from a fixed bottom, so one line sits
        low like the mockup and two lines never reach the controls row."""
        size=r13_night_say_size()
        bottom=R13_NIGHT_TEXT_BOTTOM+(30 if getattr(store,"r13_field_reading",False) else 0)
        return bottom-max(2,r13_night_say_lines(what))*(size+10)  # 0.20.4 owner: one and two lines share one top

    def r13_night_text_color():
        # Always the dark-surface roles: the night dialogue has no paper behind it, even in meetings.
        if getattr(store,"r13_thought_active",False):return r13_role_color("thought","dark")
        packet=getattr(store,"r13_packet",None)
        if packet and packet[0] is None:return r13_role_color("narration","dark")
        return R13_NIGHT_TEXT_COLOR

    def r13_night_shade_alpha():
        # The approved "대사창 진하기" setting still decides how dark the shade gets.
        return {"99":.72,"d4":1.0,"f5":1.0}.get(persistent.room13_window_alpha or "d4",1.0)

    def r13_night_shade_top(what=None):
        top=r13_night_say_top(what)-150
        if (persistent.room13_window_alpha or "d4") in ("f0","f5","fa","ff"):top-=60
        return max(240,top)

    def r13_night_ribbon():
        return Frame(R13_NIGHT_UI+"name_ribbon.png",44,0,44,0)

style r13_night_link_text is text:
    font r13_ui_font() size 20 color "#eadfc8" hover_color "#fff6e2" insensitive_color "#8f8778"
    outlines [(1,"#0b0f1e",0,0)]

screen r13_night_link(caption,glyph,icon,command,enabled=True,link_id=None):
    # Visible as small text; the pressable area stays at the shared touch height.
    button:
        id (link_id or ("r13_night_"+caption))
        ysize (80 if r13_touch_ui() else 56) yalign .5 padding (10,0)
        background None hover_background None
        action command sensitive enabled alt caption
        hbox:
            align (.5,.5) spacing 8
            # 0.20.0 (owner phone QA): on a phone the game canvas shrinks to about half, so the
            # small controls grow from 20 to 28px there (about 15pt on an iPhone in landscape).
            if glyph:
                text glyph style "r13_night_link_text" size (26 if r13_touch_ui() else 20) yalign .5
            if icon:
                add R13AntiqueIcon(icon,size=(26 if r13_touch_ui() else 18)) yalign .5 alpha (1.0 if enabled else .5)
            text caption style "r13_night_link_text" size (28 if r13_touch_ui() else 20) yalign .5

screen r13_night_controls(ready=True):
    $ line_active=renpy.get_screen("say") is not None and not any(renpy.get_screen(n) for n in ("choice","r13_topics","r13_resident_approach","r13_entry_topics","r13_entry_karo_topics"))
    $ skip_action=([SetVariable("r13_carriage_skip",True),Function(renpy.end_interaction,True)] if place=="마차 안" else [SetVariable("r13_conv_skip",True),Function(renpy.end_interaction,True)])
    hbox:
        xanchor 1.0 xpos (R13_CONCEPT_RIGHT-30) yanchor .5 ypos R13_NIGHT_CONTROL_Y spacing 0
        if _preferences.afm_enable and line_active:
            use r13_night_link("자동 읽기 중 · 정지","■",None,Preference("auto-forward","disable"),enabled=ready,link_id="r13_night_auto_stop")
            text "|" style "r13_night_link_text" color "#8f866f" yalign .5
        if line_active:
            use r13_night_link("건너뛰기","▸▸",None,skip_action,enabled=ready)
            text "|" style "r13_night_link_text" color "#8f866f" yalign .5
        use r13_night_link("더보기",None,"settings",Show("r13_more_tools"),enabled=ready)
