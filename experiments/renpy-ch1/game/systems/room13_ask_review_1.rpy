# 0.19.17 선택지 검수 1 (소유자 2026-10-17: "미리 뭘 안다는 게 불가해. 질문 선택지부터 … 말이 되게끔.")
#   맡은 인물: 구슬, 굴돌, 까로, 꽥순, 나비, 너울, 네로, 누비, 다람, 달그락, 도토, 돌목, 따닥, 모모
#   판정: 그 선택지가 처음 목록에 나올 수 있는 가장 이른 때에 아빠가 아는 것(보이는 것, 들은 답, 깃발·기록)만 전제하는가.
#   앞 층(room13_ask_*.rpy, init 193~197)과 줄기 파일은 고치지 않고 여기서 덧붙인다.
#   - steps는 {"all":[기존, 새 조건]}으로 합친다.  - 제목을 바꾸면 R13_QUESTION_SUMMARIES에 새 요약을 넣는다.
#   - 첫 대사가 제목·사실과 어긋나면 variants로 첫 갈래를 맞춘다(기존 조건 갈래는 앞에 그대로 둔다).
init 198 python:
    def _rv1_steps(key,new):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("steps")
        t["steps"]={"all":[old,new]} if old else new

    def _rv1_retitle(key,title,summary=None):
        t=ROOM13["topics"].get(key)
        if not t:return
        old=t.get("title")
        t["title"]=title
        if summary:R13_QUESTION_SUMMARIES[title]=summary
        elif old in R13_QUESTION_SUMMARIES and title not in R13_QUESTION_SUMMARIES:
            R13_QUESTION_SUMMARIES[title]=R13_QUESTION_SUMMARIES[old]

    def _rv1_set_default(key,lines,first=()):
        """기본(None) 갈래를 바꾼다. first: 기본 갈래 바로 앞에 넣을 (조건, 대사) 갈래들."""
        t=ROOM13["topics"].get(key)
        if not t:return
        rows=[row for row in (t.get("variants") or []) if row[0] is not None]
        t["variants"]=rows+list(first)+[(None,list(lines))]

    def _rv1_with_child(s):
        return s.get("daram_state") in ("with_dad","rescued")

    def _rv1_named(s):
        """초롱이 '등불을 돌보는 분'이라는 걸 아빠가 아는가(r13_mother_knowledge와 같은 근거)."""
        try:return bool(r13_mother_knowledge(s)["named"])
        except Exception:return False

    # ================================================================ 까로
    # 둘째 날 목록 맨 위의 "마차는 언제 다시 출발합니까?"(life:karo)는 첫날 축 질문(life:karo:work)이나
    # 예전 귀가 질문(karo_road)에서 "축을 고쳐도 고개가 막혔다"를 이미 들었을 수 있다. 들은 말을 처음 듣는 듯 묻지 않는다.
    if "life:karo" in ROOM13["topics"]:
        _rv1_karo_rest=[tuple(x) for x in (ROOM13["topics"]["life:karo"].get("lines") or [])[2:]]
        ROOM13["topics"]["life:karo"]["variants"]=[({"any":[{"has":["life:karo:work"]},{"has":["karo_road"]}]},[
            ("dad","축을 고쳐도 고개가 막혔다고 하셨지요. 그럼 마차는 언제쯤 다시 다닙니까?"),
            ("karo","고개를 넘는 정기 마차도 겨울에는 쉬어요. 제 마차로도 당장은 못 돌아가십니다.")]+_rv1_karo_rest)
        ]+list(ROOM13["topics"]["life:karo"].get("variants") or [])
    # "마차는 당장 못 간다"를 들은 뒤에는 "축을 갈면 출발할 수 있습니까?"를 새로 묻지 않는다(읽었으면 그대로 남는다).
    _rv1_steps("life:karo:work",{"any":[{"not":["life:karo"]},{"has":["life:karo:work"]}]})
    _rv1_steps("karo_road",{"any":[{"not":["life:karo","life:karo:work"]},{"has":["karo_road"]}]})
    # 묻는 말과 답이 어긋남: "어떻게 해야 합니까?"에 까로는 자기 일이 안 끝났다는 이야기를 한다.
    _rv1_retitle("life:karo:after","요즘 마차 일은 어떠십니까?","까로의 요즘 일을 묻는다")
    # "부인의 짐"은 남의 아내를 높이는 말이다. 아빠는 자기 아내를 "아내"라고 한다(첫 대사도 "아내의 짐을").
    _rv1_retitle("rumor_mom:karo","아내 짐을 실어 가셨다고 들었습니다")

    # ================================================================ 나비
    # "공구를 가지러 간 뒤"는 나비가 이 질문에 답하면서 처음 말하는 사실이다. 도토 기록(E11)으로 아는 것만 묻는다.
    _rv1_retitle("nabi_gap","문을 부술 때 할머니도 같이 계셨니?")
    # 메모(M01)에는 "등불을 돌보는 분"이라고만 적혀 있다. 나비에게 메모만 보였고 초롱 이름을 모를 수 있다.
    # "초롱 씨를 만났다고 하더구나"는 들은 데가 없다. 제목도 24자를 넘었다.
    _rv1_retitle("poc:nabi_packet","아내가 등불 돌보는 분께 뭘 맡겼니?","아내가 등불 돌보는 분께 맡긴 것을 묻는다")
    _rv1_set_default("poc:nabi_packet",[
        ("dad","아내 메모에 등불 돌보는 분께 소식을 물으라고 적혀 있어. 아내가 그런 분에게 뭘 맡긴 적 있었니?"),
        ("nabi","등불지기 초롱 씨요? 부인이 초롱 씨한테 봉투 하나를 건네는 건 봤어요. 접힌 채로요."),
        ("dad","그 봉투 안에 무엇이 들었는지도 아니?"),
        ("nabi","봉투는 안 읽었어요. 두 분이 하는 말도 못 들었고요."),
        ("dad","초롱 씨라고 했지. 아내가 봉투를 직접 건네는 걸 봤다는 것만 적어 둘게. 나머지는 그분에게 확인해 봐야겠구나.")],
        first=[(_rv1_named,[
            ("dad","아내 메모에 등불 돌보는 분께 소식을 물으라고 적혀 있어. 초롱 씨 말이야. 아내가 그분에게 뭘 맡긴 적 있었니?"),
            ("nabi","부인이 봉투 하나를 건네는 건 봤어요. 접힌 채로요."),
            ("dad","그 봉투 안에 무엇이 들었는지도 아니?"),
            ("nabi","봉투는 안 읽었어요. 두 분이 하는 말도 못 들었고요."),
            ("dad","아내가 봉투를 직접 건네는 걸 봤다는 것만 적어 둘게. 나머지는 초롱 씨에게 확인해 봐야겠구나.")])])
    # 24자 넘음.
    _rv1_retitle("ep1:nabi_shelter","광장 그림쟁이를 오늘 밤 재워 줄 수 있니?","그림쟁이를 재워 줄 수 있는지 묻는다")

    # ================================================================ 너울
    # 너울은 광장 길을 정리한다(첫 만남 "이 길을 정리하는 일을 맡고 있습니다", 활동 "길을 지키던 사람").
    # 1~7일에 지키는 "문"은 보이지 않는다.
    _rv1_retitle("life:neoul:work","길을 지키시는 이유가 뭡니까?","길을 지키는 이유를 묻는다")
    _rv1_set_default("life:neoul:work",[
        ("dad","이 길을 지키시는 이유가 뭡니까?"),
        ("neoul","밖에서 들어오는 사람보다, 안에서 나가는 사람이 더 많이 다칩니다."),
        ("dad","마을 밖으로 나가겠다는 사람을 막기도 합니까?"),
        ("neoul","기다리라고 할 때는 있습니다. 그렇다고 그 말에 책임이 없는 건 아닙니다.")],
        first=[(_rv1_with_child,[
            ("daram","여기 길은 왜 지키고 있어요?"),
            ("neoul","밖에서 들어오는 사람보다 안에서 나가는 사람이 더 많이 다칩니다. 그래서 지킵니다."),
            ("dad","나가겠다는 사람을 막기도 합니까?"),
            ("neoul","막지는 않아도 기다리라고 할 때는 있습니다. 그렇다고 그렇게 말한 제 책임이 없다는 건 아니고요.")])])
    # 답이 "아이를 보호실에 둔 기록"이다. 사건이 막힌 판(아이가 갇힌 적 없음)에서는 나오지 않는다.
    _rv1_steps("life:neoul:after",{"any":[{"case":"occurred"},{"has":["life:neoul:after"]}]})

    # ================================================================ 네로
    # 아빠는 어른에게 존댓말. 네로는 다른 대사 모두 해요체인데 여기만 해라체였다.
    _rv1_retitle("ep5:st_nero_after","무엇을 그렇게 꿰매고 계십니까?","무엇을 꿰매는지 묻는다")
    _rv1_set_default("ep5:st_nero_after",[
        ("resident_nero","학교 아이들 이름표예요. 표가 없는 애들 것까지요."),
        ("resident_nero","그날 밤 다 못 데려왔어요. 그래서 이름이라도 먼저 걸어 두는 거예요. 다음엔 이름을 보고 찾아올 수 있게요.")])
    if "ep5:st_nero_after" in ROOM13["topics"]:
        ROOM13["topics"]["ep5:st_nero_after"]["again"]=[(None,[("resident_nero","오늘도 이름표를 꿰매요. 다음엔 이름을 보고 찾아올 수 있게요.")])]

    # ================================================================ 따닥
    _rv1_retitle("ep4:st_ttadak_after","판자 문은 어떻게 하셨습니까?","판자 문을 어떻게 했는지 묻는다")

    # ================================================================ 모모
    # 모모 그림(전신·얼굴)에는 초록 숄이 없다(자주색 옷, 레이스 깃, 브로치). "늘 여미고 계시네요"는 보이지 않는 것을 전제한다.
    # 숄은 모모가 걸친 것이 아니라 곁에 개켜 둔 것으로 보이게 하고, 그것을 묻는다(동생 숄이라는 사실은 그대로).
    _rv1_retitle("ep6:st_momo_glasses","개켜 둔 초록 숄은 누구 겁니까?","초록 숄이 누구 것인지 묻는다")
    _rv1_set_default("ep6:st_momo_glasses",[
        (None,"모모 곁 의자에 초록 숄 하나가 곱게 개켜져 있었다. 전시품 번호는 붙어 있지 않았다."),
        ("resident_momo","제 것이 아니에요. 첫 겨울에 보호소로 간 동생 거예요."),
        ("resident_momo","옛 마을 물건이라면 뭐든 산다고들 흉보죠. 사람은 가도 물건은 남으니까, 그거라도 붙잡아 두는 거예요."),
        ("resident_momo","언젠가 누가 ‘이건 누구 것이었소’ 하고 물어봐 주면 좋겠어요. 그럼 그 이름을 한 번 더 말할 수 있으니까요.")])
    # "그림 속 장치"는 그 그림을 본 뒤(life:resident_momo:after)에야 안다.
    _rv1_steps("life:resident_momo:crisis",{"any":[{"has":["life:resident_momo:after"]},{"has":["life:resident_momo:crisis"]}]})

    # ================================================================ 굴돌
    # "옛 돌 일"은 지금은 안 한다는 전제다. 굴돌은 지금도 깨진 돌을 붙인다(ask:job). 첫 대사에 맞춘다.
    _rv1_retitle("guldol:stone","돌 일은 오래 하셨습니까?","돌 일을 오래 했는지 묻는다")
    # 아빠는 옛 시설에서 "돌이 여기서 만들어졌던 걸까" 짐작만 했다. 짐작을 사실처럼 말하지 않는다.
    if "guldol:works" in ROOM13["topics"]:
        _rv1_gw=ROOM13["topics"]["guldol:works"]
        _rv1_gw_rows=[]
        for _rv1_c,_rv1_l in (_rv1_gw.get("variants") or []):
            _rv1_l=[tuple(x) for x in _rv1_l]
            if _rv1_l and _rv1_l[0][:2]==("dad","여관 아래에 돌을 만들던 시설이 있었습니다."):
                _rv1_l=[("dad","여관 아래에서 돌을 만들던 곳 같은 시설을 봤습니다.")]+_rv1_l[1:]
            _rv1_gw_rows.append((_rv1_c,_rv1_l))
        _rv1_gw["variants"]=_rv1_gw_rows

    # ================================================================ 구슬
    # "직접 확인한 물량은 얼마나 되니?"에 구슬은 수를 말하지 않는다(사장 대신 답하지 않고 본 수량만 말하겠다는 답).
    _rv1_retitle("life:resident_guseul:after","가게 물건 수는 네가 직접 세니?","구슬이 직접 세는지 묻는다")

    # ================================================================ 도토
    # 도토가 하는 일은 장부를 옮겨 적는 일이다(ask:job, life:doto:work). "고치는 일"은 도토 답에서 처음 나온다.
    _rv1_retitle("life:doto:after","요즘 장부 일은 어떠니?","요즘 장부 일이 어떤지 묻는다")

    # ================================================================ 다람(밤 이야기)
    # 부리는 청소년이다. 다람이는 "부리 오빠"라고 부르는데 아빠가 같은 자리에서 "아저씨"라고 했다.
    _rv1_set_default("night:buri",[
        ("dad","부리 오빠를 만났어."),
        ("daram","부리 오빠는 아직 나랑 말하기 싫은가 봐."),
        ("dad","……부리 오빠한테도 시간이 필요할 거야.")])
    # 본문은 "오늘"을 뺐는데 제목에 남아 있었다(지난 일을 나중에 이야기해도 맞게).
    _rv1_retitle("night:money","사례로 받은 돈 이야기를 한다","사례로 받은 돈 이야기를 한다")
    _rv1_retitle("night:helping","같이 한 일을 이야기한다","같이 한 일을 이야기한다")
