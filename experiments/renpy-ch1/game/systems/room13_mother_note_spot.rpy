# Day 1 in 13호 (owner, 0.18.22): the mother's memo was only reachable by opening the desk case and
# then pressing "접힌 메모와 편지" inside it, so players stood in the room not knowing what to do.
# The folded paper on the desk is now its own spot in the room; it disappears once M01 is read.
# The desk case and its puzzle are unchanged.
init 129 python:
    ROOM13["objects"]["room13"]["mother_note"]=dict(rect=[138,378,104,36],text="책상 위에 접힌 종이가 있다.",
        need=["lodging"],give=[],flags=[],mother_note_spot=True)
    R13_OBJECT_NAMES["mother_note"]="책상 위 접힌 종이"

    _r13_note_spot_visible=r13_object_visible
    def r13_object_visible(spec):
        if spec.get("mother_note_spot"):
            s=store.room13 or {}
            return bool(s.get("life_poc")) and s.get("location")=="room13" and not r13_has("M01")
        # 0.18.56 (owner): the brought letter lies under the folded memo; offer it once the memo is read.
        if spec is ROOM13["objects"].get("room13",{}).get("letters") and (store.room13 or {}).get("life_poc") and not r13_has("M01"):
            return False
        return _r13_note_spot_visible(spec)

    _r13_note_spot_goal=r13_intro_goal
    def r13_intro_goal():
        s=store.room13 or {}
        if s.get("life_poc") and s.get("day")==1 and r13_has("lodging") and s.get("location")=="room13":
            if not r13_has("M01"):return "엄마가 머물던 방 · 책상 위에 접힌 종이가 있다"
            if not r13_has("E03"):return "엄마가 머물던 방 · 침대도 살펴보자"
            return "오늘은 여기까지 · 침대를 눌러 잠자리에 들자"
        return _r13_note_spot_goal()
