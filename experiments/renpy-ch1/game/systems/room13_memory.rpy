# Residents remember what happened to them (owner, 0.18.14).
#   - A resident Dad harmed stays cold, even after good rumors. Lines say so; no affection numbers.
#   - The repair is tied to that incident: an apology, paying back, or confirming the facts.
#   - Rumors only move people who just heard them (price, teacher): a good rumor makes them
#     hold judgment, it does not erase the bad one (systems/room13_bundle3.rpy, room13_carryover.rpy).
init 114 python:
    # person, grudge flag, cold lines, (repair title, cost in 냥, repair lines), extra flags on repair
    R13_GRUDGES={
        "piko":dict(person="resident_piko",flag="piko_hostile",
            cold=[("resident_piko","모모 관장님께 일러 주신 분이죠. 그 바람에 그날 저녁은 굶었어요.")],
            fix=("받은 사례금을 나눠 준다",3,[("dad","그 사례금은 제가 혼자 가질 돈이 아니었습니다. 밥값으로 받아 주세요."),
                ("resident_piko","……가짜를 그린 건 제 잘못이에요. 그래도 밥값은 받을게요. 이걸로 끝내요.")])),
        "sling":dict(person="resident_sling",flag="sling_hostile",
            cold=[("resident_sling","덕분에 우체국에는 못 나가요. 그날 뒤로 일거리도 끊겼고요.")],
            fix=("사정부터 묻지 않은 일을 사과한다",0,[("dad","편지를 연 일은 그냥 넘길 수 없었습니다. 그래도 사정부터 듣지 않고 신고한 건 성급했습니다."),
                ("dad","너울 씨, 남의 편지를 열려 한 것은 잘못입니다. 그래도 슬링의 사정을 듣고 다시 일할 기회를 주실 수 없겠습니까?"),
                ("neoul","……내일부터 다시 나오라 하시오. 편지는 받는 사람이 열게 하고."),
                ("resident_sling","고마워요. 그래도 그날 너울 앞에 저를 세운 건 안 잊을 거예요.")]),extra=("neoul_annoyed",)),
        "ttadak":dict(person="resident_ttadak",flag="ttadak_hostile",
            cold=[("resident_ttadak","제 벽 일을 신고하고 받은 사례금은 잘 쓰셨어요?")],
            fix=("신고 사례금을 돌려준다",5,[("dad","그 사례금을 받을 일이 아니었습니다. 돌려드리겠습니다."),
                ("resident_ttadak","……돈으로 봉한 벽이 다시 열리지는 않아요. 그래도 손님이 그 돈을 쥐고 있지 않다는 건 알겠어요.")])),
        "yeoni":dict(person="resident_yeoni",flag="yeoni_hostile",
            cold=[("resident_yeoni","교환대 물건 가져가신 분이죠. 그 바람에 저는 그날 하루 장사를 공쳤어요.")],
            fix=("목도리와 장갑 값을 치른다",3,[("dad","물건은 우리 것이었지만, 값을 치르고 받아 오신 건 맞습니다. 그 값은 내겠습니다."),
                ("resident_yeoni","……이제 셈은 끝났네요. 다음엔 먼저 물어봐 주세요.")])),
        "nabi":dict(person="nabi",flag="nabi_hostile",
            cold=[("nabi","뒷문 일, 할머니한테 말씀하셨잖아요. 그 바람에 그 주 아이들은 밥을 못 먹었어요.")],
            fix=("빠진 품삯만큼 아이들 밥값을 낸다",4,[("dad","그때 아이들이 못 먹은 만큼은 내가 낼게."),
                ("nabi","……돈으로 될 일이 아니었어요. 그래도 이번 주 아이들은 먹겠네요.")])),
        "ppul":dict(person="resident_ppul",flag="ppul_hostile",
            cold=[("resident_ppul","재판은 증거대로 하겠다고 했소. 그 이상은 기대하지 마시오.")],
            fix=("장부로 압박한 일을 사과한다",0,[("dad","그날 장부로 촌장님을 몰아세운 건 지나쳤습니다. 사과드립니다."),
                ("resident_ppul","사과는 받겠소. 장부를 광장에 붙이지 않는다면, 나도 그날 일은 더 꺼내지 않겠소.")])),
        "nubi":dict(person="resident_nubi",flag="nubi_hostile",
            cold=[("resident_nubi","검사원께 말씀하신 뒤로 장작이 끊겼어요. 애들이 밤에 떨어요.")],
            fix=("끊긴 장작 값을 대신 낸다",4,[("dad","장작이 끊긴 건 제가 알린 탓도 있습니다. 이번 주 장작 값은 제가 내겠습니다."),
                ("resident_nubi","……고마워요. 그래도 너울 일은 저도 어쩔 수 없었다는 것만 알아 주세요.")])),
        "siluk":dict(person="resident_siluk",flag="siluk_hostile",
            cold=[],
            fix=("받은 여덟 냥을 돌려준다",8,[("dad","그때 받은 돈을 돌려주겠습니다. 받을 돈이 아니었습니다."),
                ("resident_siluk","……돌려받는다고 그날 일이 없던 게 되진 않아요. 그래도 사람들이 하는 말은 제가 바로잡을게요.")])),
        "somi":dict(person="resident_somi",flag="somi_hostile",
            cold=[],
            fix=("할아버지 약값을 보탠다",5,[("dad","할아버지 약값에 보태렴. 그날 일을 없던 걸로 해 달라는 건 아니야."),
                ("resident_somi","……약은 이걸로 사 볼게요. 그날 일은 그래도 못 잊어요.")])),
        "eunho":dict(person="resident_eunho",flag="eunho_hostile",
            cold=[("resident_eunho","광장에 쪽지가 붙은 뒤로 손님들이 저울만 쳐다보오. 값은 정해진 대로 받겠습니다. 깎아 드릴 이유는 없소.")],
            fix=None),
    }
    # How a fair-rumor listener phrases holding judgment, by grudge.
    R13_FAIR_BUT={
        "piko":"저울 일 바로잡으셨다는 말은 들었어요. ",
        "yeoni":"광장에서 좋은 말이 돈다는 건 알아요. ",
        "nabi":"아이들 일로 좋은 말 도는 건 알아요. ",
        "nubi":"좋은 일 하신다는 말은 들었어요. ",
        "ttadak":"좋은 소문은 들었소. ",
        "sling":"좋은 소문이 도는 건 알아요. ",
    }

    for _k,_g in R13_GRUDGES.items():
        if _g["cold"]:
            ROOM13["topics"]["grudge_cold:"+_k]=dict(npc=_g["person"],title="말을 걸어 본다",day=[2,14],need=[_g["flag"]],not_flags=[_k+"_reconciled"],give=[],flags=[],lines=list(_g["cold"]))
        if _g["fix"]:
            ROOM13["topics"]["grudge_fix:"+_k]=dict(npc=_g["person"],title=_g["fix"][0]+(" (%d냥)"%_g["fix"][1] if _g["fix"][1] else ""),day=[2,14],need=[_g["flag"]],not_flags=[_k+"_reconciled"],give=[],flags=[],lines=list(_g["fix"][2]))
            R13_TOPIC_LABELS["grudge_fix:"+_k]="r13_grudge_fix"
    # A report does not identify the requester. Listening and apologizing stay
    # possible before H9, so earning trust cannot depend on the secret itself.
    ROOM13["topics"]["grudge_reason:sling"]=dict(
        npc="resident_sling",title="그때 왜 편지를 열려 했습니까?",day=[2,14],
        need=["sling_hostile"],not_flags=["sling_grudge_reason_heard","sling_reconciled"],
        discover_any=["sling_hostile"],give=[],flags=[],lines=[])
    R13_TOPIC_LABELS["grudge_reason:sling"]="r13_sling_grudge_reason"
    ROOM13["topics"]["grudge_fix:sling"]["discover_any"]=["sling_hostile"]
    # Existing cold topics close once the incident is repaired.
    for _t,_k in (("somi_after_hostile","somi"),("siluk_cold","siluk")):
        ROOM13["topics"][_t]["not_flags"]=list(ROOM13["topics"][_t].get("not_flags",[]))+[_k+"_reconciled"]

    def r13_grudge_open(key):
        return r13_has(R13_GRUDGES[key]["flag"]) and not r13_has(key+"_reconciled")

    _r13_mem_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        if key.startswith("grudge_cold:"):
            k=key.split(":",1)[1];lines=list(R13_GRUDGES[k]["cold"])
            if r13_has("rumor:fair") and k in R13_FAIR_BUT:
                who,line=lines[0]
                lines[0]=(who,R13_FAIR_BUT[k]+"그래도 "+line)
            return lines
        return _r13_mem_topic_lines(key)

    # Fact check repairs 은호: once Dad shows that 백 부인 asked for the tightened scale.
    _r13_mem_present=r13_present
    def r13_present(person,key,identity=False):
        if person=="resident_eunho" and key=="H1" and r13_has("H1") and r13_grudge_open("eunho"):
            _r13_mem_present(person,key,identity)
            r13_flag("eunho_reconciled")
            return [("resident_eunho","……백 부인 글씨구려. 저 혼자 꾸민 일이 아니라는 건 알고 계셨구려."),
                ("resident_eunho","그렇다고 제가 한 일이 없어지진 않소. 그래도 이제부터 당신한테는 남들과 같은 값만 받겠습니다.")]
        return _r13_mem_present(person,key,identity)

