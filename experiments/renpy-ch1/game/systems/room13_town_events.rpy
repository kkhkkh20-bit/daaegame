# 마을 사건 묶음 1 (docs/EVENT_CATALOG.md): 3일째 밤의 한 덩어리.
#   B 솜이의 약 도둑, C 백 부인의 고액 일자리(감금), N 여니의 장물, M 심부름꾼 콩이.
# 첫 회차에는 놓치거나 당한다. 다시 할 때는 사건 시각과 길을 아는 것이 이득이다.
# 회차 사이에 넘어가는 것은 없다(systems/room13_no_carryover.rpy): 깃발은 모두 이번 회차 것.
# 1주차 재판의 사실 입증은 기존 증거로만 한다. 여기서 얻는 기록(H1~H5)은 정황·2주차용이다.
init 102 python:
    ROOM13["evidence"]["H1"]=dict(id="H1",name="백 부인의 비축 장부",kind="기록",
        establishes="배급에서 빠진 곡식과 약초가 백 부인 창고로 들어갔다. 날짜마다 뭉치의 서명이 있다.",
        does_not_establish="누가 시켰는지, 촌장이 알았는지는 적혀 있지 않다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["H2"]=dict(id="H2",name="검사원이 센 창고 약초",kind="기록",
        establishes="마을에 약이 없다던 날, 백 부인 창고에서 나온 해열 약초 꾸러미를 서리 검사원이 직접 세어 적었다.",
        does_not_establish="백 부인이 왜 약을 쌓아 두었는지는 알 수 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["H3"]=dict(id="H3",name="뭉치의 말",kind="증언",
        establishes="백 부인이 뭉치에게 13호의 편지와 쪽지를 베껴 오라고 시켰다. 할머니가 값을 쳐 준다고 했다.",
        does_not_establish="할머니가 그 글로 무엇을 하려 했는지는 뭉치도 모른다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["H4"]=dict(id="H4",name="서리 검사원의 감금 확인",kind="기록",
        establishes="백 부인이 일을 맡긴 사람을 창고 안에 두고 밖에서 빗장을 질렀다. 서리 검사원이 그 자리에서 확인했다.",
        does_not_establish="왜 가두려 했는지는 백 부인이 말하지 않았다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["H5"]=dict(id="H5",name="무쇠 할아버지의 폐광 지도",kind="기록",
        establishes="폐광의 넓은 갱도와 막힌 곳. 눈보라가 칠 때 여러 사람이 바람을 피할 수 있는 자리가 표시돼 있다.",
        does_not_establish="지금도 무너지지 않고 들어갈 수 있는지는 직접 봐야 한다.",scenes=[],current_run_only=True,retained_on_show=True)
    R13_RECORD_SHORT.update(H1="비축 장부",H2="창고 약초 수",H3="뭉치의 말",H4="감금 확인",H5="폐광 지도")

    R13_SHOP["wedge"]=dict(title="나무 쐐기",price=2,day=(2,13),detail="문틈에 끼워 두면 밖에서 빗장을 질러도 문이 끝까지 닫히지 않는다.")
    R13_ITEM_ICONS["wedge"]=[
        "................",
        "................",
        "................",
        "............kk..",
        "..........kkbk..",
        "........kkbbbk..",
        "......kkbbbBbk..",
        "....kkbbbBbbbk..",
        "..kkbbbBbbbbBk..",
        ".kbbbbbbbbbbBk..",
        ".kBBBBBBBBBBBk..",
        ".kkkkkkkkkkkkk..",
        "................",
        "................",
        "................",
        "................",
    ]

    R13_KONGI_PLACES=(("store","공동 창고"),("workshop","수리점 뒤 골목"),("post","우체국"),("kitchen","여관 주방"))

    def r13_town():
        return dict((store.room13 or {}).get("town",{}))

    def r13_town_set(**values):
        n=winter_copy.deepcopy(store.room13);n.setdefault("town",{}).update(values);store.room13=n

    def r13_cash(delta,text):
        n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n)
        wallet["cash"]=max(0,wallet["cash"]+delta)
        wallet["ledger"].append(dict(day=n["day"],text=text,amount=delta))
        n["livelihood"]=wallet;store.room13=n

    def r13_cash_now():
        return r13_wallet(store.room13)["cash"]

    def r13_use_item(item):
        n=winter_copy.deepcopy(store.room13);wallet=r13_wallet(n)
        if item in wallet["items"]:wallet["items"].remove(item)
        wallet["used"]=list(dict.fromkeys(wallet["used"]+[item]))
        n["livelihood"]=wallet;store.room13=n

    def r13_forget_topic(key):
        # Repeatable errands must not stay "read".
        n=winter_copy.deepcopy(store.room13)
        if key in n.get("read_topics",[]):n["read_topics"].remove(key)
        store.room13=n

    def r13_kongi_report(place,day,flags):
        """What 콩이 saw at `place` on `day`: (lines, flags to set)."""
        if place=="store":
            lines=[("resident_kongi","해 질 녘마다 뭉치가 창고 뒷문으로 자루를 날라요. 장부엔 안 적고요. 백 부인 집 쪽으로요.")]
            got=["know_madam_hoard"]
            if day==2:
                lines.append(("resident_kongi","솜이도 왔었어요. 창고 지붕을 한참 올려다보더니 수리점 뒤 골목으로 갔어요."))
                got.append("somi_route_seen")
            elif day>=3 and "ev_b_caught" not in flags:
                lines.append(("resident_kongi","오후에 솜이가 지붕으로 들어갔다 나왔어요! 꾸러미를 안고 수리점 뒤 골목으로 뛰었어요."))
                got.append("somi_route_seen")
            return lines,got
        if place=="workshop":
            return ([("resident_kongi","골목 끝 집에서 기침 소리가 계속 났어요. 솜이네 할아버지요."),
                ("resident_kongi","솜이가 문 앞에서 '창고엔 약이 있는데' 하고 울었어요. 저한텐 말하지 말래요.")],
                ["somi_route_seen","know_musoe_sick"])
        if place=="post":
            return ([("resident_kongi","슬링 아저씨가 여관으로 가는 편지는 따로 빼 둬요. 할머니가 오면 먼저 보여 주고요.")],["know_sling_letters"])
        return ([("resident_kongi","밤에 주방 뒷문 쪽에서 등불이 왔다 갔다 했어요. 누군지는 못 봤어요. 문이 아니라 벽 쪽으로 갔어요.")],["know_kitchen_rear"])

    def r13_town_daily():
        """Called on every arrival: ready 콩이's report the day after the watch."""
        watch=r13_town().get("kongi_watch")
        if watch and store.room13["day"]>watch["day"] and not r13_has("kongi_report_ready"):
            r13_flag("kongi_report_ready")

    def r13_lock_overnight(room_safe):
        # Locked in until the next morning: the morning is lost, half pay.
        r13_cash(7,"백 부인 창고 정리 · 절반만 받음")
        had_warning="E18" in store.room13["evidence"]
        r13_next_day()
        r13_edit(period=1,location="store")
        if not room_safe:
            r13_flag("room_searched")
            if had_warning:r13_flag("warning_exposed")

    ROOM13["topics"]["kongi_errand"]=dict(npc="resident_kongi",title="하루 동안 한 곳을 지켜봐 달라고 한다",day=[1,6],need=[],give=[],flags=[],not_flags=["kongi_watching"],lines=[])
    ROOM13["topics"]["kongi_report"]=dict(npc="resident_kongi",title="어제 지켜본 것을 듣는다",day=[2,7],need=["kongi_report_ready"],give=[],flags=[],lines=[])
    ROOM13["topics"]["somi_worry"]=dict(npc="resident_somi",title="무슨 걱정이 있는지 묻는다",day=[2,3],need=[],give=[],flags=["know_musoe_sick","somi_route_seen"],lines=[
        (None,"솜이는 구두 밑창의 얼음을 긁다가 손을 멈췄다."),
        ("resident_somi","걱정 없어요. ……할아버지 기침이 안 멎는 거 말고는요."),
        ("dad","약은 구했니?"),
        ("resident_somi","약은 없대요. 다들 없대요. 있는 데엔 있는데."),
        ("dad","어디 사니? 할아버지께 한번 가 봐도 될까."),
        ("resident_somi","수리점 뒤 골목 끝 집이요. 오시지 마세요. 할아버지가 남 신세 지는 거 싫어해요.")])
    ROOM13["topics"]["somi_after_trust"]=dict(npc="resident_somi",title="할아버지 상태를 묻는다",day=[4,14],need=["somi_trust"],give=[],flags=[],lines=[
        ("resident_somi","할아버지가 오늘은 앉아서 수프를 드셨어요."),
        ("resident_somi","아저씨가 백 부인한테 안 가져간 거, 할아버지한테 말했어요. 빚졌다고, 꼭 갚으래요.")])
    ROOM13["topics"]["somi_after_roof"]=dict(npc="resident_somi",title="지붕 길 이야기를 한다",day=[4,14],need=["roof_path"],give=[],flags=[],lines=[
        ("resident_somi","백 부인 창고는 굴뚝 옆 판자가 헐거워요. 밤엔 미끄러우니까 발은 처마 쪽에 두세요."),
        ("resident_somi","저 놔준 거, 고마운 건 아니에요. 그냥 그런 거래였어요.")])
    ROOM13["topics"]["somi_after_hostile"]=dict(npc="resident_somi",title="말을 걸어 본다",day=[4,14],need=["somi_hostile"],give=[],flags=[],lines=[
        (None,"솜이는 내 얼굴을 보자마자 지붕 쪽으로 돌아섰다."),
        ("resident_somi","약 판 돈으로 밥은 맛있게 드셨어요?")])
    ROOM13["topics"]["musoe_after_good"]=dict(npc="resident_musoe",title="몸은 좀 어떤지 묻는다",day=[4,14],need=["musoe_recovering"],give=[],flags=[],lines=[
        ("resident_musoe","열은 내렸소. 솜이 녀석이 다 말했소."),
        ("resident_musoe","그 지도는 갖고 있으시오. 눈이 크게 오면, 그 굴 말고는 숨을 데가 없소.")])
    ROOM13["topics"]["musoe_after_bad"]=dict(npc="resident_musoe",title="몸은 좀 어떤지 묻는다",day=[4,14],need=["musoe_worse"],give=[],flags=[],lines=[
        (None,"무쇠 할아버지는 기침을 참느라 말을 몇 번 끊었다."),
        ("resident_musoe","솜이를 광장에 세웠다지. 약 몇 줌 때문에."),
        ("resident_musoe","당신 같은 외지 사람한테 기대한 내가 늙은 거요.")])
    ROOM13["topics"]["madam_after_trust"]=dict(npc="resident_madam",title="창고 일을 묻는다",day=[4,14],need=["madam_trust"],give=[],flags=[],lines=[
        ("resident_madam","도둑을 잡아 준 건 고마워요. 요즘 같은 때엔 믿을 손이 귀하죠."),
        ("resident_madam","물건이 왜 그렇게 많냐고요? 겨울은 길어요. 끝까지 살아남는 집이 있어야 나머지도 살지.")])
    ROOM13["topics"]["madam_after_hostile"]=dict(npc="resident_madam",title="말을 걸어 본다",day=[4,14],need=["madam_hostile"],give=[],flags=[],lines=[
        ("resident_madam","검사원을 데려와서 남의 창고를 세게 했다지요."),
        ("resident_madam","외지 사람은 겨울이 끝나면 떠나요. 우리는 남고. 그걸 잊지 마세요.")])
    ROOM13["topics"]["yeoni_goods"]=dict(npc="resident_yeoni",title="교환대의 낯익은 물건을 묻는다",day=[4,7],need=["room_searched"],give=[],flags=[],not_flags=["ev_n_done"],lines=[])
    ROOM13["topics"]["mungchi_confront"]=dict(npc="resident_mungchi",title="13호에서 가져간 물건을 따진다",day=[4,8],need=["know_mungchi_thief"],give=["H3"],flags=["mungchi_confessed"],not_flags=["mungchi_confessed"],lines=[
        (None,"뭉치는 작은 상자와 큰 상자 사이에서 눈을 굴렸다."),
        ("resident_mungchi","저, 저는 시키는 대로 한 거예요. 부인이 13호에 편지나 쪽지가 있으면 베껴 오라고……"),
        ("dad","베껴서 누구에게 줬지?"),
        ("resident_mungchi","부인한테요. 부인은 여관 할머니가 값을 쳐 준다고 했어요. 그게 다예요. 물건은 그냥…… 손이 갔어요."),
        ("resident_mungchi","부인한테 말하지 마세요. 저 내쫓기면 갈 데 없어요.")])

    # Topics handled by a label (choices inside). Return "roam" when time or place changed.
    R13_TOPIC_LABELS={"kongi_errand":"r13_ev_kongi_errand","kongi_report":"r13_ev_kongi_report","yeoni_goods":"r13_ev_yeoni_goods"}

