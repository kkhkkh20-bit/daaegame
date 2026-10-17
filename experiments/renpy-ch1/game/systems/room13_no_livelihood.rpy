# 0.18.91 일거리·숙박비·외상 없애기 (소유자 2026-10-17: "필요없으면 빼도 돼. 상점 돈을 얻을 방법이 애매해서")
# - 하루가 지나도 숙박비를 받지 않는다. 일거리(식사 준비·배달·수리·낚시·사냥)는 열리지 않는다.
# - 돈: 2일 아침 집에서 가져온 노잣돈 20냥 + 에피소드를 풀면 이야기에 맞는 사람이 주는 사례(R13_EP_REWARD).
#   그 밖의 기존 수입(백 부인·모모 심부름 등)은 그대로 둔다. 상점은 은호네 그대로.
# - 일을 해야만 열리던 것은 대화로 연다: 나비·까로가 본 엄마 이야기(J04·J05), 부리의 작업칼.
init 168 python:
    R13_TRAVEL_MONEY = 20

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

    # 0.18.99 돈 균형: 회의마다 똑같이 주던 사례를 없애고, 에피소드마다 한 번, 이야기에 맞는 사람이 사례한다.
    # 큰 지출(실룩 증언 10, 아이들 식량 12, 썰매 10, 대피소 15, 부리 공구함)은 하나쯤 고를 수 있고 다는 못 한다.
    # (에피소드, 주는 사람 이름, 냥, 말)
    R13_EP_REWARD = {
        "Q1":("ep1",8,"누명을 벗은 톡이 남은 등 수리비 8냥을 쥐여 주었다."),
        "Q3":("ep3",6,"풀려난 보리가 장작 판 돈 6냥을 내밀었다. \"애들 몫이오. 그 애들한테 쓰시오.\""),
        "C1":("trial",15,"재판이 끝나자 서리가 회관 위로금 15냥을 건넸다."),
        "C2":("trial",15,"재판이 끝나자 서리가 회관 위로금 15냥을 건넸다."),
        "C3":("trial",15,"재판이 끝나자 서리가 회관 위로금 15냥을 건넸다."),
        "C4":("trial",15,"재판이 끝나자 서리가 회관 위로금 15냥을 건넸다."),
        "Q5":("ep5",10,"누명을 벗은 서리가 진료소 약값에서 10냥을 덜어 주었다."),
    }
    R13_SHOP["medkit"]["price"]=30
    R13_SHOP["lockpick"]["price"]=20

    _r13_nolive_prove=r13_prove
    def r13_prove(claim):
        result=_r13_nolive_prove(claim)
        spec=R13_EP_REWARD.get(claim)
        if spec and not r13_has("reward:"+spec[0]):
            r13_flag("reward:"+spec[0])
            r13_cash(spec[1],"사례 · "+spec[2].split(" ")[0])
            renpy.notify(spec[2])
        return result

    # ---- 잠복 버그 고침 (0.18.99) ----
    # ①은 "나비를 도왔다(nabi_helped)", "부리에게 부품 수를 알렸다(buri_honest)"를 본다. 이 표식은 예전 일거리 안에서
    # 'life:' 접두사로만 생겨, 톡의 등 이야기·사서를 살리는 장작·피코를 재워 주는 길이 한 번도 열리지 않았다.
    # 일거리를 없앴으니, 직접 거드는 짧은 대화로 같은 표식을 세운다.
    ROOM13["topics"]["help:nabi"]=dict(npc="nabi",title="부엌 일, 좀 거들어 줄까?",day=[2,3],need=[],not_flags=["nabi_helped"],give=[],flags=["nabi_helped"],lines=[
        ("dad","손이 모자라 보이는데, 그릇이라도 같이 닦을까?"),
        ("nabi","손님한테 그런 일을 시키면 할머니한테 혼나요……. 그래도, 고마워요."),
        (None,"둘이서 그릇을 닦고 장작을 부엌 안으로 날랐다. 나비가 한 그릇을 따로 덮어 두었다."),
        ("nabi","이건 등불지기 초롱 씨 몫이에요. 늘 끼니를 놓치거든요. ……손님, 도움이 필요하면 말해요. 저도 갚을게요.")])
    ROOM13["topics"]["help:buri"]=dict(npc="buri",title="부품 정리, 같이 할까요?",day=[2,3],need=[],not_flags=["buri_honest"],give=[],flags=["buri_honest"],lines=[
        ("dad","부품을 크기별로 나누는 거니? 같이 세어 볼게."),
        (None,"나사와 바퀴 축을 하나씩 세어 상자에 나눠 담았다. 장부의 숫자와 실제 수가 맞지 않았다."),
        ("dad","장부에는 온도계가 있다고 적혀 있는데, 공구판 자리는 비어 있구나."),
        ("buri","아, 그거요. 톡 아저씨한테 물어보세요. 아저씨가 등 일은 다 알아요. ……알려 줘서 고마워요. 숫자 맞춰 둘게요.")])
