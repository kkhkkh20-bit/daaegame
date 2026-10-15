# 다람이 at night in 13호 (owner's knowledge-run plan E, 0.18.16).
#   다람이 reacts only to what she saw or what Dad tells her first; the topic opens with Dad's telling.
#   No directions ("show it to 서리 tomorrow"), no culprit guesses, never recorded as evidence.
#   Sleeping never waits on these.
init 117 python:
    R13_NIGHT_TALKS=[
        ("night:ledger_madam","백 부인에게 장부를 보여 준 일을 이야기한다",lambda:r13_town().get("madam_alerted_at") is not None,[
            ("dad","오늘 백 부인한테 창고 장부를 보여 줬어. 오래된 장부라고 하더라."),
            ("daram","그 아줌마한테 우리가 장부를 갖고 있다고 말해도 됐을까?"),
            ("dad","……글쎄. 아빠도 그 생각을 하고 있었어.")]),
        ("night:locked","창고에서 밤을 새운 일을 이야기한다",lambda:r13_has("store_locked_night"),[
            ("dad","어젯밤엔 창고 문이 잠겨서 못 왔어. 미안해."),
            ("daram","아빠가 안 와서 문 쪽만 보고 있었어."),
            ("dad","다음엔 늦어지면 어떻게든 알릴게.")]),
        ("night:bami","밤이와 나눈 이야기를 들려준다",lambda:r13_has("bami_warning"),[
            ("dad","밤이가 본 걸 말해 줬어. 그런데 자기 이름은 쓰지 말래."),
            ("daram","밤이는 거짓말한다기보다 무서운 것 같았어."),
            ("dad","그래. 무서운 게 이상한 일은 아니지.")]),
        ("night:money","오늘 번 돈 이야기를 한다",lambda:any(r13_has(f) and not r13_has(f.split("_")[0]+"_reconciled") for f in ("piko_hostile","ttadak_hostile","siluk_hostile","somi_hostile")),[
            ("dad","다른 사람 일을 알리고 사례를 받았어. 그래서 오늘은 돈이 좀 생겼어."),
            ("daram","오늘은 돈이 많네. 그런데 그 사람은 괜찮을까?"),
            ("dad","……아빠도 잘 모르겠다.")]),
        ("night:helped","도와준 주민 이야기를 한다",lambda:any(r13_has(f) for f in ("transport_terms","shelter_agreed","operators_terms","siluk_cart","lodging_cheap")),[
            ("dad","전에 우리가 도와준 사람이 오늘은 우리를 도와줬어."),
            ("daram","지난번에 우리가 도와준 걸 기억하고 있었네."),
            ("dad","응. 그 사람도 자기 사정이 있을 텐데 말이야.")]),
    ]
    for _k,_t,_c,_l in R13_NIGHT_TALKS:
        ROOM13["topics"][_k]=dict(npc="daram",title=_t,day=[2,14],need=["lodging"],give=[],flags=[],lines=list(_l))
    R13_NIGHT_TALK_COND=dict((k,c) for k,t,c,l in R13_NIGHT_TALKS)

    _r13_night_topics=r13_topics
    def r13_topics(person):
        rows=_r13_night_topics(person)
        return [(k,s) for k,s in rows if k not in R13_NIGHT_TALK_COND or (r13_home_with_daram() and R13_NIGHT_TALK_COND[k]())]
