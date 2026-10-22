# Impact direction for single lines (owner 2026-10-22: "여기요 여기! 이런 거 할 때 퍽 하는 효과음,
# 화면 흔들리는 연출 ... 역전재판에서 많이 쓰거든").
# A line opts in with "fx" (new-world rows and replace variants, game/v111/newworld/dNN.json):
#   jolt   small start: a quick 4px shake and a light hit (surprise, a sharp word)
#   shake  "퍽": a heavier hit and an 9px shake that dies out (shouting, grabbing, banging)
#   slam   strongest: desk/door slam, a confession pushed out (rare)
#   flash  realisation: a white flash and a sting, no shake (the moment a clue clicks)
# Like the Ace Attorney series the effect is short (a quarter to half a second), fires once as the
# line appears, and shakes the whole picture including the dialogue. Presentation only: no story
# state changes. The "화면 움직임" setting off keeps the sound and drops shake and flash; skipping
# plays nothing.
default r13_impact_log = []
init 345 python:
    R13_IMPACT_FX = {
        # kind: (sound file, shake amplitude px, duration s, flash alpha)
        "jolt": ("assets/sfx-present.wav", 4, .22, 0.0),
        "shake": ("assets/sfx-slam.wav", 9, .36, 0.0),
        "slam": ("assets/sfx-slam.wav", 14, .46, .22),
        "flash": ("assets/source-shock9.wav", 0, 0.0, .85),
    }

    class R13ImpactShake(object):
        """Saveable shake callback (owner QA 2026-10-22: saving right after a shaken line failed
        with "Can't get local object r13_impact_shake.<locals>.shake" — a nested function cannot be
        pickled into the layer's scene list). A store-level class instance pickles fine."""
        def __init__(self, amp, duration):
            self.amp = amp
            self.duration = duration
        def __call__(self, trans, st, at):
            if st >= self.duration:
                trans.xoffset = 0
                trans.yoffset = 0
                return None
            left = 1.0 - st / self.duration
            step = int(st * 45)
            trans.xoffset = int(round(self.amp * left * (1 if step % 2 else -1)))
            trans.yoffset = int(round(self.amp * .45 * left * (1 if (step // 2) % 2 else -1)))
            return 0

    def r13_impact_shake(amp, duration):
        return Transform(function=R13ImpactShake(amp, duration))

    def r13_impact(kind):
        spec = R13_IMPACT_FX.get(kind)
        if not spec or renpy.is_skipping() or renpy.in_rollback():
            return
        sound, amp, duration, flash = spec
        store.r13_impact_log.append(kind)
        if renpy.loadable(sound):
            renpy.music.play(sound, channel="scene_fx", loop=False)
        if not persistent.room13_motion:
            return
        if amp:
            for layer in ("master", "screens"):
                renpy.show_layer_at([r13_impact_shake(amp, duration)], layer=layer, reset=True)
        if flash:
            renpy.show_screen("r13_impact_flash", strength=flash)

    def r13_packet_impact(packet):
        options = packet[2] if len(packet) > 2 and isinstance(packet[2], dict) else {}
        return options.get("fx")

    # Fires once per line, at the same point the line's scene art is chosen (room13.rpy r13_lines).
    _r13_impact_line_art = r13_ep_line_art
    def r13_ep_line_art(packet):
        result = _r13_impact_line_art(packet)
        kind = r13_packet_impact(packet)
        if kind:
            r13_impact(kind)
        return result

transform r13_impact_flash_fade(strength=.85):
    alpha strength
    linear .22 alpha 0.0

screen r13_impact_flash(strength=.85):
    zorder 200
    add Solid("#fffaf0") at r13_impact_flash_fade(strength)
    timer .24 action Hide("r13_impact_flash")
