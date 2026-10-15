# 2주차 사건 4개 (docs/EVENT_CATALOG.md K·P·V·W, 0.18.10): 14일 제단의 논쟁(F1~F4)과 준비에 걸린다.
#   K 종을 울리지 마라 (9~11일 광장)  — 종으로 사람이 모이면 비어 있던 교대·운반 약속이 채워진다.
#   P 계측 조작 (9~12일 수리점)        — 가짜 숫자에 동의하면 돌 측정(F2 근거)이 막힌다. W4·W6로 조작을 밝힐 수 있다.
#   V 비축 나눔 (10~12일 창고)         — 식량을 나누는 순서. 결말 기록과 소문에 남는다.
#   W 부리의 도구 (9~12일 수리점)      — 도구가 팔리면 장치 교대가 막힌다. 톡이 풀려났으면 톡의 공구로 대신한다.
# 시간은 쓰지 않는다(일·잠만). 직접 종을 치면 그날 남은 시간을 초소에서 보낸다(사건의 대가).
init 109 python:
    R13_BAD_RUMORS=tuple(R13_BAD_RUMORS)+("rumor:favoritism","rumor:profiteer")
    R13_RUMOR_WHISPERS.update({
        "rumor:favoritism":"그 외지 사람, 식량을 자기 편부터 나눠 줬대.",
        "rumor:profiteer":"대피소 식량을 경매에 붙였대. 돈 있는 집만 먹었대.",
    })

    # P: forged numbers block the honest measurements until exposed.
    for _k in ("w2_measure1","w2_measure2"):
        ROOM13["activities"][_k]["not_flags"]=list(ROOM13["activities"][_k].get("not_flags",[]))+["numbers_forged"]
    # W: without the tools nobody can hold the device overnight, unless Tok lends his.
    ROOM13["activities"]["w2_operators"]["not_flags"]=list(ROOM13["activities"]["w2_operators"].get("not_flags",[]))+["tools_missing"]
    ROOM13["topics"].update({
        "w2_expose_numbers":_ep_topic("resident_seori","촌장의 숫자를 지난주 기록과 맞춘다",(9,13),need=["numbers_forged"],not_flags=["forgery_exposed"]),
        "w2_buy_tools":_ep_topic("resident_eunho","부리의 도구를 되산다",(9,13),need=["tools_sold"],not_flags=["tools_back"]),
    })
    R13_TOPIC_LABELS.update({"w2_expose_numbers":"r13_w2e_expose","w2_buy_tools":"r13_w2e_buy_tools"})

    def r13_w2e_unflag(*keys):
        r13_edit(flags=[f for f in store.room13["flags"] if f not in keys])

    R13_W2E_NOTES=[
        ("w2_bell_rung","종이 울려 사람들이 해 지기 전에 학교로 모였다."),
        ("w2_bell_silent","종은 끝내 울리지 않았다. 학교로 늦게 온 집이 있었다."),
        ("forgery_exposed","촌장이 요구한 가짜 숫자는 지난주 기록 앞에서 무너졌다."),
        ("numbers_forged","마을 기록에는 '돌은 괜찮다'는 숫자가 남았다."),
        ("share_patients","식량은 아픈 사람이 있는 집부터 나눴다."),
        ("share_children","식량은 표 없는 아이들부터 나눴다."),
        ("share_lottery","식량은 제비를 뽑아 나눴다. 누구도 먼저가 아니었다."),
        ("share_supporters","식량은 우리 편을 든 집부터 나눴다."),
        ("share_auction","대피소 식량 일부가 경매로 팔렸다."),
        ("tools_kept","부리는 할아버지 도구를 지켰다."),
        ("tools_sold","부리의 할아버지 도구는 도시로 팔려 갔다."),
    ]
    _r13_w2e_notes=r13_ending_notes
    def r13_ending_notes():
        return _r13_w2e_notes()+[text for key,text in R13_W2E_NOTES if r13_has(key)]

