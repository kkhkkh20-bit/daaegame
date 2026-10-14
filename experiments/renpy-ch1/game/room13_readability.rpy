# Explicit reading preference works on desktop and web, independent of Ren'Py
# device variants. It affects presentation only, never story or text speed.
default persistent.room13_large_text = False
default persistent.room13_large_text_auto = False

# A 16:9 stage letterboxed on a phone renders 20px text at ~11 CSS px. Turn large
# text on once for small screens; the settings toggle still decides afterwards.
# Device variants are only final once the display exists, so check at interaction.
init 999 python:
    def r13_small_screen_default():
        if persistent.room13_large_text_auto:
            return
        persistent.room13_large_text_auto = True
        if renpy.variant("small"):
            persistent.room13_large_text = True
            renpy.save_persistent()
            renpy.restart_interaction()
    config.interact_callbacks.append(r13_small_screen_default)

init 58 python:
    def r13_read_size(base, large=None):
        if not persistent.room13_large_text:
            # "작게" trims about a tenth; "보통" is the authored size.
            return int(max(base-3,round(base*.9))) if persistent.room13_text_small else int(base)
        return int(large if large is not None else max(base+4,round(base*1.25)))

    def r13_read_row_height(base=76):
        return int(base+20 if persistent.room13_large_text else base)
