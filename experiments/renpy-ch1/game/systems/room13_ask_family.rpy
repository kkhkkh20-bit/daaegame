# 0.19.17 질문이 앞서 나가지 않게 (g1_family: 다람, 엄마, 할머니, 나비, 토실) — 소유자 2026-10-17
#   "배달 일을 하는지 어떻게 알고 '배달 일은 힘들지 않니?'야?" / 날짜는 "N일째" 대신 요일·때·장소로.
#   질문 제목은 아빠가 지금 아는 것(눈에 보이는 것, 들은 것, 첫 만남 장면)만 전제한다.
#   - 할머니: 첫 만남 장면(접수대, "방도 준비해 뒀어요")에서 여관 주인임을 본다. 새 직업 질문 없음.
#   - 나비: 첫 만남 장면(식당에서 밥을 차려 줌, 빈 그릇을 셈)에서 여관 식사 담당임을 본다. 새 직업 질문 없음.
#   - 토실: 첫 만남 장면이 없고 인사말 대신 활동 문구("보온병을 두 손으로 꼭 안고 있다")만 보인다.
#     기존 "할머니 손녀니?"를 보이는 것에서 출발하는 첫 질문으로 바꾸고 knows_job:resident_tosil을 남긴다.
#     이름("토실아")을 부르는 질문은 이름을 들은 뒤(tosil:hello 또는 장터 친구 장면 tosil_met)에만 나온다.
#   - 다람·엄마: 가족이라 직업 전제 문제가 없다.
#   기존 줄기 파일(room13_threads_family.rpy, init 182)은 고치지 않고 이 층에서 덧붙인다.
init 193 python:
    _G1A_TH={"thought":True}

    def _g1a_add_steps(key,new):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("steps")
        t["steps"]={"all":[old,new]} if old else new

    def _g1a_retitle(key,title):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("title")
        t["title"]=title
        if old in R13_QUESTION_SUMMARIES and title not in R13_QUESTION_SUMMARIES:
            R13_QUESTION_SUMMARIES[title]=R13_QUESTION_SUMMARIES[old]

    # 토실의 이름과 처지(할머니 손녀, 여관 심부름)를 아빠가 들었는가
    _G1A_TOSIL_KNOWN=[{"has":["tosil_met"]},{"has":["knows_job:resident_tosil"]},{"has":["tosil:hello"]}]
    def _g1a_tosil_known(s=None):
        return r13_cond({"any":_G1A_TOSIL_KNOWN},s)

    # ---------------------------------------------------------------- 토실: 첫 질문
    if "tosil:hello" in ROOM13["topics"]:
        _g1a_retitle("tosil:hello","보온병 들고 심부름 가니?")
        _g1a_t=ROOM13["topics"]["tosil:hello"]
        _g1a_t["flags"]=list(_g1a_t.get("flags",[]))+[f for f in ("knows_job:resident_tosil",) if f not in _g1a_t.get("flags",[])]
        _g1a_t["variants"]=[
            ({"has":["tosil_met"]},[
                ("dad","보온병을 꼭 안고 있구나. 또 심부름 가니?"),
                ("resident_tosil","네. 여관 심부름이요. 할머니가 여관 일 도우라고 해서 같이 살아요."),
                ("dad","부모님은?"),
                ("resident_tosil","겨울엔 산 너머에서 일해요. 봄에 데리러 온대요."),
                ("resident_tosil","다람이는 몇 살이에요? 나랑 비슷해 보이는데.")]),
            (None,[
                ("dad","보온병을 꼭 안고 있구나. 심부름 가니?"),
                ("resident_tosil","네. 여관 심부름이에요. 저 토실이에요. 여관 할머니 손녀요."),
                ("resident_tosil","할머니가 여관 일 도우라고 해서 같이 살아요."),
                ("dad","부모님은?"),
                ("resident_tosil","겨울엔 산 너머에서 일해요. 봄에 데리러 온대요."),
                ("resident_tosil","같이 다니는 애는 몇 살이에요? 나랑 비슷해 보이는데.")]),
        ]

    # 이름을 부르며 묻는 알리바이 질문은 토실을 안 뒤에만(읽은 질문은 그대로 남는다).
    for _g1a_key in ("alibi:night1:resident_tosil","alibi:case:resident_tosil"):
        _g1a_add_steps(_g1a_key,{"any":_G1A_TOSIL_KNOWN+[{"has":[_g1a_key]}]})

    # ---------------------------------------------------------------- 알리바이 대사: 요일로, 모르는 아이 이름은 빼고
    # 장면형 주제(r13_alibi_topic)라 variants가 아니라 R13_ALIBI 원문과 r13_alibi_lines를 고친다. 1일=금요일.
    if ("night1","granny") in R13_ALIBI:
        R13_ALIBI[("night1","granny")]["claim"]=[
            ("dad","저희가 도착한 금요일 밤, 할머니는 어디 계셨습니까?"),
            ("granny","접수대를 지켰죠. 손님이 새로 든 날엔 늦게까지 앉아 있어요."),
            ("dad","토실이는요?"),
            ("granny","일찍 재웠어요. 그 애는 해만 지면 졸려 해요.")]
    if ("night1","resident_tosil") in R13_ALIBI:
        _g1a_a=R13_ALIBI[("night1","resident_tosil")]
        _g1a_a["claim"]=[
            ("dad","토실아, 우리가 온 금요일 밤엔 뭐 했니?"),
            ("resident_tosil","……자고 있었어요. 진짜예요."),
            ("dad","(대답이 너무 빠르다. 눈도 마주치지 않는다.)",_G1A_TH)]
        if _g1a_a.get("truth"):
            _g1a_a["truth"]=(_g1a_a["truth"][0],[
                ("dad","토실아, 우리가 온 금요일 밤에도 숲에 갔었니?"),
                ("resident_tosil","……네. 할머니가 부인한테 차 갖다 드리라고 해서요. 거짓말해서 죄송해요.")])
    for (_g1a_m,_g1a_p) in (("night1","granny"),("night1","resident_tosil")):
        _g1a_k="alibi:%s:%s"%(_g1a_m,_g1a_p)
        if _g1a_k in ROOM13["topics"] and (_g1a_m,_g1a_p) in R13_ALIBI:
            ROOM13["topics"][_g1a_k]["lines"]=list(R13_ALIBI[(_g1a_m,_g1a_p)]["claim"])

    _g1a_alibi_lines=r13_alibi_lines
    def r13_alibi_lines(key):
        rows=_g1a_alibi_lines(key)
        # 토실을 모르는 아빠는 이름을 먼저 대지 않는다. 할머니가 손녀를 스스로 말한다(재웠다는 말은 그대로).
        if key=="alibi:night1:granny" and not _g1a_tosil_known() and len(rows)>=4:
            return [rows[0],rows[1],("dad","여관에 같이 지내는 식구분들은요?"),("granny","손녀 토실이는 일찍 재웠어요. 그 애는 해만 지면 졸려 해요.")]
        return rows

    # ---------------------------------------------------------------- 할머니
    # 방 안쪽 빗장은 13호실에 올라가 본 뒤에야 보인다(13호 책상 메모 M01 = 방에 들어감).
    _g1a_add_steps("granny_rules",{"any":[{"has":["M01"]},{"has":["E03"]},{"has":["granny_rules"]}]})

    # ---------------------------------------------------------------- 나비
    # 초롱 그릇: 거들기(help:nabi) 전에는 초롱의 이름도, 그 그릇이 누구 것인지도 모른다. 보이는 그릇에서 출발한다.
    if "life:nabi" in ROOM13["topics"]:
        _g1a_retitle("life:nabi","따로 덮어 둔 그릇은 누구 몫이니?")
        def _g1a_nabi_mk(s):
            try:return bool(r13_mother_knowledge(s)["recognized"])
            except Exception:return False
        _G1A_BOWL_KNOWN=[("dad","따로 덮어 둔 그릇 말이야, 초롱 씨 몫이라고 했지?"),
            ("nabi","네. 밖에서 등불을 돌보느라 끼니때를 자주 놓치거든요.")]
        _G1A_BOWL_NEW=[("dad","부엌에 따로 덮어 둔 그릇 말이야, 누구 몫이니?"),
            ("nabi","등불지기 초롱 씨 몫이에요. 밖에서 등불을 돌보느라 끼니때를 자주 놓치거든요.")]
        _G1A_MOM_RECOG=[("dad","아내가 여기 머물 때도 초롱 씨가 여관에 자주 왔었니?"),
            ("nabi","네, 끼니 받으러 왔어요. 두 분이 무슨 이야기를 나눴는지는 못 들었어요.")]
        _G1A_MOM_ASK=[("dad","아내가 여기 머물 때도 초롱 씨가 왔었니?"),
            ("nabi","네, 아내분이 머물 때도 왔어요. 무슨 이야기를 나눴는지는 못 들었으니까, 그분에게 직접 물어봐요.")]
        _G1A_HELPED={"has":["help:nabi"]}
        ROOM13["topics"]["life:nabi"]["variants"]=[
            (lambda s:r13_cond(_G1A_HELPED,s) and _g1a_nabi_mk(s),_G1A_BOWL_KNOWN+_G1A_MOM_RECOG),
            (_G1A_HELPED,_G1A_BOWL_KNOWN+_G1A_MOM_ASK),
            (_g1a_nabi_mk,_G1A_BOWL_NEW+_G1A_MOM_RECOG),
            (None,_G1A_BOWL_NEW+_G1A_MOM_ASK),
        ]
