# Dialogue routing only. Existing encounter records remain the source of truth.
default r13_carriage_snack = False
default r13_first_encounter = False
default r13_opening_lines = []

init 58 python:
    import json as r13_opening_json
    R13_OPENING_SCENES = r13_opening_json.load(renpy.file("room13-dialogue-openings.json"))
    # The selectable line is what Dad intends to say, not an instruction to
    # the player. Authored notice/opening dialogue and meeting flags stay intact.
    R13_APPROACH_SPEECH = {
        "resident_tori":"천 끝을 좀 잡아 드릴까요?",
        "resident_bori":"이 장작도 함께 올려 드릴까요?",
        "resident_yeoni":"안녕하세요. 옷을 수선하고 계십니까?",
        "nabi":"지금 식사를 할 수 있을까요?",
        "buri":"부품을 잠깐 구경해도 되겠습니까?",
        "resident_kongi":"가게로 가려면 어느 쪽입니까?",
        "doto":"다 쓰셨으면 잠깐 여쭤봐도 될까요?",
        "resident_kkwak":"여기 물통 놓으시겠어요? 비켜 드릴게요.",
        "granny":"안녕하세요. 이 편지를 받고 찾아왔습니다.",
        "resident_librarian":"마을에 관한 책을 찾아볼 수 있을까요?",
        "resident_owlgp":"안녕하세요. 등을 살펴보고 계십니까?",
        "resident_teacher":"여기가 학교입니까? 길을 좀 여쭤봐도 될까요?",
        "karo":"까로 씨, 잠깐 여쭤봐도 되겠습니까?",
        "resident_nero":"이 길로 가면 어디가 나옵니까?",
        "resident_seol":"방금 울린 종은 무슨 뜻입니까?",
        "resident_ppul":"말씀 끝나셨으면 잠깐 여쭤봐도 될까요?",
        "resident_tok":"부품 내려놓으신 뒤에 잠깐 괜찮으실까요?",
        "bami":"제 목소리 들립니까? 여기서 이야기할게요.",
        "resident_sling":"제 아내의 우편에 관해 여쭤봐도 될까요?",
        "resident_momo":"이 물건은 어디에 쓰는 겁니까?",
        "resident_ttadak":"일 끝나시면 잠깐 이야기 나눌 수 있을까요?",
        "resident_piko":"지금 그림을 좀 봐도 될까요?",
        "resident_mungchi":"상자 옮기는 걸 도와드릴까요?",
        "resident_madam":"다 세신 뒤에 잠깐 여쭤봐도 될까요?",
        "resident_siluk":"수레 세우신 뒤에 길을 좀 여쭙겠습니다.",
        "neoul":"이쪽으로 지나가도 괜찮습니까?",
        "resident_musoe":"안녕하세요. 길을 좀 여쭤봐도 될까요?",
        "resident_somi":"신발이 불편하니?",
        "resident_seori":"안녕하세요. 서류 다 보신 뒤에 잠깐 괜찮으실까요?",
        "resident_ubak":"종이 날아가지 않게 잡아 드릴까요?",
        "resident_nubi":"세탁을 맡길 수 있을까요?",
        "resident_eunho":"물건을 구경해도 되겠습니까?",
        "resident_guseul":"정리 끝나시면 잠깐 이야기 나눌 수 있을까요?",
        "resident_badook":"이 길로 지나가도 됩니까?",
        "resident_lamplighter":"등을 점검하고 계십니까? 방해되지 않게 기다릴게요.",
        "seryeon":"제 아내 앞으로 온 우편을 확인할 수 있을까요?",
    }

    def r13_conversation_opening(person, first):
        spec = R13_OPENING_SCENES["first_meetings"].get(person)
        if spec is None:
            return []
        if not first:
            return spec["revisit"]
        state = store.room13
        early = state["day"] <= 3 and state["case_state"] == "pending"
        if not early:
            return spec["late"]
        with_child = state["daram_state"] in ("with_dad", "rescued")
        return spec["early" if with_child else "early_solo"]

    def r13_conversation_topic_lines(key):
        state = store.room13
        # Optional companion speech does not alter topic visibility or evidence.
        with_child = state["daram_state"] in ("with_dad", "rescued")
        variants = R13_OPENING_SCENES["with_daram"]
        if with_child and key in variants:
            return variants[key]
        return ROOM13["topics"][key]["lines"]


    def r13_resident_notice(person):
        spec = R13_OPENING_SCENES["first_meetings"][person]
        state = store.room13
        special = R13_OPENING_SCENES["special_notices"]
        if person == "buri" and state["victim_state"] == "dead":
            return special["buri_bereaved"]
        if person == "bami" and r13_has("bami_pressured"):
            return special["bami_pressured"]
        early = state["day"] <= 3 and state["case_state"] == "pending"
        if not early:
            return spec["notice_late"]
        with_child = state["daram_state"] in ("with_dad", "rescued")
        return spec["notice_child" if with_child else "notice_solo"]

