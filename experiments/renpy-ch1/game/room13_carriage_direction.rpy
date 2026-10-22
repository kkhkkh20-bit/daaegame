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
    # 0.19.97 (owner): the carriage dialogue has the same typing sound as every other line.
    $ typing_allowed=True
    if renpy.music.get_playing(channel="carriage_ride") is None:
        $ renpy.music.play("assets/ms14-audio/cart-roll-light.mp3", channel="carriage_ride", loop=True, fadein=.6, relative_volume=.2)
    if renpy.music.get_playing(channel="carriage_hooves") is None:
        $ renpy.music.play("assets/sfx-carriage-hooves.wav",channel="carriage_hooves",loop=True,fadein=.4,relative_volume=.18)
    $ r13_speaker("daram","neutral")
    $ renpy.pause(.65)
    return

# 0.19.98 (owner 2026-10-22: "첫 씬 다애가 마차에 서있으니 이상하고", "대사에 맞는 표정"):
# in the carriage Daram sits on the bench. Each of her lines picks a seated picture
# (art/daram-carriage-seat-20261022, drawn by Codex): an explicit "seat_<name>" pose, or the
# nearest one for the line's expression. Dad's and Karo's lines keep her as she is.
init 306 python:
    R13_CARRIAGE_SEATS=("neutral","quiz","pout","angry","secret","bravado","joy","wistful")
    R13_CARRIAGE_SEAT_OF={"neutral":"neutral","thinking":"neutral","joy":"joy","expressive":"joy","angry":"pout",
        "anxious":"wistful","distressed":"wistful","flustered":"secret","surprise":"quiz","panic":"quiz"}
    R13_CARRIAGE_SEAT_ZOOM=.62
    def r13_carriage_seat(pose):
        key=(pose or "neutral").replace("interview_","")
        if key.startswith("seat_") and key[5:] in R13_CARRIAGE_SEATS:return key[5:]
        if key=="intake21_01_bravado" or key.endswith("bravado"):return "bravado"
        return R13_CARRIAGE_SEAT_OF.get(key,"neutral")
    def r13_carriage_daram_seat_art(seat):
        return Transform("assets/room13-carriage-daram-seat-%s.webp"%seat,zoom=R13_CARRIAGE_SEAT_ZOOM)
    _r13_carriage_line_performance=r13_line_performance
    def r13_line_performance(identity,index,packet):
        # Keep an authored seated picture; the general path would fold it into "neutral".
        if store.place=="마차 안" and packet and packet[0]=="daram" and len(packet)>2 and isinstance(packet[2],dict) and str(packet[2].get("pose","")).startswith("seat_"):
            return packet[2].get("expression","neutral"),packet[2]["pose"]
        return _r13_carriage_line_performance(identity,index,packet)
    _r13_carriage_speaker=r13_speaker
    def r13_speaker(who,expression="neutral",pose=None):
        if store.place=="마차 안" and who=="daram" and not getattr(store,"r13_meeting_active",False):
            seat=r13_carriage_seat(pose or expression)
            store.dialogue_speaker=None
            store.dialogue_expression=expression if "avatar_"+str(expression) in CAST.get("daram",{}) else "neutral"
            store.r13_current_pose=pose or expression or "neutral"
            if store.r13_motion_person!="daram" or getattr(store,"r13_carriage_seat_shown",None)!=seat or "r13_visitor" not in renpy.get_showing_tags():
                renpy.show("r13_actor",what=r13_carriage_daram_seat_art(seat),tag="r13_visitor",at_list=[Transform(xanchor=.5,xpos=850,yanchor=0,ypos=96)])
                store.r13_carriage_seat_shown=seat
            store.r13_motion_person="daram"
            return
        return _r13_carriage_speaker(who,expression,pose)

default r13_carriage_seat_shown = None
