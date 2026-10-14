# 1주차 새 사건 3개 (docs/EVENT_CATALOG.md G·L·I·S·T, 0.18.11)
#   ① 엄마의 흔적 — G 피코의 초상(2~3일 낮 광장) + L 슬링의 편지(2~4일 낮 우체국).
#        엄마 초상을 보여 주면 2주차 답장이 이틀 빨라진다. 편지를 엿보게 두면 경고가 새고(2주차 추적),
#        가짜 편지를 흘리면 4일 저녁 할머니가 여관을 비운다 → 그날 사건이 일어나지 않는다.
#   ② 벽 속의 길 — I 따닥의 증축(2~4일 오후 여관) + S 뭉치의 현장 물건(5~6일 복도).
#        따닥의 증축 기록(H7)은 재판 C1에서 직접 열어 본 통로(E05) 대신 쓸 수 있다. 따닥이 증언에 동의해야 한다.
#   ③ 재판 전의 유혹 — T 거짓 증언 팔기(6일 낮 입구·창고). 사서 쓰면 재판에서 반드시 깨지고, 촌장이 판결 집행을 거부한다.
init 110 python:
    for _key,_name,_est,_not in (
        ("H7","따닥의 증축 기록","따닥이 여관 뒤에 덧지은 벽 안쪽에 13호 책장 뒤로 이어지는 옛 통로 일부가 들어 있다. 공사 때 직접 보았다.","그날 밤 누가 그 통로를 지났는지는 이 기록으로 알 수 없다."),
        ("H8","뜯긴 13호 봉인","사건 뒤 봉해 둔 13호 문 봉인을 뭉치가 뜯고 들어가 물건을 꺼냈다.","뭉치가 무엇을 만졌는지는 뭉치의 말뿐이다."),
        ("H9","할머니가 엿본 편지","할머니가 슬링에게 일자리를 빌미로 여관 손님 편지를 몰래 열어 보게 했다.","어떤 편지를 왜 보려 했는지는 할머니만 안다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind="기록",establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["W9"]=dict(id="W9",name="모모의 수집",kind="기록",establishes="모모 관장은 '옛 마을 물건'이면 무엇이든 산다. 사건 물건도 값을 더 쳐 준다.",does_not_establish="모모가 무엇을 어디에 쓰는지는 박물관 사람들도 모른다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(H7="증축 기록",H8="뜯긴 봉인",H9="엿본 편지",W9="모모의 수집")

    # C1: the extension record can stand in for the operated passage, with the builder's consent.
    for _st in R13_DEBATE["C1"]["statements"]:
        if "E05" in _st.get("accept",[]):
            _st["accept"]=list(_st["accept"])+["H7"]
            _st.setdefault("need_consent",{})["H7"]="ttadak_witness"
            _st.setdefault("consent_lines",{})["H7"]=[("resident_seori","따닥 씨는 오늘 나오지 않았습니다. 기록만으로는 그 벽 안을 누가 봤는지 확인할 수 없어요."),
                ("dad","(따닥이 직접 말해 줘야 했다.)",{"thought":True})]
            _st.setdefault("broken_by",{})["H7"]=[("resident_ttadak","여관 뒤 벽은 내가 덧지었소. 벽 안에 옛 통로가 있었고, 13호 책장 뒤로 이어지오. 내 눈으로 봤소."),
                ("seryeon","……그 방에 다른 길이 있었다고요?")]
    for _c in ROOM13["claims"]:
        if _c["id"]=="C1":
            _c["support_sets"]=list(_c["support_sets"])+[["E04","H7"],["H7","E37"]]

    R13_FAKE_TESTIMONY_LINES=[
        ("resident_siluk","제가 봤어요! 그날 밤 할머니가 2층으로 올라가는 걸!"),
        ("resident_seori","그 시각 실룩 씨는 마구간 장부에 이름을 적었습니다. 여기 글씨가 있어요."),
        ("resident_siluk","……그, 그건."),
        ("resident_ppul","돈 받고 말하는 증인을 데려온 쪽의 판결을 내가 집행할 수는 없소. 아이는 풀어 주겠소. 그 이상은 안 되오."),
        ("dad","(쉬운 길이 가장 비쌌다.)",{"thought":True})]

    ROOM13["topics"].update({
        "portrait_sling":_ep_topic("resident_sling","엄마 초상을 보여 준다",(2,7),need=["mom_portrait"],not_flags=["portrait_known"],flags=["portrait_known"],lines=[
            ("resident_sling","……이분, 밤마다 편지를 부치러 오셨어요. 받는 곳은 늘 비워 두고요."),
            ("resident_sling","초롱 아저씨가 그 편지를 받아 갔어요. 저는 그것밖에 몰라요.")]),
        "portrait_lamplighter":_ep_topic("resident_lamplighter","엄마 초상을 보여 준다",(2,7),need=["mom_portrait"],not_flags=["portrait_lamp_seen"],flags=["portrait_lamp_seen","lamplighter_trust"],lines=[
            ("resident_lamplighter","……잘 그렸네요. 이 얼굴이면 제가 아는 분이 맞아요."),
            ("resident_lamplighter","지금 어디 있는지는 저도 몰라요. 하지만 답장을 받으면, 이 그림 덕에 바로 알아볼 수 있겠어요.")]),
    })
    R13_W2E_NOTES.extend([
        ("fake_letter_planted","가짜 편지 한 장이 할머니를 그날 밤 여관 밖으로 내보냈다."),
        ("family_items_lost","13호에 두고 온 우리 짐 일부는 끝내 돌아오지 않았다."),
        ("fake_testimony_exposed","돈 주고 산 증언은 재판에서 무너졌다."),
    ])
    R13_CARRY_GOOD.extend([
        (lambda:r13_has("siluk_owes"),["transport_terms"],
            [("resident_siluk","마구간 썰매 내드릴게요. 그날 거짓말 안 시켜 주신 값이에요.")]),
    ])

    _r13_w1c_action_done=r13_w2_action_done
    def r13_w2_action_done(key,started_at=None):
        _r13_w1c_action_done(key,started_at)
        # The lamplighter knows Mom's face from the portrait: the reply comes two days sooner.
        if key=="w2_reply" and (r13_has("portrait_known") or r13_has("portrait_lamp_seen")) and store.room13.get("reply_due") is not None:
            n=winter_copy.deepcopy(store.room13);n["reply_due"]=max(r13_abs_time()+1,n["reply_due"]-2);store.room13=n

label r13_w1c_events:
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    if 2<=_d<=3 and _p<=1 and _loc=="square" and not r13_has("ev_g_done"):
        call r13_w1c_portrait
    if 2<=_d<=4 and _p<=1 and _loc=="post" and not r13_has("ev_l_done"):
        call r13_w1c_letters
    if 2<=_d<=4 and _p==1 and _loc=="inn" and not r13_has("ev_i_done"):
        call r13_w1c_extension
    if _d==4 and _p>=2 and room13["case_state"]=="pending" and r13_has("fake_letter_planted") and not r13_has("fake_letter_night"):
        call r13_w1c_fake_night
    if 5<=_d<=6 and _loc=="hall" and room13["case_state"]=="occurred" and not r13_has("ev_s_done"):
        call r13_w1c_seal
    if _d==6 and _p<=1 and _loc in ("gate","store") and room13["case_state"]=="occurred" and not r13_has("ev_t_done"):
        call r13_w1c_testimony
    if _d>=8 and r13_has("letters_safe") and r13_has("pursuit_active") and not r13_has("pursuit_managed"):
        call r13_lines([("resident_sling","편지는 제가 할머니 몰래 돌렸어요. 뒤쫓는 사람은 엉뚱한 편지만 들고 갔어요.")],"w1c:letters:safe")
        $ r13_flag("pursuit_managed")
    return None

# ---- G. 피코의 초상 ----
label r13_w1c_portrait:
    $ r13_flag("ev_g_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"광장 구석에서 피코가 낡은 판자에 물감을 문지르고 있었다. 그림 속 사람은 백 년 전 옷을 입고 있었다."),
        ("resident_piko","……'옛 마을 초상'이에요. 모모 관장님이 이런 걸 사 줘요. 오늘 못 팔면 저녁을 굶어요.")],"w1c:portrait:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "가짜라고 모모 관장에게 알린다":
                call r13_lines([("resident_momo","……물감이 아직 마르지도 않았군요. 알려 줘서 고맙소. 사례요."),
                    ("resident_piko","……")],"w1c:portrait:expose")
                $ r13_cash(6,"모모 관장의 사례")
                $ r13_flag("piko_hostile")
            "모른 척한다":
                pass
            "엄마 초상을 그려 달라고 한다 (5냥)" if r13_cash_now()>=5 and not r13_has("mom_portrait"):
                $ r13_cash(-5,"피코에게 맡긴 엄마 초상")
                call r13_lines([("dad","제 아내입니다. 눈매는 이렇고, 왼쪽 눈썹에 작은 흉이 있어요."),
                    ("daram","엄마는 웃을 때 코를 찡그려!"),
                    (None,"피코는 가짜 초상을 뒤집어 놓고 새 판자에 그렸다. 저녁이 되기 전에 엄마 얼굴이 나왔다."),
                    ("resident_piko","이건 진짜예요. 진짜를 그린 건 오랜만이네요.")],"w1c:portrait:mom")
                $ r13_flag("mom_portrait","piko_ally")
            "구운 밤을 건네 준다" if r13_has("own:snack"):
                $ r13_use_item("snack")
                call r13_lines([("resident_piko","……오늘은 이걸로 버틸게요. 가짜는 안 팔아요.")],"w1c:portrait:snack")
                $ r13_flag("piko_ally")
                $ _ep_loop=True
            "그만 간다":
                pass
    return

# ---- L. 슬링의 편지 ----
label r13_w1c_letters:
    $ r13_flag("ev_l_done")
    call r13_ev_here("search")
    call r13_lines([(None,"우체국 안쪽 화덕 위에서 주전자가 김을 뿜고 있었다. 슬링이 봉투 하나를 김에 대고 있었다."),
        ("resident_sling","……! 아, 아니에요. 봉투가 젖어서 말리는 거예요.")],"w1c:letters:open")
    menu:
        "모른 척한다":
            call r13_lines([(None,"슬링은 봉투를 열어 한 줄을 베꼈다. 받는 사람 칸에 여관 이름이 보였다.")],"w1c:letters:ignore")
            $ r13_flag("warning_exposed")
        "현장에서 붙잡는다":
            call r13_lines([("dad","편지를 여는 겁니까?"),
                ("resident_sling","……할머니가 시켰어요. 손님 편지 중에 '부인'이 보낸 게 있으면 베껴 오라고. 안 그러면 일자리가 없대요.")],"w1c:letters:catch")
            $ r13_grant(["H9"],"슬링이 털어놓은 편지 엿보기")
            $ r13_flag("know_granny_reads")
            menu:
                "가짜 편지를 흘리게 한다":
                    call r13_w1c_fake_letter
                "다시는 하지 말라고 한다":
                    call r13_lines([("resident_sling","……네. 대신 할머니한테는 아무 편지도 없었다고 할게요.")],"w1c:letters:stop")
                    $ r13_flag("letters_safe","sling_ally")
        "너울에게 알린다":
            call r13_lines([("neoul","우체국 일은 우체국 일이오. 슬링, 너는 오늘부터 나오지 마라."),
                ("resident_sling","……")],"w1c:letters:neoul")
            $ r13_flag("sling_hostile")
        "슬링을 달랜다" if r13_has("portrait_known") or r13_cash_now()>=3:
            if not r13_has("portrait_known"):
                $ r13_cash(-3,"슬링의 하루 품삯")
            call r13_lines([("dad","일자리 때문이면, 오늘 몫은 제가 내겠습니다. 편지는 그대로 보내 주세요."),
                ("resident_sling","……정말요? 그럼 앞으로 할머니한테 갈 편지는 제가 먼저 보여 드릴게요.")],"w1c:letters:calm")
            $ r13_grant(["H9"],"슬링이 털어놓은 편지 엿보기")
            $ r13_flag("letters_safe","sling_ally","know_granny_reads")
            menu:
                "가짜 편지를 흘리게 한다":
                    call r13_w1c_fake_letter
                "그대로 둔다":
                    pass
    return

label r13_w1c_fake_letter:
    call r13_lines([("dad","할머니께 이 쪽지를 베껴 드리세요. '목요일 밤, 북쪽 초소에서 기다린다.' 서명은 비워 두고요."),
        ("resident_sling","……할머니가 이걸 믿으면요?"),
        ("dad","그날 밤 할머니가 어디로 가는지 보게 되겠죠.")],"w1c:letters:fake")
    $ r13_flag("fake_letter_planted","letters_safe","sling_ally")
    return

label r13_w1c_fake_night:
    $ r13_flag("fake_letter_night")
    call r13_scene("hall","목요일 저녁 · 여관 2층 복도","night")
    call r13_lines([(None,"해가 지자 할머니가 등잔을 들고 계단을 내려갔다. 손에는 담요와 굵은 끈이 들려 있었다."),
        ("granny","잠깐 볼일이 있어요. 아이는 방에 있게 하세요."),
        ("dad","(가짜 편지의 시각이다.)",{"thought":True})],"w1c:night:open")
    menu:
        "할머니를 따라간다":
            call r13_lines([(None,"할머니는 북쪽 초소 처마 밑에서 등잔을 낮췄다. 끈을 담요 밑에 감추고, 길 쪽만 보았다."),
                ("resident_lamplighter","……할머니? 이 시간에 초소엔 왜."),
                ("granny","누가 올 거예요. 아이 엄마가."),
                ("dad","(아이 엄마를 기다리는 사람이 끈을 숨기고 있다. 초롱도 봤다.)",{"thought":True})],"w1c:night:follow")
            $ r13_flag("granny_lure_seen","prevention_witness")
        "다람이와 방에 남는다":
            call r13_lines([(None,"할머니가 나간 뒤 여관은 조용했다. 다람이는 내 무릎을 베고 잠들었다.")],"w1c:night:stay")
    call r13_scene("room","13호실","night")
    call r13_lines([("resident_owlgp","할머니가 초소 쪽으로 가는 걸 봤소. 오늘 밤은 여기 오지 않겠군."),
        ("resident_owlgp","부인에게 받은 걸 돌려드리겠소. 베껴 둔 기록이오."),
        (None,"그날 13호에서는 아무도 다치지 않았다.")],"w1c:night:safe")
    $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",period=3,location="inn")
    $ r13_flag("victim_protected")
    $ r13_grant(["E17"],"살아 있는 어르신이 간직해 온 베낀 기록")
    return

# ---- I. 따닥의 증축 ----
label r13_w1c_extension:
    $ r13_flag("ev_i_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"여관 뒷벽에서 따닥이 판자를 덧대고 있었다. 새 판자 틈으로 오래된 벽돌과 좁은 빈 공간이 보였다."),
        ("resident_ttadak","보지 마시오. 허가 없이 덧지은 거요. 너울이 알면 다 뜯고 벌금이오."),
        ("resident_ttadak","……저 안쪽 빈 데? 옛날 하인 통로요. 13호 책장 뒤까지 가오.")],"w1c:ext:open")
    menu:
        "비밀을 지켜 주겠다고 한다":
            call r13_lines([("resident_ttadak","……고맙소. 대신 필요하면 내가 본 걸 말해 주리다. 사람들 앞에서도."),
                (None,"따닥이 공사 때 그린 벽 안쪽 도면을 건넸다.")],"w1c:ext:keep")
            $ r13_grant(["H7"],"따닥이 건넨 증축 도면")
            $ r13_flag("ttadak_witness","ttadak_ally")
        "증축 기록을 산다 (5냥)" if r13_cash_now()>=5:
            $ r13_cash(-5,"따닥의 증축 도면")
            call r13_lines([("resident_ttadak","도면은 파는 거요. 내 입은 안 팔고. 사람들 앞에선 모른다 하겠소.")],"w1c:ext:buy")
            $ r13_grant(["H7"],"따닥에게서 산 증축 도면")
        "너울에게 신고한다":
            call r13_lines([("neoul","허가 없는 증축이라. 신고 사례는 다섯 냥이오. 벽은 내일 봉하겠소."),
                ("resident_ttadak","……두고 보시오.")],"w1c:ext:report")
            $ r13_cash(5,"증축 신고 사례")
            $ r13_flag("ttadak_hostile","extension_sealed")
        "모른 척 지나간다":
            pass
    return

# ---- S. 뭉치의 현장 물건 ----
label r13_w1c_seal:
    $ r13_flag("ev_s_done")
    call r13_ev_here("search")
    call r13_lines([(None,"봉해 둔 13호 문 앞에 뜯긴 봉인 종이가 떨어져 있었다. 안에서 뭉치가 자루를 들고 나왔다."),
        ("resident_mungchi","……! 버, 버린 물건인 줄 알았어요. 모모 관장님이 사건 난 방 물건은 비싸게 쳐 준대서.")],"w1c:seal:open")
    $ r13_grant(["H8"],"13호 문 앞의 뜯긴 봉인")
    menu:
        "자루를 되찾는다":
            call r13_lines([(None,"자루 안에는 다람이의 그림책과 아내가 쓰던 털실 바구니가 있었다."),
                ("daram" if room13.get("daram_state") in ("with_dad","rescued") else "dad",("엄마 털실이다……." if room13.get("daram_state") in ("with_dad","rescued") else "(다람이에게 돌려줄 것들이다.)"))],"w1c:seal:recover")
            $ r13_flag("family_items_back","mungchi_caught")
        "몰래 뒤를 밟는다":
            call r13_lines([(None,"뭉치는 박물관 뒷문에서 모모 관장에게 자루를 넘겼다. 모모는 값을 묻지도 않고 동전을 셌다."),
                ("resident_momo","사건 물건은 오래 남지요. 사람들은 무서운 걸 보러 옵니다.")],"w1c:seal:follow")
            $ r13_grant(["W9"],"박물관 뒷문에서 본 모모의 거래")
            $ r13_flag("family_items_lost")
        "너울에게 알린다":
            call r13_lines([("neoul","현장을 뜯어? 뭉치, 따라오너라. 봉인은 내가 다시 하겠소.")],"w1c:seal:neoul")
            $ r13_flag("scene_resealed","family_items_back","mungchi_detained")
        "모른 척한다":
            $ r13_flag("family_items_lost")
    return

# ---- T. 거짓 증언 팔기 ----
label r13_w1c_testimony:
    $ r13_flag("ev_t_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"실룩이 내 옆으로 바짝 붙었다. 목소리를 낮췄다."),
        ("resident_siluk","내일 재판 있죠. 제가 '할머니가 그날 밤 2층에 올라가는 걸 봤다'고 해 드릴게요. 열 냥이면 돼요."),
        ("resident_siluk","봤냐고요? 그게 중요해요? 이기면 되잖아요.")],"w1c:t:open")
    menu:
        "열 냥에 산다" if r13_cash_now()>=10:
            $ r13_cash(-10,"실룩의 증언")
            call r13_lines([("resident_siluk","거래 끝. 내일 제가 알아서 나설게요.")],"w1c:t:buy")
            $ r13_flag("fake_testimony")
        "거절한다":
            call r13_lines([("resident_siluk","손해 보시는 거예요. 다른 사람한테 팔아도 몰라요.")],"w1c:t:refuse")
        "그 시각 어디 있었는지 묻는다":
            call r13_lines([("dad","그날 밤 그 시각, 실룩 씨는 어디 있었습니까?"),
                ("resident_siluk","……마구간이요. 장부에 이름도 적었고."),
                ("dad","그럼 2층을 봤을 리 없군요. 이 거래, 제가 너울에게 말하면 어떻게 됩니까?"),
                ("resident_siluk","……알았어요. 대신 뭐든 하나 도와드릴게요. 썰매든 짐이든.")],"w1c:t:leverage")
            $ r13_flag("siluk_owes")
        "너울에게 알린다":
            call r13_lines([("neoul","증언을 판다? 재판 끝날 때까지 마구간에서 나오지 마라.")],"w1c:t:neoul")
            $ r13_flag("siluk_detained")
    return
