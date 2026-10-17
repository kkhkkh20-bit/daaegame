# 1주차 → 2주차 이어 주기 (소유자 지시, 0.18.9)
# 2주차 준비(쉴 곳·식량과 장작·밤에 지킬 사람·환자 운반)와 F1·F2 근거가 1주차에 한 일에 따라 달라진다.
#   도움이 된 일 → 그 준비의 약속이 2주차 첫 이동 때 바로 생긴다(대사로 이유를 말한다).
#   해가 된 일   → 그 주민이 거절한다. 돈이나 다른 사람을 거치는 우회로가 열린다.
# 정산은 2주차 첫 이동에서 한 번만 한다(`w1_links_done`). 모두 이번 회차 깃발이다.
init 108 python:
    def r13_bad_rumors():
        # A good rumor no longer erases bad ones (0.18.14); listeners hold judgment instead.
        return [r for r in R13_BAD_RUMORS if r13_has(r)]

    # (조건, 얻는 깃발, 대사) — 위에서부터 차례로 확인한다.
    R13_CARRY_GOOD=[
        (lambda:r13_has("bori_ally") or r13_has("bori_cleared"),["transport_terms"],
            [("resident_bori","수레는 제가 끌게요. 배급대 앞에서 아무도 안 나설 때 혼자 나서 주셨잖아요.")]),
        (lambda:r13_has("madam_exposed") or r13_has("scale_public") or "H6" in store.room13["evidence"],["supply_terms"],
            [("resident_seori","백 부인 창고와 배급 저울 기록은 이미 공개됐습니다. 그러니 식량과 장작은 공동 장부에 적고 바로 나눌 수 있습니다.")]),
        (lambda:r13_has("teacher_trust") or r13_has("kids_fed"),["shelter_agreed"],
            [("resident_teacher","교실은 지난주에 비워 뒀어요. 표 없는 아이들 밥을 챙기던 그때부터요.")]),
        (lambda:r13_has("tok_cleared") or r13_has("witness:tok"),["operators_terms"],
            [("resident_tok","장치 교대는 저랑 우박이 맡을게요. 누명 벗겨 주신 값이에요.")]),
        (lambda:r13_has("musoe_recovering"),["clinic_observation"],
            [("resident_seori","무쇠 할아버지가 약을 드신 뒤 기침이 멎고 사람을 다시 알아보셨습니다. 증상에서 돌아오는 사람이 있다는 기록입니다.")]),
        (lambda:r13_has("know_stone_failing") and ("W4" in store.room13["evidence"] or "W6" in store.room13["evidence"]),["measurement_plan"],
            [("resident_lamplighter","지난주에 센 식은 등 수랑 우박이 잰 숫자가 있으니까, 지금 다시 재 보면 비교할 수 있어요. 낮에 한 번, 저녁에 한 번요.")]),
    ]

    # Refusals: the normal week-2 topic closes; an alternative topic opens.
    ROOM13["topics"]["w2_bori"]["not_flags"]=list(ROOM13["topics"]["w2_bori"].get("not_flags",[]))+["bori_refuses","transport_terms"]
    ROOM13["topics"]["w2_eunho"]["not_flags"]=list(ROOM13["topics"]["w2_eunho"].get("not_flags",[]))+["eunho_refuses","supply_terms"]
    ROOM13["topics"]["w2_school"]["not_flags"]=list(ROOM13["topics"]["w2_school"].get("not_flags",[]))+["teacher_doubts","shelter_agreed"]
    ROOM13["topics"].update({
        "w2_sled":_ep_topic("karo","마차 썰매를 빌린다",(8,13),need=["bori_refuses"],not_flags=["transport_terms"]),
        "w2_madam_stock":_ep_topic("resident_madam","비축을 내놓으라고 한다",(8,13),need=["eunho_refuses","H1"],not_flags=["supply_terms"],flags=["supply_terms"],lines=[
            ("dad","창고 장부는 이미 제 손에 있습니다. 은호 사장이 내놓지 않은 몫은 부인 창고에서 대신 내놓으십시오."),
            ("resident_madam","……장부를 광장에 붙이지 않는다면요. 이름 적고 가져가요.")]),
        "w2_eunho_full":_ep_topic("resident_eunho","제값을 치르고 산다",(8,13),need=["eunho_refuses"],not_flags=["supply_terms"]),
        "w2_school_vouch":_ep_topic("resident_teacher","보증해 줄 사람을 데려온다",(8,13),need=["teacher_doubts"],not_flags=["shelter_agreed"]),
    })
    R13_TOPIC_LABELS.update({"w2_sled":"r13_carry_sled","w2_eunho_full":"r13_carry_eunho_full","w2_school_vouch":"r13_carry_vouch"})

    def r13_carry_vouchers():
        names=[]
        if r13_has("lamplighter_trust"):names.append("resident_lamplighter")
        if r13_has("badook_ally"):names.append("resident_badook")
        if r13_has("ppul_ally"):names.append("resident_ppul")
        if r13_has("witness:nabi"):names.append("nabi")
        return names

