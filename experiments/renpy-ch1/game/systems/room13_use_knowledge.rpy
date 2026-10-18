# Using what Dad knows without saying it (owner, 0.18.19).
#   1 Play dumb: after learning Granny reads guests' letters, Dad can answer her as usual and watch
#     where she puts letters. Telling her he knows is a separate, later choice; once she knows,
#     a planted letter no longer fools her.
#   2 A favour that tests testimony: 도토 says he saw the whole hallway; standing in the same spot,
#     the corner hides the stairs. This narrows his testimony; it says nothing about a culprit.
#   3 The warning envelope: open it at the lamp box alone (as before), or keep it sealed and open it
#     with 초롱, who can then say it is the envelope he kept, seal intact. Reading never removes
#     the record; only what can be shown changes.
init 123 python:
    for _key,_name,_kind,_est,_not in (
        ("J17","도토가 선 자리에서 본 복도","증언","도토가 그날 선 자리에 다시 서 보니, 복도 모퉁이에 가려 계단 첫 칸부터는 보이지 않았다.","그 사이에 누가 지나갔는지는 이것으로 알 수 없다."),
        ("J18","초롱이 함께 연 봉투","증언","초롱은 자기가 점검함에 맡아 둔 봉투가 맞고, 봉인이 온전한 채로 아빠와 함께 열었다고 확인했다.",""),
        ("H16","할머니의 접수대 서랍","관찰기록","손님 편지 이야기가 나오자 할머니는 접수대 아래 서랍을 한 번 열었다 닫았다.","서랍 안에 무엇이 있는지는 보지 못했다."),
    ):
        ROOM13["evidence"][_key]=dict(id=_key,name=_name,kind=_kind,establishes=_est,does_not_establish=_not,scenes=[],current_run_only=True,retained_on_show=True)
    ROOM13["evidence_sources"].update(J17="doto",J18="resident_lamplighter")
    R13_RECORD_SHORT.update(J17="도토의 시야",J18="함께 연 봉투",H16="접수대 서랍")

    ROOM13["activities"]["warning"]["title"]="점검함의 봉투를 그 자리에서 뜯어 읽는다"
    ROOM13["activities"]["warning"]["not_flags"]=list(ROOM13["activities"]["warning"].get("not_flags",[]))+["warning_sealed_held"]
    ROOM13["activities"]["warning_keep"]=dict(place="square",title="점검함의 봉투를 봉한 채 챙긴다",day=[1,13],need=["warning_location"],
        not_flags=["warning_sealed_held","E18"],flags=["warning_sealed_held"],give=[],cost=0,lines=[
        (None,"봉투 겉에는 우리 가족 이름이 아내 글씨로 적혀 있었다. 봉인은 온전했다. 뜯지 않고 품에 넣었다.")])
    R13_CONTEXT_ACTIVITIES[("square","lamp")]=tuple(R13_CONTEXT_ACTIVITIES.get(("square","lamp"),()))+("warning_keep",)

    ROOM13["topics"].update({
        "granny_letter_ask":dict(npc="granny",title="할머니와 이야기를 나눈다",day=[2,4],need=["know_granny_reads"],not_flags=["granny_dumb_done","granny_knows_found_out"],give=[],flags=[],lines=[],state={"case_state":["pending"]}),
        "granny_letter_confront":dict(npc="granny",title="“손님 편지를 열어 보게 하셨지요.”",day=[2,7],need=["H9"],not_flags=["granny_knows_found_out"],give=[],flags=["granny_knows_found_out","warning_exposed"],lines=[
            ("dad","슬링에게 손님 편지를 열어 보게 하셨지요."),
            ("granny","……누가 그런 말을 하던가요."),
            ("granny","손님이 걱정돼서 그런 거예요. 무슨 소식이 오는지는 알아야 할 것 아니에요.")]),
        "doto_view_claim":dict(npc="doto",title="“그날 복도는 어디까지 보였니?”",day=[5,13],need=[],give=[],flags=["doto_view_claim"],lines=[
            ("dad","그날 복도는 어디까지 보였니?"),
            ("doto","복도 끝까지 다 보였습니다. 누가 지나갔으면 제가 봤을 거예요.")],case="occurred"),
        "doto_view_test":dict(npc="doto",title="“그 자리에 다시 서서 봐 줄래?”",day=[5,13],need=["doto_view_claim"],give=["J17"],flags=[],lines=[
            ("dad","그날 서 있던 자리에 다시 서서, 계단 쪽을 봐 줄래?"),
            (None,"도토가 13호 문 앞에 섰다. 고개를 몇 번 기울였다."),
            ("doto","……계단 첫 칸부터는 모퉁이에 가려서 안 보이네요."),
            ("doto","문 앞은 확실히 봤습니다. 그건 변하지 않아요.")],case="occurred"),
        "warning_open_with":dict(npc="resident_lamplighter",title="“이 봉투를 같이 열어 주시겠습니까?”",day=[1,13],need=["warning_sealed_held"],not_flags=["E18"],give=["E18","J18"],flags=[],lines=[
            ("dad","점검함에서 꺼낸 봉투입니다. 뜯지 않았습니다. 같이 열어 주시겠습니까?"),
            ("resident_lamplighter","제가 맡아 둔 봉투가 맞아요. 봉인도 그대로네요."),
            (None,"초롱이 보는 앞에서 봉투를 열었다. 안쪽에 우리 가족끼리만 쓰던 매듭이 지어져 있었다."),
            (None,"「나는 너희한테 오라는 편지를 쓴 적 없어. 내가 어디로 가는지 여관에는 말하지 마. 답장은 등불 고치는 사람을 통해 보내 줘. 누구든 혼자 만나러 가지는 말고.」")]),
        "warning_open_alone":dict(npc="daram",title="봉투를 우리끼리 열어 본다",day=[1,13],need=["warning_sealed_held"],not_flags=["E18"],give=["E18"],flags=["warning_opened_alone"],lines=[
            ("daram","엄마 글씨다. 열어 봐도 돼?"),
            (None,"봉투를 열었다. 「나는 너희한테 오라는 편지를 쓴 적 없어. 내가 어디로 가는지 여관에는 말하지 마. 답장은 등불 고치는 사람을 통해 보내 줘. 누구든 혼자 만나러 가지는 말고.」")]),
    })
    R13_TOPIC_LABELS["granny_letter_ask"]="r13_granny_letter_ask"

    _r13_uk_topics=r13_topics
    def r13_topics(person):
        rows=_r13_uk_topics(person)
        return [(k,s) for k,s in rows if k!="warning_open_alone" or r13_home_with_daram()]

    _r13_uk_present=r13_present
    def r13_present(person,key,identity=False):
        if person=="granny" and key=="E18" and r13_has("E18") and not r13_has("J18"):
            lines=_r13_uk_present(person,key,identity)
            return [("granny","그 봉투가 정말 그분이 쓴 건지 누가 알아요? 뜯어진 봉투면 누구든 바꿔 넣을 수 있잖아요.")]+list(lines)
        return _r13_uk_present(person,key,identity)

label r13_granny_letter_ask:
    call r13_lines([("granny","아이 엄마한테서 소식은 없었나요?")],"granny:dumb:ask")
    menu:
        "“아직 기다리고 있습니다.”":
            call r13_lines([("dad","아직 기다리고 있습니다."),
                ("granny","그래요……. 무슨 소식이 오면 나한테도 알려 줘요."),
                (None,"할머니는 대답을 듣고 접수대 아래 서랍을 한 번 열었다 닫았다.")],"granny:dumb:play")
            $ r13_grant(["H16"],"할머니와 엄마 소식을 이야기하다 봄")
        "“편지 이야기는 다음에 하겠습니다.”":
            # 0.18.41 (owner): postponing is not giving up. Nothing is marked done, so the topic
            # stays open and the same conversation can be had later (H16 is not lost).
            call r13_lines([("granny","그래요. 바쁘시겠지요.")],"granny:dumb:later")
            return
    $ r13_flag("granny_dumb_done")
    $ r13_finish_topic("granny_letter_ask")
    return