label r13_town_events:
    $ r13_town_daily()
    if room13["day"]==3 and room13["period"] in (1,2) and not r13_has("ev_b_done"):
        if room13["location"]=="workshop" and room13["period"]==1 and r13_has("somi_route_seen"):
            call r13_ev_b_ambush
        elif room13["location"]=="store":
            call r13_ev_b_store
    if room13["day"]>=4 and not r13_has("ev_b_done"):
        call r13_ev_b_missed
    if (room13["day"]==3 and room13["period"]==2 and room13["location"]=="inn"
            and not r13_has("ev_c_done") and not r13_has("madam_hostile")):
        call r13_ev_c_offer
        if _return=="day":
            return "day"
    return None

# Arrival events run before r13_roam draws the place: draw it first.
label r13_ev_here(mood):
    call r13_scene(R13_PLACES[room13["location"]][1],R13_PLACES[room13["location"]][0],mood)
    return

# ---- B. 솜이의 약 도둑 ----

label r13_ev_b_store:
    call r13_scene("r13_store","공동 창고 앞 · 소동","search")
    if room13["period"]==1:
        call r13_lines([(None,"창고 앞이 소란스러웠다. 문 옆 보관함 봉인이 뜯겨 있었다."),
            ("resident_madam","내 약초 꾸러미가 없어졌어! 지붕으로 뭔가 뛰어갔다고!"),
            ("resident_madam","잡아 오는 사람한테 열 냥 주지. 열 냥이에요."),
            (None,"창고 지붕 끝에서 작은 그림자가 미끄러지듯 넘어갔다. 수리점 쪽이었다.")],"ev:b:store:afternoon")
    else:
        call r13_lines([(None,"저녁 창고 앞에서 뭉치가 빈 보관함을 붙들고 서 있었다."),
            ("resident_mungchi","부인 약초가 없어졌어요. 지붕으로요. 잡아 오면 열 냥 준대요."),
            (None,"지붕 위 눈에 작은 발자국이 수리점 쪽으로 이어져 있었다.")],"ev:b:store:evening")
    $ r13_flag("ev_b_seen")
    menu:
        "지붕을 따라 쫓아간다":
            $ r13_tick()
            call r13_lines([(None,"처마를 따라 몇 집을 지나자 발자국이 눈 덮인 굴뚝 사이에서 끊겼다."),
                ("dad","(지붕 위에서는 저 아이가 나보다 빠르다.)",{"thought":True})],"ev:b:roof_lost")
            $ r13_flag("ev_b_done","ev_b_lost","musoe_herbs")
        "수리점 쪽 골목으로 돌아가 앞질러 간다":
            $ r13_tick()
            call r13_ev_b_caught
        "왕구에게 알린다":
            call r13_lines([("neoul","도둑이요? 경비를 풀겠습니다. 이런 때일수록 본보기가 있어야지요."),
                (None,"다음 날 아침, 솜이가 광장 기둥 옆에 서 있었다는 이야기를 들었다. 약초는 백 부인에게 돌아갔다.")],"ev:b:guard")
            $ r13_flag("ev_b_done","somi_punished","musoe_worse","guard_caught_somi")
        "모른 척한다":
            call r13_lines([("dad","(남의 창고 일이다. 우리에겐 우리 일이 있다.)",{"thought":True})],"ev:b:ignore")
            $ r13_flag("ev_b_done","ev_b_ignored","musoe_herbs")
    return

