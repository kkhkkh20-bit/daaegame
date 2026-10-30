# Residents with nothing to say right now (owner 2026-10-22: "대화하거나 제시할 게 없으면
# 혼잣말로 넘어가도 괜찮고, 기본 인사말이라도"). Tapping such a resident does not open the
# question sheet: the first tap of the day plays that resident's greeting
# (v111/newworld/greetings.json), later taps a short thought from Dad.
# "Nothing to say" = no option of the current scene for this person here, no unread follow-up
# question, and no specific evidence reaction left to see. Family members always open as before.
init 336 python:
    R13_GREETINGS=json.load(renpy.file("v111/newworld/greetings.json")) if renpy.loadable("v111/newworld/greetings.json") else {}
    R13_IDLE_THOUGHTS=(
        "지금은 더 물어볼 게 없겠지.",
        "바쁜 사람을 자꾸 붙잡지 말자. 물을 게 생기면 다시 오자.",
        "새로 알게 된 게 생기면 그때 다시 말을 걸어 보자.",
    )
    R13_IDLE_FAMILY=("daram","mom","dad")
    # 아빠가 반말로 인사하는 아이들(첫 인사 줄에만 쓴다).
    R13_IDLE_KIDS=("bami","resident_kongi","resident_tosil","resident_somi","v111_siluk_child","v111_child")
    def r13_v111_is_kid(person):
        return person in R13_IDLE_KIDS or str(person).startswith("kid_")

    def r13_v111_has_business(person):
        here=store.room13["location"]
        if any(o.get("person")==person and o.get("location")==here for o in r13_v111_binding().get("options",[])):return True
        if any(not r13_followup_read(s["id"]) for s in r13_v111_followups(person)):return True
        for spec in R13_REACTIONS.get("present",[]):
            if spec["person"]==person and r13_v111_owned(spec["evidence"]) and r13_reaction_day_ok(spec) and not r13_reaction_seen(spec):
                return True
        return False

    # 0.20.6 (Codex R01): a reaction set is read by its own id, so the 6th-day lines do not mark
    # the different 7th-day lines for the same person and record as read, and a generic answer
    # before a meeting does not mark the meeting-dependent set. The old per person/record flag
    # (saves before 0.20.6) stands for the earliest set of that pair only.
    def r13_reaction_spec_id(spec):
        return "%s:%s:%s:%s"%(spec["person"],spec["evidence"],(spec.get("days") or [1])[0],spec.get("after_meeting") or "")
    def r13_reaction_seen(spec):
        if r13_v111_value("reacted:"+r13_reaction_spec_id(spec)):return True
        if r13_v111_value("reacted:%s:%s"%(spec["person"],spec["evidence"])):
            pair=[s for s in R13_REACTIONS.get("present",[]) if s["person"]==spec["person"] and s["evidence"]==spec["evidence"]]
            return spec is min(pair,key=lambda s:((s.get("days") or [1])[0],bool(s.get("after_meeting"))))
        return False

    def r13_v111_idle_ok(person):
        return r13_v111_active() and person not in R13_IDLE_FAMILY and not r13_v111_has_business(person)

    _r13_idle_present_reaction=r13_v111_present_reaction
    def r13_v111_present_reaction(person,shown):
        key=shown[5:] if isinstance(shown,str) and shown.startswith("V111:") else shown
        for spec in R13_REACTIONS.get("present",[]):
            # Same choice as r13_v111_present_reaction: the first set for today whose lines play.
            if spec["person"]==person and spec["evidence"]==key and r13_reaction_day_ok(spec) and r13_reaction_packets(spec["lines"]):
                r13_v111_set("reacted:"+r13_reaction_spec_id(spec),True)
                break
        return _r13_idle_present_reaction(person,shown)

    def r13_v111_idle_lines(person):
        day=(store.room13 or {}).get("day",1)
        name=next((n for n,p in MS14_SPEAKERS.items() if p==person),None)
        rows=R13_GREETINGS.get(person) or []
        if name and rows and not r13_v111_value("greeted:%s:%s"%(day,person)):
            r13_v111_set("greeted:%s:%s"%(day,person),True)
            seen=r13_v111_value("greeted_count:"+person) or 0
            r13_v111_set("greeted_count:"+person,seen+1)
            row=rows[-1]  # the working line; greetings (row 0) read as if meeting anew
            # 2026-10-30 눈가림 플레이(3~4일): 누르면 상대가 한 줄로 끊어 「이유 없는 거절」로 읽혔다(초롱·우박·백 부인·바둑이·토실).
            # 소유자 2026-10-27 「사람을 누르면 주고받기가 먼저」. 아빠가 먼저 한마디 건네고(dad), 상대는 하던 일과 그 까닭으로 받는다.
            out=[]
            if row.get("dad"):
                out.append(("dad",row["dad"],dict(expression="neutral",pose="neutral")))
            out.append(r13_nw_added_line(dict(speaker=name,text=row["text"],expression=row.get("expression","neutral"),kind="dialogue")))
            return out
        count=(r13_v111_value("idle_count") or 0)
        r13_v111_set("idle_count",count+1)
        return [r13_nw_added_line(dict(speaker="아빠",text=R13_IDLE_THOUGHTS[count%len(R13_IDLE_THOUGHTS)],kind="thought"))]

