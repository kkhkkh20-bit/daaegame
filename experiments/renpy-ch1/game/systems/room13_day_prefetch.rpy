# 2026-10-28 소유자 「처음에 에셋 통째로 로딩하게 하지 말고, 분기를 나누고 그때마다 필요한 것을 로딩」.
# 웹판은 쓸 때 받는다(Ren'Py 점진 내려받기). 날짜가 바뀌면 그날 대본에 나오는 인물 그림·장소 배경을
# 뒤에서 미리 받아 두라고 페이지(window.r13PrefetchDay, dev/build_web.py)에 알린다. 목록은 빌드가 만든다(by_day).
# 2026-11-05: 현재 날짜만 알린다. 다음 날까지 겹쳐 받던 요청은 없애고 로더의 전역 유휴 대기열에 맡긴다.
# 데스크톱·화면 시험에서는 아무것도 하지 않는다.
init 900 python:
    def r13_day_prefetch(day):
        if not renpy.emscripten or not day:return
        try:
            import emscripten
            emscripten.run_script("window.r13PrefetchDay&&r13PrefetchDay(%d)"%int(day))
        except Exception:
            pass
    def _r13_day_prefetch_check():
        state=getattr(store,"room13",None) or {}
        day=state.get("day")
        if day and day!=getattr(store,"r13_day_prefetched",None):
            store.r13_day_prefetched=day
            r13_day_prefetch(day)
    config.interact_callbacks.append(_r13_day_prefetch_check)

    def _r13_day_prefetch_after_load():
        # 저장 속 예열 표시를 브라우저의 실제 다운로드 상태로 오인하지 않는다.
        store.r13_day_prefetched=None

    config.after_load_callbacks.append(_r13_day_prefetch_after_load)

default r13_day_prefetched = None