label r13_ev_b_ambush:
    call r13_ev_here("search")
    call r13_lines([(None,"수리점 뒤 골목은 좁고 조용했다. 끝 집 문틈으로 마른기침 소리가 새어 나왔다."),
        ("dad","(솜이는 이 길로 돌아온다.)",{"thought":True})],"ev:b:ambush:arrive")
    menu:
        "골목 입구에서 기다린다":
            $ r13_tick()
            call r13_lines([(None,"해가 기울 무렵, 지붕에서 작은 몸이 툭 떨어졌다. 솜이가 꾸러미를 품에 안고 골목으로 뛰어들었다.")],"ev:b:ambush:wait")
            call r13_ev_b_caught
        "오늘은 그냥 지나간다":
            pass
    return

label r13_ev_b_caught:
    $ r13_flag("ev_b_caught","know_musoe_sick")
    call r13_lines([(None,"골목 모퉁이에서 솜이와 정면으로 부딪쳤다. 꾸러미가 눈 위로 굴렀다."),
        ("resident_somi","놔요! 할아버지 거예요!"),
        (None,"꾸러미 끈에는 백 부인 창고의 도장이 찍혀 있었다. 안에는 마른 해열 약초가 가득했다."),
        ("resident_somi","약 없다고 했잖아요. 다들 없다고. 근데 저 창고엔 있었어요. 산더미로요.")],"ev:b:caught")
    menu:
        "꾸러미를 백 부인에게 돌려준다 (현상금 10냥)":
            call r13_lines([("resident_madam","아이고, 찾았네. 약속은 약속이지. 열 냥."),
                ("resident_madam","그 애는 왕구에게 넘기세요. 버릇을 들여야 해요."),
                (None,"솜이는 끌려가면서 한 번도 뒤를 돌아보지 않았다.")],"ev:b:return_madam")
            $ r13_cash(10,"백 부인의 현상금")
            $ r13_flag("ev_b_done","madam_trust","somi_punished","musoe_worse","somi_hostile")
        "지붕 길을 알려 주면 놓아준다":
            call r13_lines([("dad","창고 지붕으로 어떻게 들어갔는지 알려 주면 못 본 걸로 하마."),
                ("resident_somi","……굴뚝 옆 판자가 헐거워요. 밤엔 미끄럽고요. 됐죠?"),
                (None,"솜이는 꾸러미를 낚아채 골목 끝 집으로 사라졌다.")],"ev:b:roof_deal")
            $ r13_flag("ev_b_done","roof_path","musoe_herbs","somi_owes")
        "꾸러미를 빼앗아 은호 사장에게 판다":
            call r13_lines([("resident_somi","그거 할아버지 거라니까요!"),
                (None,"은호 사장은 끈의 도장을 보고 입꼬리를 올렸다."),
                ("resident_eunho","백 부인 거네요. 값은 쳐 드리죠. 열여덟 냥. 대신 이건 우리 둘만 아는 걸로 해요."),
                ("dad","(이제 이 사람이 내 약점을 하나 쥐었다.)",{"thought":True})],"ev:b:sell_eunho")
            $ r13_tick()
            $ r13_cash(18,"은호에게 약초를 넘김")
            $ r13_flag("ev_b_done","eunho_holds_secret","musoe_worse","somi_hostile","rumor:sold_stolen")
        "무쇠 할아버지에게 직접 가져다준다":
            call r13_lines([(None,"골목 끝 집은 차가웠다. 무쇠 할아버지는 이불을 둘둘 감고도 떨고 있었다."),
                ("resident_musoe","……남의 창고 물건이오?"),
                ("dad","약이 없다던 창고에서 나온 겁니다. 지금은 드시는 게 먼저입니다."),
                (None,"약초를 달이는 동안 할아버지는 안주머니에서 접힌 종이를 꺼냈다."),
                ("resident_musoe","폐광 지도요. 눈이 크게 오면 그 굴 말고는 바람 피할 데가 없소. 빚은 이걸로 갚겠소.")],"ev:b:give_musoe")
            $ r13_grant(["H5"],"무쇠 할아버지가 건넨 지도")
            $ r13_flag("ev_b_done","musoe_recovering","musoe_ally","somi_trust")
        "서리 검사원에게 가져가 기록하게 한다":
            call r13_lines([(None,"진료실의 서리 검사원은 꾸러미를 저울에 올리고 하나씩 셌다."),
                ("resident_seori","창고 도장, 해열 약초 서른두 묶음. 마을에 약이 없다고 보고된 날짜와 같은 날입니다."),
                ("resident_seori","아이는 처벌 대신 진술로 남기겠습니다. 약 일부는 여기서 그 할아버지께 쓰지요."),
                ("resident_somi","……정말요?")],"ev:b:seori_record")
            $ r13_tick()
            $ r13_grant(["H2"],"서리 검사원이 센 창고 약초")
            $ r13_flag("ev_b_done","madam_hostile","somi_protected","musoe_herbs","somi_trust")
        "일부만 백 부인에게 돌려준다":
            call r13_lines([("dad","(꾸러미를 반으로 나눴다. 반은 솜이 품에, 반은 백 부인에게.)",{"thought":True}),
                ("resident_madam","……이게 다예요? 묶음이 모자란 것 같은데."),
                ("dad","찾은 건 이것뿐입니다."),
                ("resident_madam","흥. 다섯 냥이요. 반만 찾았으니까.")],"ev:b:split")
            $ r13_cash(5,"백 부인의 현상금 절반")
            $ r13_flag("ev_b_done","musoe_herbs","madam_suspicious","somi_owes")
    return

