# 오프닝 컷씬 (0.18.39, 0.18.41 다시 디자인, 0.18.47 그림책 톤으로 정리: 튀는 동작·반짝임·검은 띠·핀 대신
# 천천히 스며드는 등장, 크림색 점선, 그림책 테두리). 새 게임에서 마차 대화 앞에 한 번 나온다(약 17초).
#
#   1) 편지: 어둠 속에 초대 편지가 툭 떨어져 반짝이고, 아빠의 독백 두 줄
#   2) 지도: 그림책 테두리 속에서 마을 지도를 내려다보며 마을 밖에서 입구까지 점선이 이어지고
#      '마을 입구' 이름이 스며든다
#   3) 제목: 마을 입구 오후 풍경을 옆으로 훑고, 제목 로고
#   4) 빈 마차 안(아빠 시점): 덜컹거림, 창밖으로 눈이 스쳐 지나감, 띠가 걷히며 기존 마차 대화의 "덜컹."으로 이어짐
#
# 화면 연출만 한다. 시간·증거·관계·일정·대사는 바꾸지 않는다. 아빠는 그리지 않는다.
# 클릭하면 다음 컷으로, '건너뛰기'는 컷씬만 건너뛰고 마차 대화로 간다.
# 설정의 '움직임'이 꺼져 있으면 카메라 이동·흔들림·눈 없이 같은 컷을 정지 화면으로 보여 준다.
# 화면 테스트(renpy test)와 건너뛰기 중에는 나오지 않는다(기존 테스트가 마차 대화부터 시작한다).
# 그림은 기존 원화만 쓴다: 편지 아이콘(E01), 마을 지도 v5, 입구 파노라마(오후), 빈 마차 안, 제목 로고.
# 창 영역은 room13-dot-fx.json. 지도는 원본 1:1 픽셀로 움직인다(확대·축소 없음).

