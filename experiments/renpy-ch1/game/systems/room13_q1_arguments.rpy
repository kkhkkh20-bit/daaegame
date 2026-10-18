# Q1 version 2: facts can be established by different arguments in this run.
# Old meetings already in progress retain the original five-statement contract.
init 191 python:
    def r13_q1_v2():
        return (store.room13 or {}).get("q1_rules") in (2,3)

    def r13_q1_activate():
        s=store.room13 or {}
        if "q1_rules" in s or r13_has("lt_done"):return
        d=s.get("debate",{})
        started=any(d.get(k,{}).get("Q1") for k in ("broken","pressed","misses")) or d.get("closed",{}).get("ep1:Q1") or "Q1" in s.get("propositions",[])
        r13_edit(q1_rules=1 if started else 3)

    for key,name,fact,limit in (
        ("L15","초롱의 첫 순찰","초롱은 2일 밤 첫 순찰에서 3번 등을 열어 받침을 바로잡았다. 조각은 안에 있었고 뚜껑 틈에는 끈이 없었다.","그 뒤 등을 연 사람의 얼굴은 확인하지 못했다."),
        ("L16","초롱이 본 반출","수레 바퀴가 턱에 걸리고 부리가 도운 직후, 초롱은 3번 등에서 빛나는 조각이 들려 나오는 것을 보았다. 동튼 뒤 다시 확인하니 등 안이 비어 있었다.","반대쪽에 있어 작업자의 얼굴은 못 봤다."),
        ("L17","부리의 밤 목격","부리는 턱에 걸린 수레를 도우며 실룩의 얼굴을 봤다. 실룩이 등 앞에서 작업하고 내려올 때까지 다른 사람으로 바뀌지 않았다. 손 안은 뚜껑과 몸에 가려졌다.","조각을 꺼내는 손동작이나 창고 거래는 보지 못했다."),
        ("L18","백 부인의 매입 원장","3일 해 질 녘, 거래 27번. 조각 한 점에 두 냥. 판매자는 얼굴 대신 수령 표시를 남겼다.","표시만으로 판매자나 직접 훔친 사람을 확정할 수 없다."),
        ("L19","실룩의 대금 쪽지","실룩이 내놓은 정산 쪽지. 3일 해 질 녘, 거래 27번, 두 냥. 자기 소유 조각 한 점을 판다는 조건이 적혀 있다.","소유 확인 문구가 사실인지, 조각을 어디서 얻었는지는 알 수 없다."),
        ("L20","실룩의 두 설명","실룩은 수리점에서 톡에게 조각을 건네받았다고 했다. 이어 등 받침에 걸린 조각을 끄집어내느라 손이 아팠다고 말했다.","설명이 어긋난다는 사실만으로 살해 의도까지 알 수 없다."),
    ):
        ROOM13["evidence"][key]=dict(id=key,name=name,kind="증언" if key in ("L15","L16","L17","L20") else "물증",establishes=fact,does_not_establish=limit,scenes=[],current_run_only=True,retained_on_show=True)
        R13_RECORD_SHORT[key]=name

    ROOM13.setdefault("evidence_sources",{}).update(L15="resident_lamplighter",L16="resident_lamplighter",L17="buri",L18="resident_madam",L19="resident_siluk",L20="resident_siluk")
    R13_CONTACT_RECORDS["resident_madam"]=tuple(R13_CONTACT_RECORDS.get("resident_madam",()))+("L09",)

    _r13_qa_contact=r13_contact_presentations
    def r13_contact_presentations(person):
        rows=_r13_qa_contact(person)
        if r13_q1_v2() and person=="resident_madam" and not r13_has("lt_done") and r13_has("L09") and not r13_has("L18") and "L09" not in rows:
            rows=rows+["L09"]
        return rows

    R13_Q1_NEW_TOPICS={
        "q1v:patrol":("resident_lamplighter","등 안도 직접 보셨습니까?","r13_q1_patrol","L15"),
        "q1v:removal":("resident_lamplighter","다음 순찰 때는 어땠습니까?","r13_q1_removal","L16"),
        "q1v:buri":("buri","그날 밤에 무얼 봤니?","r13_q1_buri","L17"),
        "q1v:receipt":("resident_siluk","빵값은 어디서 마련했습니까?","r13_q1_receipt","L19"),
    }
    for key,(who,title,label,give) in R13_Q1_NEW_TOPICS.items():
        ROOM13["topics"][key]=dict(npc=who,title=title,day=[3,4],need=[],not_flags=[],give=[],flags=[],lines=[])
        R13_TOPIC_LABELS[key]=label

    def r13_q1_topic_available(key):
        if not r13_q1_v2() or not r13_has("lt_dawn") or r13_has("lt_done"):return False
        s=store.room13 or {}
        if s.get("day",1)>4 or (s.get("day")==4 and s.get("period",0)>1):return False
        if r13_has(R13_Q1_NEW_TOPICS[key][3]):return False
        return {"q1v:patrol":r13_has("L06"),"q1v:removal":r13_has("L15"),
            "q1v:buri":r13_has("lt_open") or r13_has("L16"),
            "q1v:receipt":r13_has("lt_siluk_seen")}[key]

    _r13_qa_topics=r13_topics
    def r13_topics(person):
        rows=[row for row in _r13_qa_topics(person) if row[0] not in R13_Q1_NEW_TOPICS]
        rows.extend((key,ROOM13["topics"][key]) for key,spec in R13_Q1_NEW_TOPICS.items() if spec[0]==person and r13_q1_topic_available(key))
        return rows

    _r13_qa_present=r13_present
    def r13_present(person,key,identity=False):
        if r13_q1_v2() and not r13_has("lt_done") and person=="resident_madam" and key=="L09" and r13_has("L09") and not r13_has("L18"):
            _r13_qa_present(person,key,identity)
            r13_grant(["L18"],"이름표 조각을 보고 백 부인이 내놓은 원장")
            return [("dad","광장 3번 등의 이름표입니다. 언제 누구에게서 사셨습니까?"),
                ("resident_madam","어제 해 질 녘이에요. 값을 치렀다는 기록도 있어요. 얼굴은 못 봤지만, 여기 돈을 받았다는 표시가 있잖아요."),
                (None,"원장에 3일, 거래 27번, 조각 한 점, 두 냥이라고 적혀 있었다.")]
        return _r13_qa_present(person,key,identity)

    def r13_q1_statement(sid,who,text,keys=(),lines=(),need=(),question=False,pair=False,counter=None):
        st=dict(id=sid,who=who,text=text,accept=list(keys),broken=list(lines),need=list(need),question=question,
            wrong=(who,"그 자료로는 지금 말한 부분을 확인할 수 없어요."))
        if question:st["press"]=list(lines)
        if pair:
            st["pair"]=dict(keys=list(keys),broken=list(lines),half={k:[(who,"그 자료 하나로는 두 기록이 이어지는지 알 수 없어요. 함께 대조해 주세요.")] for k in keys})
        if counter:st["counter"]=counter
        return st

    def r13_q1_counter(prompt,correct,wrong,reply):
        return dict(lines=[("neoul",prompt)],prompt="어떻게 답할까?",options=[("correct",correct),("over",wrong)],
            correct=[("dad",reply)],wrong={"over":("neoul","직접 확인한 것보다 더 나아간 말이오. 그 연결부터 설명하시오.")})

    R13_Q1_ARGUMENTS=[
        r13_q1_statement("v_accused","neoul","등을 돌보는 톡이 조각을 가져간 것 아니오?",["L03","L04","L14"],
            [("dad","등에서 발견한 흔적입니다. 톡 씨가 남긴 것인지 확인하셨습니까? 등을 돌본다는 이유만으로 가져간 사람까지 정할 수는 없습니다."),
                ("neoul","…그 손이 누구인지는 더 확인하겠소.")]),
        r13_q1_statement("v_trace","resident_siluk","그건 누구나 쓰는 갈색 끈이오.",["L04","L07"],
            [("dad","뚜껑에 남은 끈과 실룩 씨의 끈은 뜯긴 끝이 맞습니다. 한 끈에서 떨어진 조각입니다.")],pair=True),
        r13_q1_statement("v_recent","resident_siluk","내 끈이라도 전에 수리를 돕다가 남겼을 수 있소.",["L15"],
            [("resident_lamplighter","2일 밤 첫 순찰에서 받침을 바로잡으며 뚜껑도 봤어요. 그때는 틈에 끈이 없었어요.")],need=["v_trace"]),
        r13_q1_statement("v_user","neoul","끈을 다른 사람이 빌려 썼을 수도 있지 않소?",lines=[
            ("dad","2일 늦은 밤, 그 끈을 누가 쓰고 있었습니까?"),
            ("resident_siluk","내가 썼소. 수레가 턱에 걸려 부리가 도와준 뒤에 올라갔소. 느슨한 뚜껑을 고쳤을 뿐이오.")],need=["v_recent"],question=True),
        r13_q1_statement("v_action","neoul","등에 손을 댔다고 조각까지 가져간 건 아니오.",["L16"],
            [("resident_lamplighter","부리가 수레 바퀴를 도와준 직후였어요. 등에서 빛나는 조각이 들려 나왔어요. 동튼 뒤 다시 가 보니 안이 비어 있었어요.")],
            counter=r13_q1_counter("얼굴은 보았소?","꺼내는 행동을 본 겁니다.","그 사람이 실룩입니다.","이 증언으로 확인한 건 반출 행동입니다. 얼굴과 같은 시각인지는 따로 연결하겠습니다.")),
        r13_q1_statement("v_identity","resident_siluk","어두웠는데 누가 내 얼굴을 보았다는 거요?",["L17"],
            [("buri","제가 바퀴를 풀어 드렸잖아요. 바로 앞에서 얼굴을 봤어요. 실룩 씨가 등 앞에서 일하고 내려올 때까지 지켜봤어요.")],
            counter=r13_q1_counter("부리는 조각을 꺼내는 손도 보았소?","얼굴과 그 자리를 봤습니다.","훔치는 손까지 봤습니다.","얼굴과 그 자리에 있던 사람은 확인했습니다. 뚜껑에 가린 손 안은 보지 못했습니다.")),
        r13_q1_statement("v_link","neoul","두 사람이 서로 다른 때를 본 것일 수도 있소.",["L16","L17"],
            [("dad","두 분 모두 수레 바퀴가 턱에 걸려 부리가 풀어 준 바로 뒤를 말합니다."),
                ("buri","그 뒤로 실룩 씨가 내려올 때까지 다른 사람이 올라가지 않았어요. 안 보인 건 손 안에 든 것뿐이에요.")],
            need=["v_action","v_identity"],pair=True,
            counter=r13_q1_counter("같은 순간이라고 할 근거가 무엇이오?","수레를 도운 전후가 같습니다.","둘 다 밤이라고 했습니다.","같은 수레를 도운 직후입니다. 부리는 그 뒤 사람이 바뀌지 않은 것까지 확인했습니다.")),
        r13_q1_statement("v_origin","resident_madam","제 창고의 조각은 제가 정당하게 산 거예요.",["L09"],
            [("dad","이름표에 광장 3이라고 쓰여 있습니다. 톡 씨, 폐기한 조각입니까?"),
                ("resident_tok","아니에요. 제 장부에도 지금 3번 등에 넣어 둔 조각으로 적혀 있어요. 바꾸거나 버리라고 한 적 없어요."),
                ("resident_madam","어제, 3일 해 질 녘에 샀어요. 얼굴은 못 봤지만 원장에 받은 표시가 있어요.")]),
        r13_q1_statement("v_trade","resident_siluk","백 부인 원장의 표시만 보고 나라고 할 수 있소?",["L18","L19"],
            [("dad","부인의 원장과 실룩 씨가 내놓은 쪽지는 거래 27번, 조각 한 점, 두 냥으로 같습니다."),
                ("resident_siluk","돈을 대신 받아 왔을 뿐이오. 판 사람까지 나라는 건 아니오.")],need=["v_origin"],pair=True),
        r13_q1_statement("v_own","resident_siluk","나는 돈을 받아 주는 심부름만 했소.",["L19"],
            [("dad","쪽지에는 자기 소유 조각을 판다고 적혀 있습니다. 이 조건으로 돈을 받으셨습니까?"),
                ("resident_siluk","…내가 판 건 맞소. 톡이 버린다기에 받은 거요.")],need=["v_trade"]),
        r13_q1_statement("v_where","resident_siluk","톡이 버린다는 조각을 받았소.",lines=[
            ("dad","어디에서 어떻게 받으셨습니까?"),("resident_siluk","수리점에서 손에 쥐여 줬소."),
            ("resident_tok","그런 적 없어요. 그 조각은 3번 등에 있었어요."),
            ("resident_siluk","버릴 거랬잖소. 등 받침에 걸려서 끄집어내느라 손이…")],need=["v_own"],question=True),
        r13_q1_statement("v_slip","resident_siluk","나는 수리점에서 손에 쥐여 준 걸 받아 왔소.",["L20"],
            [("dad","수리점에서 건네받았다면서 왜 등 받침에서 끄집어냈다는 이야기를 하십니까?")],need=["v_where"],
            counter=r13_q1_counter("이 설명으로 어디까지 말할 수 있소?","받았다는 설명이 어긋납니다.","사람을 죽일 생각이었습니다.","건네받았다는 말과 직접 꺼냈다는 말이 다릅니다. 실룩 씨, 직접 꺼낸 겁니까?")),
        r13_q1_statement("v_permission","resident_siluk","식은 조각인 줄 알았소. 버리는 거라고 생각했소.",lines=[
            ("dad","톡 씨가 가져가도 된다고 허락한 적이 있습니까?"),
            ("resident_tok","없어요. 그 등을 쓰고 있었고, 교체나 폐기를 맡긴 적도 없어요."),
            ("resident_siluk","…허락은 안 받았소. 내가 등에서 꺼내 백 부인에게 팔았소. 돌려놓을 생각도 못 했소."),
            ("resident_siluk","빚이 열두 냥이오. 못 갚으면 아이들을 일꾼으로 보내야 했소. 등 하나 식는다고 사람이 쓰러질 줄은 몰랐소.")],question=True),
    ]

    next(st for st in R13_Q1_ARGUMENTS if st["id"]=="v_slip")["counter"]["correct"].append(("resident_siluk","…수리점에서 받은 게 아니오. 내가 등에서 꺼내 팔았소."))

    def r13_q1_done(sid):
        return sid in r13_debate_state().get("broken",{}).get("Q1",[])

    def r13_q1_removal_proved():
        return (r13_q1_done("v_action") and (r13_q1_done("v_user") or r13_q1_done("v_link"))) or r13_q1_done("v_slip")

    def r13_q1_node_open(st):
        if st["id"]=="v_permission":return r13_q1_removal_proved()
        if st["id"]=="v_trace" and not any(r13_has(k) for k in ("L04","L07")):return False
        if st["id"]=="v_identity" and not (r13_has("L17") or r13_q1_done("v_action")):return False
        if st["id"]=="v_origin" and not any(r13_has(k) for k in ("L09","L18","L19")):return False
        return all(r13_q1_done(sid) for sid in st.get("need",[]))

    _r13_qa_statements=r13_debate_statements
    def r13_debate_statements(claim):
        return R13_Q1_ARGUMENTS if claim=="Q1" and r13_q1_v2() else _r13_qa_statements(claim)

    _r13_qa_visible=r13_debate_visible
    def r13_debate_visible(claim,st):
        return r13_q1_node_open(st) if claim=="Q1" and r13_q1_v2() else _r13_qa_visible(claim,st)

    _r13_qa_required=r13_debate_required
    def r13_debate_required(claim):
        return [st["id"] for st in R13_Q1_ARGUMENTS if r13_q1_node_open(st)] if claim=="Q1" and r13_q1_v2() else _r13_qa_required(claim)

    _r13_qa_ready=r13_debate_ready
    def r13_debate_ready(claim):
        return r13_q1_removal_proved() and r13_q1_done("v_permission") if claim=="Q1" and r13_q1_v2() else _r13_qa_ready(claim)

    _r13_qa_judge=r13_debate_judge
    def r13_debate_judge(claim,sid,key):
        if claim=="Q1" and r13_q1_v2():
            st=r13_debate_statement(claim,sid)
            if key not in (store.room13 or {}).get("evidence",[]) or not r13_q1_node_open(st):return "soft",[("neoul","아직 확인하지 않은 자료나 말로 건너뛸 수는 없소.")]
            if st.get("question"):return "soft",[(st["who"],"제 말에 대해 물어 주세요. 제가 겪은 일부터 답하겠어요.")]
            if key=="L06":return "soft",[("resident_lamplighter","미지근했다는 것만으로 조각이 남아 있었다고 할 수는 없어요. 온기와 직접 본 것은 나눠 말할게요.")]
            if key=="L08":return "soft",[("neoul","그 아이가 말한 어젯밤은 기록실 일이 있던 밤이오. 광장 일이 있던 전날 밤과 같지 않소.")]
        return _r13_qa_judge(claim,sid,key)

    def r13_q1_press_done(sid):
        if not r13_q1_v2():return
        st=r13_debate_statement("Q1",sid)
        if not st.get("question") or not r13_q1_node_open(st):return
        r13_debate_mark("broken","Q1",sid)
        if sid=="v_where":r13_grant(["L20"],"광장 회의에서 들은 실룩의 두 설명")
        if sid=="v_permission":r13_flag("siluk_debt_known")

    _r13_qa_answerable=r13_debate_answerable
    def r13_debate_answerable(claim,st):
        if claim=="Q1" and r13_q1_v2():
            if not r13_q1_node_open(st):return False
            if st.get("question"):return True
        return _r13_qa_answerable(claim,st)

    _r13_qa_engageable=r13_debate_engageable
    def r13_debate_engageable(claim):
        return True if claim=="Q1" and r13_q1_v2() else _r13_qa_engageable(claim)

    _r13_qa_hints=r13_debate_hint_due
    def r13_debate_hint_due(claim,sid):
        return None if claim=="Q1" and r13_q1_v2() else _r13_qa_hints(claim,sid)

    _r13_qa_partial=r13_debate_partial_lines
    def r13_debate_partial_lines(claim):
        return [(None,t) for t in r13_q1_summary()[:2]] if claim=="Q1" and r13_q1_v2() else _r13_qa_partial(claim)

    _r13_qa_seats=r13_debate_seats
    def r13_debate_seats(session):
        if session=="ep1" and r13_q1_v2():
            step=2 if "Q1" in (store.room13 or {}).get("propositions",[]) else 1 if r13_debate_state()["broken"].get("Q1") else 0
            return [(who,step if who in R13_DEBATE["Q1"]["sway"] else 0) for who in R13_DEBATE_SEATS["ep1"]]
        return _r13_qa_seats(session)

    R13_Q1_ARGUMENT_QUESTION=("주장의 연결","누가 한 행동인지와, 그 행동이 무엇인지 함께 확인했을까?","현장에 있었다는 것, 물건을 팔았다는 것, 직접 가져갔다는 것은 서로 다르다.","초롱과 부리에게 그날 밤에 직접 본 일을 물을 수 있다. 실룩의 대금 쪽지와 백 부인의 원장은 서로 대조할 수 있다.")

    def r13_q1_question(sid):
        return R13_Q1_ARGUMENT_QUESTION if sid=="v_result" else R13_Q1_QUESTIONS[sid]

    _r13_qa_review_rows=r13_q1_review_rows
    def r13_q1_review_rows():
        if not r13_q1_v2():return _r13_qa_review_rows()
        return [("v_result",r13_has("lt_solved"),R13_Q1_ARGUMENT_QUESTION)]

    _r13_qa_summary=r13_q1_summary
    def r13_q1_summary():
        if not r13_q1_v2():return _r13_qa_summary()
        s=store.room13 or {}
        if r13_has("lt_done") and not r13_has("lt_solved") and not r13_debate_closed("Q1") and (s.get("day",1)>4 or (s.get("day")==4 and s.get("period",0)>1)):
            return "회의가 열리기 전에 조사 기한이 지났다.","톡의 혐의를 따질 기회를 놓쳤다.","톡의 처분을 바꾸지는 못했다."
        facts=[]
        for sid,text in (("v_accused","톡을 지목한 근거의 한계"),("v_trace","현장 끈의 짝"),("v_recent","끈이 남은 시기"),("v_action","조각을 꺼낸 행동"),("v_identity","등 앞에 있던 사람"),("v_link","두 목격의 연결"),("v_origin","창고 조각의 출처"),("v_trade","실룩의 거래"),("v_slip","실룩의 설명 속 모순"),("v_permission","무단 반출 인정")):
            if r13_q1_done(sid):facts.append(text)
        fact="확인한 내용: "+", ".join(facts)+"." if facts else "회의에서 근거로 확정한 내용은 없었다."
        if r13_has("lt_solved"):gap="이 근거들을 연결해 실룩의 무단 반출을 밝혔다. 다른 조사 방법까지 모두 거칠 필요는 없었다."
        elif r13_debate_ready("Q1"):gap="근거는 연결했지만 적정한 범위의 결론을 확정하지 못했다."
        elif r13_q1_removal_proved():gap="반출은 연결했지만 허락을 받아 가져갔다는 설명을 끝까지 확인하지 못했다."
        else:gap="누가 조각을 직접 가져갔는지 연결한 논증이 완성되지 않았다."
        return fact,gap,"톡은 풀려났다." if r13_has("tok_cleared") else "톡의 처분을 바꾸지는 못했다."

    _r13_qa_review_lines=r13_q1_review_lines
    def r13_q1_review_lines():
        if not r13_q1_v2():return _r13_qa_review_lines()
        rows=[(None,t) for t in r13_q1_summary()]
        if r13_q1_can_restore("meeting"):rows.append((None,"회의 직전으로 돌아가면 당시 자료로 다시 이야기할 수 있다."))
        if r13_q1_can_restore("investigation"):rows.append((None,"조사를 다시 시작하면 당시의 시간과 소지품도 함께 돌아간다."))
        return rows

    _r13_qa_notes=r13_q1_notes
    def r13_q1_notes():
        rows=_r13_qa_notes()
        if r13_q1_v2() and not r13_has("lt_done"):
            for keys,title,question in ((["L15","L16","L17"],"서로 다른 곳에서 본 그날 밤","각자 직접 본 부분이 어디까지일까?"),(["L18","L19"],"조각과 대금","돈을 받은 사람과 조각을 가져온 사람은 같을까?")):
                owned=[k for k in keys if r13_has(k)]
                if owned:rows.append(dict(title=title,fact=" / ".join(ROOM13["evidence"][k]["establishes"] for k in owned),question=question,hint="확인한 사실과 그 사실로 주장할 수 있는 범위를 나누어 보자.",keys=owned))
        return rows

