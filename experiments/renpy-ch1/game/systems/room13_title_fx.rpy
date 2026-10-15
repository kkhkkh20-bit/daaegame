# 메인 타이틀 도트 연출 (0.18.41).
#
# - 등장: 게임을 켠 뒤 처음 한 번만 로고가 천천히 떠오르듯 나타나고(페이드인, 0.18.45), 메뉴가 뒤따라 나타난다.
#   설정에서 돌아오는 등 다시 보일 때는 바로 제자리.
# - 계속: 게임 안과 같은 4px 도트 눈(두 겹), 등불·창 불빛 일렁임.
# 설정의 '움직임'이 꺼져 있으면 모두 멈춘 원래 화면이다. 메뉴 동작·저장 표시는 바꾸지 않는다.
init 61 python:
    R13_TITLE_STATE = {"intro_done": False}

    def r13_title_fx():
        spec = R13_DOT_FX.get("title", {})
        layers = []
        rig = r13_light_rig("title", (1280, 720))
        if rig:
            layers.append(rig)
        snow = dict(R13_DOT_FX.get("snow", {}))
        if snow:
            snow["layers"] = [{"count": 70, "size": 4, "vy": [18, 28], "sway": 8},
                              {"count": 12, "size": 8, "vy": [38, 52], "sway": 12}]
            layers.append(R13FxSnow(snow, (1280, 720), seed=33))
        return Fixed(*layers, xysize=(1280, 720))

    def r13_title_ease(u):
        u = min(1.0, max(0.0, u))
        return u * u * (3.0 - 2.0 * u)

    def r13_title_intro(trans, st, at, part):
        """처음 한 번만: part 0=로고, 1=메뉴. 동화처럼 천천히 떠오르는 페이드인(0.18.45 소유자).
        로고는 1.8초에 걸쳐 투명에서 나타나며 8px 아래에서 부드럽게 올라온다. 메뉴는 1.2초 뒤 1초 동안."""
        if R13_TITLE_STATE["intro_done"] or not persistent.room13_motion:
            trans.alpha = 1.0
            trans.yoffset = 0
            trans.xoffset = 0
            return None
        start, dur, rise = ((.25, 1.8, 8.0) if part == 0 else (1.2, 1.0, 6.0))
        u = r13_title_ease((st - start) / dur)
        trans.subpixel = True
        trans.alpha = u
        trans.yoffset = rise * (1.0 - u)
        if st >= start + dur:
            if part == 1:
                R13_TITLE_STATE["intro_done"] = True
            return None
        return 0

transform r13_title_logo_in:
    function renpy.curry(r13_title_intro)(part=0)

transform r13_title_menu_in:
    function renpy.curry(r13_title_intro)(part=1)
