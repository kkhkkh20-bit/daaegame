# 1주차 새 사건 3개 (docs/EVENT_CATALOG.md G·L·I·S·T, 0.18.11)
#   ① 엄마의 흔적 — G 피코의 초상(2~3일 낮 광장) + L 슬링의 편지(2~4일 낮 우체국).
#        엄마 초상은 기록으로 직접 보여 준다. 초롱이 얼굴을 확인하면 2주차 답장이 다음 날 첫 시간에 온다. 편지를 엿보게 두면 경고가 새고(2주차 추적),
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
            _st.setdefault("consent_lines",{})["H7"]=[("resident_seori","따닥 씨는 오늘 나오지 않았습니다. 기록만으로는 여관 뒤 벽 안을 누가 직접 봤는지 확인할 수 없어요."),
                ("dad","(그러려면 따닥이 직접 나서서 말해 줘야 했다.)",{"thought":True})]
            _st.setdefault("broken_by",{})["H7"]=[("resident_ttadak","여관 뒤 벽은 제가 덧지었어요. 벽 안에 옛 통로가 있었고, 13호 책장 뒤로 이어져요. 제 눈으로 봤어요."),
                ("seryeon","……13호에 문 말고 다른 길이 있었다고요?")]
    for _c in ROOM13["claims"]:
        if _c["id"]=="C1":
            _c["support_sets"]=list(_c["support_sets"])+[["E04","H7"],["H7","E37"]]

    R13_FAKE_TESTIMONY_LINES=[
        ("resident_siluk","제가 봤어요! 그날 밤 할머니가 2층으로 올라가는 걸!"),
        ("resident_seori","그 시각에 실룩 씨는 마구간 장부에 이름을 적었습니다. 여기 본인 글씨가 있어요."),
        ("resident_siluk","……그, 그건."),
        ("resident_ppul","돈 받고 말하는 증인이 나온 이상, 할머니에 대한 주장은 받아들일 수 없소. 아이는 풀어 주겠소. 그 이상은 안 되오."),
        ("dad","(돈으로 산 쉬운 길이 가장 비쌌다.)",{"thought":True})]

    # The portrait is shown from the notebook (systems/room13_present_flow.rpy, 0.18.13).
    R13_W2E_NOTES.extend([
        ("fake_letter_planted","가짜 편지 한 장이 할머니를 그날 밤 여관 밖으로 내보냈다."),
        ("family_items_lost","13호에 두고 온 우리 짐 일부는 끝내 돌아오지 않았다."),
        ("fake_testimony_exposed","돈 주고 산 증언은 재판에서 무너졌다."),
    ])
    R13_CARRY_GOOD.extend([
        (lambda:r13_has("siluk_owes"),["transport_terms"],
            [("resident_siluk","마구간 썰매를 내드릴게요. 재판 날 저한테 거짓 증언 안 시키신 값이에요.")]),
    ])

    _r13_w1c_action_done=r13_w2_action_done
    def r13_w2_action_done(key,started_at=None):
        _r13_w1c_action_done(key,started_at)
        # 초롱 knows Mom's face from the portrait, so nobody has to be found again:
        # the reply is still "the next day", but ready at that day's first period (4 units = 1 day).
        if key=="w2_reply" and r13_has("portrait_lamp_seen") and store.room13.get("reply_due") is not None:
            n=winter_copy.deepcopy(store.room13);n["reply_due"]=max(r13_abs_time()+1,(n["reply_due"]//4)*4);store.room13=n

    def r13_sling_note_confession():
        # New disclosure design: only the completed, evidence-backed confrontation
        # can create H9. Existing H9/knowledge is never erased or re-granted here.
        if not r13_has("sling_confront_completed") or not r13_sling_confront_ready():return False
        if not r13_has("H9"):
            r13_grant(["H9"],"슬링이 털어놓은 편지 엿보기")
        r13_flag("know_granny_reads","sling_confession_heard")
        return True

    def r13_sling_can_support_day():
        # Pure menu/preview gate. Knowing the wage is not a promise to pay it.
        return (r13_has("sling_job_pressure_heard") and r13_has("sling_day_wage_known")
            and not r13_has("sling_day_supported") and r13_cash_now()>=3)

    def r13_sling_support_day():
        # Only the explicit support choice calls this; protect against a repeated call.
        if not r13_sling_can_support_day():return False
        r13_cash(-3,"슬링의 하루 품삯")
        r13_flag("sling_day_supported")
        return True

label r13_w1c_events:
    call r13_owl_events
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    # From day 2 까로 comes to find Dad (owner, 0.18.12). 일거리는 0.18.91에 없어져서 마차 이야기만 한다
    # (일 안내 독백은 0.19.10에 뺐다).
    if _d>=2 and r13_has("lodging") and not r13_has("livelihood_open"):
        call r13_ev_here("calm")
        call r13_lines([(None,"까로가 눈을 털며 다가왔다. 마차 이야기를 하러 온 얼굴이었다.")]+list(ROOM13["topics"]["life:karo"]["lines"]),"w1c:karo:work", binding_route="dynamic:743")
        $ r13_finish_topic("life:karo")
    # 0.19.15: 3일 새벽(lt_dawn)에 피코가 죽었거나 진료소로 옮겨졌으면 광장에서 그림을 팔지 않는다.
    if 2<=_d<=3 and _p<=1 and _loc=="square" and not r13_has("ev_g_done") and not r13_has("piko_dead") and not r13_has("lt_dawn"):
        $ r13_offer("r13_w1c_portrait")
    if 2<=_d<=R13_CASE_DAY and _p<=1 and _loc=="post" and not r13_has("ev_l_done"):
        $ r13_offer("r13_w1c_letters")
    if 2<=_d<=R13_CASE_DAY and _p==1 and _loc=="inn" and not r13_has("ev_i_done"):
        $ r13_offer("r13_w1c_extension")
    if _d==R13_CASE_DAY and _p>=2 and room13["case_state"]=="pending" and r13_has("fake_letter_planted") and not r13_has("fake_letter_night") and not r13_has("granny_knows_found_out"):
        call r13_w1c_fake_night
    if r13_tl(5)<=_d<=r13_tl(6) and _loc=="hall" and room13["case_state"]=="occurred" and not r13_has("ev_s_done"):
        $ r13_offer("r13_w1c_seal")
    if _d==r13_tl(6) and _p<=1 and _loc in ("gate","store") and room13["case_state"]=="occurred" and not r13_has("ev_t_done"):
        $ r13_offer("r13_w1c_testimony")
    if _d>=R13_WEEK2_DAY and r13_has("letters_safe") and r13_has("pursuit_active") and not r13_has("pursuit_managed"):
        call r13_lines([("resident_sling","부인 편지는 제가 다른 길로 돌렸어요. 그래서 뒤쫓는 사람은 엉뚱한 편지만 들고 갔어요.")],"w1c:letters:safe")
        $ r13_flag("pursuit_managed")
    return None

# ---- G. 피코의 초상 ----
label r13_w1c_portrait:
    $ r13_flag("ev_g_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"광장 구석에서 피코가 낡은 판자에 물감을 문지르고 있었다. 그림 속 사람은 백 년 전 옷을 입고 있었다."),
        ("resident_piko","……‘옛 마을 초상’이에요. 모모 관장님이 이런 걸 사 줘요."),
        ("resident_piko","오늘 못 팔면 방값이 없어요. 그럼 또 등 밑이죠, 뭐.")],"w1c:portrait:open")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "가짜라고 모모 관장에게 알린다":
                call r13_lines([("resident_momo","……옛 그림이라더니 물감이 아직 마르지도 않았군요. 알려 주셔서 고마워요. 사례예요."),
                    ("resident_piko","……")],"w1c:portrait:expose")
                $ r13_cash(6,"모모 관장의 사례")
                $ r13_flag("piko_hostile")
            "모른 척한다":
                pass
            "아내 초상을 그려 달라고 한다 (5냥)" if r13_cash_now()>=5 and not r13_has("mom_portrait") and not r13_has("lt_piko_promise"):
                $ r13_cash(-5,"피코에게 맡긴 엄마 초상")
                call r13_lines([("dad","제 아내입니다. 눈매는 이렇고, 왼쪽 눈썹에 작은 흉터가 있어요."),
                    ("daram","엄마는 웃을 때 코를 찡그려!"),
                    ("daram","이렇게! 그것도 그려 줘야 돼. 약속!"),
                    (None,"다람이 새끼손가락을 내밀었다. 피코가 물감 묻은 손가락을 걸었다."),
                    ("resident_piko","약속. 진짜 사람을 그리는 건 오랜만이네요. 내일 아침까지 그려 둘게요.")],"w1c:portrait:mom")
                # 에피소드 ①: 초상은 다음 날 아침에 받는다(피코가 살면 완성본, 죽으면 코 없는 초상).
                $ r13_flag("lt_piko_promise","piko_ally")
            "구운 밤을 건네 준다" if r13_has("own:snack"):
                $ r13_use_item("snack")
                call r13_lines([("resident_piko","……오늘 저녁은 이걸로 버틸게요. 그러니 가짜 그림은 안 팔아요.")],"w1c:portrait:snack")
                $ r13_flag("piko_ally")
                $ _ep_loop=True
            "그만 간다":
                pass
    return

# ---- L. 슬링의 편지 ----
label r13_w1c_letters:
    if r13_has("ev_l_done"):
        return
    $ r13_flag("ev_l_done")
    call r13_ev_here("search")
    if "resident_sling" not in r13_met_people():
        call r13_lines([(None,"우편 일을 하는 사람이 화덕 앞에서 봉투 하나를 들고 있었다."),
            ("dad","실례합니다. 여기 우편을 맡고 계십니까?"),
            ("resident_sling","예, 슬링입니다. 잠깐만요.")],"w1c:letters:intro")
    call r13_lines([(None,"주전자에서 김이 올랐다. 슬링은 봉투의 붙인 입구만 그 김에 대고 있었다. 풀 붙인 귀퉁이가 조금씩 들렸다."),
        ("resident_sling","……! 아, 봉투가 젖어서 말리는 거예요."),
        ("dad","말리는 게 아니라 붙인 데를 떼고 계신데요. 받는 분이 열어 달라고 한 편지입니까?"),
        ("resident_sling","……아니요.")],"w1c:letters:open")
    $ r13_note_encounter("resident_sling")
    # Dad can act on the opening he saw, but cannot offer an unknown day's wage yet.
    menu:
        "“못 본 것으로 하겠습니다.”":
            call r13_lines([(None,"슬링은 김으로 연 봉투에서 편지 한 줄을 베꼈다. 받는 사람 칸에 여관 이름이 보였다.")],"w1c:letters:ignore")
            $ r13_flag("warning_exposed")
        "“편지에서 뭘 보려는 겁니까?”":
            if r13_sling_knows_requester():
                call r13_lines([("dad","편지를 열어서 무엇을 보려는 겁니까?"),
                    ("resident_sling","전에 말씀드린 할머니의 부탁이에요. 손님 편지를 베껴 오지 않으면 일자리를 잃는다고 하셨죠.")],"w1c:letters:catch:known")
            else:
                call r13_lines([("dad","편지를 열어서 무엇을 보려는 겁니까?"),
                    ("resident_sling","……편지 내용을 베끼려던 거예요. 시킨 사람이 있지만, 이름은 말 못 해요. 일자리를 잃을 수도 있어서요.")],"w1c:letters:catch")
            call r13_w1c_letters_after
        "“직접 보려는 겁니까?”":
            if r13_sling_knows_requester():
                call r13_lines([("dad","전에 말씀하신 그 부탁입니까?"),
                    ("resident_sling","네. 할머니가 손님 편지를 베껴 오라고 하셨던 일이에요.")],"w1c:letters:who:known")
            else:
                call r13_lines([("dad","직접 읽으려는 겁니까, 누가 부탁한 겁니까?"),
                    ("resident_sling","……부탁받은 일이에요. 누구인지는 말 못 해요. 거절하면 일자리가 없어질 수도 있어서요.")],"w1c:letters:who")
            call r13_w1c_letters_after
        "편지 개봉을 경비에게 알린다":
            call r13_lines([("dad","남의 편지를 열려던 일을 경비에게 알리겠습니다."),
                ("resident_sling","너울한테요? 그러면 저는 우체국에서 일 못 해요.")],"w1c:letters:report:warning")
            menu:
                "그래도 경비에게 알린다":
                    call r13_lines([(None,"나는 경비 너울을 찾아가, 슬링이 배달할 봉투의 입구를 김으로 떼고 있던 일을 전했다."),
                        ("neoul","받는 사람 허락도 없이 편지를 열려 했소? 슬링은 오늘부터 우체국에 나오지 마시오."),
                        ("resident_sling","……")],"w1c:letters:neoul")
                    $ r13_flag("sling_hostile")
                "“먼저 사정을 듣겠습니다.”":
                    if r13_sling_knows_requester():
                        call r13_lines([("dad","전에 말씀하신 사정부터 다시 듣겠습니다."),
                            ("resident_sling","할머니가 손님 편지를 베껴 오라고 했다는 말씀은 드렸죠. 거절하면 일자리를 잃는다고요.")],"w1c:letters:report:reason:known")
                    else:
                        call r13_lines([("dad","먼저 왜 그랬는지 듣겠습니다."),
                            ("resident_sling","……편지를 베껴 오라는 부탁을 받았어요. 누구 부탁인지는 말 못 해요. 그 이름을 꺼내면 일자리를 잃을까 봐요.")],"w1c:letters:report:reason")
                    call r13_w1c_letters_after
        "전에 보인 아내 초상을 꺼낸다" if "P01" in room13["evidence"] and r13_has("portrait_known"):
            call r13_lines([("dad","이 초상, 전에 보여 드렸지요. 이분은 제 아내입니다."),
                ("resident_sling","그분 가족이었군요. 그러면 이 편지를 함부로 다루면 안 되겠네요.")],"w1c:letters:portrait")
            if r13_sling_knows_requester():
                call r13_lines([("resident_sling","할머니의 부탁이라고 말씀드렸지만, 이 편지는 열지 않겠어요."),
                    ("dad","그대로 보내 주세요. 이 이야기를 함부로 퍼뜨리지는 않겠습니다.")],"w1c:letters:portrait:known")
            else:
                call r13_lines([("resident_sling","누가 시켰는지는 말 못 해요. 그 이름을 꺼냈다가 일자리를 잃을까 봐요."),
                    ("dad","편지는 그대로 보내 주세요. 말씀하지 않은 이름을 제가 짐작해 퍼뜨리지는 않겠습니다.")],"w1c:letters:portrait:guarded")
            $ r13_flag("letters_safe","sling_ally","sling_nonpaid_trust")
            call r13_w1c_letters_after(False)
    return

label r13_w1c_letters_after(ask_stop=True):
    $ r13_flag("sling_job_pressure_heard")
    if ask_stop:
        call r13_lines([("dad","여기서 하루 일하면 얼마를 받습니까?"),
            ("resident_sling","세 냥이요.")],"w1c:letters:wage")
        $ r13_flag("sling_day_wage_known")
    menu:
        "가짜 약속 쪽지를 맡긴다" if r13_sling_fake_letter_ready():
            call r13_w1c_fake_letter
        "“남의 편지는 열지 마세요.”" if ask_stop:
            call r13_lines([("dad","편지는 그대로 보내 주세요. 말씀하지 않은 이름을 제가 짐작해 퍼뜨리지는 않겠습니다."),
                ("resident_sling","……네. 편지는 열지 않을게요. 이 일은 여기서만 이야기해 주세요.")],"w1c:letters:stop")
            $ r13_flag("letters_safe","sling_ally","sling_nonpaid_trust")
        "슬링의 오늘 몫 지원 (내 돈 3냥)" if ask_stop and r13_sling_can_support_day():
            $ _sling_supported=r13_sling_support_day()
            if _sling_supported:
                call r13_lines([("dad","오늘 하루 몫 세 냥은 제가 드리겠습니다. 이 편지는 뜯지 말고 그대로 보내 주세요."),
                    ("resident_sling","……오늘 몫은 받았으니, 이 편지는 그대로 보내겠습니다.")],"w1c:letters:paid")
                $ r13_flag("letters_safe","sling_ally")
                call r13_w1c_letters_after(False)
        "“이 편지는 그대로 보내 주세요.”" if not ask_stop:
            pass
    return

label r13_w1c_fake_letter:
    if not r13_sling_knows_requester():
        call r13_lines([("resident_sling","누구에게 쪽지를 전하라는 건지, 아직 얘기가 안 됐어요.")],"w1c:letters:fake:unknown")
        return
    # Once Granny knows Dad found out (systems/room13_use_knowledge.rpy), a planted letter does not fool her.
    if r13_has("granny_knows_found_out"):
        call r13_lines([("resident_sling","할머니가 요즘은 제가 가져가는 편지를 잘 안 믿으세요. 누가 알아챘다고 하시면서요.")],"w1c:letters:fake:fail")
        return
    call r13_lines([("dad","할머니께 이 쪽지를 베껴 드리세요. ‘목요일 밤, 북쪽 초소에서 기다린다.’ 서명은 비워 두고요."),
        ("resident_sling","……할머니가 이 가짜 쪽지를 믿으면요?"),
        ("dad","그럼 목요일 밤에 할머니가 어디로 가는지 보게 되겠죠.")],"w1c:letters:fake")
    $ r13_flag("fake_letter_planted","letters_safe","sling_ally")
    return

label r13_w1c_fake_night:
    $ r13_flag("fake_letter_night")
    call r13_scene("hall","목요일 저녁 · 여관 2층 복도","night")
    call r13_lines([(None,"해가 지자 할머니가 등잔을 들고 계단을 내려갔다. 손에는 담요와 굵은 끈이 들려 있었다."),
        ("granny","잠깐 볼일이 있어서 나가요. 아이는 방에 있게 하세요."),
        ("dad","(가짜 편지에 적어 둔 바로 그 시각이다.)",{"thought":True})],"w1c:night:open")
    menu:
        "할머니를 따라간다":
            call r13_lines([(None,"할머니는 북쪽 초소 처마 밑에서 등잔을 낮췄다. 끈을 담요 밑에 감추고, 길 쪽만 보았다."),
                ("resident_lamplighter","……할머니? 이 늦은 시간에 초소엔 왜 오셨어요."),
                ("granny","기다리는 사람이 있어요. 아이 엄마가 올 거예요."),
                ("dad","(아이 엄마를 기다리는 사람이 끈을 숨기고 있다. 초롱도 봤다.)",{"thought":True})],"w1c:night:follow")
            $ r13_flag("granny_lure_seen","prevention_witness")
        "다람이와 방에 남는다":
            call r13_lines([(None,"할머니가 나간 뒤 여관은 조용했다. 다람이는 내 무릎을 베고 잠들었다.")],"w1c:night:stay")
    call r13_scene("room","13호실","night")
    call r13_lines([("resident_owlgp","할머니가 초소 쪽으로 가는 걸 봤소. 오늘 밤은 여기 오지 않겠구려."),
        ("resident_owlgp","부인에게서 맡아 둔 물건을 돌려드리겠소. 베껴 둔 기록이오."),
        (None,"그날 밤 13호에서는 아무도 다치지 않았다.")],"w1c:night:safe")
    $ r13_edit(case_state="prevented",victim_state="protected",daram_state="with_dad",period=3,location="inn")
    $ r13_flag("victim_protected")
    $ r13_grant(["E17"],"살아 있는 어르신이 간직해 온 베낀 기록")
    return

# ---- I. 따닥의 증축 ----
label r13_w1c_extension:
    $ r13_flag("ev_i_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"여관 뒷벽에서 따닥이 판자를 덧대고 있었다. 새 판자 틈으로 오래된 벽돌과 좁은 빈 공간이 보였다."),
        ("resident_ttadak","보지 마세요. 허가 없이 덧지은 거예요. 너울이 알면 다 뜯기고 벌금이에요."),
        ("resident_ttadak","……저 안쪽 빈 공간 말이에요? 옛날 하인들이 다니던 통로예요. 13호 책장 뒤까지 이어져요.")],"w1c:ext:open")
    menu:
        "비밀을 지켜 주겠다고 한다":
            call r13_lines([("resident_ttadak","……고마워요. 대신 필요하면 제가 본 걸 말해 드릴게요. 사람들 앞에서도요."),
                (None,"따닥이 증축 공사 때 그린 벽 안쪽 도면을 건넸다.")],"w1c:ext:keep")
            $ r13_grant(["H7"],"따닥이 건넨 증축 도면")
            $ r13_flag("ttadak_witness","ttadak_ally")
        "증축 기록을 산다 (5냥)" if r13_cash_now()>=5:
            $ r13_cash(-5,"따닥의 증축 도면")
            call r13_lines([("resident_ttadak","도면은 파는 거예요. 하지만 제 입은 안 팔아요. 사람들 앞에선 모른다고 할 거예요.")],"w1c:ext:buy")
            $ r13_grant(["H7"],"따닥에게서 산 증축 도면")
        "너울에게 신고한다":
            call r13_lines([("neoul","허가 없는 증축이라. 신고 사례는 다섯 냥이오. 벽은 내일 봉하겠소."),
                ("resident_ttadak","……두고 보세요.")],"w1c:ext:report")
            $ r13_cash(5,"증축 신고 사례")
            $ r13_flag("ttadak_hostile","extension_sealed")
        "모른 척 지나간다":
            pass
    return

