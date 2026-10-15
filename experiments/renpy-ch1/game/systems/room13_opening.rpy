# 오프닝 컷씬 (0.18.39). 새 게임에서 마차 대화 앞에 한 번 나온다(약 14초).
#
#   1) 검은 화면에 눈, 아빠의 짧은 독백 두 줄
#   2) 마을 입구 오후 풍경을 옆으로 훑고, 제목 로고
#   3) 빈 마차 안(아빠 시점): 덜컹거림, 창밖으로 눈이 스쳐 지나감 → 기존 마차 대화의 "덜컹."으로 이어짐
#
# 화면 연출만 한다. 시간·증거·관계·일정·대사는 바꾸지 않는다. 아빠는 그리지 않는다.
# 클릭하면 다음 컷으로, '건너뛰기'는 컷씬만 건너뛰고 마차 대화로 간다.
# 설정의 '움직임'이 꺼져 있으면 카메라 이동·흔들림·눈 없이 같은 컷을 정지 화면으로 보여 준다.
# 화면 테스트(renpy test)와 건너뛰기 중에는 나오지 않는다(기존 테스트가 마차 대화부터 시작한다).
# 그림은 기존 원화만 쓴다: 입구 파노라마(오후), 빈 마차 안, 제목 로고. 창 영역은 room13-dot-fx.json.

