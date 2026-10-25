# Keep the seated daughter at her authored position; decisions use the empty left side.
screen r13_carriage_choice_list(entries,ready,caption=""):
    if "r13_visitor" not in renpy.get_showing_tags():
        add r13_carriage_daram_seat_art(r13_carriage_seat_shown or r13_carriage_seat(r13_current_pose)):
            xpos 850 xanchor .5 ypos 96
    use r13_notebook_choice_list(None,"neutral","선택",entries,ready,caption=caption,carriage=True)