label r13_q1_patrol:
    call r13_lines([("dad","미지근했다고 하셨지요. 등 안도 직접 보셨습니까?"),
        ("resident_lamplighter","2일 밤 첫 순찰 때 받침이 흔들려서 뚜껑을 열었어요. 조각은 안에 있었어요. 틈에 끈도 없었고요."),
        ("dad","따뜻했다는 것과 직접 확인한 것은 따로 적겠습니다.")],"q1v:patrol")
    $ r13_grant(["L15"],"초롱에게 첫 순찰의 관찰을 물었다")
    return

label r13_q1_removal:
    call r13_lines([("dad","다음 순찰 때는 어땠습니까?"),
        ("resident_lamplighter","그날 밤 마지막 순찰에서, 맞은편을 보니 짐수레 바퀴가 턱에 걸렸어요. 부리가 도왔고요. 곧 등 위로 빛나는 조각이 들려 나왔어요."),
        ("resident_lamplighter","얼굴은 안 보였어요. 수리하나 보다 하고 지나쳤죠. 동튼 뒤 다시 가 보니 등 안이 비었어요. 그때 피코를 발견했어요."),
        ("dad","얼굴을 본 건 아니군요. 직접 보신 움직임과 순서를 적겠습니다.")],"q1v:removal")
    $ r13_grant(["L16"],"초롱에게 다음 순찰의 관찰을 물었다")
    return

