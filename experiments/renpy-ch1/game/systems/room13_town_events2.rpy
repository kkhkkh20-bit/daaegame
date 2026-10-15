# 마을 사건 묶음 2 (docs/EVENT_CATALOG.md): 실룩의 사기, 누비의 싼 방, 비싼 상품 둘.
# 일당(6~8냥)에서 숙식(10냥)을 빼면 하루 2~4냥 적자다. 큰돈은 사건으로만 생긴다.
init 104 python:
    R13_SHOP["medkit"]=dict(title="도시제 약상자",price=45,day=(2,13),detail="열병 환자 한 사람을 확실히 낫게 한다. 마을에 단 하나뿐이다.")
    R13_SHOP["lockpick"]=dict(title="도시 열쇠공 세트",price=35,day=(2,13),detail="잠긴 상자 하나쯤은 연다. 쓰는 걸 들키면 도둑이 된다.")
    R13_ITEM_ICONS["medkit"]=[
        "................",
        "......kkkk......",
        ".....k....k.....",
        "..kkkkkkkkkkkk..",
        "..kwwwwwwwwwwk..",
        "..kwwwwrrwwwwk..",
        "..kwwwwrrwwwwk..",
        "..kwwrrrrrrwwk..",
        "..kwwrrrrrrwwk..",
        "..kwwwwrrwwwwk..",
        "..kwwwwrrwwwwk..",
        "..kwwwwwwwwwwk..",
        "..kPPPPPPPPPPk..",
        "..kkkkkkkkkkkk..",
        "................",
        "................",
    ]
    R13_ITEM_ICONS["lockpick"]=[
        "................",
        "................",
        "..kkkkkkkkkkkk..",
        "..kcccccccccck..",
        "..kcsSkcsSkcck..",
        "..kcsSkcsSkcck..",
        "..kcsSkcsSkcck..",
        "..kcsSkcsSkcck..",
        "..kcsSkcssSkck..",
        "..kcsSkcsSkcck..",
        "..kcSkkcSkkcck..",
        "..kcccccccccck..",
        "..kkkkkkkkkkkk..",
        "................",
        "................",
        "................",
    ]

    def _ev2_topic(npc,title,day,need=(),flags=(),give=(),not_flags=(),lines=()):
        return dict(npc=npc,title=title,day=list(day),need=list(need),flags=list(flags),give=list(give),not_flags=list(not_flags),lines=list(lines))

    ROOM13["topics"].update({
        "medkit_musoe":_ev2_topic("resident_musoe","도시제 약상자를 건넨다",(2,13),need=["own:medkit"],not_flags=["musoe_recovering"],
            lines=[
            ("resident_musoe","……도시에서 온 약이오? 이 비싼 값을 내가 어떻게 갚소."),
            ("dad","대신 솜이가 남의 창고 지붕을 타지 않게만 해 주십시오."),
            ("resident_musoe","허, 그것까지 알고 왔구려. 이건 폐광 지도요. 빚은 이걸로 먼저 갚겠소.")]),
        "medkit_bori":_ev2_topic("resident_bori","아픈 아이에게 약상자를 쓰자고 한다",(4,13),need=["own:medkit","bori_child_sick"],not_flags=["bori_child_cured"],
            lines=[
            ("resident_bori","애 열이 사흘째예요. ……이 약을 정말 우리 애한테 주시는 거예요?"),
            (None,"보리는 약상자를 끌어안고 한참 동안 말이 없었다."),
            ("resident_bori","제가 장작 훔친 거, 학교에 다 말할게요. 이제 숨길 이유가 없어요.")]),
        "siluk_after":_ev2_topic("resident_siluk","마차 일을 묻는다",(3,14),need=["siluk_ally"],lines=[
            ("resident_siluk","빚이 없으니 손이 가볍네요. 마차는 언제든 부르세요."),
            ("resident_siluk","눈이 크게 오면 아픈 사람부터 마차로 실어 나를게요. 그건 약속해요.")]),
        "siluk_cold":_ev2_topic("resident_siluk","말을 걸어 본다",(3,14),need=["siluk_hostile"],lines=[
            ("resident_siluk","입막음 값은 잘 쓰셨어요? 저는 이제 두 사람한테 빚진 셈이네요.")]),
        "nubi_after":_ev2_topic("resident_nubi","너울의 부탁을 다시 묻는다",(3,14),need=["nubi_ally"],lines=[
            ("resident_nubi","너울이 외지 사람을 데려오면 장작을 주겠다고 했어요. 우리 집 난로가 꺼지면 애들이 못 버텨요."),
            ("resident_nubi","이젠 그런 일 안 할게요. 대신 그 사람 앞에서 제 이름은 꺼내지 말아 줘요.")]),
    })
    # Medkit topics run as labels so the single kit is used up.
    R13_TOPIC_LABELS.update({"medkit_musoe":"r13_medkit_give","medkit_bori":"r13_medkit_give"})
    R13_MEDKIT_RESULTS={"medkit_musoe":(["musoe_recovering","musoe_ally","medkit_used"],["H5"],"무쇠 할아버지가 건넨 지도"),
        "medkit_bori":(["bori_child_cured","bori_ally","medkit_used"],[],"")}
    _R13_SILUK_LOCKPICK=("store","ledger")
    ROOM13["activities"]["use_lockpick_box"]=dict(place="store",title="열쇠공 세트로 장부 밑 잠긴 상자를 연다",lines=[
        (None,"장부 선반 밑에 쇠 띠를 두른 작은 상자가 있었다. 상자 자물쇠는 생각보다 단순했다."),
        (None,"상자 안에는 장부가 들어 있었다. 배급표와 같은 날짜가 적혀 있었다. 빠져나간 곡식과 약초가 모두 이 창고로 들어와 있었다."),
        ("dad","(장부를 베끼고 상자를 도로 잠갔다. 열쇠공 세트는 한 번 쓰고 나니 바늘이 휘어 버렸다.)",{"thought":True})],
        day=[2,13],need=["own:lockpick"],give=["H1"],flags=["lockpick_used"],cost=1,not_flags=["lockpick_used"],item_consume="lockpick")
    R13_CONTEXT_ACTIVITIES[_R13_SILUK_LOCKPICK]=tuple(R13_CONTEXT_ACTIVITIES.get(_R13_SILUK_LOCKPICK,()))+("use_lockpick_box",)

    def r13_cheap_room_refund():
        """누비의 싼 방(6냥): 묵은 밤마다 숙식비 10냥 중 4냥을 돌려받는다."""
        t=r13_town();paid=list(t.get("cheap_nights",[]));day=store.room13["day"]
        if r13_has("lodging_cheap") and day>=3 and (day-1) not in paid:
            paid.append(day-1);r13_town_set(cheap_nights=paid)
            r13_cash(4,"누비의 싼 방 · 방값 차액")

