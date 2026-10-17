# 0.19.17 질문이 앞서 나가지 않게 (g4_market: 은호, 구슬, 백 부인, 뭉치, 실룩, 여니, 콩이, 토리, 꽥순,
#   달그락, 현이, 물결, 솔방울) — 소유자 2026-10-17
#   "배달 일을 하는지 어떻게 알고 '배달 일은 힘들지 않니?'야?" / 날짜는 "N일째" 대신 요일·때·장소로.
#   질문 제목은 아빠가 지금 아는 것(눈에 보이는 것, 들은 것, 첫 만남 장면)만 전제한다.
#   첫 만남 장면은 목록보다 먼저 반드시 나온다(r13_notice_before_talk → r13_conversation_opening).
#   - 첫 만남이나 보이는 일로 직업을 아는 사람(새 직업 질문 없음):
#       은호(물건을 늘어놓고 "이 마을 물건을 사러 왔소?"), 구슬("가게 물건을 닦고 정리해요"),
#       백 부인("제 창고에 있는 물건"), 실룩("짐을 나르는 수레입니까?" "네"), 여니(옷을 풀어 실을 감음, 수선 부탁),
#       토리("여관에 물건을 납품하는 일을 해요"), 꽥순(물통을 나름, "물 길으러 가시는 길이세요?").
#   - 첫 만남에서 일을 말하지 않는 사람: 콩이(빵 꾸러미만 보임), 뭉치(상자만 보임) → ask:job.
#   - 첫 만남 장면이 없는 새 인물(인사 대신 활동 문구만 보임): 현이·물결·솔방울 → ask:job.
#     달그락은 기존 "어디서 오셨습니까?"가 보이는 것(보따리)에서 출발해 행상임을 듣는 질문이라 그것을 첫 질문으로 쓴다.
#   기존 줄기 파일(room13_threads_market.rpy, init 185)과 조정자 수정(room13_threads_fixes.rpy, init 189)은 고치지 않고
#   이 층에서 덧붙인다. 알리바이(r13_alibi_topic)는 장면형이라 R13_ALIBI 원문을 고친다.
init 196 python:
    _G4A_TH={"thought":True}

    def _g4a_add_steps(key,new):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("steps")
        t["steps"]={"all":[old,new]} if old else new

    def _g4a_retitle(key,title):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("title")
        t["title"]=title
        if old in R13_QUESTION_SUMMARIES and title not in R13_QUESTION_SUMMARIES:
            R13_QUESTION_SUMMARIES[title]=R13_QUESTION_SUMMARIES[old]

    def _g4a_add_flag(key,flag):
        t=ROOM13["topics"].get(key)
        if not t:return
        flags=list(t.get("flags",[]))
        if flag not in flags:flags.append(flag)
        t["flags"]=flags

    def _g4a_met(s,who):
        """이 판에서 그 사람과 실제로 이야기한 적이 있는가(r13_met_people와 같은 근거, 주어진 상태로)."""
        if who in [e.get("person") for e in s.get("encounters",[]) if isinstance(e,dict)]:return True
        topics=ROOM13["topics"]
        return any(topics.get(k,{}).get("npc")==who for k in s.get("read_topics",[]))
    def _g4a_met_tori(s):
        return _g4a_met(s,"resident_tori")
    def _g4a_met_eunho(s):
        return _g4a_met(s,"resident_eunho")
    def _g4a_with_child(s):
        return s.get("daram_state") in ("with_dad","rescued")

    # ---------------------------------------------------------------- 첫 질문: 하는 일 (ask:job:<id>)
    _G4A_JOBS=[
        # 콩이(아이): 빵 꾸러미만 보였다. "요즘도 빵 배달을 하니?"는 이것을 들은 뒤.
        ("resident_kongi","콩이","바구니를 들고 다니네. 빵집 일 돕니?",[
            ("dad","바구니를 들고 다니는구나. 빵집 일을 돕니?"),
            ("resident_kongi","네! 우리 엄마 빵집이에요. 저는 구운 빵을 노점이랑 여관에 배달해요."),
            ("resident_kongi","아침엔 창고에서 심부름거리도 받아요. 길은 제가 다녀 본 데만 알려 드릴 수 있어요.")],
            "빵 배달하고 심부름해요. 다녀 본 길이면 알려 드릴게요."),
        # 뭉치(청소년): 상자만 보였다. 누구 집 일을 하는지는 몰랐다.
        ("resident_mungchi","뭉치","짐을 많이 나르는구나. 누구 일 돕니?",[
            ("dad","짐을 많이 나르는구나. 누구 일을 돕는 거니?"),
            ("resident_mungchi","백 부인 댁이요. 저는 그 집에서 심부름해요. 창고랑 장터로 짐 나르는 거요."),
            ("resident_mungchi","가족은 아니에요. 그 집에 살면서 일하는 거예요. ……부인 물건이니까 함부로 열어 보시면 안 돼요.")],
            "백 부인 댁 심부름이에요. 짐 주인은 부인이고요."),
        # 현이(어른, 가벼운 말투): 악기만 보였다.
        ("resident_hyeoni","현이","악기를 들고 다니시네요. 악사십니까?",[
            ("dad","악기를 들고 다니시네요. 악사십니까?"),
            ("resident_hyeoni","떠돌이 악사예요. 낮엔 장터에서, 저녁엔 여관 식당에서 노래하고 끼니를 얻어요."),
            ("resident_hyeoni","가사는 그날 들은 소문으로 지어요. 이번 겨울은 여기서 나기로 했고요.")],
            "낮엔 장터, 저녁엔 여관 식당이에요. 노래가 듣고 싶으면 언제든요."),
        # 물결(어른, 시원시원): 강가에선 밧줄, 식당에선 장갑, 장터에선 말린 생선 — 보이는 것이 곳마다 달라 일반 질문.
        ("resident_mulgyeol","물결","어떤 일을 하십니까?",[
            ("dad","실례지만, 어떤 일을 하십니까?"),
            ("resident_mulgyeol","나루지기예요. 얼음 위로 썰매 배를 끌어서 사람이랑 짐을 건네줘요."),
            ("resident_mulgyeol","강가 오두막에 혼자 살아요. 얼음 위로 나오실 거면 제 발자국만 밟으세요.")],
            "썰매 배 끄는 나루지기예요. 얼음 위에선 제 발자국만 밟으세요."),
        # 솔방울(어른, 담백): 어디서든 약초 다발을 들고 있다.
        ("resident_solbang","솔방울","약초를 다루시네요. 약초를 캐십니까?",[
            ("dad","약초를 늘 들고 계시네요. 약초를 캐십니까?"),
            ("resident_solbang","네. 숲에서 캐요. 캔 건 진료소에 넘기고, 남는 건 장터에 내놔요."),
            ("resident_solbang","숲 가장자리에 혼자 살아요. 약초 말고는 아는 게 별로 없어서요.")],
            "숲에서 약초를 캐서 진료소에 넘겨요. 그게 제 일이에요."),
    ]
    for _g4a_id,_g4a_name,_g4a_title,_g4a_lines,_g4a_again in _G4A_JOBS:
        ROOM13["topics"]["ask:job:"+_g4a_id]=dict(npc=_g4a_id,title=_g4a_title,day=[1,14],need=[],not_flags=[],give=[],
            flags=["knows_job:"+_g4a_id],lines=list(_g4a_lines),again=[(None,[(_g4a_id,_g4a_again)])],
            recap=_g4a_name+("이" if (ord(_g4a_name[-1])-0xAC00)%28 else "가")+" 하는 일은 이미 들었다.")
        R13_QUESTION_SUMMARIES.setdefault(_g4a_title,"하는 일을 묻는다")

    # 달그락: "어디서 오셨습니까?"(보따리를 펼친 낯선 사람에게 묻는 말)에서 행상임을 듣는다.
    _g4a_add_flag("dalgeurak:who","knows_job:resident_dalgeurak")

    # 새 첫 질문은 그 사람의 기존 질문들 앞에 둔다(같은 dict를 제자리에서 다시 채운다).
    _g4a_items=list(ROOM13["topics"].items())
    _g4a_new={k for k,_ in _g4a_items if k.startswith("ask:job:") and ROOM13["topics"][k].get("npc") in {j[0] for j in _G4A_JOBS}}
    _g4a_order=[];_g4a_placed=set()
    for _g4a_k,_g4a_t in _g4a_items:
        if _g4a_k in _g4a_new:continue
        _g4a_job="ask:job:"+str(_g4a_t.get("npc")) if isinstance(_g4a_t,dict) else None
        if _g4a_job in _g4a_new and _g4a_job not in _g4a_placed:
            _g4a_order.append((_g4a_job,ROOM13["topics"][_g4a_job]));_g4a_placed.add(_g4a_job)
        _g4a_order.append((_g4a_k,_g4a_t))
    _g4a_order+=[(k,ROOM13["topics"][k]) for k in sorted(_g4a_new-_g4a_placed)]
    ROOM13["topics"].clear()
    ROOM13["topics"].update(_g4a_order)

    # ---------------------------------------------------------------- 직업·사정을 전제한 질문에 조건
    _G4A_KONGI_JOB={"any":[{"has":["knows_job:resident_kongi"]},{"has":["smalltalk:kongi_basket"]}]}
    # "요즘도 빵 배달을 하니?": 배달한다는 걸 콩이에게 들은 뒤(첫 질문, 또는 바구니 잡아 줄 때 "배달 끝나고").
    _g4a_add_steps("life:resident_kongi:after",_G4A_KONGI_JOB)
    # 여니의 "납품"과 "토리는 혼자 안 보내요": 토리를 만나 여관 납품 이야기를 들은 뒤.
    for _g4a_k in ("life:resident_yeoni:after","life:resident_yeoni:crisis"):
        _g4a_add_steps(_g4a_k,_g4a_met_tori)
    # "썰매 배로 강을 건널 수 있습니까?": 나루지기라는 걸 들었거나 얼음판의 썰매 배 일을 겪은 뒤.
    _g4a_add_steps("mulgyeol:crossing",{"any":[{"has":["knows_job:resident_mulgyeol"]},{"has":["mulgyeol_helped"]},{"has":["mulgyeol_fell"]}]})
    # "진료소 약초는 전부 숲에서 납니까?": 진료소에 약초를 댄다는 걸 들었거나 약초 캐기를 도운 뒤.
    _g4a_add_steps("solbang:herbs",{"any":[{"has":["knows_job:resident_solbang"]},{"has":["solbang_helped"]}]})
    # "은호 사장과는 거래하십니까?": 달그락이 행상인 걸 알고, 은호 사장을 만난 뒤.
    _g4a_add_steps("dalgeurak:eunho",{"all":[
        {"any":[{"has":["knows_job:resident_dalgeurak"]},{"has":["dalgeurak:who"]},{"has":["outside_news_bought"]}]},
        _g4a_met_eunho]})
    # "아까도 말씀드렸지만, 발자국이……": 꽥순에게 돌아온 발자국 이야기를 들은 뒤.
    _g4a_add_steps("smalltalk:kkwak_tracks",{"has":["life:resident_kkwak:work"]})

    # ---------------------------------------------------------------- 제목을 보이는 것에서 출발하게
    # 은호: 예전 값을 모르는데 "가격을 바꾸셨습니까?" → 지금 값을 묻는다.
    _g4a_retitle("life:resident_eunho:work","요즘 물건값은 어떻습니까?")
    if "life:resident_eunho:work" in ROOM13["topics"]:
        ROOM13["topics"]["life:resident_eunho:work"]["variants"]=[
            ({"has":["scale_settled"]},[
                ("dad","요즘 물건값은 어떻습니까?"),
                ("resident_eunho","저울은 바로잡았소. 값을 올린 건 물건 들어오는 길이 끊겨서요."),
                ("resident_eunho","다음 물건이 언제 올지 모르니, 지금 있는 걸로 버텨야 하오.")]),
            (_g4a_with_child,[
                ("daram","여기 물건은 비싸요?"),
                ("resident_eunho","값을 좀 올렸소. 물건 들어오는 길이 끊겨서, 다음 물건이 언제 올지 모르오."),
                ("dad","그래도 이미 들어와 있던 물건인데요."),
                ("resident_eunho","있는 물건을 다 팔아 버리면 무엇으로 다음 물건을 들이겠습니까?")]),
            (None,[
                ("dad","요즘 물건값은 어떻습니까?"),
                ("resident_eunho","좀 올렸소. 물건 들어오는 길이 끊겨서, 다음 물건이 언제 올지 모르오."),
                ("dad","가게에 있는 건 이미 들어온 물건인데요."),
                ("resident_eunho","그걸 다 팔고 나면 무엇으로 다음 물건을 사겠습니까?")])]
    # 은호: 사건 뒤 "창고를 여는 일"은 은호가 먼저 꺼내는 말이다(아빠는 아직 모른다).
    _g4a_retitle("life:resident_eunho:after","요즘 걱정되는 일이 있으십니까?")
    # 구슬: 도장으로 물건을 내주는 일은 모른다. 보이는 것은 물건마다 표를 다시 확인하는 손.
    _g4a_retitle("life:resident_guseul:work","물건마다 붙은 표를 확인하니?")
    if "life:resident_guseul:work" in ROOM13["topics"]:
        ROOM13["topics"]["life:resident_guseul:work"]["variants"]=[
            (_g4a_with_child,[
                ("daram","저 물건 밑에 붙은 종이는 뭐예요?"),
                ("resident_guseul","어떤 물건을 내줄지 적힌 목록이랑 맞춰 보는 표예요. 도장만 찍혀 있다고 내주면 안 되거든요."),
                ("dad","그 목록이 바뀌면?"),
                ("resident_guseul","그래서 묶음 번호도 같이 적어요. 사장님 서명 하나만 믿고 전부 맞다고 하면 제가 혼나요.")]),
            (None,[
                ("dad","물건마다 붙은 표를 꼭 다시 확인하는구나."),
                ("resident_guseul","어떤 물건을 내줄지 적힌 종이랑 맞춰 봐요. 도장만 찍혀 있다고 내주면 안 되거든요."),
                ("dad","그 종이가 바뀌면?"),
                ("resident_guseul","그래서 묶음 번호도 적어요. 사장님 서명 하나로 전부 맞다고 하면 제가 혼나요.")])]
    # 토리(청소년): 수량을 적는다는 말은 아직 못 들었다. 제목도 부드러운 반말로.
    _g4a_retitle("smalltalk:tori_count","받은 천은 몇 장인지 세어 두니?")
    if "smalltalk:tori_count" in ROOM13["topics"]:
        ROOM13["topics"]["smalltalk:tori_count"]["variants"]=[(None,[
            ("dad","받은 천은 몇 장인지 세어 두니?"),
            ("resident_tori","받은 것하고 돌려드린 것, 둘 다 세어 둬요. 나중에 모자란다고 하면 헷갈리니까."),
            ("dad","나도 물건을 맡길 때 같이 세어 볼게."),
            ("resident_tori","그럼 좋죠. 다 끝난 뒤에 기억을 더듬어 맞춰 보는 것보다 훨씬 쉬워요.")])]
    _g4a_retitle("smalltalk:tori_stitches","바느질을 마치면 뭐부터 확인하니?")
    if "smalltalk:tori_stitches" in ROOM13["topics"]:
        _g4a_t=ROOM13["topics"]["smalltalk:tori_stitches"]
        _g4a_rows=[tuple(r) for r in _g4a_t.get("lines",[])]
        if _g4a_rows and _g4a_rows[0][0]=="dad":
            _g4a_t["variants"]=[(None,[("dad","바느질을 마치면 뭐부터 확인하니?")]+_g4a_rows[1:])]
    _g4a_retitle("life:resident_tori:crisis","지금 천을 나눌 때 뭘 챙겨야 하니?")
    # 꽥순(청소년): 제목·첫 줄을 부드러운 반말로. 발자국 이야기는 들은 뒤에만(위 steps).
    _g4a_retitle("life:resident_kkwak:after","요즘 쓸 물은 충분하니?")
    _g4a_retitle("smalltalk:kkwak_tracks","발자국만 보고 따라가면 안 되겠구나.")
    if "smalltalk:kkwak_tracks" in ROOM13["topics"]:
        ROOM13["topics"]["smalltalk:kkwak_tracks"]["variants"]=[(None,[
            ("dad","발자국만 보고 따라가면 안 되겠구나."),
            ("resident_kkwak","네. 말씀드렸잖아요. 발자국이 갔다가 돌아온 자국까지 봐야 해요."),
            ("dad","우리 아이한테도 남의 발자국을 무작정 따라가지 말라고 일러둘게."),
            ("resident_kkwak","길을 모르면 물어보세요. 아예 안 가는 게 나은 날도 있으니까요.")])]
    if "smalltalk:kkwak_ice" in ROOM13["topics"]:
        _g4a_t=ROOM13["topics"]["smalltalk:kkwak_ice"]
        _g4a_rows=[tuple(r) for r in _g4a_t.get("lines",[])]
        if _g4a_rows and _g4a_rows[0][0]=="dad":
            _g4a_t["variants"]=[(None,[("dad","물통이 얼면 어떻게 비우니?")]+_g4a_rows[1:])]

    # ---------------------------------------------------------------- 알리바이 대사: 모르는 사정을 전제하지 않게
    # 장면형 주제(r13_alibi_topic)라 variants가 아니라 R13_ALIBI 원문을 고친다. 1일=금요일.
    _G4A_ALIBI={
        # 구슬이 은호 밑에서 일하는지, 은호가 무엇이라 했는지 몰라도 되는 물음.
        ("case","resident_guseul"):[
            ("dad","사건 날 저녁엔 어디 있었니?"),
            ("resident_guseul","창고에서 은호 사장님이랑 같이 재고를 셌어요. 그날이 납품 장부 마감이었거든요."),
            ("resident_guseul","……사장님은 우리 장부 말고 다른 장부를 하나 따로 들고 계셨어요. 그건 저도 못 보게 하셨고요.")],
        # 백 부인이 저녁마다 여관에 온다는 건 부인 입에서 듣는다.
        ("case","resident_madam"):[
            ("dad","사건 날 저녁에는 어디 계셨습니까?"),
            ("resident_madam","내 창고에서 뭉치랑 보관함을 셌어요. 저녁마다 여관에 들르는데, 그날은 이상하게 가기 싫더라고요."),
            ("dad","(저녁마다 여관에 오던 사람이 하필 그날만 오지 않았다.)",_G4A_TH)],
        # 달그락이 식당 구석에 묵는다는 건 달그락이 말한다.
        ("case","resident_dalgeurak"):[
            ("dad","사건 날 저녁엔 어디 계셨습니까?"),
            ("resident_dalgeurak","식당 구석 내 자리에서 저녁 내내 장부를 썼소. 할머니는 비명 날 때까지 국을 펐소."),
            ("resident_dalgeurak","비명 뒤에 '공구를 가지러 간다'며 부엌 뒷문으로 나갔소. 식당 쪽으론 다시 안 왔소.")],
        # 현이가 식당에서 노래한다는 건 현이가 말한다.
        ("case","resident_hyeoni"):[
            ("dad","사건 날 저녁엔 어디 계셨습니까?"),
            ("resident_hyeoni","식당에서 노래하고 있었죠. 할머니는 비명 날 땐 식당에 계셨고, 그 뒤엔 부엌 쪽으로 가셔서 다시 안 오셨어요."),
            ("resident_hyeoni","비명이 들린 다음엔 다들 일어서서 2층만 쳐다봤어요.")],
        ("night1","resident_hyeoni"):[
            ("dad","저희가 온 금요일 밤엔 어디 계셨습니까?"),
            ("resident_hyeoni","식당에서 노래했죠. 새 손님이 왔다고 다들 수군거려서 노래가 잘 팔렸어요."),
            ("resident_hyeoni","할머니가 부엌에 와서 보온병에 따뜻한 차를 가득 담아 가셨어요. 손님 방에 가져가시나 했죠.")],
    }
    for (_g4a_m,_g4a_p),_g4a_claim in _G4A_ALIBI.items():
        if (_g4a_m,_g4a_p) not in R13_ALIBI:continue
        R13_ALIBI[(_g4a_m,_g4a_p)]["claim"]=list(_g4a_claim)
        _g4a_k="alibi:%s:%s"%(_g4a_m,_g4a_p)
        if _g4a_k in ROOM13["topics"]:
            ROOM13["topics"][_g4a_k]["lines"]=list(_g4a_claim)
