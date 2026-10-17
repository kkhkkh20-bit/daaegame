# 0.19.17 단서 줄기와 확인 단계 (소유자 2026-10-17)
#   "방금 겪은 일이 다음 대화에 반영되어야 한다. 지나간 이야기를 하면 안 된다. 지나간 선택지는 빠지거나
#    혼잣말로 넘어간다. 분기마다 그 사람이 얻은 정보에 따라 대사가 바뀌어야 한다."
#
# 줄기(thread): 하나의 의문이 풀려 가는 순서. 단계 n은 "n번째 사실까지 확인했다"는 뜻이고, 0은 아무것도 모른다.
#   단계는 깃발·기록·읽은 질문에서 그때그때 계산한다(저장에 따로 쓰지 않는다). 어느 경로로 알았든 같은 단계가 된다.
#   r13_thread("mom",[(id, test(state), "확인한 사실", "다음 의문"), ...])
#
# 조건(cond): None(항상) / 함수(state)->bool / dict
#   {"thread":"mom","min":2,"max":3}  줄기 단계 범위(max 생략 = 끝까지)
#   {"has":["E18"]}  깃발·기록·읽은 질문 가운데 모두 있음      {"not":["chorong_dead"]}  하나도 없음
#   {"case":"occurred"}  사건 상태      {"all":[cond, ...]}  모두      {"any":[cond, ...]}  하나라도
#
# 질문(ROOM13["topics"][key])에 붙이는 칸
#   "steps": cond           이 조건일 때만 목록에 나온다. 이야기가 지나가면 빠진다(읽었어도).
#   "variants": [(cond, lines), ...]   처음 물을 때, 지금 아는 것에 맞는 첫 갈래의 대사.
#   "again": [(cond, lines), ...]      읽은 질문을 다시 누를 때, 지금 시점에서 그 인물이 하는 말.
#   "recap": "생각"         again이 맞지 않을 때 아빠의 혼잣말 한 줄(괄호 없이 적는다).
#   읽은 질문은 날짜가 지나도 가로줄을 친 채 같은 자리에 남는다. 이야기가 지나간 질문(steps 밖)만 빠진다.
#
# 증거 반응: R13_REACTIONS[(person, key)] = [(cond, lines), ...]
#   그 인물이 일반 답("답할 근거가 없다" 류)만 하던 조합에서, 맞은 부분과 남은 빈칸을 알려 주는 답.
default r13_reaction_seen = None

init 180 python:
    R13_THREADS={}
    R13_REACTIONS={}

    def r13_thread(name,steps):
        R13_THREADS[name]=list(steps)

    def r13_known_keys(s):
        return set(s.get("flags",[]))|set(s.get("evidence",[]))|set(s.get("read_topics",[]))

    def r13_thread_step(name,state=None):
        s=(store.room13 or {}) if state is None else state
        best=0
        for i,step in enumerate(R13_THREADS.get(name,[]),1):
            try:ok=bool(step[1](s))
            except Exception:ok=False
            if ok:best=i
        return best

    def r13_thread_row(name,state=None):
        """(확인한 사실, 다음 의문) at the current step, or None before the first step."""
        n=r13_thread_step(name,state)
        if not n:return None
        step=R13_THREADS[name][n-1]
        return step[2],step[3]

    def r13_cond(cond,state=None):
        s=(store.room13 or {}) if state is None else state
        if cond is None:return True
        if callable(cond):
            try:return bool(cond(s))
            except Exception:return False
        if "thread" in cond:
            n=r13_thread_step(cond["thread"],s)
            if n<cond.get("min",0):return False
            if cond.get("max") is not None and n>cond["max"]:return False
        known=None
        if "has" in cond or "not" in cond:known=r13_known_keys(s)
        if "has" in cond and not all(k in known for k in cond["has"]):return False
        if "not" in cond and any(k in known for k in cond["not"]):return False
        if "case" in cond and s.get("case_state")!=cond["case"]:return False
        if "all" in cond and not all(r13_cond(c,s) for c in cond["all"]):return False
        if "any" in cond and not any(r13_cond(c,s) for c in cond["any"]):return False
        return True

    def r13_pick(rows,state=None):
        for cond,lines in rows or []:
            if r13_cond(cond,state):return lines
        return None

    def r13_topic_ok(spec,state=None):
        return r13_cond(spec.get("steps"),state)

    # ---- question list: drop questions the story has passed, keep read ones (struck through) in place
    _r13_thread_topics=r13_topics
    def r13_topics(person):
        rows=[(k,t) for k,t in _r13_thread_topics(person) if r13_topic_ok(t)]
        s=store.room13 or {}
        shown={k for k,_ in rows}
        read=[k for k in s.get("read_topics",[]) if k not in shown and k in ROOM13["topics"]
            and ROOM13["topics"][k].get("npc")==person and not ROOM13["topics"][k].get("special")
            and r13_topic_ok(ROOM13["topics"][k])]
        if not read:return rows
        # A read question vanished only because its day passed or because reading it set its own hiding flag.
        # Ask the earlier layers again with those two limits lifted, so every other rule still applies.
        saved={}
        try:
            for k in read:
                t=ROOM13["topics"][k];saved[k]=(t.get("day"),t.get("not_flags"))
                own=set(t.get("flags",[]))|{"topic:"+k}
                t["day"]=[1,99]
                t["not_flags"]=[f for f in t.get("not_flags",[]) if f not in own]
            back={k for k,_ in _r13_thread_topics(person)}
        finally:
            for k,(day,nf) in saved.items():
                t=ROOM13["topics"][k]
                if day is None:t.pop("day",None)
                else:t["day"]=day
                if nf is None:t.pop("not_flags",None)
                else:t["not_flags"]=nf
        return rows+[(k,ROOM13["topics"][k]) for k in read if k in back]

    # ---- first reading: the variant that matches what Dad and the resident know now
    _r13_thread_topic_lines=r13_conversation_topic_lines
    def r13_conversation_topic_lines(key):
        spec=ROOM13["topics"].get(key,{})
        lines=r13_pick(spec.get("variants"))
        return list(lines) if lines is not None else _r13_thread_topic_lines(key)

    # ---- asking a read question again: what the resident says now, or Dad's own recap
    def r13_topic_again_lines(key):
        spec=ROOM13["topics"].get(key,{})
        lines=r13_pick(spec.get("again"))
        if lines is not None:return list(lines)
        if spec.get("recap"):return [("dad","("+spec["recap"]+")",{"thought":True})]
        return None

    # ---- presenting: a specific answer where the resident would only give a generic one
    def r13_generic_present_texts(person):
        texts={"전에 보여 준 내용은 기억합니다. 다른 사실이 확인되면 다시 이야기하죠.","그 내용은 제가 확인해 드릴 수 없습니다."}
        r=R13_RESIDENTS.get(person,{})
        if r.get("unrelated"):texts.add(r["unrelated"])
        return texts

    _r13_thread_present=r13_present
    def r13_present(person,key,identity=False):
        result=_r13_thread_present(person,key,identity)
        rows=R13_REACTIONS.get((person,key))
        if not rows:return result
        generic=len(result)==1 and result[0][0]==person and result[0][1] in r13_generic_present_texts(person)
        if not generic:return result
        lines=r13_pick(rows)
        return list(lines) if lines is not None else result
