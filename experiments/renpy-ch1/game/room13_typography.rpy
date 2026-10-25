# Role tokens. Actual Pretendard Bold is used for interactive labels; body text stays legible.
init 57 python:
    # One 1280x720 grid, shared by every gameplay footer.
    R13_CONTROL = dict(width=232, gap=16, left=28, bottom=16,
        height=64, large_height=80, icon=28, icon_gap=10,
        text=22, large_text=24, alpha="e6", padding=16)
    def r13_touch_ui():
        return renpy.variant("touch") or renpy.get_physical_size()[1]<600

    def r13_control_height():
        return 88 if r13_touch_ui() else R13_CONTROL["large_height" if persistent.room13_large_text else "height"]
    def r13_control_x(column):
        return R13_CONTROL["left"]+column*(R13_CONTROL["width"]+R13_CONTROL["gap"])
    def r13_control_y():
        return 720-R13_CONTROL["bottom"]-r13_control_height()
    def r13_control_upper_y():
        return r13_control_y()-r13_control_height()-R13_CONTROL["gap"]

    def r13_field_ui_rects(offset=0):
        # Actual fixed field dock, thought fold and HUD. Shared by staging and
        # labels; touch and large-text geometry must agree with hit targets.
        h=r13_control_height()
        return [(offset+772,r13_control_y(),480,h),
                (offset+1020,r13_control_upper_y(),232,h),
                (offset+940,20,314,68),(offset+24,20,400,54),
                # 0.20.11 (owner-approved mockup 2026-10-23): the screen-edge pan arrows
                # (room13_world_camera.rpy) — a name tag never covers them.
                (offset+8,236,80,80),(offset+1192,236,80,80)]

    R13_UI_PADDING = {
        "button": (18,12), "compact": (12,8), "panel": (24,20),
        "row": (18,12), "name": (16,8),
    }
    R13_UI_COLORS = {
        "menu_text": "#fff4df", "menu_accent": "#ebcd8a",
        "menu_secondary": "#ced9d4", "menu_disabled": "#849592",
        "paper_text": "#303d38", "paper_secondary": "#536158",
        "dark_text": "#fff4df", "dark_secondary": "#ced9d4",
        "person": "#ebcd8a", "place": "#b8dbd2", "thought": "#9dc9ff",
        "evidence": "#765426", "testimony": "#365f79",
    }

init 70:
    style r13_text:
        bold False
        italic False
    style r13_button:
        padding R13_UI_PADDING["button"]
    style r13_button_text:
        font R13_UI_BOLD_FONT
        bold False
        italic False
    style r13_frame:
        padding R13_UI_PADDING["panel"]
    style r13_action_button:
        padding R13_UI_PADDING["button"]
    style r13_panel is r13_frame:
        padding R13_UI_PADDING["panel"]
    style r13_row_button is r13_button:
        padding R13_UI_PADDING["row"]
    style r13_row_button_text is r13_button_text
    style r13_compact_button is r13_action_button:
        padding R13_UI_PADDING["compact"]
    style r13_compact_button_text is r13_action_button_text:
        size 20
    style r13_title_text is r13_text:
        size 30
        color "#765426"
    style r13_secondary_text is r13_text:
        size 20
        color R13_UI_COLORS["paper_secondary"]
    style r13_secondary_dark_text is r13_secondary_text:
        color R13_UI_COLORS["dark_secondary"]
    style r13_key_text is r13_text:
        size 24
        color R13_UI_COLORS["evidence"]
    style r13_say_label:
        bold False
        italic False

# Text-only actions inherit the same centering as icon actions.
init 81:
    style r13_button_text:
        xalign .5
        yalign .5
    style r13_action_button:
        background R13ControlSurface()
        hover_background R13ControlSurface(hovered=True)
        selected_background R13ControlSurface(chosen=True)
        insensitive_background R13ControlSurface(disabled=True)
        padding (16,8)
    style r13_action_button_text:
        xalign .5
        yalign .5
        font R13_UI_BOLD_FONT
        color "#493323"
        hover_color "#793e2a"
        selected_color "#fff7e8"
        insensitive_color "#978572"
