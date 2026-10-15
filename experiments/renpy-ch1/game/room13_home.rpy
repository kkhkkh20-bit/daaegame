# Home review never spends time. Only explicit sleep advances the date.
init 79 python:
    def r13_home_with_daram():
        s=store.room13 or {}
        return s.get("location") in ("room13","guestroom") and s.get("daram_state") in ("with_dad","rescued") and "lodging" in s.get("flags",[])

    R13_GREETING["daram"]="아빠, 여기서 같이 볼까?"
    R13_CORE_PEOPLE.add("daram")
    _r13_home_where=r13_where
    def r13_where(person):
        if person=="daram":return store.room13["location"] if r13_home_with_daram() else None
        return _r13_home_where(person)

    R13_STAGE_POSITIONS[("daram","room13")]=(835,674,262)
    R13_STAGE_POSITIONS[("daram","guestroom")]=(835,674,262)
    ROOM13["topics"]["home:records"]=dict(npc="daram",title="오늘 찾은 걸 같이 볼까?",day=[1,14],need=["lodging"],give=[],flags=[],lines=[("daram","응. 나도 내가 본 걸 말해 줄게.")])
    _r13_home_topics=r13_topics
    # 0.18.21 (owner): the "look at today's finds together" topic is retired; the 기록 button does this.
    def r13_topics(person):
        return [(key,spec) for key,spec in _r13_home_topics(person) if key!="home:records"]
