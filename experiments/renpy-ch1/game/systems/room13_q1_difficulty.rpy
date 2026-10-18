# Q1 rules 3: evidence opens arguments; a committed interpretation must survive rebuttal.
# Rules 1/2 saves retain their original meeting contract.
init 192 python:
    def r13_q1_hard():
        return (store.room13 or {}).get("q1_rules")==3

    for key,name,fact,limit in (
        ("L21","덮개 작업표","2일 낮, 톡이 실룩에게 맡긴 작업. 대상은 3번 등의 덮개, 지급 부품은 나사 두 개. 조각 교체 수량과 회수 예정 수량은 모두 0이다.","작업을 맡겼다는 기록이다. 실제로 누가 무엇을 했는지는 별도 확인이 필요하다."),
        ("L22","3번 등의 자재 대장","광장 3이라는 이름표의 조각은 3번 등에 설치된 마을 자재로 등재되어 있다. 덮개 부품과 조각은 별도 항목이며, 조각의 폐기·양도 기록은 없다.","기록이 없다는 이유만으로 행위자나 절도 시각을 정할 수 없다."),
    ):
        ROOM13["evidence"][key]=dict(id=key,name=name,kind="기록",establishes=fact,does_not_establish=limit,scenes=[],current_run_only=True,retained_on_show=True)
        R13_RECORD_SHORT[key]=name
        ROOM13["evidence_sources"][key]="resident_tok"

    def r13_q1_round(prompt,correct,wrong1,reason1,wrong2,reason2):
        return dict(prompt=prompt,options=[("correct",correct),("first",wrong1),("second",wrong2)],
            wrong={"first":("neoul",reason1),"second":("neoul",reason2)})

    R13_Q1_HARD_ARGUMENTS=winter_copy.deepcopy(R13_Q1_ARGUMENTS)
    def r13_q1_hard_statement(sid):
        return next(st for st in R13_Q1_HARD_ARGUMENTS if st["id"]==sid)

    def r13_q1_set_counter(sid,rounds,correct=None,observed=None):
        st=r13_q1_hard_statement(sid)
        after=correct if correct is not None else st.get("counter",{}).get("correct",st.get("broken",[]))
        # Keep the existing counter protocol for other systems; the rules-3 label reads rounds.
        st["counter"]=dict(lines=[("neoul",rounds[0]["prompt"])],prompt=rounds[0]["prompt"],
            options=rounds[0]["options"],wrong=rounds[0]["wrong"],correct=list(after),rounds=rounds)
        if observed is not None:
            st["broken"]=list(observed)
            if st.get("pair"):st["pair"]["broken"]=list(observed)

    r13_q1_set_counter("v_trace",[
        r13_q1_round("같은 색의 끈이라면 다른 집에도 있지 않소?",
            "뜯긴 끝의 모양이 맞습니다.",
            "실룩 씨가 같은 색의 끈을 소지했습니다.","같은 물건을 쓴다는 것만으로 현장에 남긴 사람을 정할 수는 없소.",
            "등을 열 때 이 끈을 썼다는 뜻입니다.","끈을 비교하는 일과 누가 언제 썼는지는 따로 확인해야 하오.")],
        observed=[("resident_siluk","색도 굵기도 흔한 물건이오. 무엇이 같다는 거요?")])

    r13_q1_set_counter("v_recent",[
        r13_q1_round("첫 순찰의 관찰로 흔적이 남은 때를 어디까지 좁힐 수 있소?",
            "첫 순찰의 내부 확인 뒤입니다.",
            "우박이 조각을 돌려놓은 순간입니다.","조각을 돌려놓은 순간과 끈이 남은 순간을 같은 일로 볼 근거는 없소.",
            "등이 완전히 식은 뒤에 남았습니다.","끈이 걸리는 때와 등이 식는 때를 같은 시각으로 정할 수 있소?"),
        r13_q1_round("초롱은 새벽에도 미지근했다고 했소. 그러면 그때까지 조각이 있었던 것 아니오?",
            "내부 확인과 잔열은 다릅니다.",
            "새벽 뒤에만 조각을 꺼낼 수 있습니다.","남아 있던 온기만으로 조각까지 남아 있었다고 정할 수는 없소.",
            "미지근했다는 말을 취소해야 합니다.","조각이 없어도 온기는 남을 수 있소. 온도를 느꼈다는 말 자체가 거짓이 되는 것은 아니오.")],
        correct=[("dad","끈은 첫 순찰에서 뚜껑을 확인한 뒤에 남았습니다. 잔열로 그보다 정확한 시각까지 정하지는 않겠습니다.")])

    r13_q1_set_counter("v_action",[
        r13_q1_round("조각이 사라졌다는 결과와 직접 본 움직임을 나눠 말하시오.",
            "조각은 봤지만 얼굴은 못 봤습니다.",
            "빈 등을 보니 마지막 작업자입니다.","빈 등만으로 그 사이에 누가 손을 댔는지 정할 수 없소. 직접 본 부분을 대시오.",
            "어두워진 순간에 꺼낸 겁니다.","밝기가 변한 이유는 여럿일 수 있소. 목격한 움직임과 밝기를 혼동하지 마시오.")])

    r13_q1_set_counter("v_identity",[
        r13_q1_round("부리의 관찰로 확인된 사람과 행동은 어디까지요?",
            "도움받고 작업한 사람이 실룩입니다.",
            "실룩이 조각을 들고 내려왔습니다.","부리는 손 안이 가렸다고 했소. 보지 못한 물건을 보았다고 바꿀 수는 없소.",
            "등을 열었으니 반출도 실룩입니다.","등 앞의 작업과 조각 반출은 아직 연결할 부분이 남아 있소.")])

    r13_q1_set_counter("v_link",[
        r13_q1_round("두 사람은 각자 다른 곳에서 보았소. 관찰을 묶을 기준은 무엇이오?",
            "부리가 수레를 도운 직후입니다.",
            "두 사람 모두 3번 등을 보았습니다.","같은 장소에도 여러 번 사람이 올 수 있소. 두 관찰의 순서를 연결해야 하오.",
            "두 사람 모두 밤에 보았습니다.","밤이라는 넓은 시간만으로 같은 작업을 보았다고 할 수는 없소."),
        r13_q1_round("그때 부리가 본 실룩과, 초롱이 본 손의 주인이 달랐을 가능성은?",
            "내려올 때까지 작업자가 같았습니다.",
            "수레를 봤으니 얼굴도 확인했습니다.","같은 수레를 봤다고 반대편 사람의 얼굴까지 보이는 것은 아니오.",
            "손이 가렸으니 다른 이는 없습니다.","손 안이 가렸다는 사실로 다른 사람의 유무를 증명할 수는 없소.")],
        observed=[("neoul","한 사람은 얼굴을, 한 사람은 물건을 보았소. 두 기록을 함께 냈다는 것만으로 같은 작업이 되지는 않소.")])

    r13_q1_set_counter("v_origin",[
        r13_q1_round("창고 이름표에서 확인할 수 있는 것은 무엇이오?",
            "3번 등의 조각이 창고에 있습니다.",
            "판매자가 직접 3번 등을 열었습니다.","물건의 출처와 판매자가 직접 한 행동은 다른 부분이오.",
            "백 부인이 등에서 직접 가져왔습니다.","현재 보관한 사람과 처음 가져간 사람이 같다는 근거는 아직 없소.")])

    r13_q1_set_counter("v_trade",[
        r13_q1_round("같은 금액의 거래는 여럿일 수 있소. 두 기록은 무엇으로 이어집니까?",
            "날짜·번호·품목·대금이 같습니다.",
            "두 냥이라는 금액이 같습니다.","같은 값으로 거래한 다른 물건일 가능성을 금액 하나로 지울 수는 없소.",
            "돈이 필요했다는 사정과 맞습니다.","돈이 필요했다는 사정은 이 원장이 그 사람의 거래라는 증명이 아니오.")],
        observed=[("resident_madam","제 원장과 그 쪽지가 같은 거래라는 근거부터 대세요.")])

    r13_q1_set_counter("v_own",[
        r13_q1_round("쪽지에서 심부름이라는 설명과 부딪히는 부분은 무엇이오?",
            "자기 소유 조각을 판다는 조건입니다.",
            "대금을 실룩이 받았다는 부분입니다.","심부름꾼도 돈을 대신 받을 수 있소. 돈을 받았다는 사실만으로는 부족하오.",
            "창고 조각의 광장 이름표입니다.","물건의 출처가 공공 자재라는 것과 누가 판매 조건을 받아들였는지는 구별하시오."),
        r13_q1_round("그 조건을 받아들였다면, 실룩이 훔쳤다는 뜻이오?",
            "판매는 확인됐고 취득 경위는 남습니다.",
            "소유 조건이니 정당하게 받은 겁니다.","소유권을 주장한 문구가 실제 소유권까지 증명하지는 않소.",
            "자기 물건으로 팔았으니 훔친 겁니다.","건네받거나 주운 물건도 팔 수 있소. 어떻게 얻었는지 아직 답을 듣지 못했소.")],
        correct=[("resident_siluk","…내 물건이라고 팔았소. 톡이 버린다기에 받은 거요.")],
        observed=[("resident_siluk","돈을 받아 왔다는 쪽지요. 그걸로 내 심부름이라는 말을 뒤집을 수 있소?")])

    r13_q1_set_counter("v_slip",[
        r13_q1_round("실룩의 두 설명 중 어느 부분이 함께 성립할 수 없소?",
            "수리점에서 받았나, 등에서 꺼냈나입니다.",
            "조각을 팔았다는 말과 빚이 있다는 말입니다.","빚이 있는 사람이 물건을 팔았다는 두 말은 모순되지 않소.",
            "직접 꺼냈다는 말과 수리했다는 말입니다.","수리 중 물건을 꺼낼 수도 있소. 수리였다는 해명은 작업 범위까지 따져야 하오.")])

    R13_Q1_HARD_ARGUMENTS.extend([
        r13_q1_statement("h_work","resident_siluk","등에 손댄 건 톡이 맡긴 수리였소. 작업표도 있소.",lines=[
            ("dad","맡긴 일과 조각의 처리 내역을 함께 확인하겠습니다."),
            ("resident_siluk","톡의 서명이 있소. 나 혼자 멋대로 등을 만진 게 아니란 말이오."),
            ("resident_tok","덮개가 흔들린다고 해서 점검을 맡겼어요. 이건 작업표, 이쪽은 자재 대장이에요."),
            (None,"작업표에는 덮개, 나사 두 개, 조각 교체 0, 회수 예정 0이 적혀 있었다. 대장의 광장 3 조각은 사용 중인 마을 자재였다.")],question=True),
        r13_q1_statement("h_scope","resident_siluk","서명한 작업표가 있으니 조각을 가져간 것도 맡긴 일 안에 들어가오.",["L21","L22"],
            [("resident_siluk","톡이 일을 맡긴 건 분명하오. 조각을 다룬 일도 그 작업으로 봐야 하지 않겠소?")],need=["h_work"],pair=True),
    ])
    r13_q1_set_counter("h_scope",[
        r13_q1_round("작업표와 대장을 함께 놓으면 어떤 범위가 확인되오?",
            "덮개 수리와 조각 처분은 별개입니다.",
            "서명이 있으니 조각도 실룩의 것입니다.","작업을 맡긴 서명이 물건의 소유권을 넘긴 서명까지 되는 것은 아니오.",
            "회수 0이니 현장에 가지 않았습니다.","회수 수량은 누가 현장에 있었는지를 증명하지 않소."),
        r13_q1_round("대장에 양도 기록이 없으면 그것만으로 절도가 확정되는 것이오?",
            "반출은 입증했습니다. 허락도 확인하죠.",
            "빈 기록 자체가 실룩의 절도 증거입니다.","기록이 비었다는 것만으로 행위자를 만들어 낼 수는 없소.",
            "맡긴 일이니 개인 물건으로 팔 수 있죠.","작업을 맡겼다는 사실에서 개인 물건으로 처분할 권한이 나오지는 않소.")],
        correct=[("dad","실룩 씨의 반출은 앞서 연결했습니다. 이 작업표로 조각까지 넘겨받았다는 해명은 성립하지 않습니다. 별도의 허락을 받았습니까?")])
    _q1_h_permission=r13_q1_hard_statement("v_permission")
    _q1_h_permission["press"]=[("dad","덮개 점검과 별개로, 조각을 가져가도 된다고 허락받았습니까?"),
        ("resident_tok","덮개 점검만 맡겼어요. 조각을 교체하거나 폐기하라고 한 적도, 실룩 씨에게 넘긴 적도 없어요."),
        ("resident_siluk","…따로 허락받지는 않았소. 내가 꺼내 팔았소. 식었으니 버려도 되는 줄 알았소."),
        ("resident_siluk","빚이 열두 냥이오. 못 갚으면 아이들을 일꾼으로 보내야 했소. 돌려놓을 생각도 못 했소.")]

    _r13_qh_statements=r13_debate_statements
    def r13_debate_statements(claim):
        return R13_Q1_HARD_ARGUMENTS if claim=="Q1" and r13_q1_hard() else _r13_qh_statements(claim)

    _r13_qh_node_open=r13_q1_node_open
    def r13_q1_node_open(st):
        if r13_q1_hard():
            if st["id"]=="v_action":return r13_q1_done("v_user") or r13_q1_done("v_identity")
            if st["id"]=="v_identity":return r13_has("L17")
            if st["id"]=="v_origin":return r13_has("L09")
            if st["id"]=="h_work":return r13_q1_removal_proved()
            if st["id"]=="v_permission":return r13_q1_removal_proved() and r13_q1_done("h_scope")
        return _r13_qh_node_open(st)

    _r13_qh_required=r13_debate_required
    def r13_debate_required(claim):
        if claim=="Q1" and r13_q1_hard():return [st["id"] for st in R13_Q1_HARD_ARGUMENTS if r13_q1_node_open(st)]
        return _r13_qh_required(claim)

    _r13_qh_press=r13_q1_press_done
    def r13_q1_press_done(sid):
        _r13_qh_press(sid)
        if r13_q1_hard() and sid=="h_work" and r13_q1_done(sid):r13_grant(["L21","L22"],"광장 회의에서 확인한 작업표와 자재 대장")

    def r13_q1_formal_errors():
        return len((store.room13 or {}).get("q1_formal_errors",[]))

    def r13_q1_prepare_counter(sid,key):
        r13_edit(q1_argument_pending={})
        st=r13_debate_statement("Q1",sid)
        if not r13_q1_hard() or r13_debate_closed("Q1") or r13_debate_judge("Q1",sid,key)[0]!="break" or not st.get("counter",{}).get("rounds"):return False
        supports=list(st.get("pair",{}).get("keys",[key]))
        if not all(k in (store.room13 or {}).get("evidence",[]) for k in supports):return False
        r13_edit(q1_argument_pending=dict(sid=sid,supports=supports))
        return True

    def r13_q1_evaluate_counter(sid,choices):
        # Read-only; neither owning a record nor selecting a plausible sentence proves a fact.
        pending=(store.room13 or {}).get("q1_argument_pending",{})
        st=r13_debate_statement("Q1",sid);rounds=st.get("counter",{}).get("rounds",[])
        if not r13_q1_hard() or r13_debate_closed("Q1") or pending.get("sid")!=sid or not r13_q1_node_open(st) or r13_q1_done(sid):return "invalid",None
        expected=st.get("pair",{}).get("keys")
        if expected and pending.get("supports")!=list(expected):return "invalid",None
        if not expected and (len(pending.get("supports",[]))!=1 or pending["supports"][0] not in st.get("accept",[])):return "invalid",None
        if not pending.get("supports") or not all(k in (store.room13 or {}).get("evidence",[]) for k in pending["supports"]):return "invalid",None
        if len(choices)!=len(rounds) or any(choice not in dict(r["options"]) for choice,r in zip(choices,rounds)):return "invalid",None
        failed=next((i for i,choice in enumerate(choices) if choice!="correct"),None)
        return ("correct",None) if failed is None else ("wrong",failed)

    def r13_q1_commit_counter(sid,choices):
        status,failed=r13_q1_evaluate_counter(sid,choices)
        if status=="invalid":return status,failed
        pending=winter_copy.deepcopy(store.room13["q1_argument_pending"])
        if status=="correct":
            proofs=dict(store.room13.get("q1_argument_proofs",{}));proofs[sid]=dict(supports=pending["supports"],choices=list(choices))
            r13_edit(q1_argument_proofs=proofs,q1_argument_pending={})
        else:
            r13_q1_record_error(dict(sid=sid,supports=pending["supports"],choices=list(choices),failed=failed))
        return status,failed

    def r13_q1_record_error(error):
        if not r13_q1_hard() or r13_debate_closed("Q1"):return False
        errors=list(store.room13.get("q1_formal_errors",[]))+[error]
        r13_edit(q1_formal_errors=errors,q1_argument_pending={})
        if len(errors)>=3:r13_debate_close("Q1","argument_limit")
        return True

    def r13_q1_reject_evidence(sid,key,result):
        st=r13_debate_statement("Q1",sid)
        # Already settled statements and questions are not rebuttal opportunities.
        if result not in ("soft","wrong") or st.get("question") or r13_q1_done(sid):return False
        return r13_q1_record_error(dict(sid=sid,supports=[key],choices=[],failed="evidence"))

    _r13_qh_summary=r13_q1_summary
    def r13_q1_summary():
        rows=_r13_qh_summary()
        if r13_q1_hard() and (store.room13 or {}).get("debate",{}).get("closed",{}).get("ep1:Q1")=="argument_limit":
            return rows[0],"확정한 반박이 세 번 무너져 회의가 끝났다.",rows[2]
        return rows

