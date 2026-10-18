# 마을 사건 묶음 2 (docs/EVENT_CATALOG.md): 실룩의 사기, 누비의 싼 방, 비싼 상품 둘.
# 0.19.16: 숙박비 폐지에 맞춰 누비의 유인을 난방과 식사로 바꾼다.
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
            ("dad","대신 솜이가 위험한 데 다니지 않게만 살펴 주십시오."),
            ("resident_musoe","……그 애 일은 내가 알아서 하오. 이건 폐광 지도요. 빚은 이걸로 먼저 갚겠소.")]),
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
        """숙박비가 없으므로 방을 바꿔도 차액을 지급하지 않는다."""
        return

    # A deposit is not a missed deadline. These queries never write save state.
    # No overrides: runtime dependencies are wallet(init 91), town(init 102),
    # abs_time(init 56), and the final r13_people chain, all called after init.
    import collections.abc as r13_siluk_abc

    def r13_siluk_advance_record(state=None):
        s=store.room13 if state is None else state
        saved=s.get("town",{}).get("siluk_advance")
        if isinstance(saved,r13_siluk_abc.Mapping):
            return winter_copy.deepcopy(saved)
        # Legacy ledger dates are save-local, but the same -5 text was used for
        # both paid and follow. Never infer their different promises from it.
        names=("실룩에게 선금","실룩에게 선금(가진 돈 전부)")
        rows=[r for r in r13_wallet(s)["ledger"] if isinstance(r,r13_siluk_abc.Mapping) and r.get("text") in names]
        if not rows and "siluk_scammed" not in s.get("flags",[]):return None
        record=dict(version=1,branch="legacy_unknown",status="unknown_time",payment_day=None,
            payment_period=None,due_day=None,due_kind=None,due_abs=None,amount=None,
            overdue_seen=False,next_day_seen=False,witness_seen=True,unknown_seen=False)
        if len(rows)!=1:return record
        row=rows[0];day=row.get("day");amount=row.get("amount")
        if not isinstance(day,int) or isinstance(day,bool) or not 1<=day<=s.get("day",0):return record
        if not isinstance(amount,int) or isinstance(amount,bool) or amount>=0:return record
        record.update(payment_day=day,amount=-amount)
        if row["text"]==names[1] and 0<-amount<5:
            record.update(branch="legacy_paid_all",status="pending",due_day=day,due_kind="end_of_day",due_abs=day*4)
        return record

    def r13_siluk_pay_advance(branch):
        if branch not in ("paid","paid_all","follow"):return False
        s=store.room13
        # An existing deposit, including an uncertain legacy one, cannot be paid twice.
        if r13_siluk_advance_record(s) is not None:return False
        wallet=r13_wallet(s);cash=wallet["cash"]
        if branch=="paid_all":
            if not 0<cash<5:return False
            amount=cash
        else:
            if cash<5:return False
            amount=5
        day,period=s["day"],s["period"]
        due_kind="sunset" if branch=="paid" else "end_of_day"
        due_abs=(day-1)*4+2 if due_kind=="sunset" else day*4
        # Money, its ledger row, and the promise are committed in one save-local
        # assignment. There is no say/checkpoint between deduction and record.
        n=winter_copy.deepcopy(s)
        wallet["cash"]-=amount
        wallet["ledger"].append(dict(day=day,text="실룩에게 선금(가진 돈 전부)" if branch=="paid_all" else "실룩에게 선금",amount=-amount))
        n["livelihood"]=wallet
        n.setdefault("town",{})["siluk_advance"]=dict(version=1,branch=branch,amount=amount,
            payment_day=day,payment_period=period,due_day=day,due_kind=due_kind,due_abs=due_abs,
            status="pending",overdue_seen=False,next_day_seen=False,witness_seen=False,unknown_seen=False)
        if "siluk_advance_paid" not in n["flags"]:n["flags"].append("siluk_advance_paid")
        store.room13=n
        return True

    def r13_siluk_advance_notice():
        record=r13_siluk_advance_record()
        if not record or record.get("status") in ("fulfilled","resolved"):return None
        day=record.get("payment_day");due=record.get("due_abs")
        valid=(isinstance(day,int) and not isinstance(day,bool) and 1<=day<=store.room13["day"]
            and isinstance(due,int) and not isinstance(due,bool) and record.get("due_day")==day
            and record.get("due_kind") in ("sunset","end_of_day")
            and due==((day-1)*4+2 if record["due_kind"]=="sunset" else day*4))
        if record.get("status")=="unknown_time" or not valid:
            return None if record.get("unknown_seen") else "unknown"
        if r13_abs_time()<due:return None
        if not record.get("overdue_seen"):
            return "sunset" if store.room13["day"]==day else "late"
        if store.room13["day"]>day and not record.get("next_day_seen"):return "next_day"
        return None

    def r13_siluk_commit_notice(kind):
        if kind not in ("unknown","sunset","late","next_day") or kind!=r13_siluk_advance_notice():return False
        record=r13_siluk_advance_record()
        if not record:return False
        if kind=="unknown":record["unknown_seen"]=True
        else:
            record.update(status="confronted" if record.get("status")=="confronted" else "overdue",overdue_seen=True)
            if store.room13["day"]>record["payment_day"]:record["next_day_seen"]=True
        n=winter_copy.deepcopy(store.room13);n.setdefault("town",{})["siluk_advance"]=record
        if kind!="unknown" and "siluk_scammed" not in n["flags"]:n["flags"].append("siluk_scammed")
        store.room13=n
        return True

    def r13_siluk_witness_ready():
        record=r13_siluk_advance_record()
        return bool(record and record.get("branch")=="paid" and record.get("status") not in ("fulfilled","resolved")
            and not record.get("witness_seen") and r13_siluk_advance_phase()=="overdue"
            and store.room13["day"]>record["payment_day"] and "resident_kongi" in r13_people())

    def r13_siluk_commit_witness():
        if not r13_siluk_witness_ready():return False
        record=r13_siluk_advance_record();record["witness_seen"]=True
        r13_town_set(siluk_advance=record)
        return True

    # The live follow-up deliberately does not finish/archive the topic: the
    # deposit remains discussable; requests alone never count as resolution.
    ROOM13["topics"]["siluk_advance_followup"]=_ev2_topic("resident_siluk","맡긴 짐과 선금을 묻는다",(1,14),need=["siluk_advance_paid"])
    R13_TOPIC_LABELS["siluk_advance_followup"]="r13_siluk_advance_followup"

    def r13_siluk_sync_advance():
        record=r13_siluk_advance_record()
        if not record:return
        n=winter_copy.deepcopy(store.room13)
        n.setdefault("town",{}).setdefault("siluk_advance",record)
        if "siluk_advance_paid" not in n["flags"]:n["flags"].append("siluk_advance_paid")
        if n!=store.room13:store.room13=n

    def r13_siluk_advance_phase():
        record=r13_siluk_advance_record()
        if not record:return None
        if record.get("status") in ("fulfilled","resolved"):return "resolved"
        day=record.get("payment_day");due=record.get("due_abs")
        valid=(isinstance(day,int) and not isinstance(day,bool) and 1<=day<=store.room13["day"]
            and isinstance(due,int) and not isinstance(due,bool) and record.get("due_day")==day
            and record.get("due_kind") in ("sunset","end_of_day")
            and due==((day-1)*4+2 if record["due_kind"]=="sunset" else day*4))
        if not valid:return "unknown"
        return "overdue" if r13_abs_time()>=due else "pending"

    def r13_siluk_record_request(kind):
        record=r13_siluk_advance_record()
        if not record or record.get("status") in ("fulfilled","resolved"):return False
        if kind not in ("progress","explain","refund","deliver"):return False
        phase=r13_siluk_advance_phase()
        if kind in ("explain","refund","deliver") and phase!="overdue":return False
        record["last_request"]=kind
        record["contact_day"]=store.room13["day"];record["contact_period"]=store.room13["period"]
        if phase=="overdue":record["status"]="confronted"
        r13_town_set(siluk_advance=record)
        return True


