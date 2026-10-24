# Keep the seated daughter at her authored position; choices occupy the empty left side.
screen r13_carriage_choice_list(entries,ready,caption=""):
    $ context=r13_choice_context()
    $ row_height=88 if r13_touch_ui() else 80
    if "r13_visitor" not in renpy.get_showing_tags():
        add r13_carriage_daram_seat_art(r13_carriage_seat_shown or r13_carriage_seat(r13_current_pose)):
            xpos 850 xanchor .5 ypos 96
    if context:
        frame:
            area (36,30,600,132) padding (20,16) background R13InkPanel(alpha="e6",slim=True)
            text context[1] xsize 560 size r13_read_size(22,26) color "#fff4df" font r13_ui_font() line_spacing 3
    text (caption or "어떻게 할까?") xpos 56 ypos 180 xsize 560 size r13_read_size(24,28) color "#f6d18a" font r13_ui_font()
    vbox:
        pos (36,226) spacing 16
        for index,(label,command,was_read) in enumerate(entries):
            button:
                id ("r13_carriage_choice_"+str(index+1))
                xsize 600 yminimum row_height padding (64,16,20,16)
                background R13ReferenceChoice(False,index+1,parchment=True) hover_background R13ReferenceChoice(True,index+1,parchment=True)
                action r13_safe_question_action(command) sensitive ready
                text r13_question_caption(label,was_read,False) xsize 516 size r13_read_size(24,28) font r13_ui_font() color "#4b3420" yalign .5
    if ready:
        for index,(label,command,was_read) in enumerate(entries[:9]):
            key ("K_%d"%(index+1)) action r13_safe_question_action(command)
            key ("K_KP%d"%(index+1)) action r13_safe_question_action(command)
