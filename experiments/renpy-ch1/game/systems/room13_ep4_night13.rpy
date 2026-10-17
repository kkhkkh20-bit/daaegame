# 에피소드 ④ 「13호의 밤」 (8~10일). 대본: docs/EPISODE4_SCRIPT_FULL.md
#   편지를 전하던 사람이 먼저 죽었다.
#   재판(C1~C4, 10일 식당)은 기존 회의를 그대로 쓴다. 이 파일은 그 사이 8~9일과 재판 뒤를 채운다.
#   8일: 보호실 면회 거절, 부리의 수첩, 초롱의 예고(밤에 엄마 편지를 직접 전하겠다), 너울의 엿들은 말,
#        따닥의 예고(새벽에 통로를 잰다), 아이들의 쪽지. 밤에 초롱이 종탑 아래에서 죽는다(살리지 못했다면).
#   9일 새벽: 할머니의 차(목도리에 핀이 없다). 통로 안에서 따닥이 언다(살리지 못했다면).
#   살리기는 제시로만: 초롱 ← 너울의 말(+ 바둑이가 곁을 지킨다), 따닥 ← 수첩과 레버(+ 톡의 쐐기).
#   재판 뒤: 할머니가 입증됐으면 따닥의 죽음을 짧게 따진다(회의 Q4). 부리의 모자, 초롱의 등, 그림책.
#   깃발 접두사 nt_, 장면 r13_nt_*. 13호 사건이 실제로 일어났을 때만(case_state=="occurred").
init 155 python:
    for _key,_name,_est,_not in (
        ("N01","할아버지의 탐정 수첩","부엉이 할아버지의 낡은 수첩. 마지막 장에 \"13호 책장 뒤 — 바람\". 그래서 무슨 뜻? 책장 뒤가 벽이 아니라 빈 길이다.","그 길로 누가 다녔는지는 적혀 있지 않다."),
        ("N02","너울의 말","회관 뒤에서 엿들은 말. 너울: \"할머니 부탁이오. 등불지기가 품은 편지를 가져오시오.\" 그래서 무슨 뜻? 할머니가 엄마 편지를 노린다. 오늘 밤 종탑 길에서.",""),
        ("N03","따닥의 말","따닥: \"내일 새벽에 통로 길이를 한 번 더 재 보려고요. 할머니께도 말씀드렸어요.\" 그래서 무슨 뜻? 할머니는 따닥이 새벽에 통로 안에 있을 걸 알았다.",""),
        ("N05","젖은 편지","초롱이 끝까지 품에 안고 있던 편지. 남은 글자: \"다람아, 엄마 여기 있…\" 그래서 무슨 뜻? 엄마는 살아 있고, 다람에게 편지를 보냈다.",""),
        ("N06","엄마의 편지","초롱이 직접 전한 편지. \"이 마을로 오라는 편지는 엄마가 쓴 게 아니야. 할머니를 조심해.\" 그래서 무슨 뜻? 초대 편지는 할머니 손에서 나왔다.",""),
        ("N07","내려진 레버","9일 새벽, 따닥이 통로 안에 있을 때 누군가 주방에서 판자 문 레버를 당겨 내렸다. 판자 문은 그 레버로만 여닫힌다. 그래서 무슨 뜻? 판자 문은 저절로 닫히지 않는다. 누가 주방에서 내렸다.",""),
        ("N08","이름 판 맨 아래 이름","광장 이름 판 맨 아래, 반쯤 긁혀 나간 작은 이름. 네 해 전 날짜, 촌장 집과 같은 성. 그래서 무슨 뜻? 첫 번째로 제단에 간 사람은 촌장의 손녀다.",""),
        # 0.18.90 동물 특징으로 알리바이 확인: 딱따구리는 통로가 좁아 날개를 못 펴고, 부리로 벽을 두드렸다.
        ("N09","통로 벽의 부리 자국","판자 문 옆 돌벽 이음새에 부리로 쪼은 자국이 한 줄로 길게 나 있다. 처음엔 깊고 갈수록 얕다. 통로는 어깨 폭이라 날개를 펼 수 없다. 그래서 무슨 뜻? 따닥은 갇힌 뒤 오래 벽을 두드렸다. 벽 너머 주방에 있던 사람은 그 소리를 들을 수 있었다.","누가 주방에 있었는지는 이것만으로 모른다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not or "이것만으로 다른 사실까지 정할 수는 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(N01="할아버지 수첩",N02="너울의 말",N03="따닥의 말",N05="젖은 편지",N06="엄마의 편지",N07="내려진 레버",N08="이름 판 맨 아래",N09="부리 자국")

    def r13_nt_active():
        s=store.room13 or {}
        return s.get("case_state")=="occurred"

    def r13_nt_has_lever():
        return any(r13_has(k) for k in ("E05","E37","E04"))

    # 죽은 사람은 마을에 없다. 반쯤 산 사람은 진료소에 있다.
    _r13_nt_where=r13_where
    def r13_where(person):
        if person=="resident_lamplighter":
            if r13_has("chorong_dead"):return None
            if r13_has("nt_chorong_half") and r13_has("nt_night8"):return "clinic"
        if person=="resident_ttadak":
            if r13_has("ttadak_dead"):return None
            if r13_has("nt_ttadak_half") and r13_has("nt_dawn9"):return "clinic"
        return _r13_nt_where(person)

    _r13_nt_present=r13_present
    def r13_present(person,key,identity=False):
        if person=="resident_ppul" and key=="N08" and not r13_has("fair_hearing"):
            r13_flag("fair_hearing","nt_ppul_promise")
            return [("resident_ppul","……그건 내 손녀 이름이오. 네 해 전, 첫 번째 겨울이었소."),
                ("resident_ppul","그 뒤로 나는 그게 법이라고 믿어야 했소. 그러지 않으면 내가 그 애를 보낸 게 되니까."),
                ("dad","그러니 이번엔 증거로 판단해 주십시오. 또 누군가를 그렇게 보내기 전에."),
                ("resident_ppul","……알겠소. 증거대로 하겠소. 판결도 내가 집행하겠소.")]
        return _r13_nt_present(person,key,identity)

    # ---- 회의 Q4: 따닥의 죽음 (재판 뒤, 식당) ----
    R13_DEBATE_SEATS["ep4"]=["resident_seori","resident_ppul","granny","resident_tosil","nabi","buri"]
    R13_DEBATE_STANCE["ep4"]=("사고라고 본다","모르겠다","누가 닫았다고 본다")
    R13_EP_MEETING_PLACE["ep4"]="council"
    R13_EP_MEETING_HEADER["ep4"]="식당 회의 · 10일째"
    R13_DEBATE["Q4"]=dict(title="판자 문을 닫은 사람",session="ep4",chair="resident_seori",
        statements=[
            dict(id="s1",who="resident_ppul",text="목수는 혼자 통로에 들어갔다가 【문이 저절로 닫혀】 갇혔소. 딱한 사고요.",
                accept=["N07"],
                broken_by={"N07":[("dad","통로 안쪽 판자 문은 주방 손잡이를 내려야만 닫힙니다. 저절로는 안 닫힙니다."),
                    ("dad","그리고 따닥 씨는 안에서 '누구요, 열어 주시오'라고 썼습니다. 주방은 그 벽 바로 너머입니다."),(None,"……")]},
                # 0.19.15: 따닥이 살아 진료소에 있는 판(nt_ttadak_half)에는 연필 글씨를 보지 못했다. 따닥 본인의 말로 잇는다.
                broken_if={"N07":("nt_ttadak_half",[("dad","통로 안쪽 판자 문은 주방 손잡이를 내려야만 닫힙니다. 저절로는 안 닫힙니다."),
                    ("dad","따닥 씨가 직접 말했습니다. 새벽에 주방 쪽에서 쇠 소리가 났고, 누가 손잡이를 내렸다고요. 주방은 그 벽 바로 너머입니다."),(None,"……")])},
                hint="9일 아침 주방에서 본 것.",
                wrong=("resident_ppul","그게 사고가 아니라는 증거요?")),
            dict(id="s2",who="granny",text="새벽 주방엔 【늘 토실이가 불을 넣는단다】. 그 어린 게 안에 사람이 있는 줄 알았겠니.",
                accept=["N03"],
                broken_by={"N03":[("dad","따닥 씨가 그 전날 제게 말했습니다. '내일 새벽에 통로를 잰다. 할머니께도 말씀드렸다.' 안에 사람이 있다는 걸 아는 분은 할머니였습니다."),
                    (None,"맨 뒷줄에서 의자가 넘어지는 소리가 났다."),
                    ("resident_tosil","나 아니야! 할머니가 그날은 새벽에 주방 오지 말라고 했잖아. 그래서 나 안 갔어. 이불 속에 있었어. 나 아니야……!"),
                    (None,"다람이 토실 쪽을 보았다. 사흘 전 자기가 몰렸던 자리와 같은 자리였다."),
                    (None,"……"),
                    ("granny","……그래요. 토실이는 아니에요. 우리 토실이는 그날 이불 속에 있었어요.")]},
                hint="따닥이 새벽에 들어간다는 걸 미리 들은 사람.",
                wrong=("granny","그게 할머니랑 무슨 상관이에요?")),
            dict(id="s3",who="granny",text="그럼 그 새벽 【주방엔 아무도 없었던 거란다】. 두드리는 소리를 들었으면 누구라도 열어 줬겠지.",
                accept=["N09"],
                broken_by={"N09":[("dad","통로는 어깨 폭입니다. 따닥 씨는 날개를 펼 수도 없었습니다. 그래서 부리로 문 옆 벽을 쪼았습니다."),
                    ("dad","처음엔 깊게, 갈수록 얕게. 한 줄로 길게 나 있었습니다. 오래 두드렸다는 뜻입니다. 그 벽 너머가 주방입니다."),
                    ("dad","그리고 그 새벽, 할머니는 제게 김이 나는 차를 가져오셨습니다. 그 시각에 불이 있는 곳은 주방 화덕입니다."),
                    (None,"할머니가 무릎 위에 두 손을 포갰다."),
                    ("granny","……차가 식을까 봐 서둘렀지요.")]},
                hint="따닥이 안에서 남긴 소리의 흔적. 그리고 그 새벽 아빠가 받은 것.",
                wrong=("granny","그게 할머니가 주방에 있었다는 뜻인가요?")),
        ],
        conclusion=dict(prompt="판자 문은?",
            options=[("correct","안에 따닥이 있는 걸 아는 사람이 닫았다. 그건 할머니다"),
                ("over","토실이 실수로 내렸다"),
                ("weak","따닥은 통로를 너무 많이 알았다")],
            correct=[("resident_seori","문은 저절로 닫히지 않았습니다. 안에 사람이 있는 걸 아는 사람이 닫았습니다. 그 말을 미리 들은 사람 가운데 그 새벽 주방에 있던 사람은 할머니 한 분입니다.")],
            over=("resident_seori","아이는 그날 주방에 없었습니다. 아이에게 또 짐을 지우지 마십시오."),
            weak=("resident_seori","그건 까닭입니다. 누가 했는지가 아닙니다.")),
        sway=["resident_seori","nabi","buri"])

    R13_EVENT_OFFERS.update({
        "r13_nt_overhear":("회관 뒤 장작더미 그늘에서 너울이 순찰대원들에게 낮게 말한다",["nt_overhear_missed"],"너울이 순찰대원들을 데리고 종탑 쪽으로 갔다는 말을 들었다."),
    })
    R13_OFFER_ACTORS.update({"r13_nt_overhear":("neoul",None)})

# =========================================================
# 장면
# =========================================================
label r13_nt_events:
    if not r13_nt_active():
        return
    $ _ntd,_ntp,_ntloc=room13["day"],room13["period"],room13["location"]
    if _ntd==R13_CASE_DAY+1 and not r13_has("nt_dawn8"):
        call r13_nt_dawn8
        return
    if _ntd==R13_CASE_DAY+1 and _ntloc=="square" and not r13_has("nt_chorong_signal"):
        call r13_nt_chorong_signal
    if _ntd==R13_CASE_DAY+1 and _ntp==1 and _ntloc=="square" and not r13_has("nt_overheard"):
        $ r13_offer("r13_nt_overhear")
    if _ntd==R13_CASE_DAY+1 and _ntp>=1 and _ntloc in ("inn","hall","kitchen") and not r13_has("nt_ttadak_signal"):
        call r13_nt_ttadak_signal
    if _ntd==R13_CASE_DAY+1 and _ntp>=2 and not r13_has("nt_night8"):
        call r13_nt_night8
    if _ntd==R13_CASE_DAY+2 and not r13_has("nt_dawn9"):
        call r13_nt_dawn9
    return

label r13_nt_dawn8:
    $ r13_flag("nt_dawn8")
    call r13_scene("council","8일 새벽 · 여관 식당","quiet")
    call r13_lines([(None,"다람이 끌려간 뒤 잠들지 못했다. 새벽, 식당에 불이 하나 켜져 있었다."),
        (None,"할머니가 난로 앞에 앉아 토실에게 그림책을 읽어 주고 있었다. 다람의 그림책이었다."),
        (None,"(그림책) 빨간 모자는 숲을 지나 할머니 집에 갔어요.",{"book":"U04-opening"}),
        (None,"(그림책) \"할머니, 귀가 왜 그렇게 커요?\" \"우리 아가 말을 더 잘 들으려고 그렇단다.\""),
        (None,"(그림책) 사냥꾼이 와서 늑대를 잡았어요."),
        ("resident_tosil","할머니는 늑대 아니지?"),
        ("granny","그럼. 할머니는 할머니지. 자, 이제 자렴."),
        ("granny","아이 아버지, 못 주무셨군요. 다람이 책이에요. 그 애한테 넣어 주려고 꺼내 왔어요. 혼자 있으면 무섭잖아요."),
        ("dad","(고마운 사람이다. 이 마을에서 우리 편은 이 사람뿐인지도 모른다.)",{"thought":True})],"nt:dawn8:book")
    call r13_scene("ep_holding_morning","보호실 앞","quiet")
    call r13_lines([("dad","아이 얼굴만 보겠습니다. 한 번만."),
        ("neoul","회의 전까지는 안 되오. 규칙이오."),
        ("dad","아이는 일곱 살입니다."),
        ("neoul","사람이 죽었소. 나이는 회의에서 따지시오."),
        (None,"높은 창 안쪽에서 작은 손바닥 하나가 유리에 붙었다가 떨어졌다."),
        (None,"숙소 앞 눈밭에 부리가 서 있었다. 할아버지의 회중시계를 손에 꼭 쥐고. 밤새 서 있었던 것 같았다."),
        ("buri","……아저씨 애가 할아버지를 죽였다고들 해요."),
        ("buri","근데 할아버지는 아저씨를 믿었어요. 첫날 저한테 그랬어요. \"저 사람은 듣는 사람이다.\""),
        ("buri","할아버지 탐정 수첩이에요. 아무한테도 안 보여 줬어요."),
        (None,"수첩 마지막 장. 떨리는 글씨. \"13호 책장 뒤 — 바람.\""),
        ("buri","할아버지는 마지막까지 뭘 찾고 있었어요. 그게 아저씨 애면…… 그래도 알고 싶어요."),
        ("dad","(책장 뒤에서 바람이 분다. 책장 뒤가 벽이 아니라는 뜻이다.)",{"thought":True})],"nt:dawn8:buri")
    $ r13_grant(["N01"],"부리가 건넨 할아버지의 수첩")
    # 서리는 범행 도구를 다시 대조하기로 한다(예전엔 엄마가 나타난 장면에서 열렸다).
    $ r13_flag("examination_agreed")
    menu:
        "“같이 찾아보자.”":
            call r13_lines([("buri","……네.")],"nt:dawn8:together")
            $ r13_flag("nt_buri_together")
        "“다람이는 아니야.”":
            call r13_lines([("buri","그건 아저씨가 아빠니까 하는 말이잖아요.")],"nt:dawn8:defend")
    $ r13_edit(location="square")
    return

label r13_nt_chorong_signal:
    call r13_here_scene
    $ r13_flag("nt_chorong_signal")
    if r13_has("chorong_dead"):
        return
    call r13_lines([(None,"초롱이 등 기름을 채우고 있었다. 나를 보더니 주위를 살피고 다가왔다."),
        ("resident_lamplighter","다람이 일, 들었어요. ……그리고 하나 더요."),
        ("resident_lamplighter","점검함에 또 편지가 들어 있었어요. 그분 글씨예요. 아버님 부인요."),
        ("resident_lamplighter","오늘은 순찰이 많아서 못 꺼냈어요. 밤에 등 다 켜고 나서 꺼내 갈게요."),
        ("resident_lamplighter","【오늘 밤엔 꼭 직접 전해 드릴게요. 종탑 쪽이 지름길이에요.】"),
        ("resident_lamplighter","어머님 소식, 제가 꼭 전해 드린다고 했잖아요.")],"nt:chorong:signal")
    menu:
        "이름 판을 본다":
            call r13_lines([(None,"광장 이름 판. 어제 새로 새긴 부엉이 할아버지의 이름."),
                (None,"맨 아래, 오래되어 반쯤 긁혀 나간 작은 이름 하나."),
                ("dad","(네 해 전 날짜다. 아이 이름 같다. 촌장 집 문패와 성이 같다.)",{"thought":True})],"nt:chorong:board")
            $ r13_grant(["N08"],"광장 이름 판을 직접 봄")
        "그냥 지나간다":
            pass
    return

label r13_nt_overhear:
    $ r13_flag("nt_overheard")
    call r13_scene("ep_hall_front","회관 뒤 · 장작더미 그늘","quiet")
    call r13_lines([("neoul","등불지기가 오늘 밤 품고 다니는 편지가 있소. 할머니께서 꼭 가져오라 하셨소."),
        ("neoul","종탑 길에서 기다리시오. 소리 내지 말고. 다치게 하지는 마시오. 편지만이오."),
        (None,"순찰대원 하나가 물었다. \"안 주면요?\""),
        ("neoul","……안 주게 두지 마시오."),
        ("dad","(할머니가? 엄마 편지를?)",{"thought":True})],"nt:overhear")
    $ r13_grant(["N02"],"회관 뒤에서 엿들은 너울의 말")
    if not r13_has("chorong_dead"):
        call r13_lines([(None,"해 질 녘, 초롱이 회관 앞 등을 켜러 왔다."),
            ("resident_lamplighter","아버님? 걱정 마세요. 종탑 길은 제가 눈 감고도 다녀요."),
            ("resident_lamplighter","편지는 직접 전해야 해요. 그분이 그렇게 부탁하셨어요. 아무 손도 거치지 말라고.")],"nt:chorong:dusk")
        menu:
            "너울의 말을 전한다":
                call r13_lines([("dad","방금 너울이 순찰대원들한테 말하는 걸 들었습니다. 오늘 밤 종탑 길에서 초롱 씨를 기다린답니다. 할머니 부탁으로, 그 편지를 가져가려고요."),
                    ("resident_lamplighter","……할머니가요? 그 할머니가 왜요."),
                    ("resident_lamplighter","그래도 편지는 제가 들고 가야 해요. 다른 길은 너무 멀어서, 가다가 등이 다 꺼져요.")],"nt:chorong:warned")
                if r13_has("badook_doubt") and (r13_has("kd_solved") or r13_has("badook_ally")):
                    call r13_lines([("resident_badook","무슨 일이에요? ……너울 씨가 그랬어요?"),
                        ("resident_badook","오늘 밤 제 순찰 길을 종탑 쪽으로 바꿀게요. 초롱 씨 옆에 붙어 있을게요. 정직한 게 제 유일한 재주예요.")],"nt:chorong:badook")
                    $ r13_flag("nt_chorong_safe")
                else:
                    call r13_lines([("resident_lamplighter","……알았어요. 먼 길로 갈게요.")],"nt:chorong:far")
                    $ r13_flag("nt_chorong_half")
            "“오늘은 가지 마세요.”":
                call r13_lines([("resident_lamplighter","아버님도 참. 저 이 일 십 년 했어요.")],"nt:chorong:no")
    if not r13_has("fair_hearing"):
        call r13_lines([(None,"회관 안. 촌장이 모레 회의에 쓸 의자를 세고 있었다."),
            ("dad","회의는 증거로만 판단하고, 판결은 그대로 집행해 주십시오. 그 약속을 받고 싶습니다."),
            ("resident_ppul","외지 사람이 지금 마을 법을 가르치려 하오?")],"nt:ppul")
        menu:
            "이름 판 맨 아래 이름을 보여 준다" if r13_has("N08"):
                call r13_lines(r13_present("resident_ppul","N08"),"nt:ppul:board", binding_route="dynamic:369")
            "식어 가는 돌을 보여 준다" if r13_has("W4"):
                call r13_lines([("resident_ppul","……숫자는 거짓말을 안 하오. 좋소. 이번엔 말이 아니라 증거로 하겠소.")],"nt:ppul:stone")
                $ r13_flag("fair_hearing","nt_ppul_promise")
            "오늘은 물러선다":
                call r13_lines([("resident_ppul","회의는 회의대로 하오. 집행은 마을이 정하오.")],"nt:ppul:no")
    $ r13_tick()
    return

label r13_nt_ttadak_signal:
    $ r13_flag("nt_ttadak_signal")
    call r13_scene("hall","여관 뒷벽","calm")
    call r13_lines([(None,"여관 뒤에서 망치 소리가 났다. 따닥이 처마 밑 판자에 못을 박고 있었다."),
        ("resident_ttadak","아, 13호 손님! 그 방 뒤에 길 있는 거 아세요? 판자 뜯다가 찾았어요. 아무한테도 말하지 마세요, 촌장님 일이라."),
        ("resident_ttadak","촌장님이 여관 뒷벽 도면을 내일 아침까지 달래요. 일당이 두 배예요. 두 배!"),
        ("resident_ttadak","【내일 새벽에 통로 길이를 한 번 더 재 보려고요.】 할머니께도 말씀드렸어요. 레버 좀 올려 두시라고."),
        ("resident_ttadak","할머니가 웃으시더라고요. \"추우니 단단히 입으렴.\"")],"nt:ttadak:signal")
    $ r13_grant(["N03"],"여관 뒷벽에서 따닥에게 들은 말")
    menu:
        "수첩과 레버 이야기를 한다" if r13_has("N01") and r13_nt_has_lever():
            call r13_lines([("dad","부엉이 할아버지가 마지막에 적은 겁니다. \"13호 책장 뒤 — 바람.\" 할아버지는 그 통로를 알고 나서 죽었습니다."),
                ("dad","그리고 통로 안쪽 판자 문은 주방 손잡이로만 여닫습니다. 그 문엔 안쪽 손잡이가 없습니다. 누가 손잡이를 내리면, 따닥 씨는 안에 갇힙니다."),
                ("resident_ttadak","……판자 문 안쪽엔 손잡이가 없긴 했어요. 그래도 누가 일부러 내리겠어요."),
                ("resident_ttadak","알았어요. 혼자는 안 들어가요. 근데 일당은 포기 못 해요. 누가 문을 못 닫게 붙잡아 주면 모를까.")],"nt:ttadak:warned")
            if r13_has("tok_cleared") and not r13_has("tok_detained"):
                call r13_lines([("resident_tok","손잡이요? 쐐기 하나면 돼요. 쇠 쐐기를 손잡이 밑에 박으면, 누가 당겨도 안 내려가요."),
                    ("resident_tok","오늘 밤 제가 박아 둘게요. 따닥이 판자 반 치씩 길게 자르는 버릇, 저는 아직 못 고쳐 줬거든요.")],"nt:ttadak:tok")
                $ r13_flag("nt_ttadak_safe")
            else:
                call r13_lines([("resident_ttadak","그럼 망치로 문을 괴어 둘게요.")],"nt:ttadak:hammer")
                $ r13_flag("nt_ttadak_half")
        "수첩만 보여 준다" if r13_has("N01") and not r13_nt_has_lever():
            call r13_lines([("resident_ttadak","바람 부는 거야 저도 알아요.")],"nt:ttadak:weak")
        "“조심하세요.”":
            call r13_lines([("resident_ttadak","위험하긴요. 돌 통로예요. 무너질 데도 없어요.")],"nt:ttadak:no")
    return

label r13_nt_night8:
    $ r13_flag("nt_night8")
    if r13_has("kids_club"):
        call r13_scene("ep_roof_night","8일 밤 · 지붕 위","night")
        call r13_lines([(None,"밤, 지붕 위. 솜이가 앞장서고, 콩이와 토실이 뒤따랐다."),
            ("resident_somi","보호실 창은 높아서 어른 팔은 안 닿아. 우리 팔은 닿아."),
            ("resident_kongi","구운 밤 세 개. 공짜야. 이번만."),
            ("resident_tosil","나도 썼어. \"다람아, 우리 할머니가 너 걱정 많이 해.\""),
            (None,"한참 뒤, 같은 틈으로 접힌 종이가 나왔다."),
            (None,"(쪽지) 아빠. 할아버지가 내 팔을 잡았어. 아팠어. 나는 손을 쳤어. 머리는 안 쳤어."),
            (None,"(쪽지) 촛대가 떨어져서 부러졌어. 나는 침대 밑에 들어갔어. 무서워서 눈 감았어."),
            (None,"(쪽지) 그다음에 쿵 소리 났어. 나 아니야."),
            (None,"(쪽지) 아빠한테 나 안 무섭다고 해 줘. ……조금만 무서워."),
            ("resident_somi","다람이가 이거 아빠한테만 주래. 우리는 안 읽었어. ……조금 읽었어."),
            ("dad","(촛대가 부러진 뒤에 일어난 일이 하나 더 있다.)",{"thought":True})],"nt:night8:note")
        if not r13_has("E06"):
            $ r13_grant(["E06"],"아이들이 보호실 창으로 받아 온 다람의 쪽지")
    else:
        call r13_lines([(None,"보호실 창은 밤새 어두웠다. 창 아래 눈밭에 오래 서 있었다. 안에서는 아무 소리도 나지 않았다.")],"nt:night8:nonote")
    call r13_scene("ep_belltower_night","8일 밤 · 종탑 아래","night")
    if r13_has("nt_chorong_safe"):
        call r13_lines([(None,"종탑 길 모퉁이. 그림자 둘이 서 있다가, 바둑이의 등불을 보고 멈췄다."),
            ("resident_badook","순찰대 바둑이예요. 이 시간에 여기서 뭐 하세요? ……얼굴 좀 보여 주실래요?"),
            (None,"그림자들이 광장 쪽으로 사라졌다."),
            ("resident_lamplighter","직접 전해 드린다고 했잖아요."),
            (None,"(편지) 다람아, 엄마 여기 있어. 조금만 기다려. 이 마을로 오라는 편지는 엄마가 쓴 게 아니야. 아빠한테 말해 줘. 할머니를 조심해."),
            ("resident_lamplighter","오늘 등은 같이 켜요. 저 혼자는 오늘 무서워서요.")],"nt:night8:safe")
        $ r13_grant(["N06"],"초롱이 직접 전한 엄마의 편지")
    elif r13_has("nt_chorong_half"):
        call r13_lines([(None,"강가 쪽 먼 길에서 초롱이 쓰러져 있었다. 이마가 찢기고, 등잔은 깨졌다. 숨은 붙어 있다."),
            ("resident_lamplighter","미안해요……. 빼앗겼어요. 편지. 그분 글씨였는데…….")],"nt:night8:half")
        $ r13_flag("mom_letter_taken")
    else:
        call r13_lines([(None,"등이 다 켜질 시간이 지났다. 광장 동쪽 등 셋이 아직 어두웠다. 초롱은 오지 않았다."),
            (None,"종탑 계단 아래. 눈 위에 깨진 등잔이 엎어져 있었다. 기름이 눈을 검게 적셨다."),
            (None,"계단 맨 아래에 초롱이 누워 있었다. 두 팔로 가슴을 꼭 끌어안은 채였다.",{"music":None,"sfx":"heartbeat"}),
            (None,"눈 위로 여러 사람의 발자국이 광장 쪽으로 흩어져 달아나 있었다."),
            (None,"……",{"dim":True}),
            (None,"초롱의 팔을 풀자, 품 안에서 젖은 편지 한 장이 나왔다. 남은 건 한 줄뿐."),
            (None,"(편지) 다람아, 엄마 여기 있…"),
            ("dad","(어머님 소식, 꼭 전해 드릴게요—. 오늘 낮에 웃으면서 한 말이다.)",{"thought":True}),
            ("dad","(이 사람은 끝까지 놓지 않았다. 남의 엄마 편지를.)",{"thought":True})],"nt:night8:dead")
        $ r13_flag("chorong_dead")
        $ r13_grant(["N05"],"초롱의 품에서 나온 젖은 편지")
        menu:
            "초롱 대신 광장 등을 켠다":
                call r13_lines([(None,"초롱의 허리춤에서 점검함 열쇠를 꺼냈다. 등 켜는 법은 몰랐다. 초롱이 하던 걸 떠올리며 하나씩 했다."),
                    (None,"동쪽 등 하나가 켜졌다. 둘. 셋."),
                    (None,"광장 너머, 보호실의 작은 창에 불빛이 비쳤다.")],"nt:night8:lamps")
                $ r13_flag("nt_lit_lamps")
            "순찰대를 부르러 간다":
                call r13_lines([("neoul","등불지기가 미끄러졌다고 하오. 계단이 얼었소."),
                    (None,"등은 그날 밤 꺼진 채였다.")],"nt:night8:guard")
    return

label r13_nt_dawn9:
    $ r13_flag("nt_dawn9")
    call r13_scene("guestroom","9일 새벽 · 임시 객실","quiet")
    call r13_lines([(None,"문 두드리는 소리. 할머니가 김이 나는 찻잔을 들고 서 있었다.")]+
        ([("granny","초롱이 일, 들었어요. 가엾어라. 계단이 얼어서 그랬다네요.")] if r13_has("chorong_dead") else [])+
        [("granny","이거 마시고 조금이라도 눈 붙이세요. 내일 아침이 회의잖아요. 아이 아버지가 쓰러지면 다람이는 누가 데려와요."),
        (None,"할머니가 돌아서며 목도리를 여몄다. 목도리에 핀이 없었다."),
        ("dad","(……핀 자리에 실이 조금 풀려 있었다.)",{"thought":True})],"nt:dawn9:tea", binding_route="dynamic:385")
    call r13_scene("kitchen","9일 아침 · 주방과 통로","quiet")
    if r13_has("nt_ttadak_safe"):
        call r13_lines([(None,"주방. 쇠 손잡이가 반쯤 내려오다 톡의 쐐기에 걸려 멈춰 있었다. 쐐기 위에 새로 긁힌 쇳가루."),
            ("resident_ttadak","손님! 새벽에 누가 주방에서 손잡이를 세게 당겼어요. 두 번이나요. 쐐기 아니었으면 저 갇혔어요."),
            ("resident_ttadak","……누가 그랬을까요. 제가 들어간다는 거, 손님이랑 톡 씨, 할머니 말고는 몰랐는데.")],"nt:dawn9:safe")
        $ r13_grant(["N07"],"쐐기에 걸린 레버와 따닥의 말")
    elif r13_has("nt_ttadak_half"):
        call r13_lines([(None,"판자 문이 망치 위에서 한 뼘 덜 닫혀 있었다. 따닥은 그 틈에 두 손을 넣은 채 웅크려 있었다. 숨은 있다."),
            ("resident_ttadak","새벽에…… 주방 쪽에서 쇠 소리가 났어요. 누가 손잡이를 내렸어요. 손이…… 손이 안 펴져요."),
            (None,"문 옆 돌벽 이음새에 쪼은 자국이 한 줄로 길게 나 있었다."),
            ("resident_ttadak","통로가 좁아서 날개도 못 폈어요. 그래서 부리로 벽을 쪼았어요. 주방까지 들리라고. 한참을요.")],"nt:dawn9:half")
        $ r13_grant(["N07","N09"],"내려진 레버와 따닥의 말")
    else:
        call r13_lines([(None,"아침, 여관 뒷벽의 망치 소리가 들리지 않았다."),
            (None,"주방. 쇠 손잡이가 아래로 내려져 있었다."),
            ("nabi","저 아니에요. 할머니가 새벽에 저를 빨래터로 먼저 보내셨어요. 토실이도 오늘은 주방에 오지 말라고 하셨고요."),
            (None,"손잡이를 올리고 13호로 갔다. 책장이 열렸다."),
            (None,"통로 안, 판자 문 바로 앞에 따닥이 문에 기대 앉아 있었다. 무릎에 줄자를 감은 채. 눈썹에 서리가 앉아 있었다.",{"music":None,"sfx":"heartbeat"}),
            (None,"판자 문 안쪽에 연필 글씨가 있었다. 처음엔 또박또박, 나중엔 삐뚤빼뚤."),
            (None,"(글씨) 누구요. 열어 주시오."),
            (None,"(글씨) 따닥이오. 안에 있소."),
            (None,"(글씨) 추움"),
            (None,"문 옆 돌벽 이음새에 쪼은 자국이 한 줄로 길게 나 있었다. 처음엔 깊게, 갈수록 얕게. 따닥의 부리 끝이 깨져 있었다."),
            (None,"통로는 어깨 폭이었다. 날개를 펼 자리는 없었다."),
            (None,"……",{"dim":True}),
            ("dad","(이 문은 저절로 닫히지 않는다. 누군가 주방에서 손잡이를 내렸다.)",{"thought":True}),
            ("dad","(따닥이 새벽에 여기 들어간다는 걸 미리 들은 사람은—.)",{"thought":True})]+
            ([("resident_tok","따닥……. 판자를 늘 반 치씩 길게 잘랐어요. 모자라는 것보다 남는 게 낫다고."),
              ("resident_tok","도면은 다 못 그렸네. 내가 마저 그릴게.")] if r13_has("tok_cleared") else []),"nt:dawn9:dead", binding_route="dynamic:388")
        $ r13_flag("ttadak_dead")
        $ r13_grant(["N07","N09"],"내려진 레버와 통로 안에 남은 글씨·부리 자국")
    return

# ---- 재판 뒤 (room13.rpy r13_verdict에서 부른다) ----
label r13_nt_after_trial:
    if not r13_nt_active() or r13_has("nt_after"):
        return
    $ r13_flag("nt_after")
    if room13.get("trial_result")=="culprit_proven" and r13_has("N03") and r13_has("N07") and (r13_has("ttadak_dead") or r13_has("nt_ttadak_half")):
        call r13_scene("council","식당 · 따닥의 일","hearing")
        call r13_lines([("resident_seori","하나 더 있습니다. 9일 새벽, 통로 안에서 목수 따닥 씨가 얼었습니다." if r13_has("ttadak_dead") else "하나 더 있습니다. 9일 새벽, 목수 따닥 씨가 통로 안에 갇혔습니다. 손이 얼어 지금 진료소에 있습니다.")],"nt:q4:open", binding_route="dynamic:389")
        call r13_debate_run("Q4")
        if _return:
            $ r13_flag("nt_ttadak_proven")
            call r13_lines([(None,"할머니가 천천히 일어섰다. 아무도 할머니를 붙잡지 않았다."),
                (None,"할머니는 맨 뒷줄로 걸어가, 넘어진 의자를 세우고, 토실의 목도리를 다시 여며 주었다."),
                ("granny","토실아. 할머니 없어도 밥 거르지 말렴. 나비 말 잘 듣고. 밤에 무서우면 나비 방에 가렴."),
                ("resident_tosil","할머니 늑대 아니지? 그치?"),
                (None,"……"),
                ("granny","……그럼. 할머니는 할머니지."),
                ("granny","다람이 참 착한 아이란다. 그 애 엄마를 꼭 닮았지."),
                ("granny","내가 왜 그랬는지는 묻지 말렴. 아이 아버지는 아직 그걸 들을 수 없단다."),
                ("daram","(작게) ……아빠. 할머니가 나 그림책 넣어 줬어.")],"nt:q4:granny")
    if r13_has("nt_buri_together") and room13.get("daram_state")=="with_dad":
        call r13_scene("winter_square","식당 앞 계단 · 할아버지의 모자","quiet")
        call r13_lines([(None,"부리가 낡은 탐정 모자를 들고 다람 앞에 섰다. 모자 끝이 해져 있었다."),
            ("buri","할아버지 거야. 너 가져."),
            ("daram","나 할아버지 때렸는데……?"),
            ("buri","할아버지가 그랬어. 탐정은 듣는 사람이라고."),
            (None,"부리가 모자를 다람 머리에 씌워 주었다. 너무 커서 눈까지 내려왔다."),
            ("buri","너는 들었잖아. 할아버지가 아파서 네 손목을 잡은 거라는 거. 나는 그거 몰랐어."),
            ("daram","……할아버지 손, 아팠겠다."),
            ("buri","응. 근데 이제 안 아파."),
            ("daram","부리 오빠. 나 이거 잘 쓸게. 엄마 찾으면 엄마한테도 보여 줄게.")],"nt:after:hat")
        $ r13_flag("owl_hat")
    if r13_has("nt_lit_lamps"):
        call r13_scene("winter_square","광장 · 초롱의 등","quiet")
        call r13_lines([(None,"광장 이름 판에 새 이름이 새겨져 있었다. 초롱."+(" 따닥." if r13_has("ttadak_dead") else "")),
            (None,"판 앞에 등이 하나 놓여 있었다. 그 곁에 늙은 토끼 한 분이 서 있었다. 초롱을 닮은 귀였다.",{"show":"chorong_mother","expression":"anxious"}),
            (None,"초롱의 어머니가 말했다. \"그저께 밤에 그 애 대신 켜 주셨다지요. 동쪽 등 셋. 우리 집 창에서 보였어요. 그 애가 돌아온 줄 알았어요.\"",{"show":"chorong_mother","pose":"offer_lantern"}),
            (None,"\"그 애가 늘 말했어요. 남의 소식을 전하는 건 그 사람 하루를 지켜 주는 일이라고.\""),
            ("daram","……따뜻해."),
            ("daram","할머니. 초롱 아저씨가 우리 엄마 편지 지켜 줬어. 끝까지.")],"nt:after:lamp", binding_route="dynamic:392")
        $ r13_flag("chorong_lamp")
    elif r13_has("nt_chorong_safe"):
        call r13_scene("winter_square","광장 · 초롱의 등","calm")
        call r13_lines([("resident_lamplighter","오늘은 다람이가 켜 볼래?"),
            (None,"다람이 등을 하나 켰다.")]+([("daram","오늘은 이름 판에 새 이름 없지?")] if not r13_has("ttadak_dead") else []),"nt:after:lamp_alive", binding_route="dynamic:393")
    if room13.get("daram_state")=="with_dad":
        call r13_lines([("daram","아빠, 이거 내가 읽어 줄게. 보호실에서 백 번 읽었어."),
            (None,"(그림책) 빨간 모자는 숲을 지나 할머니 집에 갔어요.",{"book":"U04-opening"}),
            (None,"(그림책) \"할머니, 손이 왜 그렇게 커요?\" \"우리 아가를 꼭 안아 주려고 그렇단다.\"",{"book":"U04-ending"}),
            ("daram","……아빠. 할머니 손은 커?")],"nt:after:book")
    return