init 58 python:
    R13_OPENING_SHOTS = (4.2, 5.0, 4.4, 3.6)
    # 지도 v5 원본(1672x941) 좌표: 마을 밖 오른쪽 아래에서 다리 옆 입구까지.
    R13_OPENING_ROUTE = ((1676, 852), (1540, 842), (1400, 832), (1260, 820), (1120, 806), (974, 790))
    R13_OPENING_LINES = ("아내에게서 온 편지 한 통.", "아내가 기다리는 산마을로 간다.")

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

    class R13FxRoute(renpy.Displayable):
        """점선 경로가 t0초부터 dur초 동안 한 점씩 이어진다(4px 금색 점, 12px 간격, 어두운 테두리)."""
        def __init__(self, points, t0, dur, size, **kwargs):
            super(R13FxRoute, self).__init__(**kwargs)
            self.size = size
            self.t0, self.dur = float(t0), float(dur)
            dots = []
            for (x0, y0), (x1, y1) in zip(points, points[1:]):
                length = ((x1 - x0) ** 2 + (y1 - y0) ** 2) ** .5
                n = max(1, int(length // 12))
                for i in range(n):
                    u = i / float(n)
                    dots.append((int(x0 + (x1 - x0) * u) // 4 * 4, int(y0 + (y1 - y0) * u) // 4 * 4))
            self.dots = dots

        def render(self, width, height, st, at):
            out = renpy.Render(*self.size)
            moving = bool(persistent.room13_motion)
            shown = len(self.dots) if not moving else int(len(self.dots) * min(1.0, max(0.0, (st - self.t0) / self.dur)))
            canvas = out.canvas() if shown else None
            # 0.18.47: 연필로 그은 듯한 크림색 점선(테두리 없음).
            for i, (x, y) in enumerate(self.dots[:shown]):
                if i % 2 == 0:
                    canvas.rect((250, 236, 205, 235), (x, y, 8, 4))
            if moving and shown < len(self.dots):
                renpy.redraw(self, .03)
            return out

    def r13_opening_letter():
        return Transform(r13_record_icon("E01"), size=(224, 224), fit="contain", nearest=True)

    def r13_opening_map():
        return "assets/room13-worldmap-v5.webp"

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

# 편지: 위에서 떨어져 3px 단위로 통통.
transform r13_op_letter_drop:
    subpixel False
    alpha 0.0 yoffset -48
    pause .2
    alpha 1.0
    yoffset -36
    pause .05
    yoffset -24
    pause .05
    yoffset -12
    pause .05
    yoffset 0
    pause .07
    yoffset -9
    pause .07
    yoffset 0
    pause .06
    yoffset -3
    pause .06
    yoffset 0

transform r13_op_letter_still:
    alpha 1.0 yoffset 0

# 0.18.47: 편지는 위에서 천천히 내려앉으며 나타난다(튀지 않는다).
transform r13_op_letter_float:
    subpixel True
    alpha 0.0 yoffset -18
    pause .2
    ease 1.4 alpha 1.0 yoffset 0

# t초 뒤 dur초 동안 은은하게 나타나며 살짝 떠오른다(최대 투명도 a).
transform r13_op_soft_in(t=0.0, dur=1.0, a=1.0):
    subpixel True
    alpha 0.0 yoffset 6
    pause t
    ease dur alpha a yoffset 0

transform r13_op_delay(t=1.0):
    alpha 0.0
    pause t
    alpha 1.0

# 지도: 산 쪽에서 마을 입구 쪽으로 내려다본다(원본 1:1 픽셀, 정수 이동).
transform r13_op_map_tilt:
    subpixel False
    xpos -300 ypos 0
    pause .2
    ease 3.0 xpos -334 ypos -221

transform r13_op_map_still:
    xpos -334 ypos -221

# 입구 핀: 점선이 다 이어진 뒤 위에서 꽂힌다.
transform r13_op_pin(t=3.4):
    subpixel False
    alpha 0.0 yoffset -24
    pause t
    alpha 1.0
    yoffset -12
    pause .05
    yoffset 0
    pause .06
    yoffset -6
    pause .06
    yoffset 0

# 위아래 검은 띠.
transform r13_op_bar_top:
    on show:
        ypos -60
        easeout .4 ypos 0
    on hide:
        easein .35 ypos -60

transform r13_op_bar_bottom:
    on show:
        ypos 720
        easeout .4 ypos 660
    on hide:
        easein .35 ypos 720

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
        fixed at r13_op_fade(.6, .45):
            add r13_opening_snow()
            # 0.18.47 그림책 톤: 편지가 따뜻한 빛 속에서 천천히 내려앉고, 글은 한 줄씩 스며든다.
            add R13_STORYBOOK.get("card_glow", Null()) xalign .5 ypos 82 at r13_op_soft_in(.2, 1.6, .5)
            add r13_opening_letter() xalign .5 ypos 150 at (r13_op_letter_float if moving else r13_op_letter_still)
            text ROOM13["evidence"]["E01"]["name"]:
                font r13_ui_font() size 20 color "#c9a560" xalign .5 ypos 112 at r13_op_soft_in(1.0, 1.0)
            vbox:
                xalign .5 ypos 430 spacing 20
                text R13_OPENING_LINES[0]:
                    font r13_ui_font() size 30 color "#e9e2d0" xalign .5 at r13_op_soft_in(.9, 1.2)
                text R13_OPENING_LINES[1]:
                    font r13_ui_font() size 30 color "#e9e2d0" xalign .5 at r13_op_soft_in(2.1, 1.2)
    showif shot == 1:
        fixed at r13_op_fade(.6, .5):
            fixed at (r13_op_map_tilt if moving else r13_op_map_still):
                xysize (1672, 941)
                add r13_opening_map()
                add R13FxRoute(R13_OPENING_ROUTE, 1.0, 2.4, (1672, 941))
                frame:
                    xpos (R13_OPENING_ROUTE[-1][0]-60) ypos (R13_OPENING_ROUTE[-1][1]-70)
                    padding (14,6) background R13InkPanel()
                    at r13_op_soft_in(3.3 if moving else 0.0, .9)
                    text R13_MAP_LABELS["gate"] font r13_ui_font() size 26 color "#fff3d5"
            add r13_opening_snow()
    showif shot == 2:
        fixed at r13_op_fade(.6, .6):
            add r13_opening_gate() at (r13_op_pan if moving else r13_op_pan_still)
            add r13_opening_snow()
            # 로고 뒤 어둠: 위에서부터 부드럽게 옅어진다.
            for i in range(64):
                add Solid("#140e0a%02x" % int(190*(1.0-i/64.0)**1.4)) ypos (i*4) ysize 4
            add Transform("assets/room13-title-logo.webp", xysize=(400,160), fit="contain", nearest=True) xalign .5 ypos 64 at r13_op_logo
            text "눈에 갇힌 마을":
                font r13_ui_font() size 24 color "#f4ead2" xalign .5 ypos 226 at r13_op_sub
                outlines [(2, "#1a1410", 0, 0)]
    showif shot == 3:
        fixed at r13_op_fade(.5, .25):
            fixed at (r13_op_rattle if moving else r13_op_still):
                add r13_opening_carriage()
                add r13_opening_window_snow()
    # 그림책 장면 테두리(지도·제목 컷): 가장자리가 따뜻한 어둠으로 스며든다. 마차 컷에서 걷힌다.
    showif shot in (1, 2):
        add R13_STORYBOOK.get("frame", Null()) at r13_op_fade(.9, .8)

    if shot == 0:
        timer R13_OPENING_SHOTS[0] action SetScreenVariable("shot", 1)
    elif shot == 1:
        timer R13_OPENING_SHOTS[1] action SetScreenVariable("shot", 2)
    elif shot == 2:
        timer R13_OPENING_SHOTS[2] action SetScreenVariable("shot", 3)
    else:
        timer (R13_OPENING_SHOTS[3] - .5) action Function(r13_opening_bump)
        timer R13_OPENING_SHOTS[3] action Return(True)

    # 클릭(또는 확인 키)은 다음 컷으로. 마지막 컷에서는 마차 대화로.
    key "dismiss" action (SetScreenVariable("shot", shot + 1) if shot < 3 else Return(True))
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