# Seeing a resident does not record a meeting, grant evidence, or advance time.
# Separate return labels keep existing saved call stacks stable.
label r13_notice_before_talk(person):
    if person not in R13_OPENING_SCENES["first_meetings"] or person in r13_met_people():
        return True
    $ r13_notice_approach = r13_calendar_approach(person)
    call screen r13_resident_approach(r13_notice_approach,person)
    if not _return:
        return False
    if not r13_has("noticed:" + r13_calendar_key(person)):
        $ r13_notice_rows = r13_resident_notice(person)
        call r13_lines(r13_notice_rows, "notice:resident:" + person) from r13_notice_lines_return
        $ r13_flag("noticed:" + r13_calendar_key(person))
    return True

screen r13_resident_approach(approach,person=None):
    modal True
    zorder 40
    style_prefix "r13"
    default ready=False
    timer .25 action SetScreenVariable("ready",True)
    $ target=person or r13_target
    $ choices=[((R13_APPROACH_SPEECH.get(target,approach) if r13_calendar_phase()=="arrival" else "지금 잠깐 말씀을 여쭤봐도 될까요?"),Return(True),False),("지금은 말을 걸지 않는다",Return(False),False)]
    use r13_question_list(target,r13_conversation_pose(target),R13_NAMES[target]+"에게 말 걸기",choices,ready,return_action=Return(False))
    use r13_toolbar(investigate_action=Return(False),person=target,mode="talk",ready=ready)