label r13_w2e_events:
    if room13["day"]<8 or not room13.get("week2_started"):
        return None
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    if 9<=_d<=11 and _p<=2 and _loc=="square" and not r13_has("w2e_k_done"):
        $ r13_offer("r13_w2e_bell")
    if 9<=_d<=12 and _p<=1 and _loc=="workshop" and not r13_has("w2e_p_done"):
        $ r13_offer("r13_w2e_numbers")
    elif 9<=_d<=12 and _p<=1 and _loc=="workshop" and not r13_has("w2e_w_done"):
        $ r13_offer("r13_w2e_tools")
    if 10<=_d<=12 and _loc=="store" and not r13_has("w2e_v_done") and (r13_has("supplies_ready") or r13_has("supply_terms")):
        call r13_w2e_share
    return None

# ---- K. 종을 울리지 마라 ----
label r13_w2e_bell:
    $ r13_flag("w2e_k_done")
    call r13_ev_here("search")
    call r13_lines([(None,"광장 종탑 아래에서 설이가 종 줄을 붙잡고 서 있었다. 너울이 그 앞을 막았다."),
        ("neoul","종을 치면 사람들이 한꺼번에 몰려나오오. 그러면 길에서 넘어지고, 다툼이 나오."),
        ("resident_seol","그럼 불 꺼진 집 사람들은 어떻게 알아요? 오늘 밤에 또 두 집이 꺼져요!"),
        ("neoul","종을 마음대로 치면 초소에서 경위를 설명해야 하오.")],"w2e:bell:open:v2")
    menu:
        "설이에게 종을 치라고 한다" if r13_has("village_alerted") or r13_has("lamplighter_trust"):
            call r13_lines([("resident_seol","지난번에도 아저씨가 그러라고 했죠. 그럼 칠게요."),
                (None,"종소리가 불 꺼진 지붕들 위로 퍼졌다. 문이 하나씩 열렸다."),
                ("neoul","……사람들 줄은 내가 세우겠소. 밀지 마시오!")],"w2e:bell:ring")
            $ r13_flag("w2_bell_rung","villagers_gathered")
        "촌장에게 종을 맡겨 달라고 한다" if r13_has("fair_hearing") or r13_has("ppul_ally"):
            call r13_lines([("resident_ppul","내가 치겠소. 촌장이 친 종이면 다툼은 덜 나겠지."),
                (None,"촌장이 친 종소리에 사람들이 줄을 맞춰 학교 쪽으로 걸었다.")],"w2e:bell:ppul")
            $ r13_flag("w2_bell_rung","villagers_gathered","ppul_ally")
        "내가 직접 종을 친다 · 늦은 저녁까지":
            call r13_lines([(None,"종 줄을 당기자 무거운 종소리가 울렸다. 곧바로 너울이 내 팔을 붙잡았다."),
                ("neoul","또 당신이오? 소란을 피운 값으로 오늘은 초소에서 지내시오."),
                (None,"초소 창 너머로 사람들이 학교로 걸어가는 게 보였다. 나는 날이 저물 때까지 초소에서 나가지 못했다.")],"w2e:bell:self")
            $ r13_flag("w2_bell_rung","villagers_gathered","rumor:troublemaker")
            $ r13_edit(period=3)
        "너울 말대로 기다리자고 한다":
            call r13_lines([("resident_seol","……알겠어요. 아저씨까지 기다리자고 하면 어쩔 수 없죠."),
                (None,"그날 밤 불이 꺼진 두 집 사람들은 아침이 되어서야 학교에 왔다.")],"w2e:bell:wait")
            $ r13_flag("w2_bell_silent")
    if r13_has("villagers_gathered"):
        $ _gain=[f for f in ("operators_terms","transport_terms") if not r13_has(f)]
        if _gain:
            call r13_lines([("resident_bori" if "transport_terms" in _gain else "buri","종소리 듣고 왔어요. 비어 있는 일 있으면 말해요. 수레든 교대든.")],"w2e:bell:volunteers")
            $ r13_flag(*_gain)
    return

