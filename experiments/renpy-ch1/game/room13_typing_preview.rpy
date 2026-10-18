# A silent settings-only sample. No say callbacks, history or saved preference writes.
init 71 python:
    class R13TypingPreview(renpy.Displayable):
        def __init__(self, **kwargs):
            super(R13TypingPreview, self).__init__(**kwargs)
            self.child = None
            self.signature = None
            self.started = None

        def restart(self):
            self.signature = None
            self.started = None
            renpy.redraw(self, 0)

        def render(self, width, height, st, at):
            # Picking a speed, changing font size, or resetting settings restarts
            # the sample. Ordinary hover/interaction rebuilds do not restart it.
            signature = (preferences.text_cps, _r13_say_size(), r13_ui_font())
            if signature != self.signature:
                self.signature = signature
                self.started = st
                self.child = R13DialogueText(
                    "창밖에는 눈이 내리고 있다.\n아직 확인하지 못한 이야기가 남아 있다.",
                    slow=True, slow_cps=signature[0], slow_abortable=False,
                    size=signature[1], font=signature[2], color="#efe2c2", xmaximum=860)
            # Own local clock: replay starts at zero even if the menu was open.
            rendered = renpy.render(self.child, width, height, max(0, st-self.started), at)
            result = renpy.Render(*rendered.get_size())
            result.blit(rendered, (0,0))
            return result

        def visit(self):
            return [self.child] if self.child is not None else []
