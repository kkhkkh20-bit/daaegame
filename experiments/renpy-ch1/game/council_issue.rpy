# A narrow social-inference prototype. Physical proof and willingness to speak
# remain separate; winning this issue never establishes innocence or a culprit.
default village_testimonies = {}
default council_marks = []
default council_claim_index = 0
default council_result = "new"
default council_questions = []
default council_history = []
default council_relationship_memories = {}
default council_confirmed_support = []
default council_support_listens = 0

init 26 python:
    COUNCIL_ISSUE = json.load(renpy.file("council-issue.json"))

    def council_reset():
        store.council_marks=[]
        store.council_claim_index=0
        store.council_result="new"
        store.council_questions=[]
        store.council_history=[]
        store.council_relationship_memories={}
        store.council_confirmed_support=[]
        store.council_support_listens=0

    def council_mark(key):
        if key and key not in store.council_marks:
            store.council_marks.append(key)

    def council_resolved():
        marks=set(store.council_marks)
        return (all(x in marks for x in ("sealed_money","uncorroborated_count"))
            or all(x in marks for x in ("old_room","other_trace")))

    def council_evidence(key):
        # Unknown or stale cards cannot establish a fact through a hidden menu.
        if key not in store.source_inventory:return None
        spec=COUNCIL_ISSUE["evidence"].get(key)
        if spec:
            council_mark(spec["mark"])
            if council_resolved():store.council_result="resolved"
        return spec

    def council_listen():
        index=min(store.council_claim_index,len(COUNCIL_ISSUE["claims"])-1)
        store.council_claim_index=min(index+1,len(COUNCIL_ISSUE["claims"])-1)
        if index==len(COUNCIL_ISSUE["claims"])-1:
            store.council_result="adverse"
            if "adverse" not in store.council_history:store.council_history.append("adverse")
        return COUNCIL_ISSUE["listen"][index]

    def council_resume():
        # Keep earned proof/context and relationship memories after adjournment.
        if store.council_result in ("adverse","adjourned"):
            store.council_claim_index=0
            store.council_result="open"
            store.council_history.append("resumed")
        elif store.council_result=="new":store.council_result="open"

    def council_testimonies():
        records=getattr(store,"village_testimonies",{})
        if not isinstance(records,dict):return []
        return [dict(record,id=key) for key,record in records.items()
            if record.get("kind") in ("bed_context","access_context")]

    def council_public_allowed(record):
        return record.get("permission") in (True,"allowed","public","granted")

    def council_share_testimony(record):
        speaker=record.get("speaker","unknown")
        key="shared:"+record["id"]
        memories=store.council_relationship_memories.setdefault(speaker,[])
        first_share=key not in memories
        if first_share:
            memories.append(key)
            memories.append("public_permission_kept" if council_public_allowed(record) else "private_statement_exposed")
        # Context can slow a premature decision once. An opinion about spare beds
        # or a witness's ordinary kindness is never a physical-proof substitute.
        if first_share:
            store.council_claim_index=max(0,store.council_claim_index-1)
        council_mark("context:"+record["id"])

    def council_confirm_support(person,evidence):
        if evidence not in store.source_inventory:return False
        if evidence not in TIMELINE["support"][person]["ids"]:return False
        if person not in store.council_confirmed_support:
            store.council_confirmed_support.append(person)
            village_relationship("support_"+person,[person],2)
        return True

screen council_issue():
    modal True
    default ready = False
    timer .15 action SetScreenVariable("ready",True)
    add Solid("#100c09b8")
    frame:
        xpos 80 ypos 100 xsize 1120 ysize 510 padding (28,22)
        background Solid("#241d18f5")
        text "원탁 · 아직 결정되지 않은 의심" size 20 color "#b8a789"
        text COUNCIL_ISSUE["title"] ypos 38 size 34 color "#ffdc91"
        text COUNCIL_ISSUE["scope"] ypos 91 xsize 1045 size 18 color "#c6b699"
        $ current = COUNCIL_ISSUE["claims"][council_claim_index]
        text source_name(current["speaker"])+" · "+current["line"] ypos 143 xsize 1040 size 26 color "#f2e5ce"
        text current["reason"] ypos 235 size 19 color "#c1ab8f"
        text ("확인한 근거가 쌓였습니다. 단정을 멈출 수 있습니다." if council_resolved() else "의견은 기울고 있습니다. 근거를 내거나, 더 묻거나, 다음 말을 들을 수 있습니다.") ypos 278 xsize 1020 size 19 color "#dbbe84"
        if council_marks:
            text "이 쟁점에서 확인한 점: "+str(len(council_marks))+"개 · 재조사 후에도 남습니다" ypos 315 size 18 color "#b2c5bd"
        hbox:
            xpos 0 ypos 396 spacing 16
            textbutton "근거 제시" xsize 240 ysize 58 action Return("present") sensitive ready
            textbutton "더 묻기" xsize 240 ysize 58 action Return("ask") sensitive ready
            textbutton "듣기" xsize 240 ysize 58 action Return("listen") sensitive ready
            textbutton "재조사" xsize 240 ysize 58 action Return("return") sensitive ready