# ---- P. 계측 조작 ----
label r13_w2e_numbers:
    $ r13_flag("w2e_p_done")
    call r13_ev_here("search")
    call r13_lines([(None,"수리점 작업대 위에 우박의 계측 장부가 펼쳐져 있었다. 촌장이 손가락으로 장부의 한 줄을 눌렀다."),
        ("resident_ppul","이 숫자를 고치거라. 돌은 아직 괜찮다. 사람들이 겁먹으면 겨울을 못 넘긴다."),
        ("resident_ubak","……지금 숫자를 고치면 다음에 잴 때도 고친 숫자에 맞춰 적어야 해요.")],"w2e:numbers:open")
    menu:
        "지난주 기록을 촌장에게 보여 준다" if "W4" in room13["evidence"] or "W6" in room13["evidence"]:
            call r13_lines([("dad","지난주에도 돌은 식고 있었습니다. 우박의 숫자와 초롱이 센 등이 같은 말을 합니다."),
                ("resident_ppul","……이번 숫자를 고치면 지난주 기록까지 고쳐야겠군."),
                ("resident_ppul","됐소. 숫자는 그대로 두시오. 대신 사람들 앞에선 나와 같이 설명하시오.")],"w2e:numbers:records")
            $ r13_flag("forgery_exposed","ppul_ally")
        "진짜 숫자를 서리에게 맡기게 한다":
            call r13_lines([("resident_ubak","원본 숫자는 서리 검사원님한테 맡길게요. 고친 숫자는 촌장님 장부에만 적고요."),
                ("resident_ppul","……장부를 두 개 만들겠다는 거요? 마음대로 하시오.")],"w2e:numbers:seori")
            $ r13_flag("true_numbers_kept")
        "가짜 숫자에 동의한다":
            call r13_lines([("resident_ubak","……알겠어요. 그럼 다음 측정은 못 해요. 가짜 숫자에 맞출 기준이 없으니까요."),
                ("resident_ppul","잘 생각했소.")],"w2e:numbers:forge")
            $ r13_flag("numbers_forged","ppul_ally")
        "끼어들지 않는다":
            call r13_lines([(None,"우박이 마지못해 펜을 들었다. 장부에서 숫자 하나가 지워졌다.")],"w2e:numbers:ignore")
            $ r13_flag("numbers_forged")
    return

label r13_w2e_expose:
    if "W4" in room13["evidence"] or "W6" in room13["evidence"]:
        call r13_lines([("dad","지난주 기록입니다. 우박이 잰 출력과 초롱이 센 등입니다. 촌장 장부의 숫자와 맞지 않습니다."),
            ("resident_seori","원본이 남아 있다면 고친 장부는 공식 기록으로 쓰지 않겠습니다. 측정은 다시 할 수 있어요.")],"w2e:expose:yes")
        $ r13_w2e_unflag("numbers_forged")
        $ r13_flag("forgery_exposed")
    else:
        call r13_lines([("resident_seori","장부를 고쳤다는 말만으로는 안 됩니다. 고치기 전 원래 숫자가 어딘가 남아 있어야 해요."),
            ("dad","(지난주에 돌이나 등의 숫자를 따로 남겨 뒀다면 달랐을 것이다.)",{"thought":True})],"w2e:expose:no")
    return "roam"

