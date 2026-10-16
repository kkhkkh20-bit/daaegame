# 큰 에피소드 4개 (docs/EVENT_CATALOG.md 허브): 마을을 이해하고, 재판의 조건을 만든다.
#   1 처마 밑의 밤이   — 야생화 검사. 밤이가 4일 저녁 처마에 남아 있어야 본 것을 말할 수 있다.
#   2 나비의 빚        — 표 없는 아이들. 아이들 끼니를 따로 구해야 나비가 할머니 앞에서도 본 대로 말한다.
#   3 광장의 돌        — 돌의 삼백 년과 최근의 희생. 촌장이 "증거대로 판단하고 집행"을 약속해야 진범 판결이 집행된다.
#   4 톡의 공방        — 등 속의 돌 조각. 톡의 누명을 벗겨야 톡이 핀 이야기를 재판에서 직접 한다.
# 재판 연결(systems/room13_debate.rpy):
#   E10은 bami_consent(기존), E12·E15는 witness:nabi, E13은 witness:tok가 있어야 쓸 수 있다.
#   C4(진범)는 fair_hearing이 없으면 입증해도 집행되지 않는다(다람이 석방까지만).
# 세계 기록 W1~W5는 증거가 아니라 마을을 이해하는 기록이다.
init 103 python:
    for _key,_name,_est,_not in (
        ("W1","검사가 뜻하는 것","경비는 말이 거칠어지거나 가족을 못 알아보는 주민을 '검사'해 북쪽 보호소로 보낸다. 바둑이는 돌아온 사람을 본 적이 없다.","보호소 안에서 무슨 일이 있는지는 아무도 말하지 않는다."),
        ("W2","표 없는 아이들","배급표는 집마다 나온다. 집이 없는 아이들은 표가 없어서 여관의 남은 밥으로 버틴다. 나비가 그 밥을 날랐다.","아이들이 몇 명인지, 언제부터인지는 나비만 안다."),
        ("W3","돌의 삼백 년","도서관 기록에 따르면 광장의 돌은 삼백 년 넘게 마을을 데웠다. 겨울마다 이름이 새겨진 건 네 해 전부터다.","무엇이 네 해 전에 바뀌었는지는 적혀 있지 않다."),
        ("W4","식어 가는 돌","우박이 잰 돌의 출력은 가을보다 눈에 띄게 낮다. 밤마다 조금씩 더 떨어진다.","언제 완전히 멈출지는 측정만으로 알 수 없다."),
        ("W5","등 속의 돌 조각","마을의 등은 돌에서 떼어 낸 작은 조각으로 빛난다. 조각을 빼면 등은 금방 식는다.","조각이 왜 사람의 온기처럼 따뜻한지는 톡도 설명하지 못한다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(W1="검사의 뜻",W2="표 없는 아이들",W3="돌의 삼백 년",W4="식어 가는 돌",W5="등 속의 조각")

    # ---- 재판 연결 ----
    R13_WITNESS_GATES={"E12":"witness:nabi","E15":"witness:nabi","E13":"witness:tok"}
    R13_WITNESS_REFUSALS={
        "witness:nabi":[("nabi","……저는 할머니랑 계속 같이 있었어요. 제가 아는 건 그것뿐이에요."),
            ("dad","(나비가 전에 한 말과 다르다. 할머니 앞이라 말하지 못하는 것이다. 그 아이에게 무엇이 걸려 있는지 먼저 알아야 했다.)",{"thought":True})],
        "witness:tok":[("resident_ppul","수리공 톡은 오늘 나오지 않았소. 쪽지만으로는 누가 고친 핀인지 확인할 수 없소."),
            ("dad","(톡이 직접 말해 줘야 했다. 그가 왜 나오지 않았는지 알아봤어야 했다.)",{"thought":True})],
    }
    for _claim in ("C1","C2","C3","C4"):
        for _st in R13_DEBATE.get(_claim,{}).get("statements",[]):
            for _key,_flag in R13_WITNESS_GATES.items():
                if _key in _st.get("accept",[]):
                    _st.setdefault("need_consent",{})[_key]=_flag
                    _st.setdefault("consent_lines",{})[_key]=R13_WITNESS_REFUSALS[_flag]

    def r13_debate_gap_lines(claim,st):
        """Why a statement could not be answered, when the reason is a missing witness."""
        held=store.room13.get("evidence",[])
        for key,flag in st.get("need_consent",{}).items():
            if key in held and not r13_has(flag):
                if flag=="bami_consent":
                    return [("dad","(밤이의 기록은 있다. 하지만 밤이가 자기 이름으로 말하겠다고 한 적은 없다.)",{"thought":True})]
                return list(R13_WITNESS_REFUSALS.get(flag,[]))
        return []

    R13_C4_UNENFORCED=[("resident_ppul","말은 다 들었소. ……그러나 여관 어른을 외지 사람 말로 가둘 수는 없소."),
        ("resident_ppul","아이는 풀어 주겠소. 나머지 일은 마을이 알아서 하오."),
        ("dad","(증거는 섰다. 그러나 판결을 집행할 사람이 듣지 않는다. 촌장이 왜 이렇게까지 버티는지 먼저 알았어야 했다.)",{"thought":True})]

    # Witnesses who were not where they needed to be.
    ROOM13["topics"]["bami_saw"]["not_flags"]=list(ROOM13["topics"]["bami_saw"].get("not_flags",[]))+["bami_taken","bami_hidden_away"]
    ROOM13["topics"]["bami_boundary"]["not_flags"]=list(ROOM13["topics"]["bami_boundary"].get("not_flags",[]))+["bami_taken","bami_hidden_away"]

    _r13_episode_where=r13_where
    def r13_where(person):
        if person=="bami" and r13_has("bami_taken"):return None
        if person=="resident_tok" and r13_has("tok_detained") and not r13_has("tok_cleared"):return None
        return _r13_episode_where(person)

    # ---- 에피소드 주제 ----
    def _ep_topic(npc,title,day,need=(),flags=(),give=(),not_flags=(),lines=()):
        return dict(npc=npc,title=title,day=list(day),need=list(need),flags=list(flags),give=list(give),not_flags=list(not_flags),lines=list(lines))
    ROOM13["topics"].update({
        # 1 밤이
        "bami_away":_ep_topic("bami","그날 저녁 어디 있었는지 묻는다",(4,14),need=["bami_hidden_away"],lines=[
            ("bami","그동안 네로 아저씨네 헛간에 있었어요. 아저씨가 저를 숨겨 줬잖아요."),
            ("bami","그래서 그날 13호에서 일어난 일은 아무것도 못 봤어요. 미안해요. 저한테는 살아 있는 게 먼저였어요.")]),
        # 2 나비
        "nabi_rear":_ep_topic("nabi","주방 뒷문의 등불 이야기를 꺼낸다",(3,6),need=["know_kitchen_rear"],not_flags=["nabi_secret"],
            flags=["nabi_secret","know_nabi_debt"],give=["W2"],lines=[
            ("dad","밤마다 주방 뒷문 쪽에서 등불이 오간다고 들었어."),
            ("nabi","……누가 봤대요? 콩이가 말했죠."),
            ("nabi","남은 밥이에요. 표 없는 아이들한테 가는 거요. 할머니는 모르는 척하시고, 대신 제 품삯에서 빼요."),
            ("nabi","할머니가 거둬 주신 빚이 있으니까 아무 말도 못 해요. 그 애들만 아니면요.")]),
        "nabi_food":_ep_topic("nabi","아이들 끼니를 다른 데서 구하자고 한다",(3,6),need=["nabi_secret"],not_flags=["kids_fed"]),
        "nabi_truth":_ep_topic("nabi","이제 본 대로 말해 줄 수 있는지 묻는다",(4,7),need=["kids_fed"],flags=["witness:nabi"],lines=[
            ("nabi","이제 아이들 밥이 할머니 손에 안 달려 있으니까요."),
            ("nabi","재판에서 물으면 말할게요. 첫 비명 때까지만 같이 있었고, 그 뒤로는 못 봤다고요."),
            ("nabi","……할머니가 저를 거둔 건 맞아요. 그것도 같이 말할 거예요.")]),
        "teacher_kids":_ep_topic("resident_teacher","표 없는 아이들을 학교 급식에 넣어 달라고 한다",(3,6),need=["nabi_secret","kids_known"],flags=["kids_fed","kids_school"],not_flags=["kids_fed"],lines=[
            ("resident_teacher","표가 없는 아이들이요? ……알고는 있었어요. 모른 척했을 뿐이지요."),
            ("resident_teacher","대피소 솥에 물을 더 붓지요. 아이들 이름은 학생 명부에 올리겠어요. 그러면 촌장님도 함부로 못 뺍니다.")]),
        # 3 돌
        "librarian_stone":_ep_topic("resident_librarian","광장 돌의 옛 기록을 보여 달라고 한다",(2,13),flags=["know_stone_history"],give=["W3"],lines=[
            (None,"사서 선생님은 젖은 책 사이에서 가죽 장부 하나를 꺼냈다."),
            ("resident_librarian","돌이 마을을 데운 기록이에요. 삼백 년이 넘었어요. 축제 날짜, 고친 날짜, 날씨까지요."),
            ("resident_librarian","여기를 보세요. 네 해 전부터 겨울마다 한 줄씩 늘어요. 전부 사람 이름이에요."),
            ("dad","네 해 전에는 이름이 없었습니까?"),
            ("resident_librarian","없었어요. 그러니 ‘옛날부터 그래 왔다’는 말은 거짓말이에요. 저는 그 말이 제일 무서워요.")]),
        "ppul_hearing":_ep_topic("resident_ppul","재판을 증거대로 열어 달라고 요구한다",(4,6),not_flags=["fair_hearing"]),
        # 4 톡
        "ubak_lamp":_ep_topic("resident_ubak","광장 등 뚜껑의 나사 자국을 묻는다",(3,6),need=["clue_lamp_marks"],not_flags=["tok_cleared"]),
        "tok_testify":_ep_topic("resident_tok","재판에서 핀 이야기를 직접 해 달라고 한다",(4,7),need=["tok_cleared"],flags=["witness:tok"],lines=[
            ("resident_tok","내 누명 벗겨 준 사람 부탁인데 빠지면 안 되지."),
            ("resident_tok","내가 만든 이음은 내가 알아요. 재판에서도 똑같이 말할게요. 누가 그걸로 뭘 했는지는 모른다는 것까지요.")]),
    })
    R13_TOPIC_LABELS.update({"nabi_food":"r13_ep2_food","ppul_hearing":"r13_ep3_hearing","ubak_lamp":"r13_ep4_ubak"})
    # 0.18.50: the lamp clue was only a choice inside Tok's accusation scene; any other first choice
    # (or walking past it) locked Tok's release and his testimony. It is also a square action now.
    ROOM13["activities"]["ep4_lamp_look"]=dict(place="square",title="광장 등 뚜껑을 직접 살펴본다",day=[3,6],
        need=["ep4_seen"],not_flags=["clue_lamp_marks","tok_cleared"],flags=["clue_lamp_marks","ep4_open"],give=[],cost=0,lines=[
        (None,"광장 등 뚜껑 나사에 가느다란 줄 자국이 나 있었다. 공구가 아니라 계측기 집게가 물었던 자국이었다."),
        (None,"등 안쪽은 차가웠다. 조각이 있던 자리에 종이 눈금 조각이 끼어 있었다."),
        ("dad","(톡의 공구 자국이 아니다. 누군가 무언가를 재려고 등 뚜껑을 열었다.)",{"thought":True})])
    R13_CONTEXT_ACTIVITIES[("square","lamp")]=tuple(R13_CONTEXT_ACTIVITIES.get(("square","lamp"),()))+("ep4_lamp_look",)

    def r13_ep_first(flag):
        """True once: marks a scene as seen."""
        if r13_has(flag):return False
        r13_flag(flag);return True

label r13_episode_events:
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    # 1 밤이 — 0.18.83부터 에피소드 ② 다람 탐정단(systems/room13_ep2_kids.rpy)이 대신한다.
    #   r13_ep1_patrol / r13_ep1_eaves / r13_ep1_morning 장면은 남겨 두되 부르지 않는다.
    # 2 나비
    if _d in (2,3) and _p==2 and _loc=="kitchen" and not r13_has("ep2_seen"):
        call r13_ep2_kitchen
    # 3 돌
    if _d in (r13_tl(5),r13_tl(6)) and _p==2 and _loc=="square" and not r13_has("ep3_bell_seen"):
        $ r13_offer("r13_ep3_bell")
    # 4 톡
    if _d==3 and _p<=1 and _loc=="workshop" and not r13_has("ep4_seen"):
        $ r13_offer("r13_ep4_accused")
    if _d>=5 and r13_has("ep4_seen") and not r13_has("tok_cleared") and not r13_has("tok_detained"):
        call r13_ep4_deadline
    return

# =========================================================
# 1 처마 밑의 밤이
# =========================================================

label r13_ep1_patrol:
    $ r13_flag("ep1_patrol_seen")
    call r13_ev_here("night")
    call r13_lines([(None,"여관 문이 열리고 찬바람과 함께 경비 두 사람이 들어왔다. 너울과 바둑이였다."),
        ("neoul","이 근처 처마 밑에 사는 박쥐를 본 적 있소? 등록되지 않은 아이요."),
        ("neoul","그 아이가 밤마다 돌아다닌다는 신고가 들어왔소. 그래서 검사를 받아야 하오.")],"ep1:patrol")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "처마 쪽에 있다고 알려 준다":
                call r13_lines([("neoul","협조 고맙소. 그 아이는 곧 데려가겠소."),
                    (None,"바둑이는 처마 쪽을 올려다볼 뿐, 아무 말도 하지 않았다.")],"ep1:patrol:tell")
                $ r13_flag("bami_reported")
            "못 봤다고 한다":
                call r13_lines([("neoul","그렇소? 내일 밤에 다시 돌겠소. 그 아이를 숨겨 주는 사람도 같이 검사를 받소."),
                    ("dad","(내 말을 믿지 않는 눈치다.)",{"thought":True})],"ep1:patrol:deny")
                $ r13_flag("patrol_suspicious")
            "검사가 무엇인지 묻는다" if not r13_has("W1"):
                call r13_lines([("neoul","말이 거칠어지거나, 가족을 못 알아보거나, 밤에 이상하게 돌아다니면 야생화 초기 증상이오."),
                    ("neoul","증상이 있으면 북쪽 보호소에서 지켜보오. 다 마을을 위한 일이오."),
                    ("dad","보호소에서 돌아온 사람은 있습니까?"),
                    ("neoul","……그건 보호소에서 알아서 할 일이오."),
                    (None,"너울이 문 쪽으로 돌아서자 바둑이가 낮게 말했다."),
                    ("resident_badook","저는 돌아온 사람을 본 적이 없어요. 아직 한 번도요.")],"ep1:patrol:ask")
                $ r13_grant(["W1"],"너울·바둑이와 나눈 말")
                $ r13_flag("badook_doubt")
                $ _ep_loop=True
            "박쥐 아이의 보증을 서겠다고 한다":
                call r13_lines([("neoul","외지 사람 보증은 소용없소. 검사원 확인서라도 가져오면 모를까."),
                    ("dad","(서리 검사원의 확인서. 그 확인서라면 너울도 무시하지 못한다.)",{"thought":True})],"ep1:patrol:vouch")
                $ r13_flag("patrol_suspicious","need_certificate")
            "바둑이에게 슬쩍 두 냥을 쥐여 준다" if r13_cash_now()>=2:
                call r13_lines([("resident_badook","……이러지 마세요. 돈은 안 받아요."),
                    (None,"바둑이가 동전을 내 손에 도로 쥐여 주었다. 그 모습을 너울이 보았다."),
                    ("neoul","뇌물이라. 내일 밤에는 이 여관부터 살피겠소.")],"ep1:patrol:bribe")
                $ r13_flag("patrol_suspicious","rumor:briber")
    return

label r13_ep1_eaves:
    $ r13_flag("ep1_eaves_seen")
    call r13_ev_here("quiet")
    call r13_lines([(None,"창틀에 작은 그림자가 거꾸로 매달려 있었다. 밤이였다."),
        ("bami","아까 경비가 왔었죠. 저를 데려간대요?"),
        ("bami","저 아픈 거 아니에요. 밤에 깨어 있는 건 원래 그런 거예요. 박쥐니까요.")]+([("bami","……경비한테 제가 처마에 있다고 알려 주셨다면서요.")] if r13_has("bami_reported") else []),"ep1:eaves")
    menu:
        "네로에게 부탁해 헛간에 숨긴다":
            call r13_lines([(None,"네로는 아무것도 묻지 않고 헛간 문을 열었다. 안에는 이름표 없는 사람들이 담요를 나눠 덮고 있었다."),
                ("resident_nero","여기 있는 사람들은 다 표가 없어요. 검사도 안 받고요. 대신 밖에 나가면 안 돼요."),
                ("bami","……그럼 이제 처마엔 못 가요?"),
                ("dad","며칠만 참자.")],"ep1:nero")
            $ r13_flag("bami_hidden_away","bami_safe","know_unregistered")
        "피코에게 등록증을 그려 달라고 한다 (5냥)" if r13_cash_now()>=5:
            call r13_lines([("resident_piko","등록증? ……그림은 그림이죠. 도장 모양까지 그려 드릴게요."),
                ("resident_piko","너울은 글자를 잘 안 봐요. 도장만 보죠. 대신 이 등록증은 서리 검사원한테는 보이지 마세요."),
                ("bami","이 등록증이 있으면 처마에 있어도 돼요?"),
                ("dad","응. 이게 있으면 처마에 있어도 돼.")],"ep1:piko")
            $ r13_cash(-5,"피코의 그림 등록증")
            $ r13_flag("bami_papers","bami_safe","bami_at_eaves","forged_papers")
        "서리 검사원에게 관찰 확인서를 받는다":
            call r13_lines([("resident_seori","박쥐가 밤에 깨어 있는 게 증상이라고요? 그럼 마을 박쥐는 다 증상이겠군요."),
                (None,"서리 검사원은 밤이의 눈을 살피고 몇 가지를 물어본 뒤 확인서에 서명했다."),
                ("resident_seori","‘야생화 증상 없음.’ 너울이 이 확인서를 무시하면, 그 일은 내가 기록합니다.")],"ep1:seori")
            $ r13_flag("bami_certified","bami_safe","bami_at_eaves","seori_met_bami")
        "바둑이에게 처마 순찰을 빼 달라고 한다" if r13_has("badook_doubt"):
            call r13_lines([("resident_badook","……저도 돌아온 사람을 못 봤다고 말씀드렸죠."),
                ("resident_badook","처마 순찰은 제 구역이에요. 처마엔 아무것도 없었다고 적을게요. 대신 너울 앞에선 모르는 척해 주세요.")],"ep1:badook")
            $ r13_flag("badook_ally","bami_safe","bami_at_eaves")
        "13호 창 안쪽에서 지내게 한다":
            call r13_lines([("bami","방 안은 싫어요. 방에 들어가면 도망칠 데가 없잖아요."),
                ("bami","처마가 좋아요. 처마에선 13호 안이 다 보여요. 바닥이랑 침대 밑까지.")],"ep1:room_refused")
            jump r13_ep1_eaves_retry
        "지금은 할 수 있는 게 없다고 말한다":
            call r13_lines([("bami","……그렇겠죠. 외지 분이시니까."),
                (None,"밤이는 처마 그늘 속으로 몸을 더 작게 웅크렸다.")],"ep1:nothing")
    return

label r13_ep1_eaves_retry:
    menu:
        "네로에게 부탁해 헛간에 숨긴다":
            call r13_lines([(None,"네로는 아무것도 묻지 않고 헛간 문을 열었다. 안에는 이름표 없는 사람들이 담요를 나눠 덮고 있었다."),
                ("resident_nero","여기 있는 사람들은 다 표가 없어요. 검사도 안 받고요. 대신 밖에 나가면 안 돼요.")],"ep1:nero")
            $ r13_flag("bami_hidden_away","bami_safe","know_unregistered")
        "서리 검사원에게 관찰 확인서를 받는다":
            call r13_lines([("resident_seori","‘야생화 증상 없음.’ 너울이 이 확인서를 무시하면, 그 일은 내가 기록합니다.")],"ep1:seori")
            $ r13_flag("bami_certified","bami_safe","bami_at_eaves","seori_met_bami")
        "그냥 처마에 있게 둔다":
            pass
    return

label r13_ep1_morning:
    $ r13_flag("ep1_done")
    if r13_has("bami_safe"):
        if r13_has("bami_at_eaves") and r13_has("patrol_suspicious"):
            call r13_lines([(None,"새벽에 처마 쪽에서 너울의 목소리가 들렸다. 잠시 뒤, 발소리는 처마를 그냥 지나갔다.")],"ep1:morning:passed")
        return
    # The patrol came whether or not Dad was there to answer it.
    if r13_has("bami_reported") or r13_has("patrol_suspicious") or not r13_has("ep1_patrol_seen"):
        call r13_lines([(None,"새벽, 처마 쪽에서 날개 퍼덕이는 소리와 경비의 고함이 들렸다."),
            (None,"아침에 나가 보니 처마 밑은 비어 있었다. 바닥에 작은 발톱 자국만 남아 있었다."),
            ("dad","(밤이가 검사를 받으러 북쪽 보호소로 끌려갔다.)",{"thought":True})],"ep1:morning:taken")
        $ r13_flag("bami_taken")
    return

# =========================================================
# 2 나비의 빚
# =========================================================

label r13_ep2_kitchen:
    $ r13_flag("ep2_seen")
    call r13_ev_here("night")
    call r13_lines([(None,"주방 뒷문이 반쯤 열려 있었다. 나비가 남은 빵과 식은 수프를 천에 싸서 문밖으로 내밀고 있었다."),
        (None,"문밖에는 다 해진 신발을 신은 아이 둘이 서 있었다. 아이들은 나를 보자 얼어붙었다."),
        ("nabi","……보셨어요?")],"ep2:kitchen")
    menu:
        "못 본 척 지나간다":
            call r13_lines([("nabi","고마워요. 이건 아무것도 아니에요. 진짜로요.")],"ep2:ignore")
        "할머니에게 알린다":
            call r13_lines([("granny","나비야. 여관 밥이 네 것이니?"),
                ("nabi","……죄송해요."),
                ("granny","이번 주 품삯에서 빼마. 너는 내가 거둔 아이야. 그걸 잊지 마라."),
                (None,"뒷문이 닫혔다. 아이들 발소리가 눈 속으로 멀어졌다.")],"ep2:tell_granny")
            $ r13_flag("nabi_hostile","granny_warned_nabi")
        "음식 짐을 같이 날라 준다":
            call r13_lines([(None,"아이들은 학교 뒤 장작 창고에서 지내고 있었다. 그곳에 아이가 다섯 있었다."),
                ("nabi","표가 없어요. 집이 없으면 표도 없어요. 그래서 여관에서 남은 밥으로 버텨요."),
                ("nabi","할머니는 모르는 척하세요. 대신 제 품삯에서 빼고요. 저는 거둬 주신 빚이 있으니까요.")],"ep2:carry")
            $ r13_grant(["W2"],"나비와 아이들이 사는 곳")
            $ r13_flag("kids_known","nabi_secret","know_nabi_debt")
        "왜 밥을 빼돌리는지 묻는다":
            call r13_lines([("nabi","할머니가 길에서 저를 거둬 주셨어요. 그 빚은 평생 가도 못 갚아요."),
                ("nabi","할머니 밥을 빼돌리는 게 나쁜 거라는 건 알아요. 그래도 저 애들은 표가 없어요.")],"ep2:ask")
            $ r13_grant(["W2"],"나비에게 들은 말")
            $ r13_flag("nabi_secret","know_nabi_debt")
        "구운 밤을 아이들 손에 쥐여 준다" if r13_has("own:snack"):
            call r13_lines([(None,"아이들은 구운 밤을 받아 들고 나비 뒤로 숨었다. 한 아이가 작게 고맙다고 했다."),
                ("nabi","……이 구운 밤, 다람이 몫 아니에요? 고마워요. 얘네가 자는 데는 학교 뒤 장작 창고예요.")],"ep2:snack")
            $ r13_use_item("snack")
            $ r13_grant(["W2"],"나비와 아이들이 사는 곳")
            $ r13_flag("kids_known","nabi_secret","nabi_soft")
    return

label r13_ep2_food:
    call r13_lines([("dad","그 아이들 끼니를 할머니 밥 말고 다른 데서 구해 보면 어떨까."),
        ("nabi","어디서요? 이 마을에 남는 밥은 없어요. 다들 자기 먹을 것도 없다고 해요.")],"ep2:food:open")
    menu:
        "은호 사장에게 일주일 치를 산다 (12냥)" if r13_cash_now()>=12:
            call r13_lines([("resident_eunho","일주일 치요? 값은 정해진 대로 받습니다. 누가 먹을 건지는 묻지 않겠습니다."),
                ("nabi","……열두 냥이면 탐정님 사흘 품삯이잖아요.")],"ep2:food:buy")
            $ r13_cash(-12,"아이들 일주일 치 식량")
            $ r13_flag("kids_fed","kids_bought")
        "창고 장부로 촌장에게 배급을 요구한다" if "H1" in room13["evidence"]:
            call r13_lines([("resident_ppul","……백 부인 창고에 이 물건이 다 있었다고?"),
                ("resident_ppul","표 없는 아이들 몫으로 내놓으라 하겠소. 이 장부는 내가 맡아 두지."),
                ("nabi","촌장님이 직접 나서신다고요?")],"ep2:food:hoard")
            $ r13_flag("kids_fed","kids_registered","madam_hostile")
        "무쇠 할아버지에게 폐광 식량을 청한다" if r13_has("musoe_ally"):
            call r13_lines([("resident_musoe","굴 안에 말린 콩 자루가 있소. 솜이 몫만 남기고 가져가시오."),
                ("resident_musoe","내가 진 빚을 갚는 셈이오. 아이들 배곯는 건 나도 못 보오.")],"ep2:food:mine")
            $ r13_flag("kids_fed","kids_mine")
        "학교 사자 선생님에게 부탁하자고 한다" if r13_has("kids_known"):
            call r13_lines([("nabi","사자 선생님이요? ……선생님은 좋은 분인데, 촌장님 눈치를 봐요."),
                ("dad","학교에 직접 가서 말해 볼게.")],"ep2:food:teacher")
            $ r13_flag("try_teacher")
        "다람이 몫을 나누자고 한다":
            call r13_lines([("nabi","그건 안 돼요. 다람이도 제 몫은 먹어야죠."),
                ("nabi","……그래도 그렇게 말해 준 사람은 처음이에요.")],"ep2:food:daram")
            $ r13_flag("nabi_soft")
        "지금은 방법이 없다고 한다":
            pass
    return None

# =========================================================
# 3 광장의 돌
# =========================================================

label r13_ep3_bell:
    $ r13_flag("ep3_bell_seen")
    call r13_ev_here("night")
    call r13_lines([(None,"광장의 등이 한꺼번에 깜빡였다. 돌 표면을 타고 흐르던 빛이 숨을 고르듯 가늘어졌다."),
        (None,"종탑 아래에서 설이가 종 줄을 붙잡고 서 있었다. 너울이 그 손목을 잡고 있었다."),
        ("neoul","치지 마시오. 지금 종을 치면 다들 뛰쳐나와 난리가 날 거요."),
        ("resident_seol","종은 이럴 때 치라고 있는 거예요!"),
        ("neoul","외지 사람이 종을 마음대로 치면 초소에서 경위를 설명해야 하오. 밤새 걸릴 거요.")],"ep3:bell:v2")
    menu:
        "설이에게 종을 치라고 한다":
            call r13_lines([(None,"종소리가 마을을 갈랐다. 사람들이 문을 열고 나왔다. 그리고 아이들을 학교 쪽으로 데려갔다."),
                ("neoul","……당신 때문에 내일 아침 촌장님 앞에 불려 가게 생겼소."),
                ("resident_seol","고마워요. 종이 경고로 울린 건 네 해 만이에요.")],"ep3:ring")
            $ r13_flag("village_alerted","seol_ally","neoul_annoyed")
        "가만히 지켜본다":
            call r13_lines([(None,"종은 울리지 않았다. 몇 집의 창이 어두워졌다. 그 창들은 밤새 어두운 그대로였다."),
                (None,"아침에 보리네 아이가 열이 난다는 말을 들었다.")],"ep3:silent")
            $ r13_flag("stone_hidden","bori_child_sick")
        "우박에게 지금 돌의 출력을 재 보라고 한다":
            call r13_lines([("resident_ubak","재 볼게요. ……가을에 쟀을 때보다 눈금이 한참 아래예요."),
                ("resident_ubak","눈금이 밤마다 조금씩 더 내려가요. 이 숫자는 스승님한테만 보고했어요. 촌장님은 숫자를 싫어하시거든요."),
                ("neoul","그런 숫자는 함부로 공개하지 마시오.")],"ep3:measure")
            $ r13_grant(["W4"],"우박이 잰 돌의 출력")
            $ r13_flag("know_stone_failing","ubak_met")
        "등불지기와 함께 광장 등을 몇 개 끈다":
            call r13_lines([("resident_lamplighter","등을 끄면 돌이 덜 지쳐요. 등은 돌에서 불을 받거든요."),
                (None,"광장 등이 절반쯤 꺼지자 돌의 빛이 조금 굵어졌다. 설이가 그제야 종 줄을 놓았다."),
                ("neoul","……이번 한 번만이오.")],"ep3:lamps")
            $ r13_grant(["W5"],"등불지기와 끈 광장 등")
            $ r13_flag("lamps_saved","lamplighter_trust")
        "내가 직접 종을 친다 · 늦은 저녁까지":
            call r13_lines([(None,"줄을 당기자 묵직한 종소리가 울렸다. 너울이 내 팔을 붙잡았다."),
                ("neoul","외지 사람이 감히 마을 종을 치다니. 오늘 밤은 초소에서 보내시오."),
                (None,"그날 밤은 초소의 차가운 의자에서 보냈다. 그래도 종소리를 들은 사람들은 학교로 피했다.")],"ep3:self_ring")
            $ r13_flag("village_alerted","rumor:troublemaker","neoul_annoyed")
            $ r13_edit(period=3,location="gate")
    return

label r13_ep3_hearing:
    call r13_lines([("dad","재판은 증거로만 판단하고, 판결은 그대로 집행해 주십시오. 그 약속을 받고 싶습니다."),
        ("resident_ppul","외지 사람이 지금 마을 법을 가르치려 하오?")],"ep3:hearing:open")
    menu:
        "긁힌 이름 중 맨 아래 이름을 묻는다" if r13_has("ppul_names_seen"):
            call r13_lines([("resident_ppul","……그건 내 손녀 이름이오. 네 해 전, 첫 번째 겨울이었소."),
                ("resident_ppul","그 뒤로 나는 희생이 법이라고 믿어야 했소. 그러지 않으면 내가 그 애를 보낸 게 되니까."),
                ("dad","그러니 이번엔 증거로 판단해 주십시오. 누군가를 또 희생으로 보내기 전에 말입니다."),
                ("resident_ppul","……알겠소. 증거대로 하겠소. 판결도 내가 집행하겠소.")],"ep3:hearing:names")
            $ r13_flag("fair_hearing","ppul_ally")
        "돌의 옛 기록과 지금 출력을 보여 준다" if r13_has("know_stone_history") and r13_has("know_stone_failing"):
            call r13_lines([("dad","삼백 년 동안 기록에 이름은 없었습니다. 이름이 생긴 건 네 해 전부터고, 돌은 지금도 식고 있습니다."),
                ("dad","희생이 오래된 법이라는 말은 기록과 맞지 않습니다."),
                ("resident_ppul","……사서 선생이 그 오래된 장부를 꺼냈소? 출력 숫자는 우박이 줬고?"),
                ("resident_ppul","좋소. 이번 재판은 말이 아니라 기록으로 하겠소. 판결대로 집행하겠소.")],"ep3:hearing:records")
            $ r13_flag("fair_hearing")
        "“아이들을 구한 건 촌장님 덕입니다.”" if r13_has("village_alerted"):
            call r13_lines([("dad","어젯밤 아이들이 학교로 피한 건 촌장님이 종을 허락하셨기 때문이라고 말하겠습니다."),
                ("resident_ppul","……사람들이 그렇게 믿는다면 나쁠 건 없지."),
                ("resident_ppul","좋소. 재판은 증거대로 하겠소. 대신 당신도 내 체면을 지켜 주시오.")],"ep3:hearing:credit")
            $ r13_flag("fair_hearing","ppul_ally")
        "“이 장부를 광장에 붙일 수도 있습니다.”" if "H1" in room13["evidence"]:
            call r13_lines([("dad","배급에서 빠진 물자가 백 부인 창고에 있습니다. 이 장부를 광장에 붙이면 촌장님 배급표도 같이 흔들립니다."),
                ("resident_ppul","……지금 나를 협박하는 거요?"),
                ("resident_ppul","좋소. 재판은 증거대로 하겠소. 하지만 이 일은 잊지 않겠소.")],"ep3:hearing:threat")
            $ r13_flag("fair_hearing","ppul_hostile")
        "“증거대로 재판해 주십시오.”":
            call r13_lines([("resident_ppul","부탁으로 법을 바꾸진 않소. 재판은 마을 방식대로 하오.")],"ep3:hearing:plead")
            $ r13_flag("ppul_refused")
        "“다음에 다시 오겠습니다.”":
            pass
    return None

# =========================================================
# 4 톡의 공방
# =========================================================

label r13_ep4_accused:
    $ r13_flag("ep4_seen")
    call r13_ev_here("search")
    call r13_lines([(None,"수리점 앞에 사람들이 모여 있었다. 너울이 톡의 작업대를 손바닥으로 내리쳤다."),
        ("neoul","광장 등의 돌 조각이 없어졌소. 그 등을 열고 만지는 사람은 이 마을에 당신뿐이오."),
        ("resident_tok","나는 안 가져갔어요! 그 조각이 없으면 등이 식는다는 걸 누구보다 잘 아는 사람이 나라고요."),
        ("neoul","모레까지 돌 조각이 안 나오면 당신을 가두겠소.")],"ep4:accused")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "“증거도 없이 가둘 겁니까?”":
                call r13_lines([("dad","증거도 없이 사람을 가두겠다는 겁니까?"),
                    ("neoul","그럼 모레까지 증거를 가져오시오.")],"ep4:defend")
                $ r13_flag("ep4_open")
            "“너울 씨 말이 맞을 수도 있겠군요.”":
                call r13_lines([("neoul","보시오, 외지 사람도 내 말이 맞을 수 있다잖소."),
                    (None,"너울이 톡의 손목을 묶었다. 수리점 문에 판자가 덧대졌다."),
                    ("resident_tok","……당신도 저 사람들이랑 똑같군요.")],"ep4:side_neoul")
                $ r13_flag("tok_detained","tok_hostile")
            "광장 등을 직접 살펴본다" if not r13_has("clue_lamp_marks"):
                call r13_lines([(None,"광장 등 뚜껑 나사에 가느다란 줄 자국이 나 있었다. 공구가 아니라 계측기 집게가 물었던 자국이었다."),
                    (None,"등 안쪽은 차가웠다. 조각이 있던 자리에 종이 눈금 조각이 끼어 있었다."),
                    ("dad","(톡의 공구 자국이 아니다. 누군가 무언가를 재려고 등 뚜껑을 열었다.)",{"thought":True})],"ep4:lamp")
                $ r13_flag("clue_lamp_marks","ep4_open")
                $ _ep_loop=True
            "“등 안의 돌 조각은 뭡니까?”" if "W5" not in room13["evidence"]:
                call r13_lines([("resident_tok","등은 돌에서 떼어 낸 조각으로 빛나요. 손톱만 한 조각인데, 꺼내 들면 사람 손처럼 따뜻해요."),
                    ("resident_tok","조각이 왜 따뜻한지는 나도 몰라요. 요즘은 조각이 예전보다 빨리 식어요. 그게 무서워요.")],"ep4:sliver")
                $ r13_grant(["W5"],"톡에게 들은 등의 돌 조각")
                $ _ep_loop=True
            "끼어들지 않는다":
                $ r13_flag("ep4_open")
    return

label r13_ep4_ubak:
    call r13_lines([("dad","광장 등 나사에 계측기 집게 자국이 있었다. 종이 눈금도 끼어 있었고."),
        ("resident_ubak","……제가 했어요. 스승님이 돌 조각 하나를 몰래 재 오라고 하셨어요. 촌장님이 낸 숫자가 이상하다고요."),
        ("resident_ubak","톡 아저씨가 잡혀갈 줄은 몰랐어요. 조각은 지금 진료실 상자에 있어요.")],"ep4:ubak:confess")
    menu:
        "너울에게 우박을 넘긴다":
            call r13_lines([("neoul","검사원 조수가? ……됐소. 톡은 풀어 주겠소. 조수는 내가 데려가오."),
                ("resident_seori","제 지시였습니다. 이 아이를 데려가려면 저를 데려가십시오."),
                ("neoul","외부 관리국 사람은 내 소관이 아니오. 됐소.")],"ep4:ubak:hand_over")
            $ r13_flag("tok_cleared","ubak_punished","seori_cold")
        "서리 검사원에게 가서 함께 해명하게 한다":
            call r13_lines([("resident_seori","제가 시켰습니다. 촌장의 출력 보고가 측정값과 맞지 않아서요."),
                ("resident_seori","조각은 돌려드리지요. 대신 측정 결과는 기록에 남깁니다."),
                ("resident_ubak","톡 아저씨, 죄송해요."),
                ("resident_tok","……그래서 숫자는 맞았어? 돌이 식고 있다는 거.")],"ep4:ubak:seori")
            $ r13_grant(["W4"],"서리 검사원의 측정 기록")
            $ r13_flag("tok_cleared","seori_trust","ubak_ally","know_stone_failing","examination_agreed")
        "조각만 몰래 제자리에 돌려놓는다":
            call r13_lines([(None,"진료실 상자에서 조각을 꺼냈다. 그리고 밤사이 광장 등에 다시 끼웠다. 등이 천천히 데워졌다."),
                ("neoul","……조각이 돌아왔다고? 누가 장난을 쳤군. 톡은 증거가 없으니 풀어 주겠소.")],"ep4:ubak:return")
            $ r13_flag("tok_cleared","ubak_owes")
        "우박의 이름은 빼고 사실만 너울에게 알린다":
            call r13_lines([("dad","등 나사의 자국은 공구가 아니라 계측기 집게입니다. 톡의 작업 자국과 다릅니다. 조각은 측정이 끝나면 돌아올 겁니다."),
                ("neoul","누가 쟀다는 거요? ……이름을 안 대겠다고? 좋소, 조각만 돌아오면 톡은 풀어 주겠소.")],"ep4:ubak:anon")
            $ r13_flag("tok_cleared","ubak_ally")
        "아직은 모른 척한다":
            pass
    return None

label r13_ep4_deadline:
    call r13_lines([(None,"수리점 문에 판자가 덧대져 있었다. 결국 조각을 찾지 못한 채 기한이 지났다."),
        ("dad","(톡이 갇혔다. 너울은 끝내 다른 사람을 찾지 않았다.)",{"thought":True})],"ep4:deadline")
    $ r13_flag("tok_detained")
    return