# ---- S. 뭉치의 현장 물건 ----
label r13_w1c_seal:
    $ r13_flag("ev_s_done")
    call r13_ev_here("search")
    call r13_lines([(None,"봉해 둔 13호 문 앞에 뜯긴 봉인 종이가 떨어져 있었다. 곧 방 안에서 뭉치가 자루를 들고 나왔다."),
        ("resident_mungchi","……! 버, 버린 물건인 줄 알았어요. 모모 관장님이 사건 난 방 물건은 비싸게 쳐 준다고 해서.")],"w1c:seal:open")
    $ r13_grant(["H8"],"13호 문 앞의 뜯긴 봉인")
    menu:
        "자루를 되찾는다":
            call r13_lines([(None,"자루 안에는 다람이의 그림책과 아내가 쓰던 털실 바구니가 있었다."),
                ("daram" if room13.get("daram_state") in ("with_dad","rescued") else "dad",("엄마 털실이다……." if room13.get("daram_state") in ("with_dad","rescued") else "(다람이에게 돌려줄 것들이다.)"))],"w1c:seal:recover", binding_route="dynamic:768")
            $ r13_flag("family_items_back","mungchi_caught")
        "몰래 뒤를 밟는다":
            call r13_lines([(None,"뭉치는 박물관 뒷문에서 모모 관장에게 자루를 넘겼다. 모모는 값을 묻지도 않고 동전을 셌다."),
                ("resident_momo","사건 현장 물건은 오래 남지요. 사람들은 무서운 걸 보러 박물관에 옵니다.")],"w1c:seal:follow")
            $ r13_grant(["W9"],"박물관 뒷문에서 본 모모의 거래")
            $ r13_flag("family_items_lost")
        "너울에게 알린다":
            call r13_lines([("neoul","사건 현장 봉인을 뜯었소? 뭉치, 따라오시오. 13호 봉인은 내가 다시 하겠소.")],"w1c:seal:neoul")
            $ r13_flag("scene_resealed","family_items_back","mungchi_detained")
        "모른 척한다":
            $ r13_flag("family_items_lost")
    return

