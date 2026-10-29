# 2026-10-29 소유자 「화면 클릭부터 좌우 이동 모두 다 렉 걸려」.
# 조사 화면 한 번 그릴 때 r13_stage_people(17층)을 네 번 불렀다(화면 본체·물건 겹침·생활 묶음·이벤트 제안).
# 한 번에 약 47ms(PC 네이티브)라 화면을 다시 계산할 때마다 200ms 가까이 들었고, 웹(wasm)에서는 몇 배가 된다.
# 화면 갱신 한 번(interact_core 한 바퀴) 안·같은 상태에서는 결과가 같으므로 한 번만 계산한다.
# 상태는 r13_edit·r13_flag·r13_v111_set 이 room13 을 통째로 새 dict 로 바꾸므로 id(room13) 가 바뀌면 다시 잰다.
# 다른 변수(SetVariable 등)가 바뀌면 Ren'Py 가 갱신을 다시 시작하고 interact_callbacks 가 불리므로 그때도 다시 잰다.
init 341 python:
    _r13_stage_cache_inner = r13_stage_people
    _r13_stage_cache = {}
    _r13_stage_round = [0]

    def _r13_stage_next_round():
        _r13_stage_round[0] += 1

    config.interact_callbacks.append(_r13_stage_next_round)

    def r13_stage_people(entry=False):
        state = store.room13
        frame = (_r13_stage_round[0], id(state), state.get("location") if state else None)
        if _r13_stage_cache.get("frame") != frame:
            _r13_stage_cache["frame"] = frame
            _r13_stage_cache["values"] = {}
        values = _r13_stage_cache["values"]
        if bool(entry) not in values:
            values[bool(entry)] = _r13_stage_cache_inner(entry)
        value = values[bool(entry)]
        # 부르는 쪽이 목록을 고쳐도 다음 사람에게 번지지 않게 겉 목록은 새로 준다.
        return list(value) if isinstance(value, list) else value

    # 이름표 자리 찾기(r13_actor_nameplates)는 사람마다 후보 37칸 × 얼굴·이름표·화면 단추 겹침을 재서 한 번에 약 30ms 다.
    # 결과는 사람 자리·화면 위치·확대·화면 단추·물건 자리만으로 정해지므로, 그 값이 같으면 앞 결과를 다시 쓴다.
    _r13_nameplates_inner = r13_actor_nameplates
    _r13_nameplates_cache = {}

    def r13_actor_nameplates(actors):
        try:
            key = (tuple((a["person"], tuple(a["rect"]), a.get("pose"), a.get("x"), a.get("y"), a.get("width"), a.get("life_group"),
                          tuple((a.get("dot") or {}).get("head") or ())) for a in actors),
                   r13_world_offset(), r13_field_zoom(), r13_touch_ui(), r13_view_width(), r13_world_width(),
                   tuple(tuple(r) for r in r13_field_ui_rects(0)),
                   tuple(tuple(o) for o in (r13_nameplate_obstacles() if "r13_nameplate_obstacles" in globals() else [])),
                   tuple(g["id"] for g in getattr(store, "R13_LIFE_GROUPS", [])))
            hash(key)
        except Exception:
            return _r13_nameplates_inner(actors)
        if _r13_nameplates_cache.get("key") != key:
            _r13_nameplates_cache["key"] = key
            _r13_nameplates_cache["value"] = _r13_nameplates_inner(actors)
        return [dict(p) for p in _r13_nameplates_cache["value"]]
