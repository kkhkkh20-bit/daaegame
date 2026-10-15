# 메인 타이틀 도트 연출 (0.18.41).
#
# - 등장: 게임을 켠 뒤 처음 한 번만 로고가 위에서 떨어져 3px 단위로 통통 튀며 자리 잡고, 메뉴가 뒤따라 나타난다.
#   설정에서 돌아오는 등 다시 보일 때는 바로 제자리.
# - 계속: 게임 안과 같은 4px 도트 눈(두 겹), 등불·창 불빛 일렁임.
# 설정의 '움직임'이 꺼져 있으면 모두 멈춘 원래 화면이다. 메뉴 동작·저장 표시는 바꾸지 않는다.
init 61 python:
    R13_TITLE_STATE = {"intro_done": False}

    def r13_title_fx():
        spec = R13_DOT_FX.get("title", {})
        layers = []
        if spec.get("glow"):
            layers.append(R13FxPulse(spec["glow"], R13_LAMP_LEVELS, 1 / .16, spec["alpha"], (1280, 720)))
        snow = dict(R13_DOT_FX.get("snow", {}))
        if snow:
            snow["layers"] = [{"count": 70, "size": 4, "vy": [18, 28], "sway": 8},
                              {"count": 12, "size": 8, "vy": [38, 52], "sway": 12}]
            layers.append(R13FxSnow(snow, (1280, 720), seed=33))
        return Fixed(*layers, xysize=(1280, 720))

    def r13_title_intro(trans, st, at, part):
        """처음 한 번만: part 0=로고, 1=메뉴. 그 뒤로는 바로 제자리."""
        if R13_TITLE_STATE["intro_done"] or not persistent.room13_motion:
            trans.alpha = 1.0
            trans.yoffset = 0
            trans.xoffset = 0
            return None
        if part == 0:
            # 위에서 떨어져(0.42초) 통통 두 번. 3px 단위.
            steps = ((.00, -60, 0.0), (.06, -48, .4), (.12, -36, .7), (.18, -24, 1.0), (.24, -12, 1.0),
                     (.30, 0, 1.0), (.38, -9, 1.0), (.46, 0, 1.0), (.54, -3, 1.0), (.60, 0, 1.0))
            y, a = steps[-1][1], 1.0
            for t, yy, aa in steps:
                if st >= t:
                    y, a = yy, aa
            trans.yoffset = y
            trans.alpha = a
            return None if st >= .60 else .03
        # 메뉴: 로고가 자리 잡은 뒤 아래에서 6px 올라오며 나타난다.
        t = st - .55
        if t < 0:
            trans.alpha = 0.0
            trans.yoffset = 6
            return .03
        trans.alpha = min(1.0, t / .3)
        trans.yoffset = 6 if t < .12 else 3 if t < .24 else 0
        if t >= .3:
            R13_TITLE_STATE["intro_done"] = True
            return None
        return .03

transform r13_title_logo_in:
    function renpy.curry(r13_title_intro)(part=0)

transform r13_title_menu_in:
    function renpy.curry(r13_title_intro)(part=1)