# First meeting (owner 2026-10-22: "다들 나를 본것처럼 이야기하는데?"): a resident who has not yet
# spoken with Dad in this run greets him as a stranger; their own greeting starts after that.
# "Met" is the game's own encounter record (r13_met_people(), filled when someone speaks).
init 346 python:
    _r13_met_line_art=r13_ep_line_art
    def r13_ep_line_art(packet):
        who=packet[0] if packet else None
        if isinstance(who,str) and who not in ("dad",):
            # Owner 2026-10-22 dialogue review: whoever speaks is in the scene. A resident who
            # talks but was not staged walks in (alive and not departed: r13_v111_join filters).
            # Family keep their own location rules; a voice tagged as off-screen stays away.
            try:
                if (r13_v111_active() and who not in ("daram","mom") and who in CAST
                        and who not in (store.room13["v111"].get("people") or [])
                        and not r13_offscreen_voice(R13_NAMES.get(who,who))):
                    r13_v111_join([who])
            except Exception:
                pass
        return _r13_met_line_art(packet)
    _r13_met_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        # 0.20.7 (play review D23-03): right after a scene's conversation with this person, a
        # second tap keeps the moment instead of a stock greeting or "don't keep busy people".
        scene=(store.room13.get("v111") or {}).get("scene")
        if scene and r13_v111_value("talked:%s:%s"%(scene,person)):
            # 2026-10-29 눈가림 플레이: 2일 식당에서 나비를 다시 누르면 「그 일부터 하자」만 나와, 「그 일」이 무엇인지
            # (벤치·마른 천) 몰라 물건을 이것저것 눌렀다. 지금의 「생각」(할 행동 한 문장)이 있으면 이어 붙인다.
            goal=globals().get("r13_v111_goal",lambda:"")() or ""
            rows=[("dad","(방금 하던 이야기가 있다. 그 일부터 하자.)",dict(no_lead=True,thought=True,expression="thinking",pose="thinking"))]
            if goal:
                rows.append(("dad","("+goal+")",dict(no_lead=True,thought=True,expression="thinking",pose="thinking")))
            return rows
        day=(store.room13 or {}).get("day",1)
        if person not in r13_met_people() and person in R13_GREETINGS and not r13_v111_value("greeted:%s:%s"%(day,person)):
            name=next((n for n,p in MS14_SPEAKERS.items() if p==person),None)
            if name:
                # Owner 2026-10-22: "처음에 다 인사하는것도 웃기고". A stranger does not greet; they
                # glance over and keep working. Their own lines start once they have spoken with Dad.
                day=(store.room13 or {}).get("day",1)
                r13_v111_set("greeted:%s:%s"%(day,person),True)
                # 2026-10-30 눈가림 플레이(4일 광장 도토): 처음 보는 사람을 누르면 「힐끗 보고는 하던 일을 계속한다」 지문 뒤
                # 아빠 속말만 나와, 소유자 2026-10-27 「사람을 누르면 주고받기가 먼저, 말 없이 지문만 흐르면 안 된다」에 어긋났다.
                # 아빠가 먼저 인사하고 상대가 첫 인사(row 0, 아는 사이처럼 들리는 사람은 first)로 받는다.
                first=R13_GREETINGS[person][0]
                hello="안녕. 아저씨는 여관에 묵어." if r13_v111_is_kid(person) else "안녕하세요. 여관 13호에 묵는 사람입니다."
                return [("dad",hello,dict(expression="neutral",pose="neutral")),
                        r13_nw_added_line(dict(speaker=name,text=first.get("first") or first["text"],expression=first.get("expression","neutral"),kind="dialogue"))]
        return _r13_met_idle_lines(person)

