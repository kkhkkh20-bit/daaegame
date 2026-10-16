# Re-inspection and suspicion vs. crime (owner, 0.18.19).
#   Candlestick: every part can be looked at from the first run. If Dad watched 톡 fit the new pin
#     on day 4 (tok_repair), looking at the ornament ring now carries that comparison. Nothing is
#     unlocked by an earlier run.
#   은호: he hides a ledger when Dad comes in. It is illegal credit with interest, not the murder.
#     The fact stays useful for supplies (week 2), not for the trial.
init 122 python:
    ROOM13["evidence"]["H15"]=dict(id="H15",name="장식 고리 조각의 덧댄 이음",kind="관찰기록",
        establishes="봉해 둔 촛대 윗부분의 장식 고리는 한쪽으로 눌렸고, 그 안에 낀 가는 금속 조각은 이음을 덧대어 울퉁불퉁하다.",
        does_not_establish="조각이 누구 것인지, 언제 끼었는지는 이것만으로 알 수 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence"]["J16"]=dict(id="J16",name="은호의 외상 장부",kind="증언",
        establishes="은호는 배급표 없는 집에 이자를 붙여 외상으로 물건을 내줬다. 촌장의 허가는 없었다.",
        does_not_establish="13호 사건과 이어지는 내용은 이 장부에 없다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"]["J16"]="resident_eunho"
    R13_RECORD_SHORT.update(H15="고리 조각의 이음",J16="은호의 외상 장부")

    ROOM13["topics"].update({
        "seal_look":dict(npc="resident_seori",title="봉해 둔 촛대를 다시 볼 수 있겠습니까?",day=[5,13],need=["E07"],give=[],flags=[],lines=[],case="occurred"),
        "eunho_hidden_ledger":dict(npc="resident_eunho",title="“방금 덮은 장부는 뭡니까?”",day=[5,7],need=["saw_eunho_hide"],not_flags=["eunho_credit_known"],give=["J16"],flags=["eunho_credit_known"],lines=[
            ("dad","방금 덮은 장부는 뭡니까?"),
            ("resident_eunho","……가게 장부요."),
            ("dad","제가 들어오자마자 덮으셨습니다."),
            ("resident_eunho","외상 장부예요. 배급표 없는 집에 이자를 붙여 물건을 내줬습니다. 촌장님 허가는 없었고요."),
            ("resident_eunho","그날 밤 여관 일이랑은 상관없어요. 제가 장부를 숨긴 건 이 외상 때문이었습니다.")]),
        "w2_eunho_credit":dict(npc="resident_eunho",title="외상 장부 이야기를 꺼낸다",day=[8,13],need=["eunho_credit_known","eunho_refuses"],not_flags=["supply_terms"],give=[],flags=["supply_terms"],lines=[
            ("dad","배급표 없는 집에 붙인 이자, 서리 검사원이 알면 어떻게 될까요."),
            ("resident_eunho","……그 장부를 넘기지 않는다면, 대피소 몫은 내놓겠소. 이자도 지우지요.")]),
    })
    R13_TOPIC_LABELS["seal_look"]="r13_seal_look"

label r13_reinspect_events:
    if room13["day"] in (5,6) and room13["period"]<=1 and room13["case_state"]=="occurred" and r13_where("resident_eunho")==room13["location"] and not r13_has("saw_eunho_hide"):
        call r13_ev_here("calm")
        # 0.18.71: 은호 spends his mornings at the market stall now; the line follows the place.
        $ _eh_where={"market":"노점 판자 위","store":"창고 계산대 위"}.get(room13["location"],"탁자 위")
        call r13_lines([(None,"은호가 나를 보자 %s의 장부를 급히 덮었다. 그리고 그 위에 자루 하나를 올려놓았다."%_eh_where)],"eunho:hide")
        $ r13_flag("saw_eunho_hide")
    return

label r13_seal_look:
    call r13_lines([("resident_seori","봉인은 풀지 않고 보세요. 손은 대지 마시고요.")],"seal:open")
    $ _sl_loop=True
    while _sl_loop:
        menu:
            "전체를 살펴본다":
                call r13_lines([(None,"생각보다 무겁다. 윗부분 끝에 검게 굳은 얼룩이 있다. 받침과 윗부분은 따로 봉해져 있다.")],"seal:whole")
            "갈라진 면을 살펴본다":
                call r13_lines([(None,"윗부분의 갈라진 면은 안쪽이 날카롭게 드러나 있다. 받침 쪽 면은 무디다.")],"seal:break")
            "장식 고리를 살펴본다":
                call r13_lines([(None,"윗부분 옆의 장식 고리가 한쪽으로 눌려 있다. 고리 안에 가는 금속 조각이 끼어 있다."),
                    (None,"조각의 이음새는 덧댄 자리라 울퉁불퉁하다.")],"seal:ring")
                if "tok_repair" in room13.get("read_topics",[]):
                    call r13_lines([("dad","(톡의 작업대에서 본 핀의 연결 부위와 닮았다.)",{"thought":True})],"seal:ring:known")
                $ r13_grant(["H15"],"서리 검사원 앞에서 봉해 둔 촛대를 봄")
            "그만 본다":
                $ _sl_loop=False
    $ r13_forget_topic("seal_look")
    return
