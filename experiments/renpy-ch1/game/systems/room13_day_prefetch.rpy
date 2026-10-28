# 2026-10-28 소유자 「처음에 에셋 통째로 로딩하게 하지 말고, 분기를 나누고 그때마다 필요한 것을 로딩」.
# 웹판은 쓸 때 받는다(Ren'Py 점진 내려받기). 날짜가 바뀌면 그날과 다음 날 대본에 나오는 인물 그림·장소 배경을
# 뒤에서 미리 받아 두라고 페이지(window.r13PrefetchDay, dev/build_web.py)에 알린다. 목록은 빌드가 만든다(by_day).
# 데스크톱·화면 시험에서는 아무것도 하지 않는다.
init 900 python:
    def r13_day_prefetch(day):
        if not renpy.emscripten or not day:return
        try:
            import emscripten
            emscripten.run_script("window.r13PrefetchDay&&(r13PrefetchDay(%d),r13PrefetchDay(%d))"%(int(day),int(day)+1))
        except Exception:
            pass
    def _r13_day_prefetch_check():
        state=getattr(store,"room13",None) or {}
        day=state.get("day")
        if day and day!=getattr(store,"r13_day_prefetched",None):
            store.r13_day_prefetched=day
            r13_day_prefetch(day)
    config.interact_callbacks.append(_r13_day_prefetch_check)

default r13_day_prefetched = None
