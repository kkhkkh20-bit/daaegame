# Piko discovery precedes public notice; current Chorong questions are not old transcripts.
# Only pure display queries run during prediction. Notice is committed by its label.
init 205 python:
    R13_PIKO_CURRENT_TOPICS = ("lamplighter_guarded", "smalltalk:lamplighter_check")

    def r13_piko_notice_due(state=None):
        s = (store.room13 or {}) if state is None else state
        flags = set(s.get("flags", []))
        day, period = s.get("day", 1), s.get("period", 0)
        return ("lt_dawn" in flags and "lt_q1_notice" not in flags and "lt_done" not in flags
            and (day == 3 or (day == 4 and period <= 1)))

    def r13_piko_notice_here():
        return (r13_piko_notice_due() and (store.room13 or {}).get("location") == "square"
            and not getattr(store, "r13_meeting_active", False))

    def r13_piko_mother_purpose():
        # A commissioned L12 portrait does NOT establish an earlier meeting with Mom.
        if r13_has("L13"):
            return "피코는 아내를 본 적이 있다. 그때 어디서 만났는지 아는 사람을 찾아야 한다. 모인 사람들의 말을 들어 보자."
        return "피코가 남긴 그림과 이야기에 아내의 흔적이 더 있을까. 피코와 지내던 사람들에게 물어봐야겠다."

    def r13_piko_notice_lines(recovery=False):
        when = "오늘" if (store.room13 or {}).get("day") == 4 else "내일"
        if recovery:
            rows = [(None, "광장에 사람들이 모여 있었다. 꺼진 3번 등 이야기가 사람들 사이를 돌았다.")]
        else:
            rows = [(None, "사람들 말이 등 주변에서 겹쳐졌다. ‘톡 씨가 손댄 거 아냐?’ ‘직접 본 사람이 있대?’ 아직은 서로에게 묻는 말뿐이었다.")]
        rows += [(None, "너울이 사람들 사이로 들어와 목소리를 높였다."),
            ("neoul", "3번 등 안의 조각이 없어졌소. %s 아침부터 오후까지 광장에서 이 일을 따져 보겠소. 그날 밤 본 것이 있는 사람은 나오시오." % when, {"expression":"neutral"}),
            ("dad", "피코와 지내던 분들도 모입니까?"),
            ("neoul", "아는 일이 있으면 와서 말하면 되오.", {"expression":"neutral"}),
            ("dad", r13_piko_mother_purpose(), {"thought":True}),
            (None, "나는 사람들이 모인다는 때와 장소를 적었다.")]
        return rows

    # The existing deadline is unchanged; discovering the body is not hearing a notice.
    R13_MEETING_CLOCK = [tuple([row[0], "lt_q1_notice"] + list(row[2:])) if row[0] == "Q1" else row
        for row in R13_MEETING_CLOCK]

    _r13_piko_q1_notes = r13_q1_notes
    def r13_q1_notes():
        rows = _r13_piko_q1_notes()
        if r13_has("lt_q1_notice") or r13_has("lt_done"):
            return rows
        result = []
        for row in rows:
            row = dict(row)
            if row.get("title") == "3번 등에서 무슨 일이 있었을까?":
                row["hint"] = "피코가 남긴 것과 그날 밤을 본 사람들의 이야기를 확인하자. 이동과 평소 대화로는 시간이 흐르지 않는다."
            result.append(row)
        return result

    def r13_piko_chorong_context(key):
        if key not in R13_PIKO_CURRENT_TOPICS or not r13_has("lt_dawn"):
            return None
        # Newly learned observation opens a new current answer, not a rewritten archive.
        known = next((flag for flag in ("L16", "L15", "L06") if r13_has(flag)), "discovery")
        return "piko-after-dawn:v1:" + known

    _r13_piko_topic_context = r13_topic_current_context
    def r13_topic_current_context(key):
        return r13_piko_chorong_context(key) or _r13_piko_topic_context(key)

    def r13_piko_chorong_lines(key):
        if not r13_topic_current_fresh(key):
            return [("resident_lamplighter", "제가 본 일은 말씀드린 그대로예요. 더 확인할 것이 있으면 물어보세요.", {"expression":"anxious"})]
        if key == "lamplighter_guarded":
            rows = [("dad", "피코가 발견된 3번 등 이야기를 여쭙겠습니다.")]
            if r13_has("L16"):
                rows += [("resident_lamplighter", "동튼 뒤에 다시 보니 등 안이 비어 있었어요. 그때 피코를 발견했어요.", {"expression":"anxious"})]
            elif r13_has("L06"):
                rows += [("resident_lamplighter", "새벽에 돌 때만 해도 등은 미지근했어요. 분명히요.", {"expression":"anxious"})]
            else:
                rows += [("resident_lamplighter", "그 등에서 무슨 일이 있었는지 저도 알고 싶어요.", {"expression":"anxious"})]
            rows += [("dad", "직접 보신 일부터 차례로 여쭤보겠습니다.")]
            return rows
        past_rows = (store.room13 or {}).get("topic_transcripts", {}).get(key, [])
        heard_one_round = any(len(row) >= 2 and row[0] == "resident_lamplighter" and "한 바퀴만" in row[1] for row in past_rows)
        question = ("전에 해 지고 한 바퀴만 돈다고 하셨지요. 피코를 발견하던 날에도 그랬습니까?" if heard_one_round
            else "피코를 발견하던 날, 등을 보러 다니신 순서를 여쭤봐도 되겠습니까?")
        rows = [("dad", question)]
        if r13_has("L16"):
            rows += [("resident_lamplighter", "그날은 첫 순찰 뒤에도 다시 돌았어요. 동튼 뒤에 돌아갔을 때 피코를 발견했고요.", {"expression":"anxious"}),
                ("dad", "그날 밤의 순찰과 동튼 뒤의 발견을 나누어 적겠습니다.")]
        elif r13_has("L15"):
            rows += [("resident_lamplighter", "2일 밤 첫 순찰 때는 받침을 바로잡으려고 뚜껑을 열었어요. 그때는 조각이 안에 있었어요.", {"expression":"anxious"}),
                ("dad", "그 첫 점검 뒤의 일은 따로 여쭤보겠습니다.")]
        elif r13_has("L06"):
            rows += [("resident_lamplighter", "그날은 새벽에도 돌았어요. 그때 3번 등은 아직 미지근했어요.", {"expression":"anxious"}),
                ("dad", "그때 등 안도 직접 보셨는지부터 확인하고 싶습니다.")]
        else:
            rows += [("resident_lamplighter", "제가 본 일을 차례대로 말씀드릴게요.", {"expression":"anxious"})]
        return rows

    _r13_piko_topic_lines = r13_topic_current_lines
    def r13_topic_current_lines(key):
        if r13_piko_chorong_context(key):
            return r13_piko_chorong_lines(key)
        return _r13_piko_topic_lines(key)

    _r13_piko_topic_seen = r13_calendar_topic_seen
    def r13_calendar_topic_seen(key, spec):
        if r13_piko_chorong_context(key):
            return not r13_topic_current_fresh(key)
        return _r13_piko_topic_seen(key, spec)

    _r13_piko_topics = r13_topics
    def r13_topics(person):
        rows = _r13_piko_topics(person)
        if person != "resident_lamplighter" or not r13_has("lt_dawn"):
            return rows
        titles = {"lamplighter_guarded":"꺼진 3번 등에서 확인한 일을 묻는다",
            "smalltalk:lamplighter_check":"피코를 발견하던 날의 순찰을 묻는다"}
        return [(key, dict(spec, title=titles[key]) if key in titles else spec) for key, spec in rows]

label r13_piko_notice(recovery=False):
    if not r13_piko_notice_here():
        return
    call r13_here_scene
    call r13_lines(r13_piko_notice_lines(recovery), "ep1:piko:notice:v1", binding_route="dynamic:805")
    # No evidence, time, result or archive mutation. Interrupted saves resume the label.
    $ r13_flag("lt_q1_notice")
    return