# ---- T. 거짓 증언 팔기 ----
label r13_w1c_testimony:
    $ r13_flag("ev_t_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"실룩이 내 옆으로 바짝 붙어 목소리를 낮췄다."),
        ("resident_siluk","내일 재판 있죠. 제가 ‘할머니가 그날 밤 2층에 올라가는 걸 봤다’고 말해 드릴게요. 열 냥이면 돼요."),
        ("resident_siluk","제가 직접 봤냐고요? 그게 중요해요? 재판에서 이기면 되잖아요.")],"w1c:t:open")
    menu:
        "열 냥에 산다" if r13_cash_now()>=10:
            $ r13_cash(-10,"실룩의 증언")
            call r13_lines([("resident_siluk","거래 끝. 내일 재판에서 제가 알아서 나설게요.")],"w1c:t:buy")
            $ r13_flag("fake_testimony")
        "거절한다":
            call r13_lines([("resident_siluk","손해 보시는 거예요. 이 증언을 다른 사람한테 팔아도 전 몰라요.")],"w1c:t:refuse")
        "그 시각 어디 있었는지 묻는다":
            call r13_lines([("dad","그날 밤 그 시각, 실룩 씨는 어디 있었습니까?"),
                ("resident_siluk","……마구간에 있었어요. 마구간 장부에 이름도 적었고요."),
                ("dad","그 시각 마구간에 있었다면 2층을 봤을 리가 없군요. 이 거래를 제가 너울에게 말하면 어떻게 됩니까?"),
                ("resident_siluk","……알았어요. 대신 뭐든 하나 도와드릴게요. 썰매든 짐이든.")],"w1c:t:leverage")
            $ r13_flag("siluk_owes")
        "너울에게 알린다":
            call r13_lines([("neoul","돈 받고 증언을 팔았소? 재판 끝날 때까지 마구간에서 나오지 마시오.")],"w1c:t:neoul")
            $ r13_flag("siluk_detained")
    return