init 58 python:
    R13_OPENING_SHOTS = (4.2, 5.6, 4.2)
    R13_OPENING_LINES = ("여관에서 온 편지 한 통.", "아내가 머물던 산마을로 간다.")

    def r13_opening_wanted():
        if renpy.is_skipping():
            return False
        in_test = getattr(renpy, "is_in_test", None)
        if in_test and in_test() and not getattr(store, "r13_opening_force", False):
            return False
        return True

    class R13FxDrift(R13FxClock):
        """달리는 마차 창밖의 눈: 오른쪽에서 왼쪽으로 빠르게 스치며 조금씩 떨어진다(4px 칸)."""
        def __init__(self, size, count=46, seed=5, **kwargs):
            super(R13FxDrift, self).__init__(size, **kwargs)
            spec = R13_DOT_FX.get("snow", {})
            self.images = [spec.get("small"), spec.get("big")]
            state = seed
            self.flakes = []
            for i in range(count):
                vals = []
                for _ in range(4):
                    state = (state * 16807) % 2147483647
                    vals.append(state / 2147483647.0)
                big = 1 if vals[3] < .22 else 0
                speed = (520 + 420 * vals[2]) * (1.35 if big else 1.0)
                self.flakes.append((big, vals[0] * self.size[0], vals[1] * self.size[1], speed, speed * .18))

        def visit(self):
            return [renpy.displayable(i) for i in self.images if i]

        def draw(self, out, st):
            w, h = self.size
            renders = [renpy.render(renpy.displayable(i), 8, 8, st, 0) for i in self.images]
            for big, x0, y0, vx, vy in self.flakes:
                x = (x0 - vx * st) % (w + 16) - 8
                y = (y0 + vy * st) % (h + 16) - 8
                out.blit(renders[big], (int(x) // 4 * 4, int(y) // 4 * 4))
            return 1.0 / 20.0

    def r13_opening_snow():
        spec = dict(R13_DOT_FX.get("snow", {}))
        spec["layers"] = [{"count": 90, "size": 4, "vy": [22, 34], "sway": 8},
                          {"count": 16, "size": 8, "vy": [44, 60], "sway": 14}]
        return R13FxSnow(spec, (1280, 720), seed=21)

    def r13_opening_window_snow():
        window = R13_DOT_FX.get("opening", {}).get("carriage_window")
        if not window:
            return Null()
        return AlphaMask(R13FxDrift((1280, 720)), window["mask"])

    def r13_opening_gate():
        return Transform("assets/room13-pixel-ready-gate0173-afternoon.webp", size=(1920, 720), nearest=True)

    def r13_opening_carriage():
        return Transform("assets/room13-pixel-carriage-empty-winter.webp", size=(1280, 720), nearest=True)

    def r13_opening_bump():
        if not renpy.is_skipping():
            renpy.sound.play("assets/sfx-creak.wav", channel="sound")

default r13_opening_force = False

transform r13_op_fade(t_in=.6, t_out=.5):
    on show:
        alpha 0.0
        linear t_in alpha 1.0
    on hide:
        linear t_out alpha 0.0

# 마을 입구: 오른쪽(마을 안쪽)에서 왼쪽(입구 문과 마차)으로 천천히 훑는다. 정수 픽셀 이동만.
transform r13_op_pan:
    subpixel False
    xpos -640 ypos 0
    pause .3
    ease 5.0 xpos -40

transform r13_op_pan_still:
    xpos -320 ypos 0

# 마차 덜컹: 3px 단위로 오르내리다 끝에 크게 한 번.
transform r13_op_rattle:
    subpixel False
    yoffset 0
    block:
        pause .26
        yoffset 3
        pause .09
        yoffset 0
        pause .34
        yoffset 3
        pause .07
        yoffset 0
        repeat 4
    yoffset 9
    pause .08
    yoffset -3
    pause .08
    yoffset 0

transform r13_op_still:
    yoffset 0

transform r13_op_logo:
    alpha 0.0 yoffset 6
    pause 1.4
    easeout .7 alpha 1.0 yoffset 0

transform r13_op_sub:
    alpha 0.0
    pause 2.2
    linear .6 alpha 1.0

screen r13_opening_cut():
    modal True
    zorder 160
    default shot = 0
    default line2 = False
    $ moving = bool(persistent.room13_motion)
    add Solid("#05070b")

    showif shot == 0:
        fixed at r13_op_fade(.8, .5):
            add r13_opening_snow()
            vbox:
                xalign .5 yalign .46 spacing 22
                text R13_OPENING_LINES[0]:
                    font r13_ui_font() size 30 color "#e9e2d0" xalign .5 slow_cps 14
                if line2:
                    text R13_OPENING_LINES[1]:
                        font r13_ui_font() size 30 color "#e9e2d0" xalign .5 slow_cps 14
                else:
                    null height 36
    showif shot == 1:
        fixed at r13_op_fade(.7, .6):
            add r13_opening_gate() at (r13_op_pan if moving else r13_op_pan_still)
            add r13_opening_snow()
            # 로고 뒤 어둠: 4px 줄마다 옅어지는 계단식 그림자(도트 느낌, 경계선 없음).
            for i in range(16):
                add Solid("#05070b%02x" % int(200*(1.0-i/16.0))) ypos (i*16) ysize 16
            add Transform("assets/room13-title-logo.webp", size=(400,160), nearest=True) xalign .5 ypos 34 at r13_op_logo
            text "눈에 갇힌 마을":
                font r13_ui_font() size 24 color "#f4ead2" xalign .5 ypos 196 at r13_op_sub
                outlines [(2, "#1a1410", 0, 0)]
    showif shot == 2:
        fixed at r13_op_fade(.5, .25):
            fixed at (r13_op_rattle if moving else r13_op_still):
                add r13_opening_carriage()
                add r13_opening_window_snow()

    if shot == 0:
        timer 1.9 action SetScreenVariable("line2", True)
        timer R13_OPENING_SHOTS[0] action SetScreenVariable("shot", 1)
    elif shot == 1:
        timer R13_OPENING_SHOTS[1] action SetScreenVariable("shot", 2)
    else:
        timer (R13_OPENING_SHOTS[2] - .5) action Function(r13_opening_bump)
        timer R13_OPENING_SHOTS[2] action Return(True)

    # 클릭(또는 확인 키)은 다음 컷으로. 마지막 컷에서는 마차 대화로.
    key "dismiss" action (SetScreenVariable("shot", shot + 1) if shot < 2 else Return(True))
    textbutton "건너뛰기 ›":
        style "r13_action_button"
        xpos 988 ypos 24 xsize 184 ysize 54
        text_size r13_read_size(20,24)
        action Return(False)
        tooltip "오프닝 장면을 건너뛰고 마차 이야기로 갑니다"

label r13_opening_cut:
    if not r13_opening_wanted():
        return
    window hide
    $ renpy.music.play("assets/bgm-travel.mp3", fadein=1.2, if_changed=True)
    $ renpy.music.play("assets/amb-wind.mp3", channel="ambience", fadein=1.2, if_changed=True)
    call screen r13_opening_cut
    $ persistent.room13_opening_cut_seen = True
    return
