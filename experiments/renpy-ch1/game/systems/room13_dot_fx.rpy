# 도트 연출 (0.18.29, 0.18.31). 화면 연출만 하고 시간·증거·관계·일정은 바꾸지 않는다.
#
# - 여관 로비 벽난로 불꽃(아침·오후·저녁), 저녁 방 불빛 일렁임
# - 실외 저녁(광장·입구·제단 길) 눈 내림, 광장 저녁 가로등 빛
# - 다람이 대화 전신 눈 깜빡임(joy는 원래 눈을 감고 있어 제외)
# - (0.18.31) 광장 굴뚝 연기, 증거 획득 반짝임·튀어오름, 제시·반박 순간 흔들림과 집중선,
#   마을 지도 현재 위치 표식, 날·시간대가 바뀐 장면의 디더 전환
#
# 원본 배경·인물 그림은 바꾸지 않고 그 위에 프레임을 얹는다. 프레임과 좌표는
# assets/room13-dot-fx.json (dev/make_dot_fx.py가 만든다), 좌표는 원본 그림 픽셀 기준.
# 설정의 '움직임'을 끄거나 건너뛰기 중이면 모든 효과가 원본 그림 그대로 멈춘다.
# 함수 덮어쓰기 층을 더하지 않는다. 연결은 r13_world_background와
# r13_fullbody_close_art 안의 한 줄씩이다.

