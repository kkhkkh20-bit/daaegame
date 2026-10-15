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
    # 0.18.47 storybook tone: a slower, softer arrival and no hop.
    easeout .35 alpha 1.0 xoffset 0

screen r13_click_glint(point):
    zorder 90
    add R13ClickGlint() xpos point[0] ypos point[1] xanchor .5 yanchor .5 at r13_click_pulse
    timer .65 action Hide("r13_click_glint")

# 0.18.33 (owner): top right, clear of the person and the questions.
# 0.18.46 (owner): only the icon and the record's name, the frame hugging them, a little larger
# and moved in from the edge toward the person, as if held out to them. No caption.
define R13_EVIDENCE_CARD_CENTER = (1010, 112)
define R13_EVIDENCE_ICON_SIZE = 104
define R13_EVIDENCE_NAME_WIDTH = 190
define R13_EVIDENCE_CARD_PAD = 10

screen r13_evidence_card(key,caption="",conversation=False,notice=False):
    $ card_center=(120,92) if notice else R13_EVIDENCE_CARD_CENTER
    style_prefix "r13"
    frame:
        xanchor .5 xpos card_center[0] ypos card_center[1] padding (R13_EVIDENCE_CARD_PAD,8,R13_EVIDENCE_CARD_PAD,8)
        background R13ActionPanel()
        at r13_evidence_reveal
        vbox:
            spacing 3
            add Transform(r13_record_icon(key),size=(R13_EVIDENCE_ICON_SIZE,R13_EVIDENCE_ICON_SIZE),fit="contain",nearest=True) xalign .5
            text ROOM13["evidence"][key]["name"] size 20 color "#fff4df" xalign .5 text_align .5 xmaximum R13_EVIDENCE_NAME_WIDTH

screen r13_evidence_found(keys,conversation=False):
    # 0.18.48: above the desk close-up (90) and the item bag (95), which reopen right after a
    # find and used to cover the card. It has no buttons, so it never blocks input.
    zorder 98
    default item_index=0
    # Navigation and full record panes own their surface. Desk/item finds still show above the close-up.
    if not any(renpy.get_screen(name) for name in ("r13_map","r13_records","r13_learning_notes","r13_record_compare","r13_calendar","r13_work_board")):
        if r13_fx_active():
            add R13_STORYBOOK.get("card_glow", Null()) xpos 120 ypos (92+8+R13_EVIDENCE_ICON_SIZE//2+20) anchor (.5,.5) at r13_card_glow
        use r13_evidence_card(keys[item_index],conversation=conversation,notice=True)
    if item_index+1<len(keys):
        timer 2.4 action SetScreenVariable("item_index",item_index+1)
    else:
        timer 2.4 action Hide("r13_evidence_found")
