# 0.18.91 편의성 (2026-10-17 개선점 조사 1묶음). 화면 모양은 바꾸지 않는다.
# - 하루를 시작할 때와 회의 직전에 자동저장(r13_debate_run이 r13_autosave_now를 부른다).
# - 잠들기 확인창이 오늘 놓치게 될 일의 개수만 알려 준다(어디인지는 말하지 않는다).
# - 지도에서 고른 장소를 한 번 더 누르면 바로 이동한다.
init 165 python:
    def r13_autosave_now():
        if renpy.is_skipping() and getattr(store,"r13_conv_skip",False):return
        try:renpy.force_autosave(take_screenshot=False,block=False)
        except Exception:pass

    _r13_conv_next_day=r13_next_day
    def r13_next_day():
        _r13_conv_next_day()
        r13_autosave_now()

    def r13_sleep_missed_counts():
        s=store.room13 or {}
        day=s.get("day")
        waiting=[k for k,o in s.get("offers",{}).items() if k in R13_EVENT_OFFERS and o.get("day")==day]
        tonight=r13_evening_missions() if s.get("period")==2 else []
        return len(tonight),len(waiting)

    _r13_conv_sleep_text=r13_learning_sleep_text
    def r13_learning_sleep_text():
        text="\n".join(line for line in _r13_conv_sleep_text().split("\n") if line.strip())
        tonight,waiting=r13_sleep_missed_counts()
        if tonight:text+="\n오늘 밤에만 할 수 있는 일이 아직 %d개 남아 있다."%tonight
        if waiting:text+="\n지금 지나치면 결과만 전해 듣게 될 일이 %d개 있다."%waiting
        return text

    def r13_map_pick(key,selected):
        """First press selects a place; pressing the selected place again travels there."""
        if key==selected and key!=store.room13.get("location") and key in r13_places():
            return Return(key)
        return SetScreenVariable("selected",key)

# 0.18.91 연출: 이야기 장면(지도 위치와 다른 배경) 중에는 왼쪽 위에 장면 제목을 보인다.
default r13_scene_bg = None

init 165 python:
    def r13_hud_place():
        title=getattr(store,"place",None) or ""
        if title=="마차 안":return title
        loc=(store.room13 or {}).get("location")
        bg=getattr(store,"r13_scene_bg",None)
        if title and bg and loc in R13_PLACES and R13_PLACES[loc][1]!=bg:
            return title
        return r13_location_path().replace("마을 › ","",1)

# 0.19.2 (owner: "광장에 도착하기도 전에 피코가 대사를 친다"): a scene that fires on arrival plays
# before the hub draws the new place, so the last scene's picture (e.g. the gate) was still up.
# Arrival-triggered scenes call this first to stand in the place they belong to.
label r13_here_scene:
    $ _r13_here=R13_PLACES.get(room13["location"])
    if _r13_here and r13_scene_bg!=_r13_here[1]:
        call r13_scene(_r13_here[1],_r13_here[0],"calm")
    return
