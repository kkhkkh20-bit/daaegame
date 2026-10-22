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
        # 0.19.97 (owner 2026-10-22): "처음 마차 컷씬 빼주고 검정색에 글씨 넣어주고 대사 한 3개정도".
        # The outdoor coach cut is replaced by narration on black; the ride sounds keep playing.
        scene black with Dissolve(.8)
        $ r13_black_card=True; typing_allowed=True
        call r13_lines([(None,line) for line in R13_BLACK_CARD_LINES],"v111:opening:black")
        $ r13_black_card=False
        scene black with Dissolve(.5)
    return

default r13_black_card = False
define R13_BLACK_CARD_LINES = (
    "아내의 편지는 짧았다.",
    "아이를 데리고 와 달라는 말, 그리고 방 번호 하나.",
    "그 마을이 무엇을 태워 겨울을 나는지, 그때는 몰랐다.",
)
