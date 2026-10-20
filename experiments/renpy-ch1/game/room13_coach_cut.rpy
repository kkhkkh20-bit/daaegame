# Short exterior establishing shot; authored interior dialogue follows unchanged.
# Coordinates follow the rural road in the supplied elevated background.
transform r13_coach_recede:
    subpixel True
    anchor (.5, .70)
    pos (185, 650)
    zoom 1.0
    linear 1.8 pos (430, 554) zoom .77
    linear 1.9 pos (690, 421) zoom .53
    linear 2.1 pos (982, 280) zoom .25

transform r13_coach_still:
    anchor (.5, .70)
    pos (690, 421)
    zoom .53

screen r13_coach_exterior():
    modal True
    zorder 30
    $ moving = persistent.room13_motion and not renpy.is_skipping()
    add Transform("assets/room13-opening-village-road.webp", xysize=(1280,720), nearest=True)
    add Transform("assets/room13-opening-coach-away.webp", xysize=(360,240), nearest=True, matrixcolor=SaturationMatrix(.82)*TintMatrix("#e4edff")) at (r13_coach_recede if moving else r13_coach_still)
    fixed:
        area (1020,r13_control_y(),232,r13_control_height())
        use r13_control("건너뛰기","skip",Return(True))
    timer 6.4 action Return(True)
    key "dismiss" action Return(True)

label r13_coach_travel_cut:
    if not renpy.is_skipping():
        window hide
        $ source_pulse(False); renpy.music.stop(channel="scene_fx"); renpy.music.stop(channel="typing")
        $ renpy.music.play("assets/bgm-travel.mp3", fadein=.6, if_changed=True)
        $ renpy.music.play("assets/ms14-audio/cart-roll-light.mp3",channel="carriage_ride",loop=True,fadein=.2,relative_volume=.2)
        call screen r13_coach_exterior
    return
