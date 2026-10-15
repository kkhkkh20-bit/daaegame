# 도트 연출 (0.18.23). 화면 연출만 하고 시간·증거·관계·일정은 바꾸지 않는다.
#
# - 여관 로비 벽난로 불꽃(아침·오후·저녁), 저녁 방 불빛 일렁임
# - 실외 저녁(광장·입구·제단 길) 눈 내림, 광장 저녁 가로등 빛
# - 다람이 대화 전신 눈 깜빡임(joy는 원래 눈을 감고 있어 제외)
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

    def r13_dot_fx_wanted(location, period):
        fx = R13_DOT_FX
        if location == "inn" and period in fx.get("inn_fire", {}).get("periods", {}):
            return True
        if period in fx.get("lamp_glow", {}).get(location, {}).get("periods", []):
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
        key = (location, period, path, tuple(crop) if crop else None)
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
            glow = fx.get("inn_glow", {})
            if period in glow.get("periods", []):
                layers.append(R13FxPulse(glow["file"], item["light"], fire["fps"], glow["alpha"], size))
        lamp = fx.get("lamp_glow", {}).get(location)
        if lamp and period in lamp.get("periods", []):
            # 두세 번에 한 번 짧게 흔들리는 가로등(1.0=평소).
            levels = [1, 1, 1, 1, 1, 1, .55, 1, .8, 1, 1, 1, 1, 1, 1, 1, 1, 1, .6, 1, 1, 1, 1, 1]
            layers.append(R13FxPulse(lamp["file"], levels, 1 / .12, lamp["alpha"], size))
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

        깜빡이는 때는 보여진 시간(st)으로만 정한다. 처음 1.6초는 깜빡이지 않아
        등장 직후 화면과 테스트 캡처가 원본과 같다.
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
            return self.interval[0] + (self.interval[1] - self.interval[0]) * value

        def phase(self, st):
            start = 1.6
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