# Evidence with no fitting reaction (owner 2026-10-22: "다람이에게 편지 보내주기했는데 아무반응 없이
# 조사하기 화면으로 이동함"): Daram answers in her own voice; anyone else without a reply gets a short
# thought from Dad instead of a passing notification.
init 347 python:
    R13_DARAM_PRESENT={
        "E01":("엄마 편지잖아. 나 벌써 다 외웠어!","anxious"),
    }
    R13_DARAM_GENERIC=(
        # 0.20.9 (검토 기록 4): 다람이 따로 있던 동안의 조사를 다 본 것처럼 말하지 않는다.
        ("그거? 어느 부분을 보면 돼?","flustered"),
        ("음…… 그건 아빠가 더 잘 알잖아.","neutral"),
        ("그거 아빠 수첩에 적어 둬. 나중에 같이 보자.","neutral"),
    )
    R13_PRESENT_NOTHING=("지금 이걸 보여 줘도 더 들을 말은 없겠다.","이건 다른 사람에게 물어봐야겠다.")
    _r13_present_fallback=r13_v111_present_reaction
    def r13_v111_present_reaction(person,shown):
        lines=_r13_present_fallback(person,shown)
        if lines:return lines
        key=shown[5:] if isinstance(shown,str) and shown.startswith("V111:") else shown
        if person=="daram":
            # 편지의 출처가 밝혀진 뒤에는 '엄마 편지'라고 부르지 않는다(위조 확인·엄마의 설명).
            if key=="E01" and (r13_v111_value("forgery_confirmed") or r13_v111_value("mother_q_return")):
                return [r13_nw_added_line(dict(speaker="다람",text="우리가 받고 온 편지잖아. ……엄마가 쓴 게 아니었지.",expression="anxious",kind="dialogue"))]
            text,exp=R13_DARAM_PRESENT.get(key) or R13_DARAM_GENERIC[sum(ord(c) for c in str(key))%len(R13_DARAM_GENERIC)]
            return [r13_nw_added_line(dict(speaker="다람",text=text,expression=exp,kind="dialogue"))]
        text=R13_PRESENT_NOTHING[sum(ord(c) for c in str(key))%len(R13_PRESENT_NOTHING)]
        return [r13_nw_added_line(dict(speaker="아빠",text=text,kind="thought"))]

# 0.20.9 (검토 기록 5): 그날 첫 인사는 인물의 기본 생활 대사(greetings.json)를 쓴다. 본편에서 그 인물이
# 감독·진료 호출·운반처럼 다른 일을 맡고 있으면 예전 일과 대사 대신 지금 처지를 짧은 지문으로 보인다.
# 새 말투를 지어내지 않도록 대사가 아닌 지문으로 둔다. 첫 만남·방금 대화 처리는 그대로다.
init 348 python:
    R13_IDLE_BUSY_TEXT={
        "silluk_supervision":"%s 감독 아래 제자리를 지키고 있다. 지금은 말을 아낀다.",
        "teacher_supervision":"%s 감독 아래 제자리를 지키고 있다. 지금은 말을 아낀다.",
        "medical_call":"%s 환자 곁으로 가는 길이다. 고개만 짧게 끄덕인다.",
    }
    R13_IDLE_BUSY_DEFAULT="%s 맡은 일에서 손을 떼지 못한다. 눈인사만 건넨다."
    _r13_state_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        busy=r13_v111_value("busy:"+person)
        scene=(store.room13.get("v111") or {}).get("scene")
        talked=scene and r13_v111_value("talked:%s:%s"%(scene,person))
        name=next((n for n,p in MS14_SPEAKERS.items() if p==person),None)
        if busy and name and not talked and person in r13_met_people():
            day=(store.room13 or {}).get("day",1)
            key="greeted_busy:%s:%s:%s"%(day,person,busy)
            if not r13_v111_value(key):
                r13_v111_set(key,True)
                r13_v111_set("greeted:%s:%s"%(day,person),True)
                josa="은" if (0xAC00<=ord(name[-1])<=0xD7A3 and (ord(name[-1])-0xAC00)%28) else ("는" if 0xAC00<=ord(name[-1])<=0xD7A3 else "은")
                text=R13_IDLE_BUSY_TEXT.get(busy,R13_IDLE_BUSY_DEFAULT)%(name+josa)
                return [r13_nw_added_line(dict(speaker=None,text=text,kind="narration"))]
        return _r13_state_idle_lines(person)