label r13_q1_buri:
    call r13_lines([("dad","그날 밤, 광장에서 무얼 봤니?"),
        ("buri","수리점 공구를 치우고 돌아가던 길이었어요. 수레 바퀴가 턱에 걸렸어요. 제가 밀어 드렸어요. 실룩 씨였어요."),
        ("dad","얼굴을 직접 봤니?"),("buri","네. 바로 앞에서요. 그 뒤 실룩 씨가 3번 등 앞에서 일하고 내려올 때까지 봤어요."),
        ("dad","중간에 다른 사람이 올라갔을 수도 있을까?"),("buri","아니요. 자리를 비우지 않았어요. 그런데 몸하고 뚜껑에 가려 손 안은 안 보였어요.")],"q1v:buri")
    $ r13_grant(["L17"],"부리의 얼굴 확인과 연속 관찰")
    return

label r13_q1_receipt:
    call r13_lines([("dad","아이들 빵값은 어디서 마련하셨습니까?"),
        ("resident_siluk","백 부인에게 물건을 팔았소. 빚부터 갚으라 할 줄 알았는데 돈을 주더군."),
        ("dad","정산한 기록을 봐도 되겠습니까?"),("resident_siluk","여기 있소. 제값 받고 판 거요."),
        (None,"쪽지에는 3일 해 질 녘, 거래 27번, 두 냥이라고 쓰여 있었다. 자기 소유 조각 한 점을 판다는 조건도 있었다.")],"q1v:receipt")
    $ r13_grant(["L19"],"실룩이 직접 내놓은 대금 쪽지")
    return