label r13_town_events2:
    call r13_siluk_advance_events
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
    $ r13_note_encounter("resident_siluk")
    call r13_ev_here("calm")
    call r13_lines([(None,"광장 우물가에서 짐꾼 실룩이 먼저 다가왔다. 잠을 못 잤는지 눈 밑이 거뭇했다."),
        ("resident_siluk","외곽 초소에서 되돌아온 짐 기다리시죠? 정식 길로 가면 이틀 걸려요. 저는 남들 모르는 지름길을 알아요."),
        ("resident_siluk","그 짐, 오늘 안에 받아다 드리죠. 선금 다섯 냥만 주세요.")],"ev:a:offer")
    $ _ep_loop=True
    while _ep_loop:
        $ _ep_loop=False
        menu:
            "선금 다섯 냥을 준다" if r13_cash_now()>=5:
                $ _siluk_paid=r13_siluk_pay_advance("paid")
                if _siluk_paid:
                    call r13_lines([("resident_siluk","해 지기 전에 짐 가지고 올게요. 걱정 마세요."),
                        (None,"실룩은 선금을 챙겨 자리를 떠났다.")],"ev:a:paid")
            "가진 돈을 모두 준다" if 0<r13_cash_now()<5:
                $ _siluk_paid=r13_siluk_pay_advance("paid_all")
                if _siluk_paid:
                    call r13_lines([("resident_siluk","……이것뿐이에요? 뭐, 일단 받죠."),
                        (None,"실룩은 내가 건넨 돈을 챙겨 자리를 떠났다.")],"ev:a:paid_all")
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
                $ _siluk_paid=r13_siluk_pay_advance("follow")
                if _siluk_paid:
                    call r13_lines([(None,"실룩은 초소 쪽이 아니라 백 부인 집 뒷골목으로 갔다. 뭉치가 문을 열고 나와 동전을 받아 갔다."),
                        ("resident_mungchi","이번 주 이자는 받았어요. 부인이 다음 주엔 원금도 받겠대요."),
                        ("dad","(내가 준 돈은 결국 백 부인 금고로 갔다. 실룩은 심부름꾼일 뿐이다.)",{"thought":True})],"ev:a:follow")
                    $ r13_flag("know_siluk_debt","know_madam_hoard")
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

