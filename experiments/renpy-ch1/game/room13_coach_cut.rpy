# Static establishing landscape approved by the owner; interior dialogue follows.
# Reuse the existing outdoor snow component; only this cut's density/speed differ.
init 302 python:
    R13_COACH_SNOW = R13FxSnow(dict(R13_DOT_FX["snow"], layers=[
        dict(count=14, vy=[12,18], sway=5),
        dict(count=8, vy=[20,28], sway=8),
    ]), (1280,720), seed=17)
    R13_COACH_SNOW.cell = 1

screen r13_coach_exterior():
    modal True
    zorder 30
    add Transform("assets/room13-opening-coach-landscape.webp", xysize=(1280,720), nearest=True)
    add Transform(R13_COACH_SNOW, alpha=.6)
    fixed:
        area (1020,r13_control_y(),232,r13_control_height())
        use r13_control("건너뛰기","skip",Return(True))
    timer 3.5 action Return(True)
    key "dismiss" action Return(True)

label r13_coach_travel_cut:
    if not renpy.is_skipping():
        window hide
        $ source_pulse(False); renpy.music.stop(channel="scene_fx"); renpy.music.stop(channel="typing")
        $ renpy.music.play("assets/bgm-travel.mp3", fadein=.6, if_changed=True)
        $ renpy.music.play("assets/ms14-audio/cart-roll-light.mp3",channel="carriage_ride",loop=True,fadein=.2,relative_volume=.2)
        $ renpy.music.play("assets/sfx-carriage-hooves.wav",channel="carriage_hooves",loop=True,fadein=.4,relative_volume=.18)
        call screen r13_coach_exterior
    return