# 0.20.9 (조연 검토 4): 5일 회의에서 "사람이 보이면 부르겠소. 손부터 대진 않겠소."라고 약속한 경로.
# 6~10일 그날 첫 인사에서 돌목은 다친 팔을 몸에 붙인 채, 손 대신 먼저 부른다.
init 349 python:
    _r13_guard_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        day=(store.room13 or {}).get("day",1)
        if (person=="guard" and 6<=day<=10 and r13_v111_value("meeting:gate_post")=="win"
                and not r13_v111_value("busy:guard") and person in r13_met_people()
                and not r13_v111_value("greeted:%s:%s"%(day,person))):
            r13_v111_set("greeted:%s:%s"%(day,person),True)
            return [r13_nw_added_line(dict(speaker=None,text="돌목은 다친 팔을 몸 쪽에 붙인 채 서 있다. 발소리에 손을 뻗으려다 멈추고, 먼저 부른다.",kind="narration")),
                    r13_nw_added_line(dict(speaker="돌목",text="거기 누구요. ……아, 당신이군.",expression="neutral",kind="dialogue"))]
        return _r13_guard_idle_lines(person)

# 0.20.10 (4~14일 리뷰 P07): 다람을 눌렀는데 지금 물을 것도 새 질문도 없으면 빈 질문 화면만 열렸다.
# 장면마다 처음 한 번은 다람이 먼저 짧게 대답한다. 자료를 보여 주는 화면은 그대로 열린다.
init 350 python:
    R13_DARAM_HELLO=("응? 아빠, 왜?","나 여기 있어.")
    def r13_v111_daram_hello_due():
        scene=(store.room13.get("v111") or {}).get("scene")
        if r13_v111_has_business("daram") or r13_v111_value("daram_hello:%s"%scene):return False
        return bool(scene)
    def r13_v111_daram_hello():
        scene=(store.room13.get("v111") or {}).get("scene")
        r13_v111_set("daram_hello:%s"%scene,True)
        n=r13_v111_value("daram_hello_count") or 0
        r13_v111_set("daram_hello_count",n+1)
        return [r13_nw_added_line(dict(speaker="다람",text=R13_DARAM_HELLO[n%len(R13_DARAM_HELLO)],expression="neutral",kind="dialogue"))]

# 0.20.10 (4~14일 리뷰: 4일 초소 비명 뒤 일반 인사, 7일 빨래터 추궁 직후 "또 오셨어요?"):
# 지금 장면에 함께 있는 사람은 할 말이 없어도 평소 생활 인사를 하지 않는다. 아빠가 지금 할 일을 떠올린다.
init 351 python:
    # 사건이 막 일어났거나 추궁·청문이 이어지는 장면만(그 밖에는 소유자 결정대로 그날 첫 인사).
    R13_TENSE_SCENES={"MS14_D04_S03","MS14_D07_S01","MS14_D07_S02","MS14_D07_S04","MS14_D11_S04","MS14_D12_S04","MS14_D13_C"}
    _r13_scene_idle_lines=r13_v111_idle_lines
    def r13_v111_idle_lines(person):
        guidance=r13_day2_idle_guidance(person)
        if guidance:return guidance
        v=store.room13.get("v111") or {}
        scene_people=v.get("people") or []
        if v.get("scene") in R13_TENSE_SCENES and person in scene_people and person in r13_met_people():
            return [r13_nw_added_line(dict(speaker="아빠",kind="thought",text="지금은 인사를 나눌 때가 아니다. 이 일부터 하자."))]
        return _r13_scene_idle_lines(person)