init 57 python:
    import json as r13_fx_json
    import math as r13_fx_math

    R13_DOT_FX = r13_fx_json.load(renpy.file("assets/room13-dot-fx.json")) if renpy.loadable("assets/room13-dot-fx.json") else {}

    def r13_fx_active():
        return bool(persistent.room13_motion) and not renpy.is_skipping()

    class R13FxClock(renpy.Displayable):
        """움직임 설정이 켜져 있을 때만 프레임을 고르는 공통 바탕.

        꺼져 있으면 아무것도 그리지 않고(원본 그대로), 설정이 바뀌는 것만 살핀다.
        """
        def __init__(self, size, **kwargs):
            super(R13FxClock, self).__init__(**kwargs)
            self.size = (int(size[0]), int(size[1]))

        def draw(self, out, st):
            return None

        def render(self, width, height, st, at):
            out = renpy.Render(*self.size)
            if not r13_fx_active():
                renpy.redraw(self, .25)
                return out
            wait = self.draw(out, st)
            renpy.redraw(self, wait if wait else .1)
            return out

    class R13FxSheet(R13FxClock):
        """가로로 늘어선 시트에서 프레임 하나를 골라 지정 위치에 얹는다."""
        def __init__(self, sheet, rect, frames, fps, size, **kwargs):
            super(R13FxSheet, self).__init__(size, **kwargs)
            x, y, w, h = rect
            self.pos = (int(x), int(y))
            self.frames = [Crop((i * w, 0, w, h), sheet) for i in range(int(frames))]
            self.fps = float(fps)

        def visit(self):
            return self.frames

        def draw(self, out, st):
            index = int(st * self.fps) % len(self.frames)
            out.blit(renpy.render(self.frames[index], self.size[0], self.size[1], st, 0), self.pos)
            return 1.0 / self.fps

    class R13FxPulse(R13FxClock):
        """빛 판을 더하기 혼합으로 얹는다. 밝기는 4단계로 끊어 도트처럼 바뀐다."""
        def __init__(self, plate, levels, fps, alpha, size, **kwargs):
            super(R13FxPulse, self).__init__(size, **kwargs)
            low, high = alpha
            steps = [round(v * 3) / 3.0 for v in levels]
            self.fps = float(fps)
            self.plates = [Transform(plate, alpha=low + (high - low) * v, blend="add") for v in steps]

        def visit(self):
            return self.plates

        def draw(self, out, st):
            index = int(st * self.fps) % len(self.plates)
            out.blit(renpy.render(self.plates[index], self.size[0], self.size[1], st, 0), (0, 0))
            return 1.0 / self.fps

    class R13FxSnow(R13FxClock):
        """두 겹 눈. 위치는 시간으로만 정해지고(상태 없음) 매번 4px 칸에 맞춘다."""
        def __init__(self, spec, size, seed=13, **kwargs):
            super(R13FxSnow, self).__init__(size, **kwargs)
            self.cell = int(R13_DOT_FX.get("cell", 4))
            self.images = [spec["small"], spec["big"]]
            state = seed
            self.flakes = []
            for layer, info in enumerate(spec["layers"]):
                for i in range(int(info["count"])):
                    vals = []
                    for _ in range(4):
                        state = (state * 16807) % 2147483647
                        vals.append(state / 2147483647.0)
                    lo, hi = info["vy"]
                    self.flakes.append((layer, vals[0] * self.size[0], vals[1] * (self.size[1] + 24),
                        lo + vals[2] * (hi - lo), vals[3] * 6.283, float(info["sway"])))

        def visit(self):
            return [renpy.displayable(i) for i in self.images]

        def draw(self, out, st):
            width, height = self.size
            span = height + 24
            cell = self.cell
            renders = [renpy.render(renpy.displayable(i), 8, 8, st, 0) for i in self.images]
            for layer, x0, y0, vy, phase, sway in self.flakes:
                y = (y0 + vy * st) % span - 12
                x = (x0 + r13_fx_math.sin(st * .9 + phase) * sway) % width
                out.blit(renders[layer], (int(x) // cell * cell, int(y) // cell * cell))
            return 1.0 / 15.0

    # 등불 밝기 순서(4단계로 끊긴다): 대부분 평소, 가끔 한두 단계 어두워진다.
    R13_LAMP_LEVELS = [1, 1, .67, 1, .67, .33, .67, 1, 1, 1, .67, 1, .33, .67, 1, 1, 1, .67]

    def r13_dot_fx_wanted(location, period):
        fx = R13_DOT_FX
        if "%s:%s" % (location, period) in fx.get("lights", {}):
            return True
        if location == "inn" and period in fx.get("inn_fire", {}).get("periods", {}):
            return True
        if period in fx.get("lamp_glow", {}).get(location, {}).get("periods", []):
            return True
        smoke = fx.get("smoke", {})
        if location in smoke.get("sources", {}) and period in smoke.get("periods", []):
            return True
        if period in fx.get("lamps", {}).get(location, {}).get("periods", []):
            return True
        if location == "inn" and period in fx.get("inn_window", {}).get("periods", []):
            return True
        snow = fx.get("snow", {})
        return location in snow.get("locations", []) and period in snow.get("periods", [])

    # 같은 장면은 같은 효과 묶음을 다시 쓴다. 허브는 화면을 자주 다시 그리며
    # r13_world_background를 부르므로, 매번 그림 크기를 읽거나 새로 만들면 웹판이 멈춘다.
    R13_DOT_FX_SCENES = {}

    def r13_dot_fx_scene(location, period, source, path, crop=None):
        """r13_world_background가 부른다. 효과가 없으면 원본을 그대로 돌려준다."""
        if not R13_DOT_FX or not r13_dot_fx_wanted(location, period):
            return source
        key = (location, period, path, tuple(crop) if crop else None,r13_scene_contrast_key(location,period))
        cached = R13_DOT_FX_SCENES.get(key)
        if cached is None:
            size = tuple(int(v) for v in crop[2:]) if crop else renpy.image_size(path)
            cached = r13_dot_fx_build(location, period, source, size)
            R13_DOT_FX_SCENES[key] = cached
        return cached

    def r13_dot_fx_build(location, period, source, size):
        fx = R13_DOT_FX
        layers = []
        fire = fx.get("inn_fire", {})
        if location == "inn" and period in fire.get("periods", {}):
            item = fire["periods"][period]
            layers.append(R13FxSheet(item["sheet"], fire["rect"], fire["frames"], fire["fps"], size))
        # 0.18.53: 빛과 그림자가 함께 숨쉬는 조명 장치(이전의 빛 판 깜빡임을 대신한다).
        rig = r13_light_rig("%s:%s" % (location, period), size)
        if rig:
            layers.append(rig)
        smoke = fx.get("smoke", {})
        if location in smoke.get("sources", {}) and period in smoke.get("periods", []):
            layers.append(R13FxSmoke(smoke, smoke["sources"][location], size))
        window = fx.get("inn_window", {})
        if location == "inn" and period in window.get("periods", []):
            wx, wy, ww, wh = window["rect"]
            spec = dict(fx.get("snow", {}), layers=window["layers"])
            layers.append(Transform(AlphaMask(R13FxSnow(spec, (ww, wh), seed=7), window["mask"]), xpos=wx, ypos=wy))
        snow = fx.get("snow", {})
        if location in snow.get("locations", []) and period in snow.get("periods", []):
            layers.append(R13FxSnow(snow, size))
        if not layers:
            return source
        return Fixed(source, *layers, xysize=size)

    # ---------------------------------------------------------------- 눈 깜빡임
    def r13_blink_seed(text):
        return sum((i + 1) * ord(c) for i, c in enumerate(text))

    class R13Blink(renpy.Displayable):
        """대화 전신 그림 위에 눈꺼풀 조각을 잠깐 얹는다.

        깜빡이는 때는 보여진 시간(st)으로만 정한다. 등장 0.7초 동안은 깜빡이지 않는다.
        """
        def __init__(self, base, person, emotion, spec, **kwargs):
            super(R13Blink, self).__init__(**kwargs)
            self.base = renpy.displayable(base)
            self.half = renpy.displayable(spec["half"])
            self.closed = renpy.displayable(spec["closed"])
            self.pos = (int(spec["rect"][0]), int(spec["rect"][1]))
            blink = R13_DOT_FX.get("blink", {})
            self.timeline = [(name, float(sec)) for name, sec in blink.get("timeline", [["half", .05], ["closed", .09], ["half", .05]])]
            self.interval = tuple(blink.get("interval", [2.6, 5.2]))
            self.seed = r13_blink_seed(person + emotion)

        def visit(self):
            return [self.base, self.half, self.closed]

        def gap(self, n):
            # n번째 깜빡임 앞의 쉬는 시간(사람·표정마다 다르지만 늘 같은 순서).
            value = ((self.seed * 1103515245 + n * 12345) >> 4) % 1000 / 1000.0
            if n == 0:
                # 첫 깜빡임은 빨리(0.7초 대기 뒤 0.6~1.6초): 짧은 대사에서도 한 번은 보인다.
                return .6 + 1.0 * value
            return self.interval[0] + (self.interval[1] - self.interval[0]) * value

        def phase(self, st):
            # 표정이 자주 바뀌어도 보이도록 등장 0.7초 뒤부터 깜빡일 수 있다(0.18.41).
            start = 0.7
            n = 0
            while True:
                start += self.gap(n)
                length = sum(sec for _, sec in self.timeline)
                if st < start:
                    return None, start - st
                if st < start + length:
                    t = st - start
                    for name, sec in self.timeline:
                        if t < sec:
                            return name, sec - t
                        t -= sec
                n += 1
                start += length
                if n > 400:
                    return None, 1.0

        def render(self, width, height, st, at):
            base = renpy.render(self.base, width, height, st, at)
            if not r13_fx_active():
                renpy.redraw(self, .25)
                return base
            name, wait = self.phase(st)
            out = renpy.Render(base.width, base.height)
            out.blit(base, (0, 0))
            if name:
                piece = self.half if name == "half" else self.closed
                out.blit(renpy.render(piece, width, height, st, at), self.pos)
            renpy.redraw(self, max(.016, min(wait, .5)))
            return out

    def r13_blink_art(person, emotion, file):
        spec = R13_DOT_FX.get("blink", {}).get("people", {}).get(person, {}).get(emotion)
        if not spec:
            return file
        return R13Blink(file, person, emotion, spec)

    # ---------------------------------------------------------------- 0.18.31
    class R13FxSmoke(R13FxClock):
        """굴뚝 연기. 덩어리는 시간으로만 정해지고(상태 없음) 4px 칸에 맞춘다."""
        def __init__(self, spec, sources, size, **kwargs):
            super(R13FxSmoke, self).__init__(size, **kwargs)
            self.sources = [tuple(p) for p in sources]
            self.puffs = dict((k, renpy.displayable(v)) for k, v in spec["puffs"].items())
            self.every = float(spec["every"])
            self.life = float(spec["life"])
            self.rise = float(spec["rise"])
            self.drift = float(spec["drift"])

        def visit(self):
            return list(self.puffs.values())

        def draw(self, out, st):
            per = int(self.life / self.every) + 1
            for i, (x0, y0) in enumerate(self.sources):
                offset = i * .37
                newest = int((st + offset) / self.every)
                for n in range(newest, newest - per, -1):
                    age = st + offset - n * self.every
                    if age < 0 or age >= self.life:
                        continue
                    u = age / self.life
                    size = 4 if u < .27 else 8 if u < .62 else 12
                    level = 2 if u < .5 else 1 if u < .8 else 0
                    sway = 3 * r13_fx_math.sin(age * 1.7 + n)
                    x = x0 + self.drift * u + sway - size / 2.0
                    y = y0 - self.rise * u - size
                    piece = self.puffs["%d-%d" % (size, level)]
                    out.blit(renpy.render(piece, size, size, st, 0), (int(x) // 4 * 4, int(y) // 4 * 4))
            return 1.0 / 12.0

    class R13FxOnce(renpy.Displayable):
        """시트를 한 번만 재생하고 사라진다(증거 반짝임)."""
        def __init__(self, sheet, frames, fps, size, delay=0.0, **kwargs):
            super(R13FxOnce, self).__init__(**kwargs)
            self.delay = float(delay)
            w, h = size
            self.size = (int(w), int(h))
            self.frames = [Crop((i * w, 0, w, h), sheet) for i in range(int(frames))]
            self.fps = float(fps)

        def visit(self):
            return self.frames

        def render(self, width, height, st, at):
            out = renpy.Render(*self.size)
            if st < self.delay:
                renpy.redraw(self, self.delay - st)
                return out
            index = int((st - self.delay) * self.fps)
            if r13_fx_active() and index < len(self.frames):
                out.blit(renpy.render(self.frames[index], self.size[0], self.size[1], st, at), (0, 0))
                renpy.redraw(self, 1.0 / self.fps)
            return out

    def r13_evidence_sparkle(delay=0.0):
        spec = R13_DOT_FX.get("evidence_sparkle")
        if not spec:
            return Null()
        return R13FxOnce(spec["sheet"], spec["frames"], spec["fps"], spec["size"], delay=delay)

    class R13FxImpact(renpy.Displayable):
        """제시·반박 순간의 도트 집중선 3프레임(4px 칸, 화면 가장자리에서 안쪽으로)."""
        def __init__(self, **kwargs):
            super(R13FxImpact, self).__init__(**kwargs)
            state = 29
            self.rays = []
            for i in range(44):
                state = (state * 16807) % 2147483647
                jitter = state / 2147483647.0
                angle = (i + jitter * .6) / 44.0 * 6.283
                state = (state * 16807) % 2147483647
                self.rays.append((angle, .55 + .35 * state / 2147483647.0))

        def render(self, width, height, st, at):
            out = renpy.Render(1280, 720)
            frame = int(st / .06)
            if not r13_fx_active() or frame > 2:
                return out
            canvas = out.canvas()
            reach = (.30, .22, .14)[frame]
            for angle, length in self.rays:
                dx, dy = r13_fx_math.cos(angle), r13_fx_math.sin(angle)
                # 화면 가장자리까지의 거리(가운데 기준)
                edge = min(abs(640 / dx) if dx else 1e9, abs(360 / dy) if dy else 1e9)
                start = edge * (1 - reach * length)
                d = edge
                while d > start:
                    x = int(640 + dx * d) // 4 * 4
                    y = int(360 + dy * d) // 4 * 4
                    canvas.rect((255, 250, 232, 235), (x, y, 4, 4))
                    d -= 8
            renpy.redraw(self, .06 - (st % .06) + .001)
            return out

    def r13_fx_cue(kind):
        """소리와 같은 순간에 부르는 화면 연출. 0.18.47: 집중선·흔들림 대신 가장자리가 따뜻하게 어두워졌다 걷힌다."""
        if not r13_fx_active():
            return
        if kind in ("present", "break"):
            renpy.show_screen("r13_fx_vignette")

    def r13_evidence_hop(trans, st, at):
        # 0.18.47: 튀어오름 없음(저장된 화면 호환용으로 이름만 남김).
        trans.yoffset = 0
        return None

    # 마을 지도 현재 위치 표식: 4px 도트 핀이 반초마다 한 칸 오르내린다.
    class R13FxPin(renpy.Displayable):
        SHAPE = ("..##..", ".####.", "######", ".####.", "..##..", "..##..")

        def render(self, width, height, st, at):
            out = renpy.Render(24, 32)
            canvas = out.canvas()
            lift = 4 if (r13_fx_active() and int(st * 2) % 2) else 0
            for y, row in enumerate(self.SHAPE):
                for x, ch in enumerate(row):
                    if ch == "#":
                        color = (255, 214, 96, 255) if y in (1, 2, 3) and x in (1, 2, 3, 4) else (40, 24, 18, 255)
                        if y in (1, 2, 3) and x in (2, 3) and y == 2:
                            color = (255, 248, 214, 255)
                        canvas.rect(color, (x * 4, 4 - lift + y * 4, 4, 4))
            if r13_fx_active():
                renpy.redraw(self, .5 - (st % .5) + .001)
            return out

    # 날·시간대가 바뀐 뒤 처음 들어서는 장면: 4x4 디더로 번진다.
    def r13_scene_transition():
        # 0.18.47 그림책 톤: 종이에 번지듯 바뀐다. 날·시간대가 바뀌면 천천히(1초), 장소 이동은 0.5초.
        state = store.room13 or {}
        clock = (state.get("day"), state.get("period"))
        last = store.r13_fx_scene_clock
        store.r13_fx_scene_clock = clock
        if last is not None and last != clock and clock[0] is not None:
            return r13_bleed(1.0)
        return r13_bleed(.5)

default r13_fx_scene_clock = None

transform r13_fx_shake:
    xoffset 0
    xoffset 2
    pause .04
    xoffset -2
    pause .04
    xoffset 2
    pause .04
    xoffset 0

screen r13_fx_impact():
    zorder 140
    add R13FxImpact()
    timer .25 action Hide("r13_fx_impact")

# ---------------------------------------------------------------- 0.18.33
# 대화 중 표정이 바뀌는 순간의 몸 반응(다람이). 움찔·깡총·부르르·움츠림·갸웃.
# 움직임은 대화 그림 도트 크기(3px)의 배수로만 움직여 픽셀이 뭉개지지 않는다.
# 놀람·화남은 '먼저 반응하고 표정이 바뀐다': 앞 표정 그대로 잠깐 움찔한 뒤 새 표정으로 바뀐다.
init 57 python:
    # 0.18.37: 대화가 많은 인물로 넓혔다. 몸집이 큰 인물(부엉이 할아버지, 경비)은 움직임이 과해 보여 넣지 않았다.
    R13_REACT_PEOPLE = ("daram", "buri", "nabi", "bami", "mom", "karo", "granny", "doto", "neoul", "seryeon", "resident_seori")
    # 감정: 앞 표정을 유지하는 시간(초)
    R13_REACT_LEAD = {"surprise": .10, "angry": .07, "joy": 0.0, "anxious": 0.0, "flustered": 0.0, "thinking": 0.0}
    R13_REACT_LAST = {}          # person -> (emotion, art). 저장하지 않는 화면 기억.

    class R13Anticipate(renpy.Displayable):
        """처음 lead초는 앞 그림, 그 뒤 새 그림."""
        def __init__(self, before, after, lead, **kwargs):
            super(R13Anticipate, self).__init__(**kwargs)
            self.before = renpy.displayable(before)
            self.after = renpy.displayable(after)
            self.lead = float(lead)

        def visit(self):
            return [self.before, self.after]

        def render(self, width, height, st, at):
            if st < self.lead:
                renpy.redraw(self, self.lead - st)
                return renpy.render(self.before, width, height, st, at)
            return renpy.render(self.after, width, height, st, at)

    def r13_react_kind(who, arriving, actor_pose):
        if not r13_fx_active():
            return None
        if who not in R13_REACT_PEOPLE:
            return None
        emotion = r13_fullbody_emotion(actor_pose) if r13_fullbody_spec(who, actor_pose) else None
        # 생각하는 표정은 그림이 neutral과 같아 따로 고개를 갸웃한다(0.18.41).
        if r13_fullbody_key(actor_pose) == "thinking" and not arriving:
            return "thinking"
        last = R13_REACT_LAST.get(who)
        if emotion not in R13_REACT_LEAD:
            return None
        if arriving:
            # 등장하자마자 놀라거나 기뻐하는 경우만 반응한다(앞 표정이 없으니 기다리지 않는다).
            return emotion if emotion in ("surprise", "joy") else None
        if last and last[0] == emotion:
            return None
        return emotion

    def r13_react(kind, who, actor_pose, what, at_list):
        spec = r13_fullbody_spec(who, actor_pose)
        before = R13_REACT_LAST.get(who)
        # 앞 그림은 페이드 없이 기억한다(다시 보일 때 투명에서 시작하지 않게).
        R13_REACT_LAST[who] = ((spec or {}).get("emotion"), r13_close_art(who, actor_pose, r13_say_actor_h(), True, False) if spec else what)
        if not r13_fx_active():
            return what, at_list
        lead = R13_REACT_LEAD.get(kind, 0.0) if kind else 0.0
        if lead and before is not None:
            what = R13Anticipate(before[1], what, lead)
        else:
            lead = 0.0
        # 0.18.39 (owner): the synthesized 8-bit reaction sounds were removed; motion only.
        size = r13_body_size(who, actor_pose)
        if size:
            # 0.18.43 (owner): 1:1 대화는 부드럽게(매 프레임) 움직인다. 발밑 가운데를 축으로
            # 늘이고 눌러(스쿼시·스트레치) "확" 하는 느낌을 내고, 그 뒤엔 숨쉬기만 한다.
            # 0.18.44 (owner): no breathing; only the emotion motion, then still.
            body = R13_BODY_MOTION.get(kind) if kind else None
            if not body:
                return what, at_list
            return Fixed(At(what, body(lead)), xysize=size), at_list
        if not kind:
            return what, at_list
        motion = {"surprise": r13_react_surprise, "joy": r13_react_joy, "angry": r13_react_angry,
                  "anxious": r13_react_anxious, "flustered": r13_react_flustered,
                  "thinking": r13_react_thinking}[kind]
        return what, list(at_list) + [motion(lead)]

    def r13_body_size(who, pose):
        spec = r13_fullbody_spec(who, pose)
        if not spec:
            return None
        # 2026-10-28 캡처 검수(11일 엄마 놀람): 대사 인물이 1.55배(r13_say_actor_h)로 커졌는데 움찔 효과의 틀은 예전 키(840)로
        # 잡혀, 틀 62% 높이에 큰 그림의 62% 지점을 맞추느라 그림이 약 265px 위로 밀려 머리가 잘렸다. 지금 대사 키로 잡는다.
        scale = r13_fullbody_scale(who, r13_say_actor_h())
        return (int(round(spec["crop"][2] * scale)), int(round(spec["crop"][3] * scale)))

# 3px 배수. 앞 표정(lead) 동안 움찔/웅크림 → 새 표정과 함께 움직임 → 제자리.
transform r13_react_surprise(lead=.10):
    yoffset 0 xoffset 0
    yoffset 9
    pause max(lead, .06)
    yoffset -30
    pause .08
    yoffset -21
    pause .05
    yoffset -12
    pause .05
    yoffset -3
    pause .05
    yoffset 0

transform r13_react_joy(lead=0.0):
    yoffset 0
    yoffset -18
    pause .07
    yoffset 0
    pause .06
    yoffset -12
    pause .06
    yoffset 0

transform r13_react_angry(lead=.07):
    xoffset 0 yoffset 0
    yoffset 3
    pause max(lead, .05)
    xoffset 9
    pause .04
    xoffset -9
    pause .04
    xoffset 6
    pause .04
    xoffset -3
    pause .04
    xoffset 0 yoffset 0

transform r13_react_anxious(lead=0.0):
    yoffset 0 xoffset 0
    yoffset 6
    pause .08
    yoffset 12
    pause .10
    xoffset 3
    pause .05
    xoffset -3
    pause .05
    xoffset 3
    pause .05
    xoffset 0
    pause .20
    yoffset 6
    pause .08
    yoffset 3
    pause .08
    yoffset 0

# 생각: 한쪽으로 3px씩 기울어 잠시 머문 뒤 제자리(멈춘 채 대화).
transform r13_react_thinking(lead=0.0):
    xoffset 0 yoffset 0
    pause .05
    xoffset 3
    pause .08
    xoffset 6 yoffset 3
    pause .9
    xoffset 3
    pause .08
    xoffset 0 yoffset 0

transform r13_react_flustered(lead=0.0):
    xoffset 0
    xoffset -9
    pause .07
    xoffset 9
    pause .07
    xoffset -6
    pause .07
    xoffset 3
    pause .06
    xoffset 0


# ---------------------------------------------------------------- 0.18.37 장면 그림
init 57 python:
    R13_CINE_FX_CACHE = {}

    def r13_cinematic_fx(key, art, size):
        """장면 그림 위 등불 일렁임과 바깥 눈(움직임 설정을 따른다)."""
        spec = R13_DOT_FX.get("cinematics", {}).get(key)
        if not spec:
            return art
        cache_key = (key, tuple(size))
        cached = R13_CINE_FX_CACHE.get(cache_key)
        if cached is not None:
            return cached
        layers = []
        rig = r13_light_rig("cine:" + key, size)
        if rig:
            layers.append(rig)
        if spec.get("snow"):
            snow = dict(R13_DOT_FX.get("snow", {}))
            # 832x466 그림 기준: 눈 수와 속도를 화면 비율만큼 줄인다.
            snow["layers"] = [{"count": 70, "size": 4, "vy": [16, 26], "sway": 6},
                              {"count": 14, "size": 8, "vy": [34, 50], "sway": 10}]
            layers.append(R13FxSnow(snow, size, seed=11))
        cached = Fixed(art, *layers, xysize=size)
        R13_CINE_FX_CACHE[cache_key] = cached
        return cached


# ---------------------------------------------------------------- 0.18.43 1:1 대화 몸동작
# 원본 표정 그림 한 장을 허리 높이(그림 위에서 62%) 가운데를 축으로 늘이고 누르고 띄워 동작을 만든다(매 프레임, 부드러운 가감속).
# 동작이 끝나면 멈춘다(0.18.44 소유자: 숨쉬기 꿀렁임 제거). 조사(배경) 화면 인물은 여전히 움직이지 않는다.
init 57 python:
    def r13_body_motion_table():
        return {"surprise": r13_body_surprise, "joy": r13_body_joy, "angry": r13_body_angry,
                "anxious": r13_body_anxious, "flustered": r13_body_flustered, "thinking": r13_body_thinking}

init 58 python:
    R13_BODY_MOTION = r13_body_motion_table()

transform r13_body_base:
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62

transform r13_body_idle:
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0

# 놀람: (앞 얼굴로) 움츠림 → 새 얼굴로 확 솟구침 → 공중에서 잠깐 → 착지하며 눌림 → 제자리
transform r13_body_surprise(lead=.10):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    easein max(lead, .07) xzoom 1.033 yzoom 0.956 yoffset 4
    easeout .09 xzoom 0.9615 yzoom 1.05 yoffset -42
    easein .12 xzoom 0.9835 yzoom 1.016 yoffset -48
    easein .10 xzoom 1.033 yzoom 0.9615 yoffset 0
    easeout .16 xzoom 0.9945 yzoom 1.006
    ease .12 xzoom 1 yzoom 1

# 기쁨: 웅크렸다 통통 두 번
transform r13_body_joy(lead=0.0):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    easein .07 xzoom 1.028 yzoom 0.967
    easeout .10 xzoom 0.978 yzoom 1.033 yoffset -30
    easein .10 xzoom 1 yzoom 1 yoffset 0
    easein .05 xzoom 1.022 yzoom 0.9725
    easeout .09 xzoom 0.9835 yzoom 1.022 yoffset -18
    easein .09 xzoom 1 yzoom 1 yoffset 0
    easein .05 xzoom 1.011 yzoom 0.989
    ease .10 xzoom 1 yzoom 1

# 화남: (앞 얼굴로) 움찔 → 새 얼굴로 앞으로 들썩이며 부르르
transform r13_body_angry(lead=.07):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    easein max(lead, .05) xzoom 1.022 yzoom 0.9725 yoffset 4
    easeout .07 xzoom 0.9835 yzoom 1.028 yoffset -10
    linear .035 xoffset 10
    linear .035 xoffset -10
    linear .035 xoffset 8
    linear .035 xoffset -7
    linear .035 xoffset 5
    linear .035 xoffset -3
    ease .14 xoffset 0 yoffset 0 xzoom 1 yzoom 1

# 불안: 몸을 움츠려 잔떨림 → 천천히 펴짐
transform r13_body_anxious(lead=0.0):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    ease .18 xzoom 1.016 yzoom 0.967 yoffset 8
    linear .04 xoffset 3
    linear .04 xoffset -3
    linear .04 xoffset 3
    linear .04 xoffset -3
    linear .04 xoffset 2
    linear .04 xoffset 0
    pause .25
    ease .6 xzoom 1 yzoom 1 yoffset 0

# 당황: 좌우로 허둥지둥
transform r13_body_flustered(lead=0.0):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    ease .11 xoffset -14 yzoom 0.989
    ease .13 xoffset 14 yzoom 1.011
    ease .12 xoffset -8 yzoom 0.9945
    ease .12 xoffset 4 yzoom 1
    ease .14 xoffset 0

# 생각: 한쪽으로 천천히 기울어 머문 뒤 제자리
transform r13_body_thinking(lead=0.0):
    subpixel True
    xanchor .5 yanchor .62 xpos .5 ypos .62
    xzoom 1 yzoom 1 xoffset 0 yoffset 0
    ease .3 xoffset 12 yoffset 4 yzoom 0.9918
    pause .9
    ease .4 xoffset 0 yoffset 0 yzoom 1

# ---------------------------------------------------------------- 0.18.53 빛과 그림자
# 불빛이 흔들리면 방 전체의 명암이 같이 숨쉰다(소유자: "횃불이 있으면 그림자 부분도 일렁여야").
#  - 빛마다 따로, 매 프레임 부드럽게 흔들린다(불꽃은 빠르고 크게, 등불은 느리고 작게, 촛불은 그 사이).
#  - 가장 센 빛이 약해지면 빛에서 먼 곳이 짙어져 빛 웅덩이가 줄어들고, 세지면 넓어진다.
#  - 벽난로 앞 바닥 그림자는 불꽃이 커질 때 짙어지며 불 반대쪽으로 아주 조금 늘어난다.
# 판은 dev/make_dot_fx.py의 light_rigs()가 만든다(room13-dot-fx.json "lights").
init 57 python:
    R13_LIGHT_KINDS = {
        # (기본 밝기, 흔들림 폭, 빠르기)
        "fire": (.78, .30, 5.5),
        "candle": (.84, .20, 3.6),
        "lamp": (.93, .09, 1.1),
    }

    def r13_noise_table(seed, n=64):
        state = seed * 7919 + 13
        vals = []
        for _ in range(n):
            state = (state * 16807) % 2147483647
            vals.append(state / 2147483647.0)
        return vals

    def r13_smooth_noise(table, t):
        n = len(table)
        i = int(t) % n
        f = t - int(t)
        f = f * f * (3 - 2 * f)
        return table[i] * (1 - f) + table[(i + 1) % n] * f

    class R13FxLightRig(R13FxClock):
        def __init__(self, spec, size, **kwargs):
            super(R13FxLightRig, self).__init__(size, **kwargs)
            self.spec = spec
            self.lights = []
            for i, g in enumerate(spec["glows"]):
                base, amp, rate = R13_LIGHT_KINDS.get(g["kind"], R13_LIGHT_KINDS["lamp"])
                self.lights.append(dict(g, base=base, amp=amp, rate=rate,
                    n1=r13_noise_table(i * 3 + 1), n2=r13_noise_table(i * 3 + 2), phase=i * 1.37))
            self.lead = spec.get("lead", 0)
            self.shade = renpy.displayable(spec["shade"])
            self.sway = spec.get("sway")

        def visit(self):
            out = [self.shade] + [renpy.displayable(l["file"]) for l in self.lights]
            if self.sway:
                out.append(renpy.displayable(self.sway["file"]))
            return out

        def level(self, l, st):
            v = (.6 * r13_smooth_noise(l["n1"], st * l["rate"] + l["phase"])
                 + .25 * r13_smooth_noise(l["n2"], st * l["rate"] * 2.3)
                 + .15 * (.5 + .5 * r13_fx_math.sin(st * .9 + l["phase"])))
            # 여러 잡음을 더하면 가운데로 몰리므로 폭을 다시 넓힌다.
            v = min(1.0, max(0.0, (v - .5) * 2.0 + .5))
            # 0~1로 정규화한 세기(1=가장 밝음)와 실제 밝기
            return v, l["base"] + l["amp"] * (v - .5) * 2

        def draw(self, out, st):
            w, h = self.size
            lead_v = .5
            for i, l in enumerate(self.lights):
                v, _ = self.level(l, st)
                if i == self.lead:
                    lead_v = v
                a = .30 * l["strength"] * (.25 + .75 * v)
                g = renpy.render(Transform(l["file"], alpha=a, blend="add"), w, h, st, 0)
                out.blit(g, tuple(l["pos"]))
            # 빛 웅덩이: 가장 센 빛이 약할수록 먼 곳이 짙어진다.
            sa = self.spec["shade_alpha"] * (.15 + .85 * (1 - lead_v))
            out.blit(renpy.render(Transform(self.shade, alpha=sa), w, h, st, 0), (0, 0))
            if self.sway:
                cx, cy = self.sway["center"]
                z = 1.0 + .008 * (lead_v - .5) * 2
                r = renpy.render(Transform(self.sway["file"], zoom=z, alpha=self.sway["alpha"] * (.25 + .75 * lead_v)), w, h, st, 0)
                out.subpixel_blit(r, (cx * (1 - z), cy * (1 - z)))
            return 1.0 / 20.0

    def r13_light_rig(key, size):
        spec = R13_DOT_FX.get("lights", {}).get(key)
        return R13FxLightRig(spec, size) if spec else None
