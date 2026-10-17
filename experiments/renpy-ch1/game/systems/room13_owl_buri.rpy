# Dialogue and reactions that make what Dad said and confirmed stay with people
# (owner's reinforcement plan, 0.18.17). No attitude, morality or forgiveness scores.
#   부엉이 할아버지 alive: the glove (JSON owl_glove), the threshold on day 2, the omen on day 3 evening.
#   부리: cold after the case → an asserted innocence is answered as a father's word →
#         a record that separates the arm and head wounds revises his judgment, not his feelings.
#   백 부인's ledger: after her first answer Dad chooses to check, to ask in private, or to name 서리.
#   톡: a short follow-up only if Dad had sided with the accusation and the accusation fell.
init 118 python:
    ROOM13["evidence"]["J14"]=dict(id="J14",name="백 부인의 설명",kind="증언",
        establishes="백 부인은 장부에 적힌 상자 일부가 이미 나갔다고 설명했다.",
        does_not_establish="백 부인의 말이다. 현물이나 운반 기록으로 확인된 것은 아니다.",scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"]["J14"]="resident_madam"
    R13_RECORD_SHORT["J14"]="백 부인의 설명"

    def _r13_ob_topic(npc,title,day,need=(),not_flags=(),flags=(),lines=(),state=None):
        spec=dict(npc=npc,title=title,day=list(day),need=list(need),not_flags=list(not_flags),give=[],flags=list(flags),lines=list(lines))
        if state:spec["state"]=state
        return spec
    ROOM13["topics"].update({
        # B: the talk the respected request makes room for.
        "owl_old_case":_r13_ob_topic("resident_owlgp","예전 조사 이야기를 들을 수 있겠습니까?",(3,4),need=["owl_threshold_respected"],flags=["owl_old_case_heard"],
            state={"victim_state":["alive","protected"]},lines=[
            ("dad","예전에 기록하시던 조사 이야기를 들을 수 있겠습니까?"),
            ("resident_owlgp","그때는 나도 충분히 확인했다고 생각했소."),
            ("dad","지금은 다르게 생각하십니까?"),
            ("resident_owlgp","확인한 것과 믿은 것을…… 같은 칸에 적어 놓았더구려.")]),
        # 부리 after the case: Dad's word without a record.
        "buri_assert":_r13_ob_topic("buri","“다람이가 그랬을 리 없습니다.”",(5,7),not_flags=["buri_revised"],flags=["buri_heard_assert"],
            state={"case_state":["occurred"],"victim_state":["dead"]},lines=[
            ("buri","아이가 할아버지를 때렸다면서요."),
            ("dad","다람이가 그랬을 리 없어."),
            ("buri","아버지니까 그렇게 말할 수 있겠죠.")]),
        # 백 부인: the approach after her first answer (systems/room13_ledger.rpy sets the flag).
        "ledger_madam:approach":_r13_ob_topic("resident_madam","장부 이야기를 이어 간다",(3,14),need=["madam_ledger_answered"]),
        # 톡: only if Dad sided with the accusation, and the accusation was later dropped.
        "tok_after_doubt":_r13_ob_topic("resident_tok","그날 일을 다시 이야기한다",(4,14),need=["tok_hostile","tok_cleared"]),
    })
    R13_TOPIC_LABELS.update({"ledger_madam:approach":"r13_ledger_madam_approach","tok_after_doubt":"r13_tok_after_doubt"})

    _r13_ob_present=r13_present
    def r13_present(person,key,identity=False):
        s=store.room13
        if person=="buri" and key=="E35" and r13_has("E35") and not r13_has("buri_revised") and s.get("victim_state")=="dead":
            _r13_ob_present(person,key,identity)
            r13_flag("buri_revised")
            return [("buri","팔을 다친 것하고…… 머리를 다친 건 다른 때라는 거죠?"),
                ("dad","확인된 건 여기까지야."),
                ("buri","수리한 흔적은 봐드릴게요."),
                ("buri","다람이한테는…… 아직 무슨 말을 해야 할지 모르겠어요.")]
        if person=="buri" and key=="E17" and r13_has("E17") and s.get("victim_state")=="dead" and not r13_has("buri_hurt_past"):
            _r13_ob_present(person,key,identity)
            r13_flag("buri_hurt_past")
            return [("buri","누명을 풀려고 할아버지의 지난 일까지 전부 꺼내야 해요?"),
                ("dad","……이 기록을 어디까지 쓸지는 아직 정하지 않았어.")]
        if person=="resident_madam" and key=="H1" and r13_has("H1") and not r13_has("madam_ledger_answered") and not r13_has("ledger_counted"):
            result=_r13_ob_present(person,key,identity)
            r13_flag("madam_ledger_answered")
            return [("resident_madam","그건 지난 장부예요. 지금 물건과는 다를 수 있죠.")]+[l for l in result if "오래된 장부" not in l[1]]
        return _r13_ob_present(person,key,identity)

# ---- arrival scenes (called from r13_w1c_events) ----
label r13_owl_events:
    $ _d,_p,_loc=room13["day"],room13["period"],room13["location"]
    call r13_reinspect_events
    if _d==2 and _p==1 and _loc=="hall" and room13["victim_state"]!="dead" and not r13_has("ev_owl_threshold_done"):
        call r13_owl_threshold
    if _d==3 and _p==2 and _loc=="dining" and room13["case_state"]=="pending" and not r13_has("ev_owl_omen_done"):
        call r13_owl_omen
    return

label r13_owl_threshold:
    $ r13_flag("ev_owl_threshold_done")
    call r13_ev_here("calm")
    call r13_lines([(None,"13호 쪽 복도에서 부엉이 할아버지가 쪼그려 앉아 문턱 아래를 들여다보고 있었다."),
        ("resident_owlgp","잠깐 기다려 주시오. 문턱을 손보는 중이오.")],"owl:threshold:open")
    $ _ow_loop=True
    while _ow_loop:
        $ _ow_loop=False
        menu:
            "“수리가 끝나면 다시 오겠습니다.”":
                call r13_lines([("resident_owlgp","고맙소. ……내일 시간이 나면 내 쪽에서 이야기하리다.")],"owl:threshold:respect")
                $ r13_flag("owl_threshold_respected")
            "“문턱이 어떻게 됐습니까?”" if not r13_has("owl_threshold_asked"):
                call r13_lines([("resident_owlgp","문턱이 들떴소. 아이가 걸려 넘어지기 전에 고쳐 두려는 거요.")],"owl:threshold:ask")
                $ r13_flag("owl_threshold_asked")
                $ _ow_loop=True
            "“제 방 앞을 왜 막으십니까?”":
                call r13_lines([(None,"복도를 지나던 손님 둘이 걸음을 멈추고 우리 쪽을 보았다."),
                    ("resident_owlgp","……알겠소. 지나가시오."),
                    (None,"할아버지는 공구를 챙겨 계단 쪽으로 물러났다.")],"owl:threshold:press")
                $ r13_flag("owl_threshold_pressed")
    return

label r13_owl_omen:
    $ r13_flag("ev_owl_omen_done")
    call r13_ev_here("night")
    call r13_lines([(None,"식당 구석 자리에서 부엉이 할아버지가 다람이에게 손짓했다."),
        ("resident_owlgp","그걸 좀…… 문 옆에 놓아 주겠니."),
        ("daram","장갑이요?"),
        ("resident_owlgp","그래. 장갑."),
        (None,"할아버지는 숟가락을 내려놓고 한동안 눈을 감았다. 손등의 깃털이 가늘게 떨렸다."),
        ("resident_owlgp","……오늘은 일찍 올라가야겠군."),
        ("granny","오늘은 방에서 쉬세요. 제가 가져다드릴게요."),
        (None,"할머니가 할아버지의 팔을 받쳐 계단 쪽으로 갔다. 익숙한 손길이었다.")],"owl:omen")
    $ r13_flag("owl_omen_seen")
    return

# ---- 백 부인: how Dad handles the ledger after her first answer ----
label r13_ledger_madam_approach:
    menu:
        "“어느 항목이 달라졌습니까?”":
            call r13_lines([("resident_madam","이 상자들은 이미 나갔어요."),
                (None,"백 부인은 장부의 한 줄을 손톱으로 짚었다.")],"ledger:madam:check")
            $ r13_grant(["J14"],"백 부인이 장부를 보며 한 설명")
        "“먼저 설명부터 듣고 싶습니다.”":
            call r13_lines([("resident_madam","그럼 우리끼리 정리할 수 있겠네요."),
                ("resident_madam","그 장부를 다른 데 내놓지 않는다면, 창고 물건 값은 반만 받지요.")],"ledger:madam:private")
            menu:
                "“그 조건이면 받겠습니다.”":
                    call r13_lines([("resident_madam","말이 통하네요. 장부는 가지고 계세요. 보여 주지만 않으면 돼요.")],"ledger:madam:deal")
                    $ r13_flag("madam_deal")
                "“그 조건은 받을 수 없습니다.”":
                    call r13_lines([("resident_madam","그럼 할 말 없네요.")],"ledger:madam:nodeal")
        "“서리에게도 확인받겠습니다.”":
            call r13_lines([("resident_madam","이름이 적힌 사람들까지 모두 부를 생각인가요?")],"ledger:madam:seori")
            $ r13_flag("madam_told_seori")
    $ r13_finish_topic("ledger_madam:approach")
    return

# ---- 톡: Dad's own earlier words ----
label r13_tok_after_doubt:
    call r13_lines([("resident_tok","그날 너울 말이 맞을 수도 있다고 하셨지요. 이제는 어떻게 생각하세요?")],"tok:doubt:open")
    menu:
        "“그 의심은 거두겠습니다.”":
            call r13_lines([("resident_tok","……알겠어요. 그 말은 기억해 둘게요.")],"tok:doubt:withdraw")
            $ r13_flag("tok_doubt_withdrawn")
        "“확인된 것만 기록하겠습니다.”":
            call r13_lines([("resident_tok","기록은 기록이지요. 나도 그 정도는 압니다.")],"tok:doubt:record")
    $ r13_finish_topic("tok_after_doubt")
    return

init 119 python:
    # 다람이 reacts only to what she was part of or was told (systems/room13_night_talk.rpy).
    R13_NIGHT_TALKS_EXTRA=[
        ("night:owl","장갑을 찾아 준 할아버지 이야기를 한다",lambda:r13_has("owl_glove_seen") and store.room13.get("case_state")=="pending",[
            ("dad","장갑 찾아 준 할아버지 기억나지?"),
            ("daram","할아버지는 내가 물어보면 다 대답해 줬어."),
            ("dad","그래. 꼼꼼한 분 같더라.")]),
        ("night:buri","부리를 만난 이야기를 한다",lambda:store.room13.get("case_state")=="occurred" and store.room13.get("trial_ended") and store.room13.get("daram_state") in ("with_dad","rescued") and (r13_has("buri_revised") or r13_has("buri_heard_assert")),[
            ("dad","오늘 부리 아저씨를 만났어."),
            ("daram","부리 아저씨는 아직 나랑 말하기 싫은가 봐."),
            ("dad","……아저씨한테도 시간이 필요할 거야.")]),
        ("night:helping","오늘 같이 한 일을 이야기한다",lambda:store.room13.get("day",1)>=R13_WEEK2_DAY and any(r13_has(f) for f in ("w2_bell_rung","share_patients","share_children","share_lottery")),[
            ("dad","오늘 짐 나르는 거 같이 해 줘서 고마워."),
            ("daram","오늘은 내가 도와준 거지?"),
            ("dad","응. 네가 도와줬어.")]),
    ]
    for _k,_t,_c,_l in R13_NIGHT_TALKS_EXTRA:
        ROOM13["topics"][_k]=dict(npc="daram",title=_t,day=[1,14],need=["lodging"],give=[],flags=[],lines=list(_l))
        R13_NIGHT_TALK_COND[_k]=_c