label r13_ev_b_missed:
    call r13_ev_here("calm")
    call r13_lines([(None,"광장에서 사람들이 수군거렸다. 어제 백 부인 창고에서 약초 꾸러미가 사라졌는데, 범인은 못 잡았다고 했다.")],"ev:b:missed")
    $ r13_flag("ev_b_done","ev_b_missed","musoe_herbs")
    return

# ---- C. 백 부인의 고액 일자리 ----

label r13_ev_c_offer:
    call r13_ev_here("night")
    $ r13_speaker("resident_madam","neutral")
    if r13_has("madam_trust"):
        call r13_lines([("resident_madam","낮의 일은 고마웠어요. 믿을 손이 필요해서 그런데."),
            ("resident_madam","오늘 밤 창고 재고 좀 세어 줘요. 열다섯 냥 드리지.")],"ev:c:offer:trust")
    else:
        call r13_lines([("resident_madam","탐정 양반, 손이 비어 보이네요. 오늘 밤 창고 재고 좀 세어 줘요. 열다섯 냥."),
            ("dad","(일당의 두 배다. 밤일이라 해도 지나치게 후하다.)",{"thought":True})],"ev:c:offer")
    $ r13_flag("ev_c_done")
    menu:
        "거절한다":
            call r13_lines([("resident_madam","그래요? 아쉽네. 다른 손을 찾지 뭐.")],"ev:c:refuse")
            $ r13_flag("ev_c_refused")
            return None
        "받아들인다":
            call r13_ev_c_locked(False)
            return "day"
        "다람이에게 방을 지켜 달라고 하고 받아들인다" if room13.get("daram_state") in ("with_dad","rescued") and r13_has("lodging"):
            call r13_lines([("dad","아빠 일하러 다녀올게. 누가 와도 문 열지 말고, 오면 이름만 물어봐."),
                ("daram","응. 내가 지킬게.")],"ev:c:daram_guard")
            call r13_ev_c_locked(True)
            return "day"
        "쐐기를 챙겨 들고 받아들인다" if r13_has("own:wedge"):
            call r13_ev_c_wedge
            return None
        "서리 검사원에게 미리 말해 두고 받아들인다":
            call r13_ev_c_seori
            return None
        "받아들이는 척하고 13호로 돌아와 숨어 기다린다":
            call r13_ev_c_mungchi
            return None
        "일은 거절하고, 밤에 지붕 길로 창고에 들어간다" if r13_has("roof_path"):
            call r13_ev_c_roof
            return None
    return None

