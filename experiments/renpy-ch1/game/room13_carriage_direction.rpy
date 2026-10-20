# Opening direction only; the ordinary scene, dialogue and skip path remain in use.
default r13_carriage_narrow = False

init python:
    import math as r13_carriage_math

    def r13_carriage_seat_art():
        # Supplied A01_02 framing: keep the already-painted village out of view.
        seat = Transform(Crop((650, 0, 736, 780), "assets/ms14/carriage.webp"), xysize=(679,720), nearest=True)
        return Fixed(Solid("#211a18"), Transform(seat, xpos=300), xysize=(1280,720))

    def r13_carriage_finish():
        store.r13_carriage_narrow = False
        renpy.hide_screen("r13_evidence_card")
        renpy.show_layer_at([], reset=True)
        renpy.music.stop(channel="scene_fx", fadeout=.2)
        renpy.music.play("assets/ms14-audio/SFX_cart_stop.wav", channel="sound", relative_volume=.45)

    def r13_carriage_ride_motion(trans, st, at):
        enabled = persistent.room13_motion and not renpy.is_skipping()
        trans.xoffset = round(r13_carriage_math.sin(st * 2.4) * 1) if enabled else 0
        trans.yoffset = round(r13_carriage_math.sin(st * 5.2) * 2 + r13_carriage_math.sin(st * 1.7)) if enabled else 0
        return 1.0 / 30 if enabled else .2

# Overscan prevents exposed edges; the screens layer (text/buttons) stays still.
transform r13_carriage_ride:
    subpixel False
    nearest True
    zoom 1.015
    xalign .5
    yalign .5
    function r13_carriage_ride_motion

label r13_carriage_departure:
    $ r13_carriage_narrow = True
    call r13_scene("winter_carriage","마차 안","travel")
    scene expression r13_carriage_seat_art() as r13_carriage_background zorder -10
    show layer master at r13_carriage_ride
    $ renpy.music.play("assets/ms14-audio/SFX_cart_start.wav", channel="scene_fx", loop=False, relative_volume=.32)
    $ renpy.music.queue("assets/ms14-audio/SFX_cart_wood_roll_loop.wav", channel="scene_fx", loop=True, relative_volume=.32)
    $ renpy.music.play("assets/ms14-audio/SFX_cloth_rub_quiet.wav", channel="sound", relative_volume=.45)
    $ renpy.pause(.65)
    return