label r13_q1_hard_counter(sid):
    $ _qh_counter=r13_debate_statement("Q1",sid)["counter"]
    $ _qh_choices=[]
    $ _qh_index=0
    while _qh_index<len(_qh_counter["rounds"]):
        $ _qh_round=_qh_counter["rounds"][_qh_index]
        call r13_lines([("neoul",_qh_round["prompt"])],"q1h:counter:"+sid+":"+str(_qh_index))
        $ _qh_options=list(_qh_round["options"])
        $ _qh_shift=(sum(ord(ch) for ch in sid)+_qh_index)%len(_qh_options)
        $ _qh_options=_qh_options[_qh_shift:]+_qh_options[:_qh_shift]
        $ _qh_pick=renpy.display_menu([("어떤 설명을 주장할까?",None)]+[(text,key) for key,text in _qh_options]+[("아직 주장하지 않고 자료를 다시 본다","withdraw")])
        if _qh_pick=="withdraw":
            $ r13_edit(q1_argument_pending={})
            return None
        $ _qh_choices=_qh_choices+[_qh_pick]
        $ _qh_index+=1
    $ _qh_claim_text="\n".join(dict(r["options"])[choice] for choice,r in zip(_qh_choices,_qh_counter["rounds"]))
    call screen r13_confirm(_qh_claim_text+"\n\n이 반박을 확정합니다. 무너진 정식 반박이 세 번이면 회의가 끝납니다. 현재 %d회."%r13_q1_formal_errors(),"이 논증으로 반박한다","자료를 더 검토한다")
    if not _return:
        $ r13_edit(q1_argument_pending={})
        return None
    $ _qh_status,_qh_failed=r13_q1_commit_counter(sid,_qh_choices)
    if _qh_status=="correct":
        call r13_lines(_qh_counter["correct"],"q1h:accepted:"+sid)
        return True
    if _qh_status=="wrong":
        call r13_lines([_qh_counter["rounds"][_qh_failed]["wrong"][_qh_choices[_qh_failed]]],"q1h:rejected:"+sid)
        call r13_q1_error_notice
    return False

label r13_q1_hard_rules:
    if r13_q1_hard():
        call r13_lines([(None,"자료 열람과 질문은 자유롭다. 발언에 맞지 않는 자료를 근거로 내거나, 상대의 반론에 잘못된 답을 확정하면 오답이 된다."),
            (None,"오답 세 번이면 이번 회의가 끝난다. 해석은 확정 전에 철회할 수 있다. 실패 뒤에는 같은 자료로 회의를 처음부터 다시 할 수 있다.")],"q1h:rules")
    return

label r13_q1_error_notice:
    if r13_debate_closed("Q1"):
        call r13_lines([("neoul","반박이 세 번 무너졌소. 이 회의의 반론은 여기까지 받겠소.")],"q1h:limit")
    else:
        call r13_lines([("neoul","그 반박은 받아들이지 않겠소. 지금까지 %d번이오. 자료와 주장을 다시 살피시오."%r13_q1_formal_errors())],"q1h:warning")
    return
