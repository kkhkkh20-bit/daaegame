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

# 0.18.47: use the top-left notification area so travel and destination controls stay clear.
# 0.18.41 (owner): tight around the icon; the name wraps under it and the card grows to fit.
define R13_EVIDENCE_CARD_SIZE = 172
define R13_EVIDENCE_CARD_POS = (24, 92)
define R13_EVIDENCE_ICON_SIZE = 96

screen r13_evidence_card(key,caption,conversation=False):
    style_prefix "r13"
    frame:
        xpos R13_EVIDENCE_CARD_POS[0] ypos R13_EVIDENCE_CARD_POS[1] xsize R13_EVIDENCE_CARD_SIZE padding (8,8)
        background R13ActionPanel()
        at r13_evidence_reveal
        vbox:
            xfill True spacing 2
            add Transform(r13_record_icon(key),size=(R13_EVIDENCE_ICON_SIZE,R13_EVIDENCE_ICON_SIZE),fit="contain",nearest=True) xalign .5
            text caption size 15 color "#ebcd8a" xalign .5
            text ROOM13["evidence"][key]["name"] size 16 color "#fff4df" xalign .5 text_align .5 xmaximum (R13_EVIDENCE_CARD_SIZE-16)

screen r13_evidence_found(keys,conversation=False):
    zorder 85
    default item_index=0
    # Modal panes own their whole surface; notification lifetime still advances.
    if not any(renpy.get_screen(name) for name in ("r13_map","r13_records","r13_learning_notes","r13_record_compare","r13_calendar","r13_item_bag","r13_work_board")):
        # Warm light spreads behind the card, then fades (0.18.47 storybook tone; no star sparkle).
        if r13_fx_active():
            add R13_STORYBOOK.get("card_glow", Null()) xpos (R13_EVIDENCE_CARD_POS[0]+R13_EVIDENCE_CARD_SIZE//2) ypos (R13_EVIDENCE_CARD_POS[1]+8+R13_EVIDENCE_ICON_SIZE//2+20) anchor (.5,.5) at r13_card_glow
        use r13_evidence_card(keys[item_index],"새 증언 기록" if ROOM13["evidence"][keys[item_index]]["kind"]=="증언" else "새 자료 기록",conversation=conversation)
    if item_index+1<len(keys):
        timer 2.4 action SetScreenVariable("item_index",item_index+1)
    else:
        timer 2.4 action Hide("r13_evidence_found")
