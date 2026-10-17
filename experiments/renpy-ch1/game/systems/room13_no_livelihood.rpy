# 0.18.91 일거리·숙박비·외상 없애기 (소유자 2026-10-17: "필요없으면 빼도 돼. 상점 돈을 얻을 방법이 애매해서")
# - 하루가 지나도 숙박비를 받지 않는다. 일거리(식사 준비·배달·수리·낚시·사냥)는 열리지 않는다.
# - 돈: 2일 아침 집에서 가져온 노잣돈 15냥 + 회의에서 진실을 밝히면 주민들이 모아 주는 사례 10냥.
#   그 밖의 기존 수입(백 부인·모모 심부름 등)은 그대로 둔다. 상점은 은호네 그대로.
# - 일을 해야만 열리던 것은 대화로 연다: 나비·까로가 본 엄마 이야기(J04·J05), 부리의 작업칼.
init 168 python:
    R13_TRAVEL_MONEY = 15
    R13_MEETING_REWARD = 10

    _r13_nolive_topics=r13_topics
    def r13_topics(person):
        return [(k,s) for k,s in _r13_nolive_topics(person) if not k.startswith("job:")]

    R13_BORROW["knife"]["need"]=[]
    for _key in ("life:nabi","life:buri"):
        if _key in ROOM13["topics"]:ROOM13["topics"][_key]["need"]=[]

    ROOM13["topics"]["life:karo"]["lines"]=[
        ("dad","그럼 마차는 언제 다시 출발합니까?"),
        ("karo","바퀴 축도 고쳐야 하고, 고개를 넘는 정기 마차도 겨울에는 쉬어요. 그래서 제 마차로는 당장 돌아가실 수 없습니다."),
        ("dad","하루 이틀만 머물 생각이었는데……. 고개 말고 다른 길 사정도 아십니까?"),
        ("karo","다른 길은 직접 알아보셔야 해요. 제가 다니던 고개 길과는 사정이 다르거든요."),
        ("karo","필요한 물건은 장터 은호 사장네서 살 수 있어요. 이 마을은 서로 도우면 꼭 갚는 데라, 일을 풀어 주시면 사례도 들어올 거예요."),
        ("dad","아내 소식부터 알아보겠습니다."),
        ("karo","그러세요. 누구네 짐인지는 꼭 짐표와 같이 확인하고요.")]

    _r13_nolive_next_day=r13_next_day
    def r13_next_day():
        _r13_nolive_next_day()
        if store.room13.get("day")==2 and not r13_has("travel_money"):
            r13_flag("travel_money")
            r13_cash(R13_TRAVEL_MONEY,"집에서 가져온 노잣돈")

    # 회의에서 진실을 밝히면 주민들이 등불값을 모아 건넨다. 한 회의에 한 번.
    _r13_nolive_prove=r13_prove
    def r13_prove(claim):
        first=claim not in (store.room13 or {}).get("propositions",[])
        result=_r13_nolive_prove(claim)
        if first and not r13_has("reward:"+claim):
            r13_flag("reward:"+claim)
            r13_cash(R13_MEETING_REWARD,"회의 뒤 주민들이 모아 준 사례")
            renpy.notify("주민들이 고맙다며 %d냥을 모아 건넸다."%R13_MEETING_REWARD)
        return result

