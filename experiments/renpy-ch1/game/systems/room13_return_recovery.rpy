# 0.19.7: a save made inside a call keeps the call's generated return-site name. When a release renamed
# it, loading the save stopped with "Could not find return label". Ren'Py now drops the stale call stack
# and comes here: back to the current place in Room13, or the main menu for anything else.
define config.return_not_found_label = "r13_return_lost"

label r13_return_lost:
    window hide
    if isinstance(room13, dict) and room13.get("day") and room13.get("location") in R13_PLACES:
        $ renpy.notify("이전 판의 저장이라 하던 장면을 이어 갈 수 없어 지금 있던 곳으로 돌아왔어요.")
        jump r13_roam
    $ renpy.full_restart()