label r13_sling_grudge_reason:
    if not r13_grudge_open("sling") or r13_has("sling_grudge_reason_heard"):
        return
    if r13_sling_knows_requester():
        call r13_lines([("dad","전에 들은 편지 일을 다시 확인하고 싶습니다."),
            ("resident_sling","할머니가 베껴 오라고 했다고 말씀드렸죠. 그 사정과 별개로, 저를 경비에게 알리신 건 잊지 못해요.")],"grudge:sling:reason:known")
    else:
        call r13_lines([("dad","그때 왜 편지를 열려 했는지, 이제라도 들을 수 있겠습니까?"),
            ("resident_sling","……편지를 베껴 오라는 부탁을 받았어요. 누구 부탁인지는 말 못 해요. 일도 끊겼는데, 그 이름까지 말할 용기는 없어요.")],"grudge:sling:reason")
    $ r13_flag("sling_job_pressure_heard","sling_grudge_reason_heard")
    $ r13_finish_topic("grudge_reason:sling")
    return

label r13_grudge_fix:
    $ _gk=r13_topic.split(":",1)[1]
    if _gk=="sling" and not r13_grudge_open("sling"):
        return
    $ _gt,_gcost,_glines=R13_GRUDGES[_gk]["fix"]
    if _gcost and r13_cash_now()<_gcost:
        call r13_lines([("dad","(지금 가진 돈으로는 모자라다. %d냥이 있어야 한다.)"%_gcost,{"thought":True})],"grudge:short:"+_gk, binding_route="dynamic:610")
        return
    if _gcost:
        $ r13_cash(-_gcost,_gt)
    call r13_lines(_glines,"grudge:fix:"+_gk, binding_route="dynamic:611")
    $ r13_flag(_gk+"_reconciled",*R13_GRUDGES[_gk].get("extra",()))
    $ r13_finish_topic(r13_topic)
    if _gk=="siluk":
        $ r13_w2e_unflag("rumor:extortion")
    return
