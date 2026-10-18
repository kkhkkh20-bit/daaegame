# E18 disclosure is already real. Dad's answer and the next question are not
# chosen for the player. Reuse the existing topic dispatch and its grant timing.
init 191 python:
    def r13_granny_warning_asked(person,key,rows):
        return (person=="granny" and key=="E18" and r13_has("E18") and
            any(row[0]=="granny" and row[1]=="그분이 아직 연락을 하고 있었군요. 어디서 받았어요?" for row in rows))

    def r13_granny_warning_followup():
        # Query the final topic chain. Do not invent the comparison, bypass dates,
        # award J06 early, or replay an archived answer as fresh testimony.
        available={key for key,spec in r13_topics("granny")}
        read=(store.room13 or {}).get("read_topics",[])
        for key in ("poc:granny_letter","granny_letter"):
            if key in available and key not in read:
                return key
        return None

    def r13_granny_warning_source_known():
        # Knowing the box location is not proof Dad collected this envelope there.
        # Both real pickup routes commit their activity key only on completion.
        s=store.room13 or {}
        return "E18" in s.get("evidence",[]) and any(key in s.get("done",[]) for key in ("warning","warning_keep"))

label r13_granny_warning_reply:
    $ r13_granny_reply_topic=r13_granny_warning_followup()
    menu:
        "광장 등 밑 점검함에서 꺼냈다고 말한다" if r13_granny_warning_source_known():
            $ r13_flag("warning_source_exposed")
            call r13_lines([("dad","광장 등 밑 점검함에서 꺼냈습니다."),("granny","광장에 있었군요. 나도 부인 소식을 기다리고 있어요.",{"expression":"neutral"})],"present:granny:E18:source")
            return None
        "어디서 받았는지 왜 궁금한지 되묻는다":
            call r13_lines([("dad","어디서 받았는지는 왜 궁금하십니까?"),("granny","나도 부인 소식을 기다리고 있으니까요. 어디에 소식을 남겼는지 궁금해서요.",{"expression":"neutral"})],"present:granny:E18:why")
            return None
        "받은 곳은 밝히지 않고 초대 편지에 관해 묻는다" if r13_granny_reply_topic:
            call r13_lines([("dad","장소까지 말씀드리지는 않겠습니다.")],"present:granny:E18:withhold")
            return r13_granny_reply_topic
        "받은 곳은 밝히지 않고 다른 질문을 고른다":
            call r13_lines([("dad","장소까지 말씀드리지는 않겠습니다.")],"present:granny:E18:withhold:other")
            return None
        "봉투를 거두고 대화를 마친다":
            return "back"
