# 다람탐정 v2 엔진 한 벌.
# 대사·흐름은 game/story/dayNN.json 한 곳에만 있고, 이 파일은 그것을 읽어 돌린다.
# 원칙(소유자 C안, 2026-10-30): 같은 함수를 덮어쓰지 않는다. init 우선순위로 순서를 맞추지 않는다.
# 기능을 바꿀 때는 그 함수 하나를 고친다. dev/test_no_override.py 가 이것을 지킨다.

init python:
    import json
    import re
    import time as v2_clock

    def v2_load(path):
        f = renpy.open_file(path, encoding="utf-8")
        try:
            return json.load(f)
        finally:
            f.close()

    V2_DAY = v2_load("story/day01.json")
    V2_COMMON = v2_load("story/common.json")
    V2_LAYOUT = v2_load("data/layout.json")
    V2_PEOPLE = V2_COMMON["people"]
    V2_EVIDENCE = V2_COMMON["evidence"]
    V2_PLACES = V2_COMMON["places"]
    V2_SCENES = V2_DAY["scenes"]
    V2_GATES = V2_DAY["gates"]
    V2_PROOFS = V2_DAY["proofs"]
    V2_PERIODS = ("오전", "오후", "저녁")
    # 대화 그림이 있는 인물(아빠는 그리지 않는다).
    V2_DRAWN = ("daram", "guard", "karo", "granny", "neoul")
    V2_FACE = {"surprise": "surprise_talk", "thinking": "neutral"}
    V2_SEAT_OF = {"neutral": "neutral", "thinking": "neutral", "joy": "joy", "angry": "pout",
                  "anxious": "wistful", "flustered": "secret", "surprise": "quiz"}

    # ---- 대사 묶음 등록: 모든 단계 목록에 이름을 붙여 저장에는 (이름, 순번)만 남긴다 ----
    V2_BLOCKS = {}

    def v2_register(bid, steps):
        V2_BLOCKS[bid] = steps
        for i, st in enumerate(steps):
            if "if" in st:
                v2_register("%s/%d/then" % (bid, i), st.get("then", []))
                v2_register("%s/%d/else" % (bid, i), st.get("else", []))
            if "menu" in st:
                for j, item in enumerate(st["menu"]):
                    v2_register("%s/%d/m%d" % (bid, i, j), item.get("do", []))

    for _k, _steps in V2_DAY["nodes"].items():
        v2_register("n:" + _k, _steps)
    for _g, _gate in V2_GATES.items():
        for _i, _o in enumerate(_gate["options"]):
            v2_register("g:%s/%d" % (_g, _i), _o["do"])
    for _p, _proof in V2_PROOFS.items():
        for _i, _o in enumerate(_proof["outcomes"]):
            v2_register("p:%s/o%d" % (_p, _i), _o["do"])
        for _key in ("press", "investigate"):
            if _key in _proof:
                v2_register("p:%s/%s" % (_p, _key), _proof[_key])
        for _s in (_proof.get("observe") or {}).get("spots", []):
            v2_register("p:%s/spot:%s" % (_p, _s["id"]), _s["do"])
    for _place, _objs in V2_DAY["objects"].items():
        for _o, _spec in _objs.items():
            if "read" in _spec:
                v2_register("o:%s/%s" % (_place, _o), _spec["read"]["do"])
    for _f in V2_DAY["followups"]:
        v2_register("f:" + _f["id"], _f["do"])

    # ---- 조건: 데이터의 조건 문자열을 정해진 이름만으로 판정한다(dev/test_story_data.py 가 이름을 검사) ----
    def v2_has(e):
        return e in store.v2_ev

    def v2_value(k):
        return store.v2_vals.get(k)

    def v2_cond(expr, won=False):
        if expr is None or expr == "True":
            return True
        chosen = set(store.v2_chosen)
        names = {
            "has": v2_has,
            "v": v2_value,
            "chose": lambda *ids: all(i in chosen for i in ids),
            "chose_only": lambda *ids: chosen == set(ids),
            "won": won,
            "True": True,
            "False": False,
        }
        return bool(eval(expr, {"__builtins__": {}}, names))

    # ---- 쌓기(stack): 각 칸은 [묶음 이름, 순번, 쪽] 또는 [None, 순번, 쪽, 즉석 단계 목록] ----
    def v2_steps(frame):
        return frame[3] if frame[0] is None else V2_BLOCKS[frame[0]]

    def v2_push(bid):
        store.v2_stack.append([bid, 0, 0])

    def v2_push_steps(steps):
        if steps:
            store.v2_stack.append([None, 0, 0, list(steps)])

    def v2_goto(node):
        store.v2_stack[:] = [["n:" + node, 0, 0]]

    def v2_current():
        frame = store.v2_stack[-1]
        return frame, v2_steps(frame)[frame[1]]

    def v2_new_game():
        store.v2_vals = {}
        store.v2_ev = []
        store.v2_met = []
        store.v2_loc = "black"
        store.v2_day = V2_DAY["day"]
        store.v2_period = 0
        store.v2_minutes = 0
        store.v2_scene = None
        store.v2_gate = None
        store.v2_ui = None
        store.v2_reopen = None
        store.v2_cam = {}
        store.v2_fig = None
        store.v2_kept = {}
        store.v2_chosen = []
        store.v2_goal_seen = ""
        store.v2_ended = False
        store.v2_stack = [["n:" + V2_DAY["start"], 0, 0]]
        store.v2_trace = []

    def v2_advance():
        """다음에 사람이 볼(고를) 단계까지 비대화 단계를 실행하고 그 종류를 돌려준다."""
        while True:
            if store.v2_ui:
                return "ui"
            if not store.v2_stack:
                return None
            frame = store.v2_stack[-1]
            steps = v2_steps(frame)
            if frame[1] >= len(steps):
                store.v2_stack.pop()
                continue
            st = steps[frame[1]]
            if "t" in st:
                return "line"
            if "wait" in st:
                gate = st["wait"]
                reopen = store.v2_reopen
                store.v2_reopen = None
                if reopen and reopen[0] == gate and v2_has_business(reopen[1], gate):
                    store.v2_gate = gate
                    store.v2_ui = ["topics", reopen[1]]
                    return "ui"
                return "wait"
            if "menu" in st:
                items = v2_menu_items(st)
                if len(items) == 1:
                    # 선택지가 하나면 창을 띄우지 않고 진행한다(소유자 결정).
                    frame[1] += 1
                    v2_push_any(items[0][1])
                    continue
                return "menu"
            if "proof" in st:
                return "proof"
            if "end_day" in st:
                store.v2_stack[:] = []
                store.v2_ended = True
                persistent.v2_last_end = dict(day=store.v2_day, ev=list(store.v2_ev), vals=dict(store.v2_vals))
                return None
            frame[1] += 1
            v2_exec(st, frame)

    def v2_exec(st, frame):
        """화면을 기다리지 않는 단계 하나."""
        bid = frame[0] if frame[0] is not None else None
        if "place" in st:
            v2_set_place(st["place"], move=False)
        elif "move" in st:
            v2_set_place(st["move"], move=True)
        elif "scene" in st:
            v2_set_scene(st["scene"])
        elif "music" in st:
            renpy.music.play("assets/%s.mp3" % st["music"], channel="music", fadein=0.6, if_changed=True)
        elif "loop" in st:
            renpy.music.play("assets/ms14-audio/cart-roll-light.mp3", channel="ride", relative_volume=0.2)
            renpy.music.play("assets/sfx-carriage-hooves.wav", channel="hooves", relative_volume=0.18)
        elif "loop_stop" in st:
            renpy.music.stop(channel="ride", fadeout=0.35)
            renpy.music.stop(channel="hooves", fadeout=0.35)
        elif "get" in st:
            v2_get(st["get"])
        elif "set" in st:
            for k, val in st["set"].items():
                store.v2_vals[k] = val
        elif "add" in st:
            for k, val in st["add"].items():
                store.v2_vals[k] = (store.v2_vals.get(k) or 0) + val
        elif "if" in st:
            branch = "then" if v2_cond(st["if"]) else "else"
            if bid is not None:
                v2_push("%s/%d/%s" % (bid, frame[1] - 1, branch))
            else:
                v2_push_steps(st.get(branch, []))
        elif "goto" in st:
            v2_goto(st["goto"])
        elif "time" in st:
            store.v2_minutes += st["time"]
        elif "period" in st:
            store.v2_period = st["period"]
            v2_show_bg()
        elif "mark_read" in st:
            store.v2_vals["read:" + st["mark_read"]] = True
        elif "meeting" in st:
            store.v2_vals["meeting:" + st["meeting"][0]] = st["meeting"][1]
        elif "retry" in st:
            v2_retry(st["retry"])
        elif "run_option" in st:
            v2_run_option(st["run_option"][0], st["run_option"][1])
        else:
            raise Exception("알 수 없는 단계: %r" % (st,))

    # ---- 장소·장면·자료 ----
    def v2_set_place(place, move):
        store.v2_loc = place
        store.v2_fig = None
        renpy.scene()
        v2_show_bg()
        renpy.with_statement(Dissolve(0.8) if place in ("black", "carriage") else Dissolve(0.3))

    def v2_place_art(place):
        spec = V2_LAYOUT["places"].get(place)
        if not spec:
            return None
        art = spec["art"]
        key = str(store.v2_period)
        return "assets/" + art.get(key, art["0"])

    # 장소 좌표는 월드 좌표다. 넓은 그림을 줄여 그리는 장소(입구 0.75, 지금 판 room13_wide_gate.rpy)는
    # 화면 = (월드 - 카메라) x 배율. 카메라 값도 월드 좌표로 저장한다.
    def v2_place_spec(place=None):
        return V2_LAYOUT["places"].get(place or store.v2_loc) or {}

    def v2_zoom(place=None):
        return float(v2_place_spec(place).get("zoom", 1.0))

    def v2_cam_range(place=None):
        spec = v2_place_spec(place)
        return max(0, int(spec.get("width", 1280) - 1280.0 / v2_zoom(place)))

    def v2_cam_x(place=None):
        place = place or store.v2_loc
        spec = v2_place_spec(place)
        x = store.v2_cam.get(place, spec.get("initial_x", 0))
        return max(0, min(x, v2_cam_range(place)))

    def v2_show_bg():
        place = store.v2_loc
        if place == "black":
            renpy.show("v2bg", what=Solid("#000"))
            return
        art = v2_place_art(place)
        if place == "carriage":
            renpy.show("v2bg", what=Fixed(art, v2_carriage_snow(), xysize=(1280, 720)))
            return
        # 그림은 장소 폭(월드)에 맞춰 늘이고 배율을 곱해 그린다(지금 판 r13_world_background 와 같이 최근접).
        spec = v2_place_spec(place)
        w, h = spec.get("art_size", (spec.get("width", 1280), 720))
        z = v2_zoom(place)
        renpy.show("v2bg", what=Transform(art, size=(int(w * z), int(h * z)), nearest=True,
                                         xpos=-int(round(v2_cam_x(place) * z))))

    def v2_carriage_snow():
        # 마차 창에만 눈이 내린다(창 가림 그림을 쓴다, 지금 판 R13_COACH_SNOW 와 같은 뜻).
        snow = SnowBlossom(Solid("#ffffffd0", xysize=(3, 3)), count=60, border=40, xspeed=(-20, -60), yspeed=(60, 120), start=0)
        return AlphaMask(snow, "assets/room13-fx-carriage-window-mask.webp")

    def v2_pan(direction):
        # 지금 판 r13_pan_camera 처럼 화살표 한 번에 그 쪽 끝까지 간다(장소는 두 구역).
        store.v2_cam[store.v2_loc] = v2_cam_range() if direction > 0 else 0
        v2_show_bg()
        renpy.restart_interaction()

    def v2_focus_camera(gate_id):
        """대기에 닿으면 할 일(첫 선택지의 대상, 이동 차례면 출구) 쪽으로 카메라를 돌린다."""
        gate = V2_GATES[gate_id]
        place = gate["place"]
        spec = v2_place_spec(place)
        target = None
        if gate.get("travel"):
            target = spec.get("exit_x")
        for i, o in v2_gate_options(gate_id):
            if target is not None:
                break
            if o.get("obj"):
                r = spec.get("objects", {}).get(o["obj"][0])
                if r:
                    target = r[0] + r[2] // 2
            elif o.get("person") in spec.get("people", {}):
                target = spec["people"][o["person"]][0]
        if target is not None:
            store.v2_cam[place] = max(0, min(int(target - 640 / v2_zoom(place)), v2_cam_range(place)))
            v2_show_bg()

    def v2_set_scene(scene):
        store.v2_scene = scene
        spec = V2_SCENES[scene]
        renpy.music.play("assets/%s.mp3" % spec["music"], channel="music", fadein=0.6, if_changed=True)
        amb = "assets/amb-%s.mp3" % spec["ambience"]
        renpy.music.play(amb, channel="amb", fadein=1.0, if_changed=True, relative_volume=0.5)

    def v2_place_name(place=None):
        return V2_PLACES.get(place or store.v2_loc, {}).get("name", "")

    def v2_get(e):
        if e not in store.v2_ev:
            store.v2_ev.append(e)
            renpy.notify(V2_EVIDENCE[e]["name"])

    def v2_owned_newest():
        return list(reversed(store.v2_ev))

    # ---- 생각(목표 한 문장) ----
    def v2_goal():
        gate = V2_GATES.get(store.v2_gate) if store.v2_gate else None
        base = (gate or {}).get("goal") or (V2_SCENES.get(store.v2_scene) or {}).get("goal") or ""
        if gate and gate.get("travel"):
            place = v2_place_name(gate["travel"])
            base = (base + " " if base else "") + V2_COMMON["ui"]["travel_goal"].format(place=place, ro=v2_josa(place, "로", "으로"))
        return base

    def v2_josa(word, without, with_final):
        ch = word[-1] if word else ""
        if u"가" <= ch <= u"힣":
            final = (ord(ch) - 0xAC00) % 28
            if without == "로" and final == 8:
                return "로"
            return with_final if final else without
        return without

    # ---- 대사 ----
    V2_CHARS = {}

    def v2_char(who):
        if who not in V2_CHARS:
            name = V2_PEOPLE[who]["name"] if who in V2_PEOPLE else None
            V2_CHARS[who] = Character(name, screen="say", callback=v2_say_callback)
        return V2_CHARS[who]

    def v2_say_callback(event, interact=True, **kwargs):
        if event == "end":
            V2Input.last = v2_clock.monotonic()

    def v2_plain_len(s):
        return len(re.sub(r"\{[^}]*\}", "", s))

    def v2_wrap(text, width):
        """문장마다 줄을 바꾸고, 한 줄이 width 자를 넘으면 띄어쓰기에서 자른다(지금 판 줄바꿈 규칙과 같은 뜻)."""
        rows = []
        parts = text.split("\n") if "\n" in text else re.split(r"(?<=[.?!…])((?:\{w=[0-9.]+\})?) +", text)
        if "\n" not in text:
            merged = []
            for i in range(0, len(parts), 2):
                merged.append(parts[i] + (parts[i + 1] if i + 1 < len(parts) else ""))
            parts = merged
        for part in parts:
            line = ""
            for word in part.split(" "):
                cand = (line + " " + word) if line else word
                if line and v2_plain_len(cand) > width:
                    rows.append(line)
                    line = word
                else:
                    line = cand
            if line:
                rows.append(line)
        return rows

    def v2_pages(text):
        width = {"small": 35, "normal": 31, "large": 27}.get(persistent.v2_text_size or "normal", 31)
        rows = v2_wrap(text, width)
        # 대사판 안에는 두 줄까지 들어간다. 세 줄째는 판 아래 테두리·단추 줄에 걸려(웹 캡처 2026-10-30) 다음 쪽으로 넘긴다.
        if len(rows) <= 2:
            return ["\n".join(rows)]
        return ["\n".join(rows[i:i + 2]) for i in range(0, len(rows), 2)]

    def v2_figure(who, e=None, pose=None):
        """대화 그림: 지금 판 대사 장면처럼 가까이(머리끝이 화면 위), 아이는 키만큼 낮게."""
        if store.v2_loc == "carriage":
            seat = (pose or "")[5:] if (pose or "").startswith("seat_") else V2_SEAT_OF.get(e or "neutral", "neutral")
            return Transform("assets/room13-carriage-daram-seat-%s.webp" % seat, zoom=3, xanchor=0.5, xpos=850, ypos=96)
        face = V2_FACE.get(e or "neutral", e or "neutral")
        fig = V2_LAYOUT["figure"]
        stature = fig["stature"].get(who, 1.0)
        drop = int(round(520 * (1 - min(1.0, stature))))
        top = int(fig["top"].get(who, 0) * fig["zoom"])
        return Transform("assets/dialogue-dot-v2/%s/760/%s.webp" % (who, face), zoom=fig["zoom"],
                         xanchor=0.5, xpos=fig["x"], ypos=fig["head_top"] - top + drop)

    def v2_show_figure(who, e=None, pose=None, fx=None):
        what = v2_figure(who, e, pose)
        at = [v2_jolt] if fx == "jolt" else []
        renpy.show("v2fig", what=what, at_list=at)
        store.v2_fig = who

    def v2_listener(frame):
        """아빠·지문 줄에는 이 묶음에서 다음에 말할 사람을 미리 세운다."""
        steps = v2_steps(frame)
        for st in steps[frame[1] + 1:frame[1] + 6]:
            if "t" not in st:
                break
            if st["who"] in V2_DRAWN:
                return st["who"]
        return None

    def v2_line_kind(st):
        who = st["who"]
        if who in ("card", "doc", "narr"):
            return who
        if who == "dad" and st["t"].startswith("("):
            return "thought"
        return "talk"

    def v2_do_line():
        frame, st = v2_current()
        who = st["who"]
        kind = v2_line_kind(st)
        if frame[2] == 0:
            # 화면 시험은 대사 글자가 아니라 줄 ID·장면·상태 값을 본다.
            if st.get("id") and st["id"] not in store.v2_trace:
                store.v2_trace.append(st["id"])
            if who in V2_DRAWN:
                if store.v2_fig != who or st.get("e") or st.get("pose") or st.get("fx") == "jolt" or store.v2_loc == "carriage":
                    v2_show_figure(who, st.get("e"), st.get("pose"), st.get("fx"))
                if who not in store.v2_met:
                    store.v2_met.append(who)
            elif kind == "doc":
                renpy.hide("v2fig")
                store.v2_fig = None
            elif store.v2_loc == "carriage" and store.v2_fig is None:
                v2_show_figure("daram")
            elif kind in ("talk", "narr") and store.v2_fig is None:
                nxt = v2_listener(frame)
                if nxt:
                    v2_show_figure(nxt)
            if st.get("cut"):
                renpy.show("v2cut", what=v2_cut(st["cut"]))
            else:
                renpy.hide("v2cut")
            if st.get("fx") == "flash":
                renpy.with_statement(Fade(0.08, 0.0, 0.25, color="#fff"))
            elif st.get("fx") == "slam":
                renpy.with_statement(vpunch)
        store.v2_line = kind
        store.v2_stage = v2_stage_band() if kind != "doc" else None
        pages = v2_pages(st["t"])
        page = min(frame[2], len(pages) - 1)
        speaker = who if kind in ("talk", "thought") else None
        if kind == "card":
            renpy.say(None, pages[page])
        else:
            renpy.say(v2_char(speaker) if speaker else v2_char("narr"), pages[page])
        if page + 1 < len(pages):
            frame[2] = page + 1
        else:
            frame[1] += 1
            frame[2] = 0
            renpy.hide("v2cut")

    def v2_cut(key):
        path = "assets/evidence/%s.webp" % key
        return Transform(path, fit="contain", xysize=(420, 300), xalign=0.5, ypos=110)

    def v2_stage_band():
        stage = (V2_SCENES.get(store.v2_scene) or {}).get("stage")
        if not stage or store.v2_loc != "gate":
            return None
        return ("%s · %d일째" % (v2_place_name(), store.v2_day), "쟁점 · " + stage)

    # ---- 대기 관문(조사 화면) ----
    def v2_gate_options(gate_id):
        return [(i, o) for i, o in enumerate(V2_GATES[gate_id]["options"]) if v2_cond(o.get("when"))]

    def v2_wait_enter():
        frame, st = v2_current()
        gate = st["wait"]
        if store.v2_gate != gate:
            store.v2_gate = gate
            v2_focus_camera(gate)
        renpy.hide("v2fig")
        renpy.hide("v2cut")
        store.v2_fig = None
        store.v2_stage = None
        renpy.choice_for_skipping()

    def v2_field_people():
        """현장 인물: 도트 한 칸 = 화면 1px(장소 배율과 무관, 지금 판 room13_field_dot.rpy).
        발(월드 좌표)을 화면으로 옮기고 그림은 그 발에 세운다. 이름표는 머리 상자 위(지금 판 r13_actor_nameplates:
        높이 30, 머리와 8px 띄움, 폭은 글자 수대로, 화면 위 101 아래로는 내려가지 않음)."""
        gate = V2_GATES[store.v2_gate]
        spec = v2_place_spec()
        z = v2_zoom()
        cam = v2_cam_x()
        out = []
        for p in gate.get("people", []):
            pos = spec.get("people", {}).get(p)
            if not pos:
                continue
            pose = pos[2] if len(pos) > 2 else "neutral"
            dot = V2_LAYOUT["dots"]["%s/%s" % (p, pose)]
            left = int(round((pos[0] - cam) * z - dot["foot"][0]))
            top = int(round(pos[1] * z - dot["foot"][1]))
            hx, hy, hw, hh = dot["head"]
            name = V2_PEOPLE[p]["name"]
            tw = max(64, sum(7 if ch == " " else 16 for ch in name) + 18)
            th = 30
            tx = int(max(8, min(1280 - 8 - tw, left + hx + hw / 2.0 - tw / 2.0)))
            ty = max(101, int(top + hy) - th - 8)
            out.append(dict(who=p, img="assets/field-dot-v2/%s/%s.webp" % (p, pose), x=left, y=top,
                            w=dot["size"][0], h=dot["size"][1], tag=(tx, ty, tw, th)))
        return out

    def v2_field_objects():
        """이 장소에서 누를 수 있는 물건: 선택지가 가리키거나 관찰 글이 있는 것만."""
        spec = V2_LAYOUT["places"].get(store.v2_loc, {})
        rects = spec.get("objects", {})
        texts = V2_DAY["objects"].get(store.v2_loc, {})
        targets = {}
        for i, o in v2_gate_options(store.v2_gate):
            for key in o.get("obj") or []:
                targets.setdefault(key, o["title"])
        cam = v2_cam_x()
        z = v2_zoom()
        out = []
        for key, r in rects.items():
            if key in targets or key in texts:
                name = texts.get(key, {}).get("name") or targets.get(key, key)
                out.append((key, int((r[0] - cam) * z), int(r[1] * z), int(r[2] * z), int(r[3] * z), name))
        # 겹친 물건은 작은 것을 위에 둔다(큰 칸이 작은 물건을 덮어 누를 수 없게 되지 않게).
        out.sort(key=lambda o: -o[3] * o[4])
        return out

    def v2_field_data():
        """조사 화면 한 번 그릴 때 필요한 값(이 시간을 잰다: dev/measure)."""
        return dict(people=v2_field_people(), objects=v2_field_objects(), goal=v2_goal(),
                    cam=v2_cam_x(), cam_range=v2_cam_range())

    def v2_run_option(gate_id, index):
        o = V2_GATES[gate_id]["options"][index]
        store.v2_vals["read:opt:%s:%d" % (gate_id, index)] = True
        if o.get("person"):
            store.v2_vals["talked:%s:%s" % (store.v2_scene, o["person"])] = True
            proof = any("proof" in st for st in o["do"])
            store.v2_reopen = None if (proof or o.get("direct") or o.get("present")) else [gate_id, o["person"]]
        store.v2_ui = None
        v2_push("g:%s/%d" % (gate_id, index))

    def v2_click_person(p):
        for i, o in v2_gate_options(store.v2_gate):
            if o.get("person") == p and o.get("direct"):
                v2_run_option(store.v2_gate, i)
                return
        if v2_has_business(p, store.v2_gate):
            store.v2_ui = ["topics", p]
        else:
            v2_push_steps(v2_idle_lines(p))

    def v2_reaction(p, e):
        for r in V2_DAY["reactions"]:
            if r["person"] == p and r["ev"] == e:
                return r
        return None

    def v2_has_business(p, gate_id):
        for i, o in v2_gate_options(gate_id):
            if o.get("person") == p:
                return True
        for f in v2_followups(p):
            if not store.v2_vals.get("read:" + f["id"]):
                return True
        for r in V2_DAY["reactions"]:
            if r["person"] == p and v2_has(r["ev"]) and not store.v2_vals.get("reacted:%s:%s" % (p, r["ev"])):
                return True
        return False

    def v2_followups(p):
        return [f for f in V2_DAY["followups"] if f["person"] == p and v2_has(f["after"])]

    def v2_topics(p):
        """질문 목록: 그 사람에게 하는 말만(제시로만 내는 선택지는 넣지 않는다)."""
        rows = []
        for i, o in v2_gate_options(store.v2_gate):
            if o.get("person") == p and not o.get("present_only") and not o.get("direct"):
                read = bool(store.v2_vals.get("read:opt:%s:%d" % (store.v2_gate, i)))
                rows.append(dict(title=o["title"], key=("opt", i), read=read and o.get("remember_read", False), new=False))
        for f in v2_followups(p):
            read = bool(store.v2_vals.get("read:" + f["id"]))
            rows.append(dict(title=f["title"], key=("follow", f["id"]), read=read, new=not read))
        return rows

    def v2_pick_topic(p, key):
        if key[0] == "opt":
            v2_run_option(store.v2_gate, key[1])
        else:
            store.v2_vals["read:" + key[1]] = True
            store.v2_ui = None
            store.v2_reopen = [store.v2_gate, p]
            v2_push("f:" + key[1])

    def v2_present_to(p, e):
        """자료 제시: 이 사람·이 장소의 제시 선택지가 먼저, 아니면 반응, 일반 답, 아빠 속말."""
        for i, o in v2_gate_options(store.v2_gate):
            if o.get("person") == p and o.get("present") == e:
                v2_run_option(store.v2_gate, i)
                return
        store.v2_ui = None
        store.v2_reopen = [store.v2_gate, p]
        r = v2_reaction(p, e)
        if r:
            store.v2_vals["reacted:%s:%s" % (p, e)] = True
            v2_push_steps(r["lines"])
            return
        seed = sum(ord(c) for c in e)
        generic = V2_COMMON["present_generic"].get(p)
        if generic:
            g = generic[seed % len(generic)]
            v2_push_steps([dict(who=p, t=g["t"])])
            return
        nothing = V2_COMMON["present_nothing"]
        v2_push_steps([dict(who="dad", t=nothing[seed % len(nothing)])])

    def v2_idle_lines(p):
        """할 말이 없는 사람: 방금 이야기 → 첫 만남 → 그날 첫 인사 → 아빠 속말 돌림."""
        person = V2_PEOPLE.get(p, {})
        if store.v2_vals.get("talked:%s:%s" % (store.v2_scene, p)):
            rows = [dict(who="dad", t=V2_COMMON["just_talked"])]
            goal = v2_goal()
            if goal:
                rows.append(dict(who="dad", t="(" + goal + ")"))
            return rows
        greeted = "greeted:%d:%s" % (store.v2_day, p)
        if not store.v2_vals.get(greeted):
            store.v2_vals[greeted] = True
            if p not in store.v2_met and person.get("first"):
                return person["first"]
            if person.get("daily"):
                return person["daily"]
        n = store.v2_vals.get("idle_count") or 0
        store.v2_vals["idle_count"] = n + 1
        thoughts = V2_COMMON["idle_thoughts"]
        return [dict(who="dad", t=thoughts[n % len(thoughts)])]

    def v2_click_object(key):
        place = store.v2_loc
        matches = [(i, o) for i, o in v2_gate_options(store.v2_gate) if key in (o.get("obj") or [])]
        spec = V2_DAY["objects"].get(place, {}).get(key, {})
        if len(matches) == 1:
            v2_run_option(store.v2_gate, matches[0][0])
            return
        if len(matches) > 1:
            name = spec.get("name", key)
            prompt = dict(who="dad", t=V2_COMMON["ui"]["object_menu"].format(name=name))
            items = [dict(t=o["title"], do=[{"run_option": [store.v2_gate, i]}]) for i, o in matches]
            v2_push_steps([prompt, {"menu": items}])
            return
        read = spec.get("read")
        if read and v2_cond(read.get("when")):
            v2_push("o:%s/%s" % (place, key))
            return
        if "ev" in spec:
            if v2_has(spec["ev"]):
                v2_push_steps([dict(who="doc", t=V2_EVIDENCE[spec["ev"]]["text"])])
            else:
                v2_push_steps([dict(who="dad", t="(" + spec["before"] + ")")])
            return
        if "look" in spec:
            rows = [dict(who="dad", t="(" + spec["look"] + ")")]
            chat_key = "chat:%d:%d" % (store.v2_day, store.v2_period)
            if spec.get("chat") and (store.v2_vals.get(chat_key) or 0) < 4:
                store.v2_vals[chat_key] = (store.v2_vals.get(chat_key) or 0) + 1
                rows += spec["chat"]
            v2_push_steps(rows)

    def v2_map_places():
        """갈 수 있는 곳: 지금 장소 + 이 대기의 이동 선택지 장소."""
        out = [store.v2_loc]
        for i, o in v2_gate_options(store.v2_gate):
            if o.get("move") and o["move"] not in out:
                out.append(o["move"])
        return out

    def v2_map_go(dest):
        if dest == store.v2_loc:
            return
        for i, o in v2_gate_options(store.v2_gate):
            if o.get("move") == dest:
                v2_run_option(store.v2_gate, i)
                return

    def v2_map_locked_text(dest):
        name = v2_place_name(dest)
        gate = V2_GATES.get(store.v2_gate) or {}
        if gate.get("travel"):
            return V2_COMMON["ui"]["locked_travel"].format(place=name, eun=v2_josa(name, "는", "은"), dest=v2_place_name(gate["travel"]))
        return V2_COMMON["ui"]["locked"].format(place=name)

    def v2_field_result(res):
        kind = res[0]
        if kind == "person":
            v2_click_person(res[1])
        elif kind == "object":
            v2_click_object(res[1])
        elif kind == "map":
            v2_map_go(res[1])

    def v2_ui_result(res):
        kind = res[0]
        p = store.v2_ui[1]
        if kind == "topic":
            v2_pick_topic(p, res[1])
        elif kind == "present":
            store.v2_ui = ["present", p]
        elif kind == "show":
            v2_present_to(p, res[1])
        elif kind == "back_topics":
            store.v2_ui = ["topics", p]
        else:
            store.v2_ui = None

    # ---- 고르기(메뉴) ----
    def v2_menu_items(st):
        frame = store.v2_stack[-1]
        out = []
        for j, item in enumerate(st["menu"]):
            if v2_cond(item.get("when")):
                bid = "%s/%d/m%d" % (frame[0], frame[1], j) if frame[0] is not None else None
                out.append((item["t"], bid if bid else item.get("do", [])))
        return out

    def v2_push_any(target):
        if isinstance(target, list):
            v2_push_steps(target)
        else:
            v2_push(target)

    def v2_menu_choose(index):
        frame, st = v2_current()
        items = v2_menu_items(st)
        frame[1] += 1
        v2_push_any(items[index][1])

    # ---- 증명(회의·대조) ----
    def v2_proof_id():
        return v2_current()[1]["proof"]

    def v2_proof_won(proof, chosen):
        chosen = set(chosen)
        extras = set(proof.get("extras", []))
        return any(set(c) <= chosen and chosen <= set(c) | extras for c in proof["correct"])

    def v2_proof_kept(proof, chosen):
        """틀리면 맞는 쪽 자료만 남긴다. 덧붙임을 뺀 수가 정답 수보다 많으면 전부 걷는다(전부 내기 방지)."""
        right = set()
        for c in proof["correct"]:
            right |= set(c)
        extras = set(proof.get("extras", []))
        core = [e for e in chosen if e not in extras]
        if len(core) > max(len(c) for c in proof["correct"]):
            return []
        return [e for e in chosen if e in right]

    def v2_proof_prepare(pid):
        """증명 화면에 들어갈 때: 앞서 틀린 제출에서 남긴 맞는 자료를 골라 둔다. 짚어 보기 뒤 다시 열 때는 그대로."""
        if store.v2_pick_for != pid:
            store.v2_pick_for = pid
            store.v2_pick = list(store.v2_kept.get(pid, []))
            store.v2_pair = False

    def v2_toggle_pick(e):
        if e in store.v2_pick:
            store.v2_pick.remove(e)
        else:
            store.v2_pick.append(e)
        renpy.restart_interaction()

    def v2_pair_ready(pid):
        obs = V2_PROOFS[pid].get("observe")
        return bool(obs) and sorted(store.v2_pick) == sorted(obs["pair"])

    def v2_proof_result(res):
        frame, st = v2_current()
        pid = st["proof"]
        proof = V2_PROOFS[pid]
        kind = res[0]
        if kind != "observe":
            store.v2_pick_for = None
        if kind == "submit":
            chosen = list(res[1])
            if not chosen:
                return
            store.v2_chosen = chosen
            won = v2_proof_won(proof, chosen)
            store.v2_kept[pid] = [] if won else v2_proof_kept(proof, chosen)
            store.v2_vals["proof_given:" + pid] = ",".join(chosen)
            frame[1] += 1
            for i, o in enumerate(proof["outcomes"]):
                if v2_cond(o["when"], won=won):
                    v2_push("p:%s/o%d" % (pid, i))
                    return
        elif kind in ("press", "investigate"):
            frame[1] += 1
            v2_push("p:%s/%s" % (pid, kind))
        elif kind == "observe":
            v2_push("p:%s/spot:%s" % (pid, res[1]))

    def v2_retry(meeting):
        key = "tries:" + meeting
        store.v2_vals[key] = (store.v2_vals.get(key) or 0) + 1
        store.v2_vals[meeting + "_wrong_pending"] = True
        proof = next(p for p in V2_PROOFS.values() if p.get("meeting") == meeting)
        pid = next(k for k, p in V2_PROOFS.items() if p.get("meeting") == meeting)
        renpy.notify(proof["notify_kept"] if store.v2_kept.get(pid) else proof["notify_wrong"])

    # ---- 입력: 대사를 넘긴 직후 다시 뜬 화면이 같은 손의 다음 누름을 받지 않게(지금 판 0.6초 규칙) ----
    def v2_input_wait():
        left = 0.6 - (v2_clock.monotonic() - V2Input.last)
        return max(0.0, left)

    # ---- 시간 재기(비교 표용). 화면 시험이 부른다. ----
    def v2_measure_field(n=200):
        t0 = v2_clock.perf_counter()
        for i in range(n):
            v2_field_data()
        return (v2_clock.perf_counter() - t0) * 1000.0 / n

    # 대사를 넘긴 시각은 저장하지 않는다(벽시계 값이라 저장에 들어가면 안 된다). 클래스 속성은 저장되지 않는다.
    class V2Input(object):
        last = 0.0

transform v2_jolt:
    yoffset 0
    easein 0.06 yoffset -14
    easeout 0.1 yoffset 0

default v2_vals = {}
default v2_ev = []
default v2_met = []
default v2_loc = "black"
default v2_day = 1
default v2_period = 0
default v2_minutes = 0
default v2_scene = None
default v2_gate = None
default v2_ui = None
default v2_reopen = None
default v2_cam = {}
default v2_fig = None
default v2_kept = {}
default v2_chosen = []
default v2_goal_seen = ""
default v2_ended = False
default v2_stack = []
default v2_trace = []
default persistent.v2_last_end = None
default v2_line = "talk"
default v2_next = None
default v2_pick = []
default v2_pick_for = None
default v2_pair = False
default v2_stage = None
default persistent.v2_text_size = "normal"
