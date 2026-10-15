# Entry-only staging. 0.18.22 (owner): Daram no longer peeks out of the booth window, where
# she was cut off; she stands in the yard as an ordinary actor (positions/poses in
# room13-world-layout.json). The old booth-window art below is kept for reference only.
init 62 python:
    def r13_daram_waiting_at_gate():
        s=store.room13 or {}
        return s.get("location")=="gate" and not r13_has("entry_corrected")

    _r13_entry_visible_people=r13_visible_people
    def r13_visible_people():
        people=_r13_entry_visible_people()
        if r13_daram_waiting_at_gate() and "daram" not in people:people=people+["daram"]
        return people

    R13_WAITING_WINDOW_RECT = (1023, 330, 90, 115)
    R13_WAITING_WINDOW_FRONT = ((1098,357,57,50), (1048,408,133,33), (990,445,250,80))

    class R13WaitingWindowOcclusion(renpy.Displayable):
        def render(self, width, height, st, at):
            x, y, w, h = R13_WAITING_WINDOW_RECT
            result = renpy.Render(w, h)
            canvas = result.canvas()
            # Reservation paper, open register, and wooden sill stay in front.
            for rx, ry, rw, rh in R13_WAITING_WINDOW_FRONT:
                canvas.rect("#ffffff", (rx-x, ry-y, rw, rh))
            return result

    def r13_waiting_window_art():
        spec = r13_close_spec("daram", "neutral")
        if not spec:
            return Null(width=90, height=115)
        sx, sy, sw, sh = spec["crop"]
        # Trim the large side tail, retaining her face, shoulders, and paws.
        trim = spec["head"][0]
        portrait = Crop((sx+trim, sy, sw-trim, sh), spec["file"])
        portrait = Transform(portrait, size=R13_WAITING_WINDOW_RECT[2:], nearest=True)
        return AlphaMask(portrait, R13WaitingWindowOcclusion(), invert=True)

screen r13_waiting_window(ready=False):
    # Retired in 0.18.22: Daram is drawn in the yard by r13_stage_people.
    if False:
        $ waiting_art = r13_waiting_window_art()
        add waiting_art:
            id "r13_daram_waiting_window_art"
            xpos R13_WAITING_WINDOW_RECT[0]
            ypos R13_WAITING_WINDOW_RECT[1]
        button:
            id "r13_daram_waiting_window_hit"
            area R13_WAITING_WINDOW_RECT
            background None
            hover_background None
            padding (0,0)
            focus_mask waiting_art
            alt "대기소 창 안의 다람이와 이야기하기"
            action Return(("person","daram"))
            sensitive ready
