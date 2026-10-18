# First-case questions, optional debrief and native save checkpoints.
# No completion gate, automatic evidence, time refund or cross-run unlock.
default r13_q1_checkpoint_saved = False
default r13_q1_checkpoint_failed = False
default persistent.r13_q1_results = {}

init 181 python:
    import uuid as r13_q1_uuid

    ROOM13["topics"]["q1:review"]=dict(npc="daram",title="광장 회의를 돌아볼까?",day=[4,14],need=["lt_done"],not_flags=[],give=[],flags=[],lines=[])
    R13_TOPIC_LABELS["q1:review"]="r13_q1_review"

    R13_Q1_QUESTIONS = {
        "s1":("등을 연 사람", "톡 말고도 등을 연 사람이 있었을까?", "등을 열 줄 안다는 것과 실제로 열었다는 것은 다르다.", "3번 등의 안쪽과 뚜껑에 남은 흔적을 다시 살펴볼 수 있다."),
        "s2":("조각이 사라진 시각", "온도를 잰 뒤에도 등은 따뜻했을까?", "당사자의 말과, 그 뒤에 등을 본 사람의 말을 구분해 보자.", "등을 돌보는 초롱이 새벽에 본 것과 온도를 잰 사람의 말을 대조할 수 있다."),
        "s3":("조각의 출처", "팔린 조각이 어디서 나왔는지 확인했을까?", "돈을 주고 샀다는 말은 원래 주인에게 허락받았다는 뜻일까?", "4일 오전과 오후에 백 부인의 창고에서 조각의 표시를 확인할 수 있다. 현장의 끈이나 기록실의 목격담이 있어야 조사를 시작한다."),
        "s4":("계속되는 위험", "다른 곳의 온기도 사라지고 있을까?", "한 사람의 혐의와, 아직 남아 있는 위험은 다른 문제다.", "4일 아침에 확인한 기록실의 상황을 다시 읽어 볼 수 있다."),
        "s5":("노끈의 주인", "현장에 남은 끈은 누구의 끈과 이어질까?", "같은 색의 끈보다, 뜯긴 끝이 서로 맞는지가 중요하다.", "4일 오전과 오후, 입구에서 짐을 묶는 실룩의 끈과 현장에 남은 끈을 대조할 수 있다."),
    }

    def r13_q1_notes():
        if not r13_has("lt_dawn"):return []
        if r13_has("lt_done"):
            return [dict(title="광장 회의 · 돌아보기",fact=r13_q1_summary()[0],
                question=r13_q1_summary()[1],hint=r13_q1_summary()[2],keys=[])]
        rows=[]
        def add(title,fact,question,keys,hint):
            rows.append(dict(title=title,fact=fact,question=question,keys=keys,hint=hint))
        add("3번 등에서 무슨 일이 있었을까?","3번 등이 식었고, 그 밑에서 피코가 쓰러졌다.",
            "등이 식은 까닭과 조각이 사라진 시각은 이어질까?",[k for k in ("L00","L06") if r13_has(k)],
            "이동과 평소 대화로는 시간이 흐르지 않는다. 회의는 4일 오전부터 오후까지 광장에서 열린다. 자거나 시간을 쓰는 선택을 하면 조사 시간이 줄어든다.")
        if r13_has("lt_open"):
            add("톡만 등을 열 수 있었을까?","너울은 등을 열 줄 아는 톡을 의심했다.",R13_Q1_QUESTIONS["s1"][1],
                [k for k in ("L02","L03","L14") if r13_has(k)],R13_Q1_QUESTIONS["s1"][2])
        if r13_has("L03") or r13_has("L05"):
            add("온도를 잰 때와 조각이 사라진 때","우박은 조각을 돌려놨다고 했다." if r13_has("L05") else "등 안에 온도를 적은 쪽지가 남아 있었다.",
                R13_Q1_QUESTIONS["s2"][1],[k for k in ("L03","L05","L06") if r13_has(k)],R13_Q1_QUESTIONS["s2"][2])
        if r13_has("L04"):
            add("뚜껑에 남은 노끈","등 뚜껑 틈에 갈색 짐 노끈이 걸려 있었다.",R13_Q1_QUESTIONS["s5"][1],
                [k for k in ("L04","L07","L08") if r13_has(k)],R13_Q1_QUESTIONS["s5"][2])
        if r13_has("L09"):
            add("창고 조각의 이름표","백 부인 창고의 조각에 ‘광장 3’이라는 이름표가 붙어 있었다.",
                "등의 조각은 어떻게 창고까지 갔을까?",["L09"],R13_Q1_QUESTIONS["s3"][2])
        if r13_has("L10"):
            add("기록실에서 사라진 온기","기록실 난로에서도 조각이 사라졌다.","3번 등에서 벌어진 일과 이어질까?",["L10"],R13_Q1_QUESTIONS["s4"][2])
        return rows

    _r13_q1_notes=r13_first_mystery_notes
    def r13_first_mystery_notes():
        return r13_q1_notes()+_r13_q1_notes()

    def r13_q1_review_rows():
        held=bool((store.room13 or {}).get("debate",{}).get("closed",{}).get("ep1:Q1")) or "Q1" in (store.room13 or {}).get("propositions",[])
        if not held:return []
        return [(sid,r13_debate_is_broken("Q1",sid),text) for sid,text in R13_Q1_QUESTIONS.items()]

    def r13_q1_summary():
        rows=r13_q1_review_rows()
        done=[v[2][0] for v in rows if v[1]]
        left=[v[2][0] for v in rows if not v[1]]
        fact="반박해 바꾼 논점: "+", ".join(done)+"." if done else "회의에서 뒤집은 주장은 없었다." if rows else "회의가 열리기 전에 조사 기한이 지났다."
        gap="입증하지 못한 논점: "+", ".join(left)+"." if left else "주장은 모두 반박했지만 결론을 확정하지 않았다." if not r13_has("lt_solved") and rows else "회의의 결론을 확정했다." if rows else "톡의 혐의와 조각을 가져간 사람을 따질 기회를 놓쳤다."
        result="톡은 풀려났다." if r13_has("tok_cleared") else "톡을 풀어 주게 만들지는 못했다. 반박한 부분은 기록에 남지만, 남은 의심까지 사라진 것은 아니다."
        return fact,gap,result

    def r13_q1_review_lines():
        lines=[(None,t) for t in r13_q1_summary()]
        rows=r13_q1_review_rows()
        unproved=[v for v in rows if not v[1]]
        if unproved:
            held=any(r13_debate_answerable("Q1",r13_debate_statement("Q1",sid)) for sid,_,_ in unproved)
            missing=any(not r13_debate_answerable("Q1",r13_debate_statement("Q1",sid)) for sid,_,_ in unproved)
            if held:lines.append((None,"가지고 있던 자료로 더 따져 볼 수 있는 주장도 남았다."+(" 같은 자료로 회의만 다시 시도할 수 있다." if r13_q1_can_restore("meeting") else "")))
            if missing:lines.append((None,"지금 가진 자료만으로는 연결을 확인하기 어려운 주장도 남았다. 조사를 보완하거나, 이 결과로 이야기를 이어갈 수 있다."))
        lines.append((None,"재시도하면 당시의 시간·소지품·조사 상태로 돌아간다."))
        lines.append((None,"이번 결과는 별도로 보관되어 있다." if r13_q1_can_restore("result") else "이 결과를 남기려면 저장 메뉴에서 직접 저장해 주세요."))
        return lines

    def r13_q1_lamp_aftermath():
        if not r13_has("tok_cleared"):
            return [(None,"톡이 끌려간 뒤에도 3번 등은 식어 있었다. 부리가 빈 작업대를 바라보았다."),
                ("buri","등도 그대로고, 선생님도 안 돌아왔어요.")]
        if not r13_has("madam_store_opened"):
            return [(None,"풀려난 톡이 3번 등의 빈 뚜껑을 닫았다."),
                ("resident_tok","범인은 밝혔지만, 조각은 아직 못 돌려받았어요. 이대로는 등을 데울 수 없어요.")]
        return [(None,"톡이 돌려받은 ‘광장 3’ 조각을 등에 다시 넣었다. 등이 데워졌다. 그런데 숨 몇 번 사이에 온기가 옅어졌다."),
            ("resident_tok","이 조각, 가을엔 밤새 따뜻했어요. 지금은…….")]

    def r13_q1_afterthought():
        if r13_has("lt_solved"):
            return [("dad","(조각을 훔친 사람은 밝혔다. 하지만 이 겨울에 사람들이 온기를 잃는 일까지 끝난 것은 아니다.)",{"thought":True})]
        return [("dad","(밝힌 것과 밝히지 못한 것이 남았다. 내가 모르는 일을 안다고 말할 수는 없다.)",{"thought":True})]

    def r13_q1_checkpoint_slot(kind):
        return (store.room13 or {}).get("q1_checkpoints",{}).get(kind)

    def r13_q1_can_restore(kind):
        slot=r13_q1_checkpoint_slot(kind)
        return bool(slot and renpy.can_load(slot))

    def r13_q1_save_checkpoint(kind):
        if store.r13_q1_checkpoint_saved or store.r13_q1_checkpoint_failed:return
        s=winter_copy.deepcopy(store.room13)
        if not s.get("run_token"):s["run_token"]=r13_q1_uuid.uuid4().hex
        slot="r13q1-"+r13_q1_uuid.uuid4().hex
        s.setdefault("q1_checkpoints",{})[kind]=slot
        store.room13=s
        store.r13_q1_checkpoint_saved=True
        # Native save at an actual interaction restores the entire store and call stack.
        renpy.retain_after_load()
        try:
            renpy.save(slot,extra_info="등 도둑 · "+{"investigation":"조사 다시 보기","meeting":"회의 직전","result":"회의 결과"}[kind])
        except Exception:
            store.r13_q1_checkpoint_saved=False
            store.r13_q1_checkpoint_failed=True
            return
        if kind=="result":
            records=dict(persistent.r13_q1_results or {})
            records[s["run_token"]]=slot
            persistent.r13_q1_results=records
            renpy.save_persistent()

    def r13_q1_previous_result():
        slot=(persistent.r13_q1_results or {}).get((store.room13 or {}).get("run_token"))
        return slot if slot and renpy.can_load(slot) and slot!=r13_q1_checkpoint_slot("result") else None

    def r13_q1_restore_slot(slot):
        if not slot or not renpy.can_load(slot):
            renpy.notify("저장 시점을 찾지 못했습니다. 현재 진행은 그대로입니다.")
            return
        # Discard only the index of later morning checkpoints, as the existing day retry does.
        day=(renpy.slot_json(slot) or {}).get("r13_day",1)
        rec=dict(r13_morning_record())
        if rec.get("token")==store.room13.get("run_token"):
            rec["days"]=[d for d in rec.get("days",[]) if d<=day]
            persistent.r13_mornings=rec
            renpy.save_persistent()
        renpy.load(slot)

    _r13_q1_opening=r13_conversation_opening
    def r13_conversation_opening(person,first):
        if person=="resident_tok" and r13_has("lt_open") and not r13_has("lt_done"):
            return [(person,"너울은 제가 등을 열었다는 말만 되풀이해요. 무엇을 보고 그런 말을 하는지부터 확인해 주세요.")]
        return _r13_q1_opening(person,first)