init 75 python:
    R13_CALENDAR = R13_OPENING_SCENES["calendar"]

    def r13_calendar_phase():
        s = store.room13
        if s["day"] >= 11:
            return "crisis"
        if s.get("trial_ended") or s.get("trial_result", "pending") != "pending":
            return "after_trial"
        if s["case_state"] == "occurred":
            return "occurred"
        if s["case_state"] == "prevented":
            return "prevented"
        if s["day"] >= 4:
            return "before_case"
        return "arrival" if s["day"] == 1 else "settling"

    def r13_calendar_profile(person):
        s = store.room13
        phase = r13_calendar_phase()
        phase = "settling" if phase == "arrival" else phase
        spec = dict(R13_CALENDAR[person][phase])
        day = str(store.room13["day"])
        daily = R13_OPENING_SCENES["calendar_daily"][person]
        if day in daily:
            spec["reply"] = daily[day]
        if person == "buri" and s["case_state"] == "prevented" and phase == "after_trial":
            spec.update(action="부리는 할아버지의 공구와 자기 부품을 따로 놓았다.", reply="할아버지 건 직접 말씀 듣고 옮길 거예요. 살아 계신데 제가 다 정해 버리면 또 혼나니까요.")
        ready = R13_OPENING_SCENES["calendar_ready"].get(person)
        if store.room13["day"] >= 8 and ready and r13_has(ready[0]):
            spec.update(action=ready[1], reply=ready[2])
            if day in daily:
                spec["reply"] += " " + daily[day]
            elif phase == "crisis":
                spec["reply"] += " " + R13_OPENING_SCENES["calendar_ready_late"][person]
        if person == "bami" and r13_has("bami_protected"):
            spec.update(action="밤이는 문을 살핀 뒤 자리에 앉았다. 전처럼 내 발소리에 곧바로 몸을 숨기지는 않았다.", reply="자리는 확인했어요. 제가 여기 있다는 말은 제가 할게요. 찾아 주셨다고 대신 정하시진 말고요.")
            if day in daily:
                spec["reply"] = daily[day]
            elif phase != "occurred":
                spec["reply"] += " " + R13_CALENDAR[person][phase]["reply"]
        elif person == "bami" and r13_has("bami_pressured"):
            spec.update(action="밤이는 내 뒤를 확인했다. 나는 복도 쪽으로 몸을 비켰다.", reply="제 이름이 전해진 뒤에 누가 왔는지도 봐 주세요. 말씀하실 때만 조심하면 저는 계속 혼자 숨겨야 하니까요.")
            if day in daily or phase != "occurred":
                spec["reply"] = daily.get(day, R13_CALENDAR[person][phase]["reply"])
        if person == "buri" and r13_has("buri_refused"):
            spec["reply"] += " 그때 하신 말씀은 기억해요. 제가 나가 달라고 했던 것도요. 달라진 기록이 있으면 그 이야기부터 해 주세요."
        # Evening describes stopping/rechecking the current work, not an invented new job.
        if store.room13["period"] >= 2:
            spec["action"] += " 어두워진 자리에서는 손을 멈추고 하던 것을 다시 살폈다."
        return spec

    def r13_calendar_key(person):
        s = store.room13
        own = sorted(k for k in s.get("read_topics", []) if ROOM13["topics"].get(k, {}).get("npc") == person)
        ready = R13_OPENING_SCENES["calendar_ready"].get(person)
        signature = [s.get("case_state"), s.get("victim_state"), s.get("trial_result"), s.get("daram_state")]
        if ready:
            signature.append(r13_has(ready[0]))
        if person == "bami":
            signature.extend(r13_has(k) for k in ["bami_pressured", "bami_protected", "bami_identity_leaked"])
        if person == "buri":
            signature.append(r13_has("buri_refused"))
        digest = r13_hashlib.sha256(r13_opening_json.dumps(signature, ensure_ascii=False).encode("utf-8")).hexdigest()[:16]
        return "calendar:" + person + ":" + str(s["day"]) + ":" + str(s["period"]) + ":" + r13_calendar_phase() + ":" + digest

    def r13_calendar_activity(person):
        if not store.room13 or person not in R13_CALENDAR:
            return R13_RESIDENTS.get(person, {}).get("activity", "")
        if r13_calendar_phase() == "arrival":
            return R13_RESIDENTS.get(person, {}).get("activity", "봉투의 수취인을 확인하고 있다.")
        return r13_calendar_profile(person)["action"]

    def r13_calendar_outcome_line(person):
        s = store.room13
        variants = R13_OPENING_SCENES["calendar_outcome"].get(person, {})
        # No verdict is inferred from the date. Release/rescue needs actual saved state.
        if s["daram_state"] == "rescued":
            return variants.get("rescued")
        if s["daram_state"] == "held":
            return variants.get("held")
        if s.get("trial_result") in ("cleared", "culprit_proven"):
            return variants.get("free")
        return None

    def r13_conversation_opening(person, first):
        spec = R13_OPENING_SCENES["first_meetings"].get(person)
        if spec is None:
            return []
        s = store.room13
        phase = r13_calendar_phase()
        with_child = s["daram_state"] in ("with_dad", "rescued")
        # Original day-one introductions remain; pressure/bereavement never uses tourist greetings.
        if phase == "arrival" and s["victim_state"] != "dead" and not (person == "bami" and r13_has("bami_pressured")):
            if first:
                return spec["early" if with_child else "early_solo"]
            work = "life:" + person + ":work"
            if work in s.get("read_topics", []) and person in R13_OPENING_SCENES["calendar_memory"]:
                return [[None, r13_calendar_activity(person)], [person, R13_OPENING_SCENES["calendar_memory"][person]]]
            return spec["revisit"]
        current = r13_calendar_profile(person)
        rows = [[None, current["action"]]]
        if first:
            rows += spec["late"]
        rows.append([person, current["reply"]])
        work = "life:" + person + ":work"
        stamp = s.get("dialogue_dates", {}).get(work)
        if not first and stamp and stamp["day"] == s["day"] - 1 and person in R13_OPENING_SCENES["calendar_memory"]:
            rows.append([person, R13_OPENING_SCENES["calendar_memory"][person]])
        outcome = r13_calendar_outcome_line(person)
        if outcome and not first:
            rows.append([person, outcome])
        return rows

    def r13_resident_notice(person):
        s = store.room13
        spec = R13_OPENING_SCENES["first_meetings"][person]
        if person == "buri" and s["victim_state"] == "dead":
            return [[None, r13_calendar_profile(person)["action"]]]
        if r13_calendar_phase() == "arrival":
            return spec["notice_child" if s["daram_state"] in ("with_dad", "rescued") else "notice_solo"]
        return [[None, r13_calendar_profile(person)["action"]]]

    def r13_calendar_approach(person):
        if r13_calendar_phase() == "arrival":
            return R13_OPENING_SCENES["first_meetings"][person]["approach"]
        return "하던 일을 잠깐 멈출 수 있는지 물으며 다가간다"

    def r13_conversation_topic_lines(key):
        s = store.room13
        spec = ROOM13["topics"][key]
        person = spec["npc"]
        with_child = s["daram_state"] in ("with_dad", "rescued")
        base = R13_OPENING_SCENES["with_daram"].get(key, spec["lines"]) if with_child else spec["lines"]
        if person not in R13_CALENDAR:
            return base
        ordinary = key == "life:" + person + ":work"
        crisis = key in ("life:" + person + ":crisis", "life:" + person + ":after")
        read = key in s.get("read_topics", [])
        current = r13_calendar_profile(person)
        if ordinary and read:
            memory = R13_OPENING_SCENES["calendar_memory"].get(person)
            rows = [[None, current["action"]]]
            if memory:
                rows.append([person, memory])
            rows.append([person, current["reply"]])
            return rows
        if crisis:
            rows = [[None, current["action"]], [person, current["reply"]]]
            outcome = r13_calendar_outcome_line(person)
            if outcome:
                rows.append([person, outcome])
            if with_child:
                rows += R13_OPENING_SCENES["calendar_companion"].get(person, [])
            return rows
        if read:
            # Fixed evidence testimony is replayed as a dated record, not said again as today's event.
            stamp = s.get("dialogue_dates", {}).get(key)
            when = (str(stamp["day"]) + "일째 " + ("오전", "오후", "저녁", "늦은 저녁")[stamp["period"]]) if stamp else "이전에"
            rows = [[None, when + " 들은 이야기를 수첩에서 다시 확인했다. 아래는 당시의 기록이다."]]
            for who, text in [row[:2] for row in base]:
                name = R13_NAMES.get(who, "기록")
                rows.append([None, "(당시 기록 · " + name + ") " + text])
            return rows
        if ordinary and r13_calendar_phase() != "arrival":
            return [[None, current["action"]]] + base
        return base

    def r13_calendar_topic_title(key, spec):
        person = spec["npc"]
        if person in R13_CALENDAR and key in ("life:"+person+":work", "life:"+person+":after", "life:"+person+":crisis"):
            if key in store.room13.get("read_topics", []):
                return "그 뒤에 달라진 일을 묻는다"
        return spec["title"]


    def r13_calendar_topic_seen(key, spec):
        s = store.room13
        if key not in s.get("read_topics", []):
            return False
        person = spec["npc"]
        if person not in R13_CALENDAR or key not in ("life:"+person+":work", "life:"+person+":after", "life:"+person+":crisis"):
            return True
        view = s.get("dialogue_views", {}).get(key)
        if not view or view.get("context") != r13_calendar_key(person):
            return False
        return key != "life:"+person+":work" or view.get("mode") == "followup"
