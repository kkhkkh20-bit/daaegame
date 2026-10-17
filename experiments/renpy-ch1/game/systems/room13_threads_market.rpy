# 0.19.17 장터·창고 사람들 줄기와 다시 묻기 (systems/room13_threads.rpy 틀, 그룹 g4_market)
#   인물: 은호·구슬·백 부인·뭉치·실룩·여니·토리·콩이·꽥순·달그락·현이·물결·솔방울.
#   날짜: init 990(systems/room13_timeline.rpy)이 옛 날짜를 옮긴다. life:*:work=1~7일(사건 전),
#         life:*:after=8~10일(사건 뒤·재판 전), life:*:crisis=11~13일(둘째 주). 여기 조건은 옮긴 뒤 날짜로 쓴다.
#   라벨로 도는 주제(R13_TOPIC_LABELS: 알리바이·저울·되사기·심부름 등)는 라벨이 먼저 불려 again/variants가 닿지 않는다.
#   그런 주제에는 steps(목록에서 빠질 때)만 주고, recap은 점검 도구용으로만 둔다.
init 185 python:
    def _r13g4_day(a,b=99):
        return lambda s:a<=s.get("day",1)<=b
    _R13G4_W2=_r13g4_day(R13_WEEK2_DAY)
    _R13G4_AFTER=_r13g4_day(R13_CASE_DAY+1)
    _R13G4_DETAINED=lambda s:s.get("granny_state")=="detained"

    def _r13g4(key,**kw):
        t=ROOM13["topics"].get(key)
        if t is None:return
        t.update(kw)

    # ---------------- 은호 사장 (하오체) ----------------
    _r13g4("life:resident_eunho:work",
        variants=[({"has":["scale_settled"]},[
            ("dad","물건 가격을 바꾸셨습니까?"),
            ("resident_eunho","저울은 바로잡았소. 값을 올린 건 물건 들어오는 길이 끊겨서요."),
            ("resident_eunho","다음 물건이 언제 올지 모르니, 지금 있는 걸로 버텨야 하오.")])],
        again=[({"all":[_R13G4_W2,{"has":["supply_terms"]}]},[("resident_eunho","이제는 값보다 장부요. 누가 얼마나 가져갔는지 적히고 있으니.")]),
            (None,[("resident_eunho","물건 들어오는 길은 아직 끊겨 있소. 값 얘기는 그때 드린 그대로요.")])])
    _r13g4("life:resident_eunho:after",
        variants=[({"has":["eunho_exposed"]},[
            ("resident_eunho","자루 밑 몫까지 보셨으니, 이제 제 창고에 숨길 것도 없소."),
            ("dad","다른 창고들이 얼마나 내놓는지도 확인하겠습니다."),
            ("resident_eunho","그래 주시오. 내 창고 문만 활짝 열린 모양새는 싫소.")])],
        again=[({"has":["supply_terms"]},[("resident_eunho","약속한 몫은 장부에 적고 내놓겠소. 다른 창고도 같이 적는다면.")]),
            (None,[("resident_eunho","다른 창고가 얼마나 내놓는지는 확인해 보셨소? 그 말은 제 창고 열기 전에 해 달라 했소.")])])
    _r13g4("life:resident_eunho:crisis",
        variants=[({"all":[{"has":["eunho_refuses"]},{"not":["supply_terms"]}]},[
            ("resident_eunho","내놓으라는 말은 다들 쉽게 하오. 내놓고 나서 내가 줄을 서면 누가 기억해 줍니까?"),
            ("dad","내놓는 몫과 남길 몫을 둘 다 장부에 적겠습니다."),
            ("resident_eunho","적는 것까지는 좋소. 내놓을지는 아직 정하지 않았소.")])],
        again=[({"has":["supply_terms"]},[("resident_eunho","장부에 내 몫도 적혔소. 칭찬은 필요 없소.")]),
            (None,[("resident_eunho","남길 몫을 적는 일은 잊지 마시오. 그게 먼저요.")])])
    _r13g4("w2_supply_receipt",steps={"has":["topic:w2_supply_receipt"]},
        again=[(None,[("resident_eunho","약속한 나머지 식량은 학교로 보내기로 했소. 받은 수량은 그쪽 장부에 적어 두시오.")])])
    _r13g4("eunho_hidden",steps={"has":["hidden_stock"]},
        variants=[({"any":[{"has":["shelter_agreed"]},{"has":["E25"]}]},[
            ("dad","포장천 자루 바닥에 식량이 따로 숨겨져 있더군요. 장부에는 바닥났다고 적혀 있던데요."),
            ("resident_eunho","……겨울은 길단 말이오. 겨울 끝에 가서 아무도 가진 게 없으면, 그때는 누가 나눠 줍니까."),
            ("dad","대피소는 이미 정해졌습니다. 굶는 사람들이 먼저 쓰러집니다."),
            ("resident_eunho","알겠습니다. 숨겨 둔 몫은 대피소로 내놓겠소. 대신 가져가는 사람은 이름을 적는다는 조건이오.")])],
        again=[({"any":[{"has":["shelter_agreed"]},{"has":["E25"]}]},[("resident_eunho","숨겨 둔 몫은 대피소로 내놓기로 했소. 이름 적는 조건은 그대로요.")]),
            (None,[("resident_eunho","대피소가 정해지면 내놓겠다고 했소. 약속은 지키겠소.")])])
    _r13g4("eunho_hidden_ledger",steps={"has":["saw_eunho_hide"]},
        again=[({"has":["w2_eunho_credit"]},[("resident_eunho","그 장부 이야기는 대피소 몫과 이자로 매듭지었소. 더 할 말은 없소.")]),
            (None,[("resident_eunho","외상 장부요. 그날 밤 여관 일과는 상관없다고 말씀드렸소.")])])
    _r13g4("w2_eunho_credit",steps={"has":["eunho_credit_known"]},
        again=[(None,[("resident_eunho","대피소 몫과 이자는 그때 약속한 대로요. 장부를 넘기지 않는다는 약속도 지키시오.")])])
    _r13g4("ledger_deal",steps={"not":["eunho_refuses"]},
        again=[(None,[("resident_eunho","약속대로 당신 물건은 반값이오. 장부 이야기는 우리 둘만 아는 걸로 합시다.")])])
    _r13g4("grudge_cold:eunho",steps={"not":["eunho_reconciled"]},
        again=[(None,[("resident_eunho","값은 정해진 대로 받소. 그 이상 할 말은 없소.")])])
    _r13g4("eunho_scale",steps={"not":["scale_settled"]},recap="저울이 기운 일은 아직 매듭짓지 않았다.")
    _r13g4("eunho_pages",steps={"not":["know_stone_history"]},recap="팔려 간 옛 장부는 아직 은호 사장 손에 있다.")
    _r13g4("w2_buy_tools",steps={"not":["tools_back"]},recap="부리의 공구함은 아직 은호 사장 자루 옆에 있다.")
    _r13g4("w2_eunho_full",steps={"not":["supply_terms"]},recap="대피소 몫을 제값에 살 돈이 있을까?")
    _r13g4("alibi:case:resident_eunho",steps={"case":"occurred"},recap="은호는 그날 저녁 창고에서 구슬과 재고를 셌다고 했다.")

    # ---------------- 구슬 (수줍은 존댓말, 청소년) ----------------
    _r13g4("life:resident_guseul:work",
        again=[(None,[("resident_guseul","도장이 있어도 종이랑 묶음 번호를 같이 봐요. 그건 지금도 같아요.")])])
    _r13g4("life:resident_guseul:after",
        variants=[({"has":["eunho_credit_known"]},[
            ("resident_guseul","외상 장부 일은 사장님이 직접 말씀하셨다면서요."),
            ("dad","응. 너는 네가 본 수량만 말해 주면 돼."),
            ("resident_guseul","사장님이 좋은 일도 해 주셨어요. 이렇게 말하면 제가 거짓말하는 것 같나요?")])],
        again=[(None,[("resident_guseul","제가 본 수량은 그때 말씀드린 그대로예요. 못 본 건 사장님께 여쭤보세요.")])])
    _r13g4("life:resident_guseul:crisis",
        again=[(None,[("resident_guseul","제가 센 건 그대로예요. 나머지는 사장님이 직접 답하시기로 했잖아요.")])])
    _r13g4("life:resident_guseul:receipt",
        again=[(None,[("resident_guseul","저는 이 묶음만 봤어요. 다른 묶음은 따로 세어 보셔야 해요.")])])
    _r13g4("guseul_scale",steps={"has":["scale_rigged"]},
        again=[({"any":[{"has":["ration_fixed"]},{"has":["bori_cleared"]}]},[("resident_guseul","배급소 저울은 광장에서 다시 쟀다면서요. 저는 그날 본 것만 말씀드렸어요.")]),
            ({"has":["H6"]},[("resident_guseul","사장님이 직접 털어놓으셨다면서요. 그럼 제 말은 거기까지만 할게요.")]),
            (None,[("resident_guseul","배급소 저울 얘기는 그때 말씀드린 게 다예요. 제가 말했다고는 하지 마세요.")])])
    _r13g4("alibi:case:resident_guseul",steps={"case":"occurred"},recap="구슬은 그날 저녁 은호와 창고에서 재고를 셌다고 했다.")

    # ---------------- 백 부인 (우아한 존댓말) ----------------
    _R13G4_MADAM_OPENED={"any":[{"has":["madam_store_opened"]},{"has":["madam_exposed"]},{"has":["w2_madam_stock"]},{"has":["kids_registered"]}]}
    _r13g4("life:resident_madam:work",
        variants=[({"has":["madam_store_opened"]},[
            ("dad","물자를 나눠 쓰는 중입니까?"),
            ("resident_madam","광장 사람들이 제 창고 문까지 열고 갔지요. 이제 남은 건 우리 식구 몫이에요."),
            ("dad","혹시 남는 물자가 있다면……"),
            ("resident_madam","남는지 안 남는지 남이 어떻게 알죠? 한 번 열어 보셨으니 더 잘 아시겠네요.")])],
        again=[({"has":["madam_exposed"]},[("resident_madam","장부까지 보셨으니 제 창고 사정은 저보다 잘 아시겠네요.")]),
            (None,[("resident_madam","우리 식구 몫부터 남겨야 한다는 말은 그때와 같아요.")])])
    _r13g4("life:resident_madam:after",
        variants=[({"not":["madam_store_opened","madam_exposed","w2_madam_stock","kids_registered","supply_terms"]},[
            ("resident_madam","다들 제 창고 문만 쳐다보더군요. 열지도 않았는데 벌써 이름 없이 가져갈 궁리들이에요."),
            ("dad","가져가서 쓴 몫이 생기면 기록해 두겠습니다."),
            ("resident_madam","당연하지요. 다들 당연한 일을 부탁처럼 말씀하시네요.")])],
        again=[(None,[("resident_madam","가져가는 분은 장부에 이름을 적으라는 것, 그것만 지켜 주세요.")])])
    _r13g4("life:resident_madam:crisis",
        variants=[({"not":["madam_store_opened","madam_exposed","w2_madam_stock","kids_registered"]},[
            ("resident_madam","제 창고는 제 거예요. 다들 열어 달라는 말만 하고, 열고 난 다음 일은 말하지 않지요."),
            ("dad","부인 댁에 남겨 둘 몫도 같이 정해야겠죠."),
            ("resident_madam","그걸 먼저 묻는 분은 드물더군요. 열지 말지는 그다음에 이야기해요.")])],
        again=[(_R13G4_MADAM_OPENED,[("resident_madam","제 몫까지 비워 놓고 고맙다고 하진 마세요. 그 말은 아직 그대로예요.")]),
            (None,[("resident_madam","남겨 둘 몫부터 정하자는 말, 잊지 않았어요.")])])
    _r13g4("madam_after_trust",steps={"has":["madam_trust"]},
        again=[({"has":["madam_exposed"]},[("resident_madam","도둑을 잡아 줘서 고맙다고 한 말을 거둘 생각은 없어요. 장부 일은 별개고요.")]),
            (None,[("resident_madam","믿을 손이 귀하다고 했죠. 그 말은 그대로예요.")])])
    _R13G4_MADAM_LEAVE=("resident_madam","외지 사람은 겨울이 끝나면 떠나요. 우리 마을 사람들은 여기 남고요. 그걸 잊지 마세요.")
    _r13g4("madam_after_hostile",steps={"has":["madam_hostile"]},
        variants=[({"has":["H4"]},[("resident_madam","검사원까지 불러서 창고 빗장 일을 기록에 올리셨다지요."),_R13G4_MADAM_LEAVE]),
            ({"has":["H2"]},[("resident_madam","검사원까지 데려와서 제 창고 약초를 세게 했다지요."),_R13G4_MADAM_LEAVE]),
            ({"has":["kids_registered"]},[("resident_madam","제 장부를 촌장님께 들고 가셨다지요. 표 없는 아이들 몫까지 제 창고에서 내라더군요."),_R13G4_MADAM_LEAVE]),
            ({"all":[{"has":["bori_cleared"]},{"has":["H1"]}]},[("resident_madam","광장 배급대 앞에서 제 장부를 펼치셨다지요."),_R13G4_MADAM_LEAVE]),
            ({"has":["madam_store_opened"]},[("resident_madam","광장 사람들을 몰고 와서 제 창고 문을 열게 하셨지요."),_R13G4_MADAM_LEAVE]),
            ({"all":[{"has":["siluk_ally"]},{"has":["H1"]}]},[("resident_madam","제 장부를 들이밀어서 실룩 빚을 지우게 하셨다지요."),_R13G4_MADAM_LEAVE]),
            (None,[("resident_madam","외지 분이 남의 창고 일에 손을 대셨다는 말은 들었어요."),_R13G4_MADAM_LEAVE])],
        again=[(None,[("resident_madam","할 말은 그때 다 했어요. 외지 분은 떠나고 우리는 남는다는 거요.")])])
    _r13g4("ledger_madam:approach",steps={"not":["ledger_madam:approach"]},recap="백 부인은 장부를 두고 할 말을 이미 했다.")
    _r13g4("w2_madam_stock",steps={"has":["H1"]},
        again=[(None,[("resident_madam","이름 적고 가져가라고 했지요. 장부를 광장에 붙이지 않는다는 약속도 지키세요.")])])
    _r13g4("alibi:case:resident_madam",steps={"case":"occurred"},recap="백 부인은 그날 저녁 자기 창고에서 뭉치와 보관함을 셌다고 했다.")

    # ---------------- 뭉치 (눈치 보는 존댓말, 청소년) ----------------
    _r13g4("life:resident_mungchi:work",
        again=[({"has":["mungchi_confessed"]},[("resident_mungchi","그때 말씀드린 것 말고는 몰라요. 정말이에요.")]),
            (None,[("resident_mungchi","옮길 곳만 말해 주세요. 상자 주인은 부인한테 물어보시고요.")])])
    _r13g4("life:resident_mungchi:after",
        again=[(None,[("resident_mungchi","상자 수는 셌어요. 안에 든 건 안 봤어요.")])])
    _r13g4("life:resident_mungchi:crisis",
        again=[(None,[("resident_mungchi","제가 쌓은 상자는 적어 두셨죠? 그거면 돼요.")])])
    _r13g4("mungchi_confront",steps={"has":["know_mungchi_thief"]},
        again=[(None,[("resident_mungchi","베낀 종이는 부인한테 줬다고 말씀드렸잖아요. 그게 다예요.")])])

    # ---------------- 실룩 (해요체) ----------------
    _r13g4("life:resident_siluk:work",
        variants=[({"has":["siluk_handed"]},[
            ("dad","눈길에서도 수레가 다니네요."),
            ("resident_siluk","요즘은 제 짐이 아니라 너울이 시키는 짐만 끌어요."),
            ("dad","갈 때와 올 때가 같은 수레인지 알기 어렵겠군요."),
            ("resident_siluk","끄는 사람은 짐을 들여다보지 않아요. 지금은 들여다볼 처지도 아니고요.")])],
        again=[({"has":["siluk_handed"]},[("resident_siluk","너울이 시키는 짐만 끌어요. 수레 얘기는 그게 다예요.")]),
            (None,[("resident_siluk","수레 얘기는 그때와 같아요. 바퀴 자국만 보고 누가 탔다고는 하지 마세요.")])])
    _r13g4("life:resident_siluk:after",
        again=[(None,[("resident_siluk","새로 싣는 짐은 먼저 들여다보려고요. 그 말은 지킬게요.")])])
    _r13g4("life:resident_siluk:crisis",
        again=[({"has":["cv_stable"]},[("resident_siluk","그 수레 얘기는 마구간에서 한 그대로예요.")]),
            (None,[("resident_siluk","새로 싣는 건 전부 보여 달라는 말, 그대로예요.")])])
    _r13g4("siluk_after",steps={"has":["siluk_ally"]},
        variants=[({"has":["siluk_handed"]},[
            ("resident_siluk","마차를 부르시면 가고 싶은데, 지금은 너울 허락 없이는 마구간을 못 나가요."),
            ("resident_siluk","눈이 크게 오면 아픈 사람부터 실어 나르겠다는 말은 거두지 않을게요.")])],
        again=[({"has":["siluk_handed"]},[("resident_siluk","너울 허락 없이는 마구간을 못 나가요. 마차 얘기는 그다음이에요.")]),
            (None,[("resident_siluk","마차는 언제든 부르세요. 아픈 사람부터 싣는다는 약속도 그대로예요.")])])
    _r13g4("siluk_cold",steps={"not":["siluk_reconciled"]},
        again=[(None,[("resident_siluk","할 말 없어요. 입막음 값 얘기라면 더더욱요.")])])
    _r13g4("grudge_fix:siluk",steps={"not":["siluk_reconciled"]},recap="실룩에게 받은 여덟 냥은 아직 내 주머니에 있다.")
    _r13g4("smalltalk:siluk_cart",timeless=True,
        again=[({"has":["siluk_handed"]},[("resident_siluk","요즘은 바퀴 볼 새도 없이 끌어요.")]),
            (None,[("resident_siluk","제가 멈춘 데는 다 이유가 있다고 했죠. 지금도 그래요.")])])

    # ---------------- 여니 (시원한 해요체) ----------------
    _R13G4_YEONI_COLD={"all":[{"has":["yeoni_hostile"]},{"not":["yeoni_reconciled"]}]}
    _r13g4("life:resident_yeoni:work",
        again=[(_R13G4_YEONI_COLD,[("resident_yeoni","수선은 받아요. 말은 짧게 하고요.")]),
            (None,[("resident_yeoni","마른 옷이면 언제든 가져오세요.")])])
    _r13g4("life:resident_yeoni:after",
        again=[(None,[("resident_yeoni","토리 혼자는 안 보낸다고 했죠. 같이 갔으면 같이 돌아와 주세요.")])])
    _r13g4("life:resident_yeoni:crisis",
        again=[(None,[("resident_yeoni","저희한테 뭘 맡기실지 먼저 말해 달라는 거, 그대로예요.")])])
    _r13g4("rumor_mom:yeoni",steps={"case":"pending"},
        again=[({"has":["J13"]},[("resident_yeoni","까로 아저씨는 짐만 봤다면서요? 그럼 저도 짐 얘기만 들은 거예요.")]),
            (None,[("resident_yeoni","저는 까로 아저씨한테 들은 게 다예요. 직접 본 건 아니에요.")])])
    # grudge_cold:yeoni keeps its first-reading lines (good-rumor prefix, systems/room13_memory.rpy).
    _r13g4("grudge_cold:yeoni",steps={"not":["yeoni_reconciled"]},
        again=[(None,[("resident_yeoni","셈이 끝나기 전에는 할 말 없어요.")])])
    _r13g4("grudge_fix:yeoni",steps={"not":["yeoni_reconciled"]},recap="여니에게 목도리와 장갑 값을 아직 치르지 않았다.")
    _r13g4("yeoni_goods",steps={"not":["ev_n_done"]},recap="교환대의 목도리와 장갑 일은 이미 끝났다.")
    _r13g4("smalltalk:yeoni_seam",timeless=True,
        again=[(None,[("resident_yeoni","입을 때 당기는 곳부터 알려 주세요. 그래야 오래가요.")])])

    # ---------------- 토리 (수줍은 존댓말, 청소년) ----------------
    _r13g4("life:resident_tori:work",
        again=[(None,[("resident_tori","받은 장수는 꼭 적어 둬요. 천 끝만 잡아 주시면 돼요.")])])
    _r13g4("life:resident_tori:after",
        again=[(None,[("resident_tori","가져가는 곳만 적어 주시면 천은 드릴 수 있어요.")])])
    _r13g4("life:resident_tori:crisis",
        again=[(None,[("resident_tori","남는 천은 꼭 돌려주세요. 다음 이불을 만들어야 해서요.")])])
    _r13g4("life:resident_tori:changed",
        again=[(None,[("resident_tori","할머니 물건은 따로 묶어 뒀어요. 맡아 뒀다는 것도 적어 두셨죠?")])])
    _r13g4("life:resident_tori:repair",
        again=[(None,[("resident_tori","수리한 건 톡 씨예요. 남은 부품은 톡 씨한테 확인하세요.")])])
    _r13g4("smalltalk:tori_stitches",timeless=True,
        again=[({"any":[{"case":"occurred"},{"case":"prevented"},_R13G4_AFTER]},[("resident_tori","그 핀 이야기는 그때 들은 게 다예요. 핀은 톡 씨가 맡았으니 톡 씨한테 여쭤보세요.")]),
            (None,[("resident_tori","접히는 부분부터 본다고 했죠. 할머니 목도리도 그렇게 볼 거예요.")])])
    _r13g4("smalltalk:tori_count",timeless=True,
        again=[(None,[("resident_tori","받은 것하고 돌려드린 것, 둘 다 세어 두면 나중에 안 헷갈려요.")])])

    # ---------------- 콩이 (아이, 아빠에게 존댓말) ----------------
    _r13g4("life:resident_kongi:work",
        again=[(None,[("resident_kongi","가게까지 가는 길은 알아요. 그 너머는 몰라요.")])])
    _r13g4("life:resident_kongi:after",
        again=[(None,[("resident_kongi","빵이 언제 나올지는 저도 몰라요. 그러니까 기다리라고는 안 할게요.")])])
    _r13g4("life:resident_kongi:crisis",
        again=[(None,[("resident_kongi","없는 걸 있다고 하지는 말아 주세요. 그 말은 지금도 같아요.")])])
    _r13g4("smalltalk:kongi_basket",timeless=True,
        again=[(None,[("resident_kongi","주방 불빛은 그날 밤에 본 게 다예요. 누가 켰는지는 못 봤어요.")])])
    _r13g4("kongi_errand",steps={"not":["kongi_watching"]},recap="콩이에게 망을 봐 달라고 할 곳이 있을까?")
    _r13g4("kongi_report",steps={"has":["kongi_report_ready"]},recap="콩이가 지켜본 것을 들을 차례다.")

    # ---------------- 꽥순 (청소년, 아빠에게 해요체) ----------------
    _r13g4("life:resident_kkwak:work",
        again=[(None,[("resident_kkwak","얼음 가운데는 밟으면 안 돼요. 돌아온 자국까지 보셔야 하고요.")])])
    _r13g4("life:resident_kkwak:after",
        again=[(None,[("resident_kkwak","빨래할 물은 남겨 두셔야 해요. 그 말은 몇 번이고 할 거예요.")])])
    _r13g4("life:resident_kkwak:crisis",
        again=[(None,[("resident_kkwak","물속 일은 안 맡기신다고 했죠? 그 약속만 지켜 주세요.")])])
    _r13g4("smalltalk:kkwak_ice",timeless=True,
        again=[(None,[("resident_kkwak","통이 비어 있을 때 미리 살피는 게 제일이에요.")])])
    _r13g4("smalltalk:kkwak_tracks",timeless=True,
        again=[(None,[("resident_kkwak","길을 모르면 물어보세요. 안 가는 게 나은 날도 있어요.")])])

    # ---------------- 달그락 (능청스러운 하오체) ----------------
    # 숙박비는 없앤 설정이라(0.19.16) "숙박비를 깎아 줬지"를 물건으로 자리를 얻었다는 말로 덮는다.
    _r13g4("dalgeurak:who",timeless=True,
        variants=[(_R13G4_DETAINED,[
            ("dad","어디서 오셨습니까?"),("resident_dalgeurak","고개 너머 장터를 도는 행상이오. 첫눈 오던 날 짐수레 바퀴가 부러져서 이 마을에 발이 묶였지."),
            ("dad","고개는 넘을 수 있지 않습니까? 저희는 마차로 왔는데요."),("resident_dalgeurak","빈 마차는 겨우 지나가오. 내 짐을 지고 걸어서는 못 넘어. 까로 양반 마차 고쳐지면 짐을 실어 달라고 해 볼 참이오."),
            ("dad","여관에 묵으십니까?"),("resident_dalgeurak","식당 구석 자리요. 할머니가 물건 몇 개 받고 내준 자리였는데, 할머니가 붙잡혀 간 뒤로는 눈치껏 지내오.")]),
            (None,[
            ("dad","어디서 오셨습니까?"),("resident_dalgeurak","고개 너머 장터를 도는 행상이오. 첫눈 오던 날 짐수레 바퀴가 부러져서 이 마을에 발이 묶였지."),
            ("dad","고개는 넘을 수 있지 않습니까? 저희는 마차로 왔는데요."),("resident_dalgeurak","빈 마차는 겨우 지나가오. 내 짐을 지고 걸어서는 못 넘어. 까로 양반 마차 고쳐지면 짐을 실어 달라고 해 볼 참이오."),
            ("dad","여관에 묵으십니까?"),("resident_dalgeurak","식당 구석 자리를 얻었소. 할머니가 물건 몇 개 받고 자리를 내줬지.")])],
        again=[(None,[("resident_dalgeurak","고개 너머 행상이오. 마차가 다니면 그때 짐을 싣고 떠날 참이오.")])])
    # 아빠가 결론을 먼저 말하지 않게: 냄비가 어디서 왔는지는 의문으로 남긴다.
    _r13g4("dalgeurak:eunho",timeless=True,
        variants=[(None,[
            ("dad","은호 사장과는 거래하십니까?"),("resident_dalgeurak","은호 사장은 내 물건을 반값에 사서 제값에 팔고 싶어 하지."),
            ("resident_dalgeurak","그런데 요즘 은호 사장이 나한테 판 냄비 하나가 진료소 것이더구먼. 바닥에 진료소 표시가 있었소."),
            ("dad","(진료소 냄비가 어떻게 은호 사장 손에 들어갔을까?)",{"thought":True})])],
        again=[(None,[("resident_dalgeurak","진료소 표시가 있던 냄비 얘기는 그때 한 그대로요. 은호 사장이 어디서 받았는지는 나도 모르오.")])])
    _r13g4("alibi:case:resident_dalgeurak",steps={"case":"occurred"},recap="달그락은 비명 뒤 할머니가 부엌 뒷문으로 나갔다고 했다.")

    # ---------------- 현이 ----------------
    _r13g4("hyeoni:song",timeless=True,recap="현이의 노래는 그날 마을에 퍼진 말을 따라간다.")
    _r13g4("alibi:night1:resident_hyeoni",timeless=True,recap="현이는 첫날 밤 할머니가 보온병에 차를 담아 갔다고 했다.")
    _r13g4("alibi:case:resident_hyeoni",steps={"case":"occurred"},recap="현이는 비명 때 할머니가 식당에 있었고, 그 뒤 부엌 쪽으로 갔다고 했다.")

    # ---------------- 물결 (시원시원한 해요체) ----------------
    _r13g4("mulgyeol:crossing",timeless=True,
        again=[(None,[("resident_mulgyeol","봄 해빙 전엔 못 건너요. 가까운 얼음판까지만이에요.")])])
    _r13g4("mulgyeol:water",steps={"not":["mom_reunited"]},
        again=[({"has":["Y02"]},[("resident_mulgyeol","숲으로 가던 그 아주머니요? 그 뒤로는 강가에 안 왔어요.")]),
            (None,[("resident_mulgyeol","해 뜨기 전에 왔다가 숲으로 갔어요. 장갑에 도토리 수가 있었고요. 며칠 전부터는 안 와요.")])])
    _r13g4("mulgyeol:water_cold",steps={"not":["mom_reunited"]},
        again=[(None,[("resident_mulgyeol","아주머니 얘기는 그때 한 게 다예요.")])])

    # ---------------- 솔방울 (담백한 해요체) ----------------
    _r13g4("solbang:herbs",timeless=True,
        again=[(None,[("resident_solbang","요즘은 숲 안쪽까지 들어가야 해요. 눈 밑에 숨은 걸 찾느라 손이 많이 가고요.")])])
    _r13g4("solbang:musoe",steps={"has":["solbang_helped"]},
        variants=[({"has":["musoe_gone"]},[
            ("dad","무쇠 할아버지 약은 어떻게 됐습니까?"),
            ("resident_solbang","지어 둔 약은 끝내 못 드렸어요. 할아버지가 강 쪽으로 가셨다고 들었어요."),
            ("resident_solbang","약초 캐러 숲 안쪽까지 갈 때마다 길 표식 천이 하나씩 줄어 있어요. 누가 떼 가는 건지.")])],
        again=[({"has":["musoe_gone"]},[("resident_solbang","약은 못 드렸어요. 표식 천 얘기는 그때 말씀드린 그대로예요.")]),
            (None,[("resident_solbang","사흘 치는 지었어요. 그다음은 눈이 얼마나 오느냐에 달렸죠.")])])

    # ================= 증거 반응 (일반 답만 하던 조합) =================
    R13_REACTIONS[("resident_eunho","J16")]=[
        ({"has":["w2_eunho_credit"]},[("resident_eunho","그 장부 얘기는 이미 끝냈소. 대피소 몫과 이자는 약속한 대로요.")]),
        (None,[("resident_eunho","제가 한 말 그대로 적었구려. 배급표 없는 집에 이자를 붙인 건 맞소."),
            ("resident_eunho","다만 그날 밤 여관 일과는 상관없다는 것도 같이 적어 두시오. 이 장부에는 그 얘기가 없소.")])]
    R13_REACTIONS[("resident_kongi","K01")]=[
        ({"has":["kd_solved"]},[("resident_kongi","밤이가 아니었다면서요. 들은 말을 판 건 저예요."),
            ("resident_kongi","이제 들은 건 들었다고 말할게요.")]),
        ({"has":["kd_failed"]},[("resident_kongi","……밤이가 끌려갔대요. 저는 들은 걸 판 것뿐인데.")]),
        (None,[("resident_kongi","그거 제가 한 말이에요. 근데 본 게 아니라 창고 형들한테 들은 거예요."),
            ("resident_kongi","누가 처음 그 말을 했는지는 저도 몰라요.")])]
    R13_REACTIONS[("resident_madam","H2")]=[
        (None,[("resident_madam","검사원이 셌다면 묶음 수는 맞겠지요."),
            ("resident_madam","그 약초를 왜 쌓아 뒀는지는 여기 안 적혀 있잖아요. 겨울은 길어요.")])]
    R13_REACTIONS[("resident_madam","H3")]=[
        (None,[("resident_madam","뭉치가 그래요? 그 애 말 한마디로 제가 남의 편지를 베껴 오라 했다고 적으실 건가요?"),
            ("resident_madam","할머니 얘기는 할머니께 여쭤보세요. 저는 할 말 없어요.")])]
    R13_REACTIONS[("resident_madam","H4")]=[
        (None,[("resident_madam","바람에 빗장이 걸렸다고 했잖아요."),
            ("resident_madam","검사원이 적은 건 빗장이 걸려 있었다는 것뿐이에요. 왜 그랬는지는 안 적혀 있죠.")])]
    R13_REACTIONS[("resident_madam","H6")]=[
        (None,[("resident_madam","은호 사장이 제 이름을 댔다고요? 저울 나사를 조인 손은 제 손이 아니에요."),
            ("resident_madam","부탁을 했는지 안 했는지는 은호 사장 말뿐이잖아요.")])]
    R13_REACTIONS[("resident_madam","J14")]=[
        (None,[("resident_madam","제가 한 말이에요. 그 상자들은 이미 나갔다고요."),
            ("resident_madam","어디로 갔는지까지 말씀드릴 이유는 없어요.")])]
    R13_REACTIONS[("resident_madam","L09")]=[
        ({"has":["madam_store_opened"]},[("resident_madam","조각은 돌려줬어요. 그 일은 광장에서 끝났잖아요.")]),
        ({"has":["tok_detained"]},[("resident_madam","톡이 붙잡혀 갔다면서요. 저는 값을 치르고 산 물건을 갖고 있을 뿐이에요.")]),
        (None,[("resident_madam","사고판 것뿐이에요. 이름표가 붙어 있든 말든 저는 값을 치렀어요."),
            ("resident_madam","그 조각을 누가 어디서 꺼내 왔는지는 판 사람한테 물으세요.")])]
    R13_REACTIONS[("resident_madam","V04")]=[
        (None,[("resident_madam","쪽문 안쪽까지 보셨군요. 담요가 있는 건 맞아요."),
            ("resident_madam","그 수레에 담요를 실어 달라고 한 사람은 아무도 없었어요.")])]
    R13_REACTIONS[("resident_mungchi","H1")]=[
        (None,[("resident_mungchi","제 서명 맞아요. 부인이 하라는 데 이름만 썼어요."),
            ("resident_mungchi","왜 쌓아 두는지는 몰라요. 저는 자루를 날랐을 뿐이에요.")])]
    R13_REACTIONS[("resident_mungchi","H3")]=[
        (None,[("resident_mungchi","제가 한 말이에요. ……부인한테는 보여 주지 마세요. 정말 갈 데가 없어요.")])]
    R13_REACTIONS[("resident_mungchi","H8")]=[
        (None,[("resident_mungchi","……봉인 뜯은 건 맞아요. 모모 관장님이 사건 난 방 물건은 비싸게 쳐 준다고 해서요."),
            ("resident_mungchi","무엇을 만졌는지는 제가 말한 것밖에 없어요. 다른 건 안 건드렸어요.")])]
    R13_REACTIONS[("resident_siluk","L07")]=[
        ({"has":["lt_solved"]},[("resident_siluk","그 끈 얘기는 광장에서 끝났잖아요. 제 끈 맞아요.")]),
        (None,[("resident_siluk","제 짐 끈 맞아요. 끝이 뜯긴 것도요."),
            ("resident_siluk","이 끈으로 뭘 했는지는…… 끈이 말해 주진 않잖아요.")])]
    R13_REACTIONS[("resident_siluk","L08")]=[
        ({"has":["lt_solved"]},[("resident_siluk","애한테까지 물어보셨던 거죠. 이제 와서 탓하진 않을게요.")]),
        (None,[("resident_siluk","애 말이요? 늦게 들어온 건 맞아요."),
            ("resident_siluk","늦게 들어온 것하고 등을 연 건 다른 얘기잖아요.")])]
    R13_REACTIONS[("resident_siluk","V05")]=[
        (None,[("resident_siluk","제가 한 말이에요. 내려올 땐 늘 빈 수레였다고요."),
            ("resident_siluk","위에서 무슨 일이 있었는지는 몰라요. 끄는 사람은 뒤를 안 봐요.")])]
    R13_REACTIONS[("resident_tori","M01")]=[
        ({"has":["chorong_dead"]},[("resident_tori","이 글씨는 처음 봐요. 등불을 돌보시던 분은…… 이제 안 계시잖아요."),
            ("resident_tori","죄송해요. 저는 그 이상은 몰라요.")]),
        ({"thread":"mom","min":2},[("resident_tori","등불 돌보는 분이면 초롱 씨죠. 이미 아시는 것 같네요."),
            ("resident_tori","이 글씨를 쓴 분은 저는 몰라요.")]),
        (None,[("resident_tori","이 글씨는 처음 봐요. 누가 쓴 건지 저는 몰라요."),
            ("resident_tori","등불 이야기라면, 등을 돌보는 분께 직접 여쭤보는 게 맞을 것 같아요.")])]
    R13_REACTIONS[("resident_yeoni","J11")]=[
        ({"has":["J13"]},[("resident_yeoni","제가 한 말이네요. 까로 아저씨한테 들은 거라고 분명히 말했어요."),
            ("resident_yeoni","까로 아저씨는 짐만 봤다면서요? 그럼 부인이 초소로 갔다는 건 짐 얘기가 부풀려진 걸 수도 있겠네요.")]),
        (None,[("resident_yeoni","제가 한 말이네요. 까로 아저씨한테 들은 거예요."),
            ("resident_yeoni","부인을 직접 본 사람한테 다시 물어보세요. 저는 들은 것만 알아요.")])]
