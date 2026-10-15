# 그림책 톤 연출 (0.18.47). 소유자: "이 게임을 동화처럼." 튀는 효과보다 은은하게 스며드는 효과.
#
# - 화면 전환: 종이에 물감이 번지듯 가운데부터 바뀐다(날·시간대가 바뀌면 1초, 장소 이동은 0.5초).
# - 대사: 이름표는 말하는 사람이 바뀔 때만 살며시 나타나고, 다음 표시(▸)는 반딧불처럼 천천히 숨쉰다.
# - 증거 획득: 별 반짝임·튀어오름 대신 카드 뒤에 따뜻한 빛이 번졌다 사라진다.
# - 제시·반박: 집중선·화면 흔들림 대신 화면 가장자리가 잠깐 따뜻하게 어두워졌다 걷힌다.
# 설정의 '움직임'이 꺼져 있으면 모두 짧은 디졸브나 정지 화면이다. 상태는 바꾸지 않는다.
init 59 python:
    R13_STORYBOOK = R13_DOT_FX.get("storybook", {})

    def r13_bleed(time):
        mask = R13_STORYBOOK.get("bleed")
        if not mask or not r13_fx_active():
            return Dissolve(.25)
        return ImageDissolve(mask, time, ramplen=96)

    class R13NameFade(object):
        """이름표: 말하는 사람이 바뀔 때만 0.3초 동안 나타난다(같은 사람의 다음 대사에서는 그대로)."""
        def __init__(self):
            self.who = None
            self.started = 0.0
            self.last = -1.0
        def __call__(self, trans, st, at):
            who = store.r13_name_shown
            if who != self.who or st < self.last:
                self.who = who
                self.started = st
            self.last = st
            if not r13_fx_active():
                trans.alpha = 1.0
                trans.yoffset = 0
                return None
            u = min(1.0, max(0.0, (st - self.started) / .3))
            e = u * u * (3 - 2 * u)
            trans.alpha = e
            trans.yoffset = 4 * (1 - e)
            return 0 if u < 1.0 else None

    r13_name_fade_fn = R13NameFade()

    def r13_name_track(who):
        store.r13_name_shown = who
        return who

default r13_name_shown = None

transform r13_name_fade:
    subpixel True
    function r13_name_fade_fn

# 다음 표시: 반딧불처럼 천천히 밝아졌다 흐려진다(1.6초).
transform r13_next_glow:
    alpha .35
    block:
        ease .8 alpha 1.0
        ease .8 alpha .35
        repeat

# 증거 카드 뒤 따뜻한 빛: 0.4초에 번졌다가 1.2초에 걸쳐 사라진다.
transform r13_card_glow:
    alpha 0.0
    easein .4 alpha .55
    pause .3
    easeout 1.2 alpha 0.0

screen r13_fx_vignette():
    zorder 140
    add R13_STORYBOOK.get("vignette", Null()) at r13_vignette_pulse
    timer .9 action Hide("r13_fx_vignette")

transform r13_vignette_pulse:
    alpha 0.0
    easein .12 alpha .75
    easeout .7 alpha 0.0