label r13_ev_c_locked(room_safe):
    call r13_scene("r13_store","백 부인 창고 · 밤","night")
    call r13_lines([(None,"창고 안은 생각보다 넓었다. 자루를 세는 사이 등 뒤에서 문이 닫혔다."),
        (None,"밖에서 빗장이 걸리는 소리가 났다."),
        ("dad","부인? 문이 잠겼습니다!"),
        (None,"대답은 없었다. 등잔 기름이 다 탈 때까지 문을 두드렸다. 밤은 길었다.")],"ev:c:locked")
    $ r13_lock_overnight(room_safe)
    call r13_lines([("resident_mungchi","어, 아침이네요. 부인이 문이 저절로 잠겼대요."),
        ("resident_madam","일을 다 못 끝냈으니 절반만 드릴게요. 일곱 냥.")],"ev:c:released")
    if room_safe:
        call r13_lines([(None,"13호로 돌아가자 다람이가 문 뒤에서 졸고 있었다."),
            ("daram","밤에 누가 왔어. 뭉치 아저씨. 이름 물어보니까 그냥 갔어.")],"ev:c:room_safe")
    else:
        call r13_lines([(None,"13호로 돌아가자 짐이 뒤집혀 있었다. 수첩 사이에 끼워 둔 종이들이 다른 순서로 꽂혀 있었다."),
            ("dad","(누군가 밤새 이 방을 뒤졌다. 그래서 나를 가뒀다.)",{"thought":True})],"ev:c:room_searched")
    return

