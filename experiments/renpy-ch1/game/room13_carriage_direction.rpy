# Opening direction only; the ordinary scene, dialogue and skip path remain in use.
default r13_carriage_narrow = False

init -4 python:
    renpy.music.register_channel("carriage_ride", mixer="sfx", loop=True, stop_on_mute=True)
    renpy.music.register_channel("carriage_hooves", mixer="sfx", loop=True, stop_on_mute=True)
    config.main_menu_stop_channels = list(dict.fromkeys(list(config.main_menu_stop_channels) + ["carriage_ride", "carriage_hooves", "scene_fx", "pulse", "typing"]))

init python:
    def r13_carriage_ride_motion(trans, st, at):
        # Old saves may still refer to the former looping transform.
        trans.xoffset = 0
        trans.yoffset = 0
        return None

    def r13_carriage_seat_art():
        # The original supplied carriage fills the game canvas from the start.
        art = Transform("assets/room13-pixel-carriage-empty-winter.webp", xysize=(1280,720), nearest=True, matrixcolor=SaturationMatrix(.78)*TintMatrix("#b0bbd1"))
        snow = AlphaMask(Transform(R13_COACH_SNOW,alpha=.45),"assets/room13-fx-carriage-window-mask.webp")
        rig = r13_light_rig("carriage", (1280,720))
        return Fixed(art, snow, *([rig] if rig else []), xysize=(1280,720))

    def r13_carriage_jolt():
        if persistent.room13_motion and not renpy.is_skipping():
            renpy.show_layer_at([r13_carriage_bump], reset=True)
            renpy.pause(.48)
            renpy.show_layer_at([], reset=True)

    def r13_carriage_finish():
        store.r13_carriage_narrow = False
        store.typing_allowed = True
        renpy.hide_screen("r13_evidence_card")
        renpy.show_layer_at([], reset=True)
        renpy.music.stop(channel="carriage_ride", fadeout=.35)
        renpy.music.stop(channel="carriage_hooves", fadeout=.35)
        renpy.music.play("assets/ms14-audio/SFX_cart_stop.wav", channel="sound", relative_volume=.14)

# Retain the old transform name for saves; new scenes never apply it.
transform r13_carriage_ride:
    xoffset 0
    yoffset 0

# A single bump before Dad's response, never a looping ride animation.
transform r13_carriage_bump:
    subpixel True
    zoom 1.06
    xalign .5
    yalign .5
    easein .07 yoffset -18 xoffset 6
    easeout .10 yoffset 12 xoffset -4
    ease .13 yoffset -5 xoffset 2
    ease .18 yoffset 0 xoffset 0

label r13_carriage_departure:
    call r13_coach_travel_cut
    $ source_pulse(False); renpy.music.stop(channel="sound"); renpy.music.stop(channel="typing"); renpy.music.stop(channel="scene_fx")
    $ r13_carriage_narrow = False
    call r13_scene("winter_carriage","마차 안","travel")
    scene expression r13_carriage_seat_art() as r13_carriage_background zorder -10
    $ renpy.show_layer_at([], reset=True)
    $ typing_allowed=False; renpy.music.stop(channel="typing")
    if renpy.music.get_playing(channel="carriage_ride") is None:
        $ renpy.music.play("assets/ms14-audio/cart-roll-light.mp3", channel="carriage_ride", loop=True, fadein=.6, relative_volume=.2)
    if renpy.music.get_playing(channel="carriage_hooves") is None:
        $ renpy.music.play("assets/sfx-carriage-hooves.wav",channel="carriage_hooves",loop=True,fadein=.4,relative_volume=.18)
    $ r13_speaker("daram","neutral")
    $ renpy.pause(.65)
    return