label r13_town_events2:
    $ r13_cheap_room_refund()
    if room13["day"]==3 and room13["period"]==0 and room13["location"]=="square" and not r13_has("ev_a_done"):
        call r13_ev_a_siluk
    if room13["day"]==2 and room13["period"]==1 and room13["location"] in ("inn","square") and not r13_has("ev_q_done"):
        call r13_ev_q_nubi
        if _return=="day":
            return "day"
    return None

# ---- A. 실룩의 "빠른 길" 사기 ----

label r13_ev_a_siluk:
    $ r13_flag("ev_a_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"광장 우물가에서 짐꾼 실룩이 먼저 다가왔다. 잠을 못 잤는지 눈 밑이 거뭇했다."),
        ("resident_siluk","외곽 초소에서 되돌아온 짐 기다리시죠? 정식 길로 가면 이틀 걸려요. 저는 남들 모르는 지름길을 알아요."),
        ("resident_siluk","그 짐, 오늘 안에 받아다 드리죠. 선금 다섯 냥만 주세요.")],"ev:a:offer")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "선금 다섯 냥을 준다" if r13_cash_now()>=5:
                $ r13_cash(-5,"실룩에게 선금")
                call r13_lines([("resident_siluk","해 지기 전에 짐 가지고 올게요. 걱정 마세요."),
                    (None,"실룩은 해가 져도, 다음 날이 되어도 오지 않았다."),
                    ("resident_kongi","실룩 아저씨요? 어제 백 부인네 뒷문으로 들어가던데요.")],"ev:a:paid")
                $ r13_flag("siluk_scammed","know_siluk_debt")
            "가진 돈을 모두 준다" if 0<r13_cash_now()<5:
                $ r13_cash(-r13_cash_now(),"실룩에게 선금(가진 돈 전부)")
                call r13_lines([("resident_siluk","……이것뿐이에요? 뭐, 일단 받죠."),
                    (None,"그 뒤로 실룩은 다시 나타나지 않았다.")],"ev:a:paid_all")
                $ r13_flag("siluk_scammed")
            "거절한다":
                call r13_lines([("resident_siluk","후회하실 텐데요. 되돌아온 짐은 오래 두면 젖어요.")],"ev:a:refuse")
            "짐을 받아 오면 돈을 주겠다고 한다":
                call r13_lines([("resident_siluk","짐 받아 온 다음에 주신다고요? 저도 돈이 급하다고요!"),
                    ("resident_siluk","……백 부인한테 진 빚을 오늘까지 갚아야 해서요. 아, 아무것도 아니에요.")],"ev:a:later")
                $ r13_flag("know_siluk_debt")
                $ _ep_loop=True
            "바둑이를 불러 증인으로 세운다" if r13_has("badook_doubt") or r13_has("badook_ally"):
                call r13_lines([("resident_badook","실룩, 또 그 지름길 얘기야? 지난주에도 누가 너한테 선금을 떼였다던데."),
                    ("resident_siluk","……백 부인한테 진 빚 때문이에요. 이자가 매일 붙어요. 안 갚으면 마구간 일자리도 잃어요.")],"ev:a:badook")
                $ r13_flag("know_siluk_debt","siluk_shamed")
                $ _ep_loop=True
            "돈을 주고 몰래 뒤를 밟는다" if r13_cash_now()>=5:
                $ r13_cash(-5,"실룩에게 선금")
                call r13_lines([(None,"실룩은 초소 쪽이 아니라 백 부인 집 뒷골목으로 갔다. 뭉치가 문을 열고 나와 동전을 받아 갔다."),
                    ("resident_mungchi","이번 주 이자는 받았어요. 부인이 다음 주엔 원금도 받겠대요."),
                    ("dad","(내가 준 돈은 결국 백 부인 금고로 갔다. 실룩은 심부름꾼일 뿐이다.)",{"thought":True})],"ev:a:follow")
                $ r13_flag("siluk_scammed","know_siluk_debt","know_madam_hoard")
            "“백 부인 빚 때문입니까?”" if r13_has("know_siluk_debt") or r13_has("know_madam_hoard"):
                call r13_lines([("resident_siluk","……제 빚 얘기를 어떻게 알았어요?"),
                    ("resident_siluk","이제는 이자가 원금보다 더 많아요. 갚아도 갚아도 빚이 남아요.")],"ev:a:confront")
                menu:
                    "빚을 갚아 주고 마차를 맡긴다 (8냥)" if r13_cash_now()>=8:
                        $ r13_cash(-8,"실룩의 빚을 대신 갚음")
                        call r13_lines([("resident_siluk","진짜요? ……그럼 이제 제 마차는 탐정님 거예요. 부르시면 언제든 갈게요.")],"ev:a:pay_debt")
                        $ r13_flag("siluk_ally","siluk_cart")
                    "백 부인 장부에서 빚을 지워 주겠다고 한다" if "H1" in room13["evidence"]:
                        call r13_lines([("dad","백 부인이 배급 물자를 쌓아 둔 기록이 장부에 남아 있습니다. 그 사람은 빚을 받을 처지가 못 됩니다."),
                            ("resident_siluk","……그 장부를 들이밀면 부인도 입을 다물겠네요. 이제 제 마차는 탐정님 편에 서겠습니다.")],"ev:a:ledger")
                        $ r13_flag("siluk_ally","siluk_cart","madam_hostile")
                    "입막음 값으로 여덟 냥을 받는다":
                        $ r13_cash(8,"실룩의 입막음 값")
                        call r13_lines([("resident_siluk","……그럼 이건 우리끼리만 아는 일로 해요."),
                            (None,"실룩은 동전을 세며 끝내 고개를 들지 않았다.")],"ev:a:extort")
                        $ r13_flag("siluk_hostile","rumor:extortion")
                    "그냥 보내 준다":
                        call r13_lines([("resident_siluk","……고마워요. 다음부터는 정직하게 일할게요.")],"ev:a:let_go")
    return