screen r13_q1_checkpoint_wait(kind):
    # Invisible, one interaction long. No new visual controls or save slots overwrite user saves.
    if not r13_q1_checkpoint_saved and not r13_q1_checkpoint_failed:
        timer .05 action Function(r13_q1_save_checkpoint,kind)
    else:
        timer .05 action Return()

label r13_q1_checkpoint(kind):
    $ r13_q1_checkpoint_saved=False
    $ r13_q1_checkpoint_failed=False
    call screen r13_q1_checkpoint_wait(kind)
    if r13_q1_checkpoint_failed:
        $ renpy.notify("되돌아갈 시점을 저장하지 못했습니다. 저장 메뉴에서 직접 저장할 수 있습니다.")
    return

label r13_q1_menu_scene:
    window hide
    hide r13_visitor
    $ r13_last_partner=None
    $ dialogue_speaker=None
    return

label r13_q1_preflight:
    call r13_q1_hard_rules
    call r13_lines([(None,"회의에서는 지금 가진 자료로 이야기한다. 회의는 4일 오후가 끝나기 전까지 열 수 있다."),(None,"조사나 추리가 끝나지 않았어도 들어갈 수 있다.")],"ep1:preflight")
    call r13_q1_menu_scene
    menu:
        "회의에 들어간다":
            return True
        "조사를 더 한다":
            return False
        "보관한 이전 결과를 본다" if r13_q1_previous_result():
            $ r13_q1_restore_slot(r13_q1_previous_result())
            jump r13_q1_preflight

