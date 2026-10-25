# One set of cut-paper borders shared by every interactive surface.
init -80 python:
    def r13_sticker_button(primary=False,focused=False,disabled=False):
        role="surface.button."+("primary" if primary else "focused" if focused else "standard")
        surface=r13_asset(role)
        return Transform(surface,alpha=.65) if disabled else surface