# ---- Q. 누비의 싼 방 ----

label r13_ev_q_nubi:
    $ r13_flag("ev_q_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"누비 아주머니가 빨래 바구니를 내려놓고 내 소매를 잡았다."),
        ("resident_nubi","여관비가 하루 열 냥이죠? 우리 집 별채는 하루 여섯 냥이에요. 따뜻하고, 밥도 줘요."),
        ("dad","(사흘만 묵어도 열두 냥이 남는다. 솔깃하다.)",{"thought":True}),
        ("resident_nubi","별채 열쇠는 제가 갖고 있을게요. 밤에 문단속은 제가 해 드려요."),
        (None,"누비 아주머니는 말하면서 자꾸 초소 쪽을 돌아보았다.")],"ev:q:offer:v2")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "그 방으로 옮긴다":
                call r13_lines([(None,"별채는 따뜻했다. 문이 밖에서 잠기기 전까지는."),
                    ("neoul","외지 사람은 열병 검사를 받기 전까지 격리요. 신고가 들어왔소."),
                    ("dad","신고요? 대체 누가……"),
                    (None,"문틈으로 누비 아주머니의 뒷모습이 보였다. 손에 장작 한 묶음을 들고 있었다."),
                    (None,"다음 날 오후가 되어서야 별채 문이 열렸다.")],"ev:q:quarantined")
                $ r13_next_day()
                $ r13_edit(period=1,location="inn")
                $ r13_flag("quarantined_once","know_neoul_quarantine")
                $ r13_grant(["W1"],"격리 별채에서 들은 말")
                return "day"
            "거절한다":
                call r13_lines([("resident_nubi","……그래요. 아무래도 여관이 편하시겠죠.")],"ev:q:refuse")
            "별채가 왜 그렇게 싼지 묻는다":
                call r13_lines([("resident_nubi","값을 싸게 해야 사람이 오죠."),
                    ("dad","여관비 절반 값에 밥까지 준다고요?"),
                    ("resident_nubi","……너울이 외지 사람을 데려오면 장작을 줘요. 열병 검사한다고 하루 가둬 두는 것뿐이에요."),
                    ("resident_nubi","우리 집 난로가 꺼지면 애들이 이 겨울을 못 버텨요. 미안해요.")],"ev:q:ask")
                $ r13_flag("know_neoul_quarantine")
                menu:
                    "비밀로 해 주고, 다시는 하지 말라고 한다":
                        call r13_lines([("resident_nubi","……고마워요. 별채는 그냥 여섯 냥에 쓰셔도 돼요. 이번엔 진짜로요.")],"ev:q:keep_secret")
                        $ r13_flag("nubi_ally","lodging_cheap")
                    "서리 검사원에게 알린다":
                        call r13_lines([("resident_seori","검사권도 없는 경비가 주민을 시켜 사람을 가둔다고요? 기록하겠습니다."),
                            ("resident_nubi","……이제 장작 받는 것도 끝이네요.")],"ev:q:report")
                        $ r13_flag("neoul_exposed","nubi_hostile")
                    "너울에게 가서 따진다":
                        call r13_lines([("neoul","격리는 마을을 위한 거요. 누비가 무슨 말을 했든 간에."),
                            (None,"그날 저녁 누비네 장작더미가 반으로 줄었다는 말을 들었다.")],"ev:q:confront_neoul")
                        $ r13_flag("nubi_punished","neoul_annoyed")
            "건강 확인서를 받아 두고 옮긴다":
                call r13_lines([("resident_seori","열 없음, 기침 없음. 외지 사람이라는 건 병이 아닙니다."),
                    (None,"그날 밤 별채 문 앞에서 너울이 확인서를 읽고 혀를 찼다."),
                    ("neoul","……검사원 도장이 찍혔군. 그럼 됐소."),
                    ("resident_nubi","그 신고, 너울이 시킨 거였어요. 미안해요. 방은 여섯 냥 그대로 쓰세요.")],"ev:q:certificate")
                $ r13_flag("lodging_cheap","nubi_ally","know_neoul_quarantine","seori_met")
    return None

label r13_medkit_give:
    call r13_lines(ROOM13["topics"][r13_topic]["lines"],"medkit:"+r13_topic)
    $ _mk_flags,_mk_give,_mk_source=R13_MEDKIT_RESULTS[r13_topic]
    $ r13_flag(*_mk_flags)
    if _mk_give:
        $ r13_grant(_mk_give,_mk_source)
    $ r13_use_item("medkit")
    $ r13_finish_topic(r13_topic)
    return None