label r13_ev_c_wedge:
    call r13_scene("r13_store","백 부인 창고 · 밤","night")
    call r13_lines([(None,"창고에 들어서며 문틈 아래에 쐐기를 밀어 넣었다. 문이 닫히는 소리가 나고 빗장이 걸렸지만, 손가락 하나 들어갈 틈이 남았다."),
        (None,"재고를 세던 손이 안쪽 선반에서 멈췄다. 배급표와 같은 날짜가 적힌 장부. 빠져나간 곡식과 약초가 모두 이 창고로 들어와 있었다."),
        ("dad","(이걸 보이고 싶지 않았다면, 나를 왜 불렀을까. 아니, 나를 여기 묶어 둘 생각이었다.)",{"thought":True}),
        (None,"새벽 전에 틈으로 빗장을 들어 올려 나왔다. 백 부인은 문이 열려 있는 걸 보고 말없이 열다섯 냥을 내밀었다.")],"ev:c:wedge")
    $ r13_use_item("wedge")
    $ r13_grant(["H1"],"백 부인 창고 안쪽 선반")
    $ r13_cash(15,"백 부인 창고 정리")
    $ r13_edit(period=3,location="store")
    $ r13_flag("madam_suspicious")
    return

label r13_ev_c_seori:
    call r13_lines([("dad","검사원님, 오늘 밤 백 부인 창고에서 일합니다. 자정쯤 한 번 들러 주실 수 있겠습니까."),
        ("resident_seori","창고 일에 검사원이 왜 필요합니까? ……알겠습니다. 이유는 그때 듣지요.")],"ev:c:seori_ask")
    call r13_scene("r13_store","백 부인 창고 · 밤","night")
    call r13_lines([(None,"자루를 세는 사이 등 뒤에서 문이 닫히고 빗장이 걸렸다."),
        (None,"잠시 뒤 밖에서 목소리가 들렸다."),
        ("resident_seori","부인, 안에 사람이 있는데 빗장을 지르셨군요. 이건 기록에 남습니다."),
        ("resident_madam","……바람에 걸린 거예요."),
        ("resident_seori","바람이 빗장을 지르는 마을이면 그것도 적어 두지요.")],"ev:c:seori_caught")
    $ r13_grant(["H4"],"서리 검사원의 감금 확인")
    $ r13_edit(period=3,location="store")
    $ r13_flag("madam_exposed","madam_hostile")
    return

