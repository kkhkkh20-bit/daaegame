# Feedback never awards evidence or advances narrative time.
init 69 python:
    def r13_evidence_acquired(keys):
        if keys:
            renpy.hide_screen("r13_evidence_found")
            renpy.show_screen("r13_evidence_found", keys=list(keys),conversation=r13_feedback_in_conversation())

    def r13_click_feedback(key):
        spec=ROOM13["objects"].get(store.room13["location"],{}).get(key)
        if not spec:return
        x,y,w,h=spec["rect"]
        offset=r13_world_offset()
        mx,my=renpy.get_mouse_pos()
        point=(mx,my) if x<=mx+offset<=x+w and y<=my<=y+h else (x+w//2-offset,y+h//2)
        renpy.show_screen("r13_click_glint", point=point)

    class R13ClickGlint(renpy.Displayable):
        def render(self,width,height,st,at):
            out=renpy.Render(60,60)
            c=out.canvas()
            c.lines("#f5dfa0",True,[(30,4),(56,30),(30,56),(4,30)],2)
            c.lines("#fff9de",False,[(18,30),(27,39),(42,22)],3)
            return out

transform r13_click_pulse:
    alpha 1.0 zoom .55
    easeout .2 zoom 1.05
    linear .4 alpha 0.0 zoom 1.3

transform r13_evidence_reveal:
    alpha 0.0 xoffset -14
    easeout .18 alpha 1.0 xoffset 0
    # One 4px hop after it lands (0.18.31 dot effects; still when motion is off).
    function r13_evidence_hop

screen r13_click_glint(point):
    zorder 90
    add R13ClickGlint() xpos point[0] ypos point[1] xanchor .5 yanchor .5 at r13_click_pulse
    timer .65 action Hide("r13_click_glint")

screen r13_evidence_card(key,caption,conversation=False):
    style_prefix "r13"
    frame:
        xpos 24 ypos (24 if conversation else 232) xsize 424 ysize 120 padding R13_UI_PADDING["compact"]
        background R13ActionPanel()
        at r13_evidence_reveal
        hbox:
            spacing 12
            add Transform(r13_record_icon(key),size=(84,84),fit="contain",nearest=True) yalign .5
            vbox:
                xsize 304 yalign .5 spacing 6
                text caption size 19 color "#ebcd8a"
                text ROOM13["evidence"][key]["name"] size 20 color "#fff4df" xsize 304

screen r13_evidence_found(keys,conversation=False):
    zorder 85
    default item_index=0
    use r13_evidence_card(keys[item_index],"새 증언 기록" if ROOM13["evidence"][keys[item_index]]["kind"]=="증언" else "새 자료 기록",conversation=conversation)
    # Sparkle around the icon (systems/room13_dot_fx.rpy); one run per card.
    add r13_evidence_sparkle() xpos 14 ypos ((24 if conversation else 232)-4)
    if item_index+1<len(keys):
        timer 2.4 action SetScreenVariable("item_index",item_index+1)
    else:
        timer 2.4 action Hide("r13_evidence_found")