label r13_q1_review:
    call r13_lines([(None,"수첩을 펼쳤다. 확인한 사실과 아직 답하지 못한 의문을 나누어 적었다.")],"ep1:review:opening")
    call r13_lines(r13_q1_review_lines(),"ep1:review")
label r13_q1_review_menu:
    call r13_q1_menu_scene
    menu:
        "이 결과로 계속한다":
            return
        "남은 논점을 생각한다" if any(not row[1] for row in r13_q1_review_rows()):
            call r13_q1_hints
        "같은 자료로 회의를 다시 한다" if r13_q1_can_restore("meeting"):
            $ r13_q1_restore_slot(r13_q1_checkpoint_slot("meeting"))
        "조사를 다시 살펴본다" if r13_q1_can_restore("investigation"):
            $ r13_q1_restore_slot(r13_q1_checkpoint_slot("investigation"))
    jump r13_q1_review_menu

label r13_q1_hints:
    $ _q1_hint_options=[("어떤 논점을 다시 생각할까?",None)]+[(text[0],sid) for sid,done,text in r13_q1_review_rows() if not done]+[("돌아간다",None)]
    $ _q1_hint=renpy.display_menu(_q1_hint_options)
    if _q1_hint:
        call r13_lines([("dad",r13_q1_question(_q1_hint)[1],{"thought":True}),("dad",r13_q1_question(_q1_hint)[2],{"thought":True})],"ep1:review:thought")
        menu:
            "이 의문으로 다시 생각한다":
                pass
            "구체적인 조사 방향을 본다":
                call r13_lines([(None,r13_q1_question(_q1_hint)[3])],"ep1:review:direction")
    return