label r13_ev_c_mungchi:
    call r13_lines([("resident_madam","그럼 밤에 창고로 와요. 문은 열어 둘게요."),
        (None,"창고로 가는 대신 13호로 돌아와 등을 끄고 장롱 옆에 앉았다.")],"ev:c:pretend")
    call r13_scene("room","여관 2층 · 13호실 · 밤","night")
    call r13_lines([(None,"자정이 지나자 문고리가 천천히 돌았다. 작은 등불 하나가 들어와 수첩 쪽으로 곧장 갔다."),
        ("dad","뭘 찾지, 뭉치?"),
        ("resident_mungchi","으악! 저, 저는……")],"ev:c:mungchi_caught")
    call r13_lines([("resident_mungchi","부인이 13호에 편지나 쪽지가 있으면 베껴 오라고 했어요. 여관 할머니가 값을 쳐 준다고요."),
        ("resident_mungchi","부인한테는 말하지 마세요. 저 내쫓기면 갈 데 없어요.")],"ev:c:mungchi_confess")
    $ r13_grant(["H3"],"13호에서 붙잡은 뭉치의 말")
    $ r13_edit(period=3,location="room13")
    $ r13_flag("mungchi_confessed","madam_suspicious")
    return

label r13_ev_c_roof:
    call r13_lines([("resident_madam","그래요? 아쉽네.")],"ev:c:refuse_roof")
    call r13_scene("r13_store","백 부인 창고 지붕 · 밤","night")
    call r13_lines([(None,"솜이 말대로 굴뚝 옆 판자가 헐거웠다. 처마에 발을 두고 몸을 밀어 넣었다."),
        (None,"안쪽 선반에 배급표와 같은 날짜가 적힌 장부가 있었다. 빠져나간 곡식과 약초가 모두 이 창고로 들어와 있었다."),
        ("dad","(장부를 베끼고 판자를 제자리에 끼웠다. 아무도 내가 왔던 걸 모른다.)",{"thought":True})],"ev:c:roof")
    $ r13_grant(["H1"],"지붕 길로 들어간 백 부인 창고")
    $ r13_edit(period=3,location="store")
    return