# Actual clock boundaries, not future narration inside the payment packet.
label r13_siluk_advance_events:
    $ r13_siluk_sync_advance()
    $ _siluk_notice=r13_siluk_advance_notice()
    if _siluk_notice:
        call r13_ev_here("calm")
        if _siluk_notice=="sunset":
            call r13_lines([(None,"해가 졌지만, 실룩이 가져오기로 한 짐은 아직 받지 못했다.")],"ev:a:overdue:sunset")
        elif _siluk_notice=="late":
            call r13_lines([(None,"실룩이 짐을 가져오겠다고 약속한 날이 지났다. 아직 짐은 받지 못했다.")],"ev:a:overdue:late")
        elif _siluk_notice=="next_day":
            call r13_lines([(None,"날이 바뀌어도 실룩에게 부탁한 짐은 오지 않았다.")],"ev:a:overdue:next_day")
        else:
            call r13_lines([("dad","(실룩에게 선금을 준 일은 기억난다. 부탁한 짐부터 확인해야겠다.)",{"thought":True})],"ev:a:advance:unknown")
        $ r13_siluk_commit_notice(_siluk_notice)
    if r13_siluk_witness_ready():
        call r13_ev_here("calm")
        if room13["day"]==r13_siluk_advance_record()["payment_day"]+1:
            call r13_lines([("dad","콩이야, 실룩 아저씨 봤니? 맡긴 짐을 아직 못 받아서 찾고 있어."),
                ("resident_kongi","어제 백 부인네 뒷문으로 들어가는 걸 봤어요."),
                ("dad","안에서 뭘 했는지도 봤니?"),
                ("resident_kongi","아뇨. 들어가는 것만 봤어요."),
                ("dad","그랬구나. 고마워.")],"ev:a:witness:next_day")
        else:
            call r13_lines([("dad","콩이야, 실룩 아저씨 봤니? 맡긴 짐을 아직 못 받아서 찾고 있어."),
                ("resident_kongi","며칠 전에 백 부인네 뒷문으로 들어가는 걸 봤어요."),
                ("dad","안에서 뭘 했는지도 봤니?"),
                ("resident_kongi","아뇨. 들어가는 것만 봤어요."),
                ("dad","그랬구나. 고마워.")],"ev:a:witness:later")
        $ r13_siluk_commit_witness()
    return

