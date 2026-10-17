# 0.19.8: a save made inside a call keeps the call's generated return-site name. When a release renamed
# it, loading the save stopped with "Could not find return label". Ren'Py now drops the stale call stack
# and comes here. A save whose rollback log has no statement left at all (load_failed) comes here too.
# The scene in progress is lost; the run itself (day, records, flags) is kept and resumes at the next
# safe point: the day router for ordinary days (trial day goes to the trial, week 2 to its own router),
# the altar hub during the finale, a new start for the first-day opening, the main menu after an ending.
define config.return_not_found_label = "r13_return_lost"
define config.load_failed_label = "r13_return_lost"

label r13_return_lost:
    window hide
    python:
        # Meeting and scene state that only lives while its scene runs.
        for _r13_n in ("r13_meeting_active","r13_meeting_intro","r13_meeting_interrupting","r13_meeting_replaying",
                "r13_meeting_live_active","r13_cg_active","r13_conv_skip"):
            setattr(store,_r13_n,False)
        r13_meeting_pending_resume=None
        r13_scene_key=None
        for _r13_n in ("r13_material_corner","r13_meeting_cut_in","r13_meeting_rebuttal_hold","r13_rebuttal_cutin","r13_book","r13_calendar"):
            renpy.hide_screen(_r13_n)
        r13_cutin_music_pause(False)
    if not (room13_mode and isinstance(room13, dict) and room13.get("day") and room13.get("location") in R13_PLACES) or room13.get("ending"):
        $ renpy.full_restart()
    if "E01" not in room13.get("evidence",[]):
        jump room13_start
    $ renpy.notify("이전 판의 저장이라 하던 장면을 이어 갈 수 없어 가까운 곳에서 다시 시작했어요.")
    show screen r13_hud
    if room13.get("finale_started"):
        call r13_scene("r13_altar","북쪽 산길 끝 · 숲속 제단","hearing")
        jump r13_final_hub
    jump r13_day