# ---- N. 여니의 장물 ----

label r13_ev_yeoni_goods:
    call r13_lines([(None,"여니의 교환대 위에 낯익은 목도리와 다람이의 장갑 한 짝이 놓여 있었다."),
        ("resident_yeoni","아…… 그거요? 아침에 뭉치가 가져왔어요. 남는 물건이라고."),
        ("resident_yeoni","훔친 거라면 저도 곤란해요. 저는 바꿔 준 것뿐이에요.")],"ev:n:open")
    menu:
        "3냥에 되산다" if r13_cash_now()>=3:
            $ r13_cash(-3,"여니에게서 짐을 되삼")
            call r13_lines([("resident_yeoni","고마워요. ……뭉치 걔, 부인한테 매일 혼나요. 너무 미워하진 마세요.")],"ev:n:buy")
            $ r13_flag("ev_n_done","goods_recovered","know_mungchi_thief")
        "누가 팔았는지만 확인하고 따지지 않는다":
            call r13_lines([("resident_yeoni","뭉치예요. 백 부인 집 심부름하는. 저한테 들었다고는 하지 마세요.")],"ev:n:who")
            $ r13_flag("ev_n_done","know_mungchi_thief")
        "왕구에게 장물이라고 알린다":
            call r13_lines([("neoul","장물이요? 교환대는 오늘로 닫습니다."),
                ("resident_yeoni","……외지 분은 겨울이 끝나면 가잖아요. 저는 여기서 이걸로 먹고살아요."),
                (None,"짐은 돌아왔다. 여니는 그 뒤로 내 쪽을 보지 않았다.")],"ev:n:report")
            $ r13_flag("ev_n_done","goods_recovered","yeoni_hostile","know_mungchi_thief")
        "그냥 가져간다":
            call r13_lines([("resident_yeoni","……네. 가져가세요."),
                (None,"광장 쪽에서 누군가 혀를 차는 소리가 들렸다.")],"ev:n:take")
            $ r13_flag("ev_n_done","goods_recovered","yeoni_hostile","rumor:strongarm")
    $ r13_finish_topic("yeoni_goods")
    return None

# ---- M. 심부름꾼 콩이 ----

label r13_ev_kongi_errand:
    call r13_lines([("resident_kongi","지켜보는 거요? 하루에 두 냥. 어디요?")],"ev:m:ask")
    $ r13_kongi_pick=renpy.display_menu([(label,place) for place,label in R13_KONGI_PLACES]+[("그만둔다",None)])
    if not r13_kongi_pick:
        $ r13_forget_topic("kongi_errand")
        return None
    if r13_cash_now()<2:
        if room13["day"]==1:
            call r13_lines([("resident_kongi","첫 손님이니까 이번만 외상이에요. 대신 내일 구운 밤 하나요.")],"ev:m:free")
        else:
            call r13_lines([("resident_kongi","돈부터요. 저도 먹고살아야 해요.")],"ev:m:nocash")
            $ r13_forget_topic("kongi_errand")
            return None
    else:
        $ r13_cash(-2,"콩이에게 심부름 값")
    $ r13_town_set(kongi_watch=dict(place=r13_kongi_pick,day=room13["day"]))
    $ r13_flag("kongi_watching")
    call r13_lines([("resident_kongi","알았어요. 내일 아침에 광장으로 오세요. 본 것만 말할게요. 안 본 건 안 본 거예요.")],"ev:m:hired")
    $ r13_forget_topic("kongi_errand")
    return None

label r13_ev_kongi_report:
    $ r13_kongi_watch=r13_town().get("kongi_watch") or {}
    $ r13_kongi_lines,r13_kongi_flags=r13_kongi_report(r13_kongi_watch.get("place","kitchen"),r13_kongi_watch.get("day",room13["day"]-1),room13["flags"])
    call r13_lines(r13_kongi_lines,"ev:m:report:"+r13_kongi_watch.get("place","kitchen"))
    $ r13_flag(*r13_kongi_flags)
    python:
        _n=winter_copy.deepcopy(store.room13)
        _n["flags"]=[f for f in _n["flags"] if f not in ("kongi_watching","kongi_report_ready")]
        _n.setdefault("town",{}).pop("kongi_watch",None)
        store.room13=_n
    $ r13_forget_topic("kongi_report")
    return None