label r13_siluk_advance_followup:
    $ r13_siluk_sync_advance()
    $ _siluk_phase=r13_siluk_advance_phase()
    if not _siluk_phase:
        return
    if _siluk_phase=="resolved":
        call r13_lines([(None,"이 선금 건은 이미 정리했다. 새로 돈을 건네지는 않았다.")],"ev:a:followup:resolved")
        return
    menu:
        "맡긴 짐은 어디까지 확인하셨습니까?" if _siluk_phase in ("pending","unknown"):
            call r13_lines([("dad","선금 드리고 부탁한 짐 말입니다. 어디까지 확인하셨습니까?"),
                ("resident_siluk","……아직 가져오지는 못했어요.")],"ev:a:followup:progress")
            $ r13_siluk_record_request("progress")
        "약속한 때가 지났습니다. 어떻게 된 겁니까?" if _siluk_phase=="overdue":
            call r13_lines([("dad","짐을 가져오기로 한 때가 지났습니다. 어떻게 된 겁니까?"),
                ("resident_siluk","……받은 돈을 백 부인 빚 갚는 데 썼어요. 짐은 아직 못 가져왔어요.")],"ev:a:followup:explain")
            $ r13_flag("know_siluk_debt")
            $ r13_siluk_record_request("explain")
        "짐을 못 가져오셨으면 선금을 돌려주세요." if _siluk_phase=="overdue":
            call r13_lines([("dad","짐을 못 가져오셨으면 선금을 돌려주세요."),
                ("resident_siluk","……받은 돈을 백 부인 빚 갚는 데 썼어요. 지금은 돌려드릴 돈이 없어요."),
                ("dad","그럼 돌려받을 돈으로 남겨 두겠습니다.")],"ev:a:followup:refund")
            $ r13_flag("know_siluk_debt")
            $ r13_siluk_record_request("refund")
        "선금은 이미 드렸습니다. 부탁한 짐부터 가져와 주세요." if _siluk_phase=="overdue":
            call r13_lines([("dad","선금은 이미 드렸습니다. 부탁한 짐부터 가져와 주세요."),
                ("resident_siluk","……알겠습니다. 아직 가져오지 못했어요.")],"ev:a:followup:deliver")
            $ r13_siluk_record_request("deliver")
        "지금은 돌아간다":
            pass
    return


# ---- Q. 누비의 싼 방 ----

label r13_ev_q_nubi:
    $ r13_flag("ev_q_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"누비 아주머니가 빨래 바구니를 내려놓고 내 소매를 잡았다."),
        ("resident_nubi","여관방 춥지 않으세요? 우리 집 별채는 불을 넉넉히 때요. 따뜻한 밥도 드리고요."),
        ("dad","(다람이가 따뜻하게 잘 수 있다면…….)",{"thought":True}),
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
            "낯선 사람에게 왜 방을 내주는지 묻는다":
                call r13_lines([("resident_nubi","빈방을 놀리느니 사람이 있는 게 좋죠."),
                    ("dad","방에 식사까지 내주시는데, 저희에게 바라는 건 없습니까?"),
                    ("resident_nubi","……너울이 외지 사람을 데려오면 장작을 줘요. 열병 검사한다고 하루 가둬 두는 것뿐이에요."),
                    ("resident_nubi","우리 집 난로가 꺼지면 애들이 이 겨울을 못 버텨요. 미안해요.")],"ev:q:ask")
                $ r13_flag("know_neoul_quarantine")
                menu:
                    "비밀로 해 주고, 다시는 하지 말라고 한다":
                        call r13_lines([("resident_nubi","……고마워요. 별채는 그냥 쓰셔도 돼요. 이번엔 문도 잠그지 않을게요.")],"ev:q:keep_secret")
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
                    ("neoul","……검사원 도장이 찍혀 있구려. 그럼 됐소."),
                    ("resident_nubi","그 신고, 너울이 시킨 거였어요. 미안해요. 방은 그냥 쓰세요. 문도 잠그지 않을게요.")],"ev:q:certificate")
                $ r13_flag("lodging_cheap","nubi_ally","know_neoul_quarantine","seori_met")
    return None

label r13_medkit_give:
    call r13_lines(ROOM13["topics"][r13_topic]["lines"],"medkit:"+r13_topic, binding_route="dynamic:739")
    $ _mk_flags,_mk_give,_mk_source=R13_MEDKIT_RESULTS[r13_topic]
    $ r13_flag(*_mk_flags)
    if _mk_give:
        $ r13_grant(_mk_give,_mk_source)
    $ r13_use_item("medkit")
    $ r13_finish_topic(r13_topic)
    return None