label r13_carryover_events:
    if room13["day"]<R13_WEEK2_DAY or not room13.get("week2_started") or r13_has("w1_links_done"):
        return None
    $ r13_flag("w1_links_done")
    $ _carry=[]
    python:
        for _ok,_flags,_lines in R13_CARRY_GOOD:
            if _ok() and not all(r13_has(f) for f in _flags):
                _carry.append((_flags,_lines))
        _refuse=[]
        if (r13_has("bori_hostile") or r13_has("bori_punished")) and not (r13_has("bori_ally") or r13_has("bori_cleared")):
            _refuse.append(("bori_refuses",[("resident_bori","수레를 끌어 달라고요? 배급대 앞에서 다들 구경만 했죠. 그러니 이번엔 저도 우리 집부터 챙길래요.")]))
        if r13_has("eunho_blackmailed") and not r13_has("supply_terms") and not any("supply_terms" in fl for fl,l in _carry):
            _refuse.append(("eunho_refuses",[("resident_eunho","저울 일에 반값 받고 입 다문 분이 이제 와서 나눠 달라는 거요? 장부에 적을 이름만 하나 더 늘 뿐이오.")]))
        if len(r13_bad_rumors())>=2 and not any(f=="shelter_agreed" for fl,l in _carry for f in fl):
            _refuse.append(("teacher_doubts",[("resident_teacher","좋은 이야기도, 나쁜 이야기도 들었어요. 어느 쪽이 맞는지는 제가 직접 본 적이 없어요."),("resident_teacher","아이들이 있는 교실이니, 손님을 아는 분이 보증해 주시면 좋겠어요.")] if r13_has("rumor:fair") else [("resident_teacher","그 소문들, 저도 들었어요. 그래서 아이들이 있는 교실에 누구를 들일지는 조심해야 해요.")]))
    if not _carry and not _refuse:
        return None
    call r13_ev_here("calm")
    call r13_lines([(None,"월요일 아침이 되자, 지난주에 내가 한 일들의 결과가 먼저 나를 찾아왔다.")],"carry:open")
    while _carry:
        $ _flags,_lines=_carry.pop(0)
        call r13_lines(_lines,"carry:good:"+_flags[0])
        $ r13_flag(*_flags)
    while _refuse:
        $ _flag,_lines=_refuse.pop(0)
        call r13_lines(_lines+[("dad","(지난주에 내가 한 일 때문에 이 길은 막혔다. 다른 길을 찾아야 한다.)",{"thought":True})],"carry:refuse:"+_flag)
        $ r13_flag(_flag)
    return None

label r13_carry_sled:
    call r13_lines([("karo","썰매는 마차 바퀴 대신 쓰려고 둔 거예요. 열 냥이면 일주일 빌려 드리죠. 끄는 건 직접 하셔야 합니다.")],"carry:sled:open")
    menu:
        "썰매를 열 냥에 빌린다" if r13_cash_now()>=10:
            $ r13_cash(-10,"까로의 마차 썰매")
            call r13_lines([("karo","환자를 태울 땐 담요부터 까세요. 눈길에서는 생각보다 많이 흔들리거든요.")],"carry:sled:paid")
            $ r13_flag("transport_terms","sled_hired")
        "썰매는 다음에 빌린다":
            pass
    return

label r13_carry_eunho_full:
    call r13_lines([("resident_eunho","반값 거래는 끝났소. 대피소에 쓸 몫을 다 사려면 열다섯 냥이오.")],"carry:eunho:open")
    menu:
        "열다섯 냥을 낸다" if r13_cash_now()>=15:
            $ r13_cash(-15,"대피소 식량과 장작")
            call r13_lines([("resident_eunho","장부에는 당신 이름으로 적겠소. 사람들에게 나눠 주는 일도 당신이 맡으시오.")],"carry:eunho:paid")
            $ r13_flag("supply_terms","supplies_bought")
        "다음에 산다":
            pass
    return

label r13_carry_vouch:
    $ _v=r13_carry_vouchers()
    if not _v:
        call r13_lines([("resident_teacher","보증해 줄 분이 있으면 데려오세요. 지금은 나쁜 소문밖에 안 들려요."),
            ("dad","(지난주에 나는 이 마을에서 나를 믿어 줄 사람을 하나도 만들지 못했다.)",{"thought":True})],"carry:vouch:none")
        return
    $ _who=_v[0]
    call r13_lines([(_who,"이분은 제가 압니다. 소문이랑은 달라요. 지난주에 직접 봤어요."),
        ("resident_teacher","……보증해 줄 분이 있다면요. 교실을 쓰세요. 다만 아이들 자리는 따로 남겨 두고요.")],"carry:vouch:yes")
    $ r13_flag("shelter_agreed","vouched")
    return