# ---- W. 부리의 도구 ----
label r13_w2e_tools:
    $ r13_flag("w2e_w_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"부리가 할아버지 공구함을 작업대에 올려놓았다. 그리고 한참 내려다보았다. 은호 사장은 자루를 들고 기다렸다."),
        ("resident_eunho","도시 수집가들이 옛 공구를 좋아합니다. 이 함이면 식구들이 열흘은 먹지요."),
        ("buri","은호 사장이 이걸 사겠대요."),
        ("dad","수리할 때 쓰던 공구 아니었습니까?"),
        ("buri","맞아요. 그런데 집에 먹을 게 없어요.")],"w2e:tools:open:v2")
    # 0.18.17: choices are what Dad says; the reaction carries the meaning.
    menu:
        "“제가 값을 내겠습니다.” 12냥" if r13_cash_now()>=12:
            $ r13_cash(-12,"부리의 공구함")
            call r13_lines([("dad","이 돈은 제가 내겠습니다."),
                ("buri","빌린 걸로 적어 주세요. 그냥 받은 걸로는 못 하겠어요."),
                ("buri","장치 교대할 때 이 공구를 쓸게요.")],"w2e:tools:buy:v2")
            $ r13_flag("tools_kept","buri_tools_paid")
        "“가족 몫을 공동 장부에 올리죠.”" if r13_has("supply_terms") or r13_has("supplies_ready"):
            call r13_lines([("dad","가족이 받을 몫을 장부에 넣겠습니다. 공구는 남겨 둡시다."),
                ("buri","정말 받을 수 있으면, 팔 필요는 없어요.")],"w2e:tools:share:v2")
            $ r13_flag("tools_kept","buri_family_share")
        "“할아버지가 쓰시던 물건이잖아요.”":
            call r13_lines([("buri","저도 알아요."),
                ("buri","그래서 어제도 못 팔았어요. 오늘은 뭘 먹죠?"),
                (None,"결국 공구함은 은호의 자루 옆에 놓였다.")],"w2e:tools:talk:v2")
            $ r13_flag("tools_sold")
        "“제가 결정할 일은 아니겠지요.”":
            $ r13_flag("tools_sold")
    if r13_has("tools_sold"):
        if r13_has("tok_cleared"):
            call r13_lines([("resident_tok","공구함 없이 장치 교대를 어떻게 하오. 내 공구를 쓰시오. 누명 벗겨 준 값이오.")],"w2e:tools:tok")
        else:
            $ r13_flag("tools_missing")
            call r13_lines([("dad","(장치를 밤새 붙잡고 있을 공구가 사라졌다. 이래서는 교대를 짤 수 없다.)",{"thought":True})],"w2e:tools:missing")
    return

label r13_w2e_buy_tools:
    call r13_lines([("resident_eunho","도시로 보낼 짐은 아직 안 떠났소. 공구함을 되사려면 열여덟 냥이오.")],"w2e:buy:open")
    menu:
        "열여덟 냥에 되산다" if r13_cash_now()>=18:
            $ r13_cash(-18,"부리의 공구함 되사기")
            call r13_lines([("buri","……할아버지 공구가 돌아왔네요. 이번엔 안 팔아요.")],"w2e:buy:paid")
            $ r13_w2e_unflag("tools_missing","tools_sold")
            $ r13_flag("tools_back","tools_kept")
        "다음에 산다":
            pass
    return

# ---- V. 비축 나눔 ----
label r13_w2e_share:
    $ r13_flag("w2e_v_done")
    call r13_ev_here("search")
    call r13_lines([(None,"창고 앞에 줄이 섰다. 은호와 백 부인이 장부를 사이에 두고 나를 보았다."),
        ("resident_eunho","오늘 몫이 다 돌아가지는 않습니다. 누구부터 줄지 정해 주시오. 당신이 받아 온 몫이니까."),
        ("resident_madam","남은 몫은 경매에 붙이면 값을 더 받을 수 있어요. 그럼 다음 몫을 살 돈이 생기죠.")],"w2e:share:open")
    menu:
        "아픈 사람이 있는 집부터":
            call r13_lines([("resident_seori","진료실 환자 명단을 드리지요. 열이 있는 집이 넷입니다.")],"w2e:share:patients")
            $ r13_flag("share_patients","recovery_support")
        "표 없는 아이들부터" if r13_has("kids_fed") or "W2" in room13["evidence"]:
            call r13_lines([("nabi","……배급 줄 맨 앞에 아이들이 선 건 처음이에요.")],"w2e:share:children")
            $ r13_flag("share_children","teacher_trust")
        "제비를 뽑는다":
            call r13_lines([(None,"사람들이 하나씩 제비 쪽지를 뽑았다. 불평은 있었지만 다툼은 없었다.")],"w2e:share:lottery")
            $ r13_flag("share_lottery","rumor:fair")
        "우리 편을 든 집부터":
            call r13_lines([("resident_ppul","……그것도 방법이지. 다음엔 다들 당신 편을 들겠군.")],"w2e:share:supporters")
            $ r13_flag("share_supporters","ppul_ally","rumor:favoritism")
        "남은 몫을 경매에 붙인다":
            $ r13_cash(10,"대피소 몫 경매")
            call r13_lines([("resident_madam","거봐요. 경매로 열 냥이 생겼잖아요."),
                (None,"줄 끝에 서 있던 사람들이 빈손으로 돌아갔다.")],"w2e:share:auction")
            $ r13_flag("share_auction","rumor:profiteer")
    return
