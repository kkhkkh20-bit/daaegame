# 0.19.17 조정자 수정 (단서 줄기 데이터 다섯 묶음 뒤, init 189)
#   작업자 보고서에서 데이터 파일로는 고칠 수 없다고 넘어온 것.
init 189 python:
    # 나비가 고쳐 말한 증언(nabi_gap, E12)을 먼저 듣고 nabi_alibi를 나중에 물으면 고치기 전의 거짓 증언(J09)이 다시 들어왔다.
    #   고쳐 말하기는 처음 증언을 들은 뒤에만 열린다.
    if "nabi_gap" in ROOM13["topics"]:
        _fx_old=ROOM13["topics"]["nabi_gap"].get("steps")
        ROOM13["topics"]["nabi_gap"]["steps"]={"all":[{"has":["nabi_alibi"]}]+([_fx_old] if _fx_old else [])}

    # 아빠는 청소년(부리)에게 부드러운 반말을 쓴다(docs/reviews/20261017/03_decisions.md).
    for _fx_key,_fx_title in (("help:buri","부품 정리, 같이 할까?"),("tool:plans","도면에서 겹친 선은 어떻게 비교하니?")):
        if _fx_key in ROOM13["topics"]:
            _fx_was=ROOM13["topics"][_fx_key]["title"]
            ROOM13["topics"][_fx_key]["title"]=_fx_title
            if _fx_was in R13_QUESTION_SUMMARIES:R13_QUESTION_SUMMARIES[_fx_title]=R13_QUESTION_SUMMARIES[_fx_was]

    # 다람이(아이)와 아빠(다람 시점)에게 자료를 보여 주면 "그 내용은 제가 확인해 드릴 수 없습니다."만 나오던 조합.
    _fx_forged={"any":[{"has":["E18"]},{"has":["N06"]}]}
    R13_REACTIONS[("daram","E01")]=[
        (_fx_forged,[("daram","이건 엄마가 쓴 게 아니었잖아. 그래도 버리지는 마, 아빠. 누가 왜 썼는지 알아야 하니까.")]),
        ({"has":["letter_no_acorn"]},[("daram","도토리가 없는 편지……. 엄마가 깜빡한 걸까, 아니면…….")]),
        (None,[("daram","엄마 편지야. 오는 길에 몇 번이나 읽었어."),("daram","……그런데 아빠, 엄마 편지가 원래 이렇게 짧았어?")])]
    R13_REACTIONS[("daram","E03")]=[(None,[("daram","엄마 바느질이야! 엄마는 실 끝을 꼭 두 번 감거든."),("daram","엄마가 여기 있었던 거야. ……언제였을까?")])]
    R13_REACTIONS[("daram","E06")]=[(None,[("daram","그날 내가 아빠한테 말한 거잖아. 나는 팔만 쳤어. 머리는 안 쳤어. 정말이야.")])]
    R13_REACTIONS[("daram","M01")]=[
        ({"thread":"mom","min":5},[("daram","엄마 말대로 초롱 언니가 봉투를 갖고 있었어. 엄마는 다 준비해 두고 숨은 걸까?")]),
        ({"thread":"mom","min":2},[("daram","초롱 언니가 등불 돌보는 사람이었지. 엄마는 언니한테 뭘 맡겼을까?")]),
        (None,[("daram","엄마 글씨다! 등불 돌보는 사람한테 물어보래."),("daram","아빠, 등불 돌보는 사람이 누굴까?")])]
    R13_REACTIONS[("daram","L13")]=[(None,[("daram","이 눈썹 흉! 엄마야."),("daram","피코 아저씨는 엄마를 어디서 본 걸까?")])]
    R13_REACTIONS[("daram","N05")]=[(None,[("daram","내 이름이야……. ‘엄마 여기 있’……. 그다음엔 뭐라고 썼을까?"),("daram","아빠, 엄마는 살아 있는 거지?")])]
    R13_REACTIONS[("daram","V08")]=[(None,[("daram","내가 손을 대니까 따뜻해졌어. 아무도 안 아팠는데."),("daram","그럼 왜 사람들이 그렇게 해야 한다고 했을까?")])]
    R13_REACTIONS[("dad","E02")]=[(None,[("dad","아빠랑 네가 같이 들어왔다는 기록이야. 이게 있으면 네가 혼자 몰래 들어왔다는 말은 못 해.")])]
    R13_REACTIONS[("dad","E16")]=[(None,[("dad","사건이 나기 전부터 우리를 떼어 놓으라는 말이 있었구나."),("dad","누가 왜 그렇게까지 했을까? 같이 알아보자.")])]
    R13_REACTIONS[("dad","E34")]=[(None,[("dad","그날 아빠가 까로 씨랑 별채 밖에서 짐을 찾았다는 기록이야. 아빠가 그때 어디 있었는지는 이걸로 말할 수 있어.")])]
    R13_REACTIONS[("dad","M01")]=[
        ({"thread":"mom","min":2},[("dad","초롱 씨가 등불을 돌보는 사람이었지. 엄마는 왜 하필 초롱 씨에게 맡겼을까?")]),
        (None,[("dad","엄마 메모구나. 등불을 돌보는 사람……. 마을에서 누가 그 일을 하는지부터 찾아보자.")])]
    R13_REACTIONS[("dad","M02")]=[(None,[("dad","‘할머니께는 보여 주지 마.’……. 엄마가 왜 그렇게 썼을까?"),("dad","이 종이는 당분간 우리 둘만 아는 걸로 하자.")])]
    R13_REACTIONS[("dad","P01")]=[(None,[("dad","피코 씨가 그려 준 엄마 얼굴이구나. 눈썹 흉까지 똑같아."),("dad","이걸 보여 주면 엄마를 본 사람이 알아볼지도 몰라.")])]
    R13_REACTIONS[("dad","J18")]=[(None,[("dad","초롱 씨랑 같이 연 봉투야. 봉인이 그대로였으니, 중간에 누가 열어 보지는 않았어.")])]
    R13_REACTIONS[("dad","L08")]=[(None,[("dad","실룩 씨가 그 밤 늦게, 손이 꽁꽁 언 채 들어왔다는 거구나."),("dad","그 추운 밤에 어디서 무얼 하다 왔을까?")])]
    R13_REACTIONS[("resident_nero","Y09")]=[(None,[("resident_nero","제가 꿰맨 겁니다. 천막에서 떠난 사람들 이름이에요."),("resident_nero","이름 없이 묻히는 사람은 없게 하려고요.")])]

    # 그 밖의 자료: 다람이와 아빠는 존댓말 일반 답 대신 자기 말투로 짧게 답한다.
    R13_FX_PLAIN={"daram":[("daram","음……. 이건 나도 잘 모르겠어. 아빠는 알아?")],
        "dad":[("dad","이건 아빠도 아직 잘 모르겠어. 더 알아보고 같이 생각해 보자.")]}
    _r13_fx_present=r13_present
    def r13_present(person,key,identity=False):
        result=_r13_fx_present(person,key,identity)
        if person in R13_FX_PLAIN and len(result)==1 and result[0][0]==person and result[0][1] in r13_generic_present_texts(person):
            return list(R13_FX_PLAIN[person])
        return result

    # 이야기가 지나가 질문이 모두 빠진 인물에게, 지금 시점에 맞는 질문 하나씩(작업자 보고서의 "대신할 질문").
    def _fx_topic(key,npc,title,steps,lines,again,variants=None):
        ROOM13["topics"][key]=dict(npc=npc,title=title,day=[1,14],need=[],not_flags=[],give=[],flags=[],lines=list(lines),
            steps=steps,again=again,**({"variants":variants} if variants else {}))
    _fx_detained=lambda s:s.get("granny_state")=="detained"
    _fx_topic("aft:buri_tools","buri","할아버지 공구는 네가 맡니?",{"case":"occurred"},
        [("dad","할아버지 공구는 이제 네가 맡는 거니?"),
         ("buri","제가 아니면 아무도 안 만져요. 할아버지 손때가 묻은 거라서요."),
         ("buri","다른 사람 손 타는 건 싫어요.")],
        [(None,[("buri","공구는 제자리에 있어요. 아무도 안 만졌고요.")])])
    _fx_topic("aft:granny_who_saw","granny","아내 부탁을 본 사람이 있나요?",
        {"all":[_fx_forged,lambda s:not _fx_detained(s)]},
        [("dad","아내가 직접 부탁했다는 걸, 할머니 말고 본 사람이 있습니까?"),
         ("granny","……그런 걸 누가 일일이 봐요. 나한테 한 말이에요."),
         ("dad","(본 사람은 없다는 뜻일까?)",{"thought":True})],
        [(None,[("granny","같은 걸 몇 번이나 물어요. 나한테 한 말이라니까요.")])])
    _fx_topic("aft:nabi_after_trial","nabi","재판 끝나고 좀 괜찮니?",lambda s:bool(s.get("trial_ended")),
        [("dad","재판 끝나고 좀 괜찮니?"),
         ("nabi","본 대로 말한 거, 후회는 안 해요."),
         ("nabi","다만 부엌에서 할머니 얼굴 보기가 좀…… 어려워요.")],
        [(None,[("nabi","괜찮아요. 밥은 지어야 하니까요.")])],
        variants=[(_fx_detained,[("dad","재판 끝나고 좀 괜찮니?"),
            ("nabi","본 대로 말한 거, 후회는 안 해요."),
            ("nabi","할머니 자리가 비었어요. 그래도 밥은 지어야 하니까요.")])])
    _fx_topic("aft:nabi_chorong","nabi","초롱 씨 일, 들었니?",{"has":["chorong_dead"]},
        [("dad","초롱 씨 일, 들었니?"),
         ("nabi","들었어요. 저녁마다 광장 등이 하나씩 켜지는 걸 보면서 일했는데……."),
         ("nabi","오늘은 부엌 창에 등잔을 하나 더 켜 뒀어요.")],
        [(None,[("nabi","부엌 창 등잔은 계속 켜 둘 거예요.")])])
    _fx_topic("aft:tosil_alone","resident_tosil","할머니 없이 지낼 만하니?",_fx_detained,
        [("dad","할머니 없이 지낼 만하니?"),
         ("resident_tosil","밥은 잘 먹어요. 아저씨가 걱정할까 봐요."),
         ("resident_tosil","……할머니는 언제 와요?"),
         ("dad","(뭐라고 답해야 할까.)",{"thought":True})],
        [(None,[("resident_tosil","오늘도 밥 잘 먹었어요.")])])
    _fx_topic("aft:somi_grandpa","resident_somi","할아버지 생각 나니?",{"has":["musoe_gone"]},
        [("dad","할아버지 생각 나니?"),
         ("resident_somi","……강 쪽은 안 봐."),
         ("dad","그래. 보고 싶을 때 말해 줘. 같이 있어 줄게."),
         ("resident_somi","……응.")],
        [(None,[("resident_somi","……괜찮아. 오늘은.")])])
    _fx_topic("aft:bori_after","resident_bori","좀 어떠세요?",{"has":["dodam_dead"]},
        [("dad","좀 어떠세요?"),
         ("resident_bori","……물어보지 마요."),
         ("resident_bori","손은 움직여요. 일은 할 수 있어요."),
         ("dad","(지금 내가 할 수 있는 게 있을까.)",{"thought":True})],
        [(None,[("resident_bori","일은 하고 있어요. 그거면 됐잖아요.")])])
    _fx_topic("aft:sling_out","resident_sling","우체국 일은 어떻게 돼요?",{"has":["sling_hostile"],"not":["sling_reconciled"]},
        [("dad","우체국 일은 어떻게 됩니까?"),
         ("resident_sling","그걸 저한테 물으세요?"),
         ("resident_sling","당분간은 못 들어가요. 쌓이는 편지만 생각하면…….")],
        [(None,[("resident_sling","아직 못 들어가요. 더 묻지 마세요.")])])
    _fx_topic("aft:mulgyeol_met","resident_mulgyeol","아내를 만났어요",{"has":["mom_reunited"]},
        [("dad","아내를 만났어요. 그동안 아내 이야기를 들려주셔서 고마웠습니다."),
         ("resident_mulgyeol","만났어요? 잘됐네요!"),
         ("resident_mulgyeol","다음엔 셋이 같이 와요. 물고기 구워 줄게요.")],
        [(None,[("resident_mulgyeol","셋이 같이 오는 거, 잊지 마요!")])])

    # 엄마를 만난 뒤에는 "엄마 보고 싶어" 밤 대화가 새로 나오지 않는다.
    for _fx_key in ("night:miss_mom","night:miss_mom2"):
        if _fx_key in ROOM13["topics"] and ROOM13["topics"][_fx_key].get("steps") is None:
            ROOM13["topics"][_fx_key]["steps"]={"not":["mom_reunited"]}