label r13_q1_argument_conclude:
    menu:
        "실룩이 허락 없이 가져갔습니다.":
            $ _q1_final="correct"
        "실룩은 사람을 죽이려 했습니다.":
            $ _q1_final="over"
        "온도를 잰 우박의 책임입니다.":
            $ _q1_final="weak"
        "아직 더 따져 보겠습니다.":
            return False
    call screen r13_confirm("입증된 결론이면 회의를 마친다. 근거가 부족하거나 틀린 결론이면 오답 1회로 센다. 현재 %d / 3회."%r13_q1_formal_errors() if r13_q1_hard() else "지금까지 제시한 근거와 이 결론으로 회의를 마친다.","이 결론으로 마친다","회의에서 더 생각한다")
    if not _return:
        return False
    $ r13_debate_pick=_q1_final
    if _q1_final=="correct" and r13_debate_ready("Q1"):
        call r13_lines([("neoul","톡이 가져갔다는 혐의는 거두겠소. 실룩이 허락 없이 꺼내 팔았다는 것으로 정리하겠소."),
            ("resident_tok","고맙습니다. 하지만 그 등 밑에 있던 사람을 생각하면… 마음이 편하지는 않네요.")],"q1v:conclusion")
        return True
    if _q1_final=="over":
        call r13_lines([("neoul","조각을 가져갔다는 것과 죽일 생각이었다는 것은 다른 말이오. 그 결론을 뒷받침할 근거를 듣지 못했소.")],"q1v:over")
    elif _q1_final=="weak":
        call r13_lines([("neoul","온도를 쟀다는 것만으로 조각을 가져갔다고 확정할 수는 없소.")],"q1v:weak")
    elif r13_q1_hard():
        call r13_lines([("neoul","그 결론까지 이어지는 근거를 듣지 못했소. 확인한 사실만으로 그 주장이 성립하는지 다시 따져 보시오.")],"q1h:incomplete")
    else:
        call r13_lines([("neoul","그 결론까지 이어지는 근거를 듣지 못했소. 확인한 부분은 남기되 처분은 그대로 두겠소.")],"q1v:incomplete")
    if r13_q1_hard():
        $ r13_q1_record_error(dict(sid="conclusion",supports=[],choices=[_q1_final],failed="conclusion"))
        call r13_q1_error_notice
    else:
        $ r13_debate_close("Q1","final_unproved")
    return False

label r13_q1_argument_failure:
    call r13_lines([("neoul","이 회의에서 톡의 처분을 바꾸지는 않겠소."),(None,"톡이 끌려가며 수리점 쪽을 돌아보았다.")],"q1v:failure")
    return

label r13_q1_public_recovery:
    if r13_q1_v2():
        call r13_lines([("dad","팔았다는 조각이 지금 어디에 있습니까?"),("resident_siluk","백 부인 창고에 있소. 밑에 광장 3이라는 이름표가 있소."),
            ("resident_madam","…확인만 하세요."),(None,"사람들이 보는 앞에서 조각을 꺼냈다. 톡이 이름표와 장부를 대조했다."),
            ("resident_tok","제가 3번 등에 넣은 조각이 맞아요.")],"q1v:public-recovery")
        $ r13_grant(["L09"],"회의 뒤 공개 확인한 창고 조각")
        $ r13_edit(flags=[f for f in room13.get("flags",[]) if f!="tok_detained"])
    return