label council_open_issue:
    $ council_resume()
    $ stage,place = "meeting","여관 원탁"
    $ clock_text = village_clock()+" · 논의"
    $ source_camera,source_night = "stage",None
    hide visitor
    window hide
    scene black with Dissolve(.12)
    $ source_pulse(False)
    $ source_score("inn_meet")
    $ renpy.pause(.3,hard=True)
    scene bg council with Dissolve(.2)
    show screen round_table
    if "opened" not in council_history:
        call source_lines([["wanggu","주인부터 확인하겠습니다. 다른 의견이 있으면 지금 말하세요."],["det1","아빠, 저 사람 말만 계속 듣고 있어."],["det0","그래. 우리도 확인한 걸 말하자."]],"COUNCIL_OPEN")
        $ council_history.append("opened")
    while not council_resolved():
        call screen council_issue
        $ council_action = _return
        if council_action == "return":
            $ council_result = "adjourned"
            call source_lines(COUNCIL_ISSUE["missing"],"COUNCIL_ADJOURN")
            hide screen round_table
            return "investigate"
        elif council_action == "listen":
            $ council_listen_lines = council_listen()
            call source_lines(council_listen_lines,"COUNCIL_LISTEN")
            if council_result == "adverse":
                hide screen round_table
                return "investigate"
        elif council_action == "ask":
            $ council_question_key = "claim:"+str(council_claim_index)
            if council_question_key not in council_questions:
                call source_lines(COUNCIL_ISSUE["claims"][council_claim_index]["ask"],"COUNCIL_ASK")
                $ council_questions.append(council_question_key)
            else:
                call source_lines([["wanggu","설명은 들었습니다. 확인한 근거가 있으면 보여주십시오." ]],"COUNCIL_ASK_REPEAT")
        elif council_action == "present":
            $ council_sources = [dict(label="물증·기존 수첩",key="physical")]+[dict(label=source_name(t.get("speaker","?"))+"의 말",key=t["id"]) for t in council_testimonies()]+[dict(label="돌아가기",key="cancel")]
            if not council_testimonies():
                $ council_source_key = "physical"
            else:
                call screen source_choice("무엇을 근거로 말할까?",council_sources)
                $ council_source_key = _return["key"]
            if council_source_key == "physical":
                call screen source_evidence(present=True)
                $ council_ev = _return
                if council_ev != "cancel":
                    $ council_spec = council_evidence(council_ev)
                    if council_spec:
                        call source_lines(council_spec["lines"],"COUNCIL_EVIDENCE_"+council_ev)
                    else:
                        call source_lines([["wanggu","그 기록과 방을 숨긴 일이 어떻게 연결되는지 아직 모르겠습니다."],["det0","다른 기록도 확인하죠."]],"COUNCIL_UNRELATED")
            elif council_source_key != "cancel":
                $ council_record = next(t for t in council_testimonies() if t["id"]==council_source_key)
                $ council_share = True
                if not council_public_allowed(council_record):
                    call screen source_choice("공개해도 된다는 허락을 받지 않았다.",[dict(label="이름을 밝히고 말한다",key="share"),dict(label="지금은 말하지 않는다",key="keep")])
                    $ council_share = _return["key"] == "share"
                if council_share:
                    $ council_share_testimony(council_record)
                    call source_lines([["det0",source_name(council_record.get("speaker","?"))+" 씨에게 들었습니다. "+str(council_record.get("claim",""))],["wanggu","방을 숨긴 사정과는 관계가 있겠군요. 돈을 누가 옮겼는지까지 본 말은 아닙니다."]],"COUNCIL_CONTEXT")
                    if not council_public_allowed(council_record):
                        call source_lines([["det1","그 얘기, 여기서 해도 된다고 했어?"],["det0","…그건 내가 먼저 물었어야 했어."]],"COUNCIL_PRIVATE_EXPOSED")
    $ council_result = "resolved"
    call source_lines(COUNCIL_ISSUE["resolved"],"COUNCIL_RESOLVED")
    hide screen round_table
    return "resolved"
